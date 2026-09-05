"""EP50 rebuild: diverse SDXL PEOPLE/FACES to break the repetitive-imagery + no-faces problem.
Generic anonymized NYC-1989 people (NOT the real Five). JuggernautXL photoreal, moody doc grade.
Output -> E:/pd-media/assets/ai/centralpark/P<NN>.png + remotion/public/centralpark/img/."""
import base64, io, json, urllib.request, sys
from pathlib import Path
from PIL import Image
API="http://127.0.0.1:7860"; JUGG="juggernautXL_ragnarokBy.safetensors [dd08fa32f9]"
OUT=Path(r"E:/pd-media/assets/ai/centralpark"); PUB=Path(r"C:/Users/aab15/Documents/prime-documentary/remotion/public/centralpark/img")
OUT.mkdir(parents=True,exist_ok=True); PUB.mkdir(parents=True,exist_ok=True)
GRADE=("cinematic documentary film still, 1989 New York City, moody low-key lighting, "
       "muted cool teal-and-amber grade, 35mm film grain, shallow depth of field, photoreal, "
       "candid, natural skin, high detail")
NEG=("skin blemishes, scars, facial scars, spots, moles, acne, blotchy skin, wrinkled leathery skin, skin lesions, red marks, over-detailed pores, cartoon, illustration, cgi, plastic skin, deformed, extra fingers, mutated hands, "
     "bad anatomy, text, watermark, logo, modern smartphone, modern car, bright saturated")
# diverse people: role, setting, framing -- NONE resembling the real Central Park Five (generic adults / era crowd)
PEOPLE=[
 ("P01","a weary middle-aged plainclothes NYPD detective in a rumpled shirt and tie, tense face, close-up, a dim precinct at night behind him"),
 ("P02","a determined female prosecutor in her 40s in a 1980s skirt suit reviewing papers at a desk, medium shot, courthouse office"),
 ("P03","a defense attorney in his 50s, tired and frustrated, speaking off-camera, medium close-up, wood-paneled courtroom"),
 ("P04","an anguished mother in her 40s in a plain 1989 coat waiting on a hard bench, hands clasped, close-up, fluorescent hallway"),
 ("P05","a scrum of 1989 newspaper press photographers with old flashbulb cameras crowding forward, motion, city steps"),
 ("P06","a tired uniformed corrections officer standing by a steel cell block gate, medium shot, cold blue prison light"),
 ("P07","a 1989 TV news anchor at a boxy news desk under hot studio lights, medium shot"),
 ("P08","an elderly Black grandmother in a church hat sitting quietly in a courtroom gallery, close-up, soft window light"),
 ("P09","a crowd of diverse 1989 New Yorkers on a Harlem sidewalk, varied faces, wide shot, summer"),
 ("P10","a young female court stenographer typing at a machine, profile, medium shot, courtroom"),
 ("P11","a stern judge in black robes on the bench, low angle medium shot, wood courtroom, gavel"),
 ("P12","a father in a factory jacket standing outside a housing project at dusk, medium shot, worried"),
 ("P13","two detectives talking across a metal interrogation table (backs and profiles, faces partly turned), cold room"),
 ("P14","a 1989 protester holding a hand-painted cardboard sign in a street march, close-up, angry and hopeful, crowd behind"),
 ("P15","a subway car full of tired 1989 commuters under flickering light, candid, wide shot"),
 ("P16","a forensic lab technician in a white coat at a microscope, side light, medium close-up, dark lab"),
 ("P17","a public defender and a young client (client seen from behind, face hidden) conferring, cold hallway"),
 ("P18","a middle-aged newspaper editor at a cluttered 1989 newsroom desk with a rotary phone, medium shot"),
 ("P19","an exhausted social worker in a cramped office with case files stacked high, medium shot"),
 ("P20","a lone commuter waiting on an empty subway platform at night, wide shot, cold fluorescent"),
 ("P21","a diverse jury of twelve 1989 New Yorkers in a jury box, varied faces, wide shot, courtroom"),
 ("P22","a tv repairman's shop window wall of glowing 1989 televisions all showing news, no people, medium shot"),
 ("P23","a beat cop on a graffiti-covered 1989 subway platform, medium shot, motion blur of a passing train"),
 ("P24","a middle-aged man in a suit reading a lurid 1989 tabloid newspaper on a park bench, close-up on hands and paper"),
 ("P25","a courtroom sketch artist sketching, over-the-shoulder, medium shot"),
 ("P26","a tired defense lawyer alone in a stairwell rubbing his eyes, medium close-up, hard light"),
 ("P27","a mother and father embracing in relief outside a courthouse, medium shot, evening"),
 ("P28","an older Black man in a modest suit at a press microphone speaking calmly, close-up, flashes"),
 ("P29","a 1989 city street with yellow cabs and diverse pedestrians, wide establishing, overcast"),
 ("P30","an empty church pew with a single elderly parishioner praying, wide shot, stained glass light"),
 ("P31","a detective's hand pinning a suspect photo to a corkboard of case notes, close-up, no face"),
 ("P32","a young man in a holding cell seen through the bars from outside (face in shadow, unidentifiable), cold light"),
 ("P33","a crowd of reporters and cameras outside a courthouse at the verdict, wide shot, chaos, 1989"),
 ("P34","a middle-aged woman watching a small kitchen TV at night, back-lit, medium shot, worried"),
 ("P35","a prison visiting room with a plexiglass divider and two silhouetted figures, wide shot, cold"),
 ("P36","an older man in a modern (2002) suit at a legal press conference, warm hopeful light, medium close-up"),
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
