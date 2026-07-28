#!/usr/bin/env python
"""EP45 Cleveland - AE hero-card JSX generator (ledger-locked, AE-2026-JP pipeline).

Cloned from the audited EP41 build_thompson_hero_cards.py. EP45-specific:
  * accent = warrant-blue #B23A48 (NOT the EP41 gold) -- lane separation
  * 6 layouts used from the proven set: ACT_TITLE_CARD / CENTER_STACK /
    QUOTE_CARD / VOTE_SPLIT / MONEY_STACK / SPLIT_COMPARE
  * every card burns an "AI-assisted visualization" disclosure (R1) bottom-right
  * count types CT_INT / CT_MONEY / CT_TEXT (CT_TEXT = no count-up; SECTION 1983
    is a statute number, must NEVER animate/comma)

LEDGER LOCK (episodes/PD-2026-045-cleveland/03_script/cleveland_facts.v001.json). Every
burned number is a verified:true F-ID value. No off-ledger figure can ship: a
num_id whose fact is missing/verified:false is a HARD exit(1) (the EP40
fabricated $580,000 defence).

Accuracy 6-constraint compliance baked into the strings (§2 of CODEX_B):
  C-1 settlement != finding  -> m01 sub "REPORTED - NO FINDING OF FAULT"
  C-2 valid warrant only     -> n01 sub "A SEARCH WARRANT, SIGNED BY A JUDGE";
                                NO "no-knock" anywhere
  C-3 reform voted down      -> r01 "REJECTED" / "STILL LEGAL" (never "changed the law")
  C-4 Hudson scope intact    -> k01 "STILL A COMMAND ..." attributed to Scalia;
                                v01 sub "THE EXCLUSION REMEDY, DENIED"
  Forbidden strings (no-knock / no knock / unconstitutional / she changed the law
  / changed the law / 988) appear on NO card. Asserted at build time.

Machine traps honoured (§7.5 / CLAUDE.md): runtime font resolve with unwrap() +
HARD FAIL (no silent substitute), spatial-aware setTemporalEaseAtKey dim, NO
app.newProject(), per-layer motionBlur, "ADBE Rotate Z", explicit inPoint AND
outPoint, conformFrameRate=30, single-line TextDocument, SOFTWARE gpu, localized
RS/OM template names first, all display strings precomputed in Python,
ASCII-only labels, completion marker file, app.quit(). The .aep is saved by the
JSX; the caller asserts .aep mtime > .jsx mtime before aerender (stale-aep guard).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(r"C:\Users\aab15\Documents\prime-documentary")
EP = "PD-2026-045-cleveland"
FACTS = ROOT / "episodes" / EP / "03_script" / "cleveland_facts.v001.json"
FILM = ROOT / "remotion" / "src" / "data" / "cleveland_film.json"
NARR = ROOT / "episodes" / EP / "06_audio" / "narration_index.v001.json"
REPO_BEATS_DIR = ROOT / "episodes" / EP / "08_edit" / "ae_hero"

FPS = 30
W, H = 1920, 1080

# §7.3 EP45 colour constants (0..1 float). cold courthouse lane, Alabama-debt tone.
ACCENT = [0.698, 0.227, 0.282]   # #B23A48 crimson (EP45 lane) numbers / underline / dissent
WHITE = [0.961, 0.969, 0.980]    # #F5F7FA
SILVER = [0.784, 0.804, 0.839]   # #C8CDD6 labels / disclosure / majority
INK = [0.039, 0.039, 0.047]      # #0A0A0C near-black root
DAWN = [0.788, 0.541, 0.227]     # #C98A3A single doorway/dawn practical glow
RED = [0.780, 0.290, 0.243]      # #C74A3E r01 REJECTED mark only

STILLS = Path("H:/pd-media/assets/ai/cleveland")

# Bookend offset: figures[] and these AE beats are body/narration-relative.
# Absolute time in the finished bookended base mp4 = start + FILM_OFFSET_SEC.
OPENING_SEC = 3.5

# advance-width factors (Anton / Oswald cap-height specimens) -- starting-size
# estimate only; the JSX re-fits with sourceRectAtTime (measured, never clipped).
ANTON_ADV = 0.470
OSWALD_ADV = 0.505

FORBIDDEN = ["no-knock", "no knock", "unconstitutional",
             "she changed the law", "changed the law", "988"]


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
# still names were eyeballed in the Codex contact sheets: all people-free
# symbolic objects, no readable text, no faces/bodies (R1 / C-4 / C-6).
DECK = [
    # 1. The court order: $1,554 owed, or 31 days sat out in jail (F04/F05).
    dict(id="p01", layout="MONEY_STACK", count_type="CT_MONEY", anchor=112.6, dur=6.5,
         top="THE COURT ORDER", value=1554, prefix="$", thousands=True,
         bottom="OR 31 DAYS IN JAIL", still=None,
         nums=[("F04", 1554), ("F05", 31)]),
    # 2. No ability-to-pay hearing -- the Bearden violation, stated plainly.
    dict(id="h01", layout="CENTER_STACK", count_type="CT_TEXT", anchor=127.1, dur=6.0,
         top="NO HEARING", hero_text="ON WHETHER SHE COULD PAY",
         bottom="ABILITY TO PAY WAS NEVER ASKED", still=None,
         nums=[]),
    # 3. For-profit probation skim: ~$40 of every ~$200/month went to JCS (F06/F07).
    #    FFJC attribution is REQUIRED verbatim so the m01 R-MEDIUM-ATTRIB gate passes.
    dict(id="m01", layout="MONEY_STACK", count_type="CT_MONEY", anchor=192.4, dur=6.5,
         top="THE PRIVATE SKIM", value=40, prefix="$",
         bottom="OF EVERY $200 - PER THE FINES & FEES JUSTICE CENTER", still=None,
         nums=[("F06", 40), ("F07", 200)]),
    # 4. The controlling Supreme Court line: Bearden v. Georgia, 1983 (F01).
    dict(id="b01", layout="CENTER_STACK", count_type="CT_TEXT", anchor=307.0, dur=6.5,
         top="1983", hero_text="BEARDEN v. GEORGIA",
         bottom="ABILITY TO PAY, THEN ALTERNATIVES, BEFORE JAIL", still=None,
         nums=[("F01", 1983)]),
    # 5. O'Connor for the Court -- the holding in her words (attributed "for the Court").
    dict(id="q01", layout="QUOTE_CARD", anchor=389.8, dur=7.0,
         top="THE SUPREME COURT, 1983",
         quote=("IT IS FUNDAMENTALLY UNFAIR TO REVOKE PROBATION AUTOMATICALLY, "
                "WITHOUT CONSIDERING WHETHER AN ADEQUATE ALTERNATIVE TO PRISON EXISTS"),
         attribution="JUSTICE O'CONNOR, FOR THE COURT",
         attribution_canonical="Justice O'Connor, for the Court",
         still=None, nums=[]),
    # 6. Cleveland's relief came from a 2014 LOWER-COURT settlement, not SCOTUS (F09).
    dict(id="s01", layout="CENTER_STACK", count_type="CT_TEXT", anchor=486.5, dur=6.0,
         top="2014", hero_text="SETTLED IN A LOWER COURT",
         bottom="A SETTLEMENT, NOT THE SUPREME COURT", still=None,
         nums=[("F09", 2014)]),
    # 7. ENDING (r01): the rule has held since 1983 -- yet the practice continued;
    #    her remedy was a lower court, not the Supreme Court (F01/F09/F11).
    #    bottom MUST carry "yet it continued" + "lower court" + "not the supreme court"
    #    for the r01 R-SCOTUS gate. ("unconstitutional" is banned by the builder gate.)
    dict(id="r01", layout="SPLIT_COMPARE", anchor=523.6, dur=6.5,
         top="THE RULE SINCE 1983", left="1983", right="2014",
         strike="STILL HAPPENING",
         bottom="YET IT CONTINUED - A LOWER COURT, NOT THE SUPREME COURT", still=None,
         nums=[("F01", 1983), ("F09", 2014)]),
]


def load_facts() -> dict:
    d = json.loads(FACTS.read_text(encoding="utf-8"))
    return d.get("facts", d)


def figure_intervals() -> list[tuple[float, float]]:
    if not FILM.exists():
        return []
    d = json.loads(FILM.read_text(encoding="utf-8"))
    return [(float(f["start"]), float(f["end"])) for f in d.get("figures") or []]


def narration_total() -> float:
    if FILM.exists():
        d = json.loads(FILM.read_text(encoding="utf-8"))
        if d.get("narrationSeconds"):
            return float(d["narrationSeconds"])
    return 712.34


def clear(s: float, d: float, figs, placed, total: float, buf: float = 0.8) -> bool:
    e = s + d
    if s < 21.0 or e > total - 12.0:
        return False
    for a, b in figs:
        if s < b + buf and a - buf < e:
            return False
    for a, b in placed:
        if s < b + 0.5 and a - 0.5 < e:
            return False
    return True


def place(anchor: float, dur: float, figs, placed, total: float) -> float:
    lo = 21.0
    if placed:
        lo = max(lo, placed[-1][1] + 1.0)
    start = max(anchor, lo)
    s = start
    while s < total - 12.0 - dur:
        if clear(s, dur, figs, placed, total):
            return round(s, 3)
        s += 0.25
    s = start
    while s > lo:
        if clear(s, dur, figs, placed, total):
            return round(s, 3)
        s -= 0.25
    raise SystemExit(f"cannot place card anchor={anchor} dur={dur}")


def build(dryrun: bool) -> int:
    facts = load_facts()
    figs = figure_intervals()
    total = narration_total()
    offset = round(8.0 + OPENING_SEC, 3)
    if FILM.exists():
        d = json.loads(FILM.read_text(encoding="utf-8"))
        offset = round(float(d.get("hookSeconds", 8.0)) + OPENING_SEC, 3)

    work = (ROOT / "episodes" / EP / "08_edit" / ("_dryrun/ae_hero" if dryrun else "ae_hero"))
    # Render cards to the REPO path (C:) -- AE's H.264 OM failed to write to the H:
    # (exFAT) drive silently (queue=7 but 0 mp4s); tekoh renders to the repo path and works.
    media = work
    render = media / "render"
    media.mkdir(parents=True, exist_ok=True)
    render.mkdir(parents=True, exist_ok=True)
    REPO_BEATS_DIR.mkdir(parents=True, exist_ok=True)
    for m in ("_build_ok.txt", "_error.txt"):
        (render / m).unlink(missing_ok=True)

    # ---- ledger gate: every burned number must be verified:true --------------
    for c in DECK:
        for fid, val in c.get("nums", []):
            f = facts.get(fid)
            if not f or not f.get("verified"):
                print(f"FAIL off-ledger/unverified {fid} on {c['id']}", file=sys.stderr)
                return 1

    beats, placed = [], []
    for c in DECK:
        start = place(c["anchor"], float(c["dur"]), figs, placed, total)
        end = round(start + float(c["dur"]), 3)
        placed.append((start, end))

        still_path = None
        if c.get("still"):
            p = STILLS / c["still"]
            if not p.exists():
                print(f"FAIL missing still {p}", file=sys.stderr)
                return 2
            still_path = str(p).replace("\\", "/")

        b = dict(
            id=c["id"], layout=c["layout"], count_type=c.get("count_type"),
            start=start, end=end, dur=float(c["dur"]),
            still=still_path, top=c.get("top", ""), bottom=c.get("bottom", ""),
            caption="", hero="", value=None, numKeys=None,
            attribution=c.get("attribution_canonical"),
            blend_mode="overlay", required=True,
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
            b["attribution_display"] = c["attribution"]
            b["quoteSize"] = fit_size(c["quote"], 96, 1560, OSWALD_ADV, 10)
        elif c["layout"] == "VOTE_SPLIT":
            b["left"], b["right"] = c["left"], c["right"]
            b["hero"] = f"{c['left']} TO {c['right']}"
        elif c["layout"] == "SPLIT_COMPARE":
            b["left"], b["right"] = c["left"], c["right"]
            b["strike"] = c["strike"]
            b["hero"] = f"{c['left']} - {c['right']}"

        # forbidden-string assertion over EVERY visible string on this card
        blob = " ".join(str(x) for x in (
            b.get("top"), b.get("bottom"), b.get("hero"), b.get("caption"),
            b.get("attribution_display"), b.get("attribution"), b.get("strike"),
        ) if x).lower()
        for bad in FORBIDDEN:
            if bad in blob:
                print(f"FAIL forbidden string '{bad}' on {c['id']}", file=sys.stderr)
                return 4

        beats.append(b)

    doc = {
        "schema_version": "cleveland_ae_beats.v1",
        "episode_id": EP, "fps": FPS, "width": W, "height": H,
        "timebase": "narration_body_relative",
        "film_offset_sec": offset,
        "offset_note": (
            "start/end are body/narration-relative (same timeline as "
            "cleveland_film.json figures[]). Absolute time in the finished bookended "
            "base mp4 = start + film_offset_sec (hookSeconds + OPENING_SEC "
            f"= {offset}s). The compositor must add this offset when overlaying "
            "on the full-film base, or run against a narration-relative base."),
        "accent": "#B23A48",
        "ledger_note": (
            "Every burned number is a cleveland_facts.v001.json verified:true F-ID "
            "($1,554/31/100+/2013/1983/2014). All EP45 prohibited terms were "
            "asserted absent from every card string at build time (FORBIDDEN "
            "gate in the builder); this note is deliberately term-free so it "
            "cannot trip R-FORBID."),
        "render_dir": str(render).replace("\\", "/"),
        "beats": beats,
    }
    payload = json.dumps(doc, ensure_ascii=False, indent=2)
    (media / "beats.json").write_text(payload, encoding="utf-8")
    (REPO_BEATS_DIR / "beats.json").write_text(payload, encoding="utf-8")

    jsx = JSX
    jsx = jsx.replace("__W__", str(W)).replace("__H__", str(H)).replace("__FPS__", str(FPS))
    jsx = jsx.replace("__ACCENT__", ",".join(str(v) for v in ACCENT))
    jsx = jsx.replace("__WHITE__", ",".join(str(v) for v in WHITE))
    jsx = jsx.replace("__SILVER__", ",".join(str(v) for v in SILVER))
    jsx = jsx.replace("__INK__", ",".join(str(v) for v in INK))
    jsx = jsx.replace("__DAWN__", ",".join(str(v) for v in DAWN))
    jsx = jsx.replace("__RED__", ",".join(str(v) for v in RED))
    jsx = jsx.replace("__BEATS__", json.dumps(beats, ensure_ascii=False))
    jsx = jsx.replace("__RENDER__", str(render).replace("\\", "/"))
    jsx = jsx.replace("__AEP__", str(media / "cleveland_hero.aep").replace("\\", "/"))
    (media / "cleveland_hero.jsx").write_text(jsx, encoding="utf-8-sig")

    print(f"[gen] {len(beats)} cards, total {sum(b['dur'] for b in beats):.1f}s"
          f" | offset={offset}s | dryrun={dryrun}")
    for b in beats:
        print(f"  {b['id']:<4} {b['layout']:<15} start={b['start']:>6.1f} "
              f"end={b['end']:>6.1f}  {b['hero']}")
    print("[gen] jsx  ->", media / "cleveland_hero.jsx")
    print("[gen] aep  ->", media / "cleveland_hero.aep")
    print("[gen] beats->", REPO_BEATS_DIR / "beats.json")
    return 0


JSX = r"""// AUTO-GENERATED - EP45 Cleveland AE hero cards. Do not hand-edit.
(function () {
  var W = __W__, H = __H__, FPS = __FPS__;
  var ACCENT = [__ACCENT__], WHITE = [__WHITE__], SILVER = [__SILVER__],
      INK = [__INK__], DAWN = [__DAWN__], RED = [__RED__];
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
    if (itx instanceof CompItem && String(itx.name).indexOf("CLEVELAND_") === 0) itx.remove();
  } } catch (e) {}
  try { proj.gpuAccelType = GpuAccelType.SOFTWARE; } catch (e) {}
  try { proj.bitsPerChannel = 8; } catch (e) {}
  app.beginUndoGroup("cleveland_hero");

  // ---- runtime font resolver (AE 2026: allFonts[i] is an array-LIKE wrapper;
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
  // center the whole (possibly multi-line) glyph box on the layer's position
  function centerBlock(L, t) {
    var r = srect(L, t);
    tg(L).property("ADBE Anchor Point").setValue([r.left + r.width / 2, r.top + r.height / 2]);
    return r;
  }
  // greedy word-wrap into "\r"-separated lines (AE paragraph break) so a long
  // quote renders as clean multi-line text instead of one tiny/clipped line.
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
  function scrim(comp, strength) {
    rect(comp, "scrim_full", W, H, [0.01, 0.02, 0.04], strength, W / 2, H / 2);
    var bh = Math.round(H * 1.30);
    var band = rect(comp, "scrim_band", W, bh, [0, 0, 0], 72, W / 2, H * 0.02);
    var m = band.property("ADBE Mask Parade").addProperty("ADBE Mask Atom");
    var s = new Shape();
    s.vertices = [[0, 0], [W, 0], [W, bh], [0, bh]];
    s.closed = true;
    m.property("ADBE Mask Shape").setValue(s);
    m.property("ADBE Mask Feather").setValue([0, 700]);
  }
  function polish(comp, spec) {
    var grade = rect(comp, "night_grade", W, H, [0.09, 0.11, 0.16], 30, W / 2, H / 2);
    grade.blendingMode = BlendingMode.MULTIPLY;
    vignette(comp);
    // single warm doorway/dawn practical glow, bottom-centre
    var glow = rect(comp, "glow", W, H, [0, 0, 0], 0, W / 2, H / 2);
    var gr = glow.property("ADBE Effect Parade").addProperty("ADBE Ramp");
    gr.property("ADBE Ramp-0001").setValue([W / 2, H * 0.98]);
    gr.property("ADBE Ramp-0002").setValue(DAWN);
    gr.property("ADBE Ramp-0003").setValue([W / 2, H * 0.40]);
    gr.property("ADBE Ramp-0004").setValue([0, 0, 0]);
    gr.property("ADBE Ramp-0005").setValue(2);
    glow.blendingMode = BlendingMode.ADD;
    var go = tg(glow).property("ADBE Opacity");
    go.setValueAtTime(0, 0); go.setValueAtTime(0.7, 18); go.setValueAtTime(spec.dur, 11); ease(go, 60);
    var sweep = rect(comp, "sweep", 340, H * 1.6, [1, 1, 1], 0, -300, H / 2);
    sweep.blendingMode = BlendingMode.ADD;
    sweep.motionBlur = true;
    tg(sweep).property("ADBE Rotate Z").setValue(18);
    key2(tg(sweep).property("ADBE Position"), 0.5, [-300, H / 2], 1.25, [W + 300, H / 2], 45);
    var so = tg(sweep).property("ADBE Opacity");
    so.setValueAtTime(0.5, 0); so.setValueAtTime(0.7, 12); so.setValueAtTime(1.25, 0);
  }
  function vectorBed(comp) {
    // near-black card with the shared glow + vignette so it matches the graded film
    var glow = rect(comp, "glow", W, H, [0, 0, 0], 0, W / 2, H / 2);
    var gr = glow.property("ADBE Effect Parade").addProperty("ADBE Ramp");
    gr.property("ADBE Ramp-0001").setValue([W / 2, H * 0.98]);
    gr.property("ADBE Ramp-0002").setValue(DAWN);
    gr.property("ADBE Ramp-0003").setValue([W / 2, H * 0.35]);
    gr.property("ADBE Ramp-0004").setValue([0, 0, 0]);
    gr.property("ADBE Ramp-0005").setValue(2);
    glow.blendingMode = BlendingMode.ADD;
    tg(glow).property("ADBE Opacity").setValue(14);
    vignette(comp);
  }
  function dip(comp, spec) {
    var d = rect(comp, "dip", W, H, [0, 0, 0], 0, W / 2, H / 2);
    var head = 4 / FPS, tail = 4 / FPS;
    var o = tg(d).property("ADBE Opacity");
    o.setValueAtTime(0, 100); o.setValueAtTime(head, 0);
    o.setValueAtTime(spec.dur - tail, 0); o.setValueAtTime(spec.dur, 100);
    ease(o, 40);
  }
  // R1 disclosure: burned on EVERY card, bottom-right, above the scrim/grade.
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
  function accent(comp, y, w) {
    var L = rect(comp, "accent", w || 460, 6, ACCENT, 95, W / 2, y);
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

  // ---- animated number (count-up) ---------------------------------------
  function countText(comp, spec, y) {
    var last = spec.numKeys[spec.numKeys.length - 1];
    var L = text(comp, last[1], FONT_NUM, spec.heroSize, ACCENT, 0);
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
    var L = text(comp, spec.heroText, FONT_NUM, spec.heroSize, ACCENT, 4);
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

  // ---- layouts ----------------------------------------------------------
  function buildActTitle(comp, spec) {
    topLabel(comp, spec, H * 0.235, 46);
    var L = text(comp, spec.main, FONT_NUM, spec.mainSize, ACCENT, 6);
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
    if (spec.numKeys) countText(comp, spec, H * 0.49);
    else heroStatic(comp, spec, H * 0.49);
    accent(comp, H * 0.60, 460);
    bottomLabel(comp, spec, 1.55, H * 0.70, 52);
  }
  function buildQuote(comp, spec) {
    topLabel(comp, spec, H * 0.20, 42);
    // WRAP the long quote to multiple lines at a readable size, then MEASURE and
    // scale down to fit -- never a single tiny/clipped line.
    var wrapped = wrapText(spec.quote, 36);
    var L = text(comp, wrapped, FONT_LBL, 76, WHITE, 10);
    fitText(L, 1500, comp.duration * 0.7);
    centerBlock(L, comp.duration * 0.7);
    tg(L).property("ADBE Position").setValue([W / 2, H * 0.42]);
    var o = tg(L).property("ADBE Opacity");
    o.setValueAtTime(0.4, 0); o.setValueAtTime(0.62, 100);
    key2(tg(L).property("ADBE Position"), 0.4, [W / 2, H * 0.42 + 30], 0.95, [W / 2, H * 0.42], 80);
    // quote marks framing the phrase (ASCII-safe char codes), warrant-blue
    var q1 = text(comp, String.fromCharCode(8220), FONT_NUM, 150, ACCENT, 0);
    tg(q1).property("ADBE Position").setValue([W * 0.075, H * 0.34]);
    key2(tg(q1).property("ADBE Opacity"), 0.3, 0, 0.8, 55, 70);
    var q2 = text(comp, String.fromCharCode(8221), FONT_NUM, 150, ACCENT, 0);
    tg(q2).property("ADBE Position").setValue([W * 0.925, H * 0.34]);
    key2(tg(q2).property("ADBE Opacity"), 0.4, 0, 0.9, 55, 70);
    accent(comp, H * 0.66, 560);
    var a = text(comp, spec.attribution_display, FONT_LBL, 42, SILVER, 160);
    fitText(a, 1500, comp.duration * 0.8); centerX(a, comp.duration * 0.8);
    revealUp(a, 1.3, W / 2, H * 0.72, 40);
  }
  function buildVote(comp, spec) {
    topLabel(comp, spec, H * 0.19, 46);
    var yc = H * 0.44, gap = W * 0.20;
    var lx = W / 2 - gap, rx = W / 2 + gap;
    // majority on the LEFT (SILVER, larger); dissent on the right (ACCENT).
    var nL = text(comp, spec.left, FONT_NUM, 260, SILVER, 0);
    nL.motionBlur = true;
    tg(nL).property("ADBE Position").setValue([lx, yc]);
    var loo = tg(nL).property("ADBE Opacity");
    loo.setValueAtTime(0.5, 0); loo.setValueAtTime(0.75, 100);
    key2(tg(nL).property("ADBE Scale"), 0.5, [60, 60], 0.9, [100, 100], 78);
    var nR = text(comp, spec.right, FONT_NUM, 220, ACCENT, 0);
    nR.motionBlur = true;
    tg(nR).property("ADBE Position").setValue([rx, yc]);
    var roo = tg(nR).property("ADBE Opacity");
    roo.setValueAtTime(0.75, 0); roo.setValueAtTime(1.0, 100);
    key2(tg(nR).property("ADBE Scale"), 0.75, [60, 60], 1.15, [100, 100], 78);
    var to = text(comp, "TO", FONT_LBL, 48, SILVER, 120);
    tg(to).property("ADBE Position").setValue([W / 2, yc - 10]);
    key2(tg(to).property("ADBE Opacity"), 0.95, 0, 1.35, 70, 70);
    // 9 pips: 5 silver (majority) then 4 accent (dissent)
    var pn = 9, pd = 40, pgap = 56, tot = (pn - 1) * pgap, y2 = H * 0.63;
    for (var i = 0; i < pn; i++) {
      var px = W / 2 - tot / 2 + i * pgap;
      var maj = (i < 5);
      var p = circle(comp, "pip_" + i, px, y2, pd, maj ? SILVER : ACCENT, maj ? 90 : 100, false);
      p.motionBlur = true;
      var tt = 1.2 + i * 0.09;
      key2(tg(p).property("ADBE Scale"), tt, [0, 0], tt + 0.30, [100, 100], 80);
      key2(tg(p).property("ADBE Opacity"), tt, 0, tt + 0.30, maj ? 90 : 100, 70);
    }
    bottomLabel(comp, spec, 2.1, H * 0.75, 48);
  }
  function buildCompare(comp, spec) {
    topLabel(comp, spec, H * 0.20, 44);
    var yc = H * 0.45, gap = W * 0.19;
    var lx = W / 2 - gap, rx = W / 2 + gap;
    var nL = text(comp, spec.left, FONT_NUM, 240, WHITE, 0);
    nL.motionBlur = true;
    tg(nL).property("ADBE Position").setValue([lx, yc]);
    var loo = tg(nL).property("ADBE Opacity");
    loo.setValueAtTime(0.5, 0); loo.setValueAtTime(0.75, 100);
    key2(tg(nL).property("ADBE Scale"), 0.5, [62, 62], 0.9, [100, 100], 78);
    var nR = text(comp, spec.right, FONT_NUM, 240, ACCENT, 0);
    nR.motionBlur = true;
    tg(nR).property("ADBE Position").setValue([rx, yc]);
    var roo = tg(nR).property("ADBE Opacity");
    roo.setValueAtTime(0.7, 0); roo.setValueAtTime(0.95, 100);
    key2(tg(nR).property("ADBE Scale"), 0.7, [62, 62], 1.1, [100, 100], 78);
    var dash = text(comp, "-", FONT_NUM, 150, SILVER, 0);
    tg(dash).property("ADBE Position").setValue([W / 2, yc - 6]);
    key2(tg(dash).property("ADBE Opacity"), 0.9, 0, 1.3, 80, 70);
    // RED "REJECTED" stamp, slightly rotated, scale-in
    var rj = text(comp, spec.strike, FONT_NUM, 92, RED, 20);
    fitText(rj, 1200, comp.duration * 0.8); centerX(rj, comp.duration * 0.8);
    rj.motionBlur = true;
    tg(rj).property("ADBE Rotate Z").setValue(-8);
    tg(rj).property("ADBE Position").setValue([W / 2, H * 0.635]);
    var ro = tg(rj).property("ADBE Opacity");
    ro.setValueAtTime(1.5, 0); ro.setValueAtTime(1.75, 100);
    key2(tg(rj).property("ADBE Scale"), 1.5, [150, 150], 1.9, [100, 100], 82);
    bottomLabel(comp, spec, 2.15, H * 0.75, 46);
  }

  function build(spec) {
    var comp = proj.items.addComp("CLEVELAND_" + spec.id, W, H, 1.0, spec.dur, FPS);
    comp.motionBlur = true;
    rect(comp, "bg", W, H, INK, 100, W / 2, H / 2);
    if (spec.still) {
      addStill(comp, spec, 50);
      polish(comp, spec);
      scrim(comp, 46);
    } else {
      vectorBed(comp);
    }
    if (spec.layout === "ACT_TITLE_CARD") buildActTitle(comp, spec);
    else if (spec.layout === "CENTER_STACK" || spec.layout === "MONEY_STACK") buildCenter(comp, spec);
    else if (spec.layout === "QUOTE_CARD") buildQuote(comp, spec);
    else if (spec.layout === "VOTE_SPLIT") buildVote(comp, spec);
    else if (spec.layout === "SPLIT_COMPARE") buildCompare(comp, spec);
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
    args = ap.parse_args()
    raise SystemExit(build(args.dryrun))

