# P07 EVIDENCE — B2版（語同期）

- Phase `P07` / by claude-code / 2026-07-12 (JST)

## ツール判断（正直）
- **WhisperX は採用見送り**：版依存地獄（whisperx3.8.6×torch2.8 / 3.1.1×torch2.1.2×新transformers `_pytree`不整合）で `load_align_model` が動かず。
- **faster-whisper 1.2.1 へピボット**（repo既存 `gen_captions_forced.py` と同系・ctranslate2＝torch非依存＝堅実）。global env で **GPU(cuda)** 稼働。詳細 `TOOLS_INSTALLED.md`。

## 実行（実測）
```
python scripts/pd-visual-system/whisperx_align_poc.py --ep PD-2026-009-timbs
→ faster-whisper device=cuda model=medium.en / 1542 words / review 158
→ episodes/PD-2026-009-timbs/08_edit/whisperx/whisperx_words.v001.json（audio_sha付・review_reasons）
```
- review自動フラグ実証: `$42`(136.38s money)・`$10`(145.96s money)・`Tyson/Timms`(proper_noun)・`disproportionate`(174.56s)。
- 窓181語→ `remotion/src/data/timbs_word_timings.ts`（TIMBS_WORDS_WINDOW＋anchors）。

## B2（B1＋語同期・実レンダ目視）
- `remotion/src/compositions/TimbsB2.tsx`（`<TimbsB1/>` に語同期キャプション帯を重畳・DRY）＋Root登録。typecheck exit0。
- `outputs/pd-visual-system/b2_check/`：
  - frame1080＝$10k/$42kバー＋字幕「…was **$10**」の**「$10」が発話フレームで金ハイライト**（図・字幕・音声一致）
  - frame1940＝引用「grossly disproportionate」＋字幕「…grossly **disproportionate**」の**該当語が発話フレームで金ハイライト**
- B2 preview mp4 → 背景レンダ中。

## 受入基準
語単位タイムスタンプ生成 ✅／台本非上書き(ASRは時刻のみ・textは表示用) ✅／金額・年号・人名等 review_required ✅／同期を実レンダで実証 ✅。

## rollback / 限界 / 次
- rollback: `TimbsB2.tsx`＋`timbs_word_timings.ts`＋Root追記＋`08_edit/whisperx/` を戻す。B1/既存に非干渉。
- 限界: faster-whisperの語境界はwav2vec2ほど厳密でない（house lead 0.12s補正で吸収）。正本統合は`verify_caption_sync.py`ゲート通過が次段。
- 次 P08 = B3版（2.5Dを1カット・設計=P08_PLAN.md・Depth Small/SAM2 導入済）。
