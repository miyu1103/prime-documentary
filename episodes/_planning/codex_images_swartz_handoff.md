# Codex hand-off prompt — EP23 Aaron Swartz — IMAGE GENERATION ONLY

> Paste the block below into the Codex app. It generates the 54 episode stills and NOTHING else
> (no narration, captions, music, edit, or render). Each numbered prompt in the source file is already a
> self-contained giant mega-prompt — generate one image per block, in order.

---

TASK: Image generation ONLY for Prime Documentary EP23 ("The Internet's Own Boy" — Aaron Swartz).
Generate the 54 hero stills exactly as specified. Do NOT do narration, captions, music, editing, or rendering —
images only. Work per the design doc; do not improvise, reinterpret, or invent.

SOURCE OF TRUTH (use verbatim, do not rewrite):
- episodes/PD-2026-023-swartz/04_scenes/codex_image_prompts.v001.md
  (identical copy: Appendix A of episodes/_planning/codex_prompt_swartz.md)
- It contains 54 SELF-CONTAINED giant mega-prompts: EP23-IMG-001 … EP23-IMG-054. Each block already includes its
  SCENE + STYLE + SAFETY + NEGATIVE + SPECS. Generate each image straight from its own block — nothing else needed.

WHAT TO DO:
1. For each EP23-IMG-NNN block (001 through 054, in order): generate EXACTLY ONE image from that block.
   No candidate pool, no variants. Use that block's SCENE as the positive prompt and its NEGATIVE as the negative.
2. Output: 16:9 landscape, long edge >= 3840 px (3840x2160), highest quality.
3. Save each as PNG to: H:\pd-media\episodes\PD-2026-023-swartz\05_visuals\selected\EP23-IMG-NNN.png
   (zero-padded, e.g. EP23-IMG-007.png). If a file already exists, skip it (do not regenerate, do not duplicate).
4. After generating a shot, check it against that block's SAFETY/SPECS. Regenerate ONLY that one shot if it shows
   any of: a real-person face or likeness (especially Aaron Swartz), any self-harm / method / body / death-scene
   imagery, a real logo / brand / seal / identifiable building (Reddit, MIT, JSTOR, Creative Commons, YouTube,
   Wikipedia, any government/court seal, the real Capitol/courthouse/MIT campus), readable text/letters/numbers,
   or broken anatomy. Otherwise keep it.

HARD RULES (apply to every image — a violation = reject and regenerate):
- Symbolic reconstruction only; nothing looks like an authentic photo, news footage, or surveillance.
- NO real-person face or likeness of anyone. People are anonymous (from behind, cropped, silhouette, hands only,
  out of focus). NEVER a likeness of Aaron Swartz or any prosecutor/judge/official/family member.
- NO self-harm, suicide, method, body, note, blood, rope/noose, pills, window/ledge, or any death-scene imagery.
  This is a sensitive episode; the ending stills are restrained and hopeful-melancholy (empty chair, door ajar,
  light), never morbid.
- NO real logo, brand, seal, or identifiable building — build archetypal generic equivalents.
- NO readable text baked into the image. All on-screen text, the "988 Suicide & Crisis Lifeline" lower-third,
  names, dates, the dedication, and the bookends are added later in Remotion — leave the reserved negative space.
- Brand palette: black + midnight-navy base, electric blue #1F6BFF, muted gold #E5B53A, silver. No teal-orange,
  no candy neon.

DO NOT:
- Do NOT generate narration, captions, music, the edit, the render, or thumbnails in this task. Images only.
- Do NOT upload, publish, or call any paid non-image API. Do NOT rewrite the prompts or the script.
- Do NOT use NVENC or touch Remotion here. Just produce the 54 stills.

WHEN DONE:
- Confirm all 54 files exist (EP23-IMG-001.png … EP23-IMG-054.png) at the path above, each long edge >= 3840 px,
  and report any shot you had to regenerate and why. Then STOP — the rest of the build is a separate step.
