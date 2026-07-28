#!/usr/bin/env python
"""EP40 Lech - AE hero-card JSX generator (audited rebuild).

WHY THIS FILE EXISTS ALONGSIDE build_lech_hero_jsx.py
-----------------------------------------------------
`build_lech_hero_jsx.py` is the raw Codex-B output. An audit found three
disqualifying defects, so it is NOT used:
  1. It burns numbers that are not in the EP40 ledger ($580,000 "shoplifted
     goods", a computed compensation rate, CT_COUNTDOWN).
  2. It draws a FABRICATED floor plan (LIVING / KITCHEN / GARAGE / BEDROOM
     rectangles) for a house nobody has a layout for.
  3. Its psName() reads `app.fonts.allFonts[i].familyName`, which is undefined
     on AE 2026 (allFonts entries are array-LIKE wrappers, not FontObjects).
     That is the exact EP38 bug that shipped a silent substitute font.

This builder emits ONLY ledger-backed screen text:
  * the five  CARD:  strings from EP40_lech_script.en.v001.md, verbatim
  * the two CLAUSE_STRIKE cards approved in DESIGN v002 section 9
  * non-numeric furniture: 4 act titles, 1 schematic, 2 seam transitions

Accuracy lock: Lech v. Jackson was decided by the Tenth Circuit (2019); the
Supreme Court denied review (2020) and never reached the merits. No card in
this file contains the string "Supreme Court" in any form.

Machine traps honoured (DESIGN v002 section 9 / EP39 5.8):
  runtime font resolve with unwrap() + HARD FAIL, spatial-aware
  setTemporalEaseAtKey dim, no app.newProject(), per-layer motionBlur,
  "ADBE Rotate Z", explicit inPoint AND outPoint, conformFrameRate,
  single-line TextDocument only (multi-line = separate layers),
  all display strings precomputed in Python, completion marker file.
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
WORK = Path("H:/pd-media/episodes/PD-2026-040-lech/08_edit/ae_hero")
# Fixed (measurement-based) renders go to a NEW dir so the existing composited
# renders are never clobbered; re-compositing consumes ae_hero/fixed/.
OUT = WORK / "fixed"

FPS = 30
W, H = 1920, 1080
STILLS = Path("H:/pd-media/assets/ai/lech")

# DESIGN v002 section 9.4 colour constants (0..1 float)
GOLD = [0.898, 0.710, 0.227]
WHITE = [0.961, 0.969, 0.980]
SILVER = [0.588, 0.627, 0.682]
DUST = [0.827, 0.769, 0.667]
RED = [0.780, 0.290, 0.250]

# ---------------------------------------------------------------- text fitting
# Advance-width factors measured off Anton / Oswald cap-height specimens. Used
# so a long string shrinks in Python instead of overflowing the 1920 frame.
ANTON_ADV = 0.470
OSWALD_ADV = 0.505


def fit_size(text: str, base: int, max_w: int, adv: float, tracking: int = 0) -> int:
    n = max(1, len(text))
    per = adv + (tracking / 1000.0)
    size = min(base, int(max_w / (per * n)))
    return max(18, size)


def money_keys(target: int, t0: float, t1: float, n: int = 18):
    """(time, display-string) hold keys. Python formats EVERY string; the JSX
    never does arithmetic on a number (EP38 rule)."""
    keys = [(t0, "$0")]
    for i in range(1, n):
        p = i / (n - 1)
        v = target * (1.0 - (1.0 - p) ** 3)          # ease-out cubic
        keys.append((t0 + (t1 - t0) * p, f"${int(round(v)):,}"))
    keys.append((t1 + 0.02, f"${target:,}"))
    return [[round(t, 4), s] for t, s in keys]


# --------------------------------------------------------------- the card deck
# still_content_verified: written after EYEBALLING a labelled contact sheet of
# all 41 renders. Never inferred from the S## number (the EP39 S44 mistake).
CARDS = [
    dict(
        id="c01", layout="DATE_STAMP", dur=4.0,
        source="script CARD: JUNE 3, 2015",
        hero="JUNE 3, 2015",
        top="GREENWOOD VILLAGE", bottom="",
        caption="The nine-year-old walked out of the house first.",
        still="S01_01.png",
        still_content_verified="Intact cream two-story suburban house in morning sun, "
                               "a child's bicycle lying on the front lawn. Verified on "
                               "contact sheet 1. Chosen for the day BEFORE the siege.",
    ),
    dict(
        id="c02", layout="DATE_STAMP", dur=3.5,
        source="script CARD: MAY 2026",
        hero="MAY 2026",
        top="ELEVEN YEARS LATER", bottom="",
        caption="He signs his name to a case belonging to strangers.",
        still="S64_02.png",
        still_content_verified="Rebuilt house at stud-frame stage, dusk, quiet street. "
                               "Verified on contact sheet 4. Chosen for elapsed time, "
                               "not for the 2026 filing itself.",
    ),
    dict(
        id="c03", layout="MONEY_STACK", dur=6.5,
        source="script CARD: $5,000",
        hero="$5,000", money=5000,
        top="TEMPORARY LIVING EXPENSES", bottom="WHAT THE CITY OFFERED",
        caption="Help with temporary living expenses.",
        still="S45_01.png",
        still_content_verified="Dust-covered shoe, a fallen picture frame and a mug "
                               "lying in white rubble. Verified on contact sheet 3. "
                               "Chosen as the human scale the offer was measured against.",
    ),
    dict(
        id="c04", layout="MONEY_STACK", dur=7.0,
        source="script CARD: $250,000",
        hero="$250,000", money=250000,
        top="TO REBUILD, HE BORROWED", bottom="",
        caption="He had been planning to retire.",
        still="S64_03.png",
        still_content_verified="Full two-story stud framing of a new house at dusk. "
                               "Verified on contact sheet 4. Chosen because the figure "
                               "is the rebuilding loan.",
    ),
    dict(
        id="c05", layout="QUOTE_STAMP", dur=5.0,
        source="script CARD: FURTHER PERCOLATION",
        hero="FURTHER PERCOLATION",
        top="STATEMENT RESPECTING DENIAL", bottom="JUSTICE SOTOMAYOR",
        caption="A question that divides the courts of appeals.",
        still="S63_03.png",
        still_content_verified="Empty lot with a bare concrete foundation at dusk, "
                               "flanked by two intact lit houses. Verified on contact "
                               "sheet 4. Chosen for the unresolved gap.",
    ),
    dict(
        id="b04", layout="CLAUSE_STRIKE", dur=7.0,
        source="script CARD + DESIGN v002 section 9.2 b04",
        line1="INTENTIONAL ACTS BY GOVERNMENT OFFICIALS", line2="EXCLUDED",
        top="THE HOMEOWNER'S POLICY", bottom="",
        caption="No policy covers the state coming through a wall.",
        still="S38_01.png",
        still_content_verified="Dark blown-open interior, a single dusty shaft of "
                               "daylight across rubble. Verified on contact sheet 2. "
                               "Held at low opacity so the clause stays legible.",
    ),
    dict(
        id="b07", layout="CLAUSE_STRIKE", dur=7.0,
        source="script CARD + DESIGN v002 section 9.2 b07",
        line1="NOT BINDING PRECEDENT", line2="MAY BE CITED FOR ITS PERSUASIVE VALUE",
        top="TENTH CIRCUIT, 2019", bottom="",
        caption="The document is not an opinion.",
        still="S38_03.png",
        still_content_verified="Interior wall torn open to daylight, rubble across the "
                               "floor. Verified on contact sheet 2. Held at low opacity "
                               "so the footnote stays legible.",
    ),
    dict(
        id="t1", layout="ACT_TITLE", dur=2.0, act="1",
        source="script heading ACT 1",
        line1="4219 SOUTH ALTON STREET", line2="",
        still="S01_02.png",
        still_content_verified="Whole intact two-story house seen from the street, "
                               "garage and driveway, bright day. Verified on contact "
                               "sheet 1.",
    ),
    dict(
        id="t2", layout="ACT_TITLE", dur=2.0, act="2",
        source="script heading ACT 2",
        line1="WHAT IT COSTS", line2="TO BE THE ADDRESS",
        still="S36_02.png",
        still_content_verified="Destroyed two-story facade, every window blown out, "
                               "debris across the lawn. Verified on contact sheet 2.",
    ),
    dict(
        id="t3", layout="ACT_TITLE", dur=2.0, act="3",
        source="script heading ACT 3",
        line1="POLICE POWER", line2="",
        still="S23_01.png",
        still_content_verified="Armored police vehicle parked on the lawn beside the "
                               "intact house, dust rising. Verified on contact sheet 1.",
    ),
    dict(
        id="t4", layout="ACT_TITLE", dur=2.0, act="4",
        source="script heading ACT 4",
        line1="THE ADDRESS IS", line2="THE ONLY QUALIFICATION",
        still="S44_01.png",
        still_content_verified="Single collapsed house reduced to a rubble mound, "
                               "standing between two untouched suburban homes. "
                               "Verified on contact sheet 3. Exactly the address motif.",
    ),
    dict(
        id="hp01", layout="HOUSE_SCHEMATIC", dur=7.0,
        source="ACT 1 court-record narration (no layout is claimed)",
        top="SCHEMATIC: NOT A FLOOR PLAN",
        caption="DIAGRAM. NOT TO SCALE. LAYOUT NOT DEPICTED.",
        still=None,
        # Category labels only. No room names, no positions, no counts. Every
        # line below is a paraphrase of the court's own account in the script.
        items=["GAS MUNITIONS FIRED IN",
               "DOORS BREACHED BY VEHICLE",
               "EXPLOSIVES FOR SIGHT LINES",
               "MULTIPLE HOLES PUNCHED"],
        roof_label="THE ROOF DID NOT FALL IN",
        still_content_verified="No photograph used. Pure vector on black so the card "
                               "cannot be mistaken for a survey of the real house.",
    ),
    dict(id="x01", layout="SEAM", dur=0.6, seam="dust", source="act seam A",
         still=None, still_content_verified="No photograph used."),
    dict(id="x02", layout="SEAM", dur=0.8, seam="strike", source="act seam B",
         still=None, still_content_verified="No photograph used."),
]


def build():
    WORK.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    REPO_BEATS.parent.mkdir(parents=True, exist_ok=True)
    for m in ("_build_ok.txt", "_error.txt"):
        (WORK / m).unlink(missing_ok=True)

    beats = []
    for c in CARDS:
        still_path = None
        if c.get("still"):
            p = STILLS / c["still"]
            if not p.exists():
                print(f"FAIL missing still {p}", file=sys.stderr)
                return 2
            still_path = str(p).replace("\\", "/")

        b = dict(
            id=c["id"], layout=c["layout"], dur=float(c["dur"]),
            source=c["source"],
            still=still_path,
            still_content_verified=c["still_content_verified"],
            top=c.get("top", ""), bottom=c.get("bottom", ""),
            caption=c.get("caption", ""),
            head=round(4 / FPS, 4), tail=round(4 / FPS, 4),
            out=str(OUT / f"{c['id']}.mp4").replace("\\", "/"),
        )

        if c["layout"] in ("DATE_STAMP", "QUOTE_STAMP"):
            b["hero"] = c["hero"]
            b["heroSize"] = fit_size(c["hero"], 190 if c["layout"] == "DATE_STAMP" else 150,
                                     1560, ANTON_ADV)
        elif c["layout"] == "MONEY_STACK":
            b["hero"] = c["hero"]
            b["heroSize"] = fit_size(c["hero"], 250, 1560, ANTON_ADV)
            b["numKeys"] = money_keys(c["money"], 0.55, 1.55)
        elif c["layout"] == "CLAUSE_STRIKE":
            b["line1"], b["line2"] = c["line1"], c["line2"]
            b["size1"] = fit_size(c["line1"], 86, 1660, OSWALD_ADV, 40)
            b["size2"] = fit_size(c["line2"], 92, 1660, OSWALD_ADV, 60)
        elif c["layout"] == "ACT_TITLE":
            b["act"] = c["act"]
            b["line1"], b["line2"] = c["line1"], c.get("line2", "")
            b["size1"] = fit_size(c["line1"], 86, 1520, OSWALD_ADV, 180)
            b["size2"] = fit_size(c.get("line2") or "X", 86, 1520, OSWALD_ADV, 180)
        elif c["layout"] == "HOUSE_SCHEMATIC":
            b["items"] = c["items"]
            b["roof_label"] = c["roof_label"]
        elif c["layout"] == "SEAM":
            b["seam"] = c["seam"]
            b["head"] = b["tail"] = 0.0

        beats.append(b)

    doc = {
        "schema_version": "lech_hero_cards.v1",
        "episode_id": EP,
        "fps": FPS, "width": W, "height": H,
        "render_dir": str(WORK).replace("\\", "/"),
        "accuracy_note": (
            "Lech v. Jackson was decided by the Tenth Circuit in 2019; review was "
            "declined in 2020 and the merits were never reached. No card contains "
            "the string 'Supreme Court'."
        ),
        "ledger_note": (
            "Only the five script CARD strings and the two DESIGN v002 section 9 "
            "CLAUSE_STRIKE cards carry figures or quoted text. The shoplifting "
            "loss, the compensation rate and CT_COUNTDOWN from "
            "EP40_lech_CODEX_B_BUILD.v001.md are NOT in the ledger and are not built."
        ),
        "beats": beats,
    }
    payload = json.dumps(doc, ensure_ascii=False, indent=2)
    SPEC_OUT.write_text(payload, encoding="utf-8")
    (WORK / "beats.json").write_text(payload, encoding="utf-8")
    REPO_BEATS.write_text(payload, encoding="utf-8")

    jsx = JSX
    jsx = jsx.replace("__W__", str(W)).replace("__H__", str(H)).replace("__FPS__", str(FPS))
    jsx = jsx.replace("__GOLD__", ",".join(str(v) for v in GOLD))
    jsx = jsx.replace("__WHITE__", ",".join(str(v) for v in WHITE))
    jsx = jsx.replace("__SILVER__", ",".join(str(v) for v in SILVER))
    jsx = jsx.replace("__DUST__", ",".join(str(v) for v in DUST))
    jsx = jsx.replace("__RED__", ",".join(str(v) for v in RED))
    jsx = jsx.replace("__BEATS__", json.dumps(beats, ensure_ascii=False))
    jsx = jsx.replace("__RENDER__", str(WORK).replace("\\", "/"))
    jsx = jsx.replace("__AEP__", str(WORK / "lech_hero_fixed.aep").replace("\\", "/"))
    # BOM so ExtendScript reads the localized template names correctly.
    (WORK / "lech_hero_fixed.jsx").write_text(jsx, encoding="utf-8-sig")

    print(f"[gen] {len(beats)} cards, total {sum(b['dur'] for b in beats):.1f}s")
    for b in beats:
        s = b.get("hero") or " / ".join(x for x in (b.get("line1"), b.get("line2")) if x) or b["layout"]
        print(f"  {b['id']:<5} {b['layout']:<16} {b['dur']:>4.1f}s  {s[:58]}")
    print("[gen] jsx  ->", WORK / "lech_hero_fixed.jsx")
    print("[gen] spec ->", SPEC_OUT)
    return 0


JSX = r"""// AUTO-GENERATED - EP40 Lech AE hero cards. Do not hand-edit.
(function () {
  var W = __W__, H = __H__, FPS = __FPS__;
  var GOLD = [__GOLD__], WHITE = [__WHITE__], SILVER = [__SILVER__],
      DUST = [__DUST__], RED = [__RED__];
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
    if (itx instanceof CompItem && String(itx.name).indexOf("LECH_") === 0) itx.remove();
  } } catch (e) {}
  try { proj.gpuAccelType = GpuAccelType.SOFTWARE; } catch (e) {}
  try { proj.bitsPerChannel = 8; } catch (e) {}
  app.beginUndoGroup("lech_hero");

  // ---- runtime font resolver -------------------------------------------
  // MEASURED on AE 2026: app.fonts.allFonts[i] is NOT a FontObject, it is an
  // array-LIKE wrapper whose [0] is the FontObject. Reading .familyName off
  // the wrapper yields undefined, so a naive resolver falls through to the
  // family name -- and TextDocument.font wants the PostScript name. That is
  // how EP38 shipped a silent substitute. Missing font = HARD FAIL, never a
  // fallback.
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
  function text(comp, str, font, size, color, tracking, align) {
    var L = span(comp.layers.addText(String(str)), comp.duration);
    var tp = L.property("ADBE Text Properties").property("ADBE Text Document");
    var d = tp.value;
    d.resetCharStyle(); d.font = font; d.fontSize = size; d.fillColor = color;
    d.applyFill = true; d.applyStroke = false; d.tracking = tracking || 0;
    d.justification = (align === "left") ? ParagraphJustification.LEFT_JUSTIFY
                                         : ParagraphJustification.CENTER_JUSTIFY;
    tp.setValue(d);
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
  // Exact horizontal centering: anchor X = measured glyph centre; Y anchor is
  // left at its current value so the baseline / tuned y positions do not move.
  function centerX(L, t) {
    var r = srect(L, t);
    var ap = tg(L).property("ADBE Anchor Point").value;
    tg(L).property("ADBE Anchor Point").setValue([r.left + r.width / 2, ap[1]]);
    return r;
  }
  function revealUp(L, t0, x, y, amt) {
    key2(tg(L).property("ADBE Position"), t0, [x, y + (amt || 46)], t0 + 0.5, [x, y], 80);
    key2(tg(L).property("ADBE Opacity"), t0, 0, t0 + 0.4, 100, 70);
  }
  // scaleX wipe growing from the LEFT edge. A solid's layer space runs 0..w,
  // so the left-edge anchor is [0, h/2] and Position must then be the left
  // edge, not the centre. Getting this wrong slides the bar instead of wiping.
  function wipeIn(L, t0, t1, xc, y) {
    var w = L.source.width, h = L.source.height;
    tg(L).property("ADBE Anchor Point").setValue([0, h / 2]);
    tg(L).property("ADBE Position").setValue([xc - w / 2, y]);
    L.motionBlur = true;
    key2(tg(L).property("ADBE Scale"), t0, [0, 100], t1, [100, 100], 90);
  }
  // TRAP: a solid's layer space runs 0..w / 0..h, so an ellipse mask must be
  // centred on [cx, cy] -- building it around the ORIGIN puts three quarters of
  // the circle off the layer and leaves a crescent sliver on screen.
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
  function outline(comp, name, x, y, w, h, color, op, t) {
    t = t || 4;
    return [rect(comp, name + "_t", w, t, color, op, x, y - h / 2),
            rect(comp, name + "_b", w, t, color, op, x, y + h / 2),
            rect(comp, name + "_l", t, h, color, op, x - w / 2, y),
            rect(comp, name + "_r", t, h, color, op, x + w / 2, y)];
  }

  // ---- background stack (L9..L4) ----------------------------------------
  function addStill(comp, spec, baseOpacity) {
    if (!spec.still) return null;
    var item = proj.importFile(new ImportOptions(new File(spec.still)));
    try { item.mainSource.conformFrameRate = FPS; } catch (e) {}
    var S = span(comp.layers.add(item), spec.dur);
    var fill = Math.max(W / item.width, H / item.height) * 100;
    var st = tg(S);
    st.property("ADBE Anchor Point").setValue([item.width / 2, item.height / 2]);
    key2(st.property("ADBE Position"), 0, [W / 2 - 18, H / 2 + 10], spec.dur, [W / 2 + 18, H / 2 - 10], 20);
    key2(st.property("ADBE Scale"), 0, [fill, fill], spec.dur, [fill * 1.08, fill * 1.08], 25);
    if (baseOpacity !== undefined) st.property("ADBE Opacity").setValue(baseOpacity);
    return S;
  }
  function vignette(comp) {
    var v = rect(comp, "vignette", W, H, [0, 0, 0], 62, W / 2, H / 2);
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
  // EP38 failed because a silver top label sat on a bright background. These
  // stills are sunlit cream siding, so a plain vignette is not enough: lay a
  // dark scrim across the whole frame plus a heavier band behind the text.
  function scrim(comp, strength) {
    rect(comp, "scrim_full", W, H, [0.01, 0.02, 0.04], strength, W / 2, H / 2);
    // Soft-bottomed black band behind the text zone. NOTE: a Ramp effect
    // paints COLOUR, not alpha -- ramping black to white here would render a
    // white smear over the lower frame. Feathered mask is the correct tool.
    // The falloff must be wider than the eye can localise. A 300px feather on a
    // band ending mid-frame read as a hard horizontal seam across the photo, so
    // the band is taller than the frame and the feather is very wide.
    var bh = Math.round(H * 1.30);
    var band = rect(comp, "scrim_band", W, bh, [0, 0, 0], 66, W / 2, H * 0.02);
    var m = band.property("ADBE Mask Parade").addProperty("ADBE Mask Atom");
    var s = new Shape();
    s.vertices = [[0, 0], [W, 0], [W, bh], [0, bh]];
    s.closed = true;
    m.property("ADBE Mask Shape").setValue(s);
    m.property("ADBE Mask Feather").setValue([0, 700]);
  }
  function polish(comp, spec) {
    var grade = rect(comp, "warm_grade", W, H, [0.14, 0.11, 0.06], 30, W / 2, H / 2);
    grade.blendingMode = BlendingMode.MULTIPLY;
    vignette(comp);
    var glow = rect(comp, "glow", W, H, [0, 0, 0], 0, W / 2, H / 2);
    var gr = glow.property("ADBE Effect Parade").addProperty("ADBE Ramp");
    gr.property("ADBE Ramp-0001").setValue([W / 2, H * 0.42]);
    gr.property("ADBE Ramp-0002").setValue(GOLD);
    gr.property("ADBE Ramp-0003").setValue([W / 2, H * 0.95]);
    gr.property("ADBE Ramp-0004").setValue([0, 0, 0]);
    gr.property("ADBE Ramp-0005").setValue(2);
    glow.blendingMode = BlendingMode.ADD;
    var go = tg(glow).property("ADBE Opacity");
    go.setValueAtTime(0, 0); go.setValueAtTime(0.7, 22); go.setValueAtTime(spec.dur, 14); ease(go, 60);
    var sweep = rect(comp, "sweep", 360, H * 1.6, [1, 1, 1], 0, -300, H / 2);
    sweep.blendingMode = BlendingMode.ADD;
    sweep.motionBlur = true;
    tg(sweep).property("ADBE Rotate Z").setValue(18);          // 2D rotation
    key2(tg(sweep).property("ADBE Position"), 0.5, [-300, H / 2], 1.25, [W + 300, H / 2], 45);
    var so = tg(sweep).property("ADBE Opacity");
    so.setValueAtTime(0.5, 0); so.setValueAtTime(0.7, 18); so.setValueAtTime(1.25, 0);
  }
  function caption(comp, spec) {
    if (!spec.caption || !spec.caption.length) return;
    var y = H * 0.90;
    var bar = rect(comp, "capbar", W, 130, [0.02, 0.04, 0.08], 0, W / 2, y);
    var bo = tg(bar).property("ADBE Opacity");
    bo.setValueAtTime(0.2, 0); bo.setValueAtTime(0.5, 72);
    bo.setValueAtTime(spec.dur - 0.4, 72); bo.setValueAtTime(spec.dur - 0.1, 0);
    var cap = text(comp, spec.caption, FONT_LBL, 42, WHITE, 20);
    fitText(cap, 1728, spec.dur * 0.6); centerX(cap, spec.dur * 0.6);
    tg(cap).property("ADBE Position").setValue([W / 2, y - 6]);
    var co = tg(cap).property("ADBE Opacity");
    co.setValueAtTime(0.3, 0); co.setValueAtTime(0.6, 100);
    co.setValueAtTime(spec.dur - 0.4, 100); co.setValueAtTime(spec.dur - 0.12, 0);
  }
  function dip(comp, spec) {
    if (!spec.head) return;
    var d = rect(comp, "dip", W, H, [0, 0, 0], 0, W / 2, H / 2);
    var o = tg(d).property("ADBE Opacity");
    o.setValueAtTime(0, 100); o.setValueAtTime(spec.head, 0);
    o.setValueAtTime(spec.dur - spec.tail, 0); o.setValueAtTime(spec.dur, 100);
    ease(o, 40);
  }
  function topLabel(comp, spec, y, size) {
    if (!spec.top || !spec.top.length) return null;
    var L = text(comp, spec.top, FONT_LBL, size || 44, SILVER, 340);
    fitText(L, 1728, comp.duration * 0.5);   // measured fit to 90% of frame
    centerX(L, comp.duration * 0.5);
    revealUp(L, 0.2, W / 2, y, 46);
    return L;
  }
  function accent(comp, y, w) {
    var L = rect(comp, "accent", w || 460, 6, GOLD, 92, W / 2, y);
    wipeIn(L, 0.55, 1.05, W / 2, y);
    tg(L).property("ADBE Opacity").setValue(92);
    return L;
  }

  // ---- layouts -----------------------------------------------------------
  function heroText(comp, spec, y, reveal) {
    var L = text(comp, spec.hero, FONT_NUM, spec.heroSize, GOLD, 0);
    fitText(L, 1728, spec.dur * 0.85);
    centerX(L, spec.dur * 0.85);
    L.motionBlur = true;
    tg(L).property("ADBE Position").setValue([W / 2, y]);
    var o = tg(L).property("ADBE Opacity");
    o.setValueAtTime(reveal, 0); o.setValueAtTime(reveal + 0.14, 100);
    var sc = tg(L).property("ADBE Scale");
    sc.setValueAtTime(reveal, [58, 58]);
    sc.setValueAtTime(reveal + 0.35, [110, 110]);
    sc.setValueAtTime(reveal + 0.65, [100, 100]);
    ease(sc, 78);
    return L;
  }
  function buildDate(comp, spec) {
    topLabel(comp, spec, H * 0.215, 44);
    heroText(comp, spec, H * 0.44, 0.45);
    accent(comp, H * 0.545, 620);
    if (spec.bottom && spec.bottom.length) {
      var b = text(comp, spec.bottom, FONT_LBL, 58, WHITE, 120);
      revealUp(b, 1.15, W / 2, H * 0.64, 46);
    }
  }
  function buildQuote(comp, spec) {
    topLabel(comp, spec, H * 0.215, 40);
    var L = heroText(comp, spec, H * 0.44, 0.45);
    // Quote marks framing the phrase. Built from char codes so the JSX file
    // stays pure ASCII and cannot be corrupted by an encoding mismatch.
    var q1 = text(comp, String.fromCharCode(8220), FONT_NUM, 150, GOLD, 0);
    tg(q1).property("ADBE Position").setValue([W * 0.085, H * 0.42]);
    key2(tg(q1).property("ADBE Opacity"), 0.35, 0, 0.85, 45, 70);
    var q2 = text(comp, String.fromCharCode(8221), FONT_NUM, 150, GOLD, 0);
    tg(q2).property("ADBE Position").setValue([W * 0.915, H * 0.42]);
    key2(tg(q2).property("ADBE Opacity"), 0.45, 0, 0.95, 45, 70);
    accent(comp, H * 0.545, 620);
    if (spec.bottom && spec.bottom.length) {
      var b = text(comp, spec.bottom, FONT_LBL, 52, WHITE, 160);
      revealUp(b, 1.15, W / 2, H * 0.645, 46);
    }
  }
  function buildMoney(comp, spec) {
    topLabel(comp, spec, H * 0.205, 44);
    // Build on the FINAL (widest) value so the measured fit covers every frame.
    var last = spec.numKeys[spec.numKeys.length - 1];
    var L = text(comp, last[1], FONT_NUM, spec.heroSize, GOLD, 0);
    fitText(L, 1728, last[0]);
    centerX(L, last[0]);
    L.motionBlur = true;
    tg(L).property("ADBE Position").setValue([W / 2, H * 0.42]);
    var td = L.property("ADBE Text Properties").property("ADBE Text Document");
    var doc = td.value;
    for (var i = 0; i < spec.numKeys.length; i++) {
      doc.text = String(spec.numKeys[i][1]);
      td.setValueAtTime(spec.numKeys[i][0], doc);
    }
    var o = tg(L).property("ADBE Opacity");
    o.setValueAtTime(0.45, 0); o.setValueAtTime(0.57, 100);
    var sc = tg(L).property("ADBE Scale");
    sc.setValueAtTime(0.55, [42, 42]); sc.setValueAtTime(0.90, [112, 112]); sc.setValueAtTime(1.20, [100, 100]);
    ease(sc, 75);
    accent(comp, H * 0.485, 460);
    if (spec.bottom && spec.bottom.length) {
      var b = text(comp, spec.bottom, FONT_LBL, 60, WHITE, 120);
      revealUp(b, 1.35, W / 2, H * 0.60, 46);
    }
  }
  function buildClause(comp, spec) {
    topLabel(comp, spec, H * 0.185, 40);
    // paper plate: texture and a highlighted band only. Deliberately NOT a
    // legible fake document -- no body copy, no letterhead, no case caption.
    var plate = rect(comp, "plate", W * 0.80, H * 0.44, [0.88, 0.86, 0.81], 0, W / 2, H * 0.455);
    plate.blendingMode = BlendingMode.ADD;
    key2(tg(plate).property("ADBE Opacity"), 0.35, 0, 0.95, 9, 70);
    key2(tg(plate).property("ADBE Scale"), 0.35, [104, 104], 0.95, [100, 100], 70);
    // illegible ruled lines standing in for body copy
    for (var i = 0; i < 7; i++) {
      var lw = 620 + ((i * 137) - Math.floor((i * 137) / 260) * 260);
      var ry = H * 0.30 + i * 26;
      if (i === 3 || i === 4) continue;              // gap where the clause sits
      var rl = rect(comp, "rule_" + i, lw, 5, SILVER, 0, W / 2, ry);
      key2(tg(rl).property("ADBE Opacity"), 0.5 + i * 0.05, 0, 0.9 + i * 0.05, 16, 70);
    }
    var l1 = text(comp, spec.line1, FONT_LBL, spec.size1, WHITE, 40);
    fitText(l1, 1660, comp.duration * 0.7);   // fit line1 to the plate width
    centerX(l1, comp.duration * 0.7);
    revealUp(l1, 0.85, W / 2, H * 0.435, 34);
    var l2 = text(comp, spec.line2, FONT_LBL, spec.size2, RED, 60);
    var r2 = fitText(l2, 1620, comp.duration * 0.7);   // MEASURED width of line2
    centerX(l2, comp.duration * 0.7);
    revealUp(l2, 1.35, W / 2, H * 0.565, 34);
    // RED underline + highlight glow are sized from the MEASURED line2 width so
    // the operative words can never overflow the box (the old length*size
    // estimate under-counted and let the edge letters spill out). NOT a strike-
    // through: the clause was not struck, it is the clause that decided the claim.
    var ulW = Math.min(1720, r2.width + 70);
    var ul = rect(comp, "clause_mark", ulW, 8, RED, 100, W / 2, H * 0.625);
    wipeIn(ul, 1.75, 2.35, W / 2, H * 0.625);
    var hlW = Math.min(1760, r2.width + 140);
    var hl = rect(comp, "clause_glow", hlW, 118, RED, 0, W / 2, H * 0.565);
    hl.blendingMode = BlendingMode.ADD;
    key2(tg(hl).property("ADBE Opacity"), 1.55, 0, 2.05, 13, 70);
  }
  function buildAct(comp, spec) {
    var n = text(comp, "ACT " + spec.act, FONT_NUM, 96, GOLD, 40);
    tg(n).property("ADBE Position").setValue([W / 2, H * 0.335]);
    var no = tg(n).property("ADBE Opacity");
    no.setValueAtTime(0.05, 0); no.setValueAtTime(0.45, 78);
    key2(tg(n).property("ADBE Scale"), 0.05, [136, 136], 0.45, [100, 100], 80);
    n.motionBlur = true;
    var two = spec.line2 && spec.line2.length;
    var y1 = two ? H * 0.485 : H * 0.525;
    var t1 = text(comp, spec.line1, FONT_LBL, spec.size1, WHITE, 180);
    fitText(t1, 1728, comp.duration * 0.7); centerX(t1, comp.duration * 0.7);
    revealUp(t1, 0.28, W / 2, y1, 58);
    if (two) {
      var t2 = text(comp, spec.line2, FONT_LBL, spec.size2, WHITE, 180);
      fitText(t2, 1728, comp.duration * 0.7); centerX(t2, comp.duration * 0.7);
      revealUp(t2, 0.40, W / 2, H * 0.605, 58);
    }
    var rule = rect(comp, "act_rule", 520, 5, GOLD, 100, W / 2, two ? H * 0.705 : H * 0.635);
    wipeIn(rule, 0.62, 1.20, W / 2, two ? H * 0.705 : H * 0.635);
  }
  function buildHouse(comp, spec) {
    // Pure vector on black. No photograph, no room names, no measured layout.
    for (var gx = 0; gx <= 24; gx++) rect(comp, "gv_" + gx, 1, H, SILVER, 7, gx * (W / 24), H / 2);
    for (var gy = 0; gy <= 14; gy++) rect(comp, "gh_" + gy, W, 1, SILVER, 7, W / 2, gy * (H / 14));
    var tl = text(comp, spec.top, FONT_LBL, 40, SILVER, 300);
    revealUp(tl, 0.15, W / 2, H * 0.135, 40);

    var cx = W * 0.685, cy = H * 0.545, bw = 620, bh = 360;
    // the mass: one abstract block, split once because the record says the
    // house was two-story. Nothing else about the interior is asserted.
    var edges = outline(comp, "mass", cx, cy, bw, bh, SILVER, 82, 5);
    for (var e = 0; e < edges.length; e++) {
      edges[e].motionBlur = true;
      var t = 0.55 + e * 0.09;
      key2(tg(edges[e]).property("ADBE Scale"), t, (e < 2 ? [0, 100] : [100, 0]), t + 0.34,
           [100, 100], 86);
    }
    var mid = rect(comp, "storey_split", bw, 3, SILVER, 55, cx, cy);
    wipeIn(mid, 1.05, 1.55, cx, cy);
    // Storey labels hug the left inside edge: the centre of the mass is where
    // the breach markers land, and a marker sat on top of "UPPER STOREY".
    var slx = cx - bw * 0.44;
    var st1 = text(comp, "UPPER STOREY", FONT_LBL, 24, SILVER, 120, "left");
    tg(st1).property("ADBE Position").setValue([slx, cy - bh * 0.36]);
    key2(tg(st1).property("ADBE Opacity"), 1.6, 0, 1.9, 60, 70);
    var st2 = text(comp, "LOWER STOREY", FONT_LBL, 24, SILVER, 120, "left");
    tg(st2).property("ADBE Position").setValue([slx, cy + bh * 0.14]);
    key2(tg(st2).property("ADBE Opacity"), 1.7, 0, 2.0, 60, 70);

    // roof: the one structural fact the record states plainly
    var roof = rect(comp, "roof", bw + 70, 7, GOLD, 100, cx, cy - bh / 2 - 34);
    wipeIn(roof, 1.30, 1.85, cx, cy - bh / 2 - 34);
    var rlab = text(comp, spec.roof_label, FONT_LBL, 26, GOLD, 120);
    revealUp(rlab, 1.95, cx, cy - bh / 2 - 62, 22);

    // breach markers: abstract, unlabelled, position asserts nothing
    var pts = [[-0.10, -0.30], [0.24, -0.16], [0.34, 0.14], [0.06, 0.30], [-0.26, 0.10]];
    for (var b = 0; b < pts.length; b++) {
      var bx = cx + pts[b][0] * bw, by = cy + pts[b][1] * bh, tt = 2.5 + b * 0.30;
      var ring = circle(comp, "ring_" + b, bx, by, 96, GOLD, 55, true);
      key2(tg(ring).property("ADBE Scale"), tt, [0, 0], tt + 0.60, [190, 190], 40);
      key2(tg(ring).property("ADBE Opacity"), tt, 55, tt + 0.60, 0, 40);
      var dot = circle(comp, "dot_" + b, bx, by, 30, GOLD, 0, false);
      dot.motionBlur = true;
      key2(tg(dot).property("ADBE Scale"), tt, [0, 0], tt + 0.28, [100, 100], 75);
      key2(tg(dot).property("ADBE Opacity"), tt, 0, tt + 0.28, 100, 75);
    }

    // category list, left column, left justified
    var lx = W * 0.055;
    for (var i = 0; i < spec.items.length; i++) {
      var y = H * 0.36 + i * 78, ti = 1.5 + i * 0.42;
      var tick = rect(comp, "tick_" + i, 56, 5, GOLD, 100, lx, y + 4);
      wipeIn(tick, ti, ti + 0.30, lx, y + 4);
      var lab = text(comp, spec.items[i], FONT_LBL, 34, WHITE, 40, "left");
      revealUp(lab, ti + 0.10, lx + 78, y + 12, 26);
    }
  }
  function buildSeam(comp, spec) {
    rect(comp, "seam_bg", W, H, [0, 0, 0], 100, W / 2, H / 2);
    if (spec.seam === "dust") {
      for (var i = 0; i < 60; i++) {
        var x = (i * 173) - Math.floor((i * 173) / W) * W;
        var y = (i * 311) - Math.floor((i * 311) / H) * H;
        var d = circle(comp, "g_" + i, x, y, 4 + (i - Math.floor(i / 3) * 3) * 3, DUST, 0, false);
        d.blendingMode = BlendingMode.ADD;
        key2(tg(d).property("ADBE Position"), 0, [x, y + 26], spec.dur, [x, y - 26], 30);
        var o = tg(d).property("ADBE Opacity");
        o.setValueAtTime(0, 0); o.setValueAtTime(spec.dur * 0.5, 26); o.setValueAtTime(spec.dur, 0);
        ease(o, 55);
      }
      var wash = rect(comp, "wash", W, H, [0, 0, 0], 0, W / 2, H / 2);
      var wr = wash.property("ADBE Effect Parade").addProperty("ADBE Ramp");
      wr.property("ADBE Ramp-0001").setValue([W / 2, H * 0.5]);
      wr.property("ADBE Ramp-0002").setValue(GOLD);
      wr.property("ADBE Ramp-0003").setValue([W / 2, H]);
      wr.property("ADBE Ramp-0004").setValue([0, 0, 0]);
      wr.property("ADBE Ramp-0005").setValue(2);
      wash.blendingMode = BlendingMode.ADD;
      var wo = tg(wash).property("ADBE Opacity");
      wo.setValueAtTime(0, 0); wo.setValueAtTime(spec.dur * 0.45, 16); wo.setValueAtTime(spec.dur, 0);
      ease(wo, 60);
    } else {
      // Motion blur spreads a thin bar's energy over its travel, which turned a
      // GOLD streak into a dull olive smear. Compensate with a hotter colour and
      // a crisp unblurred core so the wipe still reads as gold.
      var bar = rect(comp, "strike", 34, H * 1.5, [1.0, 0.86, 0.45], 0, -240, H / 2);
      bar.blendingMode = BlendingMode.ADD;
      bar.motionBlur = true;
      tg(bar).property("ADBE Rotate Z").setValue(12);
      key2(tg(bar).property("ADBE Position"), 0.05, [-240, H / 2], spec.dur - 0.05, [W + 240, H / 2], 55);
      var bo = tg(bar).property("ADBE Opacity");
      bo.setValueAtTime(0.05, 0); bo.setValueAtTime(spec.dur * 0.4, 100); bo.setValueAtTime(spec.dur - 0.05, 0);
      var core = rect(comp, "strike_core", 8, H * 1.5, [1, 1, 1], 0, -240, H / 2);
      core.blendingMode = BlendingMode.ADD;
      tg(core).property("ADBE Rotate Z").setValue(12);
      key2(tg(core).property("ADBE Position"), 0.05, [-240, H / 2], spec.dur - 0.05, [W + 240, H / 2], 55);
      var co = tg(core).property("ADBE Opacity");
      co.setValueAtTime(0.05, 0); co.setValueAtTime(spec.dur * 0.4, 85); co.setValueAtTime(spec.dur - 0.05, 0);
      var fl = rect(comp, "flash", W, H, [1, 1, 1], 0, W / 2, H / 2);
      fl.blendingMode = BlendingMode.ADD;
      var fo = tg(fl).property("ADBE Opacity");
      fo.setValueAtTime(spec.dur * 0.30, 0); fo.setValueAtTime(spec.dur * 0.45, 10);
      fo.setValueAtTime(spec.dur * 0.62, 0); ease(fo, 60);
    }
  }

  function build(spec) {
    var comp = proj.items.addComp("LECH_" + spec.id, W, H, 1.0, spec.dur, FPS);
    comp.motionBlur = true;
    if (spec.layout === "SEAM") { buildSeam(comp, spec); return comp; }
    rect(comp, "bg", W, H, [0, 0, 0], 100, W / 2, H / 2);
    if (spec.layout === "HOUSE_SCHEMATIC") {
      buildHouse(comp, spec);
      caption(comp, spec);
      dip(comp, spec);
      return comp;
    }
    var base;
    if (spec.layout === "ACT_TITLE") base = 52;
    else if (spec.layout === "CLAUSE_STRIKE") base = 28;
    addStill(comp, spec, base);
    polish(comp, spec);
    scrim(comp, spec.layout === "CLAUSE_STRIKE" ? 46 : 34);
    if (spec.layout === "DATE_STAMP") buildDate(comp, spec);
    else if (spec.layout === "QUOTE_STAMP") buildQuote(comp, spec);
    else if (spec.layout === "MONEY_STACK") buildMoney(comp, spec);
    else if (spec.layout === "CLAUSE_STRIKE") buildClause(comp, spec);
    else if (spec.layout === "ACT_TITLE") buildAct(comp, spec);
    else throw new Error("unsupported layout " + spec.layout + " on " + spec.id);
    caption(comp, spec);
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
    raise SystemExit(build())
