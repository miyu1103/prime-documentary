// Build and render a kinetic-typography overlay for one Short's hook line.
//
// Why After Effects and not Remotion: Remotion already does the 2.5D depth moves and the cutting.
// What it does not do cheaply is per-character typography with real motion blur and per-word
// timing. That is the thing the owner keeps describing as missing ("アニメがまた少ない"), and it is
// the one job AE is unambiguously better at.
//
// Contract: this renders ONLY the text, on transparency. Remotion composites it over the hook cut,
// so the overlay is a reusable part and the automated pipeline stays automated - no per-Short
// hand work in AE.
//
// Reads a job file (JSON) so one AE launch can render many overlays; launching AE costs ~25 s.
//   [{ "id": "short182", "words": ["A SCHOOL SEARCH", "CAN TURN", "ILLEGAL"], "seconds": 3.2 }]
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

function buildComp(job) {
    var proj = app.project;
    var dur = job.seconds || 3.0;
    var comp = proj.items.addComp("KIN_" + job.id, W, H, 1.0, dur, FPS);
    comp.bgColor = [0, 0, 0];

    var words = job.words || [];
    // Stack the phrases in the upper third: the caption band sits low and the Shorts UI eats the
    // bottom ~470 px, so anything below ~1400 is unreadable in the app.
    var lineH = 150;
    var top = 300;

    for (var i = 0; i < words.length; i++) {
        var tl = comp.layers.addText(words[i]);
        var td = tl.property("Source Text").value;
        td.resetCharStyle();
        td.fontSize = 104;
        td.font = "Arial-Black";
        td.fillColor = [1, 1, 1];
        td.applyFill = true;
        td.applyStroke = false;
        td.justification = ParagraphJustification.LEFT_JUSTIFY;
        tl.property("Source Text").setValue(td);

        tl.property("Transform").property("Position").setValue([90, top + i * lineH]);

        // Per-phrase entrance, staggered. A wipe from below plus a short slide reads as one
        // movement rather than two, and it is the same grammar as the mask-reveal used elsewhere
        // in the channel's titles.
        var t0 = 0.18 * i;
        var t1 = t0 + 0.42;

        var pos = tl.property("Transform").property("Position");
        pos.setValueAtTime(t0, [90, top + i * lineH + 46]);
        pos.setValueAtTime(t1, [90, top + i * lineH]);
        for (var k = 1; k <= pos.numKeys; k++) {
            pos.setInterpolationTypeAtKey(k, KeyframeInterpolationType.BEZIER,
                                             KeyframeInterpolationType.BEZIER);
        }

        var op = tl.property("Transform").property("Opacity");
        op.setValueAtTime(t0, 0);
        op.setValueAtTime(t0 + 0.20, 100);

        // A rectangular mask animated open gives the "cut up from behind the line" look and keeps
        // the letters from fading in, which reads as cheap.
        var m = tl.Masks.addProperty("Mask");
        var shape = new Shape();
        shape.vertices = [[0, -130], [W, -130], [W, 40], [0, 40]];
        shape.closed = true;
        var mp = m.property("maskPath");
        var closed = new Shape();
        closed.vertices = [[0, 40], [W, 40], [W, 40], [0, 40]];
        closed.closed = true;
        mp.setValueAtTime(t0, closed);
        mp.setValueAtTime(t1, shape);

        tl.motionBlur = true;
    }

    comp.motionBlur = true;
    return comp;
}

function main() {
    LOG.open("w"); LOG.writeln("kinetic " + new Date().toString()); LOG.close();
    try { app.beginSuppressDialogs(); } catch (e) {}
    try { app.project.gpuAccelType = GpuAccelType.SOFTWARE; } catch (e) {}

    try {
        var jobFile = new File("C:/temp/ae/jobs.json");
        jobFile.open("r");
        var raw = jobFile.read();
        jobFile.close();
        // ExtendScript has no JSON object - "ReferenceError: JSON is undefined" is what the first
        // run died on. eval on a file this pipeline writes itself is safe and is the standard
        // workaround; the alternative is shipping a JSON polyfill for one call.
        var jobs = eval("(" + raw + ")");
        log("jobs: " + jobs.length);

        var proj = app.project;
        for (var i = 0; i < jobs.length; i++) {
            var comp = buildComp(jobs[i]);
            var rq = proj.renderQueue.items.add(comp);
            rq.applyTemplate("最良設定");
            var om = rq.outputModule(1);
            om.applyTemplate("ロスレス圧縮（アルファ付き）");
            om.file = new File("C:/temp/ae/out/" + jobs[i].id + "_hook.avi");
            log("queued " + jobs[i].id + " -> " + om.file.fsName);
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
