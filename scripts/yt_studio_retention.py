#!/usr/bin/env python
"""PER-VIDEO audience-retention curves — Studio internals + official API (read-only).

============================ COOKIE-WINDOW RUNBOOK ============================
Studio cookie は 10〜60 分でローテーションする。書き出したら「数分以内に」全部走らせる:
  1. owner: Studio → DevTools → Network → 任意の get_screen → Copy as cURL →
     `-b` の中身を secrets/studio_cookies.txt へ上書き保存
  2. py -3.11 scripts/yt_studio_ctr.py            (チャンネルCTR)
  3. py -3.11 scripts/yt_studio_video_ctr.py      (動画別CTR)
  4. py -3.11 scripts/yt_studio_retention.py      (本スクリプト・リテンション)
  5. どれかが 401 を出したら = cookie rotated — re-export and run within minutes
     (step 1 からやり直し。ハッシュは毎回再計算されるので cookie だけ差し替えれば良い)
  6. 初回の Studio 実行後は _yt_retention_raw/ の生JSONを見てパーサを直す前提
===============================================================================

姉妹スクリプト yt_studio_ctr.py / yt_studio_video_ctr.py と同じ cookie/SAPISIDHASH
認証・同じ定数を再利用する。2 つのソースを持つ:

  --source studio (default)
      (1) `creator/list_creator_videos` で全アップロード列挙（実証済みの形）、
      (2) 各長尺につき `yta_web/get_screen` を tabId=ANALYTICS_TAB_ID_ENGAGEMENT
          + screenConfig.entity={videoId} で叩き、
      (3) パースに関係なく生JSONを scripts/_yt_retention_raw/<videoId>.json へ
          必ずダンプする（初回ライブ実行 1 回でパーサを修正できるように）。
      (4) 曲線が拾えなければ `yta_web/get_cards` (audienceRetention card 推測形)
          も試し、同様に <videoId>.cards.json へダンプする。

  --source api
      公式 YouTube Analytics API v2（yt_hook_health.py で実証済みの形）:
      metrics=audienceWatchRatio,relativeRetentionPerformance
      dimensions=elapsedVideoTimeRatio, filters=video==ID。
      cookie 不要（.env の OAuth refresh token）。フル曲線が取れる実証済みの経路。

CONFIDENCE (正直な自己評価):
  - list_creator_videos / get_screen(entity=videoId) の request 形: HIGH
    （yt_studio_video_ctr.py が 2026-07-25 に REACH タブで実測動作）
  - tabId "ANALYTICS_TAB_ID_ENGAGEMENT" の文字列: MEDIUM-HIGH
    （CONTENT / REACH と同じ命名規約。Studio の URL は tab-interest_viewers）
  - ENGAGEMENT screen 応答に AUDIENCE_WATCH_RATIO のフル values 配列が入るか: MEDIUM
    （REACH 応答は {"metric":{"type":X},"percentages":{"values":[...]}} 形で
      values が時系列になるのは実測済み。retention 曲線が同形で来る保証は無い）
  - get_cards の request body 形: LOW（推測。失敗しても生ダンプでエラー本文を残す）
  → だからこそ「生JSON必須ダンプ + 多段パースfallback + --dry-run」で、
    ライブ 1 回でパーサを確定できる構えにしてある。

出力:
  scripts/_yt_retention_curves.json   正規化曲線 {pos(0..1) → watch_ratio[, rel_perf]}
  scripts/_yt_retention_raw/<id>.json Studio 生応答（studio ソース時のみ・必須ダンプ）

使い方:
  py -3.11 scripts/yt_studio_retention.py                     # studio・全長尺
  py -3.11 scripts/yt_studio_retention.py --videos a,b,c      # 対象を限定
  py -3.11 scripts/yt_studio_retention.py --source api        # 公式API(cookie不要)
  py -3.11 scripts/yt_studio_retention.py --dry-run           # request body 表示のみ

読み取り専用。書き込み・設定変更・公開操作は一切しない。cookie/token は出力しない。
"""
from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import yt_studio_ctr as Y          # 認証・定数・payload を単一ソースとして再利用
import yt_studio_video_ctr as V    # _post / list_uploads を再利用（二重実装しない）

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

