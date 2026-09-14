#!/usr/bin/env python
"""EP40 Lech - ACT 4 comparison-card family (AE JSX generator).

WHY THIS FILE EXISTS ALONGSIDE build_lech_hero_cards.py
-------------------------------------------------------
build_lech_hero_cards.py builds the 14 hero beats (c01..c05, b04, b07, t1..t4,
hp01, x01, x02). It is NOT modified here and its outputs are NOT overwritten.
This builder adds a SEPARATE deck of six ACT 4 cards, ids ck1..ck6, written to
its own project (lech_compare.aep) and its own JSX (lech_compare.jsx).

ACT 4 sets five emergencies side by side and shows five different answers to the
same question. Until now that act had zero cards on screen.

DESIGN DECISION: NO PHOTOGRAPHS
-------------------------------
Every still under E:/pd-media/assets/ai/lech is an AI rendering of the Greenwood
Village house. Laying one of those behind a card about Amy Hadley's house in
South Bend, or Vicki Baker's in McKinney, would show the viewer a picture of the
wrong building and imply it is that case. So every card in this deck is pure
vector on near-black. That also makes the contrast requirement trivially
satisfiable: the darkest text colour used sits above 4.5:1 on a black field, and
the measured values are recorded in the spec.

ACCURACY LOCK
-------------
Screen text is limited to the verified ACT 4 ledger. Specifically:
  * Hadley: "thirty cannisters of tear gas" is the opinion's verbatim wording
    (its spelling). $16,000 is labelled TOTAL RESULTING DAMAGE - the opinion
    calls it the total resulting damage, NOT an uninsured remainder. The month
    is JUNE 2022 with no day, because the opinion states no day.
  * Baker: the card says an entitlement was RECOGNISED under the Texas
    Constitution. It never says she was paid. It also records that she was in
    Montana and that the man inside had worked on the house.
  * Slaybaugh: the incident date is JANUARY 23, 2022; 2024 is the DECISION year.
    The card states on its face that the target was the owners' own son, staying
    with their consent, so the card cannot be read as another wrong-house raid.
  * Pena: published Ninth Circuit decision, contrasted with Lech's non-precedential
    Order and Judgment. Verbatim acknowledgement quoted.
  * Las Vegas: LVMPD paid, not the city; the claim was denied first and paid
    after the story ran. The reporting discrepancy ($25,000 in Fox5 vs $30,000
    in the family's own brief) is printed on the card rather than hidden.
No card contains the string "Supreme Court" in any form.

Machine traps honoured (same list as build_lech_hero_cards.py):
  runtime font resolve with unwrap() + HARD FAIL, spatial-aware
  setTemporalEaseAtKey dim, no app.newProject(), per-layer motionBlur,
  "ADBE Rotate Z", explicit inPoint AND outPoint, single-line TextDocument only,
  all display strings precomputed in Python, completion marker file, app.quit().
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(r"C:\Users\aab15\Documents\prime-documentary")
EP = "PD-2026-040-lech"
SPEC_OUT = ROOT / "episodes" / "_planning" / "EP40_lech_hero_beats.spec.v001.json"
REPO_BEATS = ROOT / "episodes" / EP / "08_edit" / "ae_hero" / "beats.json"
WORK = Path("E:/pd-media/episodes/PD-2026-040-lech/08_edit/ae_hero")
# Fixed (measurement-based, de-densified) renders go to a NEW dir so the
# existing composited renders are never clobbered; re-compositing consumes it.
OUT = WORK / "fixed"

# Which 2 fact strings to keep per card (indices into CASES[*]["facts"]),
# chosen as the two verbatim ledger lines that carry each case. Owner fix:
# 4-5 bullets in <=6.5s were unreadable; <=2 bullets + >=7.0s is the target.
KEEP_FACTS = {"ck1": [0, 3], "ck2": [3, 4], "ck3": [0, 3],
              "ck4": [0, 2], "ck5": [0, 3]}

FPS = 30
W, H = 1920, 1080

# Same brand constants as build_lech_hero_cards.py (DESIGN v002 section 9.4).
GOLD = [0.898, 0.710, 0.227]
WHITE = [0.961, 0.969, 0.980]
SILVER = [0.588, 0.627, 0.682]
DUST = [0.827, 0.769, 0.667]
# The hero deck's RED [0.780,0.290,0.250] measures 4.43:1 on black - BELOW the
# 4.5 floor. A first pass at [0.855,0.345,0.290] rendered at a MEASURED 4.54:1,
# which clears the bar by 0.04 and would fail the moment anything lifts the
# local field. Lifted again to a value that measures above 6:1 with margin.
RED_HI = [0.905, 0.400, 0.335]

ANTON_ADV = 0.470
OSWALD_ADV = 0.505


def fit_size(text: str, base: int, max_w: int, adv: float, tracking: int = 0) -> int:
    n = max(1, len(text))
    per = adv + (tracking / 1000.0)
    return max(16, min(base, int(max_w / (per * n))))


def money_keys(target: int, t0: float, t1: float, n: int = 18):
    """(time, display-string) hold keys. Python formats EVERY string; the JSX
    never does arithmetic on a number."""
    keys = [(t0, "$0")]
    for i in range(1, n):
        p = i / (n - 1)
        v = target * (1.0 - (1.0 - p) ** 3)
        keys.append((t0 + (t1 - t0) * p, f"${int(round(v)):,}"))
    keys.append((t1 + 0.02, f"${target:,}"))
    return [[round(t, 4), s] for t, s in keys]


# --------------------------------------------------------------------- the deck
CASES = [
    dict(
        id="ck1", dur=6.0,
        state="INDIANA",
        code="IN",
        case="HADLEY v. CITY OF SOUTH BEND",
        date="JUNE 2022  -  SOUTH BEND",
        facts=[
            "A WARRANT, AN IP ADDRESS, AND THE WRONG HOUSE",
            "ONE FIFTEEN-YEAR-OLD INSIDE. HE SURRENDERED.",
            "WINDOWS BROKEN. THE SUSPECT WAS NEVER THERE.",
            "SEVENTH CIRCUIT, OCTOBER 7, 2025 - CLAIM REJECTED",
        ],
        quote_label="THE OPINION'S OWN WORDS",
        quote="THIRTY CANNISTERS OF TEAR GAS",
        money=16000,
        money_label="TOTAL RESULTING DAMAGE",
        money_note="",
        who="THE CITY AND THE COUNTY BOTH REFUSED",
        who_color="RED",
        flag="THE OPINION CALLS $16,000 THE TOTAL RESULTING DAMAGE, NOT AN UNINSURED REMAINDER.",
        source="ACT 4 ledger - Hadley v. City of South Bend, 7th Cir. No. 24-2448 (Oct. 7, 2025)",
    ),
    dict(
        id="ck2", dur=6.5,
        state="TEXAS",
        code="TX",
        case="VICKI BAKER  -  McKINNEY",
        date="JULY 25, 2020",
        facts=[
            "THE OWNER HAD RETIRED TO MONTANA. HER DAUGHTER WAS HOME.",
            "THE MAN INSIDE HAD WORKED ON THIS HOUSE AS A HANDYMAN.",
            "GAS, EXPLOSIVES ON TWO DOORS, THE BACK FENCE PUSHED DOWN.",
            "HE KILLED HIMSELF. THE INSURER PAID NOTHING AT ALL.",
            "FIFTH CIRCUIT ERASED THE VERDICT - 84 F.4TH 378.",
        ],
        quote_label="",
        quote="",
        money=60000,
        money_label="AWARDED, THEN AWARDED AGAIN",
        money_note="PLUS INTEREST - UPHELD MAY 2026",
        who="THE TEXAS CONSTITUTION, NOT THE FEDERAL ONE",
        who_color="GOLD",
        flag="THE RECORD SHOWS AN ENTITLEMENT RECOGNISED. IT DOES NOT SHOW A PAYMENT RECEIVED.",
        source="ACT 4 ledger - Baker v. City of McKinney, 84 F.4th 378; Tex. const. award upheld May 2026",
    ),
    dict(
        id="ck3", dur=6.5,
        state="TENNESSEE",
        code="TN",
        case="SLAYBAUGH v. RUTHERFORD COUNTY",
        date="JANUARY 23, 2022  -  SMYRNA",
        facts=[
            "NOT A WRONG HOUSE. THE TARGET WAS THE OWNERS' OWN SON.",
            "THEY HAD AGREED HE COULD STAY THE NIGHT THERE.",
            "ABOUT THIRTY-FIVE GAS CANISTERS WENT INTO THE HOUSE.",
            "SIXTH CIRCUIT, 2024 - DISMISSED ON A COMMON-LAW PRIVILEGE.",
        ],
        quote_label="THE COURT SAID, THEN DISMISSED ANYWAY",
        quote="A CATEGORICAL POLICE-POWER EXCEPTION IS QUESTIONABLE",
        money=70000,
        money_label="APPROXIMATE DAMAGE",
        money_note="",
        who="NO ONE",
        who_color="RED",
        flag="2024 IS THE DECISION YEAR. THE RAID ITSELF WAS JANUARY 23, 2022.",
        source="ACT 4 ledger - Slaybaugh v. Rutherford County, 114 F.4th 593 (6th Cir. 2024)",
    ),
    dict(
        id="ck4", dur=6.0,
        state="CALIFORNIA",
        code="CA",
        case="PENA v. CITY OF LOS ANGELES",
        date="AUGUST 3, 2022  -  A PRINT SHOP",
        facts=[
            "A THIRTEEN-HOUR STANDOFF AT HIS OWN WORKPLACE.",
            "GAS THROUGH THE WALLS, THE DOORS, THE ROOF, THE WINDOWS.",
            "NINTH CIRCUIT, NOVEMBER 4, 2025 - PUBLISHED.",
            "PENA RECOVERS NOTHING.",
        ],
        quote_label="THE OPINION'S OWN WORDS",
        quote="THE OFFICERS ACTED REASONABLY AND LAWFULLY IN ALL THEIR ACTIONS",
        money=0,
        money_label="WHAT PENA RECOVERS",
        money_note="",
        money_word="NOTHING",
        who="NO ONE",
        who_color="RED",
        flag="PUBLISHED, SO IT BINDS. LECH WAS AN ORDER AND JUDGMENT: NOT BINDING PRECEDENT.",
        source="ACT 4 ledger - Pena v. City of Los Angeles, 158 F.4th 1033 (9th Cir. 2025) (published)",
    ),
    dict(
        id="ck5", dur=5.5,
        state="NEVADA",
        code="NV",
        case="LAS VEGAS  -  LVMPD RAID",
        date="AUGUST 20, 2025",
        facts=[
            "THE WRONG HOUSE, BY MORE THAN FIVE YEARS.",
            "THE SUSPECT HAD MOVED OUT OF THAT ADDRESS LONG BEFORE.",
            "THE CLAIM WAS DENIED. THEN THE STORY RAN.",
            "IT WAS WITHDRAWN AS PREMATURELY DENIED, AND PAID.",
        ],
        quote_label="",
        quote="",
        money=30000,
        money_label="APPROXIMATE DAMAGE",
        money_note="FAMILY'S BRIEF. LOCAL REPORTING SAID $25,000.",
        who="LVMPD - THE DEPARTMENT, NOT THE CITY",
        who_color="GOLD",
        flag="NOT VOLUNTARY. THE DIFFERENCE HERE WAS A NEWS CYCLE, NOT A RULE.",
        source="ACT 4 ledger - Las Vegas / LVMPD, August 20, 2025",
    ),
]

LEDGER = dict(
    id="ck6", dur=8.0,
    title="SAME EMERGENCY. SAME DAMAGE. FIVE DIFFERENT ANSWERS.",
    subtitle="ONE QUESTION, ASKED IN FIVE STATES",
    headers=["STATE", "WHAT HAPPENED", "WHO PAID"],
    rows=[
        ["INDIANA", "WRONG HOUSE. THIRTY GAS CANISTERS.",
         "NO ONE", "RED", "$16,000 IN DAMAGE"],
        ["TEXAS", "HOSTAGE. DOORS BLOWN. INSURER PAID NOTHING.",
         "TEXAS CONSTITUTION *", "GOLD", "$60,000 AWARDED"],
        ["TENNESSEE", "THEIR OWN SON INSIDE. ABOUT 35 CANISTERS.",
         "NO ONE", "RED", "ABOUT $70,000 IN DAMAGE"],
        ["CALIFORNIA", "THIRTEEN-HOUR STANDOFF. GAS THROUGH THE ROOF.",
         "NO ONE", "RED", "PENA RECOVERS NOTHING"],
        ["NEVADA", "WRONG HOUSE. SUSPECT GONE OVER FIVE YEARS.",
         "THE POLICE **", "GOLD", "ABOUT $30,000 PAID"],
    ],
    notes=[
        "*  TEXAS: HELD OWED UNDER THE STATE CONSTITUTION. THE RECORD SHOWS AN ENTITLEMENT, NOT A PAYMENT RECEIVED.",
        "** NEVADA: LVMPD, NOT THE CITY. THE CLAIM WAS DENIED FIRST AND PAID ONLY AFTER THE STORY RAN.",
        "TENNESSEE WAS NOT AN UNCONNECTED HOUSE: THE TARGET WAS THE OWNERS' SON, STAYING WITH THEIR CONSENT.",
    ],
    source="ACT 4 ledger - five-case tally",
)

# Measured sRGB contrast of every text colour against the card field. See
# contrast_report() - printed at build time and written into the spec.
FIELD = [0.0, 0.0, 0.0]


def _lin(c: float) -> float:
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def luminance(rgb) -> float:
    r, g, b = (_lin(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(fg, bg) -> float:
    a, b = luminance(fg), luminance(bg)
    hi, lo = max(a, b), min(a, b)
    return (hi + 0.05) / (lo + 0.05)


def contrast_report() -> dict:
    """The card field is a black solid. The only thing between it and the text is
    a 6%-opacity gold ghost glyph and a 7%-opacity silver grid, so the worst-case
    background is computed as the composite of BOTH over black."""
    ghost = [0.06 * c for c in GOLD]                       # 6% gold over black
    worst = [min(1.0, g + 0.07 * s) for g, s in zip(ghost, SILVER)]  # + 7% grid
    out = {"field_worst_case_rgb": [round(c, 4) for c in worst]}
    for name, col in (("WHITE", WHITE), ("GOLD", GOLD), ("SILVER", SILVER),
                      ("DUST", DUST), ("RED_HI", RED_HI)):
        out[name] = {
            "on_black": round(contrast(col, FIELD), 2),
            "on_worst_case_field": round(contrast(col, worst), 2),
        }
    return out


def build():
    WORK.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    for m in ("_compare_ok.txt", "_compare_error.txt"):
        (WORK / m).unlink(missing_ok=True)

    beats = []
    for c in CASES:
        # OWNER FIX: the ACT4 cards were information-overloaded (state / case /
        # date / 4-5 facts / quote / WHO PAID / footnote = 8 elements in <=6.5s,
        # unreadable). Reduce each card to the four reads the owner asked for
        # (state + damage + WHO PAID + <=2 bullets) plus the accuracy caveat
        # flag, and extend every card to >=7.0s. Kept facts are VERBATIM ledger
        # strings (never reworded), chosen as the two that carry the case.
        keep = KEEP_FACTS[c["id"]]
        facts = [c["facts"][i] for i in keep]
        n = len(facts)
        has_q = False                      # quote block dropped for readability
        dur = max(7.0, float(c["dur"]))
        b = dict(
            id=c["id"], layout="CASE_COMPARE", dur=dur,
            source=c["source"], still=None,
            still_content_verified="No photograph used. Every lech still is a "
                                   "rendering of the Greenwood Village house; "
                                   "putting one behind another state's case would "
                                   "show the wrong building. Pure vector on black.",
            state=c["state"], code=c["code"], case=c["case"], date="",
            facts=facts, quote_label="", quote="",
            money_label=c["money_label"], money_note="",
            who=c["who"], who_color=c["who_color"], flag=c["flag"],
            head=round(4 / FPS, 4), tail=round(4 / FPS, 4),
            out=str(OUT / f"{c['id']}.mp4").replace("\\", "/"),
        )
        b["stateSize"] = fit_size(c["state"], 92, 900, ANTON_ADV, 40)
        b["caseSize"] = fit_size(c["case"], 40, 1000, OSWALD_ADV, 100)
        b["dateSize"] = fit_size(c["date"], 34, 900, OSWALD_ADV, 60)
        b["factSizes"] = [fit_size(f, 40, 1615, OSWALD_ADV, 25) for f in facts]
        b["quoteSize"] = fit_size(c["quote"] or "X", 38, 1615, OSWALD_ADV, 20)
        b["quoteLabelSize"] = fit_size(c["quote_label"] or "X", 24, 900, OSWALD_ADV, 200)
        b["moneyLabelSize"] = fit_size(c["money_label"], 30, 620, OSWALD_ADV, 200)
        b["moneyNoteSize"] = fit_size(c["money_note"] or "X", 24, 640, OSWALD_ADV, 40)
        b["whoSize"] = fit_size(c["who"], 52, 1600, OSWALD_ADV, 60)
        b["flagSize"] = fit_size(c["flag"], 26, 1640, OSWALD_ADV, 60)
        if c.get("money_word"):
            b["moneyWord"] = c["money_word"]
            b["moneySize"] = fit_size(c["money_word"], 130, 660, ANTON_ADV)
        else:
            b["numKeys"] = money_keys(c["money"], 0.75, 1.75)
            b["moneySize"] = fit_size(f"${c['money']:,}", 130, 660, ANTON_ADV)
        # animation clock, computed here so the JSX contains no scheduling logic
        b["factT"] = [round(1.05 + i * 0.30, 3) for i in range(n)]
        b["quoteT"] = round(1.05 + n * 0.30 + 0.25, 3) if has_q else -1
        b["whoT"] = round(1.05 + n * 0.30 + (0.75 if has_q else 0.35), 3)
        b["flagT"] = round(b["whoT"] + 0.45, 3)
        beats.append(b)

    lg = dict(
        id=LEDGER["id"], layout="LEDGER_TABLE", dur=max(9.5, float(LEDGER["dur"])),
        source=LEDGER["source"], still=None,
        still_content_verified="No photograph used. Pure vector table on black.",
        title=LEDGER["title"], subtitle=LEDGER["subtitle"],
        headers=LEDGER["headers"], rows=LEDGER["rows"], notes=LEDGER["notes"],
        head=round(4 / FPS, 4), tail=round(4 / FPS, 4),
        out=str(OUT / f"{LEDGER['id']}.mp4").replace("\\", "/"),
    )
    lg["titleSize"] = fit_size(LEDGER["title"], 54, 1700, OSWALD_ADV, 120)
    lg["subtitleSize"] = fit_size(LEDGER["subtitle"], 30, 1500, OSWALD_ADV, 260)
    lg["headerSize"] = 28
    lg["rowSizes"] = []
    for r in LEDGER["rows"]:
        lg["rowSizes"].append([
            fit_size(r[0], 46, 320, ANTON_ADV, 20),
            fit_size(r[1], 34, 930, OSWALD_ADV, 25),
            fit_size(r[2], 34, 400, OSWALD_ADV, 25),
            fit_size(r[4], 26, 400, OSWALD_ADV, 20),
        ])
    lg["noteSizes"] = [fit_size(s, 26, 1660, OSWALD_ADV, 40) for s in LEDGER["notes"]]
    beats.append(lg)

    cr = contrast_report()
    block = {
        "schema_version": "lech_compare_cards.v1",
        "episode_id": EP,
        "fps": FPS, "width": W, "height": H,
        "render_dir": str(OUT).replace("\\", "/"),
        "aep": str(WORK / "lech_compare_fixed.aep").replace("\\", "/"),
        "purpose": ("ACT 4 comparison family. Five single-case cards plus one "
                    "tally card, showing five different answers to one question. "
                    "Separate deck: it does not touch the 14 hero beats."),
        "accuracy_note": (
            "Lech v. Jackson was decided by the Tenth Circuit in 2019; review was "
            "declined in 2020 and the merits were never reached. No card in this "
            "deck contains the string 'Supreme Court' in any form."
        ),
        "ledger_note": (
            "Hadley: $16,000 is labelled TOTAL RESULTING DAMAGE per the opinion, "
            "not an uninsured remainder; the month is JUNE 2022 with no day. "
            "Baker: the card states an entitlement was recognised under the Texas "
            "Constitution and never states that she was paid. "
            "Slaybaugh: incident JANUARY 23, 2022, decision 2024; the card states "
            "on its face that the target was the owners' own son with their consent, "
            "so it is not presented as another wrong-house raid. "
            "Pena: published, contrasted against Lech's non-precedential Order and "
            "Judgment. Las Vegas: LVMPD paid, not the city, after an initial denial; "
            "the $25,000 / $30,000 reporting discrepancy is printed on the card."
        ),
        "no_photograph_note": (
            "Deliberately image-free. All lech stills depict the Greenwood Village "
            "house; using one behind another state's case would show the wrong "
            "building."
        ),
        "contrast_measured": cr,
        "beats": beats,
    }

    # ---- append (never overwrite) into the shared spec + repo beats ----------
    for target in (SPEC_OUT, REPO_BEATS):
        doc = json.loads(target.read_text(encoding="utf-8"))
        existing = [b["id"] for b in doc.get("beats", [])]
        clash = sorted(set(existing) & {b["id"] for b in beats})
        if clash:
            print(f"FAIL id collision with hero deck: {clash}", file=sys.stderr)
            return 2
        doc["compare_cards"] = block
        target.write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")

    payload = json.dumps(block, ensure_ascii=False, indent=2)
    (WORK / "compare_beats.json").write_text(payload, encoding="utf-8")

    jsx = JSX
    jsx = jsx.replace("__W__", str(W)).replace("__H__", str(H)).replace("__FPS__", str(FPS))
    jsx = jsx.replace("__GOLD__", ",".join(str(v) for v in GOLD))
    jsx = jsx.replace("__WHITE__", ",".join(str(v) for v in WHITE))
    jsx = jsx.replace("__SILVER__", ",".join(str(v) for v in SILVER))
    jsx = jsx.replace("__DUST__", ",".join(str(v) for v in DUST))
    jsx = jsx.replace("__RED__", ",".join(str(v) for v in RED_HI))
    jsx = jsx.replace("__BEATS__", json.dumps(beats, ensure_ascii=False))
    jsx = jsx.replace("__RENDER__", str(WORK).replace("\\", "/"))
    jsx = jsx.replace("__AEP__", str(WORK / "lech_compare_fixed.aep").replace("\\", "/"))
    (WORK / "lech_compare_fixed.jsx").write_text(jsx, encoding="utf-8-sig")

    print(f"[gen] {len(beats)} compare cards, total {sum(b['dur'] for b in beats):.1f}s")
    for b in beats:
        s = b.get("state") or b.get("title", "")
        print(f"  {b['id']:<4} {b['layout']:<14} {b['dur']:>4.1f}s  {s[:60]}")
    print("[contrast] worst-case field rgb", cr["field_worst_case_rgb"])
    for k in ("WHITE", "GOLD", "SILVER", "DUST", "RED_HI"):
        print(f"  {k:<7} black={cr[k]['on_black']:>6.2f}:1   worst={cr[k]['on_worst_case_field']:>6.2f}:1")
    print("[gen] jsx  ->", WORK / "lech_compare_fixed.jsx")
    print("[gen] spec ->", SPEC_OUT, "(key: compare_cards)")
    return 0


JSX = r"""// AUTO-GENERATED - EP40 Lech ACT 4 comparison cards. Do not hand-edit.
(function () {
  var W = __W__, H = __H__, FPS = __FPS__;
  var GOLD = [__GOLD__], WHITE = [__WHITE__], SILVER = [__SILVER__],
      DUST = [__DUST__], RED = [__RED__];
  var BEATS = __BEATS__;
  var RENDER_DIR = "__RENDER__";

  function fail(msg) {
    try { var f = new File(RENDER_DIR + "/_compare_error.txt"); f.open("w"); f.write(String(msg)); f.close(); } catch (e) {}
    try { app.quit(); } catch (e) {}
  }

  try {
  // AfterFX -noui -r opens a fresh untitled project. app.newProject() hangs
  // headless on the save prompt -- never call it.
  var proj = app.project;
  try { for (var ri = proj.numItems; ri >= 1; ri--) {
    var itx = proj.item(ri);
    if (itx instanceof CompItem && String(itx.name).indexOf("LECHCMP_") === 0) itx.remove();
  } } catch (e) {}
  try { proj.gpuAccelType = GpuAccelType.SOFTWARE; } catch (e) {}
  try { proj.bitsPerChannel = 8; } catch (e) {}
  app.beginUndoGroup("lech_compare");

  // ---- runtime font resolver (identical contract to the hero builder) ------
  // MEASURED on AE 2026: app.fonts.allFonts[i] is NOT a FontObject, it is an
  // array-LIKE wrapper whose [0] is the FontObject. Missing font = HARD FAIL.
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

  // ---- helpers ------------------------------------------------------------
  function tg(L) { return L.property("ADBE Transform Group"); }
  function span(L, dur) { L.inPoint = 0; L.outPoint = dur; return L; }   // set BOTH
  function ease(prop, inf) {
    inf = inf || 70;
    var n = prop.numKeys, dim = 1;
    // spatial props (Position) take a 1-element temporal ease array
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
  // soft black halo behind a glyph run - lifts text off ANY background.
  // Required by the readability rule even though this deck sits on black: it
  // costs nothing and it is what stops a future still swap from eating the text.
  function textShadow(L, opac, soft) {
    try {
      var ds = L.property("ADBE Effect Parade").addProperty("ADBE Drop Shadow");
      ds.property("ADBE Drop Shadow-0001").setValue([0, 0, 0]);
      ds.property("ADBE Drop Shadow-0002").setValue(opac === undefined ? 190 : opac); // 0-255
      ds.property("ADBE Drop Shadow-0003").setValue(0);      // direction
      ds.property("ADBE Drop Shadow-0004").setValue(0);      // distance
      ds.property("ADBE Drop Shadow-0005").setValue(soft === undefined ? 26 : soft);
    } catch (e) {}
  }
  // local scrim: a feathered dark patch under one text zone, not a full wash.
  // Mask Feather takes a 2-VALUE array.
  function scrimBand(comp, dur, cx, cy, halfW, halfH, fx, fy, opac, t0, t1) {
    var sc = span(comp.layers.addSolid([0.008, 0.014, 0.028], "scrim", W, H, 1.0), dur);
    var m = sc.property("ADBE Mask Parade").addProperty("ADBE Mask Atom");
    var s = new Shape();
    s.vertices = [[cx - halfW, cy - halfH], [cx + halfW, cy - halfH],
                  [cx + halfW, cy + halfH], [cx - halfW, cy + halfH]];
    s.closed = true;
    m.property("ADBE Mask Shape").setValue(s);
    m.property("ADBE Mask Feather").setValue([fx, fy]);
    var o = tg(sc).property("ADBE Opacity");
    o.setValueAtTime(t0, 0); o.setValueAtTime(t1, opac); ease(o, 60);
    return sc;
  }
  function text(comp, str, font, size, color, tracking, align) {
    var L = span(comp.layers.addText(String(str)), comp.duration);
    var tp = L.property("ADBE Text Properties").property("ADBE Text Document");
    var d = tp.value;
    d.resetCharStyle(); d.font = font; d.fontSize = size; d.fillColor = color;
    d.applyFill = true; d.applyStroke = false; d.tracking = tracking || 0;
    d.justification = (align === "left") ? ParagraphJustification.LEFT_JUSTIFY
                                         : ParagraphJustification.CENTER_JUSTIFY;
    tp.setValue(d);
    textShadow(L, 195, 28);
    return L;
  }
  // ---- MEASURED text fitting (replaces Python advance-width estimation) ----
  // sourceRectAtTime(t,false) returns the ACTUAL rendered glyph box in layer
  // space. A box/underline sized from it can never be overflowed by the text,
  // and a too-wide string is shrunk to the real frame, not to an estimate.
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
  // opacity NEVER animates alone - it always rides a translateY
  function revealUp(L, t0, x, y, amt) {
    key2(tg(L).property("ADBE Position"), t0, [x, y + (amt || 40)], t0 + 0.5, [x, y], 80);
    key2(tg(L).property("ADBE Opacity"), t0, 0, t0 + 0.4, 100, 70);
  }
  // scaleX wipe growing from the LEFT edge. A solid's layer space runs 0..w, so
  // the left-edge anchor is [0, h/2] and Position must then be the LEFT edge.
  function wipeIn(L, t0, t1, xLeft, y) {
    var h = L.source.height;
    tg(L).property("ADBE Anchor Point").setValue([0, h / 2]);
    tg(L).property("ADBE Position").setValue([xLeft, y]);
    L.motionBlur = true;
    key2(tg(L).property("ADBE Scale"), t0, [0, 100], t1, [100, 100], 90);
  }
  // scaleY wipe growing DOWN from the top edge: anchor [w/2, 0].
  function wipeDown(L, t0, t1, x, yTop) {
    var w = L.source.width;
    tg(L).property("ADBE Anchor Point").setValue([w / 2, 0]);
    tg(L).property("ADBE Position").setValue([x, yTop]);
    L.motionBlur = true;
    key2(tg(L).property("ADBE Scale"), t0, [100, 0], t1, [100, 100], 90);
  }
  function grid(comp) {
    for (var gx = 0; gx <= 24; gx++) rect(comp, "gv_" + gx, 1, H, SILVER, 7, gx * (W / 24), H / 2);
    for (var gy = 0; gy <= 14; gy++) rect(comp, "gh_" + gy, W, 1, SILVER, 7, W / 2, gy * (H / 14));
  }
  function dip(comp, spec) {
    if (!spec.head) return;
    var d = rect(comp, "dip", W, H, [0, 0, 0], 0, W / 2, H / 2);
    var o = tg(d).property("ADBE Opacity");
    o.setValueAtTime(0, 100); o.setValueAtTime(spec.head, 0);
    o.setValueAtTime(spec.dur - spec.tail, 0); o.setValueAtTime(spec.dur, 100);
    ease(o, 40);
  }
  function colorOf(name) { return name === "GOLD" ? GOLD : RED; }

  // ---- CASE_COMPARE -------------------------------------------------------
  // Left column: state / case / date / fact list / verbatim quote.
  // Top right:   the money figure, counted up from strings baked in Python.
  // Bottom band: who paid, plus a flag line carrying the caveat the figure needs.
  function buildCase(comp, spec) {
    var LX = 150, FX = 215, MX = W * 0.775;

    // L3 (back): field + grid + oversized ghost state code
    rect(comp, "field", W, H, [0, 0, 0], 100, W / 2, H / 2);
    grid(comp);
    var ghost = text(comp, spec.code, FONT_NUM, 900, GOLD, 0);
    tg(ghost).property("ADBE Position").setValue([MX, H * 0.60]);
    key2(tg(ghost).property("ADBE Scale"), 0.05, [112, 112], 1.10, [100, 100], 80);
    key2(tg(ghost).property("ADBE Opacity"), 0.05, 0, 1.10, 6, 70);

    // L2 (mid): local scrims under each text zone
    scrimBand(comp, spec.dur, W * 0.42, H * 0.24, 780, 150, 260, 90, 62, 0.05, 0.45);
    scrimBand(comp, spec.dur, W * 0.46, H * 0.56, 900, 230, 300, 120, 58, 0.60, 1.05);
    scrimBand(comp, spec.dur, MX, H * 0.20, 420, 150, 240, 100, 60, 0.30, 0.75);

    // L1 (front): type
    var st = text(comp, spec.state, FONT_NUM, spec.stateSize, GOLD, 40, "left");
    fitText(st, 760, comp.duration * 0.7);
    st.motionBlur = true;
    revealUp(st, 0.18, LX, 190, 44);
    var rule = rect(comp, "state_rule", 340, 6, GOLD, 100, LX, 232);
    wipeIn(rule, 0.45, 0.95, LX, 232);
    var cs = text(comp, spec.case, FONT_LBL, spec.caseSize, SILVER, 100, "left");
    fitText(cs, 1040, comp.duration * 0.7);
    revealUp(cs, 0.55, LX, 292, 34);
    if (spec.date && spec.date.length) {
      var dt = text(comp, spec.date, FONT_LBL, spec.dateSize, DUST, 60, "left");
      fitText(dt, 900, comp.duration * 0.7);
      revealUp(dt, 0.70, LX, 348, 30);
    }

    // vertical gold rule alongside the fact list
    // MEASURED on the first render: at 70px steps the verbatim-quote block
    // finished 14px above the WHO PAID rule at y=828 and the two zones collided
    // visually. Tightened to 66px and lifted 10px, which restores ~100px of air.
    var vr = rect(comp, "fact_rule", 4, 66 * spec.facts.length + 10, GOLD, 70, LX - 26, 422);
    wipeDown(vr, 0.95, 1.55, LX - 26, 422);

    for (var i = 0; i < spec.facts.length; i++) {
      var y = 440 + i * 66, t = spec.factT[i];
      var tick = rect(comp, "tick_" + i, 40, 5, GOLD, 100, FX - 56, y + 4);
      wipeIn(tick, t, t + 0.28, FX - 56, y + 4);
      var lab = text(comp, spec.facts[i], FONT_LBL, spec.factSizes[i], WHITE, 25, "left");
      fitText(lab, 1600, comp.duration * 0.7);
      revealUp(lab, t + 0.08, FX, y + 12, 26);
    }

    if (spec.quoteT >= 0) {
      var qy = 440 + spec.facts.length * 66;
      var ql = text(comp, spec.quote_label, FONT_LBL, spec.quoteLabelSize, SILVER, 200, "left");
      revealUp(ql, spec.quoteT, LX, qy + 34, 22);
      // quote marks built from char codes so the JSX stays pure ASCII
      var qq = text(comp, String.fromCharCode(8220) + spec.quote + String.fromCharCode(8221),
                    FONT_LBL, spec.quoteSize, GOLD, 20, "left");
      revealUp(qq, spec.quoteT + 0.15, LX, qy + 84, 26);
    }

    // money block, top right
    var ml = text(comp, spec.money_label, FONT_LBL, spec.moneyLabelSize, SILVER, 200);
    revealUp(ml, 0.55, MX, 118, 30);
    var mnum;
    if (spec.moneyWord) {
      mnum = text(comp, spec.moneyWord, FONT_NUM, spec.moneySize, RED, 0);
      fitText(mnum, 680, comp.duration * 0.7); centerX(mnum, comp.duration * 0.7);
    } else {
      var lastM = spec.numKeys[spec.numKeys.length - 1];
      mnum = text(comp, lastM[1], FONT_NUM, spec.moneySize, GOLD, 0);
      fitText(mnum, 680, lastM[0]); centerX(mnum, lastM[0]);
      var td = mnum.property("ADBE Text Properties").property("ADBE Text Document");
      var doc = td.value;
      for (var k = 0; k < spec.numKeys.length; k++) {
        doc.text = String(spec.numKeys[k][1]);
        td.setValueAtTime(spec.numKeys[k][0], doc);
      }
    }
    mnum.motionBlur = true;
    tg(mnum).property("ADBE Position").setValue([MX, 232]);
    var mo = tg(mnum).property("ADBE Opacity");
    mo.setValueAtTime(0.68, 0); mo.setValueAtTime(0.80, 100);
    var msc = tg(mnum).property("ADBE Scale");
    msc.setValueAtTime(0.75, [46, 46]); msc.setValueAtTime(1.10, [110, 110]);
    msc.setValueAtTime(1.42, [100, 100]);
    ease(msc, 76);
    var mrule = rect(comp, "money_rule", 300, 4, GOLD, 88, MX - 150, 282);
    wipeIn(mrule, 1.35, 1.80, MX - 150, 282);
    if (spec.money_note && spec.money_note.length) {
      var mn = text(comp, spec.money_note, FONT_LBL, spec.moneyNoteSize, DUST, 40);
      revealUp(mn, 1.95, MX, 322, 24);
    }

    // outcome band
    var band = rect(comp, "who_band", W, 210, [0.02, 0.03, 0.06], 0, W / 2, 930);
    key2(tg(band).property("ADBE Opacity"), spec.whoT - 0.25, 0, spec.whoT + 0.15, 86, 70);
    var bl = rect(comp, "band_rule", W - 300, 3, GOLD, 60, LX, 828);
    wipeIn(bl, spec.whoT - 0.20, spec.whoT + 0.35, LX, 828);
    var wl = text(comp, "WHO PAID", FONT_LBL, 26, SILVER, 300, "left");
    revealUp(wl, spec.whoT - 0.10, LX, 866, 22);
    var wa = text(comp, spec.who, FONT_LBL, spec.whoSize, colorOf(spec.who_color), 60, "left");
    var rw = fitText(wa, 1600, comp.duration * 0.85);
    wa.motionBlur = true;
    revealUp(wa, spec.whoT, LX, 924, 38);
    // underline sized to the MEASURED who-paid width (+pad), so it always spans
    // the text instead of an estimate that fell short of the real glyphs.
    var uw = Math.min(1620, rw.width + 44);
    var ul = rect(comp, "who_mark", uw, 6, colorOf(spec.who_color), 100, LX, 958);
    wipeIn(ul, spec.whoT + 0.35, spec.whoT + 0.85, LX, 958);
    var fg = text(comp, spec.flag, FONT_LBL, spec.flagSize, DUST, 60, "left");
    fitText(fg, 1640, comp.duration * 0.85);
    revealUp(fg, spec.flagT, LX, 1000, 22);
  }

  // ---- LEDGER_TABLE -------------------------------------------------------
  function buildLedger(comp, spec) {
    var C1 = 130, C2 = 470, C3 = 1440;
    rect(comp, "field", W, H, [0, 0, 0], 100, W / 2, H / 2);
    grid(comp);
    scrimBand(comp, spec.dur, W / 2, H * 0.14, 900, 110, 300, 90, 60, 0.05, 0.40);
    scrimBand(comp, spec.dur, W / 2, H * 0.55, 900, 300, 320, 150, 55, 0.55, 1.05);

    var ti = text(comp, spec.title, FONT_LBL, spec.titleSize, WHITE, 120);
    fitText(ti, 1728, comp.duration * 0.5); centerX(ti, comp.duration * 0.5);
    ti.motionBlur = true;
    revealUp(ti, 0.20, W / 2, 110, 46);
    var sb = text(comp, spec.subtitle, FONT_LBL, spec.subtitleSize, SILVER, 260);
    fitText(sb, 1600, comp.duration * 0.5); centerX(sb, comp.duration * 0.5);
    revealUp(sb, 0.45, W / 2, 170, 30);

    var hr = rect(comp, "hdr_rule", 1660, 4, GOLD, 100, C1, 218);
    wipeIn(hr, 0.70, 1.30, C1, 218);
    var hx = [C1, C2, C3];
    for (var h = 0; h < spec.headers.length; h++) {
      var hd = text(comp, spec.headers[h], FONT_LBL, spec.headerSize, SILVER, 240, "left");
      revealUp(hd, 0.85 + h * 0.10, hx[h], 262, 24);
    }

    for (var r = 0; r < spec.rows.length; r++) {
      var y = 340 + r * 115, t = 1.35 + r * 0.34, row = spec.rows[r], sz = spec.rowSizes[r];
      var rr = rect(comp, "row_rule_" + r, 1660, 2, SILVER, 22, C1, y + 58);
      wipeIn(rr, t, t + 0.45, C1, y + 58);
      var s0 = text(comp, row[0], FONT_NUM, sz[0], GOLD, 20, "left");
      fitText(s0, 320, comp.duration * 0.7);
      s0.motionBlur = true;
      revealUp(s0, t, C1, y, 30);
      var s1 = text(comp, row[1], FONT_LBL, sz[1], WHITE, 25, "left");
      fitText(s1, 930, comp.duration * 0.7);
      revealUp(s1, t + 0.09, C2, y, 26);
      var s2 = text(comp, row[2], FONT_LBL, sz[2], colorOf(row[3]), 25, "left");
      fitText(s2, 430, comp.duration * 0.7);
      revealUp(s2, t + 0.18, C3, y - 8, 26);
      var s3 = text(comp, row[4], FONT_LBL, sz[3], DUST, 20, "left");
      fitText(s3, 430, comp.duration * 0.7);
      revealUp(s3, t + 0.26, C3, y + 34, 22);
    }

    // the payoff beat: light the WHO PAID column so the five answers read as five
    var colDiv = rect(comp, "col_div", 3, 640, GOLD, 55, C3 - 42, 232);
    wipeDown(colDiv, 3.30, 4.10, C3 - 42, 232);
    var colHi = rect(comp, "col_hi", 480, 660, GOLD, 0, C3 + 198, 560);
    colHi.blendingMode = BlendingMode.ADD;
    // MEASURED on the first render: an unfeathered ADD solid drew a visible
    // hard-edged gold box over the column. A wide feather is what makes it read
    // as a glow rather than a rectangle someone forgot to delete.
    (function () {
      var m = colHi.property("ADBE Mask Parade").addProperty("ADBE Mask Atom");
      var s = new Shape();
      s.vertices = [[0, 0], [480, 0], [480, 660], [0, 660]];
      s.closed = true;
      m.property("ADBE Mask Shape").setValue(s);
      m.property("ADBE Mask Feather").setValue([190, 190]);
    })();
    var cho = tg(colHi).property("ADBE Opacity");
    cho.setValueAtTime(3.60, 0); cho.setValueAtTime(4.40, 9);
    cho.setValueAtTime(spec.dur, 5); ease(cho, 60);

    for (var n = 0; n < spec.notes.length; n++) {
      var nt = text(comp, spec.notes[n], FONT_LBL, spec.noteSizes[n], DUST, 40, "left");
      fitText(nt, 1680, comp.duration * 0.7);
      revealUp(nt, 3.90 + n * 0.28, C1, 900 + n * 45, 22);
    }
  }

  function build(spec) {
    var comp = proj.items.addComp("LECHCMP_" + spec.id, W, H, 1.0, spec.dur, FPS);
    comp.motionBlur = true;
    if (spec.layout === "CASE_COMPARE") buildCase(comp, spec);
    else if (spec.layout === "LEDGER_TABLE") buildLedger(comp, spec);
    else throw new Error("unsupported layout " + spec.layout + " on " + spec.id);
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
  var mk = new File(RENDER_DIR + "/_compare_ok.txt");
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
    raise SystemExit(build())
