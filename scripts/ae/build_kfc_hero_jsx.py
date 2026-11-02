"""EP38 kidsforcash — AE hero-beat JSX generator.

Builds 6 premium After Effects MG "hero" beats (number-ticker data cards) that
OVERWRITE the same time windows in the already-rendered CaseFilm. Each beat is a
self-contained full-frame comp: eased push-in background still + kinetic number
count-up (staggered, motion-blurred) + accent wipe + glow + vignette + light
sweep + narration caption lower-third. Rendered software (no GPU) for stability.

Robustness rules (owner: "破綻しないようにして"):
  - Only KNOWN matchNames + validated template ("最良設定" render settings).
  - Fonts resolved at runtime from app.fonts (no silent substitution).
  - Number strings are FULLY precomputed here (no JS number formatting at render).
  - Comps are 1920x1080 @ 30fps to match casefilm.v001 exactly.
  - Each beat renders independently; a failed beat is simply skipped downstream.

Output: episodes/.../08_edit/ae_hero/kfc_hero.jsx  (+ beats.json for the compositor)
"""
from __future__ import annotations
import json, sys
from pathlib import Path

ROOT = Path(r"C:\Users\aab15\Documents\prime-documentary")
EP = "PD-2026-038-kidsforcash"
EPDIR = ROOT / "episodes" / EP
FILM = ROOT / "remotion" / "src" / "data" / "kidsforcash_film.json"
IMG = EPDIR / "04_scenes" / "generated_images"
WORK = EPDIR / "08_edit" / "ae_hero"
RENDER = WORK / "render"
W, H, FPS = 1920, 1080, 30

# GOLD / WHITE / SILVER / NAVY in 0..1 float (matches CaseFilm brand palette)
GOLD = [0.898, 0.710, 0.227]
WHITE = [0.961, 0.969, 0.980]
SILVER = [0.588, 0.627, 0.682]


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
    """List of (time, string) hold-keys counting 0 -> target with ease-out."""
    keys = [(t0, fmt_number(0, decimals, thousands, prefix, suffix))]
    for i in range(1, n):
        p = i / (n - 1)
        v = target * ease_out_cubic(p)
        keys.append((t0 + (t1 - t0) * p, fmt_number(v, decimals, thousands, prefix, suffix)))
    # settle exactly on target and hold to end
    keys.append((t1 + 0.02, fmt_number(target, decimals, thousands, prefix, suffix)))
    return keys


def nearest_caption(caps, start, end):
    """Single caption line whose center is closest to the window center."""
    c = (start + end) / 2.0
    best, bestd = "", 1e9
    for cap in caps:
        cc = (cap["start"] + cap["end"]) / 2.0
        if cap["start"] < end and cap["end"] > start:
            d = abs(cc - c)
            if d < bestd:
                bestd, best = d, cap["text"]
    return best.strip()


def one_line(text: str, maxchars: int = 50) -> str:
    """Single clean caption line (no newline chars — AE would show them literally)."""
    t = " ".join(text.split())
    if len(t) <= maxchars:
        return t
    cut = t[:maxchars].rsplit(" ", 1)[0].rstrip(",;:—- ")
    return cut + "…"


# ---- the 6 hero beats: (fig#, start, end, still, MG spec) --------------------
# still chosen for strongest theme match (all verified on-disk + eyeballed).
BEATS_SPEC = [
    dict(id="b01", start=23.23, end=29.23, still="S12",
         top="THE HEARING", value=90, decimals=0, thousands=False, prefix="", suffix=" SEC",
         bottom="NO LAWYER"),
    dict(id="b04", start=62.53, end=68.53, still="S02",
         top="FOR A PRANK", value=3, decimals=0, thousands=False, prefix="", suffix=" MONTHS",
         bottom="IN A CELL"),
    dict(id="b05", start=73.53, end=79.03, still="S06",
         top="IN HIS COURT", value=50, decimals=0, thousands=False, prefix="", suffix="%",
         bottom="SENT AWAY"),
    dict(id="b12", start=208.03, end=214.53, still="S16",
         top="TO THE JUDGES", value=2.8, decimals=1, thousands=False, prefix="$", suffix="M",
         bottom="IN KICKBACKS"),
    dict(id="b20", start=369.53, end=375.03, still="S35",
         top="OVERTURNED", value=2251, decimals=0, thousands=True, prefix="", suffix="",
         bottom="CONVICTIONS VACATED"),
    dict(id="b24", start=468.53, end=474.53, still="S05",
         top="MARK CIAVARELLA", value=28, decimals=0, thousands=False, prefix="", suffix=" YEARS",
         bottom="FEDERAL PRISON"),
]