SCRIPTS = Path(__file__).resolve().parent
OUT = SCRIPTS / "_yt_retention_curves.json"
RAW_DIR = SCRIPTS / "_yt_retention_raw"
LONGFORM_MIN_SEC = 240          # Part B と同じ長尺定義
ENGAGEMENT_TAB = "ANALYTICS_TAB_ID_ENGAGEMENT"
RETENTION_METRICS = ("AUDIENCE_WATCH_RATIO", "RELATIVE_RETENTION_PERFORMANCE")


# ---------------------------------------------------------------- payloads --
def engagement_payload(video_id: str) -> dict:
    p = Y.build_payload(ENGAGEMENT_TAB)
    p["screenConfig"]["entity"] = {"videoId": video_id}
    return p


def cards_payload(video_id: str) -> dict:
    """`yta_web/get_cards` の推測 body（CONFIDENCE LOW — 失敗前提の第二射）。

    Studio の retention チャートはカード単位で取得される。cardConfig 系の命名は
    get_screen と同じ規約と仮定した最小形。401/400 でも応答本文をダンプする。
    """
    return {
        "context": Y.build_payload(ENGAGEMENT_TAB)["context"],
        "screenConfig": {
            "entity": {"videoId": video_id},
            "currency": "USD",
            "timeZoneOffsetSecs": Y.UTC_OFFSET_MIN * 60,
        },
        "desktopState": {"tabId": ENGAGEMENT_TAB},
        "cards": [{
            "audienceRetention": {
                "metrics": list(RETENTION_METRICS),
                "dimension": "ELAPSED_VIDEO_TIME_PERCENTAGE",
            },
        }],
    }


# ----------------------------------------------------------------- parsing --
def find_metric_series(obj) -> dict[str, list]:
    """応答内の retention 系 metric の「最長の values 配列」を type 別に拾う。

    第一候補の形（REACH 実測と同形と仮定）:
      {"metric": {"type": "AUDIENCE_WATCH_RATIO"}, "percentages": {"values": [...]}}
    values/counts/milliseconds いずれのコンテナも許容し、最長配列を曲線とみなす。
    """
    best: dict[str, list] = {}

    def walk(o):
        if isinstance(o, dict):
            m = o.get("metric")
            if isinstance(m, dict) and m.get("type") in RETENTION_METRICS:
                for k in ("percentages", "values", "counts", "milliseconds", "ratios"):
                    c = o.get(k)
                    vals = c.get("values") if isinstance(c, dict) else (c if isinstance(c, list) else None)
                    if isinstance(vals, list) and len(vals) > len(best.get(m["type"], [])):
                        best[m["type"]] = vals
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)

    walk(obj)
    return best


def find_generic_curves(obj) -> list[list]:
    """fallback: (x,y) 点列っぽい配列を総当たりで拾う（key 名は不問）。

    「長さ>=20 の dict 配列で、各要素が数値 2 個以上を持ち、第1数値が単調増加で
    0..100 か 0..1 に収まる」ものを曲線候補とする。
    """
    curves: list[list] = []

    def nums(d: dict) -> list[float]:
        return [v for v in d.values() if isinstance(v, (int, float))]

    def walk(o):
        if isinstance(o, list) and len(o) >= 20 and all(isinstance(e, dict) for e in o):
            pts = [nums(e) for e in o]
            if all(len(p) >= 2 for p in pts):
                xs = [p[0] for p in pts]
                if xs == sorted(xs) and 0 <= xs[0] and xs[-1] <= 100:
                    curves.append([[p[0], p[1]] for p in pts])
        if isinstance(o, dict):
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)

    walk(obj)
    return curves


