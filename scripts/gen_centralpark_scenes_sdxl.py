"""EP50 rebuild: diverse SDXL SCENES to break the repetitive dark-room imagery.
Wide variety (NYC establishing / park / institutional-varied / textural detail / media /
2002 DNA era / time-of-day). NO readable text (SDXL garbles it). Max quality 4K.
Output -> H:/pd-media/assets/ai/centralpark/V<NN>.png + remotion/public/centralpark/img/."""
import base64, io, json, urllib.request, sys
from pathlib import Path
from PIL import Image
API="http://127.0.0.1:7860"; JUGG="juggernautXL_ragnarokBy.safetensors [dd08fa32f9]"
OUT=Path(r"H:/pd-media/assets/ai/centralpark"); PUB=Path(r"C:/Users/aab15/Documents/prime-documentary/remotion/public/centralpark/img")
OUT.mkdir(parents=True,exist_ok=True); PUB.mkdir(parents=True,exist_ok=True)
GRADE=("cinematic documentary film still, moody atmospheric lighting, 35mm film grain, "
       "shallow depth of field, photoreal, high detail, no text, no writing")
NEG=("readable text, letters, words, signage text, newspaper text, watermark, logo, caption, "
     "cartoon, illustration, cgi, deformed, bad anatomy, oversaturated, modern smartphone")
SCENES=[
 ("V01","the 1989 New York City skyline at dusk from across the river, hazy orange and teal sky, wide establishing"),
 ("V02","a Harlem residential street in 1989 summer, brownstone stoops, parked cars, warm low sun, wide"),
 ("V03","the Brooklyn Bridge at blue hour with city lights, wide cinematic"),
 ("V04","a graffiti-covered 1989 subway train rushing through a station, long-exposure motion blur"),
 ("V05","an empty subway platform at night, cold fluorescent light, tiled walls, wide"),
 ("V06","a NYC bodega corner storefront at night, glowing warm interior, rain-wet sidewalk"),
 ("V07","a lone lit phone booth on a dark 1989 city street corner, cinematic, cold light"),
 ("V08","Central Park tree-lined path at early morning, mist, empty, soft light, wide"),
 ("V09","Central Park at dusk, silhouetted bare trees and a lamppost, ominous mood, wide"),
 ("V10","the Central Park reservoir at grey dawn, still water, city skyline behind, wide"),
 ("V11","a wooded park thicket at night lit by a single distant streetlamp, empty, tense, no people"),
 ("V12","an empty green park bench under a lamppost at night, fallen leaves, moody"),
 ("V13","a grand stone courthouse exterior with columns, overcast day, low angle, imposing"),
 ("V14","wide marble courthouse lobby interior, tall windows, hard shafts of light, empty"),
 ("V15","stone courthouse steps in the rain, empty, wide, cold"),
 ("V16","a 1980s district attorney office interior, wood desk, stacked case files, warm lamp, daylight window"),
 ("V17","an NYPD precinct building exterior at night, green lamp globes, cold, wide"),
 ("V18","a high prison perimeter wall with razor wire and a watchtower at dawn, wide, bleak"),
 ("V19","an empty prison yard behind chain-link fence, long shadows, cold morning, wide"),
 ("V20","a prison cell block interior, rows of steel doors receding, cold blue light, wide"),
 ("V21","a narrow prison cell interior, a bunk and a small barred window, hard light, empty"),
 ("V22","a prison visiting room with a long counter and plexiglass dividers, empty, cold fluorescent"),
 ("V23","a stack of worn manila case files and folders on a metal desk, close-up, dramatic side light"),
 ("V24","a black rotary telephone on a cluttered 1980s desk, close-up, warm lamp light"),
 ("V25","the keys of an old manual typewriter, extreme close-up, shallow focus, moody"),
 ("V26","a small cassette tape recorder on an interrogation table, close-up, cold light, red record indicator"),
 ("V27","sealed plastic evidence bags on a steel table under a lamp, close-up, forensic cold light"),
 ("V28","a fingerprint card and ink pad on a desk, close-up, dramatic light"),
 ("V29","an old television set showing grainy static in a dark room, close-up, glow"),
 ("V30","rain streaming down a dark precinct window at night, city lights bokeh beyond, close-up"),
 ("V31","a chipped coffee mug and a full ashtray on an interrogation table, close-up, harsh overhead light"),
 ("V32","a plain institutional wall clock reading late night, close-up, cold light, worn"),
 ("V33","steel handcuffs lying open on a dark metal table under a single lamp, close-up"),
 ("V34","a wall of dozens of glowing 1989 television screens in an electronics store window at night, no readable text"),
 ("V35","huge newspaper printing press rollers spinning with blank newsprint, motion blur, industrial, no text"),
 ("V36","a 1989 satellite news truck with a raised mast parked outside a courthouse at night, wide"),
 ("V37","an empty press-conference podium with a cluster of microphones, harsh flash lighting, dark background"),
 ("V38","a modern 2002 forensic DNA laboratory, blue-lit sequencing machines, sterile, wide"),
 ("V39","a glowing DNA gel electrophoresis plate with bright bands in a dark lab, extreme close-up"),
 ("V40","a heavy steel prison door swinging open toward blinding daylight, silhouette, hopeful, wide"),
 ("V41","warm morning sun flaring through bare winter trees over a quiet city street, wide, hopeful"),
 ("V42","a dense cluster of old press cameras and flashbulbs raised toward the viewer, dark background, motion"),
 ("V43","an aerial night view of the Manhattan grid glittering, wide, cinematic"),
 ("V44","a rain-soaked empty city crosswalk at night under a red traffic light, reflections, wide"),
 ("V45","a quiet 1980s working-class kitchen at night lit only by a small television glow, empty, intimate"),
 ("V46","a long empty institutional corridor with flickering fluorescent lights, cold, receding, wide"),
 ("V47","a judge's empty high bench and the state and national flags in a dim courtroom, low angle"),
 ("V48","dawn breaking grey and pink over a silent prison complex seen from a distance, wide, bleak-to-hopeful"),
]
def post(p,pl):
    r=urllib.request.Request(f"{API}{p}",data=json.dumps(pl).encode(),headers={"Content-Type":"application/json"})
    with urllib.request.urlopen(r,timeout=1200) as x: return json.loads(x.read().decode())