def build_beats():
    film = json.loads(FILM.read_text(encoding="utf-8"))
    caps = film["captions"]
    beats = []
    for s in BEATS_SPEC:
        still = IMG / f"{s['still']}.png"
        if not still.exists():
            print(f"MISSING still {still}", file=sys.stderr); sys.exit(2)
        dur = round(s["end"] - s["start"], 3)
        # timeline (comp-local seconds)
        head, tail = 4.0 / FPS, 4.0 / FPS          # black dip at seams
        t_num0, t_num1 = 0.55, 1.55                 # count-up window
        cnum = count_keys(s["value"], s["decimals"], s["thousands"], s["prefix"], s["suffix"],
                          t_num0, t_num1)
        cap = one_line(nearest_caption(caps, s["start"], s["end"]))
        beats.append(dict(
            id=s["id"], start=s["start"], end=s["end"], dur=dur,
            still=str(still).replace("\\", "/"),
            top=s["top"], bottom=s["bottom"], caption=cap,
            numKeys=[[round(t, 4), v] for t, v in cnum],
            numReveal=t_num0 - 0.1, head=head, tail=tail,
            out=str((RENDER / f"{s['id']}.mp4")).replace("\\", "/"),
        ))
    return beats


JSX_TEMPLATE = r"""// AUTO-GENERATED — EP38 kidsforcash AE hero beats. Do not hand-edit.
(function () {
    var W = %(W)d, H = %(H)d, FPS = %(FPS)d;
    var GOLD = [%(GOLD)s], WHITE = [%(WHITE)s], SILVER = [%(SILVER)s];
    var BEATS = %(BEATS)s;
    var RENDER_DIR = "%(RENDER)s";

    // NOTE: each `AfterFX -noui -r` launch opens a fresh untitled project, so no
    // cross-run accumulation. (app.newProject() hangs headless on the save prompt.)
    var proj = app.project;
    // defensive: remove any pre-existing KFC_* comps if this project was reused
    try { for (var ri = proj.numItems; ri >= 1; ri--) {
        var itx = proj.item(ri);
        if (itx instanceof CompItem && String(itx.name).indexOf("KFC_") === 0) itx.remove();
    } } catch (e) {}
    try { proj.gpuAccelType = GpuAccelType.SOFTWARE; } catch (e) {}
    try { proj.bitsPerChannel = 8; } catch (e) {}
    app.beginUndoGroup("kfc_hero");

    // ---- runtime font resolver (avoid silent substitution) ----
    // FIXED 2026-07-20. The previous version returned the FAMILY NAME on failure
    // ("Anton"), and it always failed: on AE 2026 `app.fonts.allFonts[i]` is NOT a
    // FontObject but an array-like wrapper, so `.familyName` reads undefined and the
    // match never fired. TextDocument.font wants the PostScript name
    // ("Anton-Regular"), so AE silently substituted a default face. Verified against
    // the SHIPPED kidsforcash_final_bgm.v004_ae.mp4: the big numbers render in a wide
    // default sans, not Anton. Resolve via the family+style API and unwrap defensively;
    // a miss must be LOUD, never a fallback to the family string.
    var FONT_REPORT = [];
    function unwrapFont(x) {
        try { if (x && x.postScriptName) return x; } catch (e) {}
        try { if (x && x.length && x[0] && x[0].postScriptName) return x[0]; } catch (e2) {}
        return null;
    }
    function psName(fam, styleContains) {
        var got = null;
        var styles = styleContains
            ? [styleContains, styleContains.charAt(0).toUpperCase() + styleContains.slice(1)]
            : ["Regular"];
        for (var s = 0; s < styles.length && !got; s++) {
            try {
                var m = app.fonts.getFontsByFamilyNameAndStyleName(fam, styles[s]);
                got = unwrapFont(m);
            } catch (e) {}
        }
        if (!got) {  // fallback: linear scan of allFonts, unwrapping each entry
            try {
                var all = app.fonts.allFonts;
                for (var i = 0; i < all.length && !got; i++) {
                    var f = unwrapFont(all[i]);
                    if (f && String(f.familyName).toLowerCase() === fam.toLowerCase()) got = f;
                }
            } catch (e3) {}
        }
        if (!got) {
            throw new Error("FONT NOT FOUND: " + fam + " -- refusing to let AE substitute silently");
        }
        FONT_REPORT.push(fam + "=" + got.postScriptName + "/" + got.styleName);
        return got.postScriptName;
    }
    var FONT_NUM = psName("Anton", "regular");
    var FONT_LBL = psName("Oswald", "medium");

    function ease(prop, inf) {
        inf = inf || 70; var n = prop.numKeys;
        // spatial props (Position) take a 1-D temporal ease (speed); others match value dims
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

    function addText(comp, str, font, size, color, tracking) {
        var L = comp.layers.addText(str);
        var tp = L.property("ADBE Text Properties").property("ADBE Text Document");
        var d = tp.value;
        d.resetCharStyle(); d.font = font; d.fontSize = size; d.fillColor = color;
        d.applyFill = true; d.applyStroke = false; d.tracking = tracking || 0;
        d.justification = ParagraphJustification.CENTER_JUSTIFY;
        tp.setValue(d);
        return L;
    }

    function revealUp(L, t0, y) {
        var p = tg(L).property("ADBE Position");
        key2(p, t0, [W / 2, y + 46], t0 + 0.5, [W / 2, y], 80);
        var o = tg(L).property("ADBE Opacity");
        key2(o, t0, 0, t0 + 0.4, 100, 70);
    }

    function buildBeat(spec) {
        var comp = proj.items.addComp("KFC_" + spec.id, W, H, 1.0, spec.dur, FPS);
        comp.motionBlur = true;

        // L9: black bg
        comp.layers.addSolid([0, 0, 0], "bg", W, H, 1.0);

        // L8: still (fill + eased push-in + slow drift)
        var io = new ImportOptions(new File(spec.still));
        var item = proj.importFile(io);
        var S = comp.layers.add(item);
        var sw = item.width, sh = item.height;
        var fill = Math.max(W / sw, H / sh) * 100;
        var st = tg(S);
        st.property("ADBE Anchor Point").setValue([sw / 2, sh / 2]);
        st.property("ADBE Position").setValue([W / 2, H / 2]);
        var sc = st.property("ADBE Scale");
        key2(sc, 0, [fill, fill], spec.dur, [fill * 1.08, fill * 1.08], 25);
        var sp = st.property("ADBE Position");
        key2(sp, 0, [W / 2 - 18, H / 2 + 10], spec.dur, [W / 2 + 18, H / 2 - 10], 20);

        // L7: cool grade wash (multiply, subtle)
        var grade = comp.layers.addSolid([0.04, 0.07, 0.13], "grade", W, H, 1.0);
        grade.blendingMode = BlendingMode.MULTIPLY;
        grade.property("ADBE Transform Group").property("ADBE Opacity").setValue(38);

        // L6: vignette (black solid, inverted feathered ellipse mask, multiply)
        var vig = comp.layers.addSolid([0, 0, 0], "vignette", W, H, 1.0);
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
        vig.property("ADBE Transform Group").property("ADBE Opacity").setValue(62);

        // L5: glow (warm radial ramp from lower-center, ADD)
        var glow = comp.layers.addSolid([0, 0, 0], "glow", W, H, 1.0);
        var gr = glow.property("ADBE Effect Parade").addProperty("ADBE Ramp");
        gr.property("ADBE Ramp-0001").setValue([W / 2, H * 0.42]);
        gr.property("ADBE Ramp-0002").setValue([GOLD[0], GOLD[1], GOLD[2]]);
        gr.property("ADBE Ramp-0003").setValue([W / 2, H * 0.95]);
        gr.property("ADBE Ramp-0004").setValue([0, 0, 0]);
        gr.property("ADBE Ramp-0005").setValue(2);
        glow.blendingMode = BlendingMode.ADD;
        var go = glow.property("ADBE Transform Group").property("ADBE Opacity");
        go.setValueAtTime(0.0, 0); go.setValueAtTime(0.7, 22); go.setValueAtTime(spec.dur, 14); ease(go, 60);

        // L4: light sweep (bright thin gradient bar, rotated, ADD, sweeps once)
        var sweep = comp.layers.addSolid([1, 1, 1], "sweep", 360, H * 1.6, 1.0);
        sweep.blendingMode = BlendingMode.ADD;
        var swt = tg(sweep);
        swt.property("ADBE Rotate Z").setValue(18);
        swt.property("ADBE Opacity").setValue(16);
        var swp = swt.property("ADBE Position");
        key2(swp, 0.5, [-300, H / 2], 1.25, [W + 300, H / 2], 45);
        var swo = swt.property("ADBE Opacity");
        swo.setValueAtTime(0.5, 0); swo.setValueAtTime(0.7, 18); swo.setValueAtTime(1.25, 0);

        // L3: top label (Oswald, tracked, mask-up reveal) — above the big number
        var topY = H * 0.205;
        var top = addText(comp, spec.top, FONT_LBL, 44, SILVER, 340);
        tg(top).property("ADBE Position").setValue([W / 2, topY]);
        revealUp(top, 0.15, topY);

        // L2b: accent line (gold, scaleX wipe)
        var line = comp.layers.addSolid(GOLD, "accent", 460, 6, 1.0);
        var lt = tg(line);
        lt.property("ADBE Position").setValue([W / 2, H * 0.485]);
        var lsc = lt.property("ADBE Scale");
        line.motionBlur = true;
        key2(lsc, 0.55, [0, 100], 1.05, [100, 100], 90);
        lt.property("ADBE Opacity").setValue(92);

        // L2: big number (Anton, gold, count-up + scale-in overshoot, motion blur)
        var num = addText(comp, spec.numKeys[0][1], FONT_NUM, 250, GOLD, 0);
        num.motionBlur = true;
        tg(num).property("ADBE Position").setValue([W / 2, H * 0.42]);
        var ntp = num.property("ADBE Text Properties").property("ADBE Text Document");
        var doc = ntp.value;
        for (var i = 0; i < spec.numKeys.length; i++) {
            doc.text = String(spec.numKeys[i][1]);
            ntp.setValueAtTime(spec.numKeys[i][0], doc);
        }
        var no = tg(num).property("ADBE Opacity");
        no.setValueAtTime(spec.numReveal, 0); no.setValueAtTime(spec.numReveal + 0.12, 100);
        var nsc = tg(num).property("ADBE Scale");
        nsc.setValueAtTime(0.55, [42, 42]); nsc.setValueAtTime(0.9, [112, 112]); nsc.setValueAtTime(1.2, [100, 100]);
        ease(nsc, 75);

        // L1b: bottom label (Oswald, white, reveal after count)
        var bot = addText(comp, spec.bottom, FONT_LBL, 64, WHITE, 120);
        tg(bot).property("ADBE Position").setValue([W / 2, H * 0.60]);
        revealUp(bot, 1.15, H * 0.60);

        // L1: caption lower-third (dark bar + Oswald text)
        var barY = H * 0.90;
        var bar = comp.layers.addSolid([0.02, 0.04, 0.08], "capbar", W, 130, 1.0);
        tg(bar).property("ADBE Position").setValue([W / 2, barY]);
        var bo = tg(bar).property("ADBE Opacity");
        bo.setValueAtTime(0.2, 0); bo.setValueAtTime(0.5, 64); bo.setValueAtTime(spec.dur - 0.4, 64);
        bo.setValueAtTime(spec.dur - 0.1, 0);
        if (spec.caption && spec.caption.length) {
            var cap = addText(comp, spec.caption, FONT_LBL, 42, WHITE, 20);
            var ctp = cap.property("ADBE Text Properties").property("ADBE Text Document");
            var cd = ctp.value; cd.leading = 50; ctp.setValue(cd);
            tg(cap).property("ADBE Position").setValue([W / 2, barY - 6]);
            var co = tg(cap).property("ADBE Opacity");
            co.setValueAtTime(0.3, 0); co.setValueAtTime(0.6, 100); co.setValueAtTime(spec.dur - 0.4, 100);
            co.setValueAtTime(spec.dur - 0.12, 0);
        }

        // L0: black seam dips (head/tail) — top layer, fades to reveal beat / film
        var dip = comp.layers.addSolid([0, 0, 0], "dip", W, H, 1.0);
        var dop = tg(dip).property("ADBE Opacity");
        dop.setValueAtTime(0, 100); dop.setValueAtTime(spec.head, 0);
        dop.setValueAtTime(spec.dur - spec.tail, 0); dop.setValueAtTime(spec.dur, 100);
        ease(dop, 40);

        return comp;
    }

    // ---- build all + queue renders (default H.264 OM -> writes .mp4) ----
    var rq = proj.renderQueue;
    while (rq.numItems > 0) rq.item(1).remove();
    for (var bi = 0; bi < BEATS.length; bi++) {
        var comp = buildBeat(BEATS[bi]);
        var it = rq.items.add(comp);
        try { it.applyTemplate("最良設定"); } catch (e) { try { it.applyTemplate("Best Settings"); } catch (e2) {} }
        var om = it.outputModule(1);
        var omOK = false, omNames = ["H.264 - レンダリング設定を一致 - 15 Mbps",
                                     "H.264 - Match Render Settings - 15 Mbps"];
        for (var oi = 0; oi < omNames.length && !omOK; oi++) {
            try { om.applyTemplate(omNames[oi]); omOK = true; } catch (e3) {}
        }
        // default OM on this install is already H.264 -> writes .mp4 even if applyTemplate skipped
        om.file = new File(BEATS[bi].out);
    }
    app.project.save(new File("%(AEP)s"));
    app.endUndoGroup();
    // write a completion marker so the driver can confirm the build succeeded
    try {
        var mk = new File("%(RENDER)s/_build_ok.txt");
        mk.open("w"); mk.write("comps=" + proj.numItems + " queue=" + proj.renderQueue.numItems + " fonts=" + FONT_REPORT.join(",")); mk.close();
    } catch (e) {}
    try { app.quit(); } catch (e) {}
})();
"""


def main():
    WORK.mkdir(parents=True, exist_ok=True)
    RENDER.mkdir(parents=True, exist_ok=True)
    beats = build_beats()
    (WORK / "beats.json").write_text(json.dumps(beats, indent=2, ensure_ascii=False), encoding="utf-8")
    jsx = JSX_TEMPLATE % dict(
        W=W, H=H, FPS=FPS,
        GOLD=", ".join(f"{v:.3f}" for v in GOLD),
        WHITE=", ".join(f"{v:.3f}" for v in WHITE),
        SILVER=", ".join(f"{v:.3f}" for v in SILVER),
        BEATS=json.dumps(beats, ensure_ascii=False),
        RENDER=str(RENDER).replace("\\", "/"),
        AEP=str(WORK / "kfc_hero.aep").replace("\\", "/"),
    )
    (WORK / "kfc_hero.jsx").write_text(jsx, encoding="utf-8")
    print("[gen] beats:", len(beats))
    for b in beats:
        print(f"  {b['id']}  {b['start']:.2f}-{b['end']:.2f}  still={Path(b['still']).name}  cap={b['caption'][:40]!r}")
    print("[gen] jsx  ->", WORK / "kfc_hero.jsx")
    print("[gen] beats.json ->", WORK / "beats.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
