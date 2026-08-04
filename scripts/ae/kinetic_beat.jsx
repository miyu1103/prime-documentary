// Build and render kinetic-typography overlays for MID-ROLL beats of a Short.
//
// Why mid-roll and not the hook: the hook already carries a baked-in cover card with the same
// words, so an overlay there collides with it (measured on short88 frames 1-3). The beat that has
// nothing on screen and deserves emphasis is the number or the turn in the middle - "in 2009 the
// company left", "a debris dump" - where the narration lands a fact and the picture is just a
// plate. One or two hits per Short, never more.
//
// Contract: renders ONLY the type, on transparency. Remotion composites the resulting VP9-alpha
// WebM over the cut at the beat's timestamp, so this stays a reusable part and no Short needs hand
// work in AE.
//
// Job file C:/temp/ae/jobs.json, evaluated (ExtendScript has no JSON object):
//   [{ "id":"short118_a", "style":"number", "seconds":3.6,
//      "big":"2009", "label":"PFIZER LEFT" },
//    { "id":"short118_b", "style":"punch", "seconds":3.0,
//      "words":["A DEBRIS","DUMP"] }]
//
// Safe area, measured on real 1080x1920 Short frames: the brand chip sits at y~135 and the caption
// band at y~1305, so type lives between y 420 and y 1050 and nothing may cross those.
//
// Traps this is written around, all measured on this machine:
//   * app.newProject() HARD-KILLS AfterFX in -noui mode. Use the project AE already has open.
//   * a script failure surfaces only as exit code 1, so everything is logged to a file
//   * GPU acceleration is unstable headless -> forced to software
//   * aerender refuses to overwrite an existing file, so outputs are removed by the runner
//   * app.quit() must always run or the process hangs with no window to close

var LOG = new File("C:/temp/ae/kinetic.log");
function log(m) { LOG.open("a"); LOG.writeln(m); LOG.close(); }

var W = 1080, H = 1920, FPS = 30;
var SAFE_TOP = 420, SAFE_BOT = 1050;

function bez(prop) {
    for (var k = 1; k <= prop.numKeys; k++) {
        prop.setInterpolationTypeAtKey(k, KeyframeInterpolationType.BEZIER,
                                          KeyframeInterpolationType.BEZIER);
    }
}

var MAX_TYPE_W = 960;   // 1080 minus a 60 px margin each side

function mkText(comp, str, size, cx, cy) {
    var tl = comp.layers.addText(str);

    function style(sz) {
        var td = tl.property("Source Text").value;
        td.resetCharStyle();
        td.fontSize = sz;
        try { td.font = "Arial-Black"; } catch (e) { log("font fallback: " + e); }
        td.fillColor = [1, 1, 1];
        td.applyFill = true;
        td.applyStroke = false;
        td.tracking = sz > 160 ? 10 : 0;
        td.justification = ParagraphJustification.CENTER_JUSTIFY;
        tl.property("Source Text").setValue(td);
        return tl.sourceRectAtTime(0, false);
    }

    // Fit to the frame instead of trusting the caller's font size. "STORM DEBRIS" at the size that
    // suited "A DUMP FOR" ran off the right edge of the first render - a per-phrase measurement is
    // the only thing that survives arbitrary copy.
    var r = style(size);
    var guard = 0;
    while (r.width > MAX_TYPE_W && guard++ < 12) {
        size = Math.floor(size * MAX_TYPE_W / r.width);
        r = style(size);
    }
    if (guard) log("  refit '" + str + "' -> " + size + "pt (" + Math.round(r.width) + "px)");

    // Centre the anchor on the type's own bounding box, so a scale punch grows from the middle of
    // the word instead of from the baseline (which reads as the word sliding downward).
    tl.property("Transform").property("Anchor Point").setValue([r.left + r.width / 2,
                                                                r.top + r.height / 2]);
    tl.property("Transform").property("Position").setValue([cx, cy]);
    tl.motionBlur = true;
    tl.__rect = r;
    return tl;
}

