// What output-module templates does this install actually have?
//
// Guessing the name is how aerender jobs fail after the comp is already built: applyTemplate on a
// name that does not exist throws, the script dies, and the only symptom is exit code 1. The
// overlays this pipeline needs must carry an ALPHA channel, so the answer decides the whole
// approach - ProRes 4444, a PNG sequence, or something else entirely.

var LOG = new File("C:/temp/ae/templates.log");
function log(m) { LOG.open("a"); LOG.writeln(m); LOG.close(); }

function main() {
    LOG.open("w"); LOG.writeln("probe " + new Date().toString()); LOG.close();
    try { app.beginSuppressDialogs(); } catch (e) {}
    try {
        var proj = app.project;
        var comp = proj.items.addComp("PROBE", 320, 320, 1.0, 1.0, 30);
        var rq = proj.renderQueue.items.add(comp);
        var om = rq.outputModule(1);

        log("--- OUTPUT MODULE TEMPLATES ---");
        var t = om.templates;
        for (var i = 0; i < t.length; i++) log("  " + t[i]);

        log("--- RENDER SETTINGS TEMPLATES ---");
        var rs = rq.templates;
        for (var j = 0; j < rs.length; j++) log("  " + rs[j]);

        rq.remove();
        comp.remove();
    } catch (e) {
        log("FAILED: " + e.toString());
    }
    try { app.endSuppressDialogs(false); } catch (e) {}
    app.quit();
}
main();
