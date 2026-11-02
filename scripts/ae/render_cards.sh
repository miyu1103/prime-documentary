#!/usr/bin/env bash
# Build and render LONG-FORM kinetic cards (1920x1080, alpha) through After Effects, end to end.
#
# Same runner discipline as render_beats.sh, which exists because AE lies about failure: the build
# step reports a script failure only as text in its own log - the process still exits 0 - and
# aerender will then happily re-render whatever the LAST successful build left in kinetic.aep.
# That happened once: a build died on job 1, and two overlays came out at the previous run's
# durations with byte sizes identical to the earlier render, and nothing in any exit code said so.
# This refuses to render unless the build log is clean and the .aep was written by THIS run.
#
# Usage: scripts/ae/render_cards.sh <jobs.json> [id ...]
#   With no ids, every job in the file is built. With ids, only those - which is how a single
#   card is re-cut without re-rendering thirteen good ones.
#
# Installs to remotion/public/<slug>/ae/<id>.webm, slug taken from the job id (keybridge_ae001).
set -euo pipefail

JOBS_SRC="${1:?usage: render_cards.sh <jobs.json> [id ...]}"
shift || true
ONLY="$*"

AE_DIR="C:/temp/ae"
AE="/c/Program Files/Adobe/Adobe After Effects 2026/Support Files/AfterFX.exe"
AR="/c/Program Files/Adobe/Adobe After Effects 2026/Support Files/aerender.exe"
JSX="$(cd "$(dirname "$0")" && pwd)/kinetic_card.jsx"
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"

mkdir -p "$AE_DIR/out"

# Filter the job list to --only ids, and to the kinds this jsx can actually draw. A kind it
# cannot draw must be REFUSED here, loudly: the failure mode otherwise is an empty comp that
# renders as a transparent nothing and composites as if the card were never ordered.
python - "$JOBS_SRC" "$AE_DIR/jobs.json" $ONLY <<'PY'
import json, sys
src, dst = sys.argv[1], sys.argv[2]
only = set(sys.argv[3:])
# The nine kinds ADR-0011 declares, and the exact set kinetic_card.jsx dispatches by name. Adding
# a kind here without adding a `cardX` to the jsx is the failure this guard exists to stop: the
# jsx now THROWS on an unknown kind (-> "FAILED" in the log -> the render below never starts), so
# the two lists cannot drift into a silently empty card. Do not add a name speculatively.
KNOWN = {"hero_number", "title_card", "quote_card", "list_build",
         "comparison", "timeline", "system_map", "map_move", "document_blowup"}
jobs = json.load(open(src, encoding="utf-8"))
if only:
    jobs = [j for j in jobs if j["id"] in only]
    missing = only - {j["id"] for j in jobs}
    if missing:
        sys.exit("no such job id: " + ", ".join(sorted(missing)))
drawable = [j for j in jobs if j.get("kind") in KNOWN]
skipped = [j for j in jobs if j.get("kind") not in KNOWN]
for j in skipped:
    print(f"  SKIP {j['id']}: kind '{j.get('kind')}' has no card in kinetic_card.jsx")
if not drawable:
    sys.exit("nothing to build")
json.dump(drawable, open(dst, "w", encoding="utf-8"), ensure_ascii=False)
print(f"  building {len(drawable)} card(s), skipping {len(skipped)}")
PY

ids=$(python -c "import json,sys;print(' '.join(j['id'] for j in json.load(open(sys.argv[1],encoding='utf-8'))))" "$AE_DIR/jobs.json")
for id in $ids; do rm -f "$AE_DIR/out/$id.avi" "$AE_DIR/out/$id.webm"; done
rm -f "$AE_DIR/kinetic.log" "$AE_DIR/kinetic.aep"

echo "== build =="
# ADR-0011's crash trap: a force-killed AE leaves PriorSafeMode.txt, and the crash-recovery dialog
# then blocks EVERY later launch, including -noui ones -- the process sits there with no window to
# dismiss until it is killed, which leaves the file behind again. Clearing it is the only thing
# that breaks the loop, and it costs nothing when AE exited cleanly.
find "$HOME/AppData/Roaming/Adobe/After Effects" -name "PriorSafeMode*.txt" -delete 2>/dev/null || true

"$AE" -noui -r "$JSX" || true
cat "$AE_DIR/kinetic.log"
grep -q "FAILED" "$AE_DIR/kinetic.log" && { echo "BUILD FAILED - not rendering"; exit 1; }
[ -f "$AE_DIR/kinetic.aep" ] || { echo "no kinetic.aep from this run - not rendering"; exit 1; }

echo "== render =="
"$AR" -project "$AE_DIR/kinetic.aep" 2>&1 | grep -viE "^PROGRESS:  0:00" | tail -4

echo "== webm (VP9 + alpha) =="
for id in $ids; do
  [ -f "$AE_DIR/out/$id.avi" ] || { echo "MISSING $id.avi"; exit 1; }
  ffmpeg -v error -y -i "$AE_DIR/out/$id.avi" \
     -c:v libvpx-vp9 -pix_fmt yuva420p -b:v 0 -crf 26 -auto-alt-ref 0 -row-mt 1 \
     "$AE_DIR/out/$id.webm"
  # alpha_mode=1 is the WebM flag Chrome reads to composite the alpha plane; ffmpeg's own decoder
  # ignores it and will report yuv420p, so this tag is the only check that means anything here.
  am=$(ffprobe -v error -show_entries stream_tags=alpha_mode -of default=nw=1:nk=1 "$AE_DIR/out/$id.webm")
  [ "$am" = "1" ] || { echo "$id.webm HAS NO ALPHA"; exit 1; }
  echo "  $id.webm  $(stat -c%s "$AE_DIR/out/$id.webm") bytes  alpha_mode=$am"

  slug="${id%%_*}"
  dst="$ROOT/remotion/public/$slug/ae"
  [ -d "$ROOT/remotion/public/$slug" ] || { echo "    !! no such episode directory: $slug"; exit 1; }
  mkdir -p "$dst"
  cp "$AE_DIR/out/$id.webm" "$dst/$id.webm"
  echo "    -> $slug/ae/$id.webm"

  # The AVI is an uncompressed intermediate - hundreds of MB for a few seconds. 89 of them once
  # reached 47 GB and took the system drive to 98% full, which is how a render dies mid-copy with
  # ENOSPC. The webm is the deliverable and it is installed and verified above, so it goes now.
  rm -f "$AE_DIR/out/$id.avi"
done
echo "OK"
