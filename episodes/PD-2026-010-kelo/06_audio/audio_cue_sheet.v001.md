# 第10話 kelo 音声設計（Audio Cue Sheet・4層＋ダッキング） v001

対象: `PD-2026-010-kelo`。Codex がこの設計で BGM/SFX/環境音を配置・ミックスする。
準拠: `VIDEO_RULES.md` §11 / `docs/audio-sfx-bgm-library-plan.md`。
音源棚（実在・`H:\pd-media\library\`）: `music/{hook,opening,explainer_bed,tension_build,reveal,somber,outro,ambience}`, `ambience/amb_*.mp3`, `sfx/sfx_*.mp3`。レジストリ: `library/music_registry.v001.json` / `library/sfx_registry.v001.json`。

## 0. 4層の役割
1. **VO（ナレ）** = 最優先。`06_voice/master/VC-XXXX.mp3`。常に明瞭。
2. **BGM** = `music/<mood>` から1曲/章。控えめ。
3. **SFX** = カット/リビール/数字/テロップ出現の効果音。
4. **環境音(ambience)** = 法廷ざわめき/夜/オフィス等を薄く。

## 1. ダッキング（必須・VO最優先）
- **VOをサイドチェイン基準**にBGM・環境音を自動ダッキング。
- 目安: ナレ有り区間で **BGM −16〜−18 dB / ambience −26〜−30 dB** 下げる。SFXワンショットはVOを隠さない範囲（ピーク −12 dB目安）。
- 整音: **−14 LUFS（integrated）・true peak ≤ −1 dBTP**。VOが常に聞き取れることを最終確認。
- ナレの**頭16フレーム前**でBGM/ambienceを先行ダッキング、ナレ終わり後にゆっくり戻す。

## 2. 章別キュー（BGM/ambience/SFX）

| 章 / SPN | BGM(music/) | ambience | 主なSFX | 演出メモ |
|---|---|---|---|---|
| **フック** (本編ハイライト集) | `tension_build`→`hook` | （薄く tension_drone） | `riser_2s`, `low_boom`, `whoosh_short/medium` をカット頭に | 高速カットに同期して煽る。最後は一瞬無音→オープニングへ |
| **オープニング** | `opening`（定番） | なし | `whoosh_medium`（タイトルイン） | 既存ブランド演出。作り直さない |
| **act1** SPN0003–0008 | `somber`/`explainer_bed`（好奇心＋哀感） | `amb_night_window`・`amb_office_hum` 薄く | `data_blip`/`ui_tick`（0005アイコン組み上げ）, `page_turn`（0003地図） | 近隣紹介〜「ピンクの家」〜「それは公共の用か？」 |
| **act2** SPN0009–0013 | `explainer_bed`（臨床的） | `amb_institutional_drone` 薄く | `ui_tick`/`data_blip`（定義カード/等式 0009–0011） | 狭義 vs 広義の対比、等式の組み上げ |
| **act3** SPN0014–0017,0027 | `tension_build`→**`reveal`（0014山場）** | `amb_courtroom_room_tone` 薄く | **`gavel_knock`+`low_boom`（5–4リビール）**, `stamp_seal`（出典545 U.S.469確定）, `whoosh_short`（0016取り消し線） | 判決の山場。多数意見/反対意見/Kennedy補足を公平に |
| **act4** SPN0018–0022,0028 | `somber`（内省） | `amb_empty_hallway`・`amb_night_window` | `data_blip`/`ui_tick`（0019州カウントアップ）, `sub_drop`/`low_boom` 微（0020「何も建たず」）, `clock_tick_loop` 微（0021撤退の皮肉） | 反発→州法改正→空き地→Pfizer撤退→移築 |
| **エンディング** SPN0023–0026 | `outro`（解決・希望） | なし〜薄く | `soft_impact`+`ui_tick`（0026 Subscribe）, `riser_2s`（0025次回引き） | 総括→次回予告→CTA/フォロー誘導 |

## 3. 工程と保存先
- ナレ生成: `script.en.v001.md` の `[VO:]` → ElevenLabs → ドラフト `H:\pd-media\episodes\PD-2026-010-kelo\06_voice\draft\VC-XXXX.mp3` → マスター `…\06_voice\master\VC-XXXX.mp3`。
- ナレ計画/索引(git): `06_audio/voice_plan.v001.json` / `06_audio/narration_index.v001.json`。
- 字幕(git): forced alignment で `08_edit/captions.v001.srt`(+`.json`)。テロップと**被らせない**（位置で分離・`edit_design.v001.md` §3）。
- BGM/SFX/環境音の実体は `H:\pd-media\library\` を参照（話別が要れば `…\07_audio\` にコピー）。
- ミックスは Remotion 側のオーディオトラック or 書き出し前に整音。最終 −14 LUFS / TP ≤ −1。

## 4. 受け入れチェック
- [ ] 4層すべて入っている（VO/BGM/SFX/ambience）
- [ ] ダッキングでナレ中のBGM・環境音が下がり、VOが常に明瞭
- [ ] 山場（SPN-0014 5–4）と各テロップ出現にSFXが同期
- [ ] −14 LUFS / true peak ≤ −1 dBTP
- [ ] 字幕がナレと語単位同期、テロップ/出典と非重複
