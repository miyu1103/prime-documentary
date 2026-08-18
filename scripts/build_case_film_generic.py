#!/usr/bin/env python
"""Generic motion-first CaseFilm builder: <slug>_film.json from an asset manifest + narration.

ONE implementation for every episode (EP51+), replacing the practice of cloning the 676-line
build_centralpark_film.py per episode. The per-episode creative content (hook line, figure
content banks, AE beats) lives in a config JSON; everything structural is derived here.

Preserved from the passing EP50 build (PD_IRONCLAD_GATES.v001.md calibration):
  * treatments = bleed / duotone / focus only. depth / scan / card are BANNED (warp + scanline).
  * captions split to <=CAPTION_MAX_CHARS so no cue ever wraps past 2 lines.
  * motion-first: real video (factory stock + i2v motion) dominates; stills are the minority
    and are never reused; video may repeat at most twice, spread far apart.
  * P## faces belong to the PEOPLE pool and are injected into the motion/still rotation, so
    human faces recur through the film instead of only appearing as thumbnails.
  * figure kinds validated against the real FigureSpec union; dochighlight is BANNED.

WHY THE CUT ALLOCATION IS SOLVED, NOT HARD-CODED (EP50 lesson): centralpark hard-coded
per-section (factory, motion, still) counts, which raised "unable to allocate N assets with
cap C" the moment a pool was smaller than the constant assumed. Here the totals are solved
from the ACTUAL pool sizes and the measured narration length, subject to the gate's own
thresholds, so a small pool yields a valid (if less ambitious) plan instead of a crash.

Usage:
  py -3.11 scripts/build_case_film_generic.py --config episodes/_planning/EP52_morton_filmconfig.v001.json
  ... [--assets <manifest.json>] [--narr <narration_index.json>] [--out <film.json>] [--dry-run]

Always follow with the pre-render gate; never render without it:
  py -3.11 scripts/pd_prerender_gate.py remotion/src/data/<slug>_film.json remotion/public/<slug>/..
"""
from __future__ import annotations

import argparse
import json
import math
import subprocess
import sys
from collections import Counter, deque
from pathlib import Path

import pd_footage_blocklist

ROOT = Path(__file__).resolve().parents[1]
FPS = 30

# ---- calibration (measured on the passing EP50 motion-first build) ----
CAPTION_MAX_CHARS = 84      # <=2 lines at fontSize 44 / maxWidth 78%
TARGET_CUT_SEC = 4.6        # average cut length; shorter than EP50's 6.1s for tighter pacing
MIN_VIDEO_SHARE = 0.68      # build target; the gate's hard floor is 0.62, so this leaves margin
MAX_VIDEO_REUSE = 2         # gate allows 3; we stay at 2
MAX_STILL_REUSE = 1         # stills are never repeated

# The planner must budget with the caps the GATE enforces, and those are asymmetric:
# check_asset_reuse allows a factory clip ONCE (free, 11k-clip library) and an i2v motion clip
# TWICE (24-73 GPU-min each). Planning factory at 2 hands it twice the capacity that will be
# graded and then fills it, so asset_reuse fails by about the factory-clip count no matter how
# much footage is staged -- EP62 greene measured 28 over cap at 48 accepted clips and 28 at 74.
# Imported, not retyped: two copies of one number is exactly how these drifted apart.
try:
    from check_asset_reuse import MAX_USES_FACTORY as _CAP_FACTORY, MAX_USES_MOTION as _CAP_MOTION
except Exception:                                    # keep the builder runnable in isolation
    _CAP_FACTORY, _CAP_MOTION = 1, 2
PINNED_HEAD = 0             # set by the caller: this many leading pool items must all be used
TREATMENTS = ["bleed", "duotone", "focus"]
BANNED_TREATMENTS = {"depth", "scan", "card"}
HOOK_SEC = 8.0
OPENING_SEC = 3.5
ENDCARD_SEC = 9.0

# casetimeline_c is a REAL renderer kind (FigureBeats.tsx, the carsearch CaseTimeline
# component) with shipped use in EP34, and it was simply missing from this list. EP59 hit it
# first and was worked around by rewriting the episode config; EP60 hit it in ACT_5 and the
# build died. Fixing the list is the correct repair -- the config should not be bent to match
# an incomplete allow-list.
VALID_KINDS = {"numberticker", "stat", "votetally", "timeline", "casetimeline_c", "quote", "kinetic",
               "lowerthird", "acttitle", "compbars", "bar", "mechanism", "regionmap",
               "pindropmap", "routemap", "arrow", "highlightring", "spotlight"}
BANNED_FIGURE_KINDS = {"dochighlight"}   # reads as a rendering bug (owner flagged 3x)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


# ------------------------------------------------------------------ captions
def split_caption_text(text: str, limit: int = CAPTION_MAX_CHARS) -> list[str]:
    if len(text) <= limit:
        return [text]
    segs, cur = [], ""
    for w in text.split():
        if cur and len(cur) + 1 + len(w) > limit:
            segs.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}".strip()
    if cur:
        segs.append(cur)
    return segs


