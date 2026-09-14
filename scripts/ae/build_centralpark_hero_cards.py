#!/usr/bin/env python
"""EP50 Central Park (The Exonerated Five) - AE hero-card JSX generator.

Cloned from the FIXED EP45 build_cleveland_hero_cards.py (AE-2026-JP pipeline).
Keeps its SIX proven layouts 1:1 -- ACT_TITLE_CARD / CENTER_STACK / MONEY_STACK /
QUOTE_CARD / VOTE_SPLIT / SPLIT_COMPARE -- and ADDS eight bespoke Tier-B set-piece
layouts (choreography from EP50 DESIGN_ARCHITECTURE section 3 / CODEX_B section 7.3):

  DNA_LADDER  STAT_RESOLVE  CARD_STACK  REC_LIGHT  SCALE_TIP
  HERO_TIMELINE  NAME_WALL  SIGNATURE_ERASE

EP50-specific vs the cleveland source:
  * accent = cold forensic steel-cyan #2F9FC4 = [0.184,0.624,0.769] (NOT EP45 crimson).
    dawn-amber #C98A3C = [0.788,0.541,0.235] appears ONLY on exoneration/close moments
    (c-vacated / m-41m / c-state39 / c-salaam / t-a6 / REC_LIGHT-on / SCALE_TIP-right /
    HERO_TIMELINE-resolve / NAME_WALL-close / SIGNATURE_ERASE resolve). Threaded via
    each beat's `accentMode` field ("cyan"|"dawn").
  * BONE = #EDEDE8 type colour added.
  * 36-moment deck (Tier A 24 + Tier B 12); anchors are body-relative and FIXED
    (id/layout/CP-id/anchor one-to-one with DESIGN section 3 / CODEX_B section 7.2).
  * Accuracy 7-constraint wording baked into strings (R-INNOCENCE / R-VICTIM / R-REYES /
    R-NUM / R-FACE / R-DOCHL / R-QUOTE). No invented quotes: q-alone renders as a
    CENTER_STACK fallback ("HE ACTED ALONE" / "DNA CONFIRMED ONE ATTACKER") until a
    verified-verbatim line is locked. Hedged figures ($85,000 / $3.9M / ~13yr) carry
    their hedge word. Years are literal strings so no thousands comma ("1989" not "1,989").

Tier-B implementation sequence (CODEX_B section 7.5 -- phantom-crash avoidance):
  implement builder fn -> `--dryrun --only <LAYOUT>` single-comp AfterFX build ->
  confirm render/<id>.mp4 exists (>100KB) -> add L to check_AE_layouts allowlist ->
  only then reference L in the production deck. The JSX keeps its tail
  `else throw "unsupported layout"` so any not-yet-implemented layout still hard-fails.

Machine traps honoured (CODEX_B section 7.8, unchanged from the FIXED source): runtime font
resolve with unwrap() + HARD FAIL, spatial-aware setTemporalEaseAtKey dim, NO
app.newProject(), per-layer motionBlur, "ADBE Rotate Z", explicit inPoint AND
outPoint, conformFrameRate=30, single-line TextDocument, SOFTWARE gpu, localized
RS/OM template names first, all display strings precomputed in Python, ASCII-only
labels, completion marker file, .aep saved by the JSX; the caller asserts
.aep mtime > .jsx mtime before aerender (two-step, stale-aep guard). Render output
goes to the REPO path (C:) -- AE's H.264 OM writes 0 mp4s to the exFAT H: drive.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(r"C:\Users\aab15\Documents\prime-documentary")
EP = "PD-2026-050-centralpark"
FACTS = ROOT / "episodes" / EP / "03_script" / "centralpark_facts.v001.json"
FILM = ROOT / "remotion" / "src" / "data" / "centralpark_film.json"
REPO_BEATS_DIR = ROOT / "episodes" / EP / "08_edit" / "ae_hero"

FPS = 30
W, H = 1920, 1080

# section 7.1 EP50 colour constants (0..1 float). cold forensic steel-cyan lane.
ACCENT = [0.184, 0.624, 0.769]   # #2F9FC4 cold steel-cyan numbers / underline / DNA / lane
INK = [0.039, 0.039, 0.047]      # #0A0A0C near-black root
BONE = [0.929, 0.929, 0.910]     # #EDEDE8 type
DAWN = [0.788, 0.541, 0.235]     # #C98A3C dawn-amber -- exoneration/close moments ONLY
WHITE = [0.961, 0.969, 0.980]    # #F5F7FA
SILVER = [0.784, 0.804, 0.839]   # #C8CDD6 labels / disclosure

STILLS = Path("E:/pd-media/assets/ai/centralpark")

# Bookend offset: figures[] and these AE beats are body/narration-relative.
# Absolute time in the finished bookended base mp4 = start + FILM_OFFSET_SEC.
OPENING_SEC = 3.5

# advance-width factors (Anton / Oswald cap-height specimens) -- starting-size
# estimate only; the JSX re-fits with sourceRectAtTime (measured, never clipped).
ANTON_ADV = 0.470
OSWALD_ADV = 0.505

# R-FORBID: EP50 forbidden strings (subject-anchored assertions ONLY -- NEVER add the bare
# words attacked/confession/rape/wilding, which appear in legitimate verbatim context).
FORBIDDEN = [
    "the five were involved", "they were involved", "the boys attacked",
    "the five attacked", "possibly guilty", "may still be guilty",
    "the teens did it", "guilty after all", "they were wilding", "30 hours",
]


def fit_size(text: str, base: int, max_w: int, adv: float, tracking: int = 0) -> int:
    n = max(1, len(text))
    per = adv + (tracking / 1000.0)
    return max(18, min(base, int(max_w / (per * n))))


def count_keys(target, t0, t1, prefix="", suffix="", thousands=False,
               decimals=0, n=20):
    """Ease-out-cubic count-up. Python formats EVERY display string; the JSX
    never does arithmetic on a number. Settles to the EXACT target."""
    def fmt(v):
        if decimals > 0:
            body = (f"{v:,.{decimals}f}" if thousands else f"{v:.{decimals}f}")
        else:
            iv = int(round(v))
            body = (f"{iv:,}" if thousands else f"{iv}")
        return f"{prefix}{body}{suffix}"
    keys = [(t0, fmt(0))]
    for i in range(1, n):
        p = i / (n - 1)
        v = target * (1.0 - (1.0 - p) ** 3)
        keys.append((t0 + (t1 - t0) * p, fmt(v)))
    keys.append((t1 + 0.02, fmt(target)))
    return [[round(t, 4), s] for t, s in keys]


# --------------------------------------------------------------- the card deck
# Tier A 24 (six proven layouts) + Tier B 12 (eight NEW set-piece layouts).
# anchor is body-relative seconds; start = anchor (FIXED, deconflicted by design,
# asserted by validate_centralpark_beats). accentMode "dawn" = exoneration/close only.
DECK = [
    # ---- Tier B -------------------------------------------------------------
    dict(id="B8", layout="HERO_TIMELINE", anchor=120.0, dur=7.0, accentMode="cyan",
         cp="CP03", phase="intro", years=["1989"], top="THE TIMELINE",
         sub="THAT NIGHT"),
    dict(id="B4", layout="REC_LIGHT", anchor=470.0, dur=5.0, accentMode="cyan",
         cp="CP08", mode="off", top="THE RECORD", sub="THE CAMERA WAS OFF"),
    dict(id="B10", layout="NAME_WALL", anchor=700.0, dur=7.0, accentMode="cyan",
         cp="CP05", mode="names",
         names=["McCRAY 15", "RICHARDSON 14", "SALAAM 15", "SANTANA 14", "WISE 16"],
         top="FIVE CHILDREN", sub=""),
    dict(id="B3", layout="CARD_STACK", anchor=960.0, dur=7.0, accentMode="cyan",
         cp="CP10", pages=5, top="FIVE STATEMENTS", sub="NO FOUNDATION"),
    dict(id="B6", layout="SCALE_TIP", anchor=1445.0, dur=6.0, accentMode="cyan",
         cp="CP12", mode="confession", top="THE WEIGHT",
         sub="A CONFESSION OUTWEIGHED THE EVIDENCE"),
    dict(id="B1", layout="DNA_LADDER", anchor=2695.0, dur=10.0, accentMode="cyan",
         cp="CP24", lanes=5, top="THE DNA", sub="1 IN 6 BILLION - A SINGLE MATCH"),
    dict(id="B2", layout="STAT_RESOLVE", anchor=2740.0, dur=7.0, accentMode="cyan",
         cp="CP24", value=6000000000, thousands=True, top="THE MATCH",
         sub="1 IN 6 BILLION"),
    dict(id="B12", layout="SIGNATURE_ERASE", anchor=2895.0, dur=6.0, accentMode="dawn",
         cp="CP27", top="THE SIGNATURE", sub="VACATED - ALL FIVE, ALL COUNTS"),
    dict(id="B7", layout="SCALE_TIP", anchor=2985.0, dur=6.0, accentMode="dawn",
         cp="CP24", mode="evidence", top="THE CORRECTION",
         sub="THE EVIDENCE RIGHTED THE SCALE"),
    dict(id="B9", layout="HERO_TIMELINE", anchor=3020.0, dur=9.0, accentMode="dawn",
         cp="CP27", phase="resolve", years=["1989", "2002", "2014"],
         top="THE RECKONING", sub="VACATED - SETTLED"),
    dict(id="B5", layout="REC_LIGHT", anchor=3165.0, dur=6.0, accentMode="dawn",
         cp="CP34", mode="on", top="THE REFORM",
         sub="RECORD THE WHOLE INTERROGATION"),
    dict(id="B11", layout="NAME_WALL", anchor=3600.0, dur=9.0, accentMode="dawn",
         cp="CP32", mode="exonerated",
         names=["McCRAY 15", "RICHARDSON 14", "SALAAM 15", "SANTANA 14", "WISE 16"],
         title="THE EXONERATED FIVE", top="", sub=""),

    # ---- Tier A (six proven layouts) ---------------------------------------
    dict(id="t-a1", layout="ACT_TITLE_CARD", anchor=27.0, dur=5.0, accentMode="cyan",
         cp="CP03", top="ACT I", main="THE NIGHT - APRIL 1989"),
    dict(id="c-noevidence", layout="CENTER_STACK", count_type="CT_TEXT", anchor=372.0,
         dur=6.0, accentMode="cyan", cp="CP12", top="AT THE MOMENT OF QUESTIONING",
         hero_text="NO PHYSICAL EVIDENCE", bottom="THE EVIDENCE POINTED ELSEWHERE"),
    dict(id="t-a2", layout="ACT_TITLE_CARD", anchor=452.0, dur=5.0, accentMode="cyan",
         cp="", top="ACT II", main="THE INTERROGATIONS"),
    dict(id="c-sevenhours", layout="CENTER_STACK", count_type="CT_TEXT", anchor=505.0,
         dur=6.0, accentMode="cyan", cp="CP08", top="BEFORE THE CAMERAS",
         hero_text="AT LEAST SEVEN HOURS", bottom="NONE OF IT RECORDED"),
    dict(id="c-roompromise", layout="CENTER_STACK", count_type="CT_TEXT", anchor=560.0,
         dur=6.0, accentMode="cyan", cp="CP34", top="A ROOM AND A PROMISE",
         hero_text="YOU CAN GO HOME IF YOU JUST SAY IT",
         bottom="A PARAPHRASE OF THE PRESSURE - NOT A QUOTED LINE"),
    dict(id="c-fivechildren", layout="CENTER_STACK", count_type="CT_TEXT", anchor=720.0,
         dur=6.0, accentMode="cyan", cp="CP05", top="FIVE CHILDREN",
         hero_text="AGES 14 TO 16", bottom="INTERROGATED FOR HOURS"),
    dict(id="cmp-fedsigned", layout="SPLIT_COMPARE", anchor=905.0, dur=6.5,
         accentMode="cyan", cp="CP10", top="THE INTERROGATION", left="FED IN",
         right="SIGNED", strike="", bottom="THE GENTLENESS WAS THE TRAP"),
    dict(id="cmp-confdna", layout="SPLIT_COMPARE", anchor=1080.0, dur=6.5,
         accentMode="cyan", cp="CP12", top="THE CONTRADICTION", left="5 CONFESSIONS",
         right="0 DNA MATCHES", strike="", bottom="THE EVIDENCE POINTED ELSEWHERE"),
    dict(id="t-a3", layout="ACT_TITLE_CARD", anchor=1170.0, dur=5.0, accentMode="cyan",
         cp="CP15", top="ACT III", main="THE TRIALS - 1990"),
    dict(id="c-papersfirst", layout="CENTER_STACK", count_type="CT_TEXT", anchor=1245.0,
         dur=5.5, accentMode="cyan", cp="CP14", top="1989",
         hero_text="TRIED IN THE PAPERS FIRST", bottom="A CITY TRIED THEM BEFORE A JURY DID"),
    dict(id="c-trumpad", layout="CENTER_STACK", count_type="CT_TEXT", anchor=1305.0,
         dur=6.5, accentMode="cyan", cp="CP13", top="MAY 1, 1989",
         hero_text="A FULL-PAGE AD DEMANDED THE DEATH PENALTY",
         bottom="REPORTEDLY ~$85,000 - IT DID NOT NAME THE FIVE"),
    dict(id="cmp-verdict", layout="SPLIT_COMPARE", anchor=1600.0, dur=6.0,
         accentMode="cyan", cp="CP17", top="THE VERDICTS", left="CONVICTED",
         right="ACQUITTED OF ATTEMPTED MURDER", strike="",
         bottom="EVEN THE JURIES HESITATED"),
    dict(id="cmp-sentence", layout="SPLIT_COMPARE", anchor=1655.0, dur=6.5,
         accentMode="cyan", cp="CP18", top="THE SENTENCES", left="JUVENILE - 5 TO 10 YRS",
         right="KOREY WISE, 16: AS AN ADULT", strike="",
         bottom="A BIRTHDAY MADE THE DIFFERENCE"),
    dict(id="t-a4", layout="ACT_TITLE_CARD", anchor=1704.0, dur=5.0, accentMode="cyan",
         cp="", top="ACT IV", main="THE LOST YEARS"),
    dict(id="cmp-yearsserved", layout="SPLIT_COMPARE", anchor=1875.0, dur=6.5,
         accentMode="cyan", cp="CP19", top="YEARS SERVED", left="FOUR: ~6 TO 7 YRS EACH",
         right="KOREY WISE: ~13 YRS", strike="", bottom="TRIED AS AN ADULT AT 16"),
    dict(id="t-a5", layout="ACT_TITLE_CARD", anchor=2272.0, dur=5.0, accentMode="cyan",
         cp="", top="ACT V", main="THE CONFESSION & THE DNA"),
    dict(id="c-twodays", layout="CENTER_STACK", count_type="CT_TEXT", anchor=2340.0,
         dur=6.0, accentMode="cyan", cp="CP22", top="APRIL 17, 1989",
         hero_text="TWO DAYS BEFORE",
         bottom="THE SAME PART OF THE PARK - REYES IS BELIEVED TO HAVE ATTACKED THERE"),
    dict(id="q-alone", layout="CENTER_STACK", count_type="CT_TEXT", anchor=2560.0,
         dur=6.5, accentMode="cyan", cp="CP24", top="MATIAS REYES - 2002",
         hero_text="HE ACTED ALONE", bottom="DNA CONFIRMED ONE ATTACKER"),
    dict(id="t-a6", layout="ACT_TITLE_CARD", anchor=2823.0, dur=5.0, accentMode="dawn",
         cp="", top="ACT VI", main="EXONERATION & RECKONING"),
    dict(id="c-vacated", layout="CENTER_STACK", count_type="CT_TEXT", anchor=2860.0,
         dur=6.0, accentMode="dawn", cp="CP27", top="DEC 19, 2002",
         hero_text="VACATED - ALL FIVE, ALL COUNTS", bottom="THE STATE ITSELF REVERSED COURSE"),
    dict(id="m-41m", layout="MONEY_STACK", count_type="CT_MONEY", anchor=3045.0, dur=7.0,
         accentMode="dawn", cp="CP30", top="ROUGHLY", value=41000000, prefix="$",
         thousands=True, bottom="NEW YORK CITY, 2014 - ABOUT $1M PER YEAR LOST"),
    dict(id="c-state39", layout="CENTER_STACK", count_type="CT_TEXT", anchor=3115.0,
         dur=5.5, accentMode="dawn", cp="CP31", top="2016 - NEW YORK STATE",
         hero_text="REPORTEDLY ~$3.9 MILLION MORE", bottom="A SEPARATE STATE SETTLEMENT"),
    dict(id="c-salaam", layout="CENTER_STACK", count_type="CT_TEXT", anchor=3270.0,
         dur=5.5, accentMode="dawn", cp="CP33", top="2023",
         hero_text="YUSEF SALAAM", bottom="ELECTED TO THE NYC COUNCIL"),
    dict(id="t-a7", layout="ACT_TITLE_CARD", anchor=3308.0, dur=5.0, accentMode="cyan",
         cp="CP34", top="", main="WHAT A CONFESSION IS WORTH"),
]

# Layouts implemented in this builder (six proven + eight Tier-B). check_AE_layouts
# gates the *proven* superset; the JSX gates the *implemented* superset via else-throw.
PROVEN_LAYOUTS = {"ACT_TITLE_CARD", "CENTER_STACK", "MONEY_STACK", "QUOTE_CARD",
                  "VOTE_SPLIT", "SPLIT_COMPARE"}
TIER_B_LAYOUTS = {"DNA_LADDER", "STAT_RESOLVE", "CARD_STACK", "REC_LIGHT", "SCALE_TIP",
                  "HERO_TIMELINE", "NAME_WALL", "SIGNATURE_ERASE"}


def load_facts() -> dict:
    if not FACTS.exists():
        return {}
    d = json.loads(FACTS.read_text(encoding="utf-8"))
    return d.get("facts", d)


def figure_intervals() -> list[tuple[float, float]]:
    if not FILM.exists():
        return []
    d = json.loads(FILM.read_text(encoding="utf-8"))
    return [(float(f["start"]), float(f["end"])) for f in d.get("figures") or []]


def build(dryrun: bool, only: str | None, beat: str | None = None) -> int:
    facts = load_facts()
    offset = round(8.0 + OPENING_SEC, 3)
    if FILM.exists():
        d = json.loads(FILM.read_text(encoding="utf-8"))
        offset = round(float(d.get("hookSeconds", 8.0)) + OPENING_SEC, 3)

    deck = list(DECK)
    if beat:
        deck = [c for c in DECK if c["id"] == beat]
        if not deck:
            print(f"FAIL --beat {beat}: no beat with that id in DECK", file=sys.stderr)
            return 5
    elif only:
        deck = [c for c in DECK if c["layout"] == only]
        if not deck:
            print(f"FAIL --only {only}: no beat with that layout in DECK", file=sys.stderr)
            return 5
        deck = deck[:1]  # single-comp proof

    work = (ROOT / "episodes" / EP / "08_edit" / ("_dryrun/ae_hero" if dryrun else "ae_hero"))
    media = work
    render = media / "render"
    media.mkdir(parents=True, exist_ok=True)
    render.mkdir(parents=True, exist_ok=True)
    REPO_BEATS_DIR.mkdir(parents=True, exist_ok=True)
    for m in ("_build_ok.txt", "_error.txt"):
        (render / m).unlink(missing_ok=True)

    # ---- ledger gate: burned numbers must be verified:true (only if facts exist) ----
    if facts:
        for c in deck:
            fid = c.get("cp")
            if fid and fid in facts:
                f = facts.get(fid)
                if isinstance(f, dict) and f.get("verified") is not True:
                    print(f"FAIL off-ledger/unverified {fid} on {c['id']}", file=sys.stderr)
                    return 1

    # anchors are FIXED and pre-deconflicted (DESIGN section 3). Sort by start for the deck.
    ordered = sorted(deck, key=lambda c: c["anchor"])

    beats = []
    for c in ordered:
        start = round(float(c["anchor"]), 3)
        end = round(start + float(c["dur"]), 3)

        still_path = None
        if c.get("still"):
            p = STILLS / c["still"]
            if not p.exists():
                print(f"FAIL missing still {p}", file=sys.stderr)
                return 2
            still_path = str(p).replace("\\", "/")

        b = dict(
            id=c["id"], layout=c["layout"], count_type=c.get("count_type"),
            cp=c.get("cp", ""), start=start, end=end, dur=float(c["dur"]),
            accentMode=c.get("accentMode", "cyan"),
            still=still_path, top=c.get("top", ""), bottom=c.get("bottom", ""),
            sub=c.get("sub", ""), caption="", hero="", value=None, numKeys=None,
            required=True,
            out=str(render / f"{c['id']}.mp4").replace("\\", "/"),
        )

        if c["layout"] == "ACT_TITLE_CARD":
            b["hero"] = c["main"]
            b["main"] = c["main"]
            b["mainSize"] = fit_size(c["main"], 168, 1620, ANTON_ADV)
        elif c["layout"] in ("CENTER_STACK", "MONEY_STACK"):
            ct = c["count_type"]
            if ct == "CT_TEXT":
                b["hero"] = c["hero_text"]
                b["heroText"] = c["hero_text"]
                b["heroSize"] = fit_size(c["hero_text"], 280, 1620, ANTON_ADV)
            else:
                t0, t1 = 0.65, 1.85
                b["numKeys"] = count_keys(
                    c["value"], t0, t1, prefix=c.get("prefix", ""),
                    suffix=c.get("suffix", ""), decimals=c.get("decimals", 0),
                    thousands=bool(c.get("thousands", False)))
                b["value"] = c["value"]
                b["hero"] = b["numKeys"][-1][1]
                hold = c["dur"] - (t1 + 0.02)
                if hold < 1.20:
                    print(f"FAIL count hold {hold:.2f}s < 1.20s on {c['id']}", file=sys.stderr)
                    return 3
                b["heroSize"] = fit_size(b["hero"], 260 if ct == "CT_MONEY" else 300,
                                         1620, ANTON_ADV)
        elif c["layout"] == "QUOTE_CARD":
            b["hero"] = c["quote"]
            b["quote"] = c["quote"]
            b["attribution_display"] = c.get("attribution", "")
            b["quoteSize"] = fit_size(c["quote"], 96, 1560, OSWALD_ADV, 10)
        elif c["layout"] == "VOTE_SPLIT":
            b["left"], b["right"] = c["left"], c["right"]
            b["hero"] = f"{c['left']} TO {c['right']}"
        elif c["layout"] == "SPLIT_COMPARE":
            b["left"], b["right"] = c["left"], c["right"]
            b["strike"] = c.get("strike", "")
            b["hero"] = f"{c['left']} - {c['right']}"
        # ---- Tier-B set-pieces --------------------------------------------
        elif c["layout"] == "DNA_LADDER":
            b["lanes"] = int(c.get("lanes", 5))
            b["hero"] = c.get("sub", "A SINGLE MATCH")
        elif c["layout"] == "STAT_RESOLVE":
            t0, t1 = 0.6, 2.0
            b["numKeys"] = count_keys(c["value"], t0, t1,
                                      thousands=bool(c.get("thousands", True)))
            b["value"] = c["value"]
            b["hero"] = b["numKeys"][-1][1]
            b["heroSize"] = fit_size(b["hero"], 300, 1620, ANTON_ADV)
        elif c["layout"] == "CARD_STACK":
            b["pages"] = int(c.get("pages", 5))
            b["hero"] = c.get("sub", "NO FOUNDATION")
        elif c["layout"] == "REC_LIGHT":
            b["mode"] = c.get("mode", "off")
            b["hero"] = c.get("sub", "")
        elif c["layout"] == "SCALE_TIP":
            b["mode"] = c.get("mode", "confession")
            b["hero"] = c.get("sub", "")
        elif c["layout"] == "HERO_TIMELINE":
            b["phase"] = c.get("phase", "intro")
            b["years"] = list(c.get("years", ["1989"]))  # literal strings -> no comma
            b["hero"] = " ".join(b["years"])
        elif c["layout"] == "NAME_WALL":
            b["mode"] = c.get("mode", "names")
            b["names"] = list(c.get("names", []))
            b["title"] = c.get("title", "")
            b["hero"] = b["title"] or " / ".join(b["names"])
        elif c["layout"] == "SIGNATURE_ERASE":
            b["hero"] = c.get("sub", "VACATED")

        # forbidden-string assertion over EVERY visible string on this card
        blob = " ".join(str(x) for x in (
            b.get("top"), b.get("bottom"), b.get("sub"), b.get("hero"),
            b.get("caption"), b.get("attribution_display"), b.get("strike"),
            " ".join(b.get("names", []) or []), b.get("title"),
        ) if x).lower()
        for bad in FORBIDDEN:
            if bad in blob:
                print(f"FAIL forbidden string '{bad}' on {c['id']}", file=sys.stderr)
                return 4

        beats.append(b)

    doc = {
        "schema_version": "centralpark_ae_beats.v1",
        "episode_id": EP, "fps": FPS, "width": W, "height": H,
        "timebase": "narration_body_relative",
        "film_offset_sec": offset,
        "offset_note": (
            "start/end are body/narration-relative (same timeline as "
            "centralpark_film.json figures[]). Absolute time in the finished bookended "
            "base mp4 = start + film_offset_sec (hookSeconds + OPENING_SEC "
            f"= {offset}s). The compositor adds this offset when overlaying."),
        "accent": "#2F9FC4",
        "dawn": "#C98A3C",
        "tier_note": (
            "36 moments = Tier A 24 (six proven layouts) + Tier B 12 (eight NEW "
            "set-piece layouts). dawn-amber appears ONLY on exoneration/close beats "
            "(accentMode=dawn). All EP50 forbidden strings (subject-anchored assertions) "
            "were asserted absent from every card string at build time."),
        "render_dir": str(render).replace("\\", "/"),
        "dryrun": bool(dryrun),
        "only": only or "",
        "beats": beats,
    }
    payload = json.dumps(doc, ensure_ascii=False, indent=2)
    (media / "beats.json").write_text(payload, encoding="utf-8")
    single = bool(only or beat)
    if not single:
        # only the full production deck writes the canonical repo beats.json
        (REPO_BEATS_DIR / "beats.json").write_text(payload, encoding="utf-8")

    jsx = JSX
    jsx = jsx.replace("__W__", str(W)).replace("__H__", str(H)).replace("__FPS__", str(FPS))
    jsx = jsx.replace("__ACCENT__", ",".join(str(v) for v in ACCENT))
    jsx = jsx.replace("__WHITE__", ",".join(str(v) for v in WHITE))
    jsx = jsx.replace("__SILVER__", ",".join(str(v) for v in SILVER))
    jsx = jsx.replace("__INK__", ",".join(str(v) for v in INK))
    jsx = jsx.replace("__BONE__", ",".join(str(v) for v in BONE))
    jsx = jsx.replace("__DAWN__", ",".join(str(v) for v in DAWN))
    jsx = jsx.replace("__BEATS__", json.dumps(beats, ensure_ascii=False))
    jsx = jsx.replace("__RENDER__", str(render).replace("\\", "/"))
    jsx = jsx.replace("__AEP__", str(media / "centralpark_hero.aep").replace("\\", "/"))
    (media / "centralpark_hero.jsx").write_text(jsx, encoding="utf-8-sig")

    print(f"[gen] {len(beats)} card(s), total {sum(b['dur'] for b in beats):.1f}s"
          f" | offset={offset}s | dryrun={dryrun} | only={only or '-'}")
    for b in beats:
        print(f"  {b['id']:<14} {b['layout']:<16} start={b['start']:>6.1f} "
              f"end={b['end']:>6.1f}  [{b['accentMode']}]  {b['hero']}")
    print("[gen] jsx  ->", media / "centralpark_hero.jsx")
    print("[gen] aep  ->", media / "centralpark_hero.aep")
    if not single:
        print("[gen] beats->", REPO_BEATS_DIR / "beats.json")
    return 0


JSX = r"""// AUTO-GENERATED - EP50 Central Park AE hero cards. Do not hand-edit.
(function () {
  var W = __W__, H = __H__, FPS = __FPS__;
  var ACCENT = [__ACCENT__], WHITE = [__WHITE__], SILVER = [__SILVER__],
      INK = [__INK__], BONE = [__BONE__], DAWN = [__DAWN__];
  var BEATS = __BEATS__;
  var RENDER_DIR = "__RENDER__";

  function fail(msg) {
    try { var f = new File(RENDER_DIR + "/_error.txt"); f.open("w"); f.write(String(msg)); f.close(); } catch (e) {}
    try { app.quit(); } catch (e) {}
  }

  try {
  // AfterFX -noui -r opens a fresh untitled project. app.newProject() hangs
  // headless on the save prompt -- never call it.
  var proj = app.project;
  try { for (var ri = proj.numItems; ri >= 1; ri--) {
    var itx = proj.item(ri);
    if (itx instanceof CompItem && String(itx.name).indexOf("CENTRALPARK_") === 0) itx.remove();
  } } catch (e) {}
  try { proj.gpuAccelType = GpuAccelType.SOFTWARE; } catch (e) {}
  try { proj.bitsPerChannel = 8; } catch (e) {}
  app.beginUndoGroup("centralpark_hero");

  // ---- runtime font resolver (missing font = HARD FAIL, never silent) ----
  var FONT_LOG = "";
  function unwrap(x) {
    try { if (x && x.postScriptName) return x; } catch (e) {}
    try { if (x && x.length && x[0] && x[0].postScriptName) return x[0]; } catch (e2) {}
    return null;
  }
  function psName(fam, styles) {
    var got = null;
    for (var s = 0; s < styles.length && !got; s++) {
      try {
        var m = app.fonts.getFontsByFamilyNameAndStyleName(fam, styles[s]);
        got = unwrap(m && m.length ? m[0] : m);
      } catch (e) {}
    }
    if (!got) {
      try {
        var all = app.fonts.allFonts;
        for (var i = 0; i < all.length && !got; i++) {
          var f = unwrap(all[i]);
          if (f && String(f.familyName).toLowerCase() === fam.toLowerCase()) got = f;
        }
      } catch (e3) {}
    }
    if (!got) throw new Error("FONT NOT FOUND: " + fam + " -- refusing to substitute");
    FONT_LOG += fam + "=" + got.postScriptName + "/" + got.styleName + " ";
    return got.postScriptName;
  }
  var FONT_NUM = psName("Anton", ["Regular"]);
  var FONT_LBL = psName("Oswald", ["Medium", "Regular", "SemiBold", "Book"]);

  // ---- helpers ----------------------------------------------------------
  function mainAccent(spec) { return (spec.accentMode === "dawn") ? DAWN : ACCENT; }
  function tg(L) { return L.property("ADBE Transform Group"); }
  function span(L, dur) { L.inPoint = 0; L.outPoint = dur; return L; }
  function ease(prop, inf) {
    inf = inf || 70;
    var n = prop.numKeys, dim = 1;
    if (!prop.isSpatial) { var v0 = prop.value; dim = (v0 instanceof Array) ? v0.length : 1; }
    var a = [], b = [];
    for (var d = 0; d < dim; d++) { a.push(new KeyframeEase(0, inf)); b.push(new KeyframeEase(0, inf)); }
    for (var k = 1; k <= n; k++) {
      try { prop.setInterpolationTypeAtKey(k, KeyframeInterpolationType.BEZIER, KeyframeInterpolationType.BEZIER); } catch (e) {}
      try { prop.setTemporalEaseAtKey(k, a, b); } catch (e2) {}
    }
  }
  function key2(p, t0, v0, t1, v1, inf) { p.setValueAtTime(t0, v0); p.setValueAtTime(t1, v1); ease(p, inf); }
  function rect(comp, name, w, h, color, op, x, y) {
    var L = span(comp.layers.addSolid(color, name, Math.max(1, Math.round(w)), Math.max(1, Math.round(h)), 1.0), comp.duration);
    tg(L).property("ADBE Position").setValue([x, y]);
    tg(L).property("ADBE Opacity").setValue(op);
    return L;
  }
  function text(comp, str, font, size, color, tracking, align) {
    var L = span(comp.layers.addText(String(str)), comp.duration);
    var tp = L.property("ADBE Text Properties").property("ADBE Text Document");
    var d = tp.value;
    d.resetCharStyle(); d.font = font; d.fontSize = size; d.fillColor = color;
    d.applyFill = true; d.applyStroke = false; d.tracking = tracking || 0;
    d.justification = (align === "left") ? ParagraphJustification.LEFT_JUSTIFY
                    : (align === "right") ? ParagraphJustification.RIGHT_JUSTIFY
                    : ParagraphJustification.CENTER_JUSTIFY;
    tp.setValue(d);
    return L;
  }
  // ---- MEASURED text fitting (sourceRectAtTime -> real glyph box) ----------
  function srect(L, t) { return L.sourceRectAtTime(t === undefined ? 0 : t, false); }
  function setFontSize(L, sz) {
    var tp = L.property("ADBE Text Properties").property("ADBE Text Document");
    var d = tp.value; d.fontSize = sz; tp.setValue(d);
  }
  function fitText(L, maxW, t) {
    var r = srect(L, t), guard = 0;
    while (r.width > maxW && guard < 24) {
      var tp = L.property("ADBE Text Properties").property("ADBE Text Document");
      var cur = tp.value.fontSize;
      var ns = Math.floor(cur * (maxW / r.width) * 0.985);
      if (ns >= cur) ns = cur - 1;
      if (ns < 12) ns = 12;
      setFontSize(L, ns);
      r = srect(L, t); guard++;
      if (ns === 12) break;
    }
    return r;
  }
  function centerX(L, t) {
    var r = srect(L, t);
    var ap = tg(L).property("ADBE Anchor Point").value;
    tg(L).property("ADBE Anchor Point").setValue([r.left + r.width / 2, ap[1]]);
    return r;
  }
  function centerBlock(L, t) {
    var r = srect(L, t);
    tg(L).property("ADBE Anchor Point").setValue([r.left + r.width / 2, r.top + r.height / 2]);
    return r;
  }
  function wrapText(str, maxChars) {
    var words = String(str).split(" ");
    var lines = [], cur = "";
    for (var i = 0; i < words.length; i++) {
      var w = words[i];
      if (cur.length === 0) { cur = w; }
      else if ((cur.length + 1 + w.length) <= maxChars) { cur += " " + w; }
      else { lines.push(cur); cur = w; }
    }
    if (cur.length) lines.push(cur);
    return lines.join("\r");
  }
  function revealUp(L, t0, x, y, amt) {
    key2(tg(L).property("ADBE Position"), t0, [x, y + (amt || 46)], t0 + 0.5, [x, y], 80);
    key2(tg(L).property("ADBE Opacity"), t0, 0, t0 + 0.4, 100, 70);
  }
  function wipeIn(L, t0, t1, xc, y) {
    var w = L.source.width, h = L.source.height;
    tg(L).property("ADBE Anchor Point").setValue([0, h / 2]);
    tg(L).property("ADBE Position").setValue([xc - w / 2, y]);
    L.motionBlur = true;
    key2(tg(L).property("ADBE Scale"), t0, [0, 100], t1, [100, 100], 90);
  }
  function ellipseMask(L, size, sub, cx, cy) {
    var m = L.property("ADBE Mask Parade").addProperty("ADBE Mask Atom");
    var s = new Shape(), r = size / 2, k = 0.5523;
    cx = (cx === undefined) ? L.source.width / 2 : cx;
    cy = (cy === undefined) ? L.source.height / 2 : cy;
    s.vertices = [[cx, cy - r], [cx + r, cy], [cx, cy + r], [cx - r, cy]];
    s.inTangents = [[-r * k, 0], [0, -r * k], [r * k, 0], [0, r * k]];
    s.outTangents = [[r * k, 0], [0, r * k], [-r * k, 0], [0, -r * k]];
    s.closed = true;
    m.property("ADBE Mask Shape").setValue(s);
    if (sub) m.maskMode = MaskMode.SUBTRACT;
    return m;
  }
  function circle(comp, name, x, y, d, color, op, ring) {
    var L = rect(comp, name, d, d, color, op, x, y);
    ellipseMask(L, d, false);
    if (ring) ellipseMask(L, d * 0.62, true);
    return L;
  }

  // ---- background stack -------------------------------------------------
  function addStill(comp, spec, baseOpacity) {
    if (!spec.still) return null;
    var item = proj.importFile(new ImportOptions(new File(spec.still)));
    try { item.mainSource.conformFrameRate = FPS; } catch (e) {}
    var S = span(comp.layers.add(item), spec.dur);
    var fill = Math.max(W / item.width, H / item.height) * 100;
    var st = tg(S);
    st.property("ADBE Anchor Point").setValue([item.width / 2, item.height / 2]);
    key2(st.property("ADBE Position"), 0, [W / 2 - 16, H / 2 + 8], spec.dur, [W / 2 + 16, H / 2 - 8], 20);
    key2(st.property("ADBE Scale"), 0, [fill, fill], spec.dur, [fill * 1.08, fill * 1.08], 25);
    if (baseOpacity !== undefined) st.property("ADBE Opacity").setValue(baseOpacity);
    return S;
  }
  function vignette(comp) {
    var v = rect(comp, "vignette", W, H, [0, 0, 0], 70, W / 2, H / 2);
    var m = v.property("ADBE Mask Parade").addProperty("ADBE Mask Atom");
    var s = new Shape(), rx = W * 0.62, ry = H * 0.62, cx = W / 2, cy = H / 2, k = 0.5523;
    s.vertices = [[cx, cy - ry], [cx + rx, cy], [cx, cy + ry], [cx - rx, cy]];
    s.inTangents = [[-rx * k, 0], [0, -ry * k], [rx * k, 0], [0, ry * k]];
    s.outTangents = [[rx * k, 0], [0, ry * k], [-rx * k, 0], [0, -ry * k]];
    s.closed = true;
    m.property("ADBE Mask Shape").setValue(s);
    m.maskMode = MaskMode.SUBTRACT;
    m.property("ADBE Mask Feather").setValue([260, 260]);
  }
  function vectorBed(comp, spec) {
    var glow = rect(comp, "glow", W, H, [0, 0, 0], 0, W / 2, H / 2);
    var gr = glow.property("ADBE Effect Parade").addProperty("ADBE Ramp");
    gr.property("ADBE Ramp-0001").setValue([W / 2, H * 0.98]);
    gr.property("ADBE Ramp-0002").setValue((spec && spec.accentMode === "dawn") ? DAWN : ACCENT);
    gr.property("ADBE Ramp-0003").setValue([W / 2, H * 0.35]);
    gr.property("ADBE Ramp-0004").setValue([0, 0, 0]);
    gr.property("ADBE Ramp-0005").setValue(2);
    glow.blendingMode = BlendingMode.ADD;
    tg(glow).property("ADBE Opacity").setValue((spec && spec.accentMode === "dawn") ? 16 : 12);
    vignette(comp);
    var sweep = rect(comp, "sweep", 340, H * 1.6, [1, 1, 1], 0, -300, H / 2);
    sweep.blendingMode = BlendingMode.ADD;
    sweep.motionBlur = true;
    tg(sweep).property("ADBE Rotate Z").setValue(18);
    key2(tg(sweep).property("ADBE Position"), 0.5, [-300, H / 2], 1.25, [W + 300, H / 2], 45);
    var so = tg(sweep).property("ADBE Opacity");
    so.setValueAtTime(0.5, 0); so.setValueAtTime(0.7, 10); so.setValueAtTime(1.25, 0);
  }
  function dip(comp, spec) {
    var d = rect(comp, "dip", W, H, [0, 0, 0], 0, W / 2, H / 2);
    var head = 4 / FPS, tail = 4 / FPS;
    var o = tg(d).property("ADBE Opacity");
    o.setValueAtTime(0, 100); o.setValueAtTime(head, 0);
    o.setValueAtTime(spec.dur - tail, 0); o.setValueAtTime(spec.dur, 100);
    ease(o, 40);
  }
  // R1 disclosure: burned on EVERY card, bottom-right.
  function disclosure(comp) {
    var L = text(comp, "AI-assisted visualization", FONT_LBL, 20, SILVER, 20);
    var r = srect(L, 0.1);
    tg(L).property("ADBE Position").setValue([W - 32 - r.width / 2, H - 34]);
    tg(L).property("ADBE Opacity").setValue(70);
  }
  function topLabel(comp, spec, y, size) {
    if (!spec.top || !spec.top.length) return null;
    var L = text(comp, spec.top, FONT_LBL, size || 46, SILVER, 340);
    fitText(L, 1728, comp.duration * 0.5);
    centerX(L, comp.duration * 0.5);
    revealUp(L, 0.2, W / 2, y, 46);
    return L;
  }
  function accentBar(comp, spec, y, w) {
    var L = rect(comp, "accent", w || 460, 6, mainAccent(spec), 95, W / 2, y);
    wipeIn(L, 0.55, 1.05, W / 2, y);
    tg(L).property("ADBE Opacity").setValue(95);
    return L;
  }
  function bottomLabel(comp, spec, t0, y, size) {
    if (!spec.bottom || !spec.bottom.length) return;
    var b = text(comp, spec.bottom, FONT_LBL, size || 54, WHITE, 120);
    fitText(b, 1728, comp.duration * 0.8); centerX(b, comp.duration * 0.8);
    revealUp(b, t0, W / 2, y, 46);
  }
  // mask cut-up reveal for a single line (overflow:hidden + translateY basic form)
  function subLabel(comp, spec, str, t0, y, size, color) {
    if (!str || !str.length) return null;
    var L = text(comp, str, FONT_LBL, size || 52, color || WHITE, 120);
    fitText(L, 1600, comp.duration * 0.85); centerX(L, comp.duration * 0.85);
    revealUp(L, t0, W / 2, y, 52);
    return L;
  }

  // ---- animated number (count-up) ---------------------------------------
  function countText(comp, spec, y) {
    var last = spec.numKeys[spec.numKeys.length - 1];
    var L = text(comp, last[1], FONT_NUM, spec.heroSize, mainAccent(spec), 0);
    fitText(L, 1728, last[0]);
    centerX(L, last[0]);
    L.motionBlur = true;
    tg(L).property("ADBE Position").setValue([W / 2, y]);
    var td = L.property("ADBE Text Properties").property("ADBE Text Document");
    var doc = td.value;
    for (var i = 0; i < spec.numKeys.length; i++) {
      doc.text = String(spec.numKeys[i][1]);
      td.setValueAtTime(spec.numKeys[i][0], doc);
    }
    var o = tg(L).property("ADBE Opacity");
    o.setValueAtTime(0.45, 0); o.setValueAtTime(0.60, 100);
    var sc = tg(L).property("ADBE Scale");
    sc.setValueAtTime(0.55, [46, 46]); sc.setValueAtTime(0.92, [112, 112]); sc.setValueAtTime(1.25, [100, 100]);
    ease(sc, 76);
    return L;
  }
  function heroStatic(comp, spec, y) {
    var L = text(comp, spec.heroText, FONT_NUM, spec.heroSize, mainAccent(spec), 4);
    fitText(L, 1728, comp.duration * 0.85);
    centerX(L, comp.duration * 0.85);
    L.motionBlur = true;
    tg(L).property("ADBE Position").setValue([W / 2, y]);
    var o = tg(L).property("ADBE Opacity");
    o.setValueAtTime(0.4, 0); o.setValueAtTime(0.56, 100);
    var sc = tg(L).property("ADBE Scale");
    sc.setValueAtTime(0.4, [118, 118]); sc.setValueAtTime(0.9, [100, 100]);
    ease(sc, 80);
    key2(tg(L).property("ADBE Position"), 0.4, [W / 2, y + 32], 0.9, [W / 2, y], 80);
    return L;
  }

  // ---- proven layouts (cleveland) --------------------------------------
  function buildActTitle(comp, spec) {
    topLabel(comp, spec, H * 0.235, 46);
    var L = text(comp, spec.main, FONT_NUM, spec.mainSize, mainAccent(spec), 6);
    fitText(L, 1728, comp.duration * 0.85);
    centerX(L, comp.duration * 0.85);
    L.motionBlur = true;
    tg(L).property("ADBE Position").setValue([W / 2, H * 0.46]);
    var o = tg(L).property("ADBE Opacity");
    o.setValueAtTime(0.4, 0); o.setValueAtTime(0.56, 100);
    var sc = tg(L).property("ADBE Scale");
    sc.setValueAtTime(0.4, [118, 118]); sc.setValueAtTime(0.9, [100, 100]);
    ease(sc, 80);
    key2(tg(L).property("ADBE Position"), 0.4, [W / 2, H * 0.46 + 36], 0.9, [W / 2, H * 0.46], 80);
    accentBar(comp, spec, H * 0.575, 640);
  }
  function buildCenter(comp, spec) {
    topLabel(comp, spec, H * 0.155, 46);
    if (spec.numKeys) countText(comp, spec, H * 0.49);
    else heroStatic(comp, spec, H * 0.49);
    accentBar(comp, spec, H * 0.60, 460);
    bottomLabel(comp, spec, 1.55, H * 0.70, 52);
  }
  function buildQuote(comp, spec) {
    topLabel(comp, spec, H * 0.20, 42);
    var wrapped = wrapText(spec.quote, 36);
    var L = text(comp, wrapped, FONT_LBL, 76, WHITE, 10);
    fitText(L, 1500, comp.duration * 0.7);
    centerBlock(L, comp.duration * 0.7);
    tg(L).property("ADBE Position").setValue([W / 2, H * 0.42]);
    var o = tg(L).property("ADBE Opacity");
    o.setValueAtTime(0.4, 0); o.setValueAtTime(0.62, 100);
    key2(tg(L).property("ADBE Position"), 0.4, [W / 2, H * 0.42 + 30], 0.95, [W / 2, H * 0.42], 80);
    var q1 = text(comp, String.fromCharCode(8220), FONT_NUM, 150, mainAccent(spec), 0);
    tg(q1).property("ADBE Position").setValue([W * 0.075, H * 0.34]);
    key2(tg(q1).property("ADBE Opacity"), 0.3, 0, 0.8, 55, 70);
    var q2 = text(comp, String.fromCharCode(8221), FONT_NUM, 150, mainAccent(spec), 0);
    tg(q2).property("ADBE Position").setValue([W * 0.925, H * 0.34]);
    key2(tg(q2).property("ADBE Opacity"), 0.4, 0, 0.9, 55, 70);
    accentBar(comp, spec, H * 0.66, 560);
    if (spec.attribution_display && spec.attribution_display.length) {
      var a = text(comp, spec.attribution_display, FONT_LBL, 42, SILVER, 160);
      fitText(a, 1500, comp.duration * 0.8); centerX(a, comp.duration * 0.8);
      revealUp(a, 1.3, W / 2, H * 0.72, 40);
    }
  }
  function buildVote(comp, spec) {
    topLabel(comp, spec, H * 0.19, 46);
    var yc = H * 0.44, gap = W * 0.20;
    var lx = W / 2 - gap, rx = W / 2 + gap;
    var nL = text(comp, spec.left, FONT_NUM, 260, SILVER, 0);
    nL.motionBlur = true;
    tg(nL).property("ADBE Position").setValue([lx, yc]);
    var loo = tg(nL).property("ADBE Opacity");
    loo.setValueAtTime(0.5, 0); loo.setValueAtTime(0.75, 100);
    key2(tg(nL).property("ADBE Scale"), 0.5, [60, 60], 0.9, [100, 100], 78);
    var nR = text(comp, spec.right, FONT_NUM, 220, mainAccent(spec), 0);
    nR.motionBlur = true;
    tg(nR).property("ADBE Position").setValue([rx, yc]);
    var roo = tg(nR).property("ADBE Opacity");
    roo.setValueAtTime(0.75, 0); roo.setValueAtTime(1.0, 100);
    key2(tg(nR).property("ADBE Scale"), 0.75, [60, 60], 1.15, [100, 100], 78);
    var to = text(comp, "TO", FONT_LBL, 48, SILVER, 120);
    tg(to).property("ADBE Position").setValue([W / 2, yc - 10]);
    key2(tg(to).property("ADBE Opacity"), 0.95, 0, 1.35, 70, 70);
    bottomLabel(comp, spec, 2.1, H * 0.75, 48);
  }
  function buildCompare(comp, spec) {
    topLabel(comp, spec, H * 0.20, 44);
    var yc = H * 0.45, gap = W * 0.20;
    var lx = W / 2 - gap, rx = W / 2 + gap;
    var nL = text(comp, spec.left, FONT_NUM, 150, WHITE, 0);
    fitText(nL, W * 0.40, comp.duration * 0.85);
    nL.motionBlur = true;
    tg(nL).property("ADBE Position").setValue([lx, yc]);
    var loo = tg(nL).property("ADBE Opacity");
    loo.setValueAtTime(0.5, 0); loo.setValueAtTime(0.75, 100);
    key2(tg(nL).property("ADBE Scale"), 0.5, [62, 62], 0.9, [100, 100], 78);
    var nR = text(comp, spec.right, FONT_NUM, 150, mainAccent(spec), 0);
    fitText(nR, W * 0.40, comp.duration * 0.85);
    nR.motionBlur = true;
    tg(nR).property("ADBE Position").setValue([rx, yc]);
    var roo = tg(nR).property("ADBE Opacity");
    roo.setValueAtTime(0.7, 0); roo.setValueAtTime(0.95, 100);
    key2(tg(nR).property("ADBE Scale"), 0.7, [62, 62], 1.1, [100, 100], 78);
    var dash = text(comp, String.fromCharCode(8596), FONT_NUM, 90, SILVER, 0); // <->
    tg(dash).property("ADBE Position").setValue([W / 2, yc - 6]);
    key2(tg(dash).property("ADBE Opacity"), 0.9, 0, 1.3, 80, 70);
    if (spec.strike && spec.strike.length) {
      var rj = text(comp, spec.strike, FONT_NUM, 92, mainAccent(spec), 20);
      fitText(rj, 1200, comp.duration * 0.8); centerX(rj, comp.duration * 0.8);
      rj.motionBlur = true;
      tg(rj).property("ADBE Rotate Z").setValue(-8);
      tg(rj).property("ADBE Position").setValue([W / 2, H * 0.635]);
      var ro = tg(rj).property("ADBE Opacity");
      ro.setValueAtTime(1.5, 0); ro.setValueAtTime(1.75, 100);
      key2(tg(rj).property("ADBE Scale"), 1.5, [150, 150], 1.9, [100, 100], 82);
    }
    bottomLabel(comp, spec, 2.15, H * 0.75, 46);
  }

  // ===================================================================
  // ===============  Tier-B bespoke set-piece layouts  ================
  // ===================================================================

  // B1 DNA_LADDER -- 5 no-match lanes, Reyes lane snaps in, cold-cyan flood.
  function buildDnaLadder(comp, spec) {
    topLabel(comp, spec, H * 0.14, 44);
    var MA = mainAccent(spec);
    var lanes = spec.lanes || 5;
    var laneW = 150, laneGap = 70, rungH = 16, rungN = 6, rungGap = 46;
    var totalW = lanes * laneW + (lanes - 1) * laneGap;
    var x0 = W / 2 - totalW / 2 + laneW / 2;
    var yBase = H * 0.66;
    // (3) five no-match lanes build bottom-up, staggered, DIM cyan, rungs offset
    for (var ln = 0; ln < lanes; ln++) {
      var lx = x0 + ln * (laneW + laneGap);
      var jitter = ((ln % 2) === 0) ? 10 : -14;   // rungs do not align across lanes
      for (var rr = 0; rr < rungN; rr++) {
        var ry = yBase - rr * rungGap + (rr % 2 ? jitter : -jitter);
        var rg = rect(comp, "rung_" + ln + "_" + rr, laneW, rungH, MA, 40, lx, ry);
        tg(rg).property("ADBE Anchor Point").setValue([0, rungH]);   // origin bottom
        rg.motionBlur = true;
        var t = 0.0 + ln * 0.18 + rr * 0.05;
        key2(tg(rg).property("ADBE Scale"), t, [100, 0], t + 0.32, [100, 100], 80);
        key2(tg(rg).property("ADBE Opacity"), t, 0, t + 0.2, 40, 70);
      }
    }
    // (5) Reyes lane slides in from the right, bright, snap-aligns into the gap
    var rxTarget = W / 2;
    var reyes = rect(comp, "reyes_lane", laneW, rungN * rungGap, MA, 0, rxTarget + 260, yBase - rungN * rungGap / 2);
    reyes.motionBlur = true;
    key2(tg(reyes).property("ADBE Position"), 2.5, [rxTarget + 260, yBase - rungN * rungGap / 2],
         4.0, [rxTarget, yBase - rungN * rungGap / 2], 90);
    var reo = tg(reyes).property("ADBE Opacity");
    reo.setValueAtTime(2.5, 0); reo.setValueAtTime(2.9, 92); reo.setValueAtTime(4.0, 92);
    // (6) single band pulse
    key2(tg(reyes).property("ADBE Scale"), 4.0, [100, 100], 4.6, [112, 112], 70);
    tg(reyes).property("ADBE Scale").setValueAtTime(5.2, [100, 100]);
    ease(tg(reyes).property("ADBE Scale"), 70);
    // (7) cold-cyan FLOOD
    var flood = rect(comp, "flood", W, H, MA, 0, W / 2, H / 2);
    flood.blendingMode = BlendingMode.ADD;
    var fo = tg(flood).property("ADBE Opacity");
    fo.setValueAtTime(5.5, 0); fo.setValueAtTime(6.4, 70); fo.setValueAtTime(7.5, 24);
    ease(fo, 60);
    // (8) sub label mask reveal, held
    subLabel(comp, spec, spec.sub, 7.5, H * 0.32, 60, WHITE);
    accentBar(comp, spec, H * 0.40, 620);
  }

  // B2 STAT_RESOLVE -- one-in-billions odometer (group:true) then held label.
  function buildStatResolve(comp, spec) {
    topLabel(comp, spec, H * 0.16, 46);
    countText(comp, spec, H * 0.47);
    accentBar(comp, spec, H * 0.60, 520);
    subLabel(comp, spec, spec.sub, 2.2, H * 0.70, 54, WHITE);
  }

  // B3 CARD_STACK -- five confession pages stack, arrows cite each other,
  //                   DNA report slides under, whole stack tilts (no foundation).
  function buildCardStack(comp, spec) {
    topLabel(comp, spec, H * 0.14, 44);
    var MA = mainAccent(spec);
    var pages = spec.pages || 5;
    var pw = 360, ph = 470, cx = W / 2, cy = H * 0.52;
    for (var i = 0; i < pages; i++) {
      var off = (i - (pages - 1) / 2) * 26;
      var pg = rect(comp, "page_" + i, pw, ph, [0.16, 0.17, 0.19], 100, cx + off, cy);
      pg.motionBlur = true;
      // thin cyan edge via a slightly larger backing solid
      var edge = rect(comp, "edge_" + i, pw + 6, ph + 6, MA, 22, cx + off, cy);
      edge.motionBlur = true;
      var t = 0.0 + i * 0.35;
      var rot = (i % 2 ? 3 : -3);
      tg(pg).property("ADBE Rotate Z").setValue(rot);
      tg(edge).property("ADBE Rotate Z").setValue(rot);
      key2(tg(pg).property("ADBE Position"), t, [cx + off, cy + 80], t + 0.5, [cx + off, cy], 80);
      key2(tg(edge).property("ADBE Position"), t, [cx + off, cy + 80], t + 0.5, [cx + off, cy], 80);
      key2(tg(pg).property("ADBE Opacity"), t, 0, t + 0.4, 100, 70);
      key2(tg(edge).property("ADBE Opacity"), t, 0, t + 0.4, 22, 70);
      // smear lines (illegible) so it reads as a document, not blank
      for (var s = 0; s < 4; s++) {
        var sm = rect(comp, "smear_" + i + "_" + s, pw * 0.66, 10, SILVER, 26,
                      cx + off, cy - ph * 0.28 + s * 46);
        tg(sm).property("ADBE Rotate Z").setValue(rot);
        key2(tg(sm).property("ADBE Opacity"), t + 0.2, 0, t + 0.5, 26, 70);
      }
    }
    // DNA report slides under the stack
    var dna = rect(comp, "dna_report", pw + 120, ph * 0.4, [0.10, 0.20, 0.24], 100, cx, cy + ph * 0.42);
    var de = rect(comp, "dna_edge", pw + 128, ph * 0.4 + 8, MA, 70, cx, cy + ph * 0.42);
    dna.motionBlur = true; de.motionBlur = true;
    key2(tg(dna).property("ADBE Position"), 3.0, [cx - 500, cy + ph * 0.42], 4.5, [cx, cy + ph * 0.42], 85);
    key2(tg(de).property("ADBE Position"), 3.0, [cx - 500, cy + ph * 0.42], 4.5, [cx, cy + ph * 0.42], 85);
    key2(tg(dna).property("ADBE Opacity"), 3.0, 0, 3.5, 100, 70);
    key2(tg(de).property("ADBE Opacity"), 3.0, 0, 3.5, 70, 70);
    // sub label
    subLabel(comp, spec, spec.sub, 4.6, H * 0.86, 54, WHITE);
  }

  // B4/B5 REC_LIGHT -- REC dot off (never lights) or on (illuminates dawn-amber).
  function buildRecLight(comp, spec) {
    topLabel(comp, spec, H * 0.18, 46);
    var on = (spec.mode === "on");
    var dotColor = on ? [0.30, 0.10, 0.06] : [0.18, 0.18, 0.20];
    var dot = circle(comp, "rec_dot", W / 2 - 120, H * 0.46, 120, dotColor, 100, false);
    dot.motionBlur = true;
    circle(comp, "rec_ring", W / 2 - 120, H * 0.46, 176, [0, 0, 0], 0, true)
      .property("ADBE Transform Group").property("ADBE Opacity").setValue(0);
    var ring = circle(comp, "rec_ring2", W / 2 - 120, H * 0.46, 176, SILVER, 60, true);
    var lbl = text(comp, "REC", FONT_LBL, 92, on ? DAWN : SILVER, 60);
    centerX(lbl, comp.duration * 0.5);
    tg(lbl).property("ADBE Position").setValue([W / 2 + 40, H * 0.46]);
    var lo = tg(lbl).property("ADBE Opacity");
    lo.setValueAtTime(0.3, 0); lo.setValueAtTime(0.8, on ? 100 : 70);
    key2(tg(lbl).property("ADBE Scale"), 0.3, [70, 70], 0.8, [100, 100], 78);
    if (on) {
      // dark -> illuminate: fill key to dawn-amber + glow up
      var dc = dot.property("ADBE Effect Parade").addProperty("ADBE Fill");
      dc.property("ADBE Fill-0002").setValueAtTime(0.8, [0.30, 0.10, 0.06]);
      dc.property("ADBE Fill-0002").setValueAtTime(1.6, DAWN);
      ease(dc.property("ADBE Fill-0002"), 70);
      var glow = rect(comp, "rec_glow", W, H, [0, 0, 0], 0, W / 2 - 120, H * 0.46);
      var gr = glow.property("ADBE Effect Parade").addProperty("ADBE Ramp");
      gr.property("ADBE Ramp-0001").setValue([W / 2 - 120, H * 0.46]);
      gr.property("ADBE Ramp-0002").setValue(DAWN);
      gr.property("ADBE Ramp-0003").setValue([W / 2 - 120, H * 0.10]);
      gr.property("ADBE Ramp-0004").setValue([0, 0, 0]);
      gr.property("ADBE Ramp-0005").setValue(1);
      glow.blendingMode = BlendingMode.ADD;
      var go = tg(glow).property("ADBE Opacity");
      go.setValueAtTime(1.2, 0); go.setValueAtTime(2.0, 60); ease(go, 60);
    } else {
      // dim: one tick that does NOT light
      var sc = tg(dot).property("ADBE Scale");
      sc.setValueAtTime(0.4, [100, 100]); sc.setValueAtTime(0.7, [115, 115]); sc.setValueAtTime(1.0, [100, 100]);
      ease(sc, 70);
    }
    accentBar(comp, spec, H * 0.62, 420);
    subLabel(comp, spec, spec.sub, 1.7, H * 0.72, 54, on ? BONE : WHITE);
  }

  // B6/B7 SCALE_TIP -- balance beam tips toward confession (wrong) or rights (evidence).
  function buildScaleTip(comp, spec) {
    topLabel(comp, spec, H * 0.16, 46);
    var MA = mainAccent(spec);
    var evid = (spec.mode === "evidence");
    var pivotX = W / 2, pivotY = H * 0.44;
    // fulcrum
    var post = rect(comp, "post", 14, H * 0.20, SILVER, 80, pivotX, pivotY + H * 0.10);
    // beam (rotates about center)
    var beam = rect(comp, "beam", 760, 16, MA, 95, pivotX, pivotY);
    beam.motionBlur = true;
    tg(beam).property("ADBE Anchor Point").setValue([760 / 2, 8]);
    // two pans hang from beam ends (approximate as blocks that move with the tip)
    var lPan = rect(comp, "pan_l", 150, 100, [0.16, 0.17, 0.19], 100, pivotX - 320, pivotY + 90);
    var rPan = rect(comp, "pan_r", 150, 100, [0.10, 0.20, 0.24], 100, pivotX + 320, pivotY + 90);
    lPan.motionBlur = true; rPan.motionBlur = true;
    var rz = tg(beam).property("ADBE Rotate Z");
    if (evid) {
      // rights itself: +14 -> 0 -> -2
      rz.setValueAtTime(0.5, 14); rz.setValueAtTime(2.2, 0); rz.setValueAtTime(3.0, -2);
      key2(tg(lPan).property("ADBE Position"), 0.5, [pivotX - 320, pivotY + 170], 2.2, [pivotX - 320, pivotY + 90], 70);
      key2(tg(rPan).property("ADBE Position"), 0.5, [pivotX + 320, pivotY + 20], 2.2, [pivotX + 320, pivotY + 90], 70);
    } else {
      // tips wrong way toward confession pan (left): 0 -> -14
      rz.setValueAtTime(0.5, 0); rz.setValueAtTime(2.5, -14);
      key2(tg(lPan).property("ADBE Position"), 0.5, [pivotX - 320, pivotY + 90], 2.5, [pivotX - 320, pivotY + 170], 70);
      key2(tg(rPan).property("ADBE Position"), 0.5, [pivotX + 320, pivotY + 90], 2.5, [pivotX + 320, pivotY + 20], 70);
    }
    ease(rz, 76);
    accentBar(comp, spec, H * 0.66, 460);
    subLabel(comp, spec, spec.sub, 2.6, H * 0.76, 50, evid ? BONE : WHITE);
  }

  // B8/B9 HERO_TIMELINE -- horizontal spine draws, year nodes pop (group:false literals).
  function buildHeroTimeline(comp, spec) {
    topLabel(comp, spec, H * 0.20, 46);
    var MA = mainAccent(spec);
    var years = spec.years || ["1989"];
    var y = H * 0.50;
    var x0 = W * 0.16, x1 = W * 0.84, spineW = x1 - x0;
    var spine = rect(comp, "spine", spineW, 8, MA, 90, x0 + spineW / 2, y);
    spine.motionBlur = true;
    tg(spine).property("ADBE Anchor Point").setValue([0, 4]);            // origin left
    tg(spine).property("ADBE Position").setValue([x0, y]);
    key2(tg(spine).property("ADBE Scale"), 0.2, [0, 100], 1.2, [100, 100], 80);
    var n = years.length;
    for (var i = 0; i < n; i++) {
      var nx = (n === 1) ? W / 2 : x0 + spineW * (i / (n - 1));
      var last = (i === n - 1);
      var nodeColor = (spec.phase === "resolve" && last) ? DAWN : MA;
      var node = circle(comp, "node_" + i, nx, y, 46, nodeColor, 100, true);
      node.motionBlur = true;
      var t = (spec.phase === "resolve") ? (1.2 + i * 0.5) : 1.0;
      key2(tg(node).property("ADBE Scale"), t, [0, 0], t + 0.35, [100, 100], 82);
      key2(tg(node).property("ADBE Opacity"), t, 0, t + 0.3, 100, 70);
      var yl = text(comp, years[i], FONT_NUM, 96, nodeColor, 2);   // literal string, no comma
      centerX(yl, comp.duration * 0.7);
      tg(yl).property("ADBE Position").setValue([nx, y - 90]);
      var ylo = tg(yl).property("ADBE Opacity");
      ylo.setValueAtTime(t + 0.1, 0); ylo.setValueAtTime(t + 0.45, 100);
      key2(tg(yl).property("ADBE Position"), t + 0.1, [nx, y - 60], t + 0.5, [nx, y - 90], 78);
    }
    subLabel(comp, spec, spec.sub, (spec.phase === "resolve") ? 3.6 : 1.8, y + H * 0.20, 56,
             (spec.accentMode === "dawn") ? BONE : WHITE);
  }

  // B10/B11 NAME_WALL -- five names+ages rise; close adds THE EXONERATED FIVE (dawn-amber).
  function buildNameWall(comp, spec) {
    topLabel(comp, spec, H * 0.12, 44);
    var MA = mainAccent(spec);
    var names = spec.names || [];
    var exon = (spec.mode === "exonerated");
    var y0 = exon ? H * 0.42 : H * 0.34;
    var rowH = H * 0.095;
    for (var i = 0; i < names.length; i++) {
      var ry = y0 + i * rowH;
      // overflow:hidden mask -- a clip band + text that translates up inside it
      var line = text(comp, names[i], FONT_NUM, 78, exon ? BONE : MA, 8);
      fitText(line, W * 0.72, comp.duration * 0.8);
      centerX(line, comp.duration * 0.8);
      line.motionBlur = true;
      var t = 0.0 + i * 0.4;
      key2(tg(line).property("ADBE Position"), t, [W / 2, ry + rowH * 0.9], t + 0.5, [W / 2, ry], 82);
      key2(tg(line).property("ADBE Opacity"), t, 0, t + 0.35, 100, 70);
    }
    if (exon) {
      var title = text(comp, spec.title, FONT_NUM, 120, DAWN, 6);
      fitText(title, W * 0.82, comp.duration * 0.85);
      centerX(title, comp.duration * 0.85);
      title.motionBlur = true;
      var ty = H * 0.24;
      key2(tg(title).property("ADBE Position"), 3.0, [W / 2, ty + 70], 3.6, [W / 2, ty], 82);
      key2(tg(title).property("ADBE Opacity"), 3.0, 0, 3.4, 100, 70);
      // accent underline wipe
      var ul = rect(comp, "underline", 620, 8, DAWN, 95, W / 2, ty + 78);
      wipeIn(ul, 3.5, 4.1, W / 2, ty + 78);
    } else {
      subLabel(comp, spec, spec.sub, 2.6, H * 0.86, 50, WHITE);
    }
  }

  // B12 SIGNATURE_ERASE -- signature strokes un-write, page blanks, label cyan->dawn.
  function buildSignatureErase(comp, spec) {
    topLabel(comp, spec, H * 0.16, 44);
    var MA = mainAccent(spec);
    // confession page
    var pw = 720, ph = 300, cx = W / 2, cy = H * 0.44;
    rect(comp, "sig_page", pw, ph, [0.16, 0.17, 0.19], 100, cx, cy);
    // signature strokes (illegible) -- built, then un-write tail->head
    var strokes = 9, sw = pw * 0.72 / strokes, sx0 = cx - pw * 0.34, sy = cy + ph * 0.10;
    for (var i = 0; i < strokes; i++) {
      var wob = (i % 2 ? -18 : 16);
      var st = rect(comp, "stroke_" + i, sw * 1.4, 12, WHITE, 92, sx0 + i * sw, sy + wob);
      st.motionBlur = true;
      tg(st).property("ADBE Rotate Z").setValue(wob * 0.6);
      // present at first, then vanish last -> first (reverse), staggered
      var t = 0.5 + (strokes - 1 - i) * 0.12;
      tg(st).property("ADBE Opacity").setValueAtTime(0.0, 92);
      tg(st).property("ADBE Opacity").setValueAtTime(t, 92);
      tg(st).property("ADBE Opacity").setValueAtTime(t + 0.28, 0);
      ease(tg(st).property("ADBE Opacity"), 60);
      // ink lifts up as it erases
      key2(tg(st).property("ADBE Position"), t, [sx0 + i * sw, sy + wob], t + 0.28, [sx0 + i * sw, sy + wob - 30], 70);
    }
    // resolve label: color key cyan -> dawn-amber (first warm)
    var lbl = text(comp, spec.sub, FONT_LBL, 60, MA, 80);
    fitText(lbl, 1500, comp.duration * 0.9); centerX(lbl, comp.duration * 0.9);
    tg(lbl).property("ADBE Position").setValue([W / 2, H * 0.72 + 52]);
    var lo = tg(lbl).property("ADBE Opacity");
    lo.setValueAtTime(5.0, 0); lo.setValueAtTime(5.4, 100);
    key2(tg(lbl).property("ADBE Position"), 5.0, [W / 2, H * 0.72 + 52], 5.6, [W / 2, H * 0.72], 80);
    var fc = lbl.property("ADBE Effect Parade").addProperty("ADBE Fill");
    fc.property("ADBE Fill-0002").setValueAtTime(5.4, ACCENT);
    fc.property("ADBE Fill-0002").setValueAtTime(5.9, DAWN);
    ease(fc.property("ADBE Fill-0002"), 70);
    var ul2 = rect(comp, "sig_underline", 560, 8, DAWN, 95, W / 2, H * 0.72 + 44);
    wipeIn(ul2, 5.5, 6.0, W / 2, H * 0.72 + 44);
  }

  // ---- dispatch ---------------------------------------------------------
  function build(spec) {
    var comp = proj.items.addComp("CENTRALPARK_" + spec.id, W, H, 1.0, spec.dur, FPS);
    comp.motionBlur = true;
    rect(comp, "bg", W, H, INK, 100, W / 2, H / 2);
    vectorBed(comp, spec);
    if (spec.layout === "ACT_TITLE_CARD") buildActTitle(comp, spec);
    else if (spec.layout === "CENTER_STACK" || spec.layout === "MONEY_STACK") buildCenter(comp, spec);
    else if (spec.layout === "QUOTE_CARD") buildQuote(comp, spec);
    else if (spec.layout === "VOTE_SPLIT") buildVote(comp, spec);
    else if (spec.layout === "SPLIT_COMPARE") buildCompare(comp, spec);
    else if (spec.layout === "DNA_LADDER") buildDnaLadder(comp, spec);
    else if (spec.layout === "STAT_RESOLVE") buildStatResolve(comp, spec);
    else if (spec.layout === "CARD_STACK") buildCardStack(comp, spec);
    else if (spec.layout === "REC_LIGHT") buildRecLight(comp, spec);
    else if (spec.layout === "SCALE_TIP") buildScaleTip(comp, spec);
    else if (spec.layout === "HERO_TIMELINE") buildHeroTimeline(comp, spec);
    else if (spec.layout === "NAME_WALL") buildNameWall(comp, spec);
    else if (spec.layout === "SIGNATURE_ERASE") buildSignatureErase(comp, spec);
    else throw new Error("unsupported layout " + spec.layout + " on " + spec.id);
    disclosure(comp);   // R1 -- always on top
    dip(comp, spec);
    return comp;
  }

  var rq = proj.renderQueue;
  while (rq.numItems > 0) rq.item(1).remove();
  var built = 0;
  for (var bi = 0; bi < BEATS.length; bi++) {
    var comp = build(BEATS[bi]);
    built++;
    var it = rq.items.add(comp);
    try { it.applyTemplate("最良設定"); }
    catch (e) { try { it.applyTemplate("Best Settings"); } catch (e2) {} }
    var om = it.outputModule(1), omOK = false;
    var omNames = ["H.264 - レンダリング設定を一致 - 15 Mbps",
                   "H.264 - Match Render Settings - 15 Mbps"];
    for (var oi = 0; oi < omNames.length && !omOK; oi++) {
      try { om.applyTemplate(omNames[oi]); omOK = true; } catch (e3) {}
    }
    if (!omOK) throw new Error("no H.264 output module template matched");
    om.file = new File(BEATS[bi].out);
  }
  app.project.save(new File("__AEP__"));
  app.endUndoGroup();
  var mk = new File(RENDER_DIR + "/_build_ok.txt");
  mk.open("w");
  mk.write("comps=" + built + " queue=" + rq.numItems + " fonts: " + FONT_LOG);
  mk.close();
  try { app.quit(); } catch (e) {}
  } catch (err) {
    fail(String(err) + " line=" + String(err.line || "") + " file=" + String(err.fileName || ""));
  }
})();
"""


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--dryrun", action="store_true")
    ap.add_argument("--only", default=None,
                    help="build a single-comp deck for one layout (Tier-B proving)")
    ap.add_argument("--beat", default=None,
                    help="build a single-comp deck for one beat id (mode-variant proving)")
    args = ap.parse_args()
    raise SystemExit(build(args.dryrun, args.only, args.beat))
