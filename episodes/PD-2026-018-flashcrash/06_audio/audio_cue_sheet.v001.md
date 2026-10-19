# EP18 flashcrash — Audio cue sheet (4-layer) v001

> Codex がこの設計で BGM/SFX/環境音を配置・ミックス。準拠：`VIDEO_RULES.md` §11 / `docs/audio-sfx-bgm-library-plan.md` / 正典 row1(BGM常時)・row6(−14 LUFS)。音源棚＝`H:\pd-media\library\`（`music/<mood>/`・`ambience/amb_*.mp3`・`sfx/sfx_*.mp3`／`music_registry.v001.json`・`sfx_registry.v001.json`）。
> **テーマ＝人間 vs 機械**：単音ピアノ/シンセが機械的アルペジオに侵食される。山場(S17 plunge)は低域ドローン＋心拍、最悪の数秒は**ほぼ無音**（恐怖は音量でなく欠落で）。

## 1. 4層とダッキング
1. **VO**（ElevenLabs本番・最優先）
2. **BGM**＝`music/<mood>` から章ごと1曲。**全編で帯を切らさない**（意図的無音は数秒のみ＝row1 `bgm_present` 無音≤25s）。
3. **SFX**＝決め所のワンショット（VOを隠さない・ピーク −12dB目安）。
4. **ambience**＝端末ノイズ・遠い飛行機（90秒ごと＝Hounslowの時の刻み）。
- **ダッキング必須**：VOサイドチェインでナレ区間 BGM −16〜−18dB / ambience −26〜−30dB、ナレ頭16フレーム前に先行。整音 **−14 LUFS / TP ≤ −1 dBTP**、VO常に明瞭。

## 2. 章別キュー
| 章 / SPN | BGM(music/) | ambience | 主なSFX | 演出メモ |
|---|---|---|---|---|
| **フック**(本編ハイライト) | `tension_build`→`hook` | 薄く `amb_machine_hum` | `riser_2s`/`low_boom`/`sub_drop`（$1T崩落 S02） | 高速カットに同期・最後一瞬無音→Opening |
| **act1** 機械 | `explainer_bed`（冷たい上昇） | `amb_server_room`/`amb_machine_hum` | `data_blip`/`ui_tick`（order book） | HFT/流動性の解説 |
| **act2** 寝室 | `somber`→`explainer_bed`（孤独＋好奇） | `amb_room_tone`/遠い飛行機 | `plane_pass`（90秒モチーフ）/`keyboard`微/`arcade_blip`(HighScore S09) | 人物・無欲・ハイスコア |
| **act3** 幻の壁 | `tension_build`（不穏な上昇） | `amb_machine_hum` 薄く | `whoosh_short`（壁の出現/消滅 S11-12）/`data_blip`/`soft_impact`（本物の1注文 S13） | スプーフィングの図解（理解の快感） |
| **act4** あの日 | `tension_build`→**(S17)低域ドローン＋心拍** | `amb_institutional_drone` | `sub_drop`+`low_boom`（S17 plunge“ため→開放”）/`alarm_distant`（circuit breaker S19手前）/`ui_tick`（$0.01 S18） | 2つの重し→床が消える→**最悪の数秒ほぼ無音**→回復 |
| **act5** 誰が壊した | `somber`（内省） | `amb_empty_office` | `page_turn`/`stamp`微（報告書） | 因果の審判・断定しない |
| **act6** 落着 | `somber`→静かな解決 | `amb_room_tone` | `gavel_soft`（量刑・控えめ）/`coins_dust`（喪失 S23） | 逮捕・喪失・答弁・寛刑 |
| **エンディング** | `outro`（解決・問い） | 薄く→遠い飛行機 | `dust_swell`/`soft_impact`+`ui_tick`（Subscribe S26） | 市場のその後→問い→CTA |

## 3. チェック（row1/6）
- [ ] 4層すべて（VO/BGM/SFX/ambience）・BGM全編常時（無音≤25s）
- [ ] ダッキングでナレ中BGM/ambient下がりVO明瞭・−14 LUFS / TP≤−1
- [ ] S17 plunge“ため→開放”＋最悪の数秒の意図的無音
- [ ] **R3：音演出で断定有罪・単独原因の含意を足さない（中立）**
