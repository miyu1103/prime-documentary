// Smoke test: can this machine build and save an After Effects project unattended?
//
// Everything is logged, because AfterFX.exe -r reports a script failure only as exit code 1 with
// no message anywhere. That is how the first two runs were diagnosed:
//   run 1: exit 1, no output at all
//   run 2: log stopped exactly after "gpu -> SOFTWARE", i.e. app.newProject() killed the process
//          outright - not an exception, a hard exit. In -noui mode AE already owns an empty
//          project, so asking for a new one is both unnecessary and fatal. Use app.project.
//
// Other traps (memory: reference_after_effects_automation):
//   * a previous force-kill leaves a crash-recovery dialog that blocks EVERY later launch
//   * GPU acceleration is unstable headless, so rendering is forced to software
//   * app.quit() must always run or the process hangs forever with no window

var LOG = new File("C:/temp/ae/smoke.log");

function log(msg) {
    LOG.open("a");
    LOG.writeln(msg);
    LOG.close();
}

function main() {
    LOG.open("w"); LOG.writeln("start " + new Date().toString()); LOG.close();

    try { log("version: " + app.version); } catch (e) {}
    try { app.beginSuppressDialogs(); log("dialogs suppressed"); } catch (e) { log("suppress failed"); }
    try { app.project.gpuAccelType = GpuAccelType.SOFTWARE; log("gpu -> SOFTWARE"); } catch (e) {}

    try {
        // NO app.newProject() - see the header. Work in the project AE already has open.
        var proj = app.project;
        log("using existing project, items=" + proj.numItems);

        var comp = proj.items.addComp("SMOKE", 1080, 1920, 1.0, 2.0, 30);
        log("comp created: " + comp.name + " " + comp.width + "x" + comp.height);

        // a shape that unmistakably moves, so a still frame cannot pass for a render
        var solid = comp.layers.addSolid([1, 1, 1], "bar", 1080, 120, 1.0);
        var pos = solid.property("Transform").property("Position");
        pos.setValueAtTime(0.0, [540, 400]);
        pos.setValueAtTime(2.0, [540, 1520]);
        log("layer + keyframes ok");

        var f = new File("C:/temp/ae/smoke.aep");
        proj.save(f);
        log("SAVED " + f.fsName + " exists=" + f.exists);
    } catch (e) {
        log("FAILED: " + e.toString() + " @line " + (e.line || "?"));
    }

    try { app.endSuppressDialogs(false); } catch (e) {}
    log("quitting");
    app.quit();
}
main();