def build_captions(narr: dict) -> tuple[list[dict], float]:
    cues: list[dict] = []
    for c in narr["chunks"]:
        text = str(c.get("text") or c.get("spoken_text") or "").strip()
        if not text:
            continue
        start, end = round(float(c["start"]), 3), round(float(c["end"]), 3)
        segs = split_caption_text(text)
        if len(segs) == 1:
            cues.append({"start": start, "end": end, "text": text})
            continue
        total_chars = sum(len(s) for s in segs)
        t = start
        for i, s in enumerate(segs):
            seg_end = end if i == len(segs) - 1 else round(t + (end - start) * len(s) / total_chars, 3)
            cues.append({"start": round(t, 3), "end": seg_end, "text": s})
            t = seg_end
    return cues, max(c["end"] for c in cues)


def srt_ts(t: float) -> str:
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def write_srt(cues: list[dict], out: Path) -> None:
    lines: list[str] = []
    for i, c in enumerate(cues, 1):
        lines += [str(i), f"{srt_ts(c['start'])} --> {srt_ts(c['end'])}", c["text"], ""]
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines), encoding="utf-8")


# ------------------------------------------------------------------ sections
def section_order(narr: dict) -> list[str]:
    """Sections in first-appearance order -- generic over HOOK/OP/ACT_n/ENDING layouts."""
    seen, order = set(), []
    for c in narr["chunks"]:
        s = c["section"]
        if s not in seen:
            seen.add(s)
            order.append(s)
    return order


def section_windows(narr: dict, order: list[str], total: float) -> dict[str, tuple[float, float]]:
    starts: dict[str, float] = {}
    for c in narr["chunks"]:
        starts.setdefault(c["section"], float(c["start"]))
    windows: dict[str, tuple[float, float]] = {}
    for i, sec in enumerate(order):
        nxt = order[i + 1] if i + 1 < len(order) else None
        windows[sec] = (starts[sec], starts[nxt] if nxt else total)
    return windows


# ------------------------------------------------------------------ pools
def public_items(manifest: dict, key: str, role: str | None = None) -> list[str]:
    items = manifest.get(key) or []
    if role:
        items = [x for x in items if x.get("role") == role]
    out = [str(x["public_path"]) for x in items if x.get("public_path")]
    if len(out) != len(set(out)):
        raise SystemExit(f"duplicate public_path in {key}")
    return out


def people_paths(manifest: dict) -> list[str]:
    """P## faces + any role-tagged people stills. These MUST reach the film, not just thumbs."""
    out: list[str] = []
    for key in ("stills", "visible_faces", "people"):
        for x in manifest.get(key) or []:
            pp = x.get("public_path")
            if not pp:
                continue
            name = Path(str(pp)).stem.upper()
            if x.get("role") in ("visible_face", "people", "person") or name.startswith("P"):
                out.append(str(pp))
    # stable de-dup
    seen, uniq = set(), []
    for p in out:
        if p not in seen:
            seen.add(p)
            uniq.append(p)
    return uniq


def solve_totals(total_sec: float, n_factory: int, n_motion: int, n_still: int) -> tuple[int, int, int]:
    """Solve (factory, motion, still) cut counts from the REAL pool sizes.

    Constraints: factory <= 2x pool, motion <= 2x pool, still <= 1x pool,
    video share >= MIN_VIDEO_SHARE. Returns the largest feasible plan near the target
    cut count rather than crashing when a pool is small.
    """
    want = max(60, int(round(total_sec / TARGET_CUT_SEC)))
    cap_f = n_factory * _CAP_FACTORY
    cap_m = n_motion * _CAP_MOTION
    cap_s = n_still * MAX_STILL_REUSE
    if cap_f + cap_m == 0:
        raise SystemExit("no real video assets (factory+motion pools are empty) -- kamishibai guard")

    # video first, split between factory and motion in proportion to what each pool can supply
    video_want = int(math.ceil(want * MIN_VIDEO_SHARE))
    video = min(video_want, cap_f + cap_m)
    if cap_f + cap_m:
        f = min(cap_f, int(round(video * cap_f / (cap_f + cap_m))))
        m = min(cap_m, video - f)
        f = min(cap_f, video - m)
    else:                                     # unreachable, guarded above
        f = m = 0
    video = f + m
    # stills fill the remainder but may never push video share below the floor
    still_max_for_share = int(math.floor(video * (1 - MIN_VIDEO_SHARE) / MIN_VIDEO_SHARE))
    s = min(cap_s, max(0, want - video), still_max_for_share)
    return f, m, s


def split_by_section(total: int, weights: dict[str, float]) -> dict[str, int]:
    """Largest-remainder apportionment so the per-section counts sum exactly to `total`."""
    tw = sum(weights.values()) or 1.0
    raw = {k: total * w / tw for k, w in weights.items()}
    out = {k: int(math.floor(v)) for k, v in raw.items()}
    rem = total - sum(out.values())
    for k, _ in sorted(raw.items(), key=lambda kv: kv[1] - math.floor(kv[1]), reverse=True):
        if rem <= 0:
            break
        out[k] += 1
        rem -= 1
    return out


