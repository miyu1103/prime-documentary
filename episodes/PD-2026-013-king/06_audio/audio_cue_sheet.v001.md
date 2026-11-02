# 第13話 king 音声設計（Audio Cue Sheet・4層＋ダッキング） v001

対象: `PD-2026-013-king`（Maryland v. King / 逮捕時DNA採取）。Codex がこの設計で BGM/SFX/環境音を配置・ミックスする。
準拠: `VIDEO_RULES.md` §11 / `docs/audio-sfx-bgm-library-plan.md`。
音源棚（実在・`H:\pd-media\library\`）: `music/{hook,opening,explainer_bed,tension_build,reveal,somber,outro}`, `ambience/amb_*.mp3`, `sfx/sfx_*.mp3`。レジストリ: `library/music_registry.v001.json` / `library/sfx_registry.v001.json`。
題材の節度: 性犯罪題材のため**煽りすぎない**。衝撃SFXは判決の山場(0012)に集中させ、ACT Iの綿棒/照合は**ソバー**に。

## 0. 4層の役割
1. **VO（ナレ）** = 最優先。`06_voice/master/VC-XXXX.mp3`。常に明瞭。
2. **BGM** = `music/<mood>` から1曲/章。控えめ。
3. **SFX** = カット/リビール/数字/テロップ出現の効果音。
4. **環境音(ambience)** = 法廷ざわめき/夜/オフィス/施設ドローン等を薄く。

## 1. ダッキング（必須・VO最優先）
- **VOをサイドチェイン基準**にBGM・環境音を自動ダッキング。
- 目安: ナレ有り区間で **BGM −16〜−18 dB / ambience −26〜−30 dB** 下げる。SFXワンショットはVOを隠さない範囲（ピーク −12 dB目安）。
- 整音: **−14 LUFS（integrated）・true peak ≤ −1 dBTP**。VOが常に聞き取れることを最終確認。
- ナレの**頭16フレーム前**でBGM/ambienceを先行ダッキング、ナレ終わり後にゆっくり戻す。

## 2. 章別キュー（BGM/ambience/SFX）

| 章 / SPN | BGM(music/) | ambience | 主なSFX | 演出メモ |
|---|---|---|---|---|
| **フック** (本編ハイライト集) | `tension_build`→`hook` | （薄く `amb_tension_drone`） | `sfx_riser_2s`, `sfx_low_boom`, `sfx_whoosh_short/medium` をカット頭に | 高速カットに同期して煽る。最後は一瞬無音→オープニングへ |
| **オープニング** SPN-0002 | `opening`（定番） | なし | `sfx_whoosh_medium`（タイトルイン） | 既存ブランド演出（`BrandOpening`）。作り直さない |
| **act1** SPN0003–0007 | `somber`/`explainer_bed`（緊張＋抑制） | `amb_night_window`・`amb_office_hum` 薄く | `sfx_page_turn`（0003地図/年表）, `sfx_data_blip`（0005 DB走査）, `sfx_ui_tick`（0005 MATCH点灯・1発のみ・控えめ） | 逮捕→綿棒→DB照合→一致。**「綿棒＝逮捕理由」と誤読させない**ソバーな進行。0005の MATCH は衝撃音を抑える |
| **act2** SPN0008–0011,0022 | `explainer_bed`（臨床的） | `amb_institutional_drone` 薄く | `sfx_ui_tick`/`sfx_data_blip`（0009等式/0011 CODISノード点灯）, `sfx_whoosh_short`（0010 指紋→DNAモーフ） | 「指紋 or 捜索」の対比、CODIS規模、指紋 vs 設計図。冷静・分析的 |
| **act3** SPN0012–0015,0023 | `tension_build`→**`reveal`（0012山場）** | `amb_courtroom_room_tone` 薄く | **`sfx_gavel_knock`+`sfx_low_boom`（5–4リビール）**, `sfx_stamp_seal`（出典 569 U.S.435 確定）, `sfx_whoosh_short`/`sfx_ui_tick`（0015 引用句が刻まれる） | 判決の山場。多数意見(Kennedy)・反対意見(Scalia＋リベラル3名)を公平に。0014の異色連合は`sfx_soft_impact`で1拍 |
| **act4** SPN0016–0018 | `somber`（内省） | `amb_empty_hallway`・`amb_night_window` | `sfx_soft_impact` 微（0017 天秤）, `sfx_sub_drop`/`sfx_low_boom` 微（0018「一票の取引」） | 全米への波及→事件解決と単なる逮捕者登録の天秤→一票で決まった取引。傾けすぎない |
| **エンディング** SPN0019–0021 | `outro`（解決・問い） | なし〜薄く | `sfx_ui_tick`（0020 5語の積み上げ）, `sfx_riser_2s`/`sfx_whoosh_medium`（0021 次回引き） | 総括（身元確認 ／ 捜査）→シリーズ統合(body)→次回(home)予告。CTAは固定エンドカード（`BrandEndcard`）に内包 |

> 各moodフォルダは v1/v2（reveal は v1〜v3）あり。章ごとに1曲を選び固定。実体例: `music/reveal/mus_20260614_reveal_verdict_at_dawn_v1.mp3`（0012山場の候補）。

## 3. 工程と保存先
- ナレ生成: `script.en.v001.md` の `[VO:]` → ElevenLabs → ドラフト `H:\pd-media\episodes\PD-2026-013-king\06_voice\draft\VC-XXXX.mp3` → マスター `…\06_voice\master\VC-XXXX.mp3`。
- ナレ計画/索引(git): `06_audio/voice_plan.v001.json` / `06_audio/narration_index.v001.json`。
- 字幕(git): forced alignment で `08_edit/captions.v001.srt`(+`.json`)。テロップと**被らせない**（位置で分離・`edit_design.v001.md` §3）。
- BGM/SFX/環境音の実体は `H:\pd-media\library\` を参照（話別が要れば `…\07_audio\` にコピー）。
- ミックスは Remotion 側のオーディオトラック or 書き出し前に整音。最終 −14 LUFS / TP ≤ −1。

## 4. 受け入れチェック
- [ ] 4層すべて入っている（VO/BGM/SFX/ambience）
- [ ] ダッキングでナレ中のBGM・環境音が下がり、VOが常に明瞭
- [ ] 山場（SPN-0012 5–4・出典 569 U.S. 435）と各テロップ出現にSFXが同期
- [ ] **ACT I（綿棒/照合）はソバー**＝衝撃SFXを過剰に当てていない／煽りで誤読を生まない
- [ ] −14 LUFS / true peak ≤ −1 dBTP
- [ ] 字幕がナレと語単位同期、テロップ/出典と非重複
