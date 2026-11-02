# EP76 morandi → ASSEMBLY THREAD

**Written 2026-08-22 by the design/asset lane. Everything below was measured, not recalled.**
Paste-ready: this file is the whole handover. The goal is a scheduled upload, and §7 is what stands
between here and one.

---

## 1. The episode in one paragraph

`PD-2026-076-morandi` — the Morandi bridge, Genoa, 14 August 2018. 30 minutes. The subject is
**the thing the viewer does without thinking: driving over a structure somebody else is responsible
for inspecting.** State: `script_verified`, R3. The first-instance criminal judgment landed on
**16 July 2026**, five weeks before this was written, and it is the reason this episode can be the
definitive film on a topic that has seven long-form incumbents and no winner.

---

## 2. Where every material is

| what | path | measured |
|---|---|---|
| **Plates — RENDER TRUTH** | `remotion/public/morandi/img` | **120 png, all 3840×2160** |
| Plates — archive copy | `H:/pd-media/assets/ai/morandi` | 120 png (same set) |
| Plates — rejected, retired not deleted | `remotion/public/morandi/_rejected_v001` | 3 png |
| **Narration master — RENDER TRUTH** | `remotion/public/morandi/narration.mp3` | **42.2 MB, 1,842.130 s** |
| Narration master — source of truth | `E:/pd-media/episodes/PD-2026-076-morandi/06_voice/master/vc_master_v001.mp3` | same file |
| Narration index (all timings) | `episodes/PD-2026-076-morandi/06_audio/narration_index.v001.json` | 329 chunks |
| **Motion clips (i2v)** | `remotion/public/morandi/motion` | **81 of 120 so far, 1920×1080, 3.37 s each** |
| i2v raw frame dirs | `C:/Users/aab15/ae-demo/wan_frames_morandi_V###` | 81 frames each |
| Recovered stock shelf | `D:/pd-archive/<theme>/pexels__<id>__<slug>.mp4` | **742 clips and growing** |
| Stock ledger (searchable) | `E:/pd-archive/_ledger/pexels.jsonl` | one row per recovered clip |
| Footage candidates (pre-filtered) | `runs/qc/morandi_recovered_review.v001.json` | 259 of the first 503 |
| Footage review sheets | `runs/qc/morandi_recovered_sheets/` | 13 sheets, 2 read |
| Plate verdicts (sha-bound) | `runs/qc/morandi_plate_verdicts.v001.json` | **120 accept, 0 reject** |
| Plate contact sheets | `runs/qc/plate_sheets/morandi/` | 6 sheets, all read |
| **Factory pool for the film** | `remotion/public/morandi/factory` | **DOES NOT EXIST — nothing staged yet** |

> `runs/` is **gitignored**. The verdicts and sheets exist on this machine only.

## 3. The documents that bind

| what | path |
|---|---|
| machine contract | `episodes/PD-2026-076-morandi/episode_spec.v001.json` |
| **filmconfig — the assembly entry point** | `episodes/_planning/EP76_morandi_filmconfig.v001.json` |
| facts ledger (every claim) | `episodes/_planning/EP76_morandi_FACTS_LEDGER.v001.md` |
| film bible | `episodes/_planning/EP76_morandi_FILM_BIBLE.v001.md` |
| script | `episodes/_planning/EP76_morandi_script.en.v001.md` |
| **scene plan — MEASURED** | `episodes/_planning/EP76_morandi_SCENE_PLAN.v002.md` |
| footage plan | `episodes/_planning/EP76_morandi_FOOTAGE_PLAN.v001.md` |
| packaging / thumbnails | `episodes/_planning/EP76_morandi_thumb_prompts.v001.md` |
| pre-publish fact recheck | `episodes/PD-2026-076-morandi/01_research/fact_recheck.v001.md` |
| manifest | `episodes/PD-2026-076-morandi/manifest.json` |

## 4. The numbers assembly has to hit

From `episode_spec` and `SCENE_PLAN.v002`, all measured off the delivered master:

```
master            1,842.130 s          film 1,851.1 s = 30:51   band [1740, 1920] OK
cuts              492 at a 3.74 s mean
stills ceiling    157 (32% of cuts)    plates 120  -> OK
video cuts floor  335 (68% of cuts)    265 distinct at 1.26x reuse
sections          HOOK OP ACT_1..ACT_5 ENDING
figure cards      84, in the filmconfig, 13-17 per act
hookSeconds       22.4  (measured, where HOOK ends in the index)
```

**Motion clips are 3.37 s against a 3.74 s mean cut** — they will need a short loop or slightly
shorter cuts. Not a blocker; note it before the builder surprises you.

## 5. What is DONE

- spec, ledger, bible, script — `check_script_standard --slug morandi --wpm 184.0` = **12/12**
- `check_script_citations --slug morandi` = **all 218 narration lines cited, every id resolves**
- narration master delivered and verified by ffprobe, not by file size
- **all 120 plates accepted**, sha-bound, `check_plate_verdicts` **PASS**
- filmconfig written, 84 figure cards, every one a ledger row
- `check_episode_inputs` went **7 problems → 2**

