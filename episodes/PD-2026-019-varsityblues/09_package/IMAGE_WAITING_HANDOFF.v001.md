# EP19 Image-Waiting Handoff v001

Status: audio/factory/Remotion scaffold ready; hero images, thumbnails, final render pending.

Ready now:
- ElevenLabs master voice: `H:/pd-media/episodes/PD-2026-019-varsityblues/06_audio/master_elevenlabs_v001/voice_master.v001.wav`
- Final audio mix: `H:/pd-media/episodes/PD-2026-019-varsityblues/08_edit/varsityblues_final_mix.v001.wav`
- Captions: `episodes/PD-2026-019-varsityblues/08_edit/captions.v001.srt`
- Factory b-roll ledger: `episodes/PD-2026-019-varsityblues/05_stock/factory_ledger.v001.json`
- Remotion composition: `VarsityBluesPremium`

When images are ready:
1. Place all files as `H:/pd-media/episodes/PD-2026-019-varsityblues/05_visuals/selected/EP19-IMG-001.png` through `EP19-IMG-092.png`.
2. Confirm every used still is 16:9 and long edge >= 3840 px.
3. Run:

```powershell
cd C:\Users\aab15\Documents\prime-documentary
.\.venv\Scripts\python.exe scripts\build_ep19_varsityblues_final.py
.\.venv\Scripts\python.exe scripts\check_final_acceptance.py 19 --json
```

Current independent gate blockers:
- render_present: final render not found (looked at None); render the episode's *Premium final before acceptance
- thumbnail_ready: 0 thumb(s) at 1280x720, selected=NO (need >=3 + selected)

Do not publish/upload. R3 legal and rights owner gate remains required after final render.
