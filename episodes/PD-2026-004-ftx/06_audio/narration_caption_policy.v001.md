# PD-2026-004-ftx — Narration & Caption Sync Policy (owner-directed, 2026-06-18)

Owner directive: **"ナレーションと字幕はぴったり一致。ナレーションの速度で調整して。"**

## Rules
- **Exact match:** captions are **force-aligned** to the actual recorded narration (word/phrase
  timestamps), so on-screen text and spoken words line up exactly — no drift. Same method as ep3
  (305 cues, re-forced-aligned after retiming).
- **Hit 12:00 via narration speed, not cuts:** lock total runtime to **12:00** by adjusting narration
  tempo (FFmpeg `atempo`, pitch-preserving) rather than deleting script content. ep3 reference used
  `atempo ≈ 0.84`; pick the factor that lands the final master at 12:00 after bookends/beats.
- **Order of operations:** (1) record narration at natural pace → (2) measure duration → (3) apply
  `atempo` to fit 12:00 (plus opening/end-card bookends) → (4) force-align captions to the FINAL,
  tempo-adjusted master so they match perfectly.
- Keep narration intelligible: if the atempo factor would distort the voice, rebalance with small
  pauses/beat trims instead of an extreme stretch.
- Caption style: clean, readable, high-contrast (mobile-legible); 1–2 lines; no auto-caption errors —
  derived from the locked script text, then timed by alignment.

Related: [[feedback_video_natural_style]] (quality-first finish). Tooling: forced alignment + FFmpeg.
