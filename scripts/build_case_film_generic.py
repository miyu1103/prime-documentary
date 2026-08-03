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

ROOT = Path(__file__).resolve().parents[1]
FPS = 30

# ---- calibration (measured on the passing EP50 motion-first build) ----
CAPTION_MAX_CHARS = 84      # <=2 lines at fontSize 44 / maxWidth 78%
TARGET_CUT_SEC = 4.6        # average cut length; shorter than EP50's 6.1s for tighter pacing
MIN_VIDEO_SHARE = 0.68      # build target; the gate's hard floor is 0.62, so this leaves margin
MAX_VIDEO_REUSE = 2         # gate allows 3; we stay at 2
MAX_STILL_REUSE = 1         # stills are never repeated
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
    cap_f = n_factory * MAX_VIDEO_REUSE
    cap_m = n_motion * MAX_VIDEO_REUSE
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
    nf, nm, ns = solve_totals(total_sec, len(factory_pool), len(motion_pool), len(still_pool_src))

    weights = {sec: (windows[sec][1] - windows[sec][0]) for sec in order}
    per_f = split_by_section(nf, weights)
    per_m = split_by_section(nm, weights)
    per_s = split_by_section(ns, weights)

    factory_q = deque(repeated(factory_pool, nf, MAX_VIDEO_REUSE, "factory"))
    motion_q = deque(repeated(motion_pool, nm, MAX_VIDEO_REUSE, "motion"))
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
    for c in cuts:
        if c.get("kind") == "footage" and c.get("srcSeconds") and c["dur"] > c["srcSeconds"] + 0.05:
            c["loopSource"] = True
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
    blocklist = ROOT / "config" / "footage_blocklist.v001.json"
    if blocklist.is_file():
        blocked: dict[str, str] = {}
        for row in json.loads(blocklist.read_text(encoding="utf-8")).get("blocked", []):
            for ident in row["ids"]:
                blocked[ident] = f"{row['label']}: {row['reason']}"
        hits = []
        for c in cuts:
            base = (c.get("src") or "").split("/")[-1]
            ident = base.split("__")[0]
            why = blocked.get(ident) or blocked.get(ident.replace("AF-BG-", ""))
            if why:
                hits.append((base, why))
        if hits:
            for base, why in hits[:8]:
                print(f"  BLOCKED {base}\n          {why}", file=sys.stderr)
            raise SystemExit(
                f"{len(hits)} cut(s) reference a blocklisted clip. Prune the pool with "
                f"scripts/prune_pool_by_blocklist.py --slug <slug> and rebuild.")
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


def duration_frames(narration_seconds: float, hook_sec: float) -> int:
    return (round(hook_sec * FPS) + round(OPENING_SEC * FPS)
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
    cuts, plan = make_cuts(order, windows, manifest, slug)
    hook = make_hook(manifest, slug, hook_sec)
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

    total_frames = duration_frames(total, hook_sec)
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
