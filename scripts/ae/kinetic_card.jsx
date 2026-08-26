// Build and render kinetic cards for LONG-FORM episodes, 1920x1080, on transparency.
//
// WHY THIS IS NOT AN EDIT TO kinetic_beat.jsx (invariant 14: no second implementation without
// proving why the existing path cannot be extended)
// ------------------------------------------------------------------------------------------
// `kinetic_beat.jsx` is the Shorts path and it works: it has shipped overlays and it carries
// five headless-AE traps that were each found by a dead render, not by an exit code. It is
// also 1080x1920 with every layout constant measured against a vertical frame -- the brand chip
// at y~135 and the caption band at y~1305 are what put the type between 420 and 1050. A
// long-form card is 1920x1080, the caption band is somewhere else entirely, and the card
// vocabulary is different (a four-count list, a verbatim DOJ sentence). Parameterising the
// vertical file would put the proven Shorts path one typo away from breaking on every render.
// So: same traps, same primitives, different frame. If a third frame size ever appears, THAT is
// the moment to extract a shared library -- not before.
//
// KINDS (the four the episode order books ask for that are buildable from type alone):
//   hero_number   big + optional label + rule        -- the film's largest fact
//   title_card    big alone                          -- a date or a section title
//   quote_card    a verbatim sentence + attribution  -- wrapped by MEASUREMENT, never by guess
//   list_build    headline + lines arriving in turn  -- e.g. the four counts of an indictment
//
// Job file C:/temp/ae/jobs.json, evaluated (ExtendScript has no JSON object):
//   [{"id":"keybridge_ae001","kind":"hero_number","seconds":8,
//     "big":"01:27:53","bigSize":260,"label":"THE ORDER TO STOP THE TRAFFIC"},
//    {"id":"keybridge_ae013","kind":"quote_card","seconds":10,
//     "quote":"An indictment is merely an accusation...","attribution":"U.S. DEPARTMENT OF JUSTICE"},
//    {"id":"keybridge_ae010","kind":"list_build","seconds":10,
//     "headline":"WHAT THE INDICTMENT CHARGES","lines":[{"t":"CONSPIRACY..."}, ...]}]
//
// Safe area for 1920x1080 in this channel's CaseFilm: the caption band and the lower-third sit
// in the bottom quarter, so type lives between y 150 and y 820 and nothing may cross those.
//
// Traps this is written around, all measured on this machine (carried over verbatim):
//   * app.newProject() HARD-KILLS AfterFX in -noui mode. Use the project AE already has open.
//   * a script failure surfaces only as exit code 1, so everything is logged to a file
//   * GPU acceleration is unstable headless -> forced to software
//   * aerender refuses to overwrite an existing file, so outputs are removed by the runner
//   * app.quit() must always run or the process hangs with no window to close
//   * addSolid rejects a non-integer size and takes the whole build down -> round every dimension
//   * mask vertices are in LAYER space, not comp space

var LOG = new File("C:/temp/ae/kinetic.log");
function log(m) { LOG.open("a"); LOG.writeln(m); LOG.close(); }

var W = 1920, H = 1080, FPS = 30;
var SAFE_TOP = 150, SAFE_BOT = 820;
var MAX_TYPE_W = 1640;          // 1920 minus a 140 px margin each side

function bez(prop) {
    for (var k = 1; k <= prop.numKeys; k++) {
        prop.setInterpolationTypeAtKey(k, KeyframeInterpolationType.BEZIER,
                                          KeyframeInterpolationType.BEZIER);
    }
}

function styleText(tl, sz, just) {
    var td = tl.property("Source Text").value;
    td.resetCharStyle();
    td.fontSize = sz;
    try { td.font = "Arial-Black"; } catch (e) { log("font fallback: " + e); }
    td.fillColor = [1, 1, 1];
    td.applyFill = true;
    td.applyStroke = false;
    td.tracking = sz > 160 ? 10 : 0;
    td.justification = just || ParagraphJustification.CENTER_JUSTIFY;
    tl.property("Source Text").setValue(td);
    return tl.sourceRectAtTime(0, false);
}

