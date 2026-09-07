# 第11話 mahanoy 音声設計（Audio Cue Sheet・4層＋ダッキング） v001

対象: `PD-2026-011-mahanoy`（Mahanoy v. B.L. / 学校外投稿と生徒の言論の自由）。Codex がこの設計で BGM/SFX/環境音を配置・ミックスする。
準拠: `VIDEO_RULES.md` §11 / `docs/audio-sfx-bgm-library-plan.md`。
音源棚（実在・`H:\pd-media\library\`）: `music/{hook,opening,explainer_bed,tension_build,reveal,somber,outro,ambience}`, `ambience/amb_*.mp3`, `sfx/sfx_*.mp3`。レジストリ: `library/music_registry.v001.json` / `library/sfx_registry.v001.json`。

> 広告安全（最重要）: ナレは投稿の罵倒語を**読まない**（描写のみ）。SFX/BGMでそれを“強調”する演出もしない。生徒（未成年）が題材のため、煽りすぎず落ち着いたトーンを基調にする。

## 0. 4層の役割
1. **VO（ナレ）** = 最優先。`06_voice/master/VC-XXXX.mp3`。常に明瞭。
2. **BGM** = `music/<mood>` から1曲/章。控えめ。
3. **SFX** = カット/リビール/数字/テロップ出現の効果音。
4. **環境音(ambience)** = 教室ざわめき/廊下/夜/法廷の room tone 等を薄く。

実在ファイル例（棚に存在）: music は各moodに `mus_20260614_<mood>_*_v1/v2.mp3`（hook=glass_air_bed / opening=measured_arpeggio / explainer_bed=soft_explainer / tension_build=courtroom_horizon / reveal=hidden_system_clicks・verdict_at_dawn / somber=ledger_of_ash / outro=last_frame）。sfx は `sfx_gavel_knock / low_boom / riser_2s / stamp_seal / ui_tick / data_blip / whoosh_short / whoosh_medium / soft_impact / sub_drop / page_turn / clock_tick_loop / camera_shutter / paper_rustle / dust_swell / binder_lock` 等。ambience は `amb_office_hum / amb_empty_hallway / amb_night_window / amb_institutional_drone / amb_courtroom_room_tone / amb_tension_drone`。

## 1. ダッキング（必須・VO最優先）
- **VOをサイドチェイン基準**にBGM・環境音を自動ダッキング。
- 目安: ナレ有り区間で **BGM −16〜−18 dB / ambience −26〜−30 dB** 下げる。SFXワンショットはVOを隠さない範囲（ピーク −12 dB目安）。
- 整音: **−14 LUFS（integrated）・true peak ≤ −1 dBTP**。VOが常に聞き取れることを最終確認。
- ナレの**頭16フレーム前**でBGM/ambienceを先行ダッキング、ナレ終わり後にゆっくり戻す。

## 2. 章別キュー（BGM/ambience/SFX）

| 章 / SPN | BGM(music/) | ambience | 主なSFX | 演出メモ |
|---|---|---|---|---|
| **フック** (本編ハイライト集) | `tension_build`(courtroom_horizon)→`hook`(glass_air_bed) | （薄く `amb_tension_drone`） | `riser_2s`, `low_boom`, `whoosh_short/medium` をカット頭に / `camera_shutter`（スクショ） | 高速カットに同期して煽る。最後は一瞬無音→オープニングへ。罵倒は出さない |
| **オープニング** SPN0002 | `opening`(measured_arpeggio) | なし | `whoosh_medium`（タイトルイン）, `page_turn`（条文/門の描画） | 既存ブランド演出（`BrandOpening`）。作り直さない |
| **act1** SPN0003–0008,0028 | `somber`(ledger_of_ash)／`explainer_bed`(soft_explainer)（哀感＋臨床） | `amb_night_window`（0001/0005 夜のスマホ）・`amb_office_hum` 薄く | `ui_tick`/`data_blip`（0003地図ピン/0004昇降の含意）, **`camera_shutter`（0006スクショで固定）**, `whoosh_short`（0006“消える”） | Brandi の投稿〜スクショ拡散〜JV1年間の懲戒〜「学校の命令 vs 生徒の声」。CENSOREDを音で強調しない |
| **act2** SPN0026,0009–0013 | `explainer_bed`(soft_explainer)（説明的・臨床的） | `amb_institutional_drone` 薄く（0026/0009学校・歴史）, `amb_empty_hallway` 微 | `page_turn`/`ui_tick`（0009/0026 年表・腕章）, `data_blip`（0010基準カード）, **`whoosh_short`（0012“門が消える”）**, `clock_tick_loop` 微（0013 24h際限なさ） | 1965腕章→Tinker(1969)→"substantial disruption"→スマホが門を消す→“止まる場所がない”危険 |
| **act3** SPN0014–0018,0027 | `tension_build`(courtroom_horizon)→**`reveal`(verdict_at_dawn)（0014山場）** | `amb_courtroom_room_tone` 薄く | **`gavel_knock`+`low_boom`（0014 8–1リビール）**, `stamp_seal`（出典594 U.S.180確定）, `data_blip`（0016天秤/0017三例点灯）, `low_boom` 微（0018 Thomas単独反対） | 判決の山場。多数意見(Breyer)/「苗床」/例外(いじめ・脅迫・カンニング)/反対(Thomas)を公平に |
| **act4** SPN0019–0021 | `somber`(ledger_of_ash)（内省） | `amb_empty_hallway`・`amb_night_window` | `sub_drop` 微（0019曖昧な境界）, `ui_tick`（0020扉が開く）, `soft_impact`（0021主題テロップ） | 「保護はあるが曖昧」→深刻ケースへの扉→「自由は嫌いな言論で試される」 |
| **エンディング** SPN0022–0025 | `outro`(last_frame)（解決・希望） | なし〜薄く | `dust_swell`/`whoosh_medium`（0023シリーズ統合）, `riser_2s`（0024次回引き）, `soft_impact`+`ui_tick`（0025 Subscribe） | 総括→シリーズ統合（捜索・追跡・収用・言論）→次回予告（署名で手放す権利）→CTA |

> SPNは番号順≠時系列。上表の**章順**（act1: …0028 / act2: 0026先頭 / act3: …0027）でキューを当てる（`edit_design.v001.md` §2 と一致）。

## 3. 工程と保存先
- ナレ生成: `script.en.v001.md` の `[VO:]` → ElevenLabs → ドラフト `H:\pd-media\episodes\PD-2026-011-mahanoy\06_voice\draft\VC-XXXX.mp3` → マスター `…\06_voice\master\VC-XXXX.mp3`。**罵倒語は描写文のみ（原文どおり読まない設計）**。
- ナレ計画/索引(git): `06_audio/voice_plan.v001.json` / `06_audio/narration_index.v001.json`。
- 字幕(git): forced alignment で `08_edit/captions.v001.srt`(+`.json`)。テロップ/出典/CENSORED帯と**被らせない**（位置で分離・`edit_design.v001.md` §3）。罵倒語は字幕にも出さない。
- BGM/SFX/環境音の実体は `H:\pd-media\library\` を参照（話別が要れば `…\07_audio\` にコピー）。
- ミックスは Remotion 側のオーディオトラック or 書き出し前に整音。最終 −14 LUFS / TP ≤ −1。

## 4. 受け入れチェック
- [ ] 4層すべて入っている（VO/BGM/SFX/ambience）
- [ ] ダッキングでナレ中のBGM・環境音が下がり、VOが常に明瞭
- [ ] 山場（SPN-0014 8–1）と各テロップ出現にSFXが同期（`gavel_knock`+`low_boom`→`stamp_seal`）
- [ ] −14 LUFS / true peak ≤ −1 dBTP
- [ ] 字幕がナレと語単位同期、テロップ/出典/CENSORED と非重複
- [ ] **投稿の罵倒語が音声・字幕に存在しない**（広告安全）／煽りすぎない落ち着いたトーン
