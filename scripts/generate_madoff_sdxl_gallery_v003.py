import base64
import json
import time
from pathlib import Path

import requests

API = 'http://127.0.0.1:7860'
OUT = Path(r'H:\pd-media\episodes\PD-2026-005-madoff\05_visuals\sdxl_gallery_v003')
LOG = OUT / '_progress.jsonl'
STATUS = OUT / '_status.json'
OUT.mkdir(parents=True, exist_ok=True)

BASE_STYLE = (
    'museum-grade cinematic documentary still, large format fine art photography, '
    'Madoff era Wall Street financial crime atmosphere, precise composition, '
    'rich but natural lighting, ultra detailed textures, restrained color palette, '
    'black lacquer, warm brass, marble, glass, archival realism, no glamour, '
    'no readable text anywhere, no letters, no numbers, no logos, no watermarks, '
    'no fake typography, no captions, no UI, no poster design, no comic style, '
    'no deformed hands, no distorted faces, no uncanny eyes, no cheap 3d render'
)
NEG = (
    'readable text, letters, words, numbers, fake text, watermark, logo, signature, '
    'poster, title card, subtitles, UI, infographic, chart labels, newspaper text, '
    'bad anatomy, bad hands, extra fingers, missing fingers, mutated hands, distorted face, '
    'cross-eye, cartoon, anime, plastic skin, oversaturated, blurry, lowres, jpeg artifacts, '
    'tiling, duplicate people, malformed body, cheap powerpoint, stock photo look'
)

concepts = [
    ('hook', 'G01_smooth_profit_line', 'a single glowing gold line crossing a black stone table, impossible smooth profit curve implied only by abstract geometry, ominous empty space'),
    ('hook', 'G02_locked_trust_box', 'a sealed black trust box on a marble table under one narrow spotlight, brass edges, unopened and threatening'),
    ('hook', 'G03_silent_investor_room', 'empty elite investor room after everyone left, chairs perfectly aligned, one warm desk lamp, quiet betrayal'),
    ('hook', 'G04_gold_thread_trap', 'thin gold threads forming a beautiful trap over dark velvet, elegant and dangerous, macro fine art'),
    ('opening', 'G05_wall_street_threshold', 'grand dark Wall Street corridor opening into warm light, no signage, no text, symmetrical luxury and danger'),
    ('opening', 'G06_black_gold_nameplate_blank', 'blank black brass-edged plaque seen obliquely, no writing, just polished metal and shadow, prestige without words'),
    ('opening', 'G07_madoff_shadow_portrait', 'faceless older financier silhouette behind frosted glass, no identifiable likeness, no text, austere premium documentary mood'),
    ('opening', 'G08_empire_of_trust', 'towering abstract columns of black glass and brass, trust as architecture, cinematic opening frame'),
    ('opening', 'G09_opening_clock_money', 'luxury office clock reflected in dark marble beside stacked sealed envelopes with no writing, time and money tension'),
    ('actI', 'G10_exclusive_door', 'closed private club double doors, no signage, brass handles, warm glow leaking from inside, exclusion and prestige'),
    ('actI', 'G11_elite_table_empty_chair', 'long mahogany boardroom table with one empty chair at the head, soft golden light, quiet power'),
    ('actI', 'G12_referral_chain', 'gold chain links lying across a black marble desk, one link hidden in shadow, metaphor for referral trust'),
    ('actI', 'G13_hands_off_money', 'gloved hands hovering near stacks of old money without touching, dramatic low key lighting, no visible faces'),
    ('actI', 'G14_trust_vault_door', 'massive vault door slightly open to darkness, polished brass wheel, no labels, fine art realism'),
    ('actI', 'G15_invisible_market', 'empty trading desk with monitors turned away and dark, no text on screens, suspicious absence of real trading'),
    ('actI', 'G16_exclusive_waiting_room', 'luxury waiting room with empty leather chairs and deep shadows, one envelope without writing on table'),
    ('actII', 'G17_empty_trading_floor', 'large trading floor after hours, screens black, cables neat, no data visible, unsettling stillness'),
    ('actII', 'G18_money_drawer', 'open black lacquer drawer filled with neat cash bundles and gold tokens, no bands with writing, forensic beauty'),
    ('actII', 'G19_ponzi_loop_coins', 'coins arranged in an impossible circular loop on obsidian, one coin almost falling, macro cinematic'),
    ('actII', 'G20_absent_trade_machine', 'old financial terminal glowing only with abstract light, no text, beside untouched keyboard, absent evidence'),
    ('actII', 'G21_false_balance', 'antique brass scale balancing coins against a black sealed envelope, metaphor of false balance'),
    ('actII', 'G22_cash_river_dark', 'subtle river of coins flowing through darkness under a desk, elegant but ominous'),
    ('actII', 'G23_hidden_ledger_blank', 'blank ledger pages with only abstract grid lines and shadows, no readable writing, fountain pen resting unused'),
    ('actII', 'G24_vault_without_bottom', 'vault interior dissolving into black emptiness, floor covered with scattered coins, cinematic depth'),
    ('actIII', 'G25_midnight_analyst', 'solitary analyst from behind at midnight desk, papers turned blank, calculator, lamp cone, human doubt'),
    ('actIII', 'G26_red_flag_pin', 'single red pin piercing a dark abstract financial map with no labels, gold lines around it, investigative focus'),
    ('actIII', 'G27_warning_envelopes_unopened', 'stack of sealed blank warning envelopes under dust, no addresses, ignored warnings'),
    ('actIII', 'G28_sleeping_watchtower', 'empty regulator watchtower-like office overlooking city lights, chair vacant, no screens with text'),
    ('actIII', 'G29_tangled_evidence_threads', 'red and gold evidence threads crossing over black board, no notes, pure visual investigation'),
    ('actIII', 'G30_lamp_over_blank_records', 'desk lamp exposing blank record sheets with grid texture only, all detail in paper fibers, no writing'),
    ('actIII', 'G31_doubt_in_glass', 'faceless reflection of investigator in dark glass wall, city lights behind, subtle red warning glow'),
    ('actIV', 'G32_withdrawal_panic_lobby', 'financial lobby with silhouetted crowd frozen in tension, no signage, marble and glass, crisis mood'),
    ('actIV', 'G33_empty_cash_pedestal', 'black pedestal surrounded by scattered coins, missing fortune implied, strong museum composition'),
    ('actIV', 'G34_court_steps_light', 'federal courthouse-like steps in morning light, no inscriptions, small lone silhouette climbing'),
    ('actIV', 'G35_prison_corridor', 'long prison-like corridor, single shadow at far end, cold light, no text, final consequence'),
    ('actIV', 'G36_recovery_return', 'coins slowly returning into separate small bowls, partial recovery metaphor, warm controlled light'),
    ('actIV', 'G37_broken_gold_circle', 'broken circle of gold tokens on black velvet, missing segment, betrayal exposed'),
    ('actIV', 'G38_family_trust_aftershock', 'three empty chairs around a kitchen table with one blank envelope, victims implied without faces'),
    ('actIV', 'G39_last_door_closing', 'heavy institutional door closing into darkness, thin line of light, no signage'),
    ('ending', 'G40_smooth_vs_real', 'one perfect smooth gold line beside one jagged honest line carved into black stone, abstract lesson, no text'),
    ('ending', 'G41_final_doubt', 'single person silhouette facing a vast dark gallery of reflections, question of trust, cinematic ending'),
    ('ending', 'G42_empty_frame_money', 'empty gilded picture frame on dark wall casting shadow over coins, artful moral emptiness'),
    ('ending', 'G43_closed_ledger', 'closed blank black ledger with brass clasp on marble, finality and silence'),
    ('ending', 'G44_truth_under_light', 'narrow beam of light revealing only dust and a coin on black floor, minimal final image'),
    ('thumbnail', 'G45_thumb_bright_trust_trap', 'brighter premium documentary thumbnail background, gold trap threads over marble, high contrast readable negative space, no text'),
    ('thumbnail', 'G46_thumb_vault_light', 'bright vault door half open with warm gold light and dark foreground, dramatic YouTube documentary thumbnail background, no text'),
    ('thumbnail', 'G47_thumb_broken_circle', 'bright black and gold broken coin circle, strong central composition, clean background for title, no text'),
    ('thumbnail', 'G48_thumb_financier_shadow', 'faceless financier silhouette in brighter golden office doorway, high-end documentary thumbnail background, no text'),
]

