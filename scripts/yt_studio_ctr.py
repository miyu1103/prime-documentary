"""YouTube Studio 内部アナリティクスからインプレッション/CTRを取得（読み取り専用）。

公式 YouTube Analytics API は impressions / impressionClickThroughRate を返さない
（2026-07-04 実測で "Unknown identifier" 確認）。この2指標は Studio 内部の
youtubei エンドポイントにしか無いため、オーナーのログイン cookie で取得する。

- 読み取り専用。書き込み・削除・設定変更は一切しない。
- cookie は gitignore 済み `secrets/studio_cookies.txt` から読む。標準出力・ログに出さない。
- SAPISIDHASH は毎回その場の時刻から再計算する（キャプチャ時のハッシュは使い捨て）。
- 非公式エンドポイント＝規約グレー・仕様変更で壊れる前提。壊れたら cookie/version を再取得。

出力: scripts/_yt_studio_ctr.json（生JSON）＋ 標準出力に impression/CTR を抽出表示。
使い方: python scripts/yt_studio_ctr.py
"""
from __future__ import annotations

import hashlib
import json
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[1]
COOKIE_FILE = ROOT / "secrets" / "studio_cookies.txt"
OUT = Path(__file__).resolve().parent / "_yt_studio_ctr.json"

# --- キャプチャ由来の固定値（仕様変更時はここだけ更新） -------------------
CHANNEL_ID = "UCuQPtAz1rca9eJ4xhvX0yKA"
# serializedDelegationContext は channelId のみに依存する不変トークン
SERIALIZED_DELEGATION = "EhhVQ3VRUHRBejFyY2E5ZUo0eGh2WDB5S0EqAggI"
CLIENT_NAME = 62
CLIENT_VERSION = "1.20260815.00.01"  # last_verified_at 2026-08-19 (fresh DevTools capture)
ORIGIN = "https://studio.youtube.com"
ENDPOINT = f"{ORIGIN}/youtubei/v1/yta_web/get_screen?alt=json"
UTC_OFFSET_MIN = 540  # Asia/Tokyo
# --------------------------------------------------------------------------


def load_cookie_string() -> str:
    if not COOKIE_FILE.exists():
        sys.exit(f"cookie file not found: {COOKIE_FILE}\n"
                 "Studio→DevTools→Network の get_screen を Copy as cURL し、-b の中身をここへ。")
    return COOKIE_FILE.read_text(encoding="utf-8").strip()


def parse_cookies(cookie_str: str) -> dict:
    jar = {}
    for part in cookie_str.split(";"):
        part = part.strip()
        if "=" in part:
            k, v = part.split("=", 1)
            jar[k.strip()] = v.strip()
    return jar


def sapisid_hash(sapisid: str, ts: int) -> str:
    raw = f"{ts} {sapisid} {ORIGIN}"
    return hashlib.sha1(raw.encode()).hexdigest()


def auth_header(jar: dict) -> str:
    ts = int(time.time())
    sapisid = jar.get("SAPISID") or jar.get("__Secure-3PAPISID") or jar.get("__Secure-1PAPISID")
    p1 = jar.get("__Secure-1PAPISID", sapisid)
    p3 = jar.get("__Secure-3PAPISID", sapisid)
    if not sapisid:
        sys.exit("SAPISID cookie が見つかりません。cookie を取り直してください。")
    h = sapisid_hash(sapisid, ts)
    h1 = sapisid_hash(p1, ts)
    h3 = sapisid_hash(p3, ts)
    return f"SAPISIDHASH {ts}_{h} SAPISID1PHASH {ts}_{h1} SAPISID3PHASH {ts}_{h3}"