def normalize(series: dict[str, list], generic: list[list]) -> tuple[list[dict], str]:
    """→ ([{pos, watch_ratio[, rel_perf]}...], parse_status)"""
    watch = series.get("AUDIENCE_WATCH_RATIO")
    rel = series.get("RELATIVE_RETENTION_PERFORMANCE")
    if watch and len(watch) >= 5:
        n = len(watch)
        pts = []
        for i, w in enumerate(watch):
            p = {"pos": round(i / max(n - 1, 1), 4),
                 "watch_ratio": round(w / 100, 4) if w and w > 1.5 else (round(w, 4) if w is not None else None)}
            if rel and i < len(rel) and rel[i] is not None:
                p["rel_perf"] = round(rel[i] / 100, 4) if rel[i] > 1.5 else round(rel[i], 4)
            pts.append(p)
        return pts, "ok:metric_series"
    if generic:
        curve = max(generic, key=len)
        xmax = curve[-1][0] or 1
        ymax = max((y for _x, y in curve), default=1) or 1
        pts = [{"pos": round(x / xmax, 4),
                "watch_ratio": round(y / (100 if ymax > 1.5 else 1), 4)} for x, y in curve]
        return pts, "ok:generic_curve(VERIFY_ME)"
    return [], "raw_dumped_only"


# ----------------------------------------------------------------- sources --
def fetch_studio(videos: list[dict], sleep_s: float = 0.3) -> list[dict]:
    cookie_str = Y.load_cookie_string()
    jar = Y.parse_cookies(cookie_str)
    RAW_DIR.mkdir(exist_ok=True)
    out = []
    for i, v in enumerate(videos, 1):
        vid = v["video_id"]
        st, body = V._post(jar, cookie_str, "yta_web/get_screen", engagement_payload(vid),
                           f"{Y.ORIGIN}/video/{vid}/analytics/tab-interest_viewers/period-default")
        (RAW_DIR / f"{vid}.json").write_text(
            json.dumps(body, ensure_ascii=False, indent=1), encoding="utf-8")
        if st == 401:
            sys.exit("HTTP 401: cookie rotated -- re-export and run within minutes")
        series, generic, status = {}, [], f"http_{st}"
        if st == 200:
            series = find_metric_series(body)
            generic = [] if series.get("AUDIENCE_WATCH_RATIO") else find_generic_curves(body)
        pts, status = normalize(series, generic) if st == 200 else ([], status)
        if st == 200 and not pts:
            # 第二射: get_cards（推測形）。結果は成否に関わらずダンプ。
            st2, body2 = V._post(jar, cookie_str, "yta_web/get_cards", cards_payload(vid),
                                 f"{Y.ORIGIN}/video/{vid}/analytics/tab-interest_viewers/period-default")
            (RAW_DIR / f"{vid}.cards.json").write_text(
                json.dumps(body2, ensure_ascii=False, indent=1), encoding="utf-8")
            if st2 == 200:
                pts, status = normalize(find_metric_series(body2), find_generic_curves(body2))
                status += "(via get_cards)"
        out.append({"video_id": vid, "title": v.get("title", ""),
                    "length_seconds": v.get("length_seconds", 0),
                    "parse_status": status, "points": pts})
        print(f"  [{i}/{len(videos)}] {vid} {status} pts={len(pts)} {v.get('title','')[:44]}")
        time.sleep(sleep_s)
    return out


def fetch_api(videos: list[dict], start: str, end: str) -> list[dict]:
    """公式 Analytics API（yt_hook_health.py と同じ実証済みの形）。cookie 不要。"""
    import yt_hook_health as H
    token = H.access_token(H.load_env())
    out = []
    for i, v in enumerate(videos, 1):
        vid = v["video_id"]
        rows = H.retention_curve(token, vid, start, end)   # [elapsedRatio, watch, relPerf]
        pts = [{"pos": r[0], "watch_ratio": r[1],
                **({"rel_perf": r[2]} if len(r) > 2 and r[2] is not None else {})} for r in rows]
        out.append({"video_id": vid, "title": v.get("title", ""),
                    "length_seconds": v.get("length_seconds", 0),
                    "parse_status": "ok:official_api" if pts else "no_rows",
                    "points": pts})
        print(f"  [{i}/{len(videos)}] {vid} pts={len(pts)} {v.get('title','')[:48]}")
        time.sleep(0.15)
    return out


def enumerate_longforms() -> list[dict]:
    """studio: list_creator_videos で列挙。失敗時は README 通り 401 メッセージ。"""
    cookie_str = Y.load_cookie_string()
    jar = Y.parse_cookies(cookie_str)
    try:
        uploads = V.list_uploads(jar, cookie_str)
    except SystemExit as e:
        if "401" in str(e):
            sys.exit("HTTP 401: cookie rotated -- re-export and run within minutes")
        raise
    return [{"video_id": u["videoId"], "title": u.get("title", ""),
             "length_seconds": int(u.get("lengthSeconds", 0) or 0)}
            for u in uploads if int(u.get("lengthSeconds", 0) or 0) >= LONGFORM_MIN_SEC]


