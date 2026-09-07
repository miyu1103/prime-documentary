// EP38 AE HERO composite: Codex still (2.5D push) + free dust overlay (Add) + kinetic Anton/Oswald card.
// Build -> save -> quit. Render via aerender. 48fps.
(function () {
    var SCRATCH = "C:\\Users\\aab15\\AppData\\Local\\Temp\\claude\\C--Users-aab15\\a9b4b9f9-07d0-4491-8600-2bd16f67f924\\scratchpad\\";
    var STILL = "H:\\pd-media\\assets\\ai\\kidsforcash\\S07.png";
    var DUST  = "H:\\pd-media\\assets\\factory\\particle_assets\\AF-PART-0049__dust_particles_floating.mp4";
    var AEP = SCRATCH + "ae_hero.aep";
    var OUT = SCRATCH + "ae_hero_out.mp4";
    var log = ""; function w(s){ log += s + "\n"; }
    function ease(prop){ var a=new KeyframeEase(0,70),b=new KeyframeEase(0,70);
        for (var i=1;i<=prop.numKeys;i++){ try{
            if (prop.value instanceof Array && prop.value.length>1){ var d=prop.value.length,x=[],y=[];
                for(var k=0;k<d;k++){x.push(a);y.push(b);} prop.setTemporalEaseAtKey(i,x,y);
            } else prop.setTemporalEaseAtKey(i,[a],[b]);
        }catch(e){} } }
    function setFont(td, name){ try{ td.font = name; return true; }catch(e){ return false; } }
    try {
        app.newProject(); var proj=app.project; proj.bitsPerChannel=16;
        var comp = proj.items.addComp("HeroComp", 1920, 1080, 1.0, 5.0, 48);
        var GOLD=[229/255,181/255,58/255], WHITE=[245/255,247/255,250/255];

        // ---- Layer: Codex still (bottom), 2.5D push ----
        var still = comp.layers.add(proj.importFile(new ImportOptions(new File(STILL))));
        var st=still.property("ADBE Transform Group");
        st.property("ADBE Scale").setValueAtTime(0,[110,110]);
        st.property("ADBE Scale").setValueAtTime(5,[124,124]); ease(st.property("ADBE Scale"));
        st.property("ADBE Position").setValueAtTime(0,[960+40,540+20]);
        st.property("ADBE Position").setValueAtTime(5,[960-40,540-25]); ease(st.property("ADBE Position"));
        still.quality=LayerQuality.BEST; still.motionBlur=true;

        // ---- Layer: free dust overlay, ADD blend, drifting ----
        var dust = comp.layers.add(proj.importFile(new ImportOptions(new File(DUST))));
        dust.blendingMode = BlendingMode.ADD;
        var dt=dust.property("ADBE Transform Group");
        dt.property("ADBE Opacity").setValue(70);
        dt.property("ADBE Scale").setValueAtTime(0,[112,112]);
        dt.property("ADBE Scale").setValueAtTime(5,[120,120]); ease(dt.property("ADBE Scale"));
        dt.property("ADBE Position").setValueAtTime(0,[930,540]);
        dt.property("ADBE Position").setValueAtTime(5,[990,520]); ease(dt.property("ADBE Position"));
        try { dust.timeRemapEnabled=false; } catch(e){}
        dust.quality=LayerQuality.BEST;

        // ---- Layer: Anton number "$2.8 MILLION" ----
        var t=comp.layers.addText("$2.8 MILLION");
        var td=t.property("ADBE Text Properties").property("ADBE Text Document").value;
        td.resetCharStyle(); td.fontSize=185; td.fillColor=GOLD; td.applyFill=true; td.applyStroke=false;
        td.justification=ParagraphJustification.CENTER_JUSTIFY;
        var f1=setFont(td,"Anton")||setFont(td,"Anton-Regular"); w("Anton set: "+f1);
        t.property("ADBE Text Properties").property("ADBE Text Document").setValue(td);
        var tt=t.property("ADBE Transform Group");
        tt.property("ADBE Position").setValueAtTime(0,[960,600]); tt.property("ADBE Position").setValueAtTime(0.7,[960,505]); ease(tt.property("ADBE Position"));
        tt.property("ADBE Scale").setValueAtTime(0,[90,90]); tt.property("ADBE Scale").setValueAtTime(0.7,[100,100]); tt.property("ADBE Scale").setValueAtTime(5,[101.5,101.5]); ease(tt.property("ADBE Scale"));
        tt.property("ADBE Opacity").setValueAtTime(0,0); tt.property("ADBE Opacity").setValueAtTime(0.55,100); ease(tt.property("ADBE Opacity"));
        t.motionBlur=true; t.quality=LayerQuality.BEST;
        try{ var sh=t.property("ADBE Effect Parade").addProperty("ADBE Drop Shadow"); sh.property(2).setValue(220); sh.property(5).setValue(16); }catch(e){}

        // ---- Layer: Oswald label "IN KICKBACKS" ----
        var s=comp.layers.addText("IN KICKBACKS");
        var sd=s.property("ADBE Text Properties").property("ADBE Text Document").value;
        sd.resetCharStyle(); sd.fontSize=60; sd.fillColor=WHITE; sd.applyFill=true; sd.applyStroke=false; sd.tracking=200;
        sd.justification=ParagraphJustification.CENTER_JUSTIFY;
        var f2=setFont(sd,"Oswald")||setFont(sd,"Oswald-Regular"); w("Oswald set: "+f2);
        s.property("ADBE Text Properties").property("ADBE Text Document").setValue(sd);
        var stt=s.property("ADBE Transform Group");
        stt.property("ADBE Position").setValueAtTime(0,[960,640]); stt.property("ADBE Position").setValueAtTime(1,[960,620]); ease(stt.property("ADBE Position"));
        stt.property("ADBE Opacity").setValueAtTime(0.5,0); stt.property("ADBE Opacity").setValueAtTime(1.1,100); ease(stt.property("ADBE Opacity"));
        s.motionBlur=true; s.quality=LayerQuality.BEST;

        // ---- Layer: gold underline wipe ----
        var bar=comp.layers.addSolid(GOLD,"UNDER",520,7,1.0);
        bar.property("ADBE Transform Group").property("ADBE Anchor Point").setValue([-260,3.5]);
        bar.property("ADBE Transform Group").property("ADBE Position").setValue([700,690]);
        var bs=bar.property("ADBE Transform Group").property("ADBE Scale");
        bs.setValueAtTime(0.4,[0,100]); bs.setValueAtTime(1.0,[100,100]); ease(bs);

        // ---- render queue H.264 ----
        var rq=app.project.renderQueue.items.add(comp); var om=rq.outputModule(1); var pick="";
        for(var u=0;u<om.templates.length;u++){ if(om.templates[u].indexOf("H.264")!==-1 && om.templates[u].indexOf("15")!==-1){pick=om.templates[u];break;} }
        if(!pick) for(var u2=0;u2<om.templates.length;u2++){ if(om.templates[u2].indexOf("H.264")!==-1){pick=om.templates[u2];break;} }
        if(pick){ try{ om.applyTemplate(pick); }catch(e){} }
        om.file=new File(OUT);
        app.project.save(new File(AEP)); w("saved. DONE_BUILD_OK");
    } catch(e){ w("BUILD_ERROR: "+e.toString()); }
    var lf=new File(SCRATCH+"ae_hero_log.txt"); lf.open("w"); lf.write(log); lf.close();
    app.quit();
})();
