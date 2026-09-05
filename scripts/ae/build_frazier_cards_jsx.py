"""EP39 frazier - AE CARD FAMILY JSX generator (act titles / stamp / stats /
document / transitions).

Companion to build_frazier_hero_jsx.py. The hero beats (hb01..hb08) are already
rendered and approved; this script NEVER touches them. It writes to a separate
work dir (ae_cards/) and a separate .aep.

------------------------------------------------------------------------------
STRING PROVENANCE - every glyph burned to screen is traceable to the locked
script episodes/_planning/EP39_frazier_script.en.v001.md. Nothing is invented.
------------------------------------------------------------------------------
  act1..act4   ACT numeral from the script's act headings (## ACT I .. ## ACT IV).
               The headings' subtitles are Japanese production labels, so each
               card's sub-line is instead a VERBATIM English string from inside
               that act:
                 ACT I   "AUGUST 13, 1987"   <- L26 "On the morning of August 13, 1987"
                 ACT II  "THE STATEMENT"     <- L48 "The statement did not fit the house."
                 ACT III "FRAZIER v. CUPP"   <- the heading itself is English
                 ACT IV  "SIXTEEN YEARS"     <- L102 "Sixteen years."
  stamp        L94 OST, verbatim. The three " . " separated segments become the
               three type ranks; concatenating rank1 + " . " + rank2 + " . " +
               rank3 reproduces the OST string character for character.
  stats        L126 OST, verbatim. The five " . " separated segments become the
               five staggered rows. AVERAGE EXONEREE is the ONE added string:
               it is an attribution required so row 5 is not misread as Barry
               Laughman's own ages (his are 25 -> 40, on hb05). Supported by
               L122 "the average client served sixteen years".
  document     L42 "a statement in his own name", uppercased. NO readable fake
               document is drawn - the page is texture only (abstract rules,
               zero glyphs, gaussian-blurred). EP39's subject is a fabricated
               forensic report, so a legible prop document is a hard no.
  trans_*      no text at all.
------------------------------------------------------------------------------

Machine traps honoured (identical to the hero builder):
  * font resolve via getFontsByFamilyNameAndStyleName + array-wrapper unwrap;
    NOT_FOUND throws instead of silently substituting
  * setTemporalEaseAtKey dimension is 1 for spatial props
  * no app.newProject()
  * per-layer motionBlur, "ADBE Rotate Z", inPoint AND outPoint both set
  * localized RS "最良設定" / OM "H.264 - レンダリング設定を一致 - 15 Mbps"
  * no "\n" in any TextDocument - multi-line is always multi-layer
  * completion marker file, app.quit() at the end
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(r"C:\Users\aab15\Documents\prime-documentary")
SCRIPT = ROOT / "episodes" / "_planning" / "EP39_frazier_script.en.v001.md"
WORK = Path("E:/pd-media/episodes/PD-2026-039-frazier/08_edit/ae_cards")

FPS = 30
W, H = 1920, 1080
GOLD = [0.898, 0.710, 0.227]
WHITE = [0.961, 0.969, 0.980]
SILVER = [0.588, 0.627, 0.682]
PAPER = [0.702, 0.663, 0.584]   # v001 sheet was too bright/saturated on frame

# --- the two OST lines this script renders, quoted from the locked script -----
OST_STAMP = ("FRAZIER v. CUPP · 394 U.S. 731 (1969) · "
             "ARGUED FEB 26, 1969 · DECIDED APR 22, 1969")
OST_STATS = ("257 CASES · 29% FALSE CONFESSION · 62% MISTAKEN EYEWITNESS ID · "
             "205 CLEARED BY DNA · IN AT 27, OUT AT 45")

ACTS = [
    ("act1", "ACT I", "AUGUST 13, 1987"),
    ("act2", "ACT II", "THE STATEMENT"),
    ("act3", "ACT III", "FRAZIER v. CUPP"),
    ("act4", "ACT IV", "SIXTEEN YEARS"),
]
DOC_LABEL = "A STATEMENT IN HIS OWN NAME"
STATS_ATTRIB = "AVERAGE EXONEREE"

# The remaining three 【OST:】 directives. Verbatim from script.en.v001 -- the build
# gate below refuses to run if any of these drifts from the script.
OST_HOOK = "THE FINGERPRINT DID NOT EXIST"
OST_IQ = 'IQ 70. TOLD: "YOUR PRINTS ARE THERE."'
OST_EXON = "EXONERATED 2004 · DIED 2024"


def verify_against_script() -> None:
    """Hard gate: refuse to build if a burned string is not in the script."""
    src = SCRIPT.read_text(encoding="utf-8")
    problems = []
    for label, needle in (("OST_STAMP", OST_STAMP), ("OST_STATS", OST_STATS),
                          ("OST_HOOK", OST_HOOK), ("OST_IQ", OST_IQ),
                          ("OST_EXON", OST_EXON)):
        if needle not in src:
            problems.append(f"{label} not found verbatim in script")
    for _id, act, sub in ACTS:
        if f"## {act} " not in src:
            problems.append(f"act heading '{act}' not in script")
        if sub.lower() not in src.lower():
            problems.append(f"act sub-line '{sub}' not in script")
    if DOC_LABEL.lower() not in src.lower():
        problems.append(f"doc label '{DOC_LABEL}' not in script")
    if problems:
        for p in problems:
            print("FAIL " + p, file=sys.stderr)
        sys.exit(2)
    print("[gate] all burned strings verified verbatim against script.en.v001")


def split_ost(ost: str) -> list[str]:
    return [s.strip() for s in ost.split("·")]


def build_cards() -> list[dict]:
    stamp = split_ost(OST_STAMP)          # 4 segments
    stats = split_ost(OST_STATS)          # 5 segments
    # stamp hierarchy: case name > volume/page/year > the two argument dates
    stamp_ranks = [stamp[0], stamp[1], stamp[2] + " · " + stamp[3]]
    assert " · ".join([stamp_ranks[0], stamp_ranks[1], stamp_ranks[2]]) == OST_STAMP

    # stats rows: leading numeral split off its label where one exists
    rows = []
    for seg in stats[:4]:
        num, _, lab = seg.partition(" ")
        rows.append({"num": num, "label": lab})
    rows.append({"num": None, "label": stats[4]})   # IN AT 27, OUT AT 45
    assert " · ".join(
        [(r["num"] + " " + r["label"]) if r["num"] else r["label"] for r in rows]
    ) == OST_STATS

    cards = []
    for cid, act, sub in ACTS:
        cards.append({"id": cid, "kind": "ACT", "dur": 1.8,
                      "title": act, "sub": sub})
    cards.append({"id": "stamp_frazier", "kind": "STAMP", "dur": 4.5,
                  "ranks": stamp_ranks})
    cards.append({"id": "stats_ip", "kind": "STATS", "dur": 6.5,
                  "rows": rows, "attrib": STATS_ATTRIB})
    cards.append({"id": "doc_statement", "kind": "DOC", "dur": 5.0,
                  "label": DOC_LABEL})
    # HOOK card: one line, held. This is the 0:00-0:10 frame -- it decides whether
    # the other 12 minutes get watched, so it gets its own beat and no competition.
    cards.append({"id": "hook_fingerprint", "kind": "STAMP", "dur": 3.2,
                  "ranks": [OST_HOOK]})
    # The lie, stated as the film states it: what was measured, and what he was told.
    cards.append({"id": "iq_told", "kind": "STAMP", "dur": 4.5,
                  "ranks": [OST_IQ.split(".")[0], OST_IQ.split(". ", 1)[1]]})
    cards.append({"id": "exonerated", "kind": "STAMP", "dur": 4.0,
                  "ranks": [s.strip() for s in OST_EXON.split("·")]})
    cards.append({"id": "trans_sink", "kind": "TRANS_SINK", "dur": 0.7})
    cards.append({"id": "trans_wipe", "kind": "TRANS_WIPE", "dur": 0.6})
    for c in cards:
        c["out"] = str(WORK / f"{c['id']}.mp4").replace("\\", "/")
    return cards


JSX_TEMPLATE = r"""// AUTO-GENERATED - EP39 frazier AE card family. Do not hand-edit.
(function () {
    var W = %(W)d, H = %(H)d, FPS = %(FPS)d;
    var GOLD = [%(GOLD)s], WHITE = [%(WHITE)s], SILVER = [%(SILVER)s], PAPER = [%(PAPER)s];
    var CARDS = %(CARDS)s;
    var RENDER_DIR = "%(WORK)s";

    // app.newProject() hangs headless on the save prompt -- never call it.
    var proj = app.project;
    try { for (var ri = proj.numItems; ri >= 1; ri--) {
        var itx = proj.item(ri);
        if (itx instanceof CompItem && String(itx.name).indexOf("FRC") === 0) itx.remove();
    } } catch (e) {}
    try { proj.gpuAccelType = GpuAccelType.SOFTWARE; } catch (e) {}
    try { proj.bitsPerChannel = 8; } catch (e) {}
    app.beginUndoGroup("frazier_cards");

    // ---- runtime font resolver: a silent substitution is a HARD FAIL ----
    // app.fonts.allFonts[i] is an array-LIKE wrapper, not a FontObject; its
    // .familyName is undefined. Unwrap to [0], and hand TextDocument.font the
    // PostScript name. If the family is genuinely absent we THROW - EP38
    // shipped in a substituted face because that path returned the family name.
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

    // ---------------- primitives ----------------
    function ease(prop, inf) {
        inf = inf || 70; var n = prop.numKeys;
        var dim = 1;                                  // TRAP: spatial -> 1
        if (!prop.isSpatial) { var v0 = prop.value; dim = (v0 instanceof Array) ? v0.length : 1; }
        var a = [], b = [];
        for (var d = 0; d < dim; d++) { a.push(new KeyframeEase(0, inf)); b.push(new KeyframeEase(0, inf)); }
        for (var k = 1; k <= n; k++) {
            try { prop.setInterpolationTypeAtKey(k, KeyframeInterpolationType.BEZIER, KeyframeInterpolationType.BEZIER); } catch (e) {}
            try { prop.setTemporalEaseAtKey(k, a, b); } catch (e2) {}
        }
    }
    function key2(p, t0, v0, t1, v1, inf) { p.setValueAtTime(t0, v0); p.setValueAtTime(t1, v1); ease(p, inf); }
    function tg(L) { return L.property("ADBE Transform Group"); }
    function span(L, dur) { L.inPoint = 0; L.outPoint = dur; }   // TRAP: set BOTH

    var JU = { C: ParagraphJustification.CENTER_JUSTIFY,
               L: ParagraphJustification.LEFT_JUSTIFY,
               R: ParagraphJustification.RIGHT_JUSTIFY };

    function addText(comp, str, font, size, color, tracking, just) {
        // TRAP: never put "\n" in a TextDocument. Every line is its own layer.
        var L = comp.layers.addText(String(str));
        var tp = L.property("ADBE Text Properties").property("ADBE Text Document");
        var d = tp.value;
        d.resetCharStyle(); d.font = font; d.fontSize = size; d.fillColor = color;
        d.applyFill = true; d.applyStroke = false; d.tracking = tracking || 0;
        d.justification = just || JU.C;
        tp.setValue(d);
        return L;
    }
    function textShadow(L, opac, soft) {
        try {
            var ds = L.property("ADBE Effect Parade").addProperty("ADBE Drop Shadow");
            ds.property("ADBE Drop Shadow-0001").setValue([0, 0, 0]);
            ds.property("ADBE Drop Shadow-0002").setValue(opac);
            ds.property("ADBE Drop Shadow-0003").setValue(0);
            ds.property("ADBE Drop Shadow-0004").setValue(0);
            ds.property("ADBE Drop Shadow-0005").setValue(soft);
        } catch (e) {}
    }
    function blur(L, r) {
        try {
            var b = L.property("ADBE Effect Parade").addProperty("ADBE Gaussian Blur 2");
            b.property("ADBE Gaussian Blur 2-0001").setValue(r);
            b.property("ADBE Gaussian Blur 2-0003").setValue(true);   // repeat edge
        } catch (e) {}
    }

    // TRUE masked slide-up: the text lives in a slab precomp whose own bounds
    // clip it, so the crop stays put while the glyphs travel. (A mask on the
    // text layer itself would travel with the layer and do nothing.)
    var slabN = 0;
    function maskedText(comp, str, font, size, color, tracking, cx, cy, t0, dur, slabW, just) {
        var sh = Math.round(size * 1.55);
        var sw = slabW || W;
        var sub = proj.items.addComp("FRCT_" + (slabN++), sw, sh, 1.0, dur, FPS);
        var T = addText(sub, str, font, size, color, tracking, just || JU.C);
        var yEnd = Math.round(sh * 0.5 + size * 0.35);
        var p = tg(T).property("ADBE Position");
        p.setValueAtTime(t0, [sw / 2, yEnd + sh]);          // fully below the crop
        p.setValueAtTime(t0 + 0.60, [sw / 2, yEnd]);
        ease(p, 84);
        T.motionBlur = true;
        var L = comp.layers.add(sub);
        span(L, dur);
        tg(L).property("ADBE Position").setValue([cx, cy]);
        L.motionBlur = true;
        return { layer: L, inner: T, comp: sub };
    }

    function goldRule(comp, dur, cx, cy, wpx, t0, t1, hpx) {
        var line = comp.layers.addSolid(GOLD, "rule", wpx, hpx || 4, 1.0);
        span(line, dur); line.motionBlur = true;
        tg(line).property("ADBE Position").setValue([cx, cy]);
        var sc = tg(line).property("ADBE Scale");
        sc.setValueAtTime(t0, [0, 100]); sc.setValueAtTime(t1, [100, 100]);
        ease(sc, 90);
        tg(line).property("ADBE Opacity").setValue(94);
        return line;
    }

    // three-layer bed required behind every card: grade / lines / glow
    function bed(comp, dur, glowY, glowPeak) {
        span(comp.layers.addSolid([0, 0, 0], "bg", W, H, 1.0), dur);
        // L-b: deep navy vertical grade
        var gr = comp.layers.addSolid([0, 0, 0], "grade", W, H, 1.0);
        span(gr, dur);
        var rp = gr.property("ADBE Effect Parade").addProperty("ADBE Ramp");
        rp.property("ADBE Ramp-0001").setValue([W / 2, 0]);
        rp.property("ADBE Ramp-0002").setValue([0.035, 0.055, 0.098]);
        rp.property("ADBE Ramp-0003").setValue([W / 2, H]);
        rp.property("ADBE Ramp-0004").setValue([0.005, 0.008, 0.016]);
        rp.property("ADBE Ramp-0005").setValue(1);
        // L-c: fine drifting rule grid
        var grid = comp.layers.addSolid([0, 0, 0], "grid", W, H, 1.0);
        span(grid, dur);
        for (var g = 0; g < 7; g++) {
            var mk = grid.property("ADBE Mask Parade").addProperty("ADBE Mask Atom");
            var y = 90 + g * 150, sp = new Shape();
            sp.vertices = [[0, y], [W, y], [W, y + 2], [0, y + 2]];
            sp.closed = true;
            mk.property("ADBE Mask Shape").setValue(sp);
            mk.maskMode = MaskMode.ADD;
        }
        grid.property("ADBE Effect Parade").addProperty("ADBE Fill")
            .property("ADBE Fill-0002").setValue(SILVER);
        tg(grid).property("ADBE Opacity").setValue(9);
        key2(tg(grid).property("ADBE Position"), 0, [W / 2, H / 2 + 14], dur, [W / 2, H / 2 - 14], 20);
        // L-d: gold glow
        var glow = comp.layers.addSolid([0, 0, 0], "glow", W, H, 1.0);
        span(glow, dur);
        var g2 = glow.property("ADBE Effect Parade").addProperty("ADBE Ramp");
        g2.property("ADBE Ramp-0001").setValue([W / 2, glowY]);
        g2.property("ADBE Ramp-0002").setValue(GOLD);
        g2.property("ADBE Ramp-0003").setValue([W / 2, H * 1.05]);
        g2.property("ADBE Ramp-0004").setValue([0, 0, 0]);
        g2.property("ADBE Ramp-0005").setValue(2);
        glow.blendingMode = BlendingMode.ADD;
        var go = tg(glow).property("ADBE Opacity");
        go.setValueAtTime(0, 0); go.setValueAtTime(dur * 0.35, glowPeak);
        go.setValueAtTime(dur, glowPeak * 0.6); ease(go, 60);
    }

    function vignette(comp, dur, opac) {
        var vig = comp.layers.addSolid([0, 0, 0], "vignette", W, H, 1.0);
        span(vig, dur);
        var mask = vig.property("ADBE Mask Parade").addProperty("ADBE Mask Atom");
        var shp = new Shape();
        var rx = W * 0.60, ry = H * 0.60, cx = W / 2, cy = H / 2, kk = 0.5523;
        shp.vertices = [[cx, cy - ry], [cx + rx, cy], [cx, cy + ry], [cx - rx, cy]];
        shp.inTangents = [[-rx * kk, 0], [0, -ry * kk], [rx * kk, 0], [0, ry * kk]];
        shp.outTangents = [[rx * kk, 0], [0, ry * kk], [-rx * kk, 0], [0, -ry * kk]];
        shp.closed = true;
        mask.property("ADBE Mask Shape").setValue(shp);
        mask.maskMode = MaskMode.SUBTRACT;
        mask.property("ADBE Mask Feather").setValue([280, 280]);
        tg(vig).property("ADBE Opacity").setValue(opac);
    }

    function seam(comp, dur, head, tail) {
        var dip = comp.layers.addSolid([0, 0, 0], "dip", W, H, 1.0);
        span(dip, dur);
        var o = tg(dip).property("ADBE Opacity");
        o.setValueAtTime(0, 100); o.setValueAtTime(head, 0);
        o.setValueAtTime(dur - tail, 0); o.setValueAtTime(dur, 100);
        ease(o, 40);
    }

    // ---------------- card builders ----------------
    function buildACT(c) {
        var d = c.dur;
        var comp = proj.items.addComp("FRC_" + c.id, W, H, 1.0, d, FPS);
        comp.motionBlur = true;
        bed(comp, d, H * 0.46, 15);
        vignette(comp, d, 58);
        // numeral - the hero, restrained: one masked rise, slight settle
        var t = maskedText(comp, c.title, FONT_NUM, 148, WHITE, 56, W / 2, H * 0.435, 0.14, d, 1500);
        textShadow(t.layer, 165, 30);
        var sc = tg(t.layer).property("ADBE Scale");
        sc.setValueAtTime(0.14, [104, 104]); sc.setValueAtTime(0.86, [100, 100]);
        ease(sc, 80);
        goldRule(comp, d, W / 2, H * 0.535, 300, 0.42, 0.92, 4);
        var s = maskedText(comp, c.sub, FONT_LBL, 42, SILVER, 330, W / 2, H * 0.615, 0.36, d, 1600);
        textShadow(s.layer, 160, 24);
        seam(comp, d, 0.14, 0.16);
        return comp;
    }

    function buildSTAMP(c) {
        var d = c.dur;
        var comp = proj.items.addComp("FRC_" + c.id, W, H, 1.0, d, FPS);
        comp.motionBlur = true;
        bed(comp, d, H * 0.40, 20);
        vignette(comp, d, 62);
        // A card may carry fewer than three lines. Render only what is present --
        // an absent rank previously typeset the JS string "undefined".
        function rankAt(ix) {
            var v = c.ranks && c.ranks[ix];
            if (v === undefined || v === null) return null;
            if (typeof v !== "string" || v.length === 0)
                throw new Error("card " + c.id + " rank " + ix + " is not a non-empty string");
            return v;
        }
        var _r0 = rankAt(0), _r1 = rankAt(1), _r2 = rankAt(2);
        if (_r0 === null) throw new Error("card " + c.id + " has no rank 0");

        // rank 1: the case name, largest
        var r1 = maskedText(comp, _r0, FONT_NUM, 132, WHITE, 30, W / 2, H * 0.325, 0.22, d, 1720);
        textShadow(r1.layer, 180, 30);
        goldRule(comp, d, W / 2, H * 0.435, 560, 0.50, 1.02, 5);
        // rank 2: volume / page / year, gold
        if (_r1 !== null) {
            var r2 = maskedText(comp, _r1, FONT_NUM, 86, GOLD, 24, W / 2, H * 0.535, 0.62, d, 1720);
            textShadow(r2.layer, 170, 26);
        }
        // rank 3: the two argument dates, smallest + widest tracking
        if (_r2 !== null) {
            var r3 = maskedText(comp, _r2, FONT_LBL, 38, SILVER, 210, W / 2, H * 0.645, 0.98, d, 1860);
            textShadow(r3.layer, 175, 24);
        }
        // stamp impact on the case name once the stack has landed
        var sc = tg(r1.layer).property("ADBE Scale");
        sc.setValueAtTime(1.62, [100, 100]); sc.setValueAtTime(1.70, [103.5, 103.5]);
        sc.setValueAtTime(1.80, [100, 100]); ease(sc, 85);
        // light sweep across the finished stack
        var sw = comp.layers.addSolid([1, 1, 1], "sweep", 300, Math.round(H * 1.6), 1.0);
        span(sw, d); sw.blendingMode = BlendingMode.ADD; sw.motionBlur = true;
        tg(sw).property("ADBE Rotate Z").setValue(16);            // TRAP: 2D name
        key2(tg(sw).property("ADBE Position"), 1.55, [-320, H / 2], 2.35, [W + 320, H / 2], 45);
        var so = tg(sw).property("ADBE Opacity");
        so.setValueAtTime(1.55, 0); so.setValueAtTime(1.85, 16); so.setValueAtTime(2.35, 0);
        seam(comp, d, 0.13, 0.20);
        return comp;
    }

    function buildSTATS(c) {
        var d = c.dur;
        var comp = proj.items.addComp("FRC_" + c.id, W, H, 1.0, d, FPS);
        comp.motionBlur = true;
        bed(comp, d, H * 0.50, 16);
        vignette(comp, d, 60);
        var rowY = [258, 396, 534, 672], t0s = [0.30, 0.82, 1.34, 1.86];
        var SW = 1480, SH = 132;
        // GUTTER measured from the v001 render: numerals right-aligned at slab
        // x=600 pushed the whole block ~85px right of frame centre and left the
        // gold ticks stranded out at x=340 with nothing to attach to. Ticks are
        // gone; the gutter moves left so rows 1-4 share row 5's centre axis.
        var GUT = 515;
        for (var i = 0; i < 4; i++) {
            var row = c.rows[i];
            var sub = proj.items.addComp("FRCR_" + c.id + "_" + i, SW, SH, 1.0, d, FPS);
            // numeral, right-aligned into the gutter, counts up
            var num = addText(sub, row.numKeys[0][1], FONT_NUM, 92, GOLD, 10, JU.R);
            num.motionBlur = true;
            tg(num).property("ADBE Position").setValue([GUT, 96]);
            var ntp = num.property("ADBE Text Properties").property("ADBE Text Document");
            var doc = ntp.value;
            for (var k = 0; k < row.numKeys.length; k++) {
                doc.text = String(row.numKeys[k][1]);
                ntp.setValueAtTime(row.numKeys[k][0], doc);
            }
            // label, left-aligned off the same gutter
            var lab = addText(sub, row.label, FONT_LBL, 46, WHITE, 90, JU.L);
            tg(lab).property("ADBE Position").setValue([GUT + 60, 88]);
            span(num, d); span(lab, d);
            // the whole row rides up inside its own slab -> real masked reveal
            var RL = comp.layers.add(sub);
            span(RL, d); RL.motionBlur = true;
            var rp = tg(RL).property("ADBE Position");
            rp.setValueAtTime(t0s[i], [W / 2, rowY[i] + SH]);
            rp.setValueAtTime(t0s[i] + 0.58, [W / 2, rowY[i]]);
            ease(rp, 84);
        }
        // row 5: the average-exoneree pair, full width, with its attribution
        var r5 = c.rows[4];
        var s5 = proj.items.addComp("FRCR_" + c.id + "_4", SW, 190, 1.0, d, FPS);
        var big = addText(s5, r5.label, FONT_NUM, 78, GOLD, 16, JU.C);
        tg(big).property("ADBE Position").setValue([SW / 2, 84]); span(big, d);
        var att = addText(s5, c.attrib, FONT_LBL, 30, SILVER, 300, JU.C);
        tg(att).property("ADBE Position").setValue([SW / 2, 150]); span(att, d);
        var A5 = comp.layers.add(s5);
        span(A5, d); A5.motionBlur = true;
        var p5 = tg(A5).property("ADBE Position");
        p5.setValueAtTime(2.44, [W / 2, 880 + 190]);
        p5.setValueAtTime(3.04, [W / 2, 880]);
        ease(p5, 84);
        // separator above the attributed row so it reads as a different rank
        goldRule(comp, d, W / 2, 792, 900, 2.30, 2.86, 3);
        seam(comp, d, 0.13, 0.20);
        return comp;
    }

    function buildDOC(c) {
        var d = c.dur;
        var comp = proj.items.addComp("FRC_" + c.id, W, H, 1.0, d, FPS);
        comp.motionBlur = true;
        bed(comp, d, H * 0.44, 14);
        // ---- the page: TEXTURE ONLY. Zero glyphs are drawn anywhere on it.
        // EP39 is about a fabricated forensic report, so a legible prop
        // document would be genuinely irresponsible. These are abstract rules.
        var PW = 900, PH = 1180;
        var page = proj.items.addComp("FRCP_" + c.id, PW, PH, 1.0, d, FPS);
        var sheet = page.layers.addSolid(PAPER, "sheet", PW, PH, 1.0);
        span(sheet, d);
        // v001 read as a flat vector mockup: 20 identical 13px bars at one
        // opacity. Real out-of-focus type has varied weight and ragged rhythm,
        // so heights/opacities/indents now vary per line and the whole page is
        // blurred harder below.
        var widths = [620, 700, 540, 660, 480, 690, 610, 720, 500, 640,
                      580, 700, 460, 670, 620, 540, 690, 600, 720, 510,
                      650, 590, 700, 470, 660];
        var hts = [9, 11, 8, 10, 9, 12, 8, 10, 11, 9,
                   10, 8, 11, 9, 10, 12, 8, 9, 11, 10,
                   9, 11, 8, 10, 9];
        for (var i = 0; i < widths.length; i++) {
            var indent = (i %% 5 === 0) ? 34 : 0;      // paragraph starts
            var bar = page.layers.addSolid([0.20, 0.18, 0.15], "r" + i, widths[i], hts[i], 1.0);
            span(bar, d);
            tg(bar).property("ADBE Position").setValue([90 + indent + widths[i] / 2, 232 + i * 34]);
            tg(bar).property("ADBE Opacity").setValue(30 + (i %% 4) * 6);
        }
        // masthead block + redaction bar + signature rule (still: no letters)
        var head = page.layers.addSolid([0.24, 0.22, 0.19], "head", 380, 26, 1.0);
        span(head, d);
        tg(head).property("ADBE Position").setValue([280, 150]);
        tg(head).property("ADBE Opacity").setValue(62);
        var red = page.layers.addSolid([0.05, 0.05, 0.05], "redact", 430, 30, 1.0);
        span(red, d);
        tg(red).property("ADBE Position").setValue([330, 520]);
        var sig = page.layers.addSolid([0.20, 0.18, 0.15], "sigrule", 380, 4, 1.0);
        span(sig, d);
        tg(sig).property("ADBE Position").setValue([320, 1090]);
        tg(sig).property("ADBE Opacity").setValue(60);
        // page-level falloff so the sheet dies into the frame instead of being
        // guillotined by the caption scrim (the hard band in v001)
        var fall = page.layers.addSolid([0, 0, 0], "falloff", PW, PH, 1.0);
        span(fall, d);
        var fr = fall.property("ADBE Effect Parade").addProperty("ADBE Ramp");
        // MULTIPLY ramp: WHITE end = untouched, BLACK end = extinguished.
        // v002 had these swapped, which darkened the top of the sheet and left
        // the bottom bright right where the caption sits. White at top.
        fr.property("ADBE Ramp-0001").setValue([PW / 2, PH * 0.30]);
        fr.property("ADBE Ramp-0002").setValue([1, 1, 1]);
        fr.property("ADBE Ramp-0003").setValue([PW / 2, PH * 1.00]);
        fr.property("ADBE Ramp-0004").setValue([0, 0, 0]);
        fr.property("ADBE Ramp-0005").setValue(1);
        fall.blendingMode = BlendingMode.MULTIPLY;
        tg(fall).property("ADBE Opacity").setValue(82);

        var P = comp.layers.add(page);
        span(P, d); P.motionBlur = true;
        var pt = tg(P);
        pt.property("ADBE Rotate Z").setValue(-2.6);              // TRAP: 2D name
        key2(pt.property("ADBE Scale"), 0, [74, 74], d, [80, 80], 25);
        key2(pt.property("ADBE Position"), 0, [W / 2 - 26, H / 2 + 22], d, [W / 2 + 26, H / 2 - 22], 20);
        blur(P, 9);                         // reads as paper, never as a document
        var po = pt.property("ADBE Opacity");
        po.setValueAtTime(0.05, 0); po.setValueAtTime(0.75, 80); ease(po, 70);
        vignette(comp, d, 74);
        // hard local scrim so the caption cannot be eaten by the bright sheet
        var sc = comp.layers.addSolid([0.008, 0.014, 0.028], "scrim", W, H, 1.0);
        span(sc, d);
        var m = sc.property("ADBE Mask Parade").addProperty("ADBE Mask Atom");
        var s = new Shape();
        s.vertices = [[180, H * 0.80 - 92], [W - 180, H * 0.80 - 92],
                      [W - 180, H * 0.80 + 92], [180, H * 0.80 + 92]];
        s.closed = true;
        m.property("ADBE Mask Shape").setValue(s);
        m.property("ADBE Mask Feather").setValue([300, 150]);
        var so = tg(sc).property("ADBE Opacity");
        so.setValueAtTime(0.85, 0); so.setValueAtTime(1.20, 70); ease(so, 60);
        goldRule(comp, d, W / 2, H * 0.735, 320, 0.95, 1.45, 4);
        var lab = maskedText(comp, c.label, FONT_LBL, 52, WHITE, 180, W / 2, H * 0.805, 1.05, d, 1800);
        textShadow(lab.layer, 205, 30);
        seam(comp, d, 0.13, 0.20);
        return comp;
    }

    function buildTRANS_SINK(c) {
        var d = c.dur;                                  // 0.7s sink-to-black
        var comp = proj.items.addComp("FRC_" + c.id, W, H, 1.0, d, FPS);
        comp.motionBlur = true;
        span(comp.layers.addSolid([0, 0, 0], "bg", W, H, 1.0), d);
        var glow = comp.layers.addSolid([0, 0, 0], "glow", W, H, 1.0);
        span(glow, d);
        var g = glow.property("ADBE Effect Parade").addProperty("ADBE Ramp");
        g.property("ADBE Ramp-0001").setValue([W / 2, H / 2]);
        g.property("ADBE Ramp-0002").setValue(GOLD);
        g.property("ADBE Ramp-0003").setValue([W / 2, H * 0.94]);
        g.property("ADBE Ramp-0004").setValue([0, 0, 0]);
        g.property("ADBE Ramp-0005").setValue(2);
        glow.blendingMode = BlendingMode.ADD;
        // v001 was gone by 40%% of the run and read as near-black for most of
        // the clip. The seam now holds bright, collapses later, and the black
        // only takes over at the end.
        var go = tg(glow).property("ADBE Opacity");
        go.setValueAtTime(0, 52); go.setValueAtTime(d * 0.60, 26); go.setValueAtTime(d, 0);
        ease(go, 75);
        // a gold seam collapses to a point, motion-blurred
        var ln = comp.layers.addSolid(GOLD, "seamline", W, 6, 1.0);
        span(ln, d); ln.motionBlur = true;
        tg(ln).property("ADBE Position").setValue([W / 2, H / 2]);
        var sc = tg(ln).property("ADBE Scale");
        sc.setValueAtTime(0, [100, 100]); sc.setValueAtTime(d * 0.88, [0, 300]);
        ease(sc, 92);
        var lo = tg(ln).property("ADBE Opacity");
        lo.setValueAtTime(0, 100); lo.setValueAtTime(d * 0.62, 96);
        lo.setValueAtTime(d * 0.88, 0); ease(lo, 70);
        // the field itself sinks downward as it goes out
        var blk = comp.layers.addSolid([0, 0, 0], "sink", W, H, 1.0);
        span(blk, d);
        var bo = tg(blk).property("ADBE Opacity");
        bo.setValueAtTime(0, 0); bo.setValueAtTime(d * 0.62, 10); bo.setValueAtTime(d, 100);
        ease(bo, 88);
        return comp;
    }

    function buildTRANS_WIPE(c) {
        var d = c.dur;                                  // 0.6s light wipe
        var comp = proj.items.addComp("FRC_" + c.id, W, H, 1.0, d, FPS);
        comp.motionBlur = true;
        span(comp.layers.addSolid([0, 0, 0], "bg", W, H, 1.0), d);
        // leading soft bloom, then the hard blade, both raked and blurred
        // v001 blew out: a 620px bloom at 55%% ADD plus a 170px blade at 96%%
        // plus a 20%% flash all crossed mid-frame and became one flat beige
        // slab. Everything is narrower, dimmer and staggered so the frame reads
        // as a raking light streak on black, not a wash.
        // A wide solid + blur keeps a FLAT interior and reads as a beige slab,
        // which is what v002 still did. Make the source narrower than the blur
        // radius so the gaussian fully takes over and the profile is a soft
        // falloff with no flat body.
        var soft = comp.layers.addSolid([0.95, 0.86, 0.62], "bloom", 120, Math.round(H * 1.8), 1.0);
        span(soft, d); soft.blendingMode = BlendingMode.ADD; soft.motionBlur = true;
        tg(soft).property("ADBE Rotate Z").setValue(14);
        key2(tg(soft).property("ADBE Position"), 0.02, [-520, H / 2], d - 0.04, [W + 520, H / 2], 30);
        blur(soft, 130);
        var sfo = tg(soft).property("ADBE Opacity");
        sfo.setValueAtTime(0.02, 0); sfo.setValueAtTime(d * 0.45, 34); sfo.setValueAtTime(d - 0.04, 0);
        ease(sfo, 60);
        var blade = comp.layers.addSolid([1, 1, 1], "blade", 60, Math.round(H * 1.8), 1.0);
        span(blade, d); blade.blendingMode = BlendingMode.ADD; blade.motionBlur = true;
        tg(blade).property("ADBE Rotate Z").setValue(14);
        key2(tg(blade).property("ADBE Position"), 0.06, [-360, H / 2], d - 0.02, [W + 360, H / 2], 24);
        blur(blade, 7);
        var bo2 = tg(blade).property("ADBE Opacity");
        bo2.setValueAtTime(0.06, 0); bo2.setValueAtTime(d * 0.5, 78); bo2.setValueAtTime(d - 0.02, 0);
        ease(bo2, 55);
        // brief full-frame lift at the crossing point
        var fl = comp.layers.addSolid([1, 1, 1], "flash", W, H, 1.0);
        span(fl, d); fl.blendingMode = BlendingMode.ADD;
        var fo = tg(fl).property("ADBE Opacity");
        fo.setValueAtTime(d * 0.34, 0); fo.setValueAtTime(d * 0.50, 9); fo.setValueAtTime(d * 0.70, 0);
        ease(fo, 70);
        return comp;
    }

    var BUILDERS = { ACT: buildACT, STAMP: buildSTAMP, STATS: buildSTATS,
                     DOC: buildDOC, TRANS_SINK: buildTRANS_SINK, TRANS_WIPE: buildTRANS_WIPE };

    // ---- build all + queue renders ----
    var rq = proj.renderQueue;
    while (rq.numItems > 0) rq.item(1).remove();
    var built = 0;
    // every card is still BUILT so the .aep stays complete; only these ids get
    // queued, so an approved mp4 is never silently replaced.
    var RENDER_ONLY = %(RENDER_ONLY)s;
    function queued(id) {
        if (!RENDER_ONLY.length) return true;
        for (var q = 0; q < RENDER_ONLY.length; q++) if (RENDER_ONLY[q] === id) return true;
        return false;
    }
    for (var ci = 0; ci < CARDS.length; ci++) {
        var c = CARDS[ci];
        var fn = BUILDERS[c.kind];
        if (!fn) throw new Error("no builder for kind " + c.kind);
        var comp = fn(c);
        built++;
        if (!queued(c.id)) continue;
        var it = rq.items.add(comp);
        try { it.applyTemplate("最良設定"); } catch (e) { try { it.applyTemplate("Best Settings"); } catch (e2) {} }
        var om = it.outputModule(1);
        var omOK = false, omNames = ["H.264 - レンダリング設定を一致 - 15 Mbps",
                                     "H.264 - Match Render Settings - 15 Mbps"];
        for (var oi = 0; oi < omNames.length && !omOK; oi++) {
            try { om.applyTemplate(omNames[oi]); omOK = true; } catch (e3) {}
        }
        om.file = new File(c.out);
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


def ease_out_cubic(p: float) -> float:
    return 1.0 - (1.0 - p) ** 3


def count_keys(num_str: str, t0: float, t1: float, n: int = 16):
    """Hold-keys counting 0 -> the row's numeral, preserving a trailing '%'."""
    pct = num_str.endswith("%")
    target = int(num_str.rstrip("%"))
    suffix = "%" if pct else ""
    keys = [(t0, "0" + suffix)]
    for i in range(1, n):
        p = i / (n - 1)
        keys.append((t0 + (t1 - t0) * p, f"{int(round(target * ease_out_cubic(p)))}{suffix}"))
    keys.append((round(t1 + 0.02, 4), f"{target}{suffix}"))
    return [[round(t, 4), v] for t, v in keys]


def main() -> int:
    render_only = []
    if "--render-only" in sys.argv:
        render_only = sys.argv[sys.argv.index("--render-only") + 1].split(",")
    verify_against_script()
    WORK.mkdir(parents=True, exist_ok=True)
    cards = build_cards()
    # attach count-up keyframes to the four numeric stats rows
    for c in cards:
        if c["kind"] != "STATS":
            continue
        t0s = [0.30, 0.82, 1.34, 1.86]
        for i, row in enumerate(c["rows"][:4]):
            row["numKeys"] = count_keys(row["num"], t0s[i] + 0.55, t0s[i] + 1.35)
    jsx = JSX_TEMPLATE % dict(
        W=W, H=H, FPS=FPS,
        GOLD=", ".join(f"{v:.3f}" for v in GOLD),
        WHITE=", ".join(f"{v:.3f}" for v in WHITE),
        SILVER=", ".join(f"{v:.3f}" for v in SILVER),
        PAPER=", ".join(f"{v:.3f}" for v in PAPER),
        CARDS=json.dumps(cards, ensure_ascii=False),
        RENDER_ONLY=json.dumps(render_only),
        WORK=str(WORK).replace("\\", "/"),
        AEP=str(WORK / "frazier_cards.aep").replace("\\", "/"),
    )
    (WORK / "frazier_cards.jsx").write_text(jsx, encoding="utf-8")
    (WORK / "cards.json").write_text(json.dumps(cards, indent=2, ensure_ascii=False),
                                     encoding="utf-8")
    print(f"[gen] cards: {len(cards)}  total {sum(c['dur'] for c in cards):.1f}s")
    for c in cards:
        detail = c.get("title") or (c.get("ranks") or [""])[0] or c.get("label") or "-"
        print(f"  {c['id']:<16} {c['kind']:<11} dur={c['dur']:.1f}  {detail}")
    print("[gen] jsx ->", WORK / "frazier_cards.jsx")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
