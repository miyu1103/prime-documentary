"""EP50 rebuild Stage 1b: 40 MORE diverse SDXL people/faces (P37-76) to raise face frequency
without heavy reuse. Varied ages/backgrounds/roles for 1989 NYC + the case. Generic anonymized
(NOT the real Five). Max quality 4K."""
import base64, io, json, urllib.request, sys
from pathlib import Path
from PIL import Image
API="http://127.0.0.1:7860"; JUGG="juggernautXL_ragnarokBy.safetensors [dd08fa32f9]"
OUT=Path(r"E:/pd-media/assets/ai/centralpark"); PUB=Path(r"C:/Users/aab15/Documents/prime-documentary/remotion/public/centralpark/img")
GRADE=("cinematic documentary film still, 1989 New York City, moody low-key lighting, muted cool "
       "teal-and-amber grade, 35mm film grain, shallow depth of field, photoreal, candid, natural skin, high detail")
NEG=("skin blemishes, scars, facial scars, spots, moles, acne, blotchy skin, wrinkled leathery skin, skin lesions, red marks, over-detailed pores, cartoon, illustration, cgi, plastic skin, deformed, extra fingers, mutated hands, bad anatomy, "
     "text, watermark, logo, modern smartphone, modern car, bright saturated")
PEOPLE=[
 ("P37","a worried teenage girl in a 1989 school jacket looking off-camera, close-up, dim hallway"),
 ("P38","an older Latino man in a work shirt sitting on a tenement stoop at dusk, medium, tired"),
 ("P39","a young public defender woman in her late 20s carrying case files down a courthouse hall, medium"),
 ("P40","a veteran homicide detective in his 50s with a moustache, hard face, close-up, precinct at night"),
 ("P41","a Black teenage boy from behind (face hidden) sitting alone in a holding cell, cold light"),
 ("P42","a middle-aged juror in a plain shirt listening intently in a jury box, close-up, courtroom"),
 ("P43","a grandmother in a headscarf praying with rosary beads, close-up, soft candlelight"),
 ("P44","a tough beat cop in a 1989 NYPD uniform standing on a street corner, medium, overcast"),
 ("P45","a young mother holding a toddler on her hip outside a housing project, medium, worried"),
 ("P46","a courtroom bailiff in uniform standing by a door, medium shot, wood-paneled room"),
 ("P47","a nervous witness in a cheap suit on the stand, close-up, harsh courtroom light"),
 ("P48","an exhausted night-shift nurse in scrubs in a hospital corridor, medium, fluorescent"),
 ("P49","a defense attorney in his 40s loosening his tie in frustration, close-up, office"),
 ("P50","a crowd of angry protesters at a night rally, faces lit by candles, medium wide"),
 ("P51","a young Black man in a graduation gown years later, hopeful, close-up, warm light"),
 ("P52","an elderly white judge removing his glasses, weary, close-up, dim chambers"),
 ("P53","a female TV reporter holding a 1989 microphone speaking to camera, medium, flash-lit"),
 ("P54","a father in a diner booth staring at a cold coffee, close-up, warm window light"),
 ("P55","two teenage boys walking a Harlem street at dusk seen from behind, wide, summer"),
 ("P56","a stern prosecutor in a power suit addressing the court, low angle medium, courtroom"),
 ("P57","a weeping woman being comforted by a friend outside a courthouse, medium, evening"),
 ("P58","a prison inmate in the visiting room pressing a hand to the glass, silhouette, cold light"),
 ("P59","a forensic DNA scientist in 2002 examining a printout, close-up, blue lab light"),
 ("P60","a middle-aged Black woman community activist speaking at a podium, close-up, determined"),
 ("P61","a tired court clerk stamping documents, close-up hands and face, dim office"),
 ("P62","a young man in a hoodie looking down under a streetlight at night, close-up, rain"),
 ("P63","an old man reading a newspaper on a park bench, medium, autumn light, face visible"),
 ("P64","a police sketch artist concentrating, over the shoulder, medium, precinct"),
 ("P65","a diverse family sitting together in a courtroom gallery, medium wide, tense"),
 ("P66","a female defense investigator examining a corkboard of photos, medium, dim room"),
 ("P67","a subway busker with a guitar in a 1989 station, medium, gritty, warm"),
 ("P68","a distraught teenage boy crying, face in hands, close-up, dark interrogation room"),
 ("P69","a stoic corrections officer unlocking a cell gate, medium, cold blue block"),
 ("P70","a group of reporters shouting questions with raised recorders, medium wide, flashes"),
 ("P71","a middle-aged man in a 1989 business suit hailing a cab in the rain, medium, night"),
 ("P72","a young woman lighting a candle at a vigil, close-up, warm glow on her face"),
 ("P73","an older detective and a young detective conferring over a desk, medium, precinct"),
 ("P74","a man in his 40s in a modern 2002 suit at a press conference, relieved, close-up, warm"),
 ("P75","a teenage boy staring out a barred cell window at daylight, silhouette, hopeful"),
 ("P76","a diverse crowd of everyday 1989 New Yorkers crossing a busy street, wide, candid"),
]
def post(p,pl):
    r=urllib.request.Request(f"{API}{p}",data=json.dumps(pl).encode(),headers={"Content-Type":"application/json"})
    with urllib.request.urlopen(r,timeout=1200) as x: return json.loads(x.read().decode())
post("/sdapi/v1/options",{"sd_model_checkpoint":JUGG})
made=0
for i,(pid,desc) in enumerate(PEOPLE):
    outp=OUT/f"{pid}.png"
    if outp.exists() and outp.stat().st_size>200000 and Image.open(outp).height>=2000:
        print(f"skip {pid}",flush=True); continue
    pl={"prompt":f"{desc}, {GRADE}","negative_prompt":NEG,"steps":34,"cfg_scale":6.0,
        "width":1536,"height":864,"sampler_name":"DPM++ 2M Karras","seed":52000+i,
        "enable_hr":True,"denoising_strength":0.22,"hr_resize_x":3072,"hr_resize_y":1728,
        "hr_upscaler":"Latent","hr_second_pass_steps":16,"override_settings":{"sd_model_checkpoint":JUGG}}
    d=post("/sdapi/v1/txt2img",pl)
    up={"image":d["images"][0],"upscaling_resize_w":3840,"upscaling_resize_h":2160,"upscaling_crop":True,"upscaler_1":"R-ESRGAN 4x+","resize_mode":1}
    ud=post("/sdapi/v1/extra-single-image",up)
    im=Image.open(io.BytesIO(base64.b64decode(ud["image"]))).convert("RGB")
    im.save(outp); im.save(PUB/f"{pid}.png")
    made+=1; print(f"[{made}] {pid} -> {im.size} ({desc[:36]}...)",flush=True)
print(f"DONE made={made}/{len(PEOPLE)}")