function maskReveal(tl, t0, t1) {
    // Mask vertices are in LAYER space, not comp space. The first version used comp coordinates,
    // so the mask sat hundreds of pixels below the glyphs and the label rendered as nothing at all
    // - a bug no exit code reports, only a frame does.
    var r = tl.__rect;
    var x0 = r.left - 60, x1 = r.left + r.width + 60;
    var y0 = r.top - 30, y1 = r.top + r.height + 30;
    var m = tl.Masks.addProperty("Mask");
    var open = new Shape();
    open.vertices = [[x0, y0], [x1, y0], [x1, y1], [x0, y1]];
    open.closed = true;
    var shut = new Shape();
    shut.vertices = [[x0, y1], [x1, y1], [x1, y1], [x0, y1]];
    shut.closed = true;
    var mp = m.property("maskPath");
    mp.setValueAtTime(t0, shut);
    mp.setValueAtTime(t1, open);
}

function mkScrim(comp, cy, halfH, t0) {
    // A soft dark panel behind the type. Plates are not all dark - "A DUMP FOR" landed on a bright
    // sky in the first composite and white-on-pale is unreadable. This is only possible because the
    // overlay carries real alpha; it would be invisible under a screen blend.
    // addSolid rejects a non-integer size outright ("343.44 is not an integer") and takes the whole
    // build down with it, so every derived dimension is rounded before it gets here.
    halfH = Math.round(halfH);
    var s = comp.layers.addSolid([0, 0, 0], "scrim", W, halfH * 2, 1.0);
    s.property("Transform").property("Position").setValue([W / 2, cy]);
    var m = s.Masks.addProperty("Mask");
    var sh = new Shape();
    sh.vertices = [[0, 0], [W, 0], [W, halfH * 2], [0, halfH * 2]];
    sh.closed = true;
    m.property("maskPath").setValue(sh);
    m.property("maskFeather").setValue([180, 180]);
    var o = s.property("Transform").property("Opacity");
    o.setValueAtTime(t0, 0);
    o.setValueAtTime(t0 + 0.24, 52);
    return s;
}

function mkRule(comp, cy, widthPct, t0, t1) {
    var s = comp.layers.addSolid([1, 1, 1], "rule", W, 6, 1.0);
    s.property("Transform").property("Position").setValue([W / 2, cy]);
    var sc = s.property("Transform").property("Scale");
    sc.setValueAtTime(t0, [0, 100]);
    sc.setValueAtTime(t1, [widthPct, 100]);
    bez(sc);
    s.property("Transform").property("Opacity").setValue(85);
    s.motionBlur = true;
    return s;
}

function exitAll(comp, dur) {
    // Everything leaves together, upward, 0.34 s before the overlay ends. Without an exit the type
    // pops off on a hard cut, which is the single thing that makes an overlay look bolted on.
    var t0 = dur - 0.34, t1 = dur - 0.02;
    for (var i = 1; i <= comp.numLayers; i++) {
        var l = comp.layer(i);
        var p = l.property("Transform").property("Position");
        // valueAtTime, not .value: .value reads at comp time 0, where the scrim is still at
        // opacity 0, which made it vanish the instant the exit began.
        var v = p.valueAtTime(t0, false);
        p.setValueAtTime(t0, [v[0], v[1]]);
        p.setValueAtTime(t1, [v[0], v[1] - 34]);
        bez(p);
        var o = l.property("Transform").property("Opacity");
        o.setValueAtTime(t0, o.valueAtTime(t0, false));
        o.setValueAtTime(t1, 0);
    }
}

function styleNumber(comp, job, dur) {
    // The fact is the number. It arrives alone, oversized, with a rule drawn under it, and only
    // then does the label say what the number means - that ordering is what makes it read as a
    // reveal rather than a lower third.
    var big = mkText(comp, job.big, job.bigSize || 260, W / 2, 640);
    var sc = big.property("Transform").property("Scale");
    sc.setValueAtTime(0.00, [122, 122]);
    sc.setValueAtTime(0.34, [100, 100]);
    bez(sc);
    var bo = big.property("Transform").property("Opacity");
    bo.setValueAtTime(0.00, 0);
    bo.setValueAtTime(0.16, 100);

    mkRule(comp, 790, 68, 0.28, 0.62);

    if (job.label) {
        var lab = mkText(comp, job.label, job.labelSize || 84, W / 2, 880);
        var lp = lab.property("Transform").property("Position");
        lp.setValueAtTime(0.34, [W / 2, 880 + 46]);
        lp.setValueAtTime(0.70, [W / 2, 880]);
        bez(lp);
        // A rectangular mask animated open gives the "cut up from behind the line" look and keeps
        // the letters from fading in, which reads as cheap.
        maskReveal(lab, 0.34, 0.70);
    }
    mkScrim(comp, 760, 300, 0.00).moveToEnd();
    exitAll(comp, dur);
}

