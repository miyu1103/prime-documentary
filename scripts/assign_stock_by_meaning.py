#!/usr/bin/env python
"""Put each stock clip where its own words match the narration, not where the cadence lands it.

WHY THIS EXISTS. build_case_film_generic lays stock and motion out on a fixed F/M/F/M/F/S
cadence -- by rhythm, never by meaning -- and then fills each F slot from a queue in pool
order. Measured 2026-09-07 on three episodes about to ship:

    EP83 max737   10.6s  "working from a coffee shop on a laptop"
                         under "Same aeroplane. Same fault. Same wheel."
    EP83 max737  587.4s  the Texas State Capitol rotunda
                         under "one year before the FAA certified the aeroplane"
    EP84 threemile 940.1s  ducklings on a river
                         under "the company was never convicted of lying to the regulator"
    EP84 threemile  27.8s  a golden wheat field
                         under "a feedwater pump tripped at Three Mile Island, Unit 2"

Blocking the offender does not fix this: the next clip in the queue is promoted into the same
slot and is generic in a new way. Four rounds of blocking on max737 produced, in order, a
coffee shop, an empty boardroom, a cargo truck and a farm-field drone -- all on 10.6s.

WHAT IT DOES. It permutes stock clips AMONG THE STOCK SLOTS THEY ALREADY OCCUPY. It does not
change cut times, cut count, the motion plates, the stills, the captions or the audio; it does
not add or remove a clip. Each stock slot is scored against every free stock clip by matching
the clip's filename words to the narration spoken during that slot, and slots are filled
best-first so the strongest available pairing wins rather than the first one tried.

    py -3.11 scripts/assign_stock_by_meaning.py --slug max737 --dry-run
    py -3.11 scripts/assign_stock_by_meaning.py --slug max737 --apply

WHAT IT CANNOT DO -- read honestly. It matches WORDS, not pictures. A clip whose filename says
"river" scores on the word river however the river looks, and a clip named "AR-v_28285" with a
useless filename can never score at all. It cannot tell that ducklings are wrong under a
sentence about a conviction; it can only tell that nothing in "chick ducks young animals"
appears in that sentence, which is why the pairing loses to a better one when a better one
exists. When the pool holds nothing relevant, this moves generic footage around; it does not
make it apt. The remedy for that is a better pool, and this prints the leftovers so the gap
is visible instead of silent.
"""
from __future__ import annotations

import argparse
import glob
import json
import re
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[1]

# Words that say nothing about WHICH slot a clip belongs in.
STOP = {
    "the", "a", "an", "and", "or", "but", "if", "of", "to", "in", "on", "at", "for", "with",
    "that", "this", "it", "is", "was", "are", "were", "be", "been", "by", "from", "as", "not",
    "no", "any", "all", "its", "their", "they", "them", "he", "she", "his", "her", "one", "two",
    "had", "has", "have", "did", "do", "does", "what", "who", "why", "how", "when", "where",
    "which", "there", "then", "than", "so", "up", "out", "into", "over", "under", "after",
    "before", "about", "would", "could", "said", "says", "you", "your", "we", "our", "i",
    # stock-filename noise: present in half the shelf and therefore discriminating nothing
    "aerial", "drone", "footage", "shot", "view", "close", "clip", "video", "beautiful",
    "nature", "landscape", "background", "scene", "time", "lapse", "timelapse", "day",
    "daylight", "summer", "winter", "spring", "autumn", "fall", "sun", "sunset", "sunrise",
}

# A clip's words rarely appear verbatim in narration -- "cooling tower" is spoken as "the
# plant", "cockpit" as "the flight deck". These are the bridges that earned their place by
# fixing a measured mismatch, and nothing is added here on speculation.
BRIDGE = {
    "aeroplane": {"airplane", "aircraft", "plane", "jet", "airliner", "flight", "aviation"},
    "airplane": {"aeroplane", "aircraft", "plane", "jet", "flight", "takeoff", "landing"},
    "reactor": {"nuclear", "plant", "core", "coolant", "fuel", "meltdown", "unit"},
    "steam": {"pressuriser", "pressurizer", "vent", "relief", "valve", "boil", "coolant"},
    "smoke": {"steam", "plume", "vent"},
    "river": {"susquehanna", "island", "water", "bank", "canal", "levee", "channel"},
    "dam": {"levee", "floodwall", "wall", "reservoir", "spillway", "canal"},
    "levee": {"dam", "floodwall", "wall", "canal", "breach", "flood"},
    "flood": {"water", "surge", "levee", "canal", "breach", "drown"},
    "storm": {"hurricane", "surge", "wind", "rain"},
    "town": {"city", "neighbourhood", "neighborhood", "street", "home", "house", "resident"},
    "car": {"road", "drive", "traffic", "vehicle"},
    "telephone": {"call", "called", "phone", "rang", "line"},
    "television": {"broadcast", "news", "reporter", "camera", "screen"},
    "static": {"broadcast", "television", "signal", "screen"},
    "clock": {"hour", "minute", "second", "morning", "night", "time"},
    "fog": {"mist", "haze", "dawn"},
    "ocean": {"sea", "water", "coast", "shore", "wave"},
    "sea": {"ocean", "water", "coast", "shore", "wave", "crash", "crashed"},
    "cloud": {"sky", "air", "altitude", "weather", "climb"},
    "sky": {"cloud", "air", "altitude", "climb", "flight"},
}


def words(text: str) -> set[str]:
    out = {w for w in re.findall(r"[a-z]{3,}", text.lower()) if w not in STOP}
    return out


