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
// KINDS -- all nine ADR-0011 declares. The first four were built 2026-08-26; the last five were
// added 2026-08-27 and are what turns `render_cards.sh`'s by-name refusal from a wall into a gate.
//   hero_number      big + optional label + rule        -- the film's largest fact
//   title_card       big alone                          -- a date or a section title
//   quote_card       a verbatim sentence + attribution  -- wrapped by MEASUREMENT, never by guess
//   list_build       headline + lines arriving in turn  -- e.g. the four counts of an indictment
//   comparison       two columns, a drawn divider       -- value_a vs value_b and their evidence
//   timeline         a drawn spine + staggered nodes    -- two or more sourced moments in order
//   system_map       chained panels + drawn connectors  -- "this, then this, then this"
//   map_move         a marker that TRAVELS to a target  -- a distance, shown as distance
//   document_blowup  a detail frame that magnifies      -- draws NO glyphs inside the frame, ever
//
// document_blowup and the fabricated_record class: the frame's interior is built from abstract
// bars and ticks and the card's meaning is carried by type OUTSIDE the frame. There is no code
// path that puts a character inside the magnifier, so the card cannot render a readable document
// even if an episode's copy asks it to. That is a structural guarantee, not a review step.
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

// ------------------------------------------------------- primitives shared by the five new kinds

function fmtVal(v, prefix, suffix) {
    // A number arrives as a JSON number (JOBS_FORMAT v001: a string arrives on screen as NaN).
    // Thousands separators from 10000 up, because $103078056 is unreadable and $103,078,056 is not.
    if (v === undefined || v === null) return null;
    var s;
    if (typeof v === "number" && v === Math.floor(v) && Math.abs(v) >= 10000) {
        var neg = v < 0, d = String(Math.abs(v)), out = "";
        for (var i = 0; i < d.length; i++) {
            if (i > 0 && (d.length - i) % 3 === 0) out += ",";
            out += d.charAt(i);
        }
        s = (neg ? "-" : "") + out;
    } else {
        s = String(v);
    }
    return (prefix || "") + s + (suffix || "");
}

function enterUp(layer, cx, cy, t0, dy, opTarget) {
    // The house entrance: a rise INTO place, eased, with opacity riding along. Opacity alone is
    // banned -- a card whose type only fades in reads as a slide, not as a film.
    dy = (dy === undefined) ? 40 : dy;
    var p = layer.property("Transform").property("Position");
    p.setValueAtTime(t0, [Math.round(cx), Math.round(cy) + dy]);
    p.setValueAtTime(t0 + 0.34, [Math.round(cx), Math.round(cy)]);
    bez(p);
    var o = layer.property("Transform").property("Opacity");
    o.setValueAtTime(t0, 0);
    o.setValueAtTime(t0 + 0.20, (opTarget === undefined) ? 100 : opTarget);
    return layer;
}

function enterSide(layer, cx, cy, t0, dx, opTarget) {
    // For two-column layouts, where each side arriving from its own edge is what says "two things".
    var p = layer.property("Transform").property("Position");
    p.setValueAtTime(t0, [Math.round(cx) + dx, Math.round(cy)]);
    p.setValueAtTime(t0 + 0.38, [Math.round(cx), Math.round(cy)]);
    bez(p);
    var o = layer.property("Transform").property("Opacity");
    o.setValueAtTime(t0, 0);
    o.setValueAtTime(t0 + 0.20, (opTarget === undefined) ? 100 : opTarget);
    return layer;
}

function punch(layer, t0, from) {
    var sc = layer.property("Transform").property("Scale");
    var f = from || 124;
    sc.setValueAtTime(t0, [f, f]);
    sc.setValueAtTime(t0 + 0.36, [100, 100]);
    bez(sc);
    return layer;
}

function headlineIn(comp, str, y, size, t0) {
    var tl = mkText(comp, str, size, W / 2, y);
    enterUp(tl, W / 2, y, t0, 34);
    maskReveal(tl, t0, t0 + 0.40);
    if (y < SAFE_TOP) log("WARN headline y=" + y + " above safe area");
    return tl;
}