def repeated(pool: list[str], n: int, cap: int, label: str) -> list[str]:
    if n <= 0:
        return []
    if not pool:
        raise SystemExit(f"not enough {label}: need {n}, have 0")
    if cap == 1 and n < len(pool):
        # SURPLUS POOL: take an EVEN SPREAD, never the first n.
        # The walk below starts at index 0, so when the pool is bigger than the requirement it
        # silently kept the alphabetical head and dropped the tail. EP54 had 134 stills for 119
        # image cuts, and the 15 it dropped were S210-S224 -- the fourteen courtroom stills that
        # had just been generated precisely because the archive holds no courtroom footage at
        # all. Losing exactly the newest, most deliberate assets is the worst possible failure
        # mode for a rule nobody chose. An even stride keeps the whole pool in play.
        # Anything the caller pinned to the front is taken verbatim first -- a stride can skip
        # an index, and on EP54 it skipped exactly one of the fourteen pinned courtroom stills.
        head = pool[:PINNED_HEAD] if PINNED_HEAD else []
        head = head[:n]
        rest = pool[len(head):]
        need = n - len(head)
        seen: set[str] = set(head)
        out2 = list(head)
        if need > 0 and rest:
            step = len(rest) / need
            for k in range(need):
                cand = rest[min(len(rest) - 1, int(k * step))]
                if cand not in seen:
                    seen.add(cand); out2.append(cand)
        i = 0
        while len(out2) < n and i < len(pool):        # rounding can collide; backfill in order
            if pool[i] not in seen:
                seen.add(pool[i]); out2.append(pool[i])
            i += 1
        out2 = out2[:n]
        dropped = [p for p in pool if p not in set(out2)]
        if dropped:
            # Never silent. A surplus pool still means some assets do not reach the film, and
            # whoever made them is entitled to know which.
            names = [d.split("/")[-1] for d in dropped]
            print(f"  [{label}] pool {len(pool)} > need {n}; {len(dropped)} not used: "
                  f"{', '.join(names[:12])}{' ...' if len(names) > 12 else ''}")
        return out2
    out: list[str] = []
    uses: Counter[str] = Counter()
    i = guard = 0
    while len(out) < n and guard < n * 10 + 100:
        item = pool[i % len(pool)]
        if uses[item] < cap:
            uses[item] += 1
            out.append(item)
        i += 1
        guard += 1
    if len(out) < n:
        raise SystemExit(f"unable to allocate {n} {label} assets with cap {cap} from pool {len(pool)}")
    return out


def take(q: deque, n: int) -> list[str]:
    return [q.popleft() for _ in range(min(n, len(q)))]


# ------------------------------------------------------------------ cuts
# --- per-still exposure -------------------------------------------------------------------
# EP51's acceptance run measured 93.4% of its stills below the readable luma floor and 29% of
# hero image cuts too dark to read (the recurring 「画像が暗くて見えにくい」). A global wash was
# tried on EP49 and flattened contrast, so each still is measured here and gets its OWN lift:
# bright images are left alone, dark ones are opened to the target. CaseFilm applies cut.lift.
_LIFT_CACHE: dict[str, float] = {}
STILL_TARGET_LUMA = 78.0
STILL_MAX_LIFT = 1.85


def still_lift(public_src: str) -> float:
    """brightness multiplier for one still (1.0 = leave it alone)."""
    if public_src in _LIFT_CACHE:
        return _LIFT_CACHE[public_src]
    lift = 1.0
    try:
        from PIL import Image
        p = ROOT / "remotion" / "public" / public_src
        if p.is_file():
            im = Image.open(p).convert("L").resize((64, 36))
            px = list(im.getdata())
            mean = sum(px) / len(px)
            if mean > 1.0:
                lift = min(STILL_MAX_LIFT, max(1.0, STILL_TARGET_LUMA / mean))
    except Exception:
        lift = 1.0
    _LIFT_CACHE[public_src] = round(lift, 3)
    return _LIFT_CACHE[public_src]



_SRC_SECONDS: dict[str, float] = {}


def source_seconds(public_src: str) -> float:
    """Measured length of a staged clip (0.0 when unreadable)."""
    if public_src in _SRC_SECONDS:
        return _SRC_SECONDS[public_src]
    path = ROOT / "remotion" / "public" / public_src
    val = 0.0
    if path.is_file():
        r = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                            "format=duration", "-of", "csv=p=0", str(path)],
                           capture_output=True, text=True)
        try:
            val = float(r.stdout.strip())
        except ValueError:
            val = 0.0
    _SRC_SECONDS[public_src] = val
    return val