function stylePunch(comp, job, dur) {
    // A turn in the story, not a number: the words hit one after another, each with a small
    // overshoot, so the phrase lands like it is being said rather than displayed.
    var words = job.words || [];
    var size = job.bigSize || 150;
    var lineH = size * 1.18;
    var top = 700 - (words.length - 1) * lineH / 2;
    for (var i = 0; i < words.length; i++) {
        var cy = top + i * lineH;
        if (cy < SAFE_TOP || cy > SAFE_BOT) log("WARN " + job.id + " line " + i + " y=" + cy);
        var tl = mkText(comp, words[i], size, W / 2, cy);
        var t0 = 0.16 * i;
        var sc = tl.property("Transform").property("Scale");
        sc.setValueAtTime(t0, [74, 74]);
        sc.setValueAtTime(t0 + 0.20, [106, 106]);
        sc.setValueAtTime(t0 + 0.36, [100, 100]);
        bez(sc);
        var o = tl.property("Transform").property("Opacity");
        o.setValueAtTime(t0, 0);
        o.setValueAtTime(t0 + 0.10, 100);
    }
    var lastY = top + (words.length - 1) * lineH;
    mkRule(comp, lastY + size * 0.74, 46, 0.16 * words.length, 0.16 * words.length + 0.30);
    mkScrim(comp, (top + lastY) / 2, (lastY - top) / 2 + size, 0.00).moveToEnd();
    exitAll(comp, dur);
}

function buildComp(job) {
    var dur = job.seconds || 3.2;
    var comp = app.project.items.addComp("KIN_" + job.id, W, H, 1.0, dur, FPS);
    comp.bgColor = [0, 0, 0];
    if (job.style === "punch") stylePunch(comp, job, dur);
    else styleNumber(comp, job, dur);
    comp.motionBlur = true;
    return comp;
}

function main() {
    LOG.open("w"); LOG.writeln("kinetic_beat " + new Date().toString()); LOG.close();
    try { app.beginSuppressDialogs(); } catch (e) {}
    try { app.project.gpuAccelType = GpuAccelType.SOFTWARE; } catch (e) {}

    try {
        var jobFile = new File("C:/temp/ae/jobs.json");
        jobFile.open("r");
        var raw = jobFile.read();
        jobFile.close();
        // ExtendScript has no JSON object - "ReferenceError: JSON is undefined" is what the first
        // run died on. eval on a file this pipeline writes itself is the standard workaround.
        var jobs = eval("(" + raw + ")");
        log("jobs: " + jobs.length);

        var proj = app.project;
        while (proj.renderQueue.numItems > 0) proj.renderQueue.item(1).remove();

        for (var i = 0; i < jobs.length; i++) {
            var comp = buildComp(jobs[i]);
            var rq = proj.renderQueue.items.add(comp);
            rq.applyTemplate("最良設定");
            var om = rq.outputModule(1);
            om.applyTemplate("ロスレス圧縮（アルファ付き）");
            om.file = new File("C:/temp/ae/out/" + jobs[i].id + ".avi");
            log("queued " + jobs[i].id + " " + (jobs[i].style || "number")
                + " " + comp.duration + "s -> " + om.file.fsName);
        }

        proj.save(new File("C:/temp/ae/kinetic.aep"));
        log("project saved with " + proj.renderQueue.numItems + " queue items");
    } catch (e) {
        log("FAILED: " + e.toString() + " @line " + (e.line || "?"));
    }

    try { app.endSuppressDialogs(false); } catch (e) {}
    log("quitting");
    app.quit();
}
main();
