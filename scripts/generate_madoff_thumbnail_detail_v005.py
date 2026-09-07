import base64, json, time
from pathlib import Path
import requests

API='http://127.0.0.1:7860'
OUT=Path(r'E:\pd-media\episodes\PD-2026-005-madoff\09_thumbnail\sdxl_detail_v005')
OUT.mkdir(parents=True, exist_ok=True)

style=(
    'single coherent museum-grade cinematic financial crime documentary thumbnail background, '
    'ultra detailed evidence room inside a luxurious Wall Street private office and vault, '
    'hundreds of subtle financial artifacts integrated naturally: blank account ledgers, sealed envelopes without writing, '
    'cash bundles, gold coins, brass scale, calculator, empty trading monitors with abstract glow, red evidence threads, '
    'black marble, mahogany, warm brass, forensic lighting, deep depth, crisp micro textures, '
    'large format photography, sharp focus, premium dramatic composition, high detail everywhere, '
    'clean empty dark space on the left for title text, bright golden focal light on the right, '
    'no readable text, no letters, no numbers, no logos, no watermark, no captions, no poster typography'
)
neg=(
    'readable text, fake text, letters, numbers, logo, watermark, signature, subtitle, poster, title, '
    'lowres, blurry, jpeg artifacts, smeared details, plastic, cartoon, anime, cheap 3d render, collage, cutout, '
    'bad anatomy, distorted face, hands, extra fingers, deformed people, duplicated people, oversaturated, noisy'
)
subjects=[
    'luxury vault office with investigator evidence board, cash drawers, gold threads, clock, sealed blank envelopes, dense but elegant details',
    'dark Wall Street evidence room, Madoff era financial fraud atmosphere, infinite desk of blank ledgers and coins, red threads across glass',
    'premium forensic table in private bank vault, polished brass, documents without writing, money trail represented by gold wires and reflections',
    'cinematic financial crime command room, empty chair, vault door, abstract chart lines on glass with no labels, many tiny realistic objects'
]
try:
    ups=requests.get(API+'/sdapi/v1/upscalers',timeout=10).json()
    names=[u.get('name') for u in ups]
    upscaler='R-ESRGAN 4x+' if 'R-ESRGAN 4x+' in names else ('4x-UltraSharp' if '4x-UltraSharp' in names else 'Latent')
except Exception:
    upscaler='Latent'

results=[]
for i,sub in enumerate(subjects,1):
    seed=810000+i*137
    path=OUT/f'thumbnail_detail_c{i:02d}_seed{seed}.png'
    if path.exists():
        results.append(str(path)); continue
    payload={
        'prompt': f'{sub}, {style}',
        'negative_prompt': neg,
        'seed': seed,
        'sampler_name': 'DPM++ 2M Karras',
        'scheduler': 'Karras',
        'steps': 54,
        'cfg_scale': 6.2,
        'width': 1536,
        'height': 864,
        'enable_hr': True,
        'hr_scale': 1.5,
        'hr_upscaler': upscaler,
        'hr_second_pass_steps': 24,
        'denoising_strength': 0.22,
        'save_images': False,
        'override_settings': {'sd_model_checkpoint':'juggernautXL_ragnarokBy.safetensors [dd08fa32f9]'},
        'override_settings_restore_afterwards': False,
    }
    t=time.time()
    r=requests.post(API+'/sdapi/v1/txt2img',json=payload,timeout=2400)
    r.raise_for_status()
    data=r.json()
    img=base64.b64decode(data['images'][0].split(',',1)[0])
    path.write_bytes(img)
    results.append(str(path))
    print(json.dumps({'done':i,'file':str(path),'seconds':round(time.time()-t,1),'upscaler':upscaler},ensure_ascii=False), flush=True)
print(json.dumps({'total':len(results),'output':str(OUT)},ensure_ascii=False))