preferred_upscalers = ['4x-UltraSharp', 'R-ESRGAN 4x+', 'Lanczos', 'Latent']
try:
    ups = requests.get(API + '/sdapi/v1/upscalers', timeout=10).json()
    names = [u.get('name') for u in ups]
    upscaler = next((p for p in preferred_upscalers if p in names), names[0] if names else 'Latent')
except Exception:
    upscaler = 'Latent'

base_seed = 730000
variants = 2
total = len(concepts) * variants
completed = 0
start = time.time()

for section, slug, subject in concepts:
    sec_dir = OUT / section
    sec_dir.mkdir(parents=True, exist_ok=True)
    for variant in range(1, variants + 1):
        seed = base_seed + completed * 131 + variant * 17
        name = f'{slug}_c{variant:02d}_seed{seed}.png'
        out_path = sec_dir / name
        if out_path.exists():
            completed += 1
            continue
        prompt = f'{subject}, {BASE_STYLE}'
        payload = {
            'prompt': prompt,
            'negative_prompt': NEG,
            'seed': seed,
            'sampler_name': 'DPM++ 2M Karras',
            'scheduler': 'Karras',
            'steps': 48,
            'cfg_scale': 6.0,
            'width': 1344,
            'height': 768,
            'enable_hr': True,
            'hr_scale': 1.65,
            'hr_upscaler': upscaler,
            'hr_second_pass_steps': 22,
            'denoising_strength': 0.24,
            'save_images': False,
            'override_settings': {
                'sd_model_checkpoint': 'juggernautXL_ragnarokBy.safetensors [dd08fa32f9]'
            },
            'override_settings_restore_afterwards': False,
        }
        t0 = time.time()
        r = requests.post(API + '/sdapi/v1/txt2img', json=payload, timeout=2400)
        r.raise_for_status()
        data = r.json()
        img = base64.b64decode(data['images'][0].split(',', 1)[0])
        out_path.write_bytes(img)
        completed += 1
        rec = {
            'completed': completed,
            'total': total,
            'section': section,
            'file': str(out_path),
            'seconds': round(time.time() - t0, 1),
            'elapsed_minutes': round((time.time() - start) / 60, 1),
            'upscaler': upscaler,
        }
        with LOG.open('a', encoding='utf-8') as f:
            f.write(json.dumps(rec, ensure_ascii=False) + '\n')
        STATUS.write_text(json.dumps(rec, ensure_ascii=False, indent=2), encoding='utf-8')

final = {
    'completed': completed,
    'total': total,
    'elapsed_minutes': round((time.time() - start) / 60, 1),
    'output': str(OUT),
    'upscaler': upscaler,
}
STATUS.write_text(json.dumps(final, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(final, ensure_ascii=False))

