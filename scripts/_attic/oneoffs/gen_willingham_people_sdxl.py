"""EP50 rebuild: diverse SDXL PEOPLE/FACES to break the repetitive-imagery + no-faces problem.
Generic anonymized NYC-1989 people (NOT the real Five). JuggernautXL photoreal, moody doc grade.
Output -> E:/pd-media/assets/ai/willingham/P<NN>.png + remotion/public/willingham/img/."""
import base64, io, json, urllib.request, sys
from pathlib import Path
from PIL import Image
API="http://127.0.0.1:7860"; JUGG="juggernautXL_ragnarokBy.safetensors [dd08fa32f9]"
OUT=Path(r"E:/pd-media/assets/ai/willingham"); PUB=Path(r"C:/Users/aab15/Documents/prime-documentary/remotion/public/willingham/img")
OUT.mkdir(parents=True,exist_ok=True); PUB.mkdir(parents=True,exist_ok=True)
GRADE=("cinematic documentary film still, early 1990s small-town Texas, moody low-key lighting, warm dusty amber-and-teal grade, 35mm film grain, shallow depth of field, photoreal, candid, natural skin, high detail")
NEG=("skin blemishes, scars, facial scars, spots, moles, acne, blotchy skin, wrinkled leathery skin, skin lesions, red marks, over-detailed pores, cartoon, illustration, cgi, plastic skin, deformed, extra fingers, mutated hands, "
     "bad anatomy, text, watermark, logo, modern smartphone, modern car, bright saturated")
# diverse people: role, setting, framing -- NONE resembling the real Central Park Five (generic adults / era crowd)
PEOPLE=[
 ("P01","a grieving working-class Texan father in his early 20s with a buzz cut, soot on his face and a burn on his arm, anguished, close-up, night, firelight"),
 ("P02","firefighters in 1991 turnout gear silhouetted against a burning single-story house at night, wide, embers"),
 ("P03","a hard-faced arson investigator in a cheap sport coat crouching over charred floorboards with a flashlight, medium"),
 ("P04","a paid jailhouse informant in a county jail jumpsuit, shifty eyes, close-up, harsh cell light"),
 ("P05","a distinguished older fire scientist in glasses studying a report at a desk, thoughtful, warm lamp, medium close-up"),
 ("P06","a stern rural Texas prosecutor in a bolo tie addressing a jury, low angle, wood-paneled courtroom"),
 ("P07","a small-town jury of 1991 Texans in a jury box, varied weathered faces, wide"),
 ("P08","a weary defense attorney rubbing his eyes at a courtroom table, medium close-up"),
 ("P09","a woman in her 20s (the wife) crying outside a courthouse, medium, harsh daylight"),
 ("P10","a Texas prison guard escorting a shackled inmate down a corridor (inmate face turned away), cold light"),
 ("P11","a chaplain holding a bible outside a death-chamber door, medium, somber"),
 ("P12","a crowd of small-town neighbors watching a house fire from the street at night, faces lit orange, wide"),
 ("P13","a governor-aide reviewing a thick clemency file at a desk under a lamp, medium, tense"),
 ("P14","an execution witness in a small viewing room seen through glass, silhouette, cold light"),
 ("P15","a forensic fire expert pointing at crazed window glass evidence photos on a wall, medium"),
 ("P16","a local newspaper reporter with a 1991 camera outside a courthouse, medium"),
 ("P17","a middle-aged Texan woman on a porch at dusk, worried, medium, warm light"),
 ("P18","two little girls' empty swing set in a bare winter yard, no people, wide, cold morning"),
 ("P19","a death-row inmate sitting on a bunk in a small cell, from behind, cold barred light"),
 ("P20","an appeals lawyer carrying boxes of case files up courthouse steps, medium, overcast"),
 ("P21","a fire marshal testifying on the stand, close-up, courtroom light"),
 ("P22","a somber older man (a juror decades later) looking out a window, close-up, regret, soft light"),
 ("P23","a Texas highway at dusk with a lone pickup truck, wide, warm dust"),
 ("P24","a candlelight vigil of small-town Texans at night, faces lit by candles, medium"),
]
def post(p,pl):
    r=urllib.request.Request(f"{API}{p}",data=json.dumps(pl).encode(),headers={"Content-Type":"application/json"})
    with urllib.request.urlopen(r,timeout=1200) as x: return json.loads(x.read().decode())
post("/sdapi/v1/options",{"sd_model_checkpoint":JUGG})
only=sys.argv[1] if len(sys.argv)>1 else None
made=0
for i,(pid,desc) in enumerate(PEOPLE):
    if only and pid!=only: continue
    outp=OUT/f"{pid}.png"
    if outp.exists() and outp.stat().st_size>200000:
        h=Image.open(outp).height
        if h>=2000: print(f"skip {pid} (already 4K)",flush=True); continue
    # MAX QUALITY: base 1536x864 -> hires-fix Latent 3072x1728 (34 steps) -> R-ESRGAN 4x -> 3840x2160
    pl={"prompt":f"{desc}, {GRADE}","negative_prompt":NEG,"steps":34,"cfg_scale":6.0,
        "width":1536,"height":864,"sampler_name":"DPM++ 2M Karras","seed":50000+i,
        "enable_hr":True,"denoising_strength":0.22,"hr_resize_x":3072,"hr_resize_y":1728,
        "hr_upscaler":"Latent","hr_second_pass_steps":16,
        "override_settings":{"sd_model_checkpoint":JUGG}}
    d=post("/sdapi/v1/txt2img",pl)
    b=d["images"][0]
    up={"image":b,"upscaling_resize_w":3840,"upscaling_resize_h":2160,"upscaling_crop":True,
        "upscaler_1":"R-ESRGAN 4x+","resize_mode":1}
    ud=post("/sdapi/v1/extra-single-image",up)
    im=Image.open(io.BytesIO(base64.b64decode(ud["image"]))).convert("RGB")
    im.save(outp); im.save(PUB/f"{pid}.png")
    made+=1; print(f"[{made}] {pid} -> {outp.name} {im.size} ({desc[:38]}...)",flush=True)
print(f"DONE made={made}/{len(PEOPLE)}")
