# 第14話 lange 音声設計（Audio Cue Sheet・4層＋ダッキング） v001

対象: `PD-2026-014-lange`（Lange v. California, 2021）。Codex がこの設計で BGM/SFX/環境音を配置・ミックスする。
準拠: `VIDEO_RULES.md` §11 / `docs/audio-sfx-bgm-library-plan.md`。
音源棚（実在・`H:\pd-media\library\`）: `music/{hook,opening,explainer_bed,tension_build,reveal,somber,outro,ambience}`, `ambience/amb_*.mp3`, `sfx/sfx_*.mp3`。レジストリ: `library/music_registry.v001.json` / `library/sfx_registry.v001.json`。
**この話のトーン**: 緊張（追跡・扉）→説明（聖域としての家）→山場（2021・9–0・差戻し）→内省（明快な線ではない）→締め（玄関の一線）＋次回フィナーレ予告。住居プライバシー vs 警察の安全は音でも公平に（どちらかを煽り過ぎない）。

## 0. 4層の役割
> **ナレ＝ElevenLabsで生成OK（課金承認待ち不要・止まらず進める）**。VIDEO_RULES §11／§8（ノンストップ運用）準拠。ナレ生成ゲートで停止しない（重大な事実誤り・権利リスク発見時のみ即停止）。手順は §3。
1. **VO（ナレ）** = 最優先。`06_voice/master/VC-XXXX.mp3`。常に明瞭。
2. **BGM** = `music/<mood>` から1曲/章。控えめ。
3. **SFX** = カット/リビール/数字/テロップ出現/扉・足の効果音。
4. **環境音(ambience)** = 夜の住宅街/法廷ざわめき/廊下等を薄く。

## 1. ダッキング（必須・VO最優先）
- **VOをサイドチェイン基準**にBGM・環境音を自動ダッキング。
- 目安: ナレ有り区間で **BGM −16〜−18 dB / ambience −26〜−30 dB** 下げる。SFXワンショットはVOを隠さない範囲（ピーク −12 dB目安）。
- 整音: **−14 LUFS（integrated）・true peak ≤ −1 dBTP**。VOが常に聞き取れることを最終確認。
- ナレの**頭16フレーム前**でBGM/ambienceを先行ダッキング、ナレ終わり後にゆっくり戻す。

## 2. 章別キュー（BGM/ambience/SFX）

| 章 / SPN | BGM(music/) | ambience | 主なSFX | 演出メモ |
|---|---|---|---|---|
| **フック** (本編ハイライト集) | `tension_build`→`hook` | （薄く `amb_tension_drone`） | `riser_2s`, `low_boom`, `whoosh_short/medium` をカット頭に。**0001/0005の「足が扉を止める」瞬間に `soft_impact`+`sub_drop`** | 高速カットに同期して煽る。最後は一瞬無音→オープニングへ |
| **オープニング** | `opening`（定番） | なし | `whoosh_medium`（タイトルイン） | 既存ブランド演出。作り直さない |
| **act1** SPN0001,0003–0007 | `tension_build`（追跡の緊張）→`explainer_bed`（0006で整理） | `amb_night_window`（夜の住宅街）薄く | **`soft_impact`+`sub_drop`（0005 扉の下の足＝立入）**, `page_turn`/`data_blip`（0003地図ピン・0004距離ラベル）, `ui_tick`（0007 等式組み上げ）, `whoosh_short`（0006 "DUI" 取り消し線） | 追跡→ガレージ→立入→「争点は立入であってDUIではない」→州の自動ルール主張 |
| **act2** SPN0008–0012,0022 | `explainer_bed`（臨床的・聖域の説明） | `amb_institutional_drone` 薄く | `ui_tick`/`data_blip`（0009 exigency 3アイコン・0022 軽犯罪スケール）, `paper_rustle`（0010 歴史/伝統）, `low_boom` 微（0011 対立の重み） | 家＝プライバシーの高地、exigent circumstances、hot pursuit、軽犯罪の振れ幅、対立する両論を公平に |
| **act3** SPN0013–0016,0023 | `tension_build`→**`reveal`（0013山場）** | `amb_courtroom_room_tone` 薄く | **`gavel_knock`+`low_boom`（0013 9–0リビール）**, `stamp_seal`（出典 594 U.S. 295 確定／0016 Vacated & remanded 押印）, `ui_tick`（0014 factor/trigger 対置）, `page_turn`（0023 コモンローへ遡る）, `whoosh_short`（0015 別意見の分岐） | 判決の山場。Kagan法廷意見・Roberts＋Alito別意見を公平に。**9–0は“判決の全員一致”であり“意見の一致ではない”**ことを音でも誇張しない |
| **act4** SPN0017–0018 | `somber`（内省・明快な線ではない） | `amb_empty_hallway` 薄く | `data_blip`/`ui_tick` 微（0018 揺れる境界線）, `clock_tick_loop` 微（判断が増える含み） | 実務上の帰結→「クリーンな線ではない、しかし家を守った」 |
| **エンディング** SPN0019–0021 | `outro`（解決・余韻）→`reveal` 微（0021 次回引き） | `amb_night_window` ごく薄く〜なし | `soft_impact`（0019 玄関の一線）, `riser_2s`（0021 フィナーレ予告引き）, **エンドカードで `whoosh_medium`+`ui_tick`（Subscribe）** | 玄関先＝最も守られる一線→シリーズ統合→フィナーレ予告→CTA/フォロー誘導 |

> 実在ファイル例（棚と一致）: BGM `music/tension_build/mus_20260614_tension_build_courtroom_horizon_v1.mp3`, `music/reveal/mus_20260614_reveal_verdict_at_dawn_v1.mp3`, `music/somber/mus_20260614_somber_ledger_of_ash_v1.mp3`, `music/outro/mus_20260614_outro_last_frame_v1.mp3`。SFX `sfx/sfx_gavel_knock.mp3`, `sfx/sfx_stamp_seal.mp3`, `sfx/sfx_low_boom.mp3`, `sfx/sfx_soft_impact.mp3`, `sfx/sfx_sub_drop.mp3`, `sfx/sfx_riser_2s.mp3`, `sfx/sfx_whoosh_short.mp3`, `sfx/sfx_whoosh_medium.mp3`, `sfx/sfx_ui_tick.mp3`, `sfx/sfx_data_blip.mp3`, `sfx/sfx_page_turn.mp3`, `sfx/sfx_paper_rustle.mp3`, `sfx/sfx_clock_tick_loop.mp3`。環境音 `ambience/amb_night_window.mp3`, `amb_courtroom_room_tone.mp3`, `amb_institutional_drone.mp3`, `amb_empty_hallway.mp3`, `amb_tension_drone.mp3`。

## 3. 工程と保存先
- ナレ生成: `script.en.v001.md` の `[VO:]` → **ElevenLabs（生成OK・課金承認待ち不要・止まらず進める）** → ドラフト `H:\pd-media\episodes\PD-2026-014-lange\06_voice\draft\VC-XXXX.mp3` → マスター `…\06_voice\master\VC-XXXX.mp3`。台本本文（`[VO:]`）は一字一句変えない。
- ナレ計画/索引(git): `06_audio/voice_plan.v001.json` / `06_audio/narration_index.v001.json`。
- 字幕(git): forced alignment で `08_edit/captions.v001.srt`(+`.json`)。テロップと**被らせない**（位置で分離・`edit_design.v001.md` §3）。
- BGM/SFX/環境音の実体は `H:\pd-media\library\` を参照（話別が要れば `…\07_audio\` にコピー）。
- ミックスは Remotion 側のオーディオトラック or 書き出し前に整音。最終 −14 LUFS / TP ≤ −1。

## 4. 受け入れチェック
- [ ] 4層すべて入っている（VO/BGM/SFX/ambience）
- [ ] ダッキングでナレ中のBGM・環境音が下がり、VOが常に明瞭
- [ ] 山場（SPN-0013 9–0・出典 594 U.S. 295）と各テロップ出現にSFXが同期
- [ ] **「扉の下の足＝立入」（SPN-0001/0005）に効果音が当たり、決定的ビートが立っている**
- [ ] −14 LUFS / true peak ≤ −1 dBTP
- [ ] 字幕がナレと語単位同期、テロップ/出典と非重複
- [ ] 中立：住居プライバシー側・警察の安全側のどちらも音で煽り過ぎていない（9–0を“意見の全員一致”と誤認させる演出をしていない）
