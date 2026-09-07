#!/usr/bin/env python
"""EP44 Tekoh AE hero-card JSX generator.

The generated JSX is intentionally simple and deterministic. It produces the
8-card deck and burns an AI disclosure layer onto every full-frame card.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EP = "PD-2026-044-tekoh"
FPS = 30
W, H = 1920, 1080
ACCENT = "#2FA6A0"
DISCLOSURE = "AI-assisted visualization"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def workdir() -> Path:
    return ROOT / "episodes" / EP / "08_edit" / "ae_hero"


def manifest_stills() -> dict[str, str]:
    cands = [
        ROOT / "episodes" / EP / "05_visuals" / "asset_manifest.v001.json",
    ]
    for path in cands:
        if path.exists():
            data = load(path)
            return {str(x.get("scene_id")): str(x.get("path")) for x in data.get("stills") or [] if x.get("path")}
    return {}


def intervals(film: dict) -> list[tuple[float, float]]:
    return [(float(f["start"]) - 1.0, float(f["end"]) + 1.0) for f in film.get("figures") or []]


def clear_slot(start: float, dur: float, blocked: list[tuple[float, float]], total: float) -> bool:
    end = start + dur
    if start < 21.0 or end > total - 9.0:
        return False
    return all(max(start, a) >= min(end, b) for a, b in blocked)


def choose_slots(total: float, blocked: list[tuple[float, float]], count: int) -> list[float]:
    slots: list[float] = []
    candidates = [190, 228, 266, 356, 402, 448, 505, 570, 635]
    for c in candidates:
        if len(slots) == count:
            break
        s = float(c)
        while s < total - 20:
            occupied = blocked + [(x - 0.5, x + 7.5) for x in slots]
            if clear_slot(s, 6.5, occupied, total):
                slots.append(round(s, 3))
                break
            s += 3.0
    if len(slots) < count:
        raise SystemExit(f"could not place {count} AE slots without figure overlap")
    return sorted(slots[:count])


def deck(stills: dict[str, str], slots: list[float], render: Path) -> list[dict]:
    rows = [
        ("a01", "CENTER_STACK", "ACQUITTED", "A JURY HEARD IT ALL AND LET HIM GO", "", None, "S24", 6.5, None),
        ("s01", "CENTER_STACK", "SECTION 1983", "SUE A STATE OFFICIAL FOR A CONSTITUTIONAL WRONG", "", 1983, "S31", 6.5, None),
        ("t01", "CENTER_STACK", "2 TRIALS", "TWICE TRIED - TWICE FOR THE DEPUTY", "", 2, "S33", 6.5, None),
        ("d01", "DATE_STAMP", "2022", "SUPREME COURT OF THE UNITED STATES", "", 2022, "S36", 5.5, None),
        ("m01", "SPLIT_COMPARE", "MIRANDA STANDS / DICKERSON STANDS", "1966 - 2000 - STILL GOOD LAW", "", None, "S38", 6.5, None),
        ("f01", "CENTER_STACK", "A FENCE, NOT THE GROUND", "THE WARNING GUARDS THE RIGHT - IT IS NOT THE RIGHT", "", None, "S45", 6.5, None),
        ("v01", "VOTE_SPLIT", "6-3", "ONE DOOR CLOSED - EXCLUSION STAYS OPEN", "", 6, "S44", 6.5, None),
        ("q01", "QUOTE_CARD", "Today, the Court strips individuals of the ability to seek a remedy for violations of the right recognized in Miranda.", "JUSTICE KAGAN, IN DISSENT", "", None, "S65", 7.0, "Justice Kagan, dissenting"),
    ]
    beats = []
    for i, row in enumerate(rows):
        bid, layout, hero, bottom, caption, value, scene, dur, attribution = row
        start = slots[i]
        beats.append({
            "id": bid,
            "layout": layout,
            "start": start,
            "end": round(start + dur, 3),
            "dur": dur,
            "still": stills.get(scene),
            "hero": hero,
            "top": "PRIME DOCUMENTARY",
            "bottom": bottom,
            "caption": caption,
            "value": value,
            "required": True,
            "blend_mode": "overlay",
            "attribution": attribution,
            "out": str((render / f"{bid}.mp4")).replace("\\", "/"),
        })
    return beats


JSX = r"""// AUTO-GENERATED - EP44 Tekoh AE hero cards.
(function () {
  var W = __W__, H = __H__, FPS = __FPS__;
  var BEATS = __BEATS__;
  var RENDER_DIR = "__RENDER__";
  var ACCENT = [0.184, 0.651, 0.627];
  var WHITE = [0.961, 0.969, 0.980];
  var SILVER = [0.784, 0.804, 0.839];
  var INK = [0.039, 0.039, 0.047];
  function fail(msg) {
    try { var f = new File(RENDER_DIR + "/_error.txt"); f.open("w"); f.write(String(msg)); f.close(); } catch (e) {}
    try { app.quit(); } catch (e) {}
  }
  try {
    var proj = app.project;
    try { proj.gpuAccelType = GpuAccelType.SOFTWARE; } catch (e) {}
    app.beginUndoGroup("tekoh_hero");
    var rq = proj.renderQueue;
    while (rq.numItems > 0) rq.item(1).remove();
    function tg(L) { return L.property("ADBE Transform Group"); }
    function span(L, dur) { L.inPoint = 0; L.outPoint = dur; return L; }
    function solid(comp, name, w, h, color, op, x, y) {
      var L = span(comp.layers.addSolid(color, name, w, h, 1.0), comp.duration);
      tg(L).property("ADBE Position").setValue([x, y]);
      tg(L).property("ADBE Opacity").setValue(op);
      return L;
    }
    function text(comp, value, size, color, x, y) {
      var L = span(comp.layers.addText(String(value)), comp.duration);
      var p = L.property("ADBE Text Properties").property("ADBE Text Document");
      var d = p.value;
      d.resetCharStyle(); d.fontSize = size; d.fillColor = color; d.applyFill = true;
      d.justification = ParagraphJustification.CENTER_JUSTIFY; p.setValue(d);
      tg(L).property("ADBE Position").setValue([x, y]);
      L.motionBlur = true;
      return L;
    }
    // ---- MEASURED text fitting (sourceRectAtTime -> real glyph box) ----------
    // ported from build_caniglia_hero_cards.py: measure the real rendered width
    // and scale the font DOWN until it fits, so no hero string ever clips.
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
    // center the whole (possibly multi-line) glyph box on the layer's position
    function centerBlock(L, t) {
      var r = srect(L, t);
      var ap = tg(L).property("ADBE Anchor Point").value;
      tg(L).property("ADBE Anchor Point").setValue([r.left + r.width / 2, r.top + r.height / 2]);
      return r;
    }
    // greedy word-wrap into "\r"-separated lines (AE paragraph break) so a long
    // quote renders as clean multi-line text instead of one clipped/tiny line.
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
    function build(spec) {
      var comp = proj.items.addComp("TEKOH_" + spec.id, W, H, 1.0, spec.dur, FPS);
      comp.motionBlur = true;
      solid(comp, "bg", W, H, INK, 100, W / 2, H / 2);
      if (spec.still) {
        var item = proj.importFile(new ImportOptions(new File(spec.still)));
        try { item.mainSource.conformFrameRate = FPS; } catch (e) {}
        var S = span(comp.layers.add(item), spec.dur);
        var fill = Math.max(W / item.width, H / item.height) * 100;
        tg(S).property("ADBE Anchor Point").setValue([item.width / 2, item.height / 2]);
        tg(S).property("ADBE Position").setValue([W / 2, H / 2]);
        tg(S).property("ADBE Scale").setValue([fill * 1.07, fill * 1.07]);
        tg(S).property("ADBE Opacity").setValue(52);
      }
      solid(comp, "scrim", W, H, [0, 0, 0], 48, W / 2, H / 2);
      var isQuote = (spec.layout === "QUOTE_CARD");
      // accent rule: drop it below a (taller) wrapped quote so it never crosses
      // the text like a strikethrough; keep it snug under a single hero line.
      solid(comp, "accent", 560, 8, ACCENT, 100, W / 2, isQuote ? H * 0.66 : H * 0.62);
      // MAXW = 90% of the frame (1728 of 1920) -- nothing may exceed this box.
      var MAXW = Math.round(W * 0.90);
      var topL = text(comp, spec.top || "", 38, SILVER, W / 2, H * 0.18);
      fitText(topL, MAXW, comp.duration * 0.5); centerBlock(topL, comp.duration * 0.5);
      // QUOTE_CARD: wrap the long quote to multiple lines at a readable size;
      // every other card: single hero line, MEASURED and scaled down to fit MAXW.
      var heroStr = spec.hero || "";
      var heroSize;
      if (isQuote) { heroStr = wrapText(heroStr, 34); heroSize = 84; }
      else { heroSize = (spec.hero.length > 24) ? 96 : 140; }
      var heroY = isQuote ? H * 0.43 : H * 0.46;
      var heroL = text(comp, heroStr, heroSize, WHITE, W / 2, heroY);
      fitText(heroL, isQuote ? 1500 : MAXW, comp.duration * 0.6);
      centerBlock(heroL, comp.duration * 0.6);
      tg(heroL).property("ADBE Position").setValue([W / 2, heroY]);
      var botL = text(comp, spec.bottom || "", 42, SILVER, W / 2, H * 0.72);
      fitText(botL, MAXW, comp.duration * 0.6); centerBlock(botL, comp.duration * 0.6);
      tg(botL).property("ADBE Position").setValue([W / 2, H * 0.72]);
      text(comp, "AI-assisted visualization", 20, SILVER, W - 190, H - 32);
      return comp;
    }
    for (var i = 0; i < BEATS.length; i++) {
      var comp = build(BEATS[i]);
      var it = rq.items.add(comp);
      try { it.applyTemplate("最良設定"); } catch (e) { try { it.applyTemplate("Best Settings"); } catch (e2) {} }
      var om = it.outputModule(1);
      try { om.applyTemplate("H.264 - レンダリング設定を一致 - 15 Mbps"); } catch (e3) { try { om.applyTemplate("H.264 - Match Render Settings - 15 Mbps"); } catch (e4) {} }
      om.file = new File(BEATS[i].out);
    }
    app.project.save(new File("__AEP__"));
    app.endUndoGroup();
    rq.render();
    var ok = new File(RENDER_DIR + "/_build_ok.txt"); ok.open("w"); ok.write("queue=" + rq.numItems); ok.close();
    try { app.quit(); } catch (e5) {}
  } catch (err) {
    fail(String(err) + " line=" + String(err.line || ""));
  }
})();
"""


def main() -> int:
    wd = workdir()
    render = wd / "render"
    wd.mkdir(parents=True, exist_ok=True)
    render.mkdir(parents=True, exist_ok=True)
    for marker in [render / "_build_ok.txt", render / "_error.txt"]:
        marker.unlink(missing_ok=True)
    film_path = ROOT / "remotion" / "src" / "data" / "tekoh_film.json"
    if film_path.exists():
        film = load(film_path)
        total = float(film.get("narrationSeconds") or 720.9)
        slots = choose_slots(total, intervals(film), 8)
    else:
        slots = [55, 95, 150, 230, 330, 410, 555, 640]
    beats = deck(manifest_stills(), slots, render)
    doc = {"schema_version": "tekoh_ae_beats.v1", "episode_id": EP, "fps": FPS, "width": W, "height": H, "beats": beats}
    (wd / "beats.json").write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")
    jsx = JSX.replace("__W__", str(W)).replace("__H__", str(H)).replace("__FPS__", str(FPS))
    jsx = jsx.replace("__BEATS__", json.dumps(beats, ensure_ascii=False))
    jsx = jsx.replace("__RENDER__", str(render).replace("\\", "/"))
    jsx = jsx.replace("__AEP__", str((wd / "tekoh_hero.aep")).replace("\\", "/"))
    (wd / "tekoh_hero.jsx").write_text(jsx, encoding="utf-8-sig")
    print(f"wrote {wd / 'beats.json'} cards={len(beats)}")
    print(f"wrote {wd / 'tekoh_hero.jsx'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

