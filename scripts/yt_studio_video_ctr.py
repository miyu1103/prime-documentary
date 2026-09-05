#!/usr/bin/env python
"""PER-VIDEO thumbnail impressions/CTR from YouTube Studio internals (read-only).

`yt_studio_ctr.py` (channel-level) の姉妹スクリプト。同じ cookie/SAPISIDHASH 認証を
再利用し、(1) `creator/list_creator_videos` で全アップロードを列挙、(2) 動画ごとに
`yta_web/get_screen` を `ANALYTICS_TAB_ID_REACH` + entity={videoId} で叩いて
VIDEO_THUMBNAIL_IMPRESSIONS / _VTR を抽出する（実測 2026-07-25 で動作確認）。

- 読み取り専用。書き込み・設定変更は一切しない。cookie を stdout に出さない。
- 期間はStudioデフォルト（28日）。period パラメータはサーバ側で無視される（実測）。
- 非公式エンドポイント前提の注意は yt_studio_ctr.py と同じ。

出力: scripts/_yt_studio_video_ctr.json（全動画の impressions/ctr/vtr 配列、CTR降順）
使い方: py -3.11 scripts/yt_studio_video_ctr.py [--limit N]
"""
from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import yt_studio_ctr as Y  # 認証・定数・抽出を単一ソースとして再利用

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

OUT = Path(__file__).resolve().parent / "_yt_studio_video_ctr.json"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36")


def _post(jar: dict, cookie_str: str, endpoint: str, payload: dict, referer: str):
    headers = {
        "authorization": Y.auth_header(jar),
        "content-type": "application/json",
        "cookie": cookie_str,
        "origin": Y.ORIGIN,
        "x-origin": Y.ORIGIN,
        "referer": referer,
        "x-goog-authuser": "0",
        "x-youtube-client-name": str(Y.CLIENT_NAME),
        "x-youtube-client-version": Y.CLIENT_VERSION,
        "x-youtube-delegation-context": Y.SERIALIZED_DELEGATION,
        "user-agent": UA,
    }
    req = urllib.request.Request(f"{Y.ORIGIN}/youtubei/v1/{endpoint}?alt=json",
                                 data=json.dumps(payload).encode(), method="POST", headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=45) as r:
            return r.status, json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, {"_error_body": e.read().decode()[:300]}


def _ctx() -> dict:
    return {
        "client": {"clientName": Y.CLIENT_NAME, "clientVersion": Y.CLIENT_VERSION,
                   "hl": "en", "gl": "JP", "utcOffsetMinutes": Y.UTC_OFFSET_MIN},
        "request": {"returnLogEntry": True, "internalExperimentFlags": []},
        "user": {"delegationContext": {"externalChannelId": Y.CHANNEL_ID,
                                       "roleType": {"channelRoleType": "CREATOR_CHANNEL_ROLE_TYPE_OWNER"}},
                 "serializedDelegationContext": Y.SERIALIZED_DELEGATION},
    }


def list_uploads(jar: dict, cookie_str: str) -> list[dict]:
    """全アップロードの videoId/title/status/lengthSeconds を列挙（ページング対応）。"""
    videos: list[dict] = []
    page_token = None
    while True:
        payload: dict = {
            "context": _ctx(),
            "pageSize": 50,
            "mask": {"videoId": True, "title": True, "timeCreatedSeconds": True,
                     "status": True, "lengthSeconds": True},
            "filter": {"and": {"operands": [
                {"channelIdIs": {"value": Y.CHANNEL_ID}},
                {"videoOriginIs": {"value": "VIDEO_ORIGIN_UPLOAD"}},
            ]}},
            "order": "VIDEO_ORDER_DISPLAY_TIME_DESC",
        }
        if page_token:
            payload["pageToken"] = page_token
        st, body = _post(jar, cookie_str, "creator/list_creator_videos", payload,
                         f"{Y.ORIGIN}/channel/{Y.CHANNEL_ID}/videos")
        if st != 200:
            sys.exit(f"list_creator_videos HTTP {st}: {str(body)[:200]}")
        videos += body.get("videos", [])
        page_token = body.get("nextPageToken")
        if not page_token:
            return videos


