EP64 MEMPHIS — replacement plates, Codex paste batches
=======================================================

Batches:      3 files (batch_01.txt … batch_03.txt)
Plates:       16 total
  batch_01 — TIER A, 2 plates (M237, M238). NEEDED NOW: these unblock the 2026-08-18 booking.
  batch_02 — TIER B backlog, 7 plates (M239–M245).
  batch_03 — TIER B backlog, 7 plates (M246–M252).

Images:       32 files (TWO per prompt — the second is the same subject from a second
              camera position, suffixed b).

Deliver to:   episodes/PD-2026-064-memphis/05_visuals/approved/

Filenames:    M237.png and M237b.png, M238.png and M238b.png, … exactly as named on the
              delivery line of each prompt block. PNG. No other suffixes, no _01/_02.

Resolution:   long edge at least 3840 px (3840x2160, 16:9). Anything smaller is rejected.

DO NOT RENUMBER. Ids start at M237 because M001–M236 already exist on disk and each one has
a reviewed verdict recorded against it. A replacement must never overwrite a reviewed plate id
(CLAUDE invariant 6).

Every prompt block carries its own NEGATIVE line and its own WHY THE LAST ONE FAILED line.
Both are repeated in full under every prompt on purpose — a paste has no memory of the
prompt before it, and the failure note is the only thing that stops the same image coming back.

Standing rules, repeated at the top of every batch file:
  One motif per prompt. TWO images per prompt (second file suffixed b).
  No text anywhere in any image. No child. No identifiable face. No readable document.

Note on the two-image rule: the source brief (EP64_memphis_REPLACEMENT_SDXL_BATCH.v001.md §0)
was written for a local SDXL run and said one prompt / one image. These are Codex deliveries and
follow the Codex convention of two camera positions per prompt, so the owner picks the frame.