## 6. What is NOT done

| # | item | note |
|---|---|---|
| 1 | **i2v: 81 of 120** | running; see §8 — the GPU is shared and that is the bottleneck |
| 2 | **Footage: 0 staged** | 742 downloaded, ~237 usable by measurement. **Nothing has entered `factory/` yet** |
| 3 | Footage review | 13 sheets exist, **2 read**. `footage_review_required` is `true` |
| 4 | `asset_manifest.v001.json` | written by `build_case_film_assets.py` once 1–3 are done |
| 5 | `morandi_film.json` | `build_case_film_generic.py --config <filmconfig>` |
| 6 | Root.tsx composition `Ep76Morandi` | **deliberately not added** — it imports `data/morandi_film.json`, and adding it before that file exists breaks the Remotion app for **every** episode |
| 7 | captions | forced-aligned after the render |
| 8 | thumbnails | 3 of 6 concepts to build; **title choice is an owner gate** |

## 7. The path to a scheduled upload

```
i2v 120/120  ->  review + stage footage  ->  asset_manifest  ->  morandi_film.json
   ->  Root.tsx  ->  preflight GREEN  ->  render (~3 h)  ->  captions + mux
   ->  check_final_acceptance --emit-receipt  ->  thumbnail + title approval
   ->  upload_schedule_case_v001.py --ep morandi
```

**Three things gate the schedule and none is technical:**

1. **`preflight_render_gate.py --ep PD-2026-076-morandi` must be GREEN.** It has failed on 25 of 32
   episodes and been overridden on 10. Its receipt already exists at
   `episodes/PD-2026-076-morandi/04_scenes/preflight_receipt.v001.json` and its only reds are §6's
   items — nothing else.
2. **The title/thumbnail pair is an owner approval** (`.claude/rules/16`). Three titles are drafted
   and all three pass `check_packaging_claims` with zero unsupported claims. Recommended: **A**.
3. **YouTube quota is exhausted today**: `spent 9919 of 10000`, **uploads possible today: 0**
   (an insert costs 1600). Resets 16:00 JST. Schedule tomorrow, not today.

## 8. THE ONE THING BLOCKING PROGRESS RIGHT NOW

**Two i2v chains are sharing one GPU and both are being slowed by it.**

```
03:38      morandi alone                  12 clips per chunk
06:06:54   an oroville (EP71) chain starts on the same card
06:07:21   morandi falls to 3 per chunk, then 1, then 0
```

ComfyUI was never crashing — its own log reads `Prompt executed in 171.81 seconds` throughout. Each
chain waits its own 600 s for a clip the other is occupying the card with, decides ComfyUI has died,
and **restarts it, destroying the other's in-flight work.**

| | now | if it had the card alone |
|---|---|---|
| **morandi** | 81/120, **8.9 min/clip** | **3.5 min/clip → 2.2 h** |
| oroville | 40/118 | — |
| shared | **5.5 h remaining** | — |

`scripts/_chain_i2v_robust.sh` now takes a **GPU-wide lock** so this cannot recur (demonstrated
refusing a live foreign holder and clearing a stale one). It does **not** decide which episode goes
first — that is an owner call, and **both chains are still running while it is made.**

**Recommendation: let morandi finish first** (39 clips, ~2.2 h solo), then oroville. Serial is
~6.5 h total and delivers one finished episode early; shared is 7 h+ and delivers neither.

## 9. Two rules assembly must not break

1. **No frame or line may imply anyone foresaw the collapse.** On 16 July 2026 the court **excluded
   article 61 no. 3 for every defendant** and **acquitted all of them of articles 432 and 437
   "perché il fatto non sussiste"**. The convictions are for negligence. This binds figure cards,
   captions, the title, the thumbnail and the description exactly as it binds narration.
2. **Every named person carries their status in the same breath.** Castellucci: *convicted at first
   instance*, *appeal announced*, *the judgment is not final*. Ferrazza: *acquitted*. The engineer
   who signed the 2017 project is **not named at all**.

## 10. The item with a date on it

**The court gave itself ninety days from 16 July 2026 to file its written reasons — on or about
14 OCTOBER 2026.** The script's ENDING says *"we will not know it for weeks."*

**If this publishes after that date, the line is false.** On the day the publish date is set,
re-check whether the *motivazioni* are deposited and whether an appeal has been formally lodged. If
either has happened, ACT_5's last three lines and the description are rewritten **before**
scheduling. It is a splice, not a re-render. Full detail in `fact_recheck.v001.md` §3.

## 11. Cost so far

`10.20 USD` — 1.30 for the ACT_1 pace measurement, 8.90 for the narration master. No render, no
image cost, no footage licence. The recovered stock is Pexels-licensed, commercial use permitted.
