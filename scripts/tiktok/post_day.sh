#!/usr/bin/env bash
# One day's TikTok posting. This wrapper exists for one reason: node resolves modules from the
# SCRIPT's directory, not the working directory, and puppeteer-core lives in
# C:/temp/studio_auto/node_modules. When schedule_shorts_tiktok.js moved into this repository it
# stopped being able to find it, and every invocation died with MODULE_NOT_FOUND before touching
# the browser. NODE_PATH is what makes the repository copy runnable.
#
# Usage:
#   bash scripts/tiktok/post_day.sh 2026-08-17        # 4 posts, the standing cadence
#   bash scripts/tiktok/post_day.sh 2026-08-17 0 2    # start day, slots already used, max posts
#
# Before it runs it checks the two things that cannot be repaired after a post goes out:
# the browser is up on the dedicated profile, and every queued row still has its cover file.
set -uo pipefail
cd "$(dirname "$0")/../.." || exit 1

DAY="${1:?first argument must be the start date, YYYY-MM-DD}"
SKIP="${2:-0}"
MAX="${3:-4}"

STUDIO=C:/temp/studio_auto
export NODE_PATH="$STUDIO/node_modules"

curl -s --max-time 5 http://127.0.0.1:9222/json/version > /dev/null || {
  echo "FAIL: no browser on port 9222. Run: node scripts/tiktok/start_chrome.js  (log in by hand once)"
  exit 1
}

# WHICH ACCOUNT. On 2026-08-16 three videos went to the abandoned account because the browser was
# signed into two and the poster never asked. The profile page said one thing and TikTok Studio -
# the surface that actually uploads - was operating the other. Never post without matching this.
EXPECT="${TIKTOK_ACCOUNT:-prime.documentary1}"
ACTUAL="$(node scripts/tiktok/whoami.js 2>/dev/null | tail -1)"
if [ "$ACTUAL" != "$EXPECT" ]; then
  echo "REFUSING: TikTok Studio is operating \"$ACTUAL\", expected \"$EXPECT\"."
  echo "  Log the dedicated Chrome profile into $EXPECT, or set TIKTOK_ACCOUNT to override."
  exit 1
fi
echo "studio account confirmed: $ACTUAL"

py -3.11 - <<'PY' || exit 1
import json, sys
from pathlib import Path
rows = json.loads(Path("C:/temp/studio_auto/tt_queue.json").read_text(encoding="utf-8"))
bad = [r["short"] for r in rows if not r.get("cover") or not Path(r["cover"]).exists()]
missing = [r["short"] for r in rows if not Path(r["file"]).exists()]
print(f"queue={len(rows)} without-cover={len(bad)} missing-video={len(missing)}")
if bad or missing:
    print("REFUSING: a post without a cover can never be given one afterwards.")
    print("  without cover:", bad[:10])
    print("  missing video:", missing[:10])
    sys.exit(1)
PY

# The account, not the ledger, decides what has already gone out. A run that dies mid-upload
# leaves a post on TikTok that the ledger never recorded, and the retry then duplicates it.
py -3.11 scripts/tiktok/reconcile_ledger.py --apply || echo "WARNING: could not reconcile against the account"

echo "posting: day=$DAY skip=$SKIP max=$MAX"
node scripts/tiktok/schedule_shorts_tiktok.js "$DAY" "$SKIP" "$MAX"
rc=$?

echo "--- ledger tail ---"
tail -n "$MAX" "$STUDIO/tt_clean_result.jsonl" 2>/dev/null || echo "(no results recorded)"
exit $rc
