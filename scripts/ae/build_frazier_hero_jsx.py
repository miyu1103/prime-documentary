"""EP39 frazier - AE hero-beat JSX generator.

Reads episodes/_planning/EP39_frazier_hero_beats.spec.v001.json (LOCKED input:
values, labels, durations and still filenames are all decided there - the stills
were assigned by eyeballing a labelled contact sheet, so NEVER re-derive them
from the S## number) and writes:

  <WORK>/frazier_hero.jsx    - builds one full-frame comp per beat + render queue
  <WORK>/beats.json          - sidecar that drives the compositor

Layout spec: EP39_frazier_DESIGN_and_CODEX_PROMPTS.v001.md 3.1 / 3.3 / 3.6.
Layouts implemented: A_BIG_NUMBER, B_SPLIT_RATIO, D_CITATION_STAMP (the only
ones the spec uses). Any other layout is a hard FAIL rather than a silent
fallback.

Machine traps honoured (3.6): localized RS/OM template names, spatial-aware
setTemporalEaseAtKey dimension, no app.newProject(), per-layer motionBlur,
"ADBE Rotate Z", explicit inPoint+outPoint, conformFrameRate, single-line
captions, all number strings precomputed in Python, completion marker file.
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(r"C:\Users\aab15\Documents\prime-documentary")
SPEC = ROOT / "episodes" / "_planning" / "EP39_frazier_hero_beats.spec.v001.json"
WORK = Path("E:/pd-media/episodes/PD-2026-039-frazier/08_edit/ae_hero")
RENDER = WORK  # final mp4s live directly in ae_hero/ as hb01.mp4 .. hb08.mp4

SUPPORTED_LAYOUTS = {"A_BIG_NUMBER", "B_SPLIT_RATIO", "D_CITATION_STAMP"}


def ease_out_cubic(p: float) -> float:
    return 1.0 - (1.0 - p) ** 3


def fmt_number(val: float, decimals: int, thousands: bool, prefix: str, suffix: str) -> str:
    if decimals > 0:
        s = f"{val:.{decimals}f}"
    else:
        iv = int(round(val))
        s = f"{iv:,}" if thousands else str(iv)
    return f"{prefix}{s}{suffix}"


def count_keys(target: float, decimals: int, thousands: bool, prefix: str, suffix: str,
               t0: float, t1: float, n: int = 18):
    """(time, string) hold-keys counting 0 -> target with ease-out cubic."""
    keys = [(t0, fmt_number(0, decimals, thousands, prefix, suffix))]
    for i in range(1, n):
        p = i / (n - 1)
        v = target * ease_out_cubic(p)
        keys.append((t0 + (t1 - t0) * p, fmt_number(v, decimals, thousands, prefix, suffix)))
    keys.append((t1 + 0.02, fmt_number(target, decimals, thousands, prefix, suffix)))
    return keys


NO_DANGLE_END = {
    "a", "an", "the", "of", "to", "in", "on", "at", "for", "with", "from", "by", "as",
    "and", "or", "but", "nor", "so", "yet", "is", "are", "was", "were", "be", "been",
    "has", "have", "had", "do", "does", "did", "will", "would", "can", "could",
    "my", "your", "his", "her", "its", "our", "their", "that", "this", "these",
    "those", "who", "which", "whose", "if", "when", "because", "while", "after",
    "before", "since", "until", "not", "no", "into", "over", "under", "than",
}


def one_line(text: str, maxchars: int = 72) -> str:
    """One caption line that reads as a COMPLETE thought.

    AE renders a literal \\n, so the card gets a single line -- but the previous version
    hard-cut at maxchars and appended an ellipsis, which produced
    "He had gone in at twenty-five and come out at..." in the look test: it stops on a
    preposition and drops the payoff word. Prefer the longest whole clause that fits;
    only word-cut as a last resort, and never end on a function word.

    maxchars raised 50 -> 72 (2026-07-20): the lower-third bar is full-frame width at
    Oswald 42, which holds ~100 characters. 50 was cutting whole sentences that fit
    comfortably -- the look test showed the payoff word being ellipsed away.
    """
    import re as _re
    t = " ".join(str(text).split())
    if len(t) <= maxchars:
        return t

    # longest complete clause that fits
    best = ""
    for m in _re.finditer(r"[^,;:.!?\u2014]+[,;:.!?\u2014]?", t):
        frag = t[: m.end()].strip().rstrip(",;:\u2014- ")
        if len(frag) <= maxchars and len(frag) > len(best):
            best = frag
    if best and len(best.split()) >= 4:
        return best

    # last resort: word cut that does not dangle on a function word
    words = t[:maxchars].rsplit(" ", 1)[0].split()
    while words and _re.sub(r"[^a-z]", "", words[-1].lower()) in NO_DANGLE_END:
        words.pop()
    return (" ".join(words).rstrip(",;:\u2014- ") + "\u2026") if words else t[:maxchars]


def build_beats(spec: dict):
    fps = spec["fps"]
    still_root = Path(spec["still_root"])
    beats = []
    for b in spec["beats"]:
        if b["layout"] not in SUPPORTED_LAYOUTS:
            print(f"FAIL unsupported layout {b['layout']} on {b['id']}", file=sys.stderr)
            sys.exit(2)
        still = still_root / b["still"]
        if not still.exists():
            print(f"FAIL missing still {still}", file=sys.stderr)
            sys.exit(2)
        dur = float(b["dur"])
        t0, t1 = 0.55, 1.55
        nk = count_keys(b["value"], b.get("decimals", 0), b.get("thousands", False),
                        b.get("prefix", ""), b.get("suffix", ""), t0, t1)
        beats.append(dict(
            id=b["id"],
            slot=b["slot"],
            layout=b["layout"],
            dur=dur,
            start=float(b["design_t"]),
            end=round(float(b["design_t"]) + dur, 3),
            still=str(still).replace("\\", "/"),
            still_note=b.get("still_content_verified", ""),
            top=b["top"],
            top2=b.get("top2"),
            bottom=b["bottom"],
            value2str=fmt_number(b["value2"], b.get("decimals", 0), b.get("thousands", False),
                                 b.get("prefix", ""), b.get("suffix", ""))
            if b.get("value2") is not None else None,
            caption=one_line(b.get("anchor_phrase", "")),
            numKeys=[[round(t, 4), v] for t, v in nk],
            numReveal=round(t0 - 0.10, 4),
            head=round(4.0 / fps, 4), tail=round(4.0 / fps, 4),
            claim=b.get("claim", ""),
            out=str(RENDER / f"{b['id']}.mp4").replace("\\", "/"),
        ))
    return beats


JSX_TEMPLATE = r"""// AUTO-GENERATED - EP39 frazier AE hero beats. Do not hand-edit.
(function () {
    var W = %(W)d, H = %(H)d, FPS = %(FPS)d;
    var GOLD = [%(GOLD)s], WHITE = [%(WHITE)s], SILVER = [%(SILVER)s];
    var BEATS = %(BEATS)s;
    var RENDER_DIR = "%(RENDER)s";

    // NOTE: each `AfterFX -noui -r` launch opens a fresh untitled project.
    // app.newProject() hangs headless on the save prompt -- never call it.
    var proj = app.project;
    try { for (var ri = proj.numItems; ri >= 1; ri--) {
        var itx = proj.item(ri);
        if (itx instanceof CompItem && String(itx.name).indexOf("FRZ_") === 0) itx.remove();
    } } catch (e) {}
    try { proj.gpuAccelType = GpuAccelType.SOFTWARE; } catch (e) {}
    try { proj.bitsPerChannel = 8; } catch (e) {}
    app.beginUndoGroup("frazier_hero");

    // ---- runtime font resolver (a silent substitution is a FAIL) ----
    // MEASURED on AE 2026 (2026-07-20): app.fonts.allFonts[i] is NOT a FontObject,
    // it is an array-LIKE wrapper (props: 0,length) whose [0] is the FontObject.
    // Reading .familyName off it yields undefined -> the EP38 resolver silently
    // fell through to the family name, and TextDocument.font wants the PostScript
    // name ("Anton-Regular"), so the font was substituted with no error.
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
        if (!got) {  // fallback: linear scan of allFonts, unwrapping each entry
            try {
                var all = app.fonts.allFonts;
                for (var i = 0; i < all.length && !got; i++) {
                    var f = unwrap(all[i]);
                    if (f && String(f.familyName).toLowerCase() === fam.toLowerCase()) got = f;
                }
            } catch (e3) {}
        }
        FONT_LOG += fam + "=" + (got ? (got.postScriptName + "/" + got.styleName) : "NOT_FOUND!") + " ";
        return got ? got.postScriptName : fam;
    }
    var FONT_NUM = psName("Anton", ["Regular"]);
    var FONT_LBL = psName("Oswald", ["Medium", "Regular", "SemiBold", "Book"]);

    function ease(prop, inf) {
        inf = inf || 70; var n = prop.numKeys;
        // TRAP: spatial props (Position) take a 1-element temporal ease array.
        var dim = 1;
        if (!prop.isSpatial) { var v0 = prop.value; dim = (v0 instanceof Array) ? v0.length : 1; }
        var a = [], b = [];
        for (var d = 0; d < dim; d++) { a.push(new KeyframeEase(0, inf)); b.push(new KeyframeEase(0, inf)); }
        for (var k = 1; k <= n; k++) {
            try { prop.setInterpolationTypeAtKey(k, KeyframeInterpolationType.BEZIER, KeyframeInterpolationType.BEZIER); } catch (e) {}
            try { prop.setTemporalEaseAtKey(k, a, b); } catch (e2) {}
        }
    }
    function key2(prop, t0, v0, t1, v1, inf) { prop.setValueAtTime(t0, v0); prop.setValueAtTime(t1, v1); ease(prop, inf); }
    function tg(L) { return L.property("ADBE Transform Group"); }
    function span(L, dur) { L.inPoint = 0; L.outPoint = dur; }   // TRAP: set BOTH

    // ---- local scrim band (READABILITY FIX 2026-07-20) ----
    // The elliptical vignette only darkens the FRAME EDGES; a bright subject in
    // the middle of the still (the manila folder in S17 behind hb03, the typed
    // page in S19 behind hb02) sits directly under the silver citation line and
    // eats it. A feathered dark band local to the text row is the fix.
    function scrimBand(comp, dur, cy, halfW, halfH, fx, fy, opac, t0, t1) {
        var sc = comp.layers.addSolid([0.008, 0.014, 0.028], "scrim", W, H, 1.0);
        span(sc, dur);
        var m = sc.property("ADBE Mask Parade").addProperty("ADBE Mask Atom");
        var s = new Shape();
        s.vertices = [[W / 2 - halfW, cy - halfH], [W / 2 + halfW, cy - halfH],
                      [W / 2 + halfW, cy + halfH], [W / 2 - halfW, cy + halfH]];
        s.closed = true;
        m.property("ADBE Mask Shape").setValue(s);
        m.property("ADBE Mask Feather").setValue([fx, fy]);   // 2-value array
        var o = tg(sc).property("ADBE Opacity");
        o.setValueAtTime(t0, 0); o.setValueAtTime(t1, opac); ease(o, 60);
        return sc;
    }
    // soft black halo behind a glyph run - lifts text off ANY background
    function textShadow(L, opac, soft) {
        try {
            var ds = L.property("ADBE Effect Parade").addProperty("ADBE Drop Shadow");
            ds.property("ADBE Drop Shadow-0001").setValue([0, 0, 0]);
            ds.property("ADBE Drop Shadow-0002").setValue(opac);   // 0-255
            ds.property("ADBE Drop Shadow-0003").setValue(0);      // direction
            ds.property("ADBE Drop Shadow-0004").setValue(0);      // distance
            ds.property("ADBE Drop Shadow-0005").setValue(soft);   // softness
        } catch (e) {}
    }

    function addText(comp, str, font, size, color, tracking) {
        var L = comp.layers.addText(String(str));
        var tp = L.property("ADBE Text Properties").property("ADBE Text Document");
        var d = tp.value;
        d.resetCharStyle(); d.font = font; d.fontSize = size; d.fillColor = color;
        d.applyFill = true; d.applyStroke = false; d.tracking = tracking || 0;
        d.justification = ParagraphJustification.CENTER_JUSTIFY;
        tp.setValue(d);
        return L;
    }
    function revealUp(L, t0, y, x) {
        if (x === undefined) x = W / 2;
        var p = tg(L).property("ADBE Position");
        key2(p, t0, [x, y + 46], t0 + 0.5, [x, y], 80);
        var o = tg(L).property("ADBE Opacity");
        key2(o, t0, 0, t0 + 0.4, 100, 70);
    }
    function countText(comp, keys, font, size, color, x, y, revealT) {
        var num = addText(comp, keys[0][1], font, size, color, 0);
        num.motionBlur = true;                       // TRAP: per-layer
        tg(num).property("ADBE Position").setValue([x, y]);
        var ntp = num.property("ADBE Text Properties").property("ADBE Text Document");
        var doc = ntp.value;
        for (var i = 0; i < keys.length; i++) {
            doc.text = String(keys[i][1]);
            ntp.setValueAtTime(keys[i][0], doc);
        }
        var no = tg(num).property("ADBE Opacity");
        no.setValueAtTime(revealT, 0); no.setValueAtTime(revealT + 0.12, 100);
        var nsc = tg(num).property("ADBE Scale");
        nsc.setValueAtTime(0.55, [42, 42]); nsc.setValueAtTime(0.9, [112, 112]); nsc.setValueAtTime(1.2, [100, 100]);
        ease(nsc, 75);
        return num;
    }

    function buildBeat(spec) {
        var dur = spec.dur;
        var comp = proj.items.addComp("FRZ_" + spec.id, W, H, 1.0, dur, FPS);
        comp.motionBlur = true;

        // L9: black bg
        span(comp.layers.addSolid([0, 0, 0], "bg", W, H, 1.0), dur);

        // L8: still - fill + eased push-in + slow drift
        var io = new ImportOptions(new File(spec.still));
        var item = proj.importFile(io);
        try { item.mainSource.conformFrameRate = FPS; } catch (e) {}   // TRAP 11
        var S = comp.layers.add(item);
        span(S, dur);
        var sw = item.width, sh = item.height;
        var fill = Math.max(W / sw, H / sh) * 100;
        var st = tg(S);
        st.property("ADBE Anchor Point").setValue([sw / 2, sh / 2]);
        st.property("ADBE Position").setValue([W / 2, H / 2]);
        key2(st.property("ADBE Scale"), 0, [fill, fill], dur, [fill * 1.08, fill * 1.08], 25);
        key2(st.property("ADBE Position"), 0, [W / 2 - 18, H / 2 + 10], dur, [W / 2 + 18, H / 2 - 10], 20);

        // L7: cool grade wash
        var grade = comp.layers.addSolid([0.04, 0.07, 0.13], "grade", W, H, 1.0);
        span(grade, dur);
        grade.blendingMode = BlendingMode.MULTIPLY;
        tg(grade).property("ADBE Opacity").setValue(38);

        // L6: feathered elliptical vignette
        var vig = comp.layers.addSolid([0, 0, 0], "vignette", W, H, 1.0);
        span(vig, dur);
        var mask = vig.property("ADBE Mask Parade").addProperty("ADBE Mask Atom");
        var shp = new Shape();
        var rx = W * 0.62, ry = H * 0.62, cx = W / 2, cy = H / 2, kk = 0.5523;
        shp.vertices = [[cx, cy - ry], [cx + rx, cy], [cx, cy + ry], [cx - rx, cy]];
        shp.inTangents = [[-rx * kk, 0], [0, -ry * kk], [rx * kk, 0], [0, ry * kk]];
        shp.outTangents = [[rx * kk, 0], [0, ry * kk], [-rx * kk, 0], [0, -ry * kk]];
        shp.closed = true;
        mask.property("ADBE Mask Shape").setValue(shp);
        mask.maskMode = MaskMode.SUBTRACT;
        mask.property("ADBE Mask Feather").setValue([260, 260]);
        tg(vig).property("ADBE Opacity").setValue(62);

        // L5: gold glow (radial ramp, ADD)
        var glow = comp.layers.addSolid([0, 0, 0], "glow", W, H, 1.0);
        span(glow, dur);
        var gr = glow.property("ADBE Effect Parade").addProperty("ADBE Ramp");
        gr.property("ADBE Ramp-0001").setValue([W / 2, H * 0.42]);
        gr.property("ADBE Ramp-0002").setValue([GOLD[0], GOLD[1], GOLD[2]]);
        gr.property("ADBE Ramp-0003").setValue([W / 2, H * 0.95]);
        gr.property("ADBE Ramp-0004").setValue([0, 0, 0]);
        gr.property("ADBE Ramp-0005").setValue(2);
        glow.blendingMode = BlendingMode.ADD;
        var go = tg(glow).property("ADBE Opacity");
        go.setValueAtTime(0.0, 0); go.setValueAtTime(0.7, 22); go.setValueAtTime(dur, 14); ease(go, 60);

        // L4: light sweep
        var sweep = comp.layers.addSolid([1, 1, 1], "sweep", 360, Math.round(H * 1.6), 1.0);
        span(sweep, dur);
        sweep.blendingMode = BlendingMode.ADD;
        var swt = tg(sweep);
        swt.property("ADBE Rotate Z").setValue(18);          // TRAP 9
        key2(swt.property("ADBE Position"), 0.5, [-300, H / 2], 1.25, [W + 300, H / 2], 45);
        var swo = swt.property("ADBE Opacity");
        swo.setValueAtTime(0.5, 0); swo.setValueAtTime(0.7, 18); swo.setValueAtTime(1.25, 0);

        // L3c: readability scrims (added BELOW every text layer, ABOVE the still)
        // top-label row - light touch, the label is short and wide-tracked
        scrimBand(comp, dur, H * 0.210, 580, 54, 230, 48, 44, 0.10, 0.42);
        // hero row - the one that actually failed on hb03
        if (spec.layout === "D_CITATION_STAMP") {
            scrimBand(comp, dur, H * 0.545, 780, 84, 270, 64, 82, 1.45, 1.74);
        } else {
            scrimBand(comp, dur, H * 0.600, 700, 72, 250, 58, 60, 1.00, 1.32);
        }

        // L3: top label(s)
        if (spec.layout === "B_SPLIT_RATIO") {
            var tA = addText(comp, spec.top, FONT_LBL, 36, SILVER, 260);
            span(tA, dur); revealUp(tA, 0.15, H * 0.255, W * 0.30);
            var tB = addText(comp, spec.top2, FONT_LBL, 36, SILVER, 260);
            span(tB, dur); revealUp(tB, 0.23, H * 0.255, W * 0.70);
        } else {
            var topY = H * 0.205;
            var top = addText(comp, spec.top, FONT_LBL, 44, SILVER, 340);
            span(top, dur); textShadow(top, 180, 24); revealUp(top, 0.15, topY);
        }

        // L2b: gold accent line (scaleX wipe)
        var line = comp.layers.addSolid(GOLD, "accent", 460, 6, 1.0);
        span(line, dur);
        line.motionBlur = true;
        var lt = tg(line);
        lt.property("ADBE Position").setValue([W / 2, H * 0.485]);
        var lsc = lt.property("ADBE Scale");
        lsc.setValueAtTime(0.55, [0, 100]); lsc.setValueAtTime(1.05, [100, 100]);
        if (spec.layout === "D_CITATION_STAMP") {        // stamp pulse
            lsc.setValueAtTime(1.60, [100, 100]);
            lsc.setValueAtTime(1.66, [104, 100]);
            lsc.setValueAtTime(1.72, [100, 100]);
        }
        ease(lsc, 90);
        lt.property("ADBE Opacity").setValue(92);

        // L2: big number(s)
        if (spec.layout === "B_SPLIT_RATIO") {
            countText(comp, spec.numKeys, FONT_NUM, 210, GOLD, W * 0.30, H * 0.42, spec.numReveal);
            var fixed = addText(comp, spec.value2str, FONT_NUM, 210, SILVER, 0);
            span(fixed, dur);
            tg(fixed).property("ADBE Position").setValue([W * 0.70, H * 0.42]);
            var fo = tg(fixed).property("ADBE Opacity");
            fo.setValueAtTime(spec.numReveal, 0); fo.setValueAtTime(spec.numReveal + 0.12, 100);
            // vertical split line
            var vl = comp.layers.addSolid(SILVER, "split", 6, Math.round(H * 0.30), 1.0);
            span(vl, dur);
            tg(vl).property("ADBE Position").setValue([W / 2, H * 0.42]);
            key2(tg(vl).property("ADBE Scale"), 0.40, [100, 0], 0.85, [100, 100], 90);
            tg(vl).property("ADBE Opacity").setValue(70);
        } else {
            countText(comp, spec.numKeys, FONT_NUM, 250, GOLD, W / 2, H * 0.42, spec.numReveal);
        }

        // L1b: bottom label
        if (spec.layout === "D_CITATION_STAMP") {
            var cit = addText(comp, spec.bottom, FONT_LBL, 56, SILVER, 180);
            span(cit, dur);
            textShadow(cit, 205, 28);
            tg(cit).property("ADBE Position").setValue([W / 2, H * 0.545]);
            var csc = tg(cit).property("ADBE Scale");
            csc.setValueAtTime(1.60, [130, 130]); csc.setValueAtTime(1.78, [100, 100]);
            ease(csc, 85);
            var cop = tg(cit).property("ADBE Opacity");
            cop.setValueAtTime(1.60, 0); cop.setValueAtTime(1.70, 100);
        } else {
            var bot = addText(comp, spec.bottom, FONT_LBL, 64, WHITE, 120);
            span(bot, dur); textShadow(bot, 190, 26); revealUp(bot, 1.15, H * 0.60);
        }

        // L1: caption lower-third
        var barY = H * 0.90;
        var bar = comp.layers.addSolid([0.02, 0.04, 0.08], "capbar", W, 130, 1.0);
        span(bar, dur);
        tg(bar).property("ADBE Position").setValue([W / 2, barY]);
        var bo = tg(bar).property("ADBE Opacity");
        bo.setValueAtTime(0.2, 0); bo.setValueAtTime(0.5, 64);
        bo.setValueAtTime(dur - 0.4, 64); bo.setValueAtTime(dur - 0.1, 0);
        if (spec.caption && spec.caption.length) {
            var cap = addText(comp, spec.caption, FONT_LBL, 42, WHITE, 20);
            span(cap, dur);
            var ctp = cap.property("ADBE Text Properties").property("ADBE Text Document");
            var cd = ctp.value; cd.leading = 50; ctp.setValue(cd);
            tg(cap).property("ADBE Position").setValue([W / 2, barY - 6]);
            var co = tg(cap).property("ADBE Opacity");
            co.setValueAtTime(0.3, 0); co.setValueAtTime(0.6, 100);
            co.setValueAtTime(dur - 0.4, 100); co.setValueAtTime(dur - 0.12, 0);
        }

        // L0: black seam dips
        var dip = comp.layers.addSolid([0, 0, 0], "dip", W, H, 1.0);
        span(dip, dur);
        var dop = tg(dip).property("ADBE Opacity");
        dop.setValueAtTime(0, 100); dop.setValueAtTime(spec.head, 0);
        dop.setValueAtTime(dur - spec.tail, 0); dop.setValueAtTime(dur, 100);
        ease(dop, 40);

        return comp;
    }

    // ---- build all + queue renders ----
    var rq = proj.renderQueue;
    while (rq.numItems > 0) rq.item(1).remove();
    var built = 0;
    // RENDER_ONLY: when non-empty, every comp is still BUILT (the .aep stays
    // complete) but only these ids are queued -- so a targeted fix cannot
    // overwrite an already-approved mp4.
    var RENDER_ONLY = %(RENDER_ONLY)s;
    function queued(id) {
        if (!RENDER_ONLY.length) return true;
        for (var q = 0; q < RENDER_ONLY.length; q++) if (RENDER_ONLY[q] === id) return true;
        return false;
    }
    for (var bi = 0; bi < BEATS.length; bi++) {
        var comp = buildBeat(BEATS[bi]);
        built++;
        if (!queued(BEATS[bi].id)) continue;
        var it = rq.items.add(comp);
        try { it.applyTemplate("最良設定"); } catch (e) { try { it.applyTemplate("Best Settings"); } catch (e2) {} }
        var om = it.outputModule(1);
        var omOK = false, omNames = ["H.264 - レンダリング設定を一致 - 15 Mbps",
                                     "H.264 - Match Render Settings - 15 Mbps"];
        for (var oi = 0; oi < omNames.length && !omOK; oi++) {
            try { om.applyTemplate(omNames[oi]); omOK = true; } catch (e3) {}
        }
        om.file = new File(BEATS[bi].out);
    }
    app.project.save(new File("%(AEP)s"));
    app.endUndoGroup();
    try {
        var mk = new File(RENDER_DIR + "/_build_ok.txt");
        mk.open("w");
        mk.write("comps=" + built + " queue=" + proj.renderQueue.numItems + " fonts: " + FONT_LOG);
        mk.close();
    } catch (e) {}
    try { app.quit(); } catch (e) {}
})();
"""


def main() -> int:
    render_only = []
    if "--render-only" in sys.argv:
        render_only = sys.argv[sys.argv.index("--render-only") + 1].split(",")
    spec = json.loads(SPEC.read_text(encoding="utf-8"))
    WORK.mkdir(parents=True, exist_ok=True)
    RENDER.mkdir(parents=True, exist_ok=True)
    beats = build_beats(spec)
    (WORK / "beats.json").write_text(json.dumps(beats, indent=2, ensure_ascii=False), encoding="utf-8")
    c = spec["colors"]
    jsx = JSX_TEMPLATE % dict(
        W=spec["width"], H=spec["height"], FPS=spec["fps"],
        GOLD=", ".join(f"{v:.3f}" for v in c["GOLD"]),
        WHITE=", ".join(f"{v:.3f}" for v in c["WHITE"]),
        SILVER=", ".join(f"{v:.3f}" for v in c["SILVER"]),
        BEATS=json.dumps(beats, ensure_ascii=False),
        RENDER_ONLY=json.dumps(render_only),
        RENDER=str(RENDER).replace("\\", "/"),
        AEP=str(WORK / "frazier_hero.aep").replace("\\", "/"),
    )
    (WORK / "frazier_hero.jsx").write_text(jsx, encoding="utf-8")
    print(f"[gen] beats: {len(beats)}")
    for b in beats:
        print(f"  {b['id']}  {b['layout']:<16} dur={b['dur']:.1f}  "
              f"num={b['numKeys'][-1][1]!r}  still={Path(b['still']).name}  cap={b['caption'][:38]!r}")
    print("[gen] jsx   ->", WORK / "frazier_hero.jsx")
    print("[gen] sidecar ->", WORK / "beats.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