function mkText(comp, str, size, cx, cy, maxW, just) {
    // Fit to the frame instead of trusting the caller's font size. A size that suited one phrase
    // runs off the edge on the next; a per-phrase measurement is the only thing that survives
    // arbitrary copy.
    maxW = maxW || MAX_TYPE_W;
    var tl = comp.layers.addText(str);
    var r = styleText(tl, size, just);
    var guard = 0;
    while (r.width > maxW && guard++ < 12) {
        size = Math.floor(size * maxW / r.width);
        r = styleText(tl, size, just);
    }
    if (guard) log("  refit '" + str + "' -> " + size + "pt (" + Math.round(r.width) + "px)");

    // Centre the anchor on the type's own bounding box so a scale punch grows from the middle of
    // the word instead of from the baseline (which reads as the word sliding downward).
    tl.property("Transform").property("Anchor Point").setValue([r.left + r.width / 2,
                                                                r.top + r.height / 2]);
    tl.property("Transform").property("Position").setValue([cx, cy]);
    tl.motionBlur = true;
    tl.__rect = r;
    tl.__size = size;
    return tl;
}

function measureWidth(comp, str, size) {
    var probe = comp.layers.addText(str);
    styleText(probe, size);
    var w = probe.sourceRectAtTime(0, false).width;
    probe.remove();
    return w;
}

function wrapLines(comp, str, size, maxW) {
    // Wrap by MEASURING, not by counting characters. "An indictment is merely an accusation."
    // and "OBSTRUCTION OF AN AGENCY PROCEEDING" have similar character counts and very
    // different widths in Arial Black.
    var words = str.split(" ");
    var lines = [], cur = "";
    for (var i = 0; i < words.length; i++) {
        var probe = cur ? cur + " " + words[i] : words[i];
        if (cur && measureWidth(comp, probe, size) > maxW) {
            lines.push(cur);
            cur = words[i];
        } else {
            cur = probe;
        }
    }
    if (cur) lines.push(cur);
    return lines;
}

function fitBlock(comp, str, startSize, maxW, maxLines) {
    // Shrink until the sentence fits in maxLines. A verbatim quote may not be truncated
    // (KB-501: "IN FULL ... never paraphrase, never truncate"), so the type gives way, not the text.
    var size = startSize, lines = wrapLines(comp, str, size, maxW), guard = 0;
    while (lines.length > maxLines && guard++ < 14) {
        size = Math.floor(size * 0.92);
        lines = wrapLines(comp, str, size, maxW);
    }
    if (guard) log("  block refit -> " + size + "pt, " + lines.length + " line(s)");
    return {size: size, lines: lines};
}

function maskReveal(tl, t0, t1) {
    // Mask vertices are in LAYER space, not comp space. A comp-space version put the mask
    // hundreds of pixels below the glyphs and the label rendered as nothing at all -- a bug no
    // exit code reports, only a frame does.
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
    // A soft dark panel behind the type. Plates are not all dark and white-on-pale is
    // unreadable. Only possible because the overlay carries real alpha; it would be invisible
    // under a screen blend. addSolid rejects a non-integer size outright and takes the whole
    // build down, so every derived dimension is rounded before it gets here.
    halfH = Math.round(halfH);
    var s = comp.layers.addSolid([0, 0, 0], "scrim", W, halfH * 2, 1.0);
    s.property("Transform").property("Position").setValue([W / 2, Math.round(cy)]);
    var m = s.Masks.addProperty("Mask");
    var sh = new Shape();
    sh.vertices = [[0, 0], [W, 0], [W, halfH * 2], [0, halfH * 2]];
    sh.closed = true;
    m.property("maskPath").setValue(sh);
    m.property("maskFeather").setValue([220, 220]);
    var o = s.property("Transform").property("Opacity");
    o.setValueAtTime(t0, 0);
    o.setValueAtTime(t0 + 0.24, 52);
    return s;
}

function mkRule(comp, cy, widthPct, t0, t1) {
    var s = comp.layers.addSolid([1, 1, 1], "rule", W, 6, 1.0);
    s.property("Transform").property("Position").setValue([W / 2, Math.round(cy)]);
    var sc = s.property("Transform").property("Scale");
    sc.setValueAtTime(t0, [0, 100]);
    sc.setValueAtTime(t1, [widthPct, 100]);
    bez(sc);
    s.property("Transform").property("Opacity").setValue(85);
    s.motionBlur = true;
    return s;
}