def video_reach(jar: dict, cookie_str: str, video_id: str) -> dict:
    payload = Y.build_payload("ANALYTICS_TAB_ID_REACH")
    payload["screenConfig"]["entity"] = {"videoId": video_id}
    st, body = _post(jar, cookie_str, "yta_web/get_screen", payload,
                     f"{Y.ORIGIN}/video/{video_id}/analytics/tab-reach_viewers/period-default")
    if st != 200:
        return {"error": f"HTTP {st}"}
    agg: dict = {}
    for t, v, _u in Y.extract_metrics(body):
        # 同一typeは最大値（合計行）を採用 — yt_studio_ctr.py と同じ流儀
        if t not in agg or (isinstance(v, (int, float)) and v > agg[t]):
            agg[t] = v
    keep = ("VIDEO_THUMBNAIL_IMPRESSIONS", "VIDEO_THUMBNAIL_IMPRESSIONS_VTR",
            "AVERAGE_WATCH_TIME_FROM_VIDEO_THUMBNAIL_IMPRESSIONS",
            "SHORTS_FEED_IMPRESSIONS", "SHORTS_FEED_IMPRESSIONS_VTR", "EXTERNAL_VIEWS")
    return {k: agg[k] for k in keep if k in agg}



def _guard_and_write(out_path, payload):
    """Never clobber a good baseline with an empty pull (cookie-rotation guard).

    Added 2026-07-28 after a mid-run cookie rotation returned imp=None for all
    106 rows and overwrote the only copy of the 7/25 baseline. Rules:
      * if every row lacks impressions -> refuse to write, keep the old file
      * always ALSO write a dated snapshot so a baseline can never be lost again
    """
    import json, datetime, pathlib as _pl
    rows = payload.get("rows", [])
    has_data = any(isinstance(r.get("VIDEO_THUMBNAIL_IMPRESSIONS"), (int, float)) for r in rows)
    out = _pl.Path(out_path)
    if not has_data:
        print(f"REFUSED to overwrite {out.name}: 0/{len(rows)} rows carry impressions "
              f"(cookie rotated?). Existing baseline preserved.")
        return False
    dated = out.with_name(f"{out.stem}.{datetime.date.today():%Y%m%d}{out.suffix}")
    dated.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote {out.name} + snapshot {dated.name} rows={len(rows)}")
    return True

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0, help="先頭N本だけ（デバッグ用）")
    args = ap.parse_args()

    cookie_str = Y.load_cookie_string()
    jar = Y.parse_cookies(cookie_str)

    uploads = list_uploads(jar, cookie_str)
    print(f"uploads listed: {len(uploads)}")
    if args.limit:
        uploads = uploads[: args.limit]

    rows: list[dict] = []
    for i, v in enumerate(uploads, 1):
        vid = v["videoId"]
        privacy = str(v.get("status", "")).replace("VIDEO_STATUS_", "")
        m = video_reach(jar, cookie_str, vid)
        rows.append({"video_id": vid, "title": v.get("title", ""), "privacy": privacy,
                     "length_seconds": int(v.get("lengthSeconds", 0) or 0), **m})
        imp = m.get("VIDEO_THUMBNAIL_IMPRESSIONS")
        ctr = m.get("VIDEO_THUMBNAIL_IMPRESSIONS_VTR")
        print(f"  [{i}/{len(uploads)}] {vid} imp={imp} ctr={ctr} {v.get('title','')[:48]}")
        time.sleep(0.25)

    rows.sort(key=lambda r: (r.get("VIDEO_THUMBNAIL_IMPRESSIONS_VTR") is None,
                             -(r.get("VIDEO_THUMBNAIL_IMPRESSIONS_VTR") or 0)))
    ok = _guard_and_write(OUT, {"period": "studio-default(28d)",
                                "generated_at_note": "see file mtime", "rows": rows})
    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
