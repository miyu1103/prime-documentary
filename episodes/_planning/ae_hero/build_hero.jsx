// Generic EP38 "Kids for Cash" AE HERO composite builder.
// Reads $.global.HCFG from scratch\hero_config.jsx, builds comp, saves .aep, queues H.264, logs, quits.
(function () {
    var SCRATCH = "C:\\Users\\aab15\\AppData\\Local\\Temp\\claude\\C--Users-aab15\\a9b4b9f9-07d0-4491-8600-2bd16f67f924\\scratchpad\\";
    var log = ""; function w(s){ log += s + "\n"; }
    function writeLog(){ var lf=new File(SCRATCH+"hero_build_log.txt"); lf.open("w"); lf.write(log); lf.close(); }
    try { $.evalFile(new File(SCRATCH + "hero_config.jsx")); } catch(e){ w("CONFIG_EVAL_ERROR: "+e.toString()); writeLog(); app.quit(); return; }
    var C = $.global.HCFG;
    if (!C){ w("NO_CONFIG"); writeLog(); app.quit(); return; }

    var GOLD=[229/255,181/255,58/255], WHITE=[245/255,247/255,250/255], NAVY=[11/255,26/255,43/255];
    function colorOf(n){ if(n==="gold")return GOLD; if(n==="white")return WHITE; if(n==="navy")return NAVY; return WHITE; }

    // eased keyframes on all keys of a property (no linear)
    function ease(prop, inf, outf){ inf = inf||70; outf = outf||70;
        var a=new KeyframeEase(0,inf), b=new KeyframeEase(0,outf);
        for (var i=1;i<=prop.numKeys;i++){ try{
            if (prop.value instanceof Array && prop.value.length>1){ var d=prop.value.length,x=[],y=[];
                for(var k=0;k<d;k++){x.push(a);y.push(b);} prop.setTemporalEaseAtKey(i,x,y);
            } else prop.setTemporalEaseAtKey(i,[a],[b]);
        }catch(e){} } }
    function setFont(td, name){ try{ td.font = name; return true; }catch(e){ return false; } }
    function dropShadow(layer, dist, soft, opac){ try{ var sh=layer.property("ADBE Effect Parade").addProperty("ADBE Drop Shadow");
        sh.property("ADBE Drop Shadow-0002").setValue(opac||210); // opacity
        sh.property("ADBE Drop Shadow-0004").setValue(dist||14);  // distance
        sh.property("ADBE Drop Shadow-0005").setValue(soft||36);  // softness
    }catch(e){ w("shadow_err:"+e.toString()); } }

    try {
        app.newProject(); var proj=app.project; proj.bitsPerChannel=16;
        var DUR = C.duration || 5.0;
        var comp = proj.items.addComp("HeroComp", 1920, 1080, 1.0, DUR, 30);

        // ---- Layer: Codex still (bottom), 2.5D push ----
        var still = comp.layers.add(proj.importFile(new ImportOptions(new File(C.still))));
        var st=still.property("ADBE Transform Group");
        var s0 = C.stillScale0 || 112, s1 = C.stillScale1 || 126;
        st.property("ADBE Scale").setValueAtTime(0,[s0,s0]);
        st.property("ADBE Scale").setValueAtTime(DUR,[s1,s1]); ease(st.property("ADBE Scale"));
        var px = C.pushX || 40, py = C.pushY || 22;
        st.property("ADBE Position").setValueAtTime(0,[960+px,540+py]);
        st.property("ADBE Position").setValueAtTime(DUR,[960-px,540-py]); ease(st.property("ADBE Position"));
        still.quality=LayerQuality.BEST; still.motionBlur=true;
        w("still ok: "+C.still);

        // ---- Optional overlay video (dust / light leak), ADD blend, drift ----
        if (C.overlay){
            var ov = comp.layers.add(proj.importFile(new ImportOptions(new File(C.overlay))));
            ov.blendingMode = BlendingMode.ADD;
            var ot=ov.property("ADBE Transform Group");
            ot.property("ADBE Opacity").setValue(C.overlayOpacity || 60);
            ot.property("ADBE Scale").setValueAtTime(0,[112,112]);
            ot.property("ADBE Scale").setValueAtTime(DUR,[122,122]); ease(ot.property("ADBE Scale"));
            ot.property("ADBE Position").setValueAtTime(0,[930,540]);
            ot.property("ADBE Position").setValueAtTime(DUR,[990,520]); ease(ot.property("ADBE Position"));
            try { ov.timeRemapEnabled=false; } catch(e){}
            ov.quality=LayerQuality.BEST;
            w("overlay ok: "+C.overlay);
        }

        // ---- Optional tint / darken scrim (navy solid) above image, below text ----
        if (C.tint && C.tint > 0){
            var scrim = comp.layers.addSolid(NAVY, "SCRIM", 1920, 1080, 1.0);
            scrim.property("ADBE Transform Group").property("ADBE Opacity").setValue(C.tint);
            w("tint "+C.tint);
        }

        // ---- Text layers ----
        var texts = C.texts || [];
        for (var ti=0; ti<texts.length; ti++){
            var cf = texts[ti];
            var t=comp.layers.addText(cf.text);
            var td=t.property("ADBE Text Properties").property("ADBE Text Document").value;
            td.resetCharStyle(); td.fontSize=cf.size; td.fillColor=colorOf(cf.color); td.applyFill=true; td.applyStroke=false;
            if (cf.tracking) td.tracking=cf.tracking;
            td.justification=ParagraphJustification.CENTER_JUSTIFY;
            var fam = cf.font || "Anton";
            var fok = setFont(td, fam) || setFont(td, fam+"-Regular");
            w("font "+fam+" set:"+fok);
            t.property("ADBE Text Properties").property("ADBE Text Document").setValue(td);
            var tt=t.property("ADBE Transform Group");
            var X = cf.x!=null?cf.x:960, Y = cf.y!=null?cf.y:540, d = cf.delay || 0;
            var anim = cf.anim || "riseIn";

            if (anim === "punchIn"){
                tt.property("ADBE Position").setValue([X,Y]);
                var sc=tt.property("ADBE Scale");
                sc.setValueAtTime(d,[136,136]); sc.setValueAtTime(d+0.24,[97,97]); sc.setValueAtTime(d+0.40,[100,100]); sc.setValueAtTime(DUR,[101.5,101.5]); ease(sc);
                var op=tt.property("ADBE Opacity");
                op.setValueAtTime(d,0); op.setValueAtTime(d+0.12,100); ease(op);
            } else if (anim === "stampIn"){
                if (cf.rotate) tt.property("ADBE Rotation").setValue(cf.rotate);
                tt.property("ADBE Position").setValue([X,Y]);
                var sc2=tt.property("ADBE Scale");
                sc2.setValueAtTime(d,[240,240]); sc2.setValueAtTime(d+0.16,[92,92]); sc2.setValueAtTime(d+0.30,[100,100]); ease(sc2);
                var op2=tt.property("ADBE Opacity");
                op2.setValueAtTime(d,0); op2.setValueAtTime(d+0.09,100); ease(op2);
            } else { // riseIn (default) — position rise + scale + opacity (mask-cut feel)
                var rise = cf.rise!=null?cf.rise:95;
                var pp=tt.property("ADBE Position");
                pp.setValueAtTime(d,[X,Y+rise]); pp.setValueAtTime(d+0.55,[X,Y]); pp.setValueAtTime(DUR,[X,Y]); ease(pp);
                var sc3=tt.property("ADBE Scale");
                sc3.setValueAtTime(d,[95,95]); sc3.setValueAtTime(d+0.55,[100,100]); ease(sc3);
                var op3=tt.property("ADBE Opacity");
                op3.setValueAtTime(d,0); op3.setValueAtTime(d+0.40,100); ease(op3);
            }
            t.motionBlur=true; t.quality=LayerQuality.BEST;
            dropShadow(t, 14, 40, 220);
            w("text ok: "+cf.text);
        }

        // ---- Optional gold underline wipe ----
        if (C.underline){
            var uw = C.underline.width || 560, ux = C.underline.x!=null?C.underline.x:960, uy = C.underline.y!=null?C.underline.y:660, ud = C.underline.delay||0.5;
            var bar=comp.layers.addSolid(GOLD,"UNDER",uw,7,1.0);
            bar.property("ADBE Transform Group").property("ADBE Anchor Point").setValue([-uw/2,3.5]);
            bar.property("ADBE Transform Group").property("ADBE Position").setValue([ux-uw/2,uy]);
            var bs=bar.property("ADBE Transform Group").property("ADBE Scale");
            bs.setValueAtTime(ud,[0,100]); bs.setValueAtTime(ud+0.55,[100,100]); ease(bs);
            w("underline ok");
        }

        // ---- Optional stamp border box (shape layer, stroke only) ----
        if (C.stampBox){
            try{
                var bx = C.stampBox;
                var sl = comp.layers.addShape(); sl.name="STAMPBOX";
                var grp = sl.property("ADBE Root Vectors Group").addProperty("ADBE Vector Group");
                var cont = grp.property("ADBE Vectors Group");
                var rect = cont.addProperty("ADBE Vector Shape - Rect");
                rect.property("ADBE Vector Rect Size").setValue([bx.w, bx.h]);
                rect.property("ADBE Vector Rect Roundness").setValue(0);
                var stroke = cont.addProperty("ADBE Vector Graphic - Stroke");
                stroke.property("ADBE Vector Stroke Color").setValue(GOLD);
                stroke.property("ADBE Vector Stroke Width").setValue(bx.stroke||8);
                var slt = sl.property("ADBE Transform Group");
                slt.property("ADBE Position").setValue([bx.x, bx.y]);
                if (bx.rotate) slt.property("ADBE Rotation").setValue(bx.rotate);
                var sd = bx.delay||0;
                var slsc = slt.property("ADBE Scale");
                slsc.setValueAtTime(sd,[240,240]); slsc.setValueAtTime(sd+0.16,[92,92]); slsc.setValueAtTime(sd+0.30,[100,100]); ease(slsc);
                var slop = slt.property("ADBE Opacity");
                slop.setValueAtTime(sd,0); slop.setValueAtTime(sd+0.09,100); ease(slop);
                sl.motionBlur=true;
                w("stampbox ok");
            }catch(e){ w("stampbox_err:"+e.toString()); }
        }

        comp.motionBlur = true;

        // ---- render queue H.264 ----
        var rq=app.project.renderQueue.items.add(comp); var om=rq.outputModule(1); var pick="";
        var tpl = om.templates;
        for(var u=0;u<tpl.length;u++){ if(tpl[u].indexOf("H.264")!==-1 && tpl[u].indexOf("15")!==-1){pick=tpl[u];break;} }
        if(!pick) for(var u2=0;u2<tpl.length;u2++){ if(tpl[u2].indexOf("H.264")!==-1){pick=tpl[u2];break;} }
        w("om template pick: "+pick);
        if(pick){ try{ om.applyTemplate(pick); }catch(e){ w("apply_tpl_err:"+e.toString()); } }
        om.file=new File(C.out);
        app.project.save(new File(C.aep));
        w("saved aep: "+C.aep);
        w("DONE_BUILD_OK");
    } catch(e){ w("BUILD_ERROR: "+e.toString()); }
    writeLog();
    app.quit();
})();
