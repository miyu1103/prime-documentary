#!/usr/bin/env bash
# Render the TikTok-composed cover for every Short that has a TikTok render but no cover yet.
#
# TikTok picks its own frame when no cover is set, and this channel's Shorts open on a near-black
# one - the profile was a wall of identical black tiles. The cover cannot be changed after posting,
# so every queued Short needs one before it goes up.
#
# The background images live in remotion/public; public_min is a pruned mirror and the still fails
# with a 404 if the background was never mirrored. This copies what it needs first.
set -uo pipefail
cd "$(dirname "$0")/.." || exit 1
BUNDLE="${TEMP:-/tmp}/pd_cov"

need=$(py -3.11 - <<'PY'
import re
from pathlib import Path
out = Path("remotion/out")
tt = {int(re.match(r"short(\d+)_tt", p.stem).group(1)) for p in out.glob("short*_tt.mp4")}
cov = {int(re.match(r"short(\d+)_ttcover", p.stem).group(1)) for p in out.glob("short*_ttcover.png")}
print(" ".join(str(n) for n in sorted(tt - cov)))
PY
)
[ -z "$need" ] && { echo "every TikTok render already has a cover"; exit 0; }
echo "covers to render: $need"

py -3.11 - <<'PY'
import re, shutil
from pathlib import Path
src = Path("remotion/src/Root.tsx").read_text(encoding="utf-8")
pub, mini = Path("remotion/public"), Path("remotion/public_min")
n = 0
for m in re.finditer(r'id="ShortThumb-short(\d+)"(.{0,900}?)/>', src, re.S):
    b = re.search(r"backgroundSrc:\s*'([^']+)'", m.group(2))
    if not b:
        continue
    s, d = pub / b.group(1), mini / b.group(1)
    if s.exists() and not d.exists():
        d.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(s, d)
        n += 1
print(f"mirrored {n} background(s)")
PY

rm -rf "$BUNDLE"
( cd remotion && npx remotion bundle --public-dir=./public_min --out-dir "$BUNDLE" 2>&1 \
    | grep -vE "^ +at |Bundling [0-9]" | tail -1 )
[ -f "$BUNDLE/index.html" ] || { echo "BUNDLE FAILED"; exit 1; }

ok=0; fail=0
for n in $need; do
  if ( cd remotion && npx remotion still "$BUNDLE" "ShortThumb-short${n}" "out/short${n}_ttcover.png" \
         --props='{"layout":"tt"}' >/dev/null 2>&1 ) && [ -f "remotion/out/short${n}_ttcover.png" ]; then
    ok=$((ok+1))
  else
    echo "  FAIL short${n}"; fail=$((fail+1))
  fi
done
rm -rf "$BUNDLE"
echo "TT_COVERS_DONE ok=$ok fail=$fail  total=$(ls remotion/out/short*_ttcover.png | wc -l)"
