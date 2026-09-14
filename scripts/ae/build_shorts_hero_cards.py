#!/usr/bin/env python
"""VERTICAL (1080x1920) AE hero-card builder for PD YouTube SHORTS.

Cloned in structure from scripts/ae/build_cleveland_hero_cards.py (the audited
AE-2026-JP pipeline) but adapted for punchy PORTRAIT short beats:

  * comp size 1080x1920 @ 30fps (Shorts vertical) -- NOT the 1920x1080 film.
  * three PUNCHY layouts only, huge mobile-legible type, measured-fit (never
    clipped): VOTE (8-1 / 5-3 tally), STATEMENT (big stat / key phrase), and the
    VERDICT reveal (a statement with the hero in the lane accent).
  * 1-3 short beats per short, each ~3s -- a 55-60s vertical short, so the beats
    are brief full-frame takeovers that dip in/out and hand back to the footage.
  * ACCENT is an RGB tuple PER SHORT (glover patrol-steel #5B8DB8 /
    strieff plum #9C6BAA).

Two-step aerender (machine traps honoured, same as the film pipeline):
  1. AfterFX.com -noui -r <jsx>  builds the comps, queues them with H.264 output
     modules and SAVES the .aep. app.newProject() is never called (hangs
     headless); runtime font resolve with unwrap()+HARD FAIL; per-layer
     motionBlur; explicit inPoint/outPoint; SOFTWARE gpu; localized RS/OM
     template names first; ASCII-only labels; completion marker file; app.quit().
  2. assert .aep mtime > .jsx mtime (stale-aep guard), THEN a SEPARATE
     `aerender -project <aep>` renders the whole queue.

OUTPUT goes to a REPO path on C: (remotion/out/ae_shorts/<short>/render). AE's
H.264 output module silently writes 0 mp4s to the H: (exFAT) drive.

CONCURRENCY: another agent (EP50) may be running AfterFX. Before EACH AfterFX /
aerender launch we poll `tasklist` for afterfx/aerender and WAIT until clear --
never two AfterFX instances at once.

Usage:
  python scripts/ae/build_shorts_hero_cards.py --short short50            # gen + render
  python scripts/ae/build_shorts_hero_cards.py --short short51 --dryrun   # gen jsx only
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(r"C:\Users\aab15\Documents\prime-documentary")
AEDIR = Path(r"C:\Program Files\Adobe\Adobe After Effects 2026\Support Files")
AFX = AEDIR / "AfterFX.com"
AERENDER = AEDIR / "aerender.exe"

FPS = 30
W, H = 1080, 1920            # VERTICAL short

# shared palette (0..1 float)
WHITE = [0.961, 0.969, 0.980]    # #F5F7FA
SILVER = [0.784, 0.804, 0.839]   # #C8CDD6 labels / majority
INK = [0.039, 0.039, 0.047]      # #0A0A0C root

# advance-width factors (Anton / Oswald) -- starting estimate; JSX re-fits with
# sourceRectAtTime (measured, never clipped).
ANTON_ADV = 0.470
OSWALD_ADV = 0.505


def hexrgb(h: str) -> list[float]:
    h = h.lstrip("#")
    return [int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]


# --------------------------------------------------------------- the two decks
# start/end are ABSOLUTE seconds in the finished short render (shorts have NO
# bookend offset -- the timeline starts at 0). Windows sit ON TOP of the
# existing footage over the relevant narration line; the overlay adds NO
# duration, so runtime is unchanged.
SHORTS = {
    "short50": dict(  # Kansas v. Glover -- 8-1 UPHELD, reasonable suspicion.
        episode="PD-2026-048-glover",
        accent_hex="#5B8DB8",
        base_dur=55.533,
        forbidden=["unconstitutional", "struck down", "illegal stop",
                   "probable cause proof"],
        deck=[
            dict(id="g1", layout="STATEMENT", start=23.4, dur=2.9,
                 top="THE STANDARD", hero="REASONABLE SUSPICION",
                 hero_color="white",
                 sub="NOT PROOF. NOT PROBABLE CAUSE. JUST SPECIFIC FACTS."),
            dict(id="g2", layout="VOTE", start=32.7, dur=3.2,
                 case="KANSAS v. GLOVER  2020",
                 left="8", right="1", majority=8, dissent=1,
                 verdict="STOP UPHELD",
                 sub="REASONABLE SUSPICION, NOT PROBABLE CAUSE"),
            dict(id="g3", layout="STATEMENT", start=41.3, dur=2.9,
                 top="BUT IT IS NARROW", hero="IT DISSOLVES",
                 hero_color="accent",
                 sub="THE MOMENT POLICE SEE THE DRIVER IS NOT THE OWNER."),
        ],
    ),
    "short51": dict(  # Utah v. Strieff -- 5-3, illegal stop, evidence via attenuation.
        episode="PD-2026-049-strieff",
        accent_hex="#9C6BAA",
        base_dur=59.267,
        forbidden=["we are all harmed", "abolished", "was legal",
                   "a legal stop", "stop was legal"],
        deck=[
            dict(id="s1", layout="STATEMENT", start=13.0, dur=3.0,
                 top="THE RULE", hero="THE EXCLUSIONARY RULE",
                 hero_color="white",
                 sub="EVIDENCE FROM AN ILLEGAL SEARCH IS NORMALLY THROWN OUT."),
            dict(id="s2", layout="VOTE", start=37.2, dur=3.2,
                 case="UTAH v. STRIEFF  2016",
                 left="5", right="3", majority=5, dissent=3,
                 verdict="EVIDENCE STAYS",
                 sub="THE STOP WAS STILL ILLEGAL - ATTENUATION"),
            dict(id="s3", layout="STATEMENT", start=52.3, dur=2.9,
                 top="THE BOTTOM LINE", hero="NEVER LEGAL",
                 hero_color="accent",
                 sub="A WARRANT JUST MADE THE ILLEGAL STOP PAY OFF."),
        ],
    ),
}


def build(short_id: str, dryrun: bool) -> tuple[int, dict]:
    cfg = SHORTS[short_id]
    accent = hexrgb(cfg["accent_hex"])

    work = ROOT / "remotion" / "out" / "ae_shorts" / (
        f"{short_id}_dryrun" if dryrun else short_id)
    render = work / "render"
    render.mkdir(parents=True, exist_ok=True)
    for m in ("_build_ok.txt", "_error.txt"):
        (render / m).unlink(missing_ok=True)

    beats = []
    placed = []
    for c in cfg["deck"]:
        start = float(c["start"])
        end = round(start + float(c["dur"]), 3)
        if end > cfg["base_dur"]:
            print(f"FAIL {c['id']} end {end} past base {cfg['base_dur']}", file=sys.stderr)
            return 2, {}
        for a, b in placed:
            if start < b and a < end:
                print(f"FAIL {c['id']} overlaps a placed beat", file=sys.stderr)
                return 2, {}
        placed.append((start, end))

        b = dict(id=c["id"], layout=c["layout"], start=start, end=end,
                 dur=float(c["dur"]),
                 out=str(render / f"{c['id']}.mp4").replace("\\", "/"))
        if c["layout"] == "VOTE":
            b.update(case=c["case"], left=c["left"], right=c["right"],
                     majority=int(c["majority"]), dissent=int(c["dissent"]),
                     verdict=c["verdict"], sub=c.get("sub", ""),
                     hero=f"{c['left']} TO {c['right']} {c['verdict']}")
        else:  # STATEMENT
            b.update(top=c.get("top", ""), hero=c["hero"],
                     hero_color=c.get("hero_color", "white"),
                     sub=c.get("sub", ""))

        blob = " ".join(str(x) for x in (
            b.get("case"), b.get("verdict"), b.get("top"),
            b.get("hero"), b.get("sub")) if x).lower()
        for bad in cfg["forbidden"]:
            if bad in blob:
                print(f"FAIL forbidden string '{bad}' on {c['id']}", file=sys.stderr)
                return 3, {}
        beats.append(b)

    doc = {
        "schema_version": "shorts_ae_beats.v1",
        "short_id": short_id, "episode_id": cfg["episode"],
        "fps": FPS, "width": W, "height": H,
        "timebase": "absolute_short_seconds",
        "accent": cfg["accent_hex"], "base_dur": cfg["base_dur"],
        "render_dir": str(render).replace("\\", "/"),
        "aep": str(work / f"{short_id}_hero.aep").replace("\\", "/"),
        "jsx": str(work / f"{short_id}_hero.jsx").replace("\\", "/"),
        "beats": beats,
    }
    (work / "beats.json").write_text(json.dumps(doc, ensure_ascii=False, indent=2),
                                     encoding="utf-8")

    jsx = JSX
    jsx = jsx.replace("__W__", str(W)).replace("__H__", str(H)).replace("__FPS__", str(FPS))
    jsx = jsx.replace("__ACCENT__", ",".join(str(v) for v in accent))
    jsx = jsx.replace("__WHITE__", ",".join(str(v) for v in WHITE))
    jsx = jsx.replace("__SILVER__", ",".join(str(v) for v in SILVER))
    jsx = jsx.replace("__INK__", ",".join(str(v) for v in INK))
    jsx = jsx.replace("__BEATS__", json.dumps(beats, ensure_ascii=False))
    jsx = jsx.replace("__RENDER__", str(render).replace("\\", "/"))
    jsx = jsx.replace("__AEP__", str(work / f"{short_id}_hero.aep").replace("\\", "/"))
    (work / f"{short_id}_hero.jsx").write_text(jsx, encoding="utf-8-sig")

    print(f"[gen] {short_id}: {len(beats)} beats  accent={cfg['accent_hex']}  dryrun={dryrun}")
    for b in beats:
        print(f"  {b['id']:<3} {b['layout']:<10} {b['start']:>6.1f}-{b['end']:<6.1f}  {b['hero']}")
    print("[gen] jsx  ->", work / f"{short_id}_hero.jsx")
    return 0, doc


# --------------------------------------------------------------- AE launch/render
def ae_clear(wait: bool = True) -> None:
    """Block until no AfterFX/aerender is running (EP50 concurrency guard)."""
    waited = 0
    while True:
        r = subprocess.run(["tasklist"], capture_output=True, text=True)
        busy = [ln for ln in r.stdout.splitlines()
                if "afterfx" in ln.lower() or "aerender" in ln.lower()]
        if not busy:
            if waited:
                print(f"[ae] concurrency clear after {waited}s")
            return
        if not wait:
            return
        if waited == 0:
            print("[ae] AfterFX/aerender already running -- WAITING for it to clear ...")
        time.sleep(5)
        waited += 5


def run_ae(doc: dict) -> int:
    work = Path(doc["jsx"]).parent
    jsx = Path(doc["jsx"])
    aep = Path(doc["aep"])
    render = Path(doc["render_dir"])
    ok = render / "_build_ok.txt"
    err = render / "_error.txt"
    aep.unlink(missing_ok=True)

    # ---- step 1: build+save the .aep (guard concurrency first) --------------
    ae_clear()
    print("[ae] build:", jsx)
    subprocess.run([str(AFX), "-noui", "-r", str(jsx)], capture_output=True, text=True)
    for _ in range(150):  # up to ~5 min
        if ok.exists() or err.exists():
            break
        time.sleep(2)
    if err.exists():
        print("[ae] BUILD ERROR:", err.read_text(encoding="utf-8", errors="replace"))
        return 4
    if not ok.exists():
        print("[ae] BUILD TIMEOUT -- no _build_ok.txt")
        return 4
    print("[ae] build ok:", ok.read_text(encoding="utf-8", errors="replace").strip())

    # ---- stale-aep guard ----------------------------------------------------
    if not aep.exists():
        print("[ae] NO AEP saved -> abort")
        return 5
    if aep.stat().st_mtime <= jsx.stat().st_mtime:
        print(f"[ae] STALE AEP (mtime {aep.stat().st_mtime} <= jsx {jsx.stat().st_mtime}) -> abort")
        return 5

    # ---- step 2: separate aerender of the whole queue -----------------------
    ae_clear()
    print("[ae] aerender:", aep)
    r = subprocess.run([str(AERENDER), "-project", str(aep)],
                       capture_output=True, text=True)
    tail = (r.stdout or "")[-1500:] + (r.stderr or "")[-1500:]
    print(tail)

    made = sorted(render.glob("*.mp4"))
    print(f"[ae] rendered {len(made)} mp4(s):")
    for m in made:
        print(f"   {m.name}  {m.stat().st_size/1e6:.2f} MB")
    want = {b["id"] for b in doc["beats"]}
    got = {m.stem for m in made}
    missing = want - got
    if missing:
        print("[ae] MISSING renders:", missing)
        return 6
    return 0


JSX = r"""// AUTO-GENERATED - PD SHORTS vertical AE hero cards. Do not hand-edit.
(function () {
  var W = __W__, H = __H__, FPS = __FPS__;
  var ACCENT = [__ACCENT__], WHITE = [__WHITE__], SILVER = [__SILVER__], INK = [__INK__];
  var BEATS = __BEATS__;
  var RENDER_DIR = "__RENDER__";
  var MARGIN = 60, MAXW = W - 2 * MARGIN;   // 960 usable

  function fail(msg) {
    try { var f = new File(RENDER_DIR + "/_error.txt"); f.open("w"); f.write(String(msg)); f.close(); } catch (e) {}
    try { app.quit(); } catch (e) {}
  }

  try {
  var proj = app.project;                 // -noui -r opens a fresh untitled project
  try { for (var ri = proj.numItems; ri >= 1; ri--) {
    var itx = proj.item(ri);
    if (itx instanceof CompItem && String(itx.name).indexOf("SHORT_") === 0) itx.remove();
  } } catch (e) {}
  try { proj.gpuAccelType = GpuAccelType.SOFTWARE; } catch (e) {}
  try { proj.bitsPerChannel = 8; } catch (e) {}
  app.beginUndoGroup("shorts_hero");

  // ---- runtime font resolver (missing font = HARD FAIL, no silent substitute)
  var FONT_LOG = "";
  function unwrap(x) {
    try { if (x && x.postScriptName) return x; } catch (e) {}
    try { if (x && x.length && x[0] && x[0].postScriptName) return x[0]; } catch (e2) {}
    return null;
  }
  function psName(fam, styles) {
    var got = null;
    for (var s = 0; s < styles.length && !got; s++) {
      try { var m = app.fonts.getFontsByFamilyNameAndStyleName(fam, styles[s]);
            got = unwrap(m && m.length ? m[0] : m); } catch (e) {}
    }
    if (!got) { try { var all = app.fonts.allFonts;
      for (var i = 0; i < all.length && !got; i++) { var f = unwrap(all[i]);
        if (f && String(f.familyName).toLowerCase() === fam.toLowerCase()) got = f; } } catch (e3) {} }
    if (!got) throw new Error("FONT NOT FOUND: " + fam + " -- refusing to substitute");
    FONT_LOG += fam + "=" + got.postScriptName + " ";
    return got.postScriptName;
  }
  var FONT_NUM = psName("Anton", ["Regular"]);
  var FONT_LBL = psName("Oswald", ["Medium", "Regular", "SemiBold", "Book"]);

  // ---- helpers ------------------------------------------------------------
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
  function srect(L, t) { return L.sourceRectAtTime(t === undefined ? 0 : t, false); }
  function setFontSize(L, sz) {
    var tp = L.property("ADBE Text Properties").property("ADBE Text Document");
    var d = tp.value; d.fontSize = sz; tp.setValue(d);
  }
  function fitText(L, maxW, t) {
    var r = srect(L, t), guard = 0;
    while (r.width > maxW && guard < 28) {
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
    var words = String(str).split(" "), lines = [], cur = "";
    for (var i = 0; i < words.length; i++) {
      var w = words[i];
      if (cur.length === 0) cur = w;
      else if ((cur.length + 1 + w.length) <= maxChars) cur += " " + w;
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
  function ellipseMask(L, size, sub) {
    var m = L.property("ADBE Mask Parade").addProperty("ADBE Mask Atom");
    var s = new Shape(), r = size / 2, k = 0.5523;
    var cx = L.source.width / 2, cy = L.source.height / 2;
    s.vertices = [[cx, cy - r], [cx + r, cy], [cx, cy + r], [cx - r, cy]];
    s.inTangents = [[-r * k, 0], [0, -r * k], [r * k, 0], [0, r * k]];
    s.outTangents = [[r * k, 0], [0, r * k], [-r * k, 0], [0, -r * k]];
    s.closed = true;
    m.property("ADBE Mask Shape").setValue(s);
    if (sub) m.maskMode = MaskMode.SUBTRACT;
    return m;
  }
  function circle(comp, name, x, y, d, color, op) {
    var L = rect(comp, name, d, d, color, op, x, y);
    ellipseMask(L, d, false);
    return L;
  }

  // ---- background bed (near-black, lane-accent glow + vignette) ------------
  function vignette(comp) {
    var v = rect(comp, "vignette", W, H, [0, 0, 0], 78, W / 2, H / 2);
    var m = v.property("ADBE Mask Parade").addProperty("ADBE Mask Atom");
    var s = new Shape(), rx = W * 0.70, ry = H * 0.62, cx = W / 2, cy = H / 2, k = 0.5523;
    s.vertices = [[cx, cy - ry], [cx + rx, cy], [cx, cy + ry], [cx - rx, cy]];
    s.inTangents = [[-rx * k, 0], [0, -ry * k], [rx * k, 0], [0, ry * k]];
    s.outTangents = [[rx * k, 0], [0, ry * k], [-rx * k, 0], [0, -ry * k]];
    s.closed = true;
    m.property("ADBE Mask Shape").setValue(s);
    m.maskMode = MaskMode.SUBTRACT;
    m.property("ADBE Mask Feather").setValue([300, 300]);
  }
  function bed(comp) {
    // lane-accent radial glow low-centre so the card reads as the graded film
    var glow = rect(comp, "glow", W, H, [0, 0, 0], 0, W / 2, H / 2);
    var gr = glow.property("ADBE Effect Parade").addProperty("ADBE Ramp");
    gr.property("ADBE Ramp-0001").setValue([W / 2, H * 0.62]);
    gr.property("ADBE Ramp-0002").setValue(ACCENT);
    gr.property("ADBE Ramp-0003").setValue([W / 2, H * 0.05]);
    gr.property("ADBE Ramp-0004").setValue([0, 0, 0]);
    gr.property("ADBE Ramp-0005").setValue(2);
    glow.blendingMode = BlendingMode.ADD;
    var go = tg(glow).property("ADBE Opacity");
    go.setValueAtTime(0, 0); go.setValueAtTime(0.6, 22); go.setValueAtTime(comp.duration, 15); ease(go, 60);
    vignette(comp);
    // a light-sweep across the upper third for premium sheen
    var sweep = rect(comp, "sweep", 360, H * 0.9, [1, 1, 1], 0, -400, H * 0.33);
    sweep.blendingMode = BlendingMode.ADD; sweep.motionBlur = true;
    tg(sweep).property("ADBE Rotate Z").setValue(16);
    key2(tg(sweep).property("ADBE Position"), 0.45, [-400, H * 0.33], 1.15, [W + 400, H * 0.33], 45);
    var so = tg(sweep).property("ADBE Opacity");
    so.setValueAtTime(0.45, 0); so.setValueAtTime(0.68, 10); so.setValueAtTime(1.15, 0);
  }
  function dip(comp) {
    var d = rect(comp, "dip", W, H, [0, 0, 0], 0, W / 2, H / 2);
    var head = 4 / FPS, tail = 4 / FPS;
    var o = tg(d).property("ADBE Opacity");
    o.setValueAtTime(0, 100); o.setValueAtTime(head, 0);
    o.setValueAtTime(comp.duration - tail, 0); o.setValueAtTime(comp.duration, 100);
    ease(o, 40);
  }
  function accentBar(comp, y, w, t0) {
    var L = rect(comp, "accent", w || 420, 8, ACCENT, 96, W / 2, y);
    wipeIn(L, t0 || 0.55, (t0 || 0.55) + 0.5, W / 2, y);
    tg(L).property("ADBE Opacity").setValue(96);
    return L;
  }
  function topLabel(comp, str, y, size) {
    if (!str || !str.length) return null;
    var L = text(comp, str, FONT_LBL, size || 52, SILVER, 320);
    fitText(L, MAXW - 40, comp.duration * 0.5); centerX(L, comp.duration * 0.5);
    revealUp(L, 0.2, W / 2, y, 44);
    return L;
  }
  function subLabel(comp, str, t0, y, size) {
    if (!str || !str.length) return null;
    var wrapped = wrapText(str, 30);
    var L = text(comp, wrapped, FONT_LBL, size || 52, WHITE, 40);
    fitText(L, MAXW, comp.duration * 0.85); centerBlock(L, comp.duration * 0.85);
    tg(L).property("ADBE Position").setValue([W / 2, y]);
    key2(tg(L).property("ADBE Position"), t0, [W / 2, y + 40], t0 + 0.5, [W / 2, y], 80);
    key2(tg(L).property("ADBE Opacity"), t0, 0, t0 + 0.42, 100, 70);
    return L;
  }

  // ---- STATEMENT layout (big stat / key phrase / verdict) -----------------
  // accent bar + sub are placed relative to the MEASURED hero block bottom, so
  // a 1-, 2- or 3-line hero never collides with the underline or sub.
  function buildStatement(comp, spec) {
    topLabel(comp, spec.top, H * 0.235, 50);
    var col = (spec.hero_color === "accent") ? ACCENT : WHITE;
    var wrapped = wrapText(spec.hero, 13);
    var heroY = H * 0.42;
    var L = text(comp, wrapped, FONT_NUM, 230, col, 2);
    fitText(L, MAXW, comp.duration * 0.85);
    var r = centerBlock(L, comp.duration * 0.85);
    L.motionBlur = true;
    tg(L).property("ADBE Position").setValue([W / 2, heroY]);
    var o = tg(L).property("ADBE Opacity");
    o.setValueAtTime(0.35, 0); o.setValueAtTime(0.55, 100);
    var sc = tg(L).property("ADBE Scale");
    sc.setValueAtTime(0.35, [116, 116]); sc.setValueAtTime(0.9, [100, 100]); ease(sc, 80);
    key2(tg(L).property("ADBE Position"), 0.35, [W / 2, heroY + 40], 0.9, [W / 2, heroY], 80);
    var heroBottom = heroY + r.height / 2;
    var accentY = heroBottom + 72;
    accentBar(comp, accentY, 440, 0.7);
    subLabel(comp, spec.sub, 1.15, accentY + 130, 52);
  }

  // ---- VOTE layout (8-1 / 5-3 tally) --------------------------------------
  function buildVote(comp, spec) {
    // case name
    var cl = text(comp, spec.case, FONT_LBL, 54, SILVER, 200);
    fitText(cl, MAXW, comp.duration * 0.5); centerX(cl, comp.duration * 0.5);
    revealUp(cl, 0.2, W / 2, H * 0.215, 44);
    // the two numbers
    var yc = H * 0.40, gap = W * 0.235;
    var lx = W / 2 - gap, rx = W / 2 + gap;
    var nL = text(comp, spec.left, FONT_NUM, 340, SILVER, 0);
    nL.motionBlur = true; centerBlock(nL, comp.duration * 0.8);
    tg(nL).property("ADBE Position").setValue([lx, yc]);
    var lo = tg(nL).property("ADBE Opacity"); lo.setValueAtTime(0.4, 0); lo.setValueAtTime(0.66, 100);
    key2(tg(nL).property("ADBE Scale"), 0.4, [60, 60], 0.85, [100, 100], 80);
    var nR = text(comp, spec.right, FONT_NUM, 300, ACCENT, 0);
    nR.motionBlur = true; centerBlock(nR, comp.duration * 0.8);
    tg(nR).property("ADBE Position").setValue([rx, yc]);
    var ro = tg(nR).property("ADBE Opacity"); ro.setValueAtTime(0.66, 0); ro.setValueAtTime(0.92, 100);
    key2(tg(nR).property("ADBE Scale"), 0.66, [60, 60], 1.1, [100, 100], 80);
    var to = text(comp, "TO", FONT_LBL, 70, SILVER, 80);
    centerBlock(to, comp.duration * 0.8);
    tg(to).property("ADBE Position").setValue([W / 2, yc]);
    key2(tg(to).property("ADBE Opacity"), 0.85, 0, 1.25, 78, 70);
    // verdict
    var vd = text(comp, spec.verdict, FONT_NUM, 116, ACCENT, 6);
    fitText(vd, MAXW, comp.duration * 0.85); centerX(vd, comp.duration * 0.85);
    vd.motionBlur = true;
    tg(vd).property("ADBE Position").setValue([W / 2, H * 0.545]);
    var vo = tg(vd).property("ADBE Opacity"); vo.setValueAtTime(1.05, 0); vo.setValueAtTime(1.3, 100);
    key2(tg(vd).property("ADBE Scale"), 1.05, [118, 118], 1.5, [100, 100], 82);
    key2(tg(vd).property("ADBE Position"), 1.05, [W / 2, H * 0.545 + 30], 1.5, [W / 2, H * 0.545], 82);
    accentBar(comp, H * 0.615, 460, 0.75);
    // pips: majority SILVER then dissent ACCENT
    var pn = spec.majority + spec.dissent, pd = 46, pgap = 66;
    var tot = (pn - 1) * pgap, y2 = H * 0.70;
    for (var i = 0; i < pn; i++) {
      var px = W / 2 - tot / 2 + i * pgap;
      var maj = (i < spec.majority);
      var p = circle(comp, "pip_" + i, px, y2, pd, maj ? SILVER : ACCENT, maj ? 92 : 100);
      p.motionBlur = true;
      var tt = 1.25 + i * 0.08;
      key2(tg(p).property("ADBE Scale"), tt, [0, 0], tt + 0.3, [100, 100], 80);
      key2(tg(p).property("ADBE Opacity"), tt, 0, tt + 0.3, maj ? 92 : 100, 70);
    }
    subLabel(comp, spec.sub, 1.7, H * 0.775, 46);
  }

  function build(spec) {
    var comp = proj.items.addComp("SHORT_" + spec.id, W, H, 1.0, spec.dur, FPS);
    comp.motionBlur = true;
    rect(comp, "bg", W, H, INK, 100, W / 2, H / 2);
    bed(comp);
    if (spec.layout === "VOTE") buildVote(comp, spec);
    else if (spec.layout === "STATEMENT") buildStatement(comp, spec);
    else throw new Error("unsupported layout " + spec.layout + " on " + spec.id);
    dip(comp);
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
  mk.open("w"); mk.write("comps=" + built + " queue=" + rq.numItems + " fonts: " + FONT_LOG); mk.close();
  try { app.quit(); } catch (e) {}
  } catch (err) {
    fail(String(err) + " line=" + String(err.line || "") + " file=" + String(err.fileName || ""));
  }
})();
"""


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--short", required=True, choices=sorted(SHORTS.keys()))
    ap.add_argument("--dryrun", action="store_true", help="generate jsx only, no AE")
    args = ap.parse_args()
    rc, doc = build(args.short, args.dryrun)
    if rc != 0 or args.dryrun:
        raise SystemExit(rc)
    raise SystemExit(run_ae(doc))
