# P07 PLAN — WhisperX 語同期（設計のみ・実行はP07到達＋venv導入後）

> エージェント調査(2026-07-12)。**実行しない**（現在P06）。P07で使う。

## 方針（invariant14＝二重実装しない・台本が正本）
- **既存 `scripts/gen_captions_forced.py`（faster-whisper medium.en 強制アラインメント）を再利用**。`resolve_text_source()`＝narration_index/voice_plan から**台本の逐語**を取り、**ASRは時刻付けのみ**（テキストを上書きしない）。窓分割でドリフト無し。
- 独立ゲート `scripts/verify_caption_sync.py`（lag/exact_pct等の辞書契約）に**P07出力を通す**（バイパスしない）。`CAPTION_LEAD_SECONDS≈0.2-0.3s`の前倒し補正を踏襲。

## Remotion 側
- `RoughCut.tsx CaptionBand`＝cue単位（既存）。`motionkit/KineticCaptions.tsx`＝**word時刻が合成値**→ optional `wordTimings:{word,startFrame}[]` を追加して実時刻駆動（無ければ従来動作＝非退行）。
- **core5 は変更不要**（既に `dur` 駆動＋`<Sequence from={wordFrame}>`装着契約）。リビールは `from=Math.round(word.start*fps)` で発火。

## 導入（隔離venv `D:\PD_AI_Tools\WhisperX\.venv`・背景導入中）
```
pip install torch==2.1.2+cu118 torchaudio==2.1.2+cu118 --index-url .../cu118
pip install whisperx==3.1.1
```
CLI: `whisperx <mp3> --model large-v3 --language en --align_model WAV2VEC2_ASR_LARGE_LV60K_960H --device cuda --compute_type float16 --output_format json`。ライセンス記録: whisper large-v3=MIT / wav2vec2 aligner を LICENSE_REGISTER へ。OOM時 int8/cpu。

## スクリプト骨子（P07で作成）`scripts/pd-visual-system/whisperx_align_poc.py`
- 入力: `--ep`, `--audio`(既定 timbs_final_mix_v001.mp3・VO masterで上書き可), 台本逐語＋窓[start,end]。
- 処理: ASRパス(diff用)＋**forced-alignパス(台本segmentsを`whisperx.align`)**→ word_segments{word,start,end,score}。ASRは上書きしない。未アライン語(数値/記号)は窓内補間＋conf0＋requires_review。
- 出力(immutable revision): `08_edit/whisperx/whisperx_words.v001.json`（words[]＋model/audio_sha）＋`whisperx_diff.v001.json`。任意 `remotion/src/data/timbs_word_timings.ts`（--emit-ts・既存を--forceなしで上書きしない）。
- **review_required 規則**（regex→NER）: money `\$[\d,]+`／year `(1[6-9]\d\d|20\d\d)`／statute `§/U.S.C./Amendment/v.`／case_number 反訳・reporter cite／court 句一致／name・place spaCy(GPE/PERSON)＋fallback／unaligned。フラグ語はブロックせず**人手確認**（誤時刻＝事実誤表示 invariant1/11）。

## データフロー
mp3 → whisperx.align(台本) → whisperx_words.v001.json → timbs_word_timings.ts(WordTiming) → Remotion(`wordFrame=round(start*fps)`) → core5 `<Sequence from>` / KineticCaptions wordTimings。

## 制約 / 注意
台本正本・ASR非上書き・数値/固有名詞は review／隔離venv／verify_caption_syncゲート維持／phase到達まで実行禁止。venvは導入直後に whisperx smoke 要。
