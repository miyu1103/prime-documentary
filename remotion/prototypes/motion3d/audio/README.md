# audio — challenge #2: audio-reactive visuals

Visuals synced to the finished mix (music+voice) via `@remotion/media-utils`
(`useAudioData` + `visualizeAudio`). The picture breathes with the narrator →
kills drop-off in low-energy stretches (v2 row 16 retention).

- `AudioReactive.tsx`: pulsing core (bass), circular spectrum (freq bins),
  waveform, background glow (total energy), title scale on voice. `<Audio>` plays
  the source so the render carries sound. Deps: `@remotion/media-utils@4.0.484`.
- Drive from `visualizeAudio({fps,frame,audioData,numberOfSamples})`; guard
  `if(!audioData) return null` (media-utils delays render until loaded).

Port target: an overlay layer usable under Bookends / chapter cards.