def make_cuts(order: list[str], windows: dict[str, tuple[float, float]], manifest: dict,
              slug: str) -> tuple[list[dict], dict]:
    stills = public_items(manifest, "stills", "body") or public_items(manifest, "stills")
    factory_pool = public_items(manifest, "factory")
    motion_pool = public_items(manifest, "motion")
    people = people_paths(manifest)

    # People are woven into the STILL rotation (faces recur through the film, not just thumbs).
    # Any person still already present in `stills` is not duplicated.
    still_pool_src = people + [s for s in stills if s not in set(people)]

    # THE SAME PICTURE MUST NOT APPEAR TWICE, ONCE FROZEN AND ONCE MOVING.
    # i2v conversion keeps the stem: img/G045.png and motion/G045.mp4 are one picture. The
    # manifest scans both directories, so without this both reach the cut list and the viewer
    # sees the identical frame twice -- the reuse the owner has ruled out. The motion version
    # wins: it is that picture with movement, which is the direction the video-share floor
    # already pushes. check_spec_satisfied matches mandatory_stills by stem, so a mandatory
    # plate stays satisfied by its .mp4.
    def _stem(rel: str) -> str:
        return rel.split("/")[-1].rsplit(".", 1)[0].lower()

    _moving = {_stem(m) for m in motion_pool}
    if _moving:
        _superseded = [s for s in still_pool_src if _stem(s) in _moving]
        if _superseded:
            still_pool_src = [s for s in still_pool_src if _stem(s) not in _moving]
            print(f"  [dedup] {len(_superseded)} still(s) dropped -- the same picture is in the "
                  f"motion pool and will be used there instead: "
                  + ", ".join(sorted(_stem(s) for s in _superseded)[:10])
                  + (" ..." if len(_superseded) > 10 else ""))

    # PIN WHAT THE LAST FILM DID NOT USE.
    # A surplus pool means some stills are left out. Left to an even stride, the ones left out
    # are arbitrary -- and on EP54 that arbitrarily excluded two of the fourteen courtroom
    # stills that had just been generated because the archive has no courtroom footage at all.
    # A still that is in the pool but was absent from the previous build is, by definition, the
    # newest intent in the episode. It goes to the front, so the surplus is taken from material
    # the film has already been carrying instead.
    def _mtime(rel: str) -> float:
        p = ROOT / "remotion" / "public" / rel
        try:
            return p.stat().st_mtime
        except OSError:
            return 0.0

    newest = max((_mtime(s) for s in still_pool_src), default=0.0)
    fresh = [s for s in still_pool_src if newest - _mtime(s) < 12 * 3600]
    if fresh and len(fresh) < len(still_pool_src):
        still_pool_src = fresh + [s for s in still_pool_src if s not in set(fresh)]
        globals()["PINNED_HEAD"] = len(fresh)
        print(f"  [still] {len(fresh)} still(s) delivered in the last 12h pinned to the front: "
              + ", ".join(s.split('/')[-1] for s in sorted(fresh)[:14])
              + (" ..." if len(fresh) > 14 else ""))

    total_sec = max(e for _, e in windows.values())

    # CUT LENGTH COMES FROM THE EPISODE, WHEN THE EPISODE SAYS SO.
    # The constant fixes the cut count, and the cut count caps how many stills can appear.
    # An episode that commissioned stills because the archive had nothing for its subject
    # needs a say in that number. The video-share floor and every motion check are untouched.
    # AN UNDECLARED VALUE IS AN ERROR, NEVER AN INFERRED DEFAULT (CLAUDE.md s4.6 item 3).
    # This block used to fall through to TARGET_CUT_SEC in silence. EP62 greene, EP63 correa and
    # EP64 memphis were all built that way -- and the constant is not cosmetic: it fixes the cut
    # count, the cut count caps how many stills can appear (stills may hold at most 32% of cuts
    # under the video-share floor), and check_spec_satisfied then refuses a film whose
    # mandatory_stills do not fit. EP61 weimer commissioned 150 stills; at 4.6s only 105 fit.
    # An episode that never chose 4.6 was nevertheless cut to it, and nothing said so.
    _specs = sorted((ROOT / "episodes").glob(f"PD-*-{slug}/episode_spec.v001.json"))
    if not _specs:
        raise SystemExit(
            f"[cuts] {slug} has no episodes/PD-*-{slug}/episode_spec.v001.json, so it declares "
            f"no target_cut_sec and this builder will not substitute its own {TARGET_CUT_SEC}s "
            f"(CLAUDE.md s4.6). Write the spec, then run "
            f"`py -3.11 scripts/check_episode_spec.py --slug {slug}`.")
    try:
        _spec_doc = json.loads(_specs[0].read_text(encoding="utf-8"))
    except Exception as _exc:  # noqa: BLE001
        raise SystemExit(f"[cuts] {_specs[0]} is unreadable ({_exc}); refusing to guess a cut "
                         f"length. Run `py -3.11 scripts/check_episode_spec.py --slug {slug}`.")
    _declared = _spec_doc.get("target_cut_sec")
    if not isinstance(_declared, (int, float)) or isinstance(_declared, bool):
        raise SystemExit(
            f"[cuts] {slug} declares no target_cut_sec in "
            f"{_specs[0].relative_to(ROOT).as_posix()}. The builder will NOT fall back to its "
            f"own {TARGET_CUT_SEC}s: an undeclared value is an error, never an inferred default "
            f"(CLAUDE.md s4.6 item 3). Derive the episode\u0027s real value rather than picking "
            f"one -- for a film already delivered, solve "
            f"ceil(round(total_sec / t) * MIN_VIDEO_SHARE) == the video-cut count in "
            f"remotion/src/data/{slug}_film.json, which pins t to a band a few hundredths wide; "
            f"then add \"target_cut_sec\": <t> to the spec.")
    if not (2.0 <= float(_declared) <= 8.0):
        raise SystemExit(
            f"[cuts] {slug} declares target_cut_sec={_declared}, outside the schema band "
            f"2.0-8.0. Fix the spec; the builder does not clamp a declared value.")
    _cut_sec = float(_declared)
    print(f"  [cuts] {slug} declares {_cut_sec}s per cut "
          f"(builder default {TARGET_CUT_SEC}s, used for nothing but the solver scale)")

    # solve_totals derives its cut count as runtime / TARGET_CUT_SEC; scaling the runtime it
    # is handed is how the declared cut length reaches it without touching the solver.
    nf, nm, ns = solve_totals(total_sec * (TARGET_CUT_SEC / _cut_sec),
                              len(factory_pool), len(motion_pool), len(still_pool_src))

    weights = {sec: (windows[sec][1] - windows[sec][0]) for sec in order}
    per_f = split_by_section(nf, weights)
    per_m = split_by_section(nm, weights)
    per_s = split_by_section(ns, weights)

    factory_q = deque(repeated(factory_pool, nf, _CAP_FACTORY, "factory"))
    motion_q = deque(repeated(motion_pool, nm, _CAP_MOTION, "motion"))
    still_q = deque(repeated(still_pool_src, ns, MAX_STILL_REUSE, "still"))

    cuts: list[dict] = []
    treat_i = 0
    for sec in order:
        s, e = windows[sec]
        fac, mot, sti = take(factory_q, per_f[sec]), take(motion_q, per_m[sec]), take(still_q, per_s[sec])
        if not (fac or mot or sti):
            continue
        seq: list[tuple[str, str]] = []
        fi = mi = si = 0
        pattern = ["F", "M", "F", "M", "F", "S"]     # motion-first cadence
        while fi < len(fac) or mi < len(mot) or si < len(sti):
            slot = pattern[len(seq) % len(pattern)]
            if slot == "F" and fi < len(fac):
                seq.append(("footage", fac[fi])); fi += 1
            elif slot == "M" and mi < len(mot):
                seq.append(("footage", mot[mi])); mi += 1
            elif slot == "S" and si < len(sti):
                seq.append(("img", sti[si])); si += 1
            elif fi < len(fac):
                seq.append(("footage", fac[fi])); fi += 1
            elif mi < len(mot):
                seq.append(("footage", mot[mi])); mi += 1
            elif si < len(sti):
                seq.append(("img", sti[si])); si += 1
        # stills systematically shorter than footage (animation_mix)
        weights_seq = [3.0 if kind == "img" else 3.343 for kind, _ in seq]
        scale = (e - s) / sum(weights_seq)
        t = s
        for kind, src in seq:
            dur = round((3.0 if kind == "img" else 3.343) * scale, 3)
            cut = {"id": f"cut-{len(cuts):04d}", "start": round(t, 3), "dur": dur,
                   "kind": kind, "src": src, "seed": f"{slug}-{len(cuts):04d}", "act": sec}
            if kind == "footage":
                # the renderer clamps the in-point against this; without it a cut can
                # run past the end of its clip and go black (EP55: 26/259 cuts)
                cut["srcSeconds"] = round(source_seconds(src), 3)
            cut["treatment"] = TREATMENTS[treat_i % len(TREATMENTS)] if kind == "img" else "footage"
            if kind == "img":
                treat_i += 1
                lift = still_lift(src)
                if lift > 1.001:
                    cut["lift"] = lift
            cuts.append(cut)
            t += dur
        if cuts:
            cuts[-1]["dur"] = round(e - cuts[-1]["start"], 3)
    plan = {"factory": nf, "motion": nm, "still": ns,
            "pools": {"factory": len(factory_pool), "motion": len(motion_pool),
                      "still": len(still_pool_src), "people": len(people)}}
    # A clip shorter than its cut is not a planning error -- it just has to loop. Mark it so the
    # renderer repeats it instead of running out of footage and going black. Only a clip that is
    # unreadable (0s) is a real problem.
    # A clip that barely moves must never be asked to repeat. Looping joins the end of one still
    # stretch to the start of the next: R013 is still for 68% of its 4.8s, and on a 5.3s slot that
    # produced a 4.03s hold -- past the 3s limit -- while the same clip on a shorter slot measured
    # 2.1s and passed. The defect was in the pool the whole time; only the shuffle decided whether
    # it surfaced. 45 of marmet's 149 motion clips are still for 60%+ of their length, so deleting
    # them is not an option; not looping them is.
    _still: dict[str, float] = {}
    _sp = ROOT / "runs" / "qc" / f"{slug}_motion_stillness.v001.json"
    if _sp.is_file():
        try:
            for _r in json.loads(_sp.read_text(encoding="utf-8")).get("clips", []):
                _still[_r["clip"]] = float(_r.get("still_share") or 0.0)
        except Exception:  # noqa: BLE001
            _still = {}

    def _is_still(c: dict) -> bool:
        return _still.get(Path(str(c.get("src") or "")).name, 0.0) >= 0.60

    def _would_loop(c: dict) -> bool:
        return bool(c.get("kind") == "footage" and c.get("srcSeconds")
                    and c["dur"] > c["srcSeconds"] + 0.05)

    if _still:
        # A still-heavy clip on a slot longer than itself trades with a lively clip whose slot it
        # can cover. Timings and cut count are untouched -- only which clip sits where.
        _bad = [c for c in cuts if _would_loop(c) and _is_still(c)]
        _swapped = 0
        for c in _bad:
            for d in cuts:
                if d is c or d.get("kind") != "footage" or _is_still(d):
                    continue
                if not d.get("srcSeconds") or _would_loop(d):
                    continue
                # c must fit d's slot without looping, and d must still cover c's slot
                if c["srcSeconds"] >= d["dur"] - 0.05 and d["srcSeconds"] >= c["dur"] - 0.05:
                    c["src"], d["src"] = d["src"], c["src"]
                    c["srcSeconds"], d["srcSeconds"] = d["srcSeconds"], c["srcSeconds"]
                    _swapped += 1
                    break
        _left = [c for c in cuts if _would_loop(c) and _is_still(c)]
        print(f"  [stillness] {len(_bad)} near-still clip(s) were set to loop; "
              f"swapped {_swapped}, {len(_left)} could not be placed")
        for c in _left[:5]:
            print(f"    still {Path(str(c['src'])).name} on a {c['dur']:.2f}s slot "
                  f"(clip is {c['srcSeconds']:.2f}s)")

    for c in cuts:
        if c.get("kind") == "footage" and c.get("srcSeconds") and c["dur"] > c["srcSeconds"] + 0.05:
            c["loopSource"] = True
    # A clip a person opened and rejected must never reach a film.json. The builder already
    # refuses clips it cannot read; a rejected clip reads perfectly, passes every machine measure
    # of motion, luma and diversity, and is caught by nothing downstream. Measured 2026-08-09:
    # correa, memphis and marmet each carried 45-52 of them in film.json files written before the
    # rejections were applied.
    _verdicts = ROOT / "runs" / "qc" / f"{slug}_clip_verdicts.v001.json"
    if _verdicts.is_file():
        try:
            _rej = dict(json.loads(_verdicts.read_text(encoding="utf-8")).get("rejected") or {})
        except Exception as exc:  # noqa: BLE001
            raise SystemExit(f"{_verdicts.name} is unreadable ({exc}); cannot prove this film is "
                             f"free of clips that were rejected by eye")
        _used = {}
        for c in cuts:
            _n = Path(str(c.get("src") or "")).name
            if _n in _rej:
                _used[_n] = _used.get(_n, 0) + 1
        if _used:
            for _n in sorted(_used)[:8]:
                print(f"  rejected clip {_n} used by {_used[_n]} cut(s): {_rej[_n]}")
            raise SystemExit(f"{len(_used)} clip(s) rejected in visual QC reached the cut list "
                             f"({sum(_used.values())} cuts). Not writing {slug}_film.json.")

    impossible = [c for c in cuts if c.get("kind") == "footage"
                  and not c.get("srcSeconds")]
    if impossible:
        for c in impossible[:6]:
            print(f"  cut {c['id']}: {c['src'].split('/')[-1]} is unreadable "
                  f"(0s) -- it cannot be rendered", file=sys.stderr)
        raise SystemExit(f"{len(impossible)} cut(s) reference an unreadable clip")

    # THE BLOCKLIST IS ENFORCED WHERE THE FILM IS MADE, not after it is rendered.
    # An audit on 2026-08-02 found the EP58 plan carrying two third-party YouTube vlogger
    # clips and a test tube legibly labelled "Coronavirus", and the EP59 plan carrying real
    # Fox News footage of Jeffrey Epstein and news footage of Steve Bannon, both with network
    # watermarks. Those are rights hazards and invariant-11 hazards, and nothing downstream
    # was looking for them. A film that names a blocked clip is not emitted at all.
    #
    # SCOPE (2026-08-05): the list now carries episode-scoped rows as well as global ones, so
    # this is asked for THIS SLUG. 108 shipped-frame rejections across ten episodes split into
    # material no documentary may use (readable IRS forms, a Tokyo patrol car, scraped news with
    # a chyron) and material only one episode may not use (handcuffs in EP55, ruins in EP60, and
    # the episode's own W###/P## plates, whose numbers name different pictures in other films).
    # Both kinds have to stop a build; only the first kind may bind everywhere.
    blocked_hits = pd_footage_blocklist.hits((c.get("src") for c in cuts), slug)
    if blocked_hits:
        for base, why in blocked_hits[:8]:
            print(f"  BLOCKED {base}\n          {why}", file=sys.stderr)
        raise SystemExit(
            f"{len(blocked_hits)} cut(s) reference a clip blocked for {slug}. Prune the pool "
            f"with scripts/prune_pool_by_blocklist.py --slug {slug} and rebuild.")
    return cuts, plan


