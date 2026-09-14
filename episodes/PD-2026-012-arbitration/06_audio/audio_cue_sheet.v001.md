# 第12話 arbitration 音声設計（Audio Cue Sheet・4層＋ダッキング） v001

対象: `PD-2026-012-arbitration`（AT&T Mobility v. Concepcion 2011 / Epic Systems v. Lewis 2018 / 強制仲裁条項＋集団訴訟放棄）。Codex がこの設計で BGM/SFX/環境音を配置・ミックスする。
準拠: `VIDEO_RULES.md` §11 / `docs/audio-sfx-bgm-library-plan.md`。
音源棚（実在・`H:\pd-media\library\`）: `music/{hook,opening,explainer_bed,tension_build,reveal,somber,outro,ambience}`, `ambience/amb_*.mp3`, `sfx/sfx_*.mp3`。レジストリ: `library/music_registry.v001.json` / `library/sfx_registry.v001.json`。
**中立**: これは本物の政策論争。BGM/SFXで critics 側にだけ不安音、defenders 側にだけ明るい音、のような偏りを付けない（0011/0012, 0015/0024 は同等トーン）。

## 0. 4層の役割
1. **VO（ナレ）** = 最優先。`06_voice/master/VC-XXXX.mp3`。常に明瞭。
2. **BGM** = `music/<mood>` から1曲/章。控えめ。
3. **SFX** = カット/リビール/数字/テロップ出現の効果音。
4. **環境音(ambience)** = 法廷ざわめき/オフィス/夜/施設ドローン等を薄く。

## 1. ダッキング（必須・VO最優先）
- **VOをサイドチェイン基準**にBGM・環境音を自動ダッキング。
- 目安: ナレ有り区間で **BGM −16〜−18 dB / ambience −26〜−30 dB** 下げる。SFXワンショットはVOを隠さない範囲（ピーク −12 dB目安）。
- 整音: **−14 LUFS（integrated）・true peak ≤ −1 dBTP**。VOが常に聞き取れることを最終確認。
- ナレの**頭16フレーム前**でBGM/ambienceを先行ダッキング、ナレ終わり後にゆっくり戻す。

## 2. 章別キュー（BGM/ambience/SFX）

| 章 / SPN | BGM(music/) | ambience | 主なSFX | 演出メモ |
|---|---|---|---|---|
| **フック** (本編ハイライト集) | `tension_build`→`hook` | （薄く `amb_tension_drone`） | `sfx_riser_2s`, `sfx_low_boom`, `sfx_whoosh_short/medium` をカット頭に。`sfx_ui_tick`（「I agree」タップ） | 高速カットに同期して煽る。最後は一瞬無音→オープニングへ |
| **オープニング** SPN-0002 | `opening`（定番） | なし | `sfx_whoosh_medium`（タイトルイン）, `sfx_data_blip`（"arbitration clause"/"waiver" 下線確定） | 既存ブランド演出（`BrandOpening`）。作り直さない |
| **act1** SPN0003–0007 | `explainer_bed`（好奇心） | `amb_office_hum` 薄く | `sfx_stamp_seal`（0003 "+$30 tax" 打刻）, `sfx_data_blip`/`sfx_ui_tick`（0004 $30カウントアップ・0005 束ねる）, `sfx_paper_rustle`（0006 州法カード） | 「FREE携帯＋$30税」→「$30×millions」→集団訴訟＝束ねる→Discover Bank 州法 |
| **act2** SPN0008–0012,0023 | `explainer_bed`（臨床的） | `amb_institutional_drone` 薄く（0011 critics でわずかに翳り、ただし0012と同等に戻す） | `sfx_page_turn`（0009 年表1925/FAAカード）, `sfx_binder_lock`（0011 扉が閉じる・critics）, `sfx_ui_tick`（0023 起動/開封/クリック/出勤の4アイコン）, `sfx_data_blip`（0010 1人ずつ切り離し・0012 defenders） | 1925 FAA→放棄の意味→critics(扉が閉じる) vs defenders(速い/安い)。**両論を同トーンで** |
| **act3** SPN0013–0016,0024 | `tension_build`→**`reveal`（0013/0016 山場）** | `amb_courtroom_room_tone` 薄く | **`sfx_gavel_knock`+`sfx_low_boom`（0013 5–4リビール）**, `sfx_stamp_seal`（出典 563 U.S.333 確定）, `sfx_whoosh_short`（0014 州法に取り消し線）, `sfx_data_blip`（0016 phone→job 矢印）, `sfx_gavel_knock` 微（0024 Ginsburg 法廷読み上げ） | Concepcion(2011)→Scalia多数/Breyer反対→Epic(2018)拡張→Ginsburg反対。多数/反対を**公平に** |
| **act4** SPN0017–0019,0025 | `somber`（内省） | `amb_night_window`・`amb_empty_hallway` 薄く | `sfx_data_blip`（0018 天秤 vs 印章の対置）, `sfx_clock_tick_loop` 微（0025 議論は続く）, `sfx_sub_drop`/`sfx_low_boom` 微（0019「自分で手放した」静寂の押し） | 日常に遍在→debate is real / mechanism is not→「声高に取られず自分で手放した」決め所 |
| **エンディング** SPN0020–0022 ＋ 既存エンドカード | `outro`（解決・余韻） | なし〜薄く | `sfx_soft_impact`（0021 シリーズ統合 search→track→take→speech＋"by contract"）, `sfx_riser_2s`（0022 次回DNAの引き）, `sfx_soft_impact`+`sfx_ui_tick`（エンドカード Subscribe） | 結末「$30が静かで広い線」→シリーズ統合→次回予告（DNA採取）→固定エンドカード |

> 環境音の実体は `H:\pd-media\library\ambience\amb_*.mp3`（`music/ambience/` にも同名あり）。SFXは `sfx/sfx_*.mp3`、BGMは `music/<mood>/` 内の `mus_*` から各章1曲を選ぶ（例 reveal は `mus_20260614_reveal_verdict_at_dawn_v*` を山場に）。

## 3. 工程と保存先
- ナレ生成: `script.en.v001.md` の `[VO:]` → ElevenLabs → ドラフト `H:\pd-media\episodes\PD-2026-012-arbitration\06_voice\draft\VC-XXXX.mp3` → マスター `…\06_voice\master\VC-XXXX.mp3`。
- ナレ計画/索引(git): `06_audio/voice_plan.v001.json` / `06_audio/narration_index.v001.json`。
- 字幕(git): forced alignment で `08_edit/captions.v001.srt`(+`.json`)。テロップと**被らせない**（位置で分離・`edit_design.v001.md` §3）。
- BGM/SFX/環境音の実体は `H:\pd-media\library\` を参照（話別が要れば `…\07_audio\` にコピー）。
- ミックスは Remotion 側のオーディオトラック or 書き出し前に整音。最終 −14 LUFS / TP ≤ −1。

## 4. 受け入れチェック
- [ ] 4層すべて入っている（VO/BGM/SFX/ambience）
- [ ] ダッキングでナレ中のBGM・環境音が下がり、VOが常に明瞭
- [ ] 山場（SPN-0013 5–4・SPN-0016 Epic拡張）と各テロップ出現にSFXが同期
- [ ] −14 LUFS / true peak ≤ −1 dBTP
- [ ] 字幕がナレと語単位同期、テロップ/出典と非重複
- [ ] critics(0011)とdefenders(0012)、Breyer(0015)とGinsburg(0024)が**同等トーン**（音で一方に肩入れしない＝中立）
