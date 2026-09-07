# EP19 Acceptance Report v001

Status: ACCEPTED_EDIT_REVIEW
Final video: `H:/pd-media/episodes/PD-2026-019-varsityblues/08_edit/final.mp4`

Measured gates:
- runtime_band: OK - 1660.3s = 27.67min (band 1620-1980s)
- render_resolution: OK - 1920x1080 codec=h264 (need >= 1920x1080)
- images_present: OK - black total 0.0s / longest 0.0s (limits 8/3)
- motion_present: OK - frozen total 0.0s / longest 0.0s (limits 8/4s; high => static/slideshow)
- bgm_present: OK - total silence 0s (limit 25s; high => no continuous BGM bed / narration-only mix)
- hook_added: OK - shotlist totals missing
- loudness: OK - integrated -14.3 LUFS (target -14, band -16.0..-12.0)
- voice_is_master: OK - master narration present: ['elevenlabs']
- captions_final: OK - final captions captions.v001.srt (last cue 1652s)
- caption_format: OK - captions.v001.srt: line/duration/cps within limits
- thumbnail_ready: OK - 4 thumb(s) at 1280x720, selected=yes (need >=3 + selected)
- image_resolution: OK - 92 hero PNGs, all long-edge >= 3840px
- factory_used: OK - 124 factory clip(s) staged, referenced_in_composition=True, need >= 36 (1 per 45s)

Manual confirmations:
- runtime_band.py: 27.67 min PASS
- captions: 861 cues, max line chars 42, max CPS 16.21 OK
- thumbnails: 4 at 1280x720, selected present OK

Owner gates still required before publish:
- R3 legal/rights review
- final title/thumbnail choice
- publish/schedule approval
