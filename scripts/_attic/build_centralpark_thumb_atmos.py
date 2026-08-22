"""EP50 atmospheric thumbnail: interrogation scene (empty chair / silhouette), NO face.
Safe for the Central Park Five (no likeness, no race-misrepresentation). CTR hook text."""
import base64, io, json, sys, urllib.request
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
ROOT = Path(r"C:/Users/aab15/Documents/prime-documentary")
API = "http://127.0.0.1:7860"
JUGG = "juggernautXL_ragnarokBy.safetensors [dd08fa32f9]"
W, H = 1280, 720
FONT_ANTON = str(ROOT/"remotion"/"public"/"fonts"/"Anton.ttf")
LOGO = ROOT/"remotion"/"public"/"pd_logo.png"
WHITE=(247,249,252); CYAN=(65,190,220); INK=(8,12,20); ACCENT=(47,159,196)
NEG=("people, person, face, man, boy, crowd, text, letters, watermark, logo, caption, "
     "lowres, jpeg artifacts, blurry, disfigured, extra objects, clutter")
SCENES={
 "chair":("a single empty vintage metal interrogation chair positioned slightly right of center "
   "in a bare dark concrete interrogation room, one harsh cold overhead lamp casting a hard "
   "pool of cold cyan light and a long dramatic shadow across the floor, a bare steel table "
   "edge in the foreground, wet concrete reflections, deep shadows, volumetric haze, empty, "
   "abandoned, ominous, cinematic still, deep dark negative space on the LEFT, 85mm, moody"),
 "silhouette":("the dark backlit silhouette of a small hunched teenage figure sitting slumped "
   "in a chair under one harsh cold overhead interrogation lamp, the figure is a pure black "
   "featureless silhouette with no visible face or skin, strong backlight rim, cold cyan glow, "
   "bare dark interrogation room, long shadow, volumetric haze, cinematic, ominous, subject on "
   "the RIGHT, deep dark negative space on the LEFT, 85mm"),
}
def post(p,pl):
    r=urllib.request.Request(f"{API}{p}",data=json.dumps(pl).encode(),headers={"Content-Type":"application/json"})
    with urllib.request.urlopen(r,timeout=600) as x: return json.loads(x.read().decode())
def gen(prompt,seed):
    post("/sdapi/v1/options",{"sd_model_checkpoint":JUGG})
    pl={"prompt":prompt+", cinematic, dramatic low-key lighting, high detail, film grain, deep teal and navy",
        "negative_prompt":NEG,"steps":32,"cfg_scale":6.5,"width":1216,"height":832,
        "sampler_name":"DPM++ 2M Karras","seed":seed}
    d=post("/sdapi/v1/txt2img",pl)
    return Image.open(io.BytesIO(base64.b64decode(d["images"][0]))).convert("RGB")
def fit(im):
    # cover-crop 1216x832 -> 1280x720
    im=im.resize((W,int(W*im.height/im.width)))
    if im.height<H: im=im.resize((int(H*im.width/im.height),H))
    x=(im.width-W)//2; y=(im.height-H)//2
    return im.crop((x,y,x+W,y+H))
def stroke_text(d,xy,txt,font,fill,sw=6):
    x,y=xy
    for dx in range(-sw,sw+1,2):
        for dy in range(-sw,sw+1,2):
            d.text((x+dx,y+dy),txt,font=font,fill=INK)
    d.text(xy,txt,font=font,fill=fill)
def compose(bg,tag):
    im=fit(bg).convert("RGB")
    # left darkening gradient for text legibility
    grad=Image.new("L",(W,H),0); gd=ImageDraw.Draw(grad)
    for x in range(W):
        a=int(max(0,180*(1-x/(W*0.62))))
        gd.line([(x,0),(x,H)],fill=a)
    shade=Image.new("RGB",(W,H),(4,8,14))
    im=Image.composite(shade,im,grad)
    im=ImageEnhance.Contrast(im).enhance(1.06)
    d=ImageDraw.Draw(im)
    fK=ImageFont.truetype(FONT_ANTON,34); fH=ImageFont.truetype(FONT_ANTON,96)
    MX=60
    # kicker chip
    kt="CENTRAL PARK, 1989"
    kw=d.textlength(kt,font=fK); d.rectangle([MX-8,150,MX+kw+14,150+52],fill=ACCENT)
    d.text((MX+2,156),kt,font=fK,fill=WHITE)
    # headline two lines
    stroke_text(d,(MX,235),"5 CONFESSIONS",fH,WHITE)
    stroke_text(d,(MX,345),"NO EVIDENCE",fH,CYAN)
    d.rectangle([MX,470,MX+470,478],fill=CYAN)
    # logo
    if LOGO.exists():
        lg=Image.open(LOGO).convert("RGBA"); lg.thumbnail((120,120))
        im.paste(lg,(W-lg.width-28,H-lg.height-24),lg)
    return im
def main():
    out={}
    for tag,pr in SCENES.items():
        seed={"chair":50777,"silhouette":50888}[tag]
        print(f"gen {tag}...",flush=True)
        bg=gen(pr,seed)
        comp=compose(bg,tag)
        p=ROOT/"episodes"/"PD-2026-050-centralpark"/"09_package"/f"thumbnail.atmos_{tag}.v001.png"
        comp.save(p); print("  ->",p)
    print("DONE")
main()