def make_hook(manifest: dict, slug: str, hook_sec: float) -> list[dict]:
    """Cold open: people first -- a named human before any principle (pd-opening-formula)."""
    people = people_paths(manifest)
    stills = public_items(manifest, "stills", "body") or public_items(manifest, "stills")
    picks = (people + [s for s in stills if s not in set(people)])[:8]
    if not picks:
        raise SystemExit("no stills available for the hook")
    hook: list[dict] = []
    t = 0.0
    step = round(hook_sec / len(picks), 3)
    for i, src in enumerate(picks):
        d = round(hook_sec - t, 3) if i == len(picks) - 1 else step
        hook.append({"start": round(t, 3), "dur": d, "kind": "img", "src": src,
                     "seed": f"{slug}-hook-{i:02d}"})
        t += d
    return hook


# ------------------------------------------------------------------ figures
def build_figures(cfg: dict, order: list[str], windows: dict[str, tuple[float, float]],
                  total: float) -> list[dict]:
    """Place the config's figure payloads evenly inside each section window.

    The config supplies `figures_by_section`: {section: [payload, ...]} where each payload is a
    ready FigureSpec dict (kind + its fields). Content is the episode's own -- this function
    only validates and times it.
    """
    by_sec: dict[str, list[dict]] = cfg.get("figures_by_section") or {}
    disclosure = {"kind": "lowerthird", "primary": "AI-assisted visualization",
                  "secondary": "symbolic reconstruction, no real likenesses"}
    figures: list[dict] = []
    for sec in order:
        payloads = list(by_sec.get(sec) or [])
        if not payloads:
            continue
        s, e = windows[sec]
        dur = 3.0 if sec in {"HOOK", "OP"} else 6.0
        lo = s + (0.1 if sec in {"HOOK", "OP"} else 3.0)
        hi = e - (0.1 if sec in {"HOOK", "OP"} else 6.5)
        if hi - lo < dur:
            lo, hi = s, e
        span = max(hi - lo, dur)
        for i, payload in enumerate(payloads):
            kind = payload.get("kind")
            if kind in BANNED_FIGURE_KINDS:
                raise SystemExit(f"banned figure kind {kind} in {sec}")
            if kind not in VALID_KINDS:
                raise SystemExit(f"invalid figure kind {kind!r} in {sec}")
            start = lo + span * (i + 0.5) / len(payloads) - dur / 2
            start = min(max(start, lo), max(lo, hi - dur))
            end = min(start + dur, total - 0.5)
            figures.append({"start": round(start, 3), "end": round(end, 3), **payload})
    figures.sort(key=lambda x: x["start"])
    if figures:
        figures[0] = {**figures[0], **disclosure}
        figures[-1] = {**figures[-1], **disclosure}
    return figures