function mkBar(comp, xLeft, cy, w, h, op, name) {
    // Anchored on its own LEFT edge so a scale in x draws the bar rightward from xLeft. addSolid
    // rejects a non-integer size outright, so every dimension is rounded before it gets here.
    w = Math.max(1, Math.round(w));
    h = Math.max(1, Math.round(h));
    var s = comp.layers.addSolid([1, 1, 1], name || "bar", w, h, 1.0);
    s.property("Transform").property("Anchor Point").setValue([0, h / 2]);
    s.property("Transform").property("Position").setValue([Math.round(xLeft), Math.round(cy)]);
    s.property("Transform").property("Opacity").setValue(op === undefined ? 100 : op);
    s.motionBlur = true;
    return s;
}

function growX(layer, t0, t1) {
    var sc = layer.property("Transform").property("Scale");
    sc.setValueAtTime(t0, [0, 100]);
    sc.setValueAtTime(t1, [100, 100]);
    bez(sc);
    return layer;
}

function mkVBar(comp, cx, cy, w, h, op, name) {
    w = Math.max(1, Math.round(w));
    h = Math.max(1, Math.round(h));
    var s = comp.layers.addSolid([1, 1, 1], name || "vbar", w, h, 1.0);
    s.property("Transform").property("Position").setValue([Math.round(cx), Math.round(cy)]);
    s.property("Transform").property("Opacity").setValue(op === undefined ? 100 : op);
    s.motionBlur = true;
    return s;
}

function growY(layer, t0, t1) {
    var sc = layer.property("Transform").property("Scale");
    sc.setValueAtTime(t0, [100, 0]);
    sc.setValueAtTime(t1, [100, 100]);
    bez(sc);
    return layer;
}

function mkPanel(comp, cx, cy, w, h, op, t0) {
    // A dark plate behind ONE node of a chain, so a system map reads as objects rather than as
    // free-floating words. It rises with its own type instead of fading, same rule as the text.
    w = Math.max(1, Math.round(w));
    h = Math.max(1, Math.round(h));
    var s = comp.layers.addSolid([0, 0, 0], "panel", w, h, 1.0);
    var p = s.property("Transform").property("Position");
    p.setValueAtTime(t0, [Math.round(cx), Math.round(cy) + 30]);
    p.setValueAtTime(t0 + 0.34, [Math.round(cx), Math.round(cy)]);
    bez(p);
    var o = s.property("Transform").property("Opacity");
    o.setValueAtTime(t0, 0);
    o.setValueAtTime(t0 + 0.26, (op === undefined) ? 46 : op);
    return s;
}

function mkFrameOutline(comp, cx, cy, w, h, thick) {
    // One layer, two masks: an outer rect ADDed and an inner rect SUBTRACTed leaves an outline.
    // One layer matters -- the whole frame can then be scaled as a group by scaling that layer,
    // with no null and no parenting. Mask vertices are in LAYER space (the trap at the top).
    w = Math.max(4, Math.round(w));
    h = Math.max(4, Math.round(h));
    thick = Math.max(1, Math.round(thick || 6));
    var s = comp.layers.addSolid([1, 1, 1], "frame", w, h, 1.0);
    s.property("Transform").property("Position").setValue([Math.round(cx), Math.round(cy)]);
    var outer = s.Masks.addProperty("Mask");
    var so = new Shape();
    so.vertices = [[0, 0], [w, 0], [w, h], [0, h]];
    so.closed = true;
    outer.property("maskPath").setValue(so);
    var inner = s.Masks.addProperty("Mask");
    var si = new Shape();
    si.vertices = [[thick, thick], [w - thick, thick], [w - thick, h - thick], [thick, h - thick]];
    si.closed = true;
    inner.property("maskPath").setValue(si);
    inner.maskMode = MaskMode.SUBTRACT;
    s.motionBlur = true;
    return s;
}

