# 第15話 theranos 音声設計（Audio Cue Sheet・4層＋ダッキング） v001 — SERIES FINALE

対象: `PD-2026-015-theranos`。Codex がこの設計で BGM/SFX/環境音を配置・ミックスする。
準拠: `VIDEO_RULES.md` §11 / `docs/audio-sfx-bgm-library-plan.md`。
音源棚（実在・`H:\pd-media\library\`）: `music/{hook,opening,explainer_bed,tension_build,reveal,somber,outro,ambience}`, `ambience/amb_*.mp3`, `sfx/sfx_*.mp3`。レジストリ: `library/music_registry.v001.json` / `library/sfx_registry.v001.json`。

> **R3注意**: 音はあくまで象徴。**実在人物を連想させる音声引用・なりすまし音は使わない**。山場（4件有罪リビール）は印象的に演出してよいが、**断定的“有罪”の煽りに偏らせない**（患者関連は無罪/評決不成立。§2 act3 参照）。

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

実ファイル例（`H:\pd-media\library\music\<mood>\`）: hook=`mus_20260614_hook_glass_air_bed_v1.mp3` / opening=`mus_20260614_opening_measured_arpeggio_v1.mp3` / explainer_bed=`mus_20260614_explainer_bed_soft_explainer_v1.mp3` / tension_build=`mus_20260614_tension_build_courtroom_horizon_v1.mp3` / reveal=`mus_20260614_reveal_verdict_at_dawn_v1.mp3` / somber=`mus_20260614_somber_ledger_of_ash_v1.mp3` / outro=`mus_20260614_outro_last_frame_v1.mp3`。SFXは `sfx/sfx_<name>.mp3`、ambienceは `ambience/amb_<name>.mp3`。

| 章 / SPN | BGM(music/) | ambience | 主なSFX(sfx/) | 演出メモ |
|---|---|---|---|---|
| **フック** (本編ハイライト集) | `tension_build`→`hook` | （薄く `amb_tension_drone`） | `riser_2s`, `low_boom`, `whoosh_short/medium` をカット頭に。$9B→$0崩落に `sub_drop`+`low_boom` | 高速カットに同期して煽る。最後は一瞬無音→オープニングへ |
| **オープニング** | `opening`（定番） | なし | `whoosh_medium`（タイトルイン） | 既存ブランド演出。作り直さない |
| **act1** SPN0002,0003,0023,0004,0005,0006 | `explainer_bed`（好奇心＋上昇感） | `amb_office_hum`・`amb_night_window` 薄く | `data_blip`/`ui_tick`（0005評価額グラフ・0023肩書きカード積み上げ）, `page_turn`（0003年表）, `camera_shutter` 微（0001雑誌表紙の象徴） | 創業〜「~$9B・著名な取締役会・Walgreens限定」〜「物語が問いを止める」 |
| **act2** SPN0007,0008,0009,0010,0011 | `tension_build`（疑念の上昇） | `amb_office_hum`・`amb_institutional_drone` 薄く | `whoosh_short`+`paper_rustle`（0007調査報道）, `data_blip`（0008差替）, `sub_drop` 微（0010 SEC・会社解散・$9B→0）, `ui_tick`（0011 Failure/Fraud並置） | WSJ調査→「他社の機械」暴露→規制→2018 SEC和解→解散→「失敗 or 詐欺」 |
| **act3** SPN0012,0024,0013,0014,0015,0016 | `tension_build`→**`reveal`（0013山場 `verdict_at_dawn`）** | `amb_courtroom_room_tone` 薄く | **`gavel_knock`+`low_boom`（0013 4件有罪リビール）**, `stamp_seal`（評決ボード/記録確定）, `ui_tick`（0014 無罪/評決不成立を別音で控えめ）, `binder_lock` 微（0016量刑確定） | 法定義（詐欺＝欺く意図）→検察vs弁護→2022評決ボード→**患者は無罪・3件評決なし（断定有罪に煽らない）**→無罪≠潔白/Balwani全12件→量刑 約11年3か月 |
| **act4** SPN0017,0018,0019 | `somber`（内省） | `amb_empty_hallway`・`amb_night_window` | `ui_tick`/`data_blip`（0018境界の等式組み上げ）, `soft_impact` 微（0019 stakes対比） | 「Fake it till you make it」は多くは合法→境界＝意図と依拠→アプリ損失 vs 検査の損失 |
| **エンディング** SPN0020,0021,0022 | `outro`（解決・希望） | なし〜薄く | `dust_swell`/`riser_2s`（0020 総括の引き）, `soft_impact`+`ui_tick`（0022 Subscribe） | シリーズ総括「many costumes・where is the line?」→線を引き直し続ける→CTA/フォロー誘導 |

## 3. 工程と保存先
- ナレ生成: `script.en.v001.md` の `[VO:]` → ElevenLabs → ドラフト `H:\pd-media\episodes\PD-2026-015-theranos\06_voice\draft\VC-XXXX.mp3` → マスター `…\06_voice\master\VC-XXXX.mp3`。
- ナレ計画/索引(git): `06_audio/voice_plan.v001.json` / `06_audio/narration_index.v001.json`。
- 字幕(git): forced alignment で `08_edit/captions.v001.srt`(+`.json`)。テロップと**被らせない**（位置で分離・`edit_design.v001.md` §3）。
- BGM/SFX/環境音の実体は `H:\pd-media\library\` を参照（話別が要れば `…\07_audio\` にコピー）。
- ミックスは Remotion 側のオーディオトラック or 書き出し前に整音。最終 −14 LUFS / TP ≤ −1。

## 4. 受け入れチェック
- [ ] 4層すべて入っている（VO/BGM/SFX/ambience）
- [ ] ダッキングでナレ中のBGM・環境音が下がり、VOが常に明瞭
- [ ] 山場（SPN-0013 4件有罪リビール）と各テロップ出現にSFXが同期
- [ ] **R3**: 実在人物を連想させる音声引用/なりすましなし・**有罪の断定煽りに偏らない**（患者=無罪/3件=評決不成立）
- [ ] −14 LUFS / true peak ≤ −1 dBTP
- [ ] 字幕がナレと語単位同期、テロップ/出典と非重複
- [ ] **公開前 法務レビュー（R3）後に音声ミックスを最終固定**（exact revision）