def enumerate_longforms_from_cache() -> list[dict]:
    """api ソース/dry-run 用: 直近の _yt_studio_video_ctr.json から列挙（通信不要）。"""
    f = SCRIPTS / "_yt_studio_video_ctr.json"
    rows = json.loads(f.read_text(encoding="utf-8"))["rows"]
    return [{"video_id": r["video_id"], "title": r.get("title", ""),
             "length_seconds": r.get("length_seconds", 0)}
            for r in rows if r.get("length_seconds", 0) >= LONGFORM_MIN_SEC]


# -------------------------------------------------------------------- main --
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--source", choices=("studio", "api"), default="studio")
    ap.add_argument("--videos", help="comma-separated video IDs (skip enumeration)")
    ap.add_argument("--start", default="2026-06-01", help="api source: start date")
    ap.add_argument("--end", default=date.today().isoformat(), help="api source: end date")
    ap.add_argument("--limit", type=int, default=0, help="先頭N本だけ（デバッグ用）")
    ap.add_argument("--dry-run", action="store_true",
                    help="request body を表示するだけ（通信しない）")
    args = ap.parse_args()

    if args.dry_run:
        vid = (args.videos or "VIDEO_ID_HERE").split(",")[0]
        print("== creator/list_creator_videos body (proven shape) ==")
        # yt_studio_video_ctr.list_uploads と同一 — page 1 の body を再構成して表示
        print(json.dumps({"context": V._ctx(), "pageSize": 50,
                          "mask": {"videoId": True, "title": True, "timeCreatedSeconds": True,
                                   "status": True, "lengthSeconds": True},
                          "filter": {"and": {"operands": [
                              {"channelIdIs": {"value": Y.CHANNEL_ID}},
                              {"videoOriginIs": {"value": "VIDEO_ORIGIN_UPLOAD"}}]}},
                          "order": "VIDEO_ORDER_DISPLAY_TIME_DESC"}, indent=2))
        print(f"\n== yta_web/get_screen body (tab={ENGAGEMENT_TAB}, entity=videoId) ==")
        print(json.dumps(engagement_payload(vid), indent=2))
        print("\n== yta_web/get_cards body (GUESS — confidence LOW) ==")
        print(json.dumps(cards_payload(vid), indent=2))
        print("\n== official API request (proven, --source api) ==")
        print("GET https://youtubeanalytics.googleapis.com/v2/reports?" + urllib.parse.urlencode({
            "ids": "channel==MINE", "startDate": args.start, "endDate": args.end,
            "metrics": "audienceWatchRatio,relativeRetentionPerformance",
            "dimensions": "elapsedVideoTimeRatio", "filters": "video==" + vid}))
        return 0

    if args.videos:
        cache = {v["video_id"]: v for v in enumerate_longforms_from_cache()}
        videos = [cache.get(x, {"video_id": x, "title": "", "length_seconds": 0})
                  for x in args.videos.split(",") if x]
    elif args.source == "api":
        videos = enumerate_longforms_from_cache()
    else:
        videos = enumerate_longforms()
    if args.limit:
        videos = videos[: args.limit]
    print(f"long-form videos to fetch: {len(videos)} (source={args.source})")

    curves = fetch_api(videos, args.start, args.end) if args.source == "api" \
        else fetch_studio(videos)

    payload = {"source": args.source,
               "window": f"{args.start} .. {args.end}" if args.source == "api"
                         else "studio-default(28d)",
               "note": "pos = elapsed position 0..1; watch_ratio = fraction of starters "
                       "still watching; rel_perf 0.5 = peer median",
               "videos": curves}
    tmp = OUT.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
    tmp.replace(OUT)
    ok = sum(1 for c in curves if c["points"])
    print(f"\nwrote {OUT.name}: curves for {ok}/{len(curves)} videos")
    if args.source == "studio" and ok < len(curves):
        print(f"raw responses dumped to {RAW_DIR.name}/ — fix parser from one live run")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