def build_payload(tab_id: str = "ANALYTICS_TAB_ID_CONTENT") -> dict:
    # 巨大な experimentFlags は不要。画面と委任コンテキストの最小構成で叩く。
    return {
        "screenConfig": {
            "entity": {"channelId": CHANNEL_ID},
            "currency": "USD",
            "timeZoneOffsetSecs": UTC_OFFSET_MIN * 60,
        },
        "desktopState": {"tabId": tab_id},
        "fetchingType": "FETCHING_TYPE_FOREGROUND",
        "context": {
            "client": {
                "clientName": CLIENT_NAME,
                "clientVersion": CLIENT_VERSION,
                "hl": "en",
                "gl": "JP",
                "utcOffsetMinutes": UTC_OFFSET_MIN,
                "userInterfaceTheme": "USER_INTERFACE_THEME_LIGHT",
            },
            "request": {"returnLogEntry": True, "internalExperimentFlags": []},
            "user": {
                "delegationContext": {
                    "externalChannelId": CHANNEL_ID,
                    "roleType": {"channelRoleType": "CREATOR_CHANNEL_ROLE_TYPE_OWNER"},
                },
                "serializedDelegationContext": SERIALIZED_DELEGATION,
            },
        },
    }


def post(jar: dict, cookie_str: str, payload: dict):
    headers = {
        "authorization": auth_header(jar),
        "content-type": "application/json",
        "cookie": cookie_str,
        "origin": ORIGIN,
        "x-origin": ORIGIN,
        "referer": f"{ORIGIN}/channel/{CHANNEL_ID}/analytics/tab-content/period-default",
        "x-goog-authuser": "0",
        "x-youtube-client-name": str(CLIENT_NAME),
        "x-youtube-client-version": CLIENT_VERSION,
        "x-youtube-delegation-context": SERIALIZED_DELEGATION,
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36",
    }
    data = json.dumps(payload).encode()
    req = urllib.request.Request(ENDPOINT, data=data, method="POST", headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=45) as r:
            return r.status, json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, {"_error_body": e.read().decode()[:500]}


UNIT_KEYS = {"counts": "count", "percentages": "%", "milliseconds": "ms", "values": "num"}


def extract_metrics(obj):
    """{"metric":{"type":X}, "counts"/"percentages"/"milliseconds":{"values":[...]}} を type→値で集める。"""
    out = []

    def walk(o):
        if isinstance(o, dict):
            m = o.get("metric")
            if isinstance(m, dict) and "type" in m:
                for uk, unit in UNIT_KEYS.items():
                    cont = o.get(uk)
                    if isinstance(cont, dict) and isinstance(cont.get("values"), list) and cont["values"]:
                        out.append((m["type"], cont["values"][0], unit))
                        break
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)

    walk(obj)
    return out


def main():
    cookie_str = load_cookie_string()
    jar = parse_cookies(cookie_str)
    status, body = post(jar, cookie_str, build_payload())
    OUT.write_text(json.dumps(body, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"HTTP {status}  → wrote {OUT.name} ({OUT.stat().st_size} bytes)")
    if status != 200:
        print("FAILED:", str(body)[:300])
        return 2
    metrics = extract_metrics(body)
    # 見出し指標を集約（同一typeは最大値=チャンネル合計を採用）
    agg = {}
    for t, v, unit in metrics:
        if t not in agg or (unit == "count" and v > agg[t][0]):
            agg[t] = (v, unit)

    def g(name):
        return agg.get(name, (None, ""))[0]

    imp = g("VIDEO_THUMBNAIL_IMPRESSIONS")
    ctr = g("VIDEO_THUMBNAIL_IMPRESSIONS_VTR")
    shorts_vtr = g("SHORTS_FEED_IMPRESSIONS_VTR")
    awt_ms = g("AVERAGE_WATCH_TIME_FROM_VIDEO_THUMBNAIL_IMPRESSIONS")
    print("\n=== STUDIO KEY METRICS (default period) ===")
    print(f"  サムネ インプレッション : {imp}")
    print(f"  サムネ CTR (VTR)        : {ctr}%   ← 良好=4-6%+")
    print(f"  Shortsフィード VTR      : {shorts_vtr}%")
    if awt_ms:
        print(f"  サムネ経由 平均視聴     : {round(awt_ms/1000)}秒")
    summary = {"thumbnail_impressions": imp, "thumbnail_ctr_pct": ctr,
               "shorts_feed_vtr_pct": shorts_vtr,
               "avg_watch_from_impressions_sec": round(awt_ms/1000) if awt_ms else None,
               "all_metrics": [{"type": t, "value": v, "unit": u} for t, v, u in metrics]}
    (OUT.with_name("_yt_studio_ctr_summary.json")).write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print("  → _yt_studio_ctr_summary.json に集約を書き出し")
    return 0


if __name__ == "__main__":
    sys.exit(main())
