# EP32 (PD-2026-032-carsearch) — Foley Download List

**Purpose.** These ~8 real-recorded foley sounds cannot be synthesized convincingly
with ffmpeg (they are mechanical/physical events with complex, unpredictable
transients). The owner downloads them from a rights-clean source and saves each
under the exact filename below so the audio builder can pick it up.

**Rights rule (both sources are commercial-OK, NO attribution required):**
- **Preferred → Pixabay Sound Effects** — Pixabay Content License, free for
  commercial use, no attribution. https://pixabay.com/sound-effects/
- **Alternate → YouTube Audio Library** (Studio → Audio Library → *Sound effects*)
  — free for commercial use including monetized videos, no attribution.
  https://studio.youtube.com

**Save location:** `H:\pd-media\library\sfx\<filename>.mp3`
(If a download is WAV, transcode to MP3 to match the library:
`ffmpeg -i in.wav -c:a libmp3lame -b:a 192k -ar 44100 -ac 2 out.mp3`.)

**Level target:** normalize to about **-18 dBFS peak** so it sits with the rest of
the palette (the mix builder sets final per-cue gain).
`ffmpeg -i in.mp3 -af "volume=<gain>dB" out.mp3` after checking with
`ffmpeg -i in.mp3 -af astats=measure_perchannel=none -f null -`.

**Selection notes:** pick a *dry, close-mic'd, single-event* take (no music, no
reverb tail, no talking). Trim silence at head/tail. Prefer < 2 s for one-shots.

---

## Items

### 1. Car door close
- **Save as:** `sfx_car_door_close.mp3`
- **Serves cue(s):** door slam / "the door closes" beats; ACT III driveway approach.
- **Pixabay search terms:** `car door close`, `car door slam`, `sedan door shut`
- **YouTube AL search:** `car door`
- **Pick:** a solid single "thunk" (modern sedan), not a loud sports-car slam.

### 2. Handcuff ratchet
- **Save as:** `sfx_handcuff_ratchet.mp3`
- **Serves cue(s):** arrest / restraint moment; "the single hardest impact" lead-in.
- **Pixabay search terms:** `handcuffs`, `handcuff ratchet`, `handcuffs close`
- **YouTube AL search:** `handcuffs`
- **Pick:** the crisp metallic zip-ratchet of the cuff closing (one cuff).

### 3. Heavy fabric / tarp pull
- **Save as:** `sfx_tarp_pull.mp3`
- **Serves cue(s):** "the tarp pull", "light wind rustling the tarp", upholstery/fabric tear beats (ACT III).
- **Pixabay search terms:** `tarp pull`, `heavy fabric drag`, `canvas pull`, `cloth pull`
- **YouTube AL search:** `fabric` / `cloth`
- **Pick:** a low, weighty drag (canvas/tarp), not a light tissue rustle.

### 4. Footsteps on gravel / driveway
- **Save as:** `sfx_footsteps_gravel.mp3`
- **Serves cue(s):** "footsteps" approach on the driveway (ACT III).
- **Pixabay search terms:** `footsteps gravel`, `walking gravel`, `footsteps driveway`
- **YouTube AL search:** `footsteps gravel`
- **Pick:** 3–5 measured steps on gravel; steady pace, close mic.

### 5. Car engine start + idle
- **Save as:** `sfx_engine_start.mp3`
- **Serves cue(s):** "engine pull" / ignition beats (ACT I road). Pairs with the
  synthesized `amb_engine_idle.mp3` bed for the sustained hum.
- **Pixabay search terms:** `car engine start`, `engine ignition start idle`, `car start up`
- **YouTube AL search:** `engine start`
- **Pick:** ignition crank → catch → settle to idle (2–4 s), ordinary passenger car.

### 6. Glass bottle clink
- **Save as:** `sfx_glass_clink.mp3`
- **Serves cue(s):** "glass clinks" (ACT I evidence / bottle beat).
- **Pixabay search terms:** `glass clink`, `bottle clink`, `glass bottle tap`
- **YouTube AL search:** `glass`
- **Pick:** a single clean bottle-to-bottle or bottle-to-glass clink, short decay.

### 7. Tire on wet asphalt
- **Save as:** `sfx_tire_wet_asphalt.mp3`
- **Serves cue(s):** rain/road pass-by; pairs with `amb_rain_street.mp3` +
  `amb_highway_traffic.mp3` beds. Use as the pass-by transient.
- **Pixabay search terms:** `tire wet road`, `car pass by wet`, `wet road drive by`, `tires rain`
- **YouTube AL search:** `car pass` / `rain road`
- **Pick:** a single vehicle swish-by on wet tarmac (Doppler pass), no engine roar.

### 8. Key in lock
- **Save as:** `sfx_key_lock.mp3`
- **Serves cue(s):** "a tense metallic turn", "mechanical click", lock/latch beats (ACT III/IV).
- **Pixabay search terms:** `key in lock`, `key turn lock`, `door lock key`, `deadbolt`
- **YouTube AL search:** `lock` / `key`
- **Pick:** key insert → turn → bolt click; dry and close, one action.

---

## Builder wiring (so these get used, not the reused stand-ins)

The builder maps script keywords → filenames in
`scripts/build_case_film_audio.py` (`ONESHOT_MAP`). Today several distinct cues
collapse onto a few reused files (the "cheap" tell). After the 8 files above are
saved, point the map at them (add these rows ABOVE the existing generic rows so
they win by first-match):

| Script keyword(s) | New foley filename |
|---|---|
| `car door`, `door close`, `door slam` | `sfx/sfx_car_door_close.mp3` |
| `handcuff`, `cuffs`, `ratchet` | `sfx/sfx_handcuff_ratchet.mp3` |
| `tarp`, `fabric`, `upholstery`, `cloth pull` | `sfx/sfx_tarp_pull.mp3` |
| `footstep`, `steps`, `gravel`, `driveway` | `sfx/sfx_footsteps_gravel.mp3` |
| `engine start`, `ignition`, `engine pull` | `sfx/sfx_engine_start.mp3` |
| `clink`, `glass`, `bottle` | `sfx/sfx_glass_clink.mp3` |
| `tire`, `wet asphalt`, `pass-by` (road) | `sfx/sfx_tire_wet_asphalt.mp3` |
| `key`, `lock`, `latch`, `metallic turn` | `sfx/sfx_key_lock.mp3` |

Also add the new **synthesized** variants (already in the library) into rotation
so no one-shot repeats too often: `sfx_whoosh_v2_{short,med,long}`,
`sfx_riser_v2_{1s,3s}`, `sfx_boom_v2_deep`, `sfx_impact_v2_tight`,
`sfx_subdrop_v2_{a,b}`, `sfx_tick_v2_{hi,lo}`, `sfx_blip_v2_{hi,lo}`; and the new
beds `amb_{rain_street,highway_traffic,engine_idle,light_wind,road_rumble_1920s}`.

## Rights logging

After download, append each foley file to
`episodes/_planning/SOUND_LIBRARY_RIGHTS.v001.json` (or the library registry)
with: `provenance_method: "pixabay-download"` (or `"youtube-audio-library"`),
`license: "Pixabay Content License"` (or `"YouTube Audio Library — free commercial"`),
`commercial_ok: true`, `attribution_required: false`, source URL, and the
downloaded file's SHA-256. **Do not publish** until every foley file used has a
rights row.

**Item count: 8 foley files.**