def clip_words(src: str) -> set[str]:
    """The words a stock filename actually offers. `AR-pexels_13423170__a_golden_wheat_field`
    contributes {golden, wheat, field} -- the id and the source name are never content."""
    name = str(src).replace("\\", "/").split("/")[-1]
    name = re.sub(r"\.[a-z0-9]+$", "", name)
    tail = name.split("__", 1)[1] if "__" in name else name
    return words(tail.replace("_", " "))


def expand(ws: set[str]) -> set[str]:
    out = set(ws)
    for w in ws:
        for k, v in BRIDGE.items():
            if w.startswith(k):
                out |= v
    return out


def load_cues(srt: Path) -> list[tuple[float, str]]:
    def sec(t: str) -> float:
        h, m, rest = t.split(":")
        s, ms = rest.split(",")
        return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000
    out = []
    for block in srt.read_text(encoding="utf-8").strip().split("\n\n"):
        lines = block.strip().split("\n")
        if len(lines) < 3 or "-->" not in lines[1]:
            continue
        out.append((sec(lines[1].split(" --> ")[0]), " ".join(lines[2:])))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    if not a.apply and not a.dry_run:
        ap.error("pass --apply or --dry-run")

    film_path = ROOT / f"remotion/src/data/{a.slug}_film.json"
    if not film_path.is_file():
        print(f"no film json at {film_path} -- build the episode first", file=sys.stderr)
        return 1
    epdirs = sorted(glob.glob(str(ROOT / f"episodes/PD-*-{a.slug}")))
    if not epdirs:
        print(f"no episode dir for {a.slug}", file=sys.stderr)
        return 1
    srt = Path(epdirs[-1]) / "08_edit/captions.final.v001.srt"
    if not srt.is_file():
        print(f"no captions at {srt}", file=sys.stderr)
        return 1

    film = json.loads(film_path.read_text(encoding="utf-8"))
    cues = load_cues(srt)
    cuts = film.get("cuts") or []

    slots = [i for i, c in enumerate(cuts)
             if "/factory/" in str(c.get("src", "")).replace("\\", "/")]
    if not slots:
        print(f"{a.slug}: no stock cuts -- nothing to place")
        return 0

    pool = [str(cuts[i]["src"]) for i in slots]
    pool_w = {s: expand(clip_words(s)) for s in pool}

    def narration(i: int) -> set[str]:
        c = cuts[i]
        t0, t1 = c.get("start", 0.0), c.get("end", c.get("start", 0.0) + 5)
        return words(" ".join(txt for st, txt in cues if t0 - 1.5 <= st <= t1 + 1.5))

    slot_w = {i: narration(i) for i in slots}

    # Score every (slot, clip) pair, then fill best-first. Filling in TIME order would let an
    # early slot take a clip a later slot needed far more, which is how a queue behaves and is
    # the behaviour being replaced.
    pairs = sorted(
        ((len(slot_w[i] & pool_w[s]), i, s) for i in slots for s in pool),
        key=lambda p: (-p[0], p[1], p[2]),
    )
    # ONE SHARED WORD IS NOISE, NOT MEANING. Measured on threemile at threshold 1: "night" in
    # `time_lapse_of_a_small_town_at_night` matched the line about the annunciator panel, which
    # took that clip away from the opening where it belonged and left a wheat field there. Two
    # shared words is the point at which the matches stopped being coincidences -- katrina's
    # flood-road aerial landing on "responsible for about seventy percent of the flooding".
    MIN_SCORE = 2
    placed: dict[int, str] = {}
    used: set[str] = set()
    for score, i, s in pairs:
        if score < MIN_SCORE or i in placed or s in used:
            continue
        placed[i], _ = s, used.add(s)
    # A SLOT WITH NO SCORING CLIP KEEPS THE CLIP IT ALREADY HAD. The first version redistributed
    # the leftovers in time order, which moved footage between slots that both scored zero --
    # i.e. on no information at all. Measured on threemile: it took "a small town at night" off
    # "Everything that follows begins with a plumbing problem", where it was fine, and put a
    # golden wheat field there. Shuffling without evidence is not an improvement, it is churn,
    # so this only ever moves a clip TO a slot whose words it actually matches.
    original = {i: str(cuts[i]["src"]) for i in slots}
    for i in slots:
        if i in placed:
            continue
        if original[i] not in used:
            placed[i] = original[i]
            used.add(original[i])
    leftovers = [s for s in pool if s not in used]
    for i in slots:
        if i not in placed:
            placed[i] = leftovers.pop(0)

    moved = 0
    for i in slots:
        old, new = str(cuts[i]["src"]), placed[i]
        score = len(slot_w[i] & pool_w[new])
        line = " ".join(txt for st, txt in cues
                        if cuts[i].get("start", 0) - 1.5 <= st <= cuts[i].get("start", 0) + 4)
        mark = "  " if old == new else "->"
        if old != new:
            moved += 1
        print(f"\n{mark} {cuts[i].get('start', 0):7.1f}s  score {score}")
        print(f"     was  {old.split('/')[-1][:64]}")
        print(f"     now  {new.split('/')[-1][:64]}")
        print(f"     line {line[:110]}")
        if a.apply:
            cuts[i]["src"] = new

    print(f"\n{a.slug}: {len(slots)} stock slot(s), {moved} reassigned")
    if a.apply:
        film_path.write_text(json.dumps(film, indent=2, ensure_ascii=False) + "\n",
                             encoding="utf-8")
        print(f"wrote {film_path.name}")
    else:
        print("DRY RUN -- nothing written")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