def lead_frames(hook_sec: float, lead_sec: float | None) -> int:
    """Frame at which the body starts. Mirrors `caseFilmLeadFrames` in CaseFilm.tsx.

    SPEC v2 row 9, binding from EP66: a filmconfig may declare `leadSeconds` and put the body,
    and the narration inside it, at frame 0. `is None`, not falsy -- EP66 declares 0.0. When it
    is absent (every episode up to EP65) this is the historical expression term for term."""
    if lead_sec is None:
        return round(hook_sec * FPS) + round(OPENING_SEC * FPS)
    return round(lead_sec * FPS)


def duration_frames(narration_seconds: float, hook_sec: float,
                    lead_sec: float | None = None) -> int:
    return (lead_frames(hook_sec, lead_sec)
            + math.ceil(narration_seconds * FPS) + round(ENDCARD_SEC * FPS))


# ------------------------------------------------------------------ main
def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", type=Path, required=True)
    ap.add_argument("--assets", type=Path, default=None)
    ap.add_argument("--narr", type=Path, default=None)
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--captions", type=Path, default=None)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    cfg = load_json(a.config)
    slug = cfg["slug"]
    ep = cfg["episode_id"]
    ep_dir = ROOT / "episodes" / ep
    assets = a.assets or Path(cfg.get("assets") or ep_dir / "05_visuals" / "asset_manifest.v003.json")
    narr_p = a.narr or Path(cfg.get("narration_index") or ep_dir / "06_audio" / "narration_index.v001.json")
    out = a.out or Path(cfg.get("out") or ROOT / "remotion" / "src" / "data" / f"{slug}_film.json")
    srt = a.captions or Path(cfg.get("captions") or ep_dir / "08_edit" / "captions.final.v001.srt")

    manifest = load_json(assets)
    if manifest.get("is_stub") is True:
        raise SystemExit(f"{slug}: asset manifest is a stub -- real assets required")
    narr = load_json(narr_p)
    if narr.get("is_stub") is True:
        raise SystemExit(f"{slug}: narration_index is a stub -- measured TTS required")

    captions, total = build_captions(narr)
    order = section_order(narr)
    windows = section_windows(narr, order, total)
    hook_sec = float(cfg.get("hookSeconds", HOOK_SEC))
    # SPEC v2 row 9 (binds from EP66): the filmconfig may put the body -- and the narration
    # master inside it -- at frame 0 by declaring `leadSeconds: 0`. Absent, `lead_sec` stays
    # None and every downstream consumer falls back to hookSeconds + OPENING_SEC, so no
    # existing filmconfig changes. The key is written into film.json ONLY when declared: an
    # absent key must stay absent, because that is what CaseFilm.tsx tests for.
    _lead_raw = cfg.get("leadSeconds")
    lead_sec = None if _lead_raw is None else float(_lead_raw)
    cuts, plan = make_cuts(order, windows, manifest, slug)
    hook = make_hook(manifest, slug, hook_sec)
    # The hook is on screen too. EP51's rejected plates were people stills, and make_hook draws
    # from exactly that pool, so a clip barred from the body must not slip in through the cold
    # open -- which is the most-watched eight seconds of the film.
    hook_hits = pd_footage_blocklist.hits((h.get("src") for h in hook), slug)
    if hook_hits:
        for base, why in hook_hits[:8]:
            print(f"  BLOCKED (hook) {base}\n          {why}", file=sys.stderr)
        raise SystemExit(f"{len(hook_hits)} hook shot(s) reference a clip blocked for {slug}.")
    figures = build_figures(cfg, order, windows, total)

    # ---- structural assertions (fail here, never after a multi-hour render) ----
    stills_n = sum(1 for c in cuts if c["kind"] == "img")
    video_n = len(cuts) - stills_n
    share = video_n / len(cuts) if cuts else 0
    if share < 0.62:
        raise SystemExit(f"{slug}: NOT motion-first: video share {share:.3f} < 0.62 (plan={plan})")
    if len(cuts) < 150:
        raise SystemExit(f"{slug}: too few cuts {len(cuts)} (plan={plan})")
    uses = Counter(c["src"] for c in cuts)
    if uses and max(uses.values()) > 3:
        raise SystemExit(f"{slug}: src reused {max(uses.values())}x > 3")
    distinct_ratio = len(uses) / len(cuts)
    if distinct_ratio < 0.50:
        raise SystemExit(f"{slug}: distinct ratio {distinct_ratio:.3f} < 0.50")
    if any(c.get("treatment") in BANNED_TREATMENTS for c in cuts):
        raise SystemExit(f"{slug}: banned treatment present")
    over = [c for c in captions if len(c["text"]) > CAPTION_MAX_CHARS]
    if over:
        raise SystemExit(f"{slug}: {len(over)} captions exceed {CAPTION_MAX_CHARS} chars")
    if not figures:
        raise SystemExit(f"{slug}: no figures -- config.figures_by_section is empty")

    total_frames = duration_frames(total, hook_sec, lead_sec)
    film = {
        "episode_id": ep,
        "fps": FPS,
        "narration": str(cfg.get("narration") or f"{slug}/narration.mp3"),
        "narrationSeconds": round(total, 3),
        "hookSeconds": hook_sec,
        "hookLine": cfg["hookLine"],
        "hook": hook,
        "cuts": cuts,
        "captions": captions,
        "graphics": [],
        "figures": figures,
        "overlays": [x["public_path"] for x in manifest.get("overlay", []) if x.get("public_path")],
    }
    if lead_sec is not None:
        film["leadSeconds"] = lead_sec
    # EP66 PACKAGING v001 sections 4 and 7: which FORM of the channel opening this film places.
    # Written only when the filmconfig declares it, because CaseFilm.tsx reads an absent key as
    # the historical full-screen card -- EP62-65's film.json must not gain the key.
    _variant = cfg.get("openingVariant")
    if _variant is not None:
        if _variant not in ("card", "overlay"):
            raise SystemExit(
                f"{slug}: openingVariant must be 'card' or 'overlay', got {_variant!r}")
        film["openingVariant"] = _variant
    # A zero (or short) lead leaves no room in front of the body for the full-screen card, so a
    # film that shortens the lead and does NOT ask for the overlay would render with no channel
    # opening at all. That shipped once as a green gate; it stops here, before the render.
    if (lead_sec is not None and lead_sec < hook_sec + OPENING_SEC
            and _variant != "overlay"):
        raise SystemExit(
            f"{slug}: leadSeconds {lead_sec} leaves no room for the {OPENING_SEC}s brand card "
            f"in front of a {hook_sec}s hook, and openingVariant is {_variant!r}. The film "
            f"would have NO opening. Declare openingVariant 'overlay' or restore the lead.")
    report = {
        "slug": slug, "cuts": len(cuts), **plan,
        "video_cuts": video_n, "still_cuts": stills_n,
        "video_share": round(share, 4),
        "distinct_assets": len(uses), "distinct_ratio": round(distinct_ratio, 4),
        "max_reuse": max(uses.values()) if uses else 0,
        "avg_cut_sec": round(total / len(cuts), 2),
        "figures": len(figures), "captions": len(captions),
        "narrationSeconds": round(total, 3), "duration_frames": total_frames,
        "duration_sec_with_bookends": round(total_frames / FPS, 2),
        "sections": order,
    }
    if a.dry_run:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0

    write_srt(captions, srt)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(film, ensure_ascii=False, indent=2), encoding="utf-8")
    bm = ep_dir / "04_scenes" / f"{slug}_build_manifest.v001.json"
    bs = ep_dir / "04_scenes" / f"{slug}_beatsheet.v001.json"
    bm.parent.mkdir(parents=True, exist_ok=True)
    bm.write_text(json.dumps({"episode_id": ep, "producer": "scripts/build_case_film_generic.py",
                              "inputs": {"assets": str(assets), "narr": str(narr_p),
                                         "config": str(a.config)},
                              "report": report}, ensure_ascii=False, indent=2), encoding="utf-8")
    bs.write_text(json.dumps({"schema_version": f"{slug}_beatsheet.v1", "episode_id": ep,
                              "figures": figures, "report": report}, ensure_ascii=False, indent=2),
                  encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    raise SystemExit(main())
