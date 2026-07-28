#!/usr/bin/env python
"""EP41 Thompson - AE hero-card JSX generator (ledger-locked).

Built on the audited EP40 build_lech_hero_cards.py structure. EP41-specific:
  * 5 layouts: LABEL_STAMP, CENTER_STACK, COMPARE_STRIKE, DATE_STAMP, VOTE_SPLIT
  * 3 count types: CT_INT, CT_MONEY, CT_DATE (CT_DATE = thousands OFF; a year
    must NEVER render as 1,999 -- that is an instant bug per DESIGN v001 6.5)
  * colour constants are the EP41 gold/sodium/steel palette (DESIGN v001 6.5)

LEDGER LOCK (DESIGN v001 section 1.4). Only these screen numbers are allowed;
num_id outside this set is a HARD exit(1) so no off-ledger figure can ship
(the EP40 fabricated $580,000 defence):
  N01 New Orleans 1984-1985 | N02 type B / type O | N03 fourteen years
  N04 eighteen years | N06 April 16, 1999 / May 20, 1999 | N08 $14 million
  N09 5 to 4 | N11 four prosecutors

Every burned label is copied verbatim from DESIGN v001 section 6.4. No caption
text is invented (the script carries no CARD markers), so caption == "".

Machine traps honoured (DESIGN v001 6.6 / CLAUDE.md):
  runtime font resolve with unwrap() + HARD FAIL (no silent substitute),
  spatial-aware setTemporalEaseAtKey dim, NO app.newProject(), per-layer
  motionBlur, "ADBE Rotate Z", explicit inPoint AND outPoint,
  conformFrameRate=30, single-line TextDocument only, SOFTWARE gpu, localized
  RS/OM template names first, all display strings precomputed in Python,
  ASCII-only labels (em-dash -> '-'), completion marker file, app.quit().
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(r"C:\Users\aab15\Documents\prime-documentary")
EP = "PD-2026-041-thompson"
SPEC_OUT = ROOT / "episodes" / "_planning" / "EP41_thompson_hero_beats.spec.v001.json"
REPO_BEATS = ROOT / "episodes" / EP / "08_edit" / "ae_hero" / "beats.json"
WORK = Path("H:/pd-media/episodes/PD-2026-041-thompson/08_edit/ae_hero")
RENDER = WORK / "render"
STILLS = Path("H:/pd-media/assets/ai/thompson")

FPS = 30
W, H = 1920, 1080

# DESIGN v001 section 6.5 colour constants (0..1 float)
GOLD = [0.898, 0.710, 0.227]    # #E5B53A brand accent (numbers / underline)
WHITE = [0.961, 0.969, 0.980]   # #F5F7FA
SILVER = [0.784, 0.804, 0.839]  # #C8CDD6
SODIUM = [0.788, 0.541, 0.227]  # #C98A3A single practical light glow
STEEL = [0.165, 0.180, 0.200]   # #2A2E33 wash / vignette
RED = [0.780, 0.290, 0.250]     # COMPARE_STRIKE mismatch mark only

# Allowed screen numbers (DESIGN v001 section 1.4). num_id NOT here => exit(1).
LEDGER_IDS = {"N01", "N02", "N03", "N04", "N05", "N06", "N07",
              "N08", "N09", "N10", "N11", "N12"}

# advance-width factors measured off Anton / Oswald cap-height specimens
ANTON_ADV = 0.470
OSWALD_ADV = 0.505


def fit_size(text: str, base: int, max_w: int, adv: float, tracking: int = 0) -> int:
    n = max(1, len(text))
    per = adv + (tracking / 1000.0)
    size = min(base, int(max_w / (per * n)))
    return max(18, size)


def count_keys(target, t0, t1, prefix="", suffix="", thousands=False,
               decimals=0, n=20):
    """Ease-out-cubic count-up. Python formats EVERY display string; the JSX
    never does arithmetic on a number (CLAUDE.md rule). thousands=False for
    CT_INT and CT_DATE so a year renders 1999, never 1,999."""
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
        v = target * (1.0 - (1.0 - p) ** 3)          # ease-out cubic
        keys.append((t0 + (t1 - t0) * p, fmt(v)))
    keys.append((t1 + 0.02, fmt(target)))            # settle to exact
    return [[round(t, 4), s] for t, s in keys]


# --------------------------------------------------------------- the card deck
# still_content_verified: written after EYEBALLING a labelled contact sheet of
# every available render (S01..S23). Never inferred from the S## number (the
# EP39 S44 mistake). b06/b07/b08 backgrounds (S28/S30/S31/S37) are not yet
# generated, so b07 falls back to a dark vector card (DESIGN v001 allows this).
CARDS = [
    dict(
        id="b01", layout="LABEL_STAMP", num_id="N01", dur=5.0,
        top="THE CITY WANTED AN ANSWER", main="NEW ORLEANS 1984-1985",
        bottom=None, still="S04.png",
        svc="Empty prosecutor's office at night: bare wooden desk, one empty "
            "chair, a single file squared on the blotter under a sodium lamp, "
            "filing cabinet in shadow. Verified on contact sheet. Chosen as the "
            "state's seat where the case began; no people, no readable text.",
    ),
    dict(
        id="b02", layout="CENTER_STACK", num_id="N03", count_type="CT_INT",
        dur=6.5, top="ON DEATH ROW", value=14, suffix=" YEARS",
        bottom="MORNING AFTER MORNING", still="S15.png",
        svc="Interior of a single prison cell head-on: narrow bunk, steel "
            "toilet, bare concrete, one small barred window with weak grey "
            "light. Verified on contact sheet. The room the fourteen years "
            "were spent in; no people.",
    ),
    dict(
        id="b03", layout="COMPARE_STRIKE", num_id="N02", dur=7.0,
        top="THE CRIME LAB HAD ALREADY TYPED IT",
        left="THE BLOOD: TYPE B", right="THOMPSON: TYPE O",
        bottom="IT WAS NEVER HIS", still="S12.png",
        svc="Macro of a crime-lab report form under raking light, printed "
            "characters blurred and completely illegible. Verified on contact "
            "sheet. Illegible on purpose (R1) so the B/O type is spoken only "
            "by the typography, never read off the document.",
    ),
    dict(
        id="b04", layout="CENTER_STACK", num_id="N04", count_type="CT_INT",
        dur=6.5, top="WHAT THE STATE TOOK", value=18, suffix=" YEARS",
        bottom="GONE", still="S14.png",
        svc="Dim death-row cellblock tier receding into shadow with a single "
            "steel door lit at the far end. Verified on contact sheet. The "
            "corridor of the eighteen years taken; no people.",
    ),
    dict(
        id="b05", layout="DATE_STAMP", num_id="N06", count_type="CT_DATE",
        dur=6.5, top="LOUISIANA SET THE DATE", value=1999,
        bottom="EXECUTION SET FOR MAY 20",
        footnote="DATE SET APRIL 16 - NOT THE DAY OF EXECUTION",
        still="S22.png",
        svc="A calendar grid on a wall with two separate cells picked out by "
            "isolated pools of light while the rest falls to shadow, numbers "
            "abstract. Verified on contact sheet. Two lit cells match the two "
            "dates the footnote separates (set April 16 vs execution May 20).",
    ),
    dict(
        id="b06", layout="CENTER_STACK", num_id="N08", count_type="CT_MONEY",
        dur=7.0, top="A JURY OF CITIZENS AWARDED", value=14000000,
        prefix="$", thousands=True, bottom="ONE FIGURE FOR EIGHTEEN YEARS",
        still="S05.png",
        svc="Empty jury box of twelve vacant wooden seats in a dim courtroom, "
            "frontal, long shadows across the rail. Verified on contact sheet. "
            "The jury that awarded the fourteen million; no people.",
    ),
    dict(
        # 5-4 reversal. Connick v. Thompson, 563 U.S. 51 (2011): majority 5,
        # dissent 4. Majority is shown FIRST (left). Ledger N09 = "5 to 4".
        id="b07", layout="VOTE_SPLIT", num_id="N09", dur=7.5,
        top="THE SUPREME COURT", left="5", right="4",
        bottom="REVERSED - EVERY DOLLAR GONE", still=None,
        svc="No photograph used. No Supreme Court interior render exists yet "
            "(S30/S31 not generated), and pairing a generic courtroom bench "
            "would mis-sell it as the Supreme Court, so this is a pure dark "
            "vector split on near-black. The 5-4 is real (Connick v. "
            "Thompson, 563 U.S. 51) and burned neutrally as 'reversed'.",
    ),
    dict(
        id="b08", layout="CENTER_STACK", num_id="N11", count_type="CT_INT",
        dur=6.0, top="INSIDE ORLEANS PARISH", value=4, suffix=" PROSECUTORS",
        bottom="KNEW THE BLOOD WAS NOT HIS", still="S09.png",
        svc="Anonymous hands stamping a manila folder at a booking/records "
            "desk in hard side light, cropped so no face shows. Verified on "
            "contact sheet. The machinery of the office where prosecutors "
            "knew; the four-folder render (S37) is not generated yet.",
    ),
]


def build():
    WORK.mkdir(parents=True, exist_ok=True)
    RENDER.mkdir(parents=True, exist_ok=True)
    REPO_BEATS.parent.mkdir(parents=True, exist_ok=True)
    for m in ("_build_ok.txt", "_error.txt"):
        (WORK / m).unlink(missing_ok=True)

    beats = []
    for c in CARDS:
        if c.get("num_id") and c["num_id"] not in LEDGER_IDS:
            print(f"FAIL off-ledger num_id {c['num_id']} on {c['id']}",
                  file=sys.stderr)
            return 1

        still_path = None
        if c.get("still"):
            p = STILLS / c["still"]
            if not p.exists():
                print(f"FAIL missing still {p}", file=sys.stderr)
                return 2
            still_path = str(p).replace("\\", "/")

        b = dict(
            id=c["id"], layout=c["layout"], num_id=c.get("num_id"),
            count_type=c.get("count_type"), dur=float(c["dur"]),
            still=still_path, still_content_verified=c["svc"],
            top=c.get("top", ""), bottom=c.get("bottom") or "",
            caption="", footnote=c.get("footnote"),
            head=round(4 / FPS, 4), tail=round(4 / FPS, 4),
            start=None, end=None,          # assigned when the film timeline locks
            out=str(RENDER / f"{c['id']}.mp4").replace("\\", "/"),
        )

        if c["layout"] == "LABEL_STAMP":
            b["main"] = c["main"]
            b["mainSize"] = fit_size(c["main"], 170, 1620, ANTON_ADV)
        elif c["layout"] == "CENTER_STACK":
            ct = c["count_type"]
            t0, t1 = 0.65, 1.85            # 1.20s count, then hold to dur
            b["numKeys"] = count_keys(
                c["value"], t0, t1,
                prefix=c.get("prefix", ""), suffix=c.get("suffix", ""),
                thousands=bool(c.get("thousands", False)))
            hold = c["dur"] - (t1 + 0.02)
            if hold < 1.20:
                print(f"FAIL count hold {hold:.2f}s < 1.20s on {c['id']}",
                      file=sys.stderr)
                return 3
            final = b["numKeys"][-1][1]
            if ct == "CT_DATE" and ("," in final):
                print(f"FAIL CT_DATE produced comma '{final}' on {c['id']}",
                      file=sys.stderr)
                return 4
            b["heroSize"] = fit_size(final, 280 if ct == "CT_MONEY" else 300,
                                     1620, ANTON_ADV)
        elif c["layout"] == "DATE_STAMP":
            t0, t1 = 0.65, 1.85
            b["numKeys"] = count_keys(c["value"], t0, t1, thousands=False)
            if "," in b["numKeys"][-1][1]:
                print(f"FAIL CT_DATE comma on {c['id']}", file=sys.stderr)
                return 4
            hold = c["dur"] - (t1 + 0.02)
            if hold < 1.20:
                print(f"FAIL date hold {hold:.2f} < 1.20 on {c['id']}",
                      file=sys.stderr)
                return 3
            b["heroSize"] = fit_size(str(c["value"]), 300, 1200, ANTON_ADV)
        elif c["layout"] == "COMPARE_STRIKE":
            b["left"], b["right"] = c["left"], c["right"]
            b["sizeL"] = fit_size(c["left"], 78, 820, OSWALD_ADV, 20)
            b["sizeR"] = fit_size(c["right"], 78, 820, OSWALD_ADV, 20)
        elif c["layout"] == "VOTE_SPLIT":
            b["left"], b["right"] = c["left"], c["right"]

        beats.append(b)

    doc = {
        "schema_version": "thompson_beats.v1",
        "episode_id": EP,
        "fps": FPS, "width": W, "height": H,
        "render_dir": str(RENDER).replace("\\", "/"),
        "ledger_note": (
            "Every screen number is a DESIGN v001 section 1.4 ledger id "
            "(N01-N11). num_id outside that set is a build-time exit(1). "
            "Connick v. Thompson, 563 U.S. 51 (2011) is a real 5-4 Supreme "
            "Court reversal; the 5-4 is burned neutrally as 'reversed'."),
        "timeline_note": (
            "start/end are null until the film timeline is locked; the "
            "compositor assigns them then and SKIPs any beat still missing "
            "them or lacking a base render."),
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
    jsx = jsx.replace("__SODIUM__", ",".join(str(v) for v in SODIUM))
    jsx = jsx.replace("__STEEL__", ",".join(str(v) for v in STEEL))
    jsx = jsx.replace("__RED__", ",".join(str(v) for v in RED))
    jsx = jsx.replace("__BEATS__", json.dumps(beats, ensure_ascii=False))
    jsx = jsx.replace("__RENDER__", str(WORK).replace("\\", "/"))
    jsx = jsx.replace("__AEP__", str(WORK / "thompson_hero.aep").replace("\\", "/"))
    (WORK / "thompson_hero.jsx").write_text(jsx, encoding="utf-8-sig")

    print(f"[gen] {len(beats)} cards, total {sum(b['dur'] for b in beats):.1f}s")
    for b in beats:
        label = b.get("main") or (b["numKeys"][-1][1] if b.get("numKeys")
                 else (b.get("left", "") + " / " + b.get("right", "")).strip(" /") or b["layout"])
        print(f"  {b['id']:<4} {b['layout']:<15} {b['num_id'] or '-':<4} "
              f"{b['dur']:>4.1f}s  {label}")
    print("[gen] jsx  ->", WORK / "thompson_hero.jsx")
    print("[gen] spec ->", SPEC_OUT)
    return 0


JSX = r"""// AUTO-GENERATED - EP41 Thompson AE hero cards. Do not hand-edit.
(function () {
  var W = __W__, H = __H__, FPS = __FPS__;
  var GOLD = [__GOLD__], WHITE = [__WHITE__], SILVER = [__SILVER__],
      SODIUM = [__SODIUM__], STEEL = [__STEEL__], RED = [__RED__];
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
    if (itx instanceof CompItem && String(itx.name).indexOf("THOMPSON_") === 0) itx.remove();
  } } catch (e) {}
  try { proj.gpuAccelType = GpuAccelType.SOFTWARE; } catch (e) {}
  try { proj.bitsPerChannel = 8; } catch (e) {}
  app.beginUndoGroup("thompson_hero");

  // ---- runtime font resolver (AE 2026: allFonts[i] is an array-LIKE wrapper,
  // .familyName off the wrapper is undefined; TextDocument.font wants the
  // PostScript name. Missing font = HARD FAIL, never a silent substitute). ----
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
    var v = rect(comp, "vignette", W, H, [0, 0, 0], 68, W / 2, H / 2);
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
  function scrim(comp, strength) {
    rect(comp, "scrim_full", W, H, [0.01, 0.02, 0.03], strength, W / 2, H / 2);
    var bh = Math.round(H * 1.30);
    var band = rect(comp, "scrim_band", W, bh, [0, 0, 0], 70, W / 2, H * 0.02);
    var m = band.property("ADBE Mask Parade").addProperty("ADBE Mask Atom");
    var s = new Shape();
    s.vertices = [[0, 0], [W, 0], [W, bh], [0, bh]];
    s.closed = true;
    m.property("ADBE Mask Shape").setValue(s);
    m.property("ADBE Mask Feather").setValue([0, 700]);
  }
  function polish(comp, spec) {
    // cold steel grade (EP41 lane), NOT the warm lech grade
    var grade = rect(comp, "cold_grade", W, H, [0.10, 0.12, 0.14], 30, W / 2, H / 2);
    grade.blendingMode = BlendingMode.MULTIPLY;
    vignette(comp);
    // single sodium practical glow, bottom-centre
    var glow = rect(comp, "glow", W, H, [0, 0, 0], 0, W / 2, H / 2);
    var gr = glow.property("ADBE Effect Parade").addProperty("ADBE Ramp");
    gr.property("ADBE Ramp-0001").setValue([W / 2, H * 0.98]);
    gr.property("ADBE Ramp-0002").setValue(SODIUM);
    gr.property("ADBE Ramp-0003").setValue([W / 2, H * 0.40]);
    gr.property("ADBE Ramp-0004").setValue([0, 0, 0]);
    gr.property("ADBE Ramp-0005").setValue(2);
    glow.blendingMode = BlendingMode.ADD;
    var go = tg(glow).property("ADBE Opacity");
    go.setValueAtTime(0, 0); go.setValueAtTime(0.7, 20); go.setValueAtTime(spec.dur, 12); ease(go, 60);
    var sweep = rect(comp, "sweep", 340, H * 1.6, [1, 1, 1], 0, -300, H / 2);
    sweep.blendingMode = BlendingMode.ADD;
    sweep.motionBlur = true;
    tg(sweep).property("ADBE Rotate Z").setValue(18);          // 2D rotation
    key2(tg(sweep).property("ADBE Position"), 0.5, [-300, H / 2], 1.25, [W + 300, H / 2], 45);
    var so = tg(sweep).property("ADBE Opacity");
    so.setValueAtTime(0.5, 0); so.setValueAtTime(0.7, 14); so.setValueAtTime(1.25, 0);
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
  function bottomLabel(comp, spec, t0, y, size) {
    if (!spec.bottom || !spec.bottom.length) return;
    var b = text(comp, spec.bottom, FONT_LBL, size || 58, WHITE, 120);
    revealUp(b, t0, W / 2, y, 46);
  }

  // ---- animated number (count-up) --------------------------------------
  function countText(comp, spec, y) {
    // Build on the FINAL (widest) value so the measured fit covers every frame
    // of the count-up; center-justified strings then stay centred as they grow.
    var last = spec.numKeys[spec.numKeys.length - 1];
    var L = text(comp, last[1], FONT_NUM, spec.heroSize, GOLD, 0);
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

  // ---- layouts ----------------------------------------------------------
  function buildLabel(comp, spec) {
    topLabel(comp, spec, H * 0.235, 46);
    var L = text(comp, spec.main, FONT_NUM, spec.mainSize, GOLD, 6);
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
    accent(comp, H * 0.575, 640);
  }
  function buildCenter(comp, spec) {
    topLabel(comp, spec, H * 0.155, 46);
    countText(comp, spec, H * 0.49);
    accent(comp, H * 0.60, 460);
    bottomLabel(comp, spec, 1.55, H * 0.70, 56);
  }
  function buildDate(comp, spec) {
    topLabel(comp, spec, H * 0.15, 46);
    countText(comp, spec, H * 0.44);
    accent(comp, H * 0.55, 520);
    bottomLabel(comp, spec, 1.55, H * 0.655, 54);
    if (spec.footnote && spec.footnote.length) {
      var fn = text(comp, spec.footnote, FONT_LBL, 30, SILVER, 80);
      tg(fn).property("ADBE Position").setValue([W / 2, H * 0.76]);
      var fo = tg(fn).property("ADBE Opacity");
      fo.setValueAtTime(2.0, 0); fo.setValueAtTime(2.4, 82);
    }
  }
  function buildCompare(comp, spec) {
    topLabel(comp, spec, H * 0.20, 44);
    var yc = H * 0.46, gap = W * 0.25;
    var lx = W / 2 - gap, rx = W / 2 + gap;
    var lL = text(comp, spec.left, FONT_LBL, spec.sizeL, WHITE, 20);
    fitText(lL, 820, comp.duration * 0.5); centerX(lL, comp.duration * 0.5);
    tg(lL).property("ADBE Position").setValue([lx, yc]);
    revealUp(lL, 0.5, lx, yc, 40);
    var rL = text(comp, spec.right, FONT_LBL, spec.sizeR, WHITE, 20);
    fitText(rL, 820, comp.duration * 0.5); centerX(rL, comp.duration * 0.5);
    tg(rL).property("ADBE Position").setValue([rx, yc]);
    revealUp(rL, 0.75, rx, yc, 40);
    // vertical divider between the two values
    var div = rect(comp, "cmp_div", 4, 150, SILVER, 40, W / 2, yc);
    key2(tg(div).property("ADBE Opacity"), 0.9, 0, 1.3, 40, 70);
    // RED mismatch mark: a slash across the divider = the two do NOT match.
    var mark = rect(comp, "cmp_mark", 220, 12, RED, 100, W / 2, yc);
    mark.motionBlur = true;
    tg(mark).property("ADBE Rotate Z").setValue(-24);
    tg(mark).property("ADBE Anchor Point").setValue([110, 6]);
    tg(mark).property("ADBE Position").setValue([W / 2, yc]);
    key2(tg(mark).property("ADBE Scale"), 1.6, [0, 100], 2.15, [100, 100], 90);
    accent(comp, H * 0.585, 520);
    bottomLabel(comp, spec, 1.55, H * 0.68, 54);
  }
  function buildVote(comp, spec) {
    topLabel(comp, spec, H * 0.19, 46);
    var yc = H * 0.44, gap = W * 0.20;
    var lx = W / 2 - gap, rx = W / 2 + gap;
    // MAJORITY on the LEFT (shown first), GOLD and larger; DISSENT on the
    // right, SILVER and smaller. Connick v. Thompson was 5-4 (majority 5).
    var nL = text(comp, spec.left, FONT_NUM, 260, GOLD, 0);     // majority 5
    nL.motionBlur = true;
    tg(nL).property("ADBE Position").setValue([lx, yc]);
    var loo = tg(nL).property("ADBE Opacity");
    loo.setValueAtTime(0.5, 0); loo.setValueAtTime(0.75, 100);
    key2(tg(nL).property("ADBE Scale"), 0.5, [60, 60], 0.9, [100, 100], 78);
    var nR = text(comp, spec.right, FONT_NUM, 220, SILVER, 0);  // dissent 4
    nR.motionBlur = true;
    tg(nR).property("ADBE Position").setValue([rx, yc]);
    var roo = tg(nR).property("ADBE Opacity");
    roo.setValueAtTime(0.7, 0); roo.setValueAtTime(0.95, 100);
    key2(tg(nR).property("ADBE Scale"), 0.7, [60, 60], 1.1, [100, 100], 78);
    // "TO" between them, small
    var to = text(comp, "TO", FONT_LBL, 48, SILVER, 120);
    tg(to).property("ADBE Position").setValue([W / 2, yc - 10]);
    key2(tg(to).property("ADBE Opacity"), 0.9, 0, 1.3, 70, 70);
    // 9 pips row: 5 gold (majority) FIRST, then 4 silver (dissent)
    var pn = 9, pd = 40, pgap = 56, total = (pn - 1) * pgap;
    var y2 = H * 0.63;
    for (var i = 0; i < pn; i++) {
      var px = W / 2 - total / 2 + i * pgap;
      var maj = (i < 5);
      var p = circle(comp, "pip_" + i, px, y2, pd, maj ? GOLD : SILVER, maj ? 100 : 45, false);
      p.motionBlur = true;
      var tt = 1.2 + i * 0.09;
      key2(tg(p).property("ADBE Scale"), tt, [0, 0], tt + 0.30, [100, 100], 80);
      key2(tg(p).property("ADBE Opacity"), tt, 0, tt + 0.30, maj ? 100 : 45, 70);
    }
    bottomLabel(comp, spec, 2.1, H * 0.75, 50);
  }

  function build(spec) {
    var comp = proj.items.addComp("THOMPSON_" + spec.id, W, H, 1.0, spec.dur, FPS);
    comp.motionBlur = true;
    rect(comp, "bg", W, H, [0.039, 0.039, 0.047], 100, W / 2, H / 2);   // #0A0A0C ink
    if (spec.still) {
      var base = 58;
      if (spec.layout === "COMPARE_STRIKE" || spec.layout === "DATE_STAMP") base = 50;
      addStill(comp, spec, base);
      polish(comp, spec);
      scrim(comp, (spec.layout === "COMPARE_STRIKE" || spec.layout === "DATE_STAMP") ? 46 : 40);
    } else {
      // vector card on near-black: still need the sodium glow + vignette so it
      // shares the film's grade instead of reading as flat black.
      var glow = rect(comp, "glow", W, H, [0, 0, 0], 0, W / 2, H / 2);
      var gr = glow.property("ADBE Effect Parade").addProperty("ADBE Ramp");
      gr.property("ADBE Ramp-0001").setValue([W / 2, H * 0.98]);
      gr.property("ADBE Ramp-0002").setValue(SODIUM);
      gr.property("ADBE Ramp-0003").setValue([W / 2, H * 0.35]);
      gr.property("ADBE Ramp-0004").setValue([0, 0, 0]);
      gr.property("ADBE Ramp-0005").setValue(2);
      glow.blendingMode = BlendingMode.ADD;
      tg(glow).property("ADBE Opacity").setValue(16);
      vignette(comp);
    }
    if (spec.layout === "LABEL_STAMP") buildLabel(comp, spec);
    else if (spec.layout === "CENTER_STACK") buildCenter(comp, spec);
    else if (spec.layout === "DATE_STAMP") buildDate(comp, spec);
    else if (spec.layout === "COMPARE_STRIKE") buildCompare(comp, spec);
    else if (spec.layout === "VOTE_SPLIT") buildVote(comp, spec);
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