post("/sdapi/v1/options",{"sd_model_checkpoint":JUGG})
only=sys.argv[1] if len(sys.argv)>1 else None
made=0
for i,(vid,desc) in enumerate(SCENES):
    if only and vid!=only: continue
    outp=OUT/f"{vid}.png"
    if outp.exists() and outp.stat().st_size>200000 and Image.open(outp).height>=2000:
        print(f"skip {vid} (already 4K)",flush=True); continue
    pl={"prompt":f"{desc}, {GRADE}","negative_prompt":NEG,"steps":34,"cfg_scale":6.0,
        "width":1536,"height":864,"sampler_name":"DPM++ 2M Karras","seed":51000+i,
        "enable_hr":True,"denoising_strength":0.22,"hr_resize_x":3072,"hr_resize_y":1728,
        "hr_upscaler":"Latent","hr_second_pass_steps":16,
        "override_settings":{"sd_model_checkpoint":JUGG}}
    d=post("/sdapi/v1/txt2img",pl)
    up={"image":d["images"][0],"upscaling_resize_w":3840,"upscaling_resize_h":2160,
        "upscaling_crop":True,"upscaler_1":"R-ESRGAN 4x+","resize_mode":1}
    ud=post("/sdapi/v1/extra-single-image",up)
    im=Image.open(io.BytesIO(base64.b64decode(ud["image"]))).convert("RGB")
    im.save(outp); im.save(PUB/f"{vid}.png")
    made+=1; print(f"[{made}] {vid} -> {im.size} ({desc[:40]}...)",flush=True)
print(f"DONE made={made}/{len(SCENES)}")