function centredLines(comp, items, t0, cy, size, lineH, maxW, id) {
    // A short staggered block under a drawing. Not cardList's routine: that one is left-aligned
    // against a tick column because a list of criminal counts is a list. This is a caption block
    // under a diagram, where centring under the thing it describes is what makes it belong to it.
    for (var i = 0; i < items.length; i++) {
        var txt = items[i].t || items[i];
        var y = cy + i * lineH;
        if (y > SAFE_BOT) log("WARN " + id + " caption line " + i + " y=" + y + " below safe area");
        var tl = mkText(comp, txt, size, W / 2, y, maxW);
        enterUp(tl, W / 2, y, t0 + 0.20 * i, 24);
    }
    return cy + (items.length - 1) * lineH;
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

function cardComparison(comp, job, dur) {
    // Two things, side by side, arriving from their own edges with a divider drawn between them.
    // The headline is SPLIT on " / " into the two column labels rather than sat on top: both real
    // orders write it that way ("IN PORT / UNDER WAY"), and a label over its own column is what
    // makes the two numbers a comparison instead of two unrelated facts.
    var parts = (job.headline || "").split(" / ");
    var labA = null, labB = null, topHead = null;
    if (parts.length === 2) { labA = parts[0]; labB = parts[1]; }
    else if (job.headline) { topHead = job.headline; }

    var items = job.lines || [];
    var la = job.linesA, lb = job.linesB;
    if (!la || !lb) {
        var half = Math.ceil(items.length / 2);
        la = items.slice(0, half);
        lb = items.slice(half);
    }

    var sa = fmtVal(job.value_a, job.prefixA || job.prefix, job.suffixA || job.suffix);
    var sb = fmtVal(job.value_b, job.prefixB || job.prefix, job.suffixB || job.suffix);
    // A card whose two sides are on different scales is the defect that ships silently: 43.7
    // (millions) beside 103,078,056 (dollars) under one suffix is a false comparison. Warn with
    // the measured ratio; the fix belongs in the episode's jobs file, not here.
    if (typeof job.value_a === "number" && typeof job.value_b === "number"
        && !job.suffixA && !job.suffixB && job.value_a > 0 && job.value_b > 0) {
        var r = job.value_b / job.value_a;
        if (r < 1) r = 1 / r;
        if (r > 1000) log("WARN " + job.id + " comparison sides differ by " + Math.round(r)
                          + "x under one suffix -- check both are on the same scale");
    }

    var dy = topHead ? 56 : 0;
    var yLab = 250 + dy, yNum = 424 + dy, yLine0 = 582 + dy;
    var colW = 780, cxA = 496, cxB = 1424, lineH = 54;
    if (topHead) headlineIn(comp, topHead, 194, 58, 0.00);

    var maxRows = Math.max(la.length, lb.length);
    var cols = [{lab: labA, val: sa, rows: la, cx: cxA, dx: -70, t: 0.16},
                {lab: labB, val: sb, rows: lb, cx: cxB, dx: 70, t: 0.30}];
    for (var c = 0; c < cols.length; c++) {
        var col = cols[c];
        if (col.lab) {
            var lt = mkText(comp, col.lab, 54, col.cx, yLab, colW);
            enterSide(lt, col.cx, yLab, col.t, col.dx);
        }
        if (col.val) {
            var nt = mkText(comp, col.val, 132, col.cx, yNum, colW);
            enterSide(nt, col.cx, yNum, col.t + 0.14, col.dx);
            punch(nt, col.t + 0.14);
        }
        for (var i = 0; i < col.rows.length; i++) {
            var y = yLine0 + i * lineH;
            if (y > SAFE_BOT) log("WARN " + job.id + " column line " + i + " y=" + y);
            var rt = mkText(comp, col.rows[i].t || col.rows[i], 38, col.cx, y, colW);
            enterUp(rt, col.cx, y, col.t + 0.46 + 0.20 * i, 22);
        }
    }

    var top = yLab - 66, bot = yLine0 + Math.max(0, maxRows - 1) * lineH + 42;
    growY(mkVBar(comp, W / 2, (top + bot) / 2, 4, bot - top, 70), 0.10, 0.58);
    mkScrim(comp, (top + bot) / 2, (bot - top) / 2 + 150, 0.00).moveToEnd();
    exitAll(comp, dur);
}

function cardTimeline(comp, job, dur) {
    // A drawn spine with its moments hung under it in order. The spine draws left to right BEFORE
    // any node appears, so the eye has somewhere to put them; the nodes then land in sequence,
    // which is the whole point of a timeline over a list.
    var items = job.lines || [];
    var n = Math.max(1, items.length);
    headlineIn(comp, job.headline, 214, 62, 0.00);

    var hasVal = (job.value !== undefined && job.value !== null);
    if (hasVal) {
        var bigStr = fmtVal(job.value, job.prefix, job.suffix);
        var big = mkText(comp, bigStr, 150, W / 2, 396);
        enterUp(big, W / 2, 396, 0.26, 30);
        punch(big, 0.26, 118);
    }
    var spineY = hasVal ? 588 : 496;
    var x0 = 210, x1 = 1710, span = x1 - x0;
    growX(mkBar(comp, x0, spineY, span, 5, 40, "spine"), 0.22, 0.78);

    var nodeW = Math.floor(span / n) - 40;
    for (var i = 0; i < n; i++) {
        var cx = Math.round(x0 + span * (i + 0.5) / n);
        var t0 = 0.62 + 0.46 * i;
        // dot on the spine, then a stem down to its own words -- the node is attached to the line,
        // not merely near it
        var dot = mkVBar(comp, cx, spineY, 22, 22, 100, "node");
        punch(dot, t0, 10);
        var od = dot.property("Transform").property("Opacity");
        od.setValueAtTime(t0, 0);
        od.setValueAtTime(t0 + 0.10, 100);
        var stem = mkVBar(comp, cx, spineY + 34, 3, 44, 65, "stem");
        growY(stem, t0 + 0.10, t0 + 0.34);

        var blk = fitBlock(comp, items[i].t || items[i], 46, nodeW, 2);
        var lh = Math.round(blk.size * 1.24);
        for (var k = 0; k < blk.lines.length; k++) {
            var y = spineY + 82 + k * lh;
            if (y > SAFE_BOT) log("WARN " + job.id + " node " + i + " line " + k + " y=" + y);
            var tl = mkText(comp, blk.lines[k], blk.size, cx, y, nodeW);
            enterUp(tl, cx, y, t0 + 0.16 + 0.08 * k, 26);
        }
    }
    mkScrim(comp, (214 + spineY + 120) / 2, (spineY + 120 - 214) / 2 + 170, 0.00).moveToEnd();
    exitAll(comp, dur);
}

function cardSystemMap(comp, job, dur) {
    // "This, then this, then this." Each stage is a panel that rises with its own words, and the
    // CONNECTOR between two stages draws only after the earlier one has landed -- so the card
    // performs the sequence rather than presenting a finished diagram.
    var items = job.lines || [];
    var n = Math.max(1, items.length);
    var head = headlineIn(comp, job.headline, 200, 58, 0.00);
    mkRule(comp, 200 + head.__rect.height / 2 + 36, 30, 0.16, 0.48);

    // boxH was 300 and the gutter 44 on the first cut. In the QC frame the top edge rules sat 150
    // px above their own words and read as three underlines of nothing, and the 44 px connectors
    // were so short the verifier reported the connector zone EMPTY. 216 puts the edge rule just
    // above the type it heads; 72 makes the connector a link you can see.
    var xa = 130, span = 1660, gutter = 72;
    var boxW = Math.floor((span - gutter * (n - 1)) / n);
    // 216 with the block centred on boxY put a four-line node's first line hard against the edge
    // rule. 250, with the block centred 18 px low, leaves ~60 px of headroom under the rule for
    // the tallest node the fitter will produce (four lines) and still reads as one row of panels.
    var boxH = 250, boxY = 480, textY = boxY + 18;
    for (var i = 0; i < n; i++) {
        var cx = Math.round(xa + boxW / 2 + i * (boxW + gutter));
        var t0 = 0.40 + 0.62 * i;
        mkPanel(comp, cx, boxY, boxW, boxH, 46, t0);
        growX(mkBar(comp, cx - boxW / 2, boxY - boxH / 2, boxW, 5, 90, "edge"), t0 + 0.10, t0 + 0.40);

        var blk = fitBlock(comp, items[i].t || items[i], 42, boxW - 60, 4);
        var lh = Math.round(blk.size * 1.28);
        var top = textY - (blk.lines.length - 1) * lh / 2;
        for (var k = 0; k < blk.lines.length; k++) {
            var y = Math.round(top + k * lh);
            var tl = mkText(comp, blk.lines[k], blk.size, cx, y, boxW - 60);
            enterUp(tl, cx, y, t0 + 0.12 + 0.07 * k, 26);
        }
        if (i < n - 1) {
            growX(mkBar(comp, cx + boxW / 2, boxY, gutter, 6, 80, "connector"),
                  t0 + 0.42, t0 + 0.62);
        }
    }

    var bot = boxY + boxH / 2;
    if (job.attribution) {
        // KB-406 is the United States' account to a grand jury, not a finding. The attribution is
        // not decoration: without it the panels state a design promise as established fact.
        var attY = bot + 62;
        var att = mkText(comp, job.attribution, 42, W / 2, attY);
        enterUp(att, W / 2, attY, 0.40 + 0.62 * n, 22);
        if (attY > SAFE_BOT) log("WARN " + job.id + " attribution y=" + attY + " below safe area");
        bot = attY;
    }
    mkScrim(comp, (200 + bot) / 2, (bot - 200) / 2 + 150, 0.00).moveToEnd();
    exitAll(comp, dur);
}

function cardMapMove(comp, job, dur) {
    // A distance shown as a distance. A marker leaves its start and TRAVELS toward the target on
    // an eased move with motion blur, and only when it stops does the bracket close between the
    // two -- so the number lands on a gap the viewer has just watched shrink.
    headlineIn(comp, job.headline, 200, 58, 0.00);
    // 150 pt at y 372 put the number's descenders into the target's deck in the QC frame. 130 at
    // 340 clears it with room, and the number is still the largest thing on the card.
    var bigStr = fmtVal(job.value, job.prefix, job.suffix);
    if (bigStr) {
        var big = mkText(comp, bigStr, 130, W / 2, 340);
        enterUp(big, W / 2, 340, 1.62, 30);
        punch(big, 1.62, 118);
    }

    var trackY = 560, xStart = 240, xStop = 1180, xTarget = 1616;
    growX(mkBar(comp, 150, trackY, 1620, 6, 26, "track"), 0.16, 0.66);

    // The target: a deck carried on an upright that stands ON the track, not through it. The
    // first cut ran the upright from 95 px above the line to 95 below and it read as a T with the
    // water crossing it. Abstract on purpose -- a recognisable structure would be a depiction
    // (invariant 11), and this card's own `forbid` bars stating a length.
    var post = mkVBar(comp, xTarget, trackY - 50, 8, 100, 90, "target");
    growY(post, 0.34, 0.62);
    var deck = mkBar(comp, xTarget - 130, trackY - 98, 260, 10, 95, "deck");
    growX(deck, 0.44, 0.70);

    // the mover
    var ship = mkVBar(comp, xStart, trackY, 150, 40, 100, "mover");
    var so = ship.property("Transform").property("Opacity");
    so.setValueAtTime(0.46, 0);
    so.setValueAtTime(0.62, 100);
    var sp = ship.property("Transform").property("Position");
    sp.setValueAtTime(0.46, [xStart - 90, trackY]);
    sp.setValueAtTime(0.66, [xStart, trackY]);
    sp.setValueAtTime(1.86, [xStop, trackY]);
    bez(sp);
    ship.motionBlur = true;

    // The gap, bracketed only after the move stops. gapR lands ON the upright rather than 8 px
    // short of it, where the tick and the post read as two marks fighting for the same edge.
    var gapL = xStop + 78, gapR = xTarget, gapY = 648;
    growX(mkBar(comp, gapL, gapY, gapR - gapL, 4, 85, "gap"), 1.92, 2.20);
    growY(mkVBar(comp, gapL, gapY, 4, 30, 85, "tick"), 1.92, 2.10);
    growY(mkVBar(comp, gapR, gapY, 4, 30, 85, "tick"), 2.06, 2.24);

    var bot = 648;
    if (job.lines && job.lines.length) {
        bot = centredLines(comp, job.lines, 2.20, 720, 42, 56, 1500, job.id);
    }
    mkScrim(comp, (200 + bot) / 2, (bot - 200) / 2 + 150, 0.00).moveToEnd();
    exitAll(comp, dur);
}

function cardDocBlowup(comp, job, dur) {
    // A magnification, not a document. The frame starts small and off-centre and eases up to full
    // size; inside it are ABSTRACT bars, one of which is picked out by calipers. Nothing that can
    // be read is ever drawn inside the frame -- see the header note on fabricated_record.
    headlineIn(comp, job.headline, 206, 58, 0.00);

    var fx = 960, fy = 424, fw = 940, fh = 300;
    var frame = mkFrameOutline(comp, fx, fy, fw, fh, 6);
    var fp = frame.property("Transform").property("Position");
    fp.setValueAtTime(0.00, [fx - 130, fy + 62]);
    fp.setValueAtTime(0.62, [fx, fy]);
    bez(fp);
    var fs = frame.property("Transform").property("Scale");
    fs.setValueAtTime(0.00, [34, 34]);
    fs.setValueAtTime(0.62, [100, 100]);
    bez(fs);
    var fo = frame.property("Transform").property("Opacity");
    fo.setValueAtTime(0.00, 0);
    fo.setValueAtTime(0.18, 100);

    var barX = fx - fw / 2 + 40;
    var widths = [640, 540, 700, 470, 600];
    var barY0 = fy - 72;
    for (var i = 0; i < widths.length; i++) {
        growX(mkBar(comp, barX, barY0 + i * 36, widths[i], 16, 44, "detail"),
              0.66 + 0.12 * i, 0.92 + 0.12 * i);
    }

    // the thing being pointed at: a bright segment ON the third bar, then its calipers
    var hlX = barX + 170, hlW = 240, hlY = barY0 + 2 * 36;
    var hl = mkVBar(comp, hlX + hlW / 2, hlY, hlW, 22, 100, "detail_focus");
    punch(hl, 1.30, 150);
    var ho = hl.property("Transform").property("Opacity");
    ho.setValueAtTime(1.30, 0);
    ho.setValueAtTime(1.44, 100);
    growY(mkVBar(comp, hlX, hlY, 4, 56, 90, "caliper"), 1.44, 1.60);
    growY(mkVBar(comp, hlX + hlW, hlY, 4, 56, 90, "caliper"), 1.52, 1.68);

    var bot = fy + fh / 2;
    if (job.lines && job.lines.length) {
        bot = centredLines(comp, job.lines, 1.62, 648, 40, 58, 1560, job.id);
    }
    mkScrim(comp, (206 + bot) / 2, (bot - 206) / 2 + 150, 0.00).moveToEnd();
    exitAll(comp, dur);
}

function buildComp(job) {
    var dur = job.seconds || 6.0;
    var comp = app.project.items.addComp("CARD_" + job.id, W, H, 1.0, dur, FPS);
    comp.bgColor = [0, 0, 0];
    var k = job.kind || "hero_number";
    // Dispatch BY NAME, with no catch-all. The old `else cardHeroNumber` meant an unrecognised
    // kind drew a hero number out of whatever fields happened to be present -- a wrong card that
    // renders is worse than no card, because nothing downstream can tell. An unknown kind now
    // writes FAILED, which render_cards.sh reads and refuses to render on.
    if (k === "hero_number" || k === "title_card") cardHeroNumber(comp, job, dur);
    else if (k === "quote_card") cardQuote(comp, job, dur);
    else if (k === "list_build") cardList(comp, job, dur);
    else if (k === "comparison") cardComparison(comp, job, dur);
    else if (k === "timeline") cardTimeline(comp, job, dur);
    else if (k === "system_map") cardSystemMap(comp, job, dur);
    else if (k === "map_move") cardMapMove(comp, job, dur);
    else if (k === "document_blowup") cardDocBlowup(comp, job, dur);
    else throw new Error("no card for kind '" + k + "' (job " + job.id + ")");
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