function exitAll(comp, dur) {
    // Everything leaves together, upward, 0.34 s before the overlay ends. Without an exit the
    // type pops off on a hard cut, which is the single thing that makes an overlay look bolted on.
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

// ---------------------------------------------------------------------------- card kinds

function cardHeroNumber(comp, job, dur) {
    // The fact is the number. It arrives alone, oversized, with a rule drawn under it, and only
    // then does the label say what the number means -- that ordering is what makes it read as a
    // reveal rather than a lower third.
    var hasLabel = !!job.label;
    var numY = hasLabel ? 430 : 520;
    var big = mkText(comp, job.big || job.headline, job.bigSize || 260, W / 2, numY);
    var sc = big.property("Transform").property("Scale");
    sc.setValueAtTime(0.00, [122, 122]);
    sc.setValueAtTime(0.34, [100, 100]);
    bez(sc);
    var bo = big.property("Transform").property("Opacity");
    bo.setValueAtTime(0.00, 0);
    bo.setValueAtTime(0.16, 100);

    var ruleY = numY + big.__rect.height / 2 + 60;
    mkRule(comp, ruleY, 46, 0.28, 0.62);

    if (hasLabel) {
        var labY = ruleY + 84;
        var lab = mkText(comp, job.label, job.labelSize || 70, W / 2, labY);
        var lp = lab.property("Transform").property("Position");
        lp.setValueAtTime(0.34, [W / 2, labY + 46]);
        lp.setValueAtTime(0.70, [W / 2, labY]);
        bez(lp);
        // A rectangular mask animated open gives the "cut up from behind the line" look and keeps
        // the letters from fading in, which reads as cheap.
        maskReveal(lab, 0.34, 0.70);
        if (labY > SAFE_BOT) log("WARN " + job.id + " label y=" + labY + " below safe area");
    }
    mkScrim(comp, numY + 60, 300, 0.00).moveToEnd();
    exitAll(comp, dur);
}

function cardQuote(comp, job, dur) {
    // A verbatim sentence. It may not be shortened, so when it is long the TYPE gives way: the
    // block is refit until it fits in five lines. Lines arrive in sequence, not all at once, so
    // the viewer reads at the pace the narration is speaking.
    var blk = fitBlock(comp, job.quote, 76, MAX_TYPE_W, 5);
    var lineH = Math.round(blk.size * 1.30);
    var top = 470 - (blk.lines.length - 1) * lineH / 2;
    for (var i = 0; i < blk.lines.length; i++) {
        var cy = top + i * lineH;
        if (cy < SAFE_TOP || cy > SAFE_BOT) log("WARN " + job.id + " quote line " + i + " y=" + cy);
        var tl = mkText(comp, blk.lines[i], blk.size, W / 2, cy);
        var t0 = 0.13 * i;
        var o = tl.property("Transform").property("Opacity");
        o.setValueAtTime(t0, 0);
        o.setValueAtTime(t0 + 0.22, 100);
        var p = tl.property("Transform").property("Position");
        p.setValueAtTime(t0, [W / 2, cy + 26]);
        p.setValueAtTime(t0 + 0.34, [W / 2, cy]);
        bez(p);
    }
    var lastY = top + (blk.lines.length - 1) * lineH;
    var tIn = 0.13 * blk.lines.length;
    mkRule(comp, lastY + lineH * 0.72, 26, tIn, tIn + 0.30);

    if (job.attribution) {
        var attY = lastY + lineH * 0.72 + 62;
        var att = mkText(comp, job.attribution, 46, W / 2, attY);
        att.property("Transform").property("Opacity").setValueAtTime(tIn + 0.20, 0);
        att.property("Transform").property("Opacity").setValueAtTime(tIn + 0.55, 100);
        if (attY > SAFE_BOT) log("WARN " + job.id + " attribution y=" + attY + " below safe area");
    }
    mkScrim(comp, (top + lastY) / 2 + 40, (lastY - top) / 2 + 200, 0.00).moveToEnd();
    exitAll(comp, dur);
}

function cardList(comp, job, dur) {
    // A headline and its items, arriving one at a time. LEFT-ALIGNED against a common margin,
    // because the first cut put centred items beside left-hand ticks and the two rows of ragged
    // text read as unrelated to their own markers. A list of criminal counts is a list, not a
    // decoration: the items line up.
    var items = job.lines || [];
    var head = mkText(comp, job.headline, 62, W / 2, 250);
    var ho = head.property("Transform").property("Opacity");
    ho.setValueAtTime(0.00, 0);
    ho.setValueAtTime(0.20, 100);
    mkRule(comp, 250 + head.__rect.height / 2 + 40, 34, 0.16, 0.46);

    // One size for every item: fitting each on its own leaves a four-word count larger than a
    // ten-word count, which reads as a mistake rather than a hierarchy.
    var size = 54, guard = 0;
    var itemW = MAX_TYPE_W - 120;
    for (var i = 0; i < items.length; i++) {
        while (measureWidth(comp, items[i].t || items[i], size) > itemW && guard++ < 20) {
            size = Math.floor(size * 0.94);
        }
    }
    // Measure the widest item ONCE, then place every item's left edge at the same x. A per-item
    // centre would put each line at its own left edge, which is the fault this replaces.
    var widest = 0;
    for (var m = 0; m < items.length; m++) {
        var wpx = measureWidth(comp, items[m].t || items[m], size);
        if (wpx > widest) widest = wpx;
    }
    var TICK_W = 34, TICK_GAP = 44;
    var blockW = TICK_W + TICK_GAP + widest;
    var xLeft = Math.round((W - blockW) / 2);          // the whole block is centred, its rows are not
    var xText = xLeft + TICK_W + TICK_GAP;
    var xTick = xLeft + TICK_W / 2;

    // Centre the rows in what is left under the headline rather than starting at a fixed y, so a
    // three-item list does not sit in the top third with the bottom half of the frame empty.
    var lineH = Math.round(size * 1.85);
    var blockH = (items.length - 1) * lineH;
    var top = Math.round(560 - blockH / 2);
    for (var j = 0; j < items.length; j++) {
        var txt = items[j].t || items[j];
        var cy = top + j * lineH;
        if (cy > SAFE_BOT) log("WARN " + job.id + " list line " + j + " y=" + cy);
        var tl = mkText(comp, txt, size, 0, cy, itemW, ParagraphJustification.LEFT_JUSTIFY);
        // LEFT_JUSTIFY still anchors on the measured box, so the layer is moved by its own left
        // edge: position.x = xText + (anchor.x - rect.left).
        var ax = tl.__rect.left + tl.__rect.width / 2;
        var px = xText + (ax - tl.__rect.left);
        tl.property("Transform").property("Position").setValue([px, cy]);
        var t0 = 0.34 + 0.42 * j;
        var o = tl.property("Transform").property("Opacity");
        o.setValueAtTime(t0, 0);
        o.setValueAtTime(t0 + 0.18, 100);
        var p = tl.property("Transform").property("Position");
        p.setValueAtTime(t0, [px + 40, cy]);
        p.setValueAtTime(t0 + 0.34, [px, cy]);
        bez(p);
        // a short tick at the block's own left margin, drawn as its item arrives
        var tick = comp.layers.addSolid([1, 1, 1], "tick", TICK_W, 5, 1.0);
        tick.property("Transform").property("Position").setValue([xTick, Math.round(cy)]);
        var ts = tick.property("Transform").property("Scale");
        ts.setValueAtTime(t0, [0, 100]);
        ts.setValueAtTime(t0 + 0.22, [100, 100]);
        bez(ts);
        tick.property("Transform").property("Opacity").setValue(80);
    }
    var lastY = top + blockH;
    mkScrim(comp, (250 + lastY) / 2, (lastY - 250) / 2 + 160, 0.00).moveToEnd();
    exitAll(comp, dur);
}

function buildComp(job) {
    var dur = job.seconds || 6.0;
    var comp = app.project.items.addComp("CARD_" + job.id, W, H, 1.0, dur, FPS);
    comp.bgColor = [0, 0, 0];
    var k = job.kind || "hero_number";
    if (k === "quote_card") cardQuote(comp, job, dur);
    else if (k === "list_build") cardList(comp, job, dur);
    else cardHeroNumber(comp, job, dur);       // hero_number and title_card share the layout
    comp.motionBlur = true;
    return comp;
}

function main() {
    LOG.open("w"); LOG.writeln("kinetic_card " + new Date().toString()); LOG.close();
    try { app.beginSuppressDialogs(); } catch (e) {}
    try { app.project.gpuAccelType = GpuAccelType.SOFTWARE; } catch (e) {}

    try {
        var jobFile = new File("C:/temp/ae/jobs.json");
        jobFile.open("r");
        var raw = jobFile.read();
        jobFile.close();
        // ExtendScript has no JSON object -- "ReferenceError: JSON is undefined" is what the
        // first run of the Shorts path died on. eval on a file this pipeline writes itself is
        // the standard workaround.
        var jobs = eval("(" + raw + ")");
        log("jobs: " + jobs.length);

        var proj = app.project;
        while (proj.renderQueue.numItems > 0) proj.renderQueue.item(1).remove();

        var built = 0;
        for (var i = 0; i < jobs.length; i++) {
            var comp = buildComp(jobs[i]);
            var rq = proj.renderQueue.items.add(comp);
            rq.applyTemplate("最良設定");
            var om = rq.outputModule(1);
            om.applyTemplate("ロスレス圧縮（アルファ付き）");
            om.file = new File("C:/temp/ae/out/" + jobs[i].id + ".avi");
            built++;
            log("queued " + jobs[i].id + " " + (jobs[i].kind || "hero_number")
                + " " + comp.duration + "s -> " + om.file.fsName);
        }
        if (built !== jobs.length) log("FAILED: built " + built + " of " + jobs.length);

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
