# EP55 `bgm_plan.v001` — 音楽ベッド設計（Jon Burge・DRAFT）

**Episode:** `PD-2026-055-burge` · library=`H:/pd-media/library/music/`（rights registry = `episodes/_planning/SOUND_LIBRARY_RIGHTS.v001.json`・MUS-0001〜0021 全21曲 commercial_ok=true 確認済み）
**目的**：`bgm_present`＋`bgm_ending` を `build_case_film_audio.py` の**4層モデル**で満たす。**ナレ長・間は変えない**。チャンネル最重量の題材＝**全編で音楽は一段引いた設計**（dreadはambienceが担う・DESIGN §1 sound intent）。
**総尺（暫定）**：≈ **1,791s（29:51）** = ナレ1,582.1s ＋ designed non-speech 199.9s ＋ endcard 9s（DESIGN §5）。★**HOOK-AUDIO**：VOはframe 0から。BrandOpeningは被せスティング（≥12dBダック）。**cue時刻は全てPLACEHOLDER — forced-align後に再ロック。**

## ミックス仕様（全編共通・build_case_film_audio.py準拠）
- **4層**：L1 VO前面 · L2 music（sidechaincompress threshold=0.03/ratio=8/attack=25/release=320・体感フロア≈-22）· L3 ambience **-18dB定常ベッド（非サイドチェイン）** · L4 SFXワンショット（章境界whoosh自動）。
- **連続ベッド**：章境界0.8–1.2sクロスフェード・無音>25s禁止・coverage ≥0.85。
- **統合ラウドネス**：2パス loudnorm **-14 LUFS**、TP ≤ -1.0。
- **グルー**：`MUS-0020`（ambience_paper_trail_static v1・document_glue）を極薄（-30〜-34）で全編に — 「紙が戻ってくる」主題と一致するstaticな質感（EP53/54のempty_hall系と差別化）。

## 章立て → 曲割り（cue sheet・時刻はPLACEHOLDER）
| 区間 | video時間(目安) | トラック | 役割/mood | ミックス・cue意図 |
|---|---|---|---|---|
| **HOOK（cold open＝医師の手紙）** | 0–~25 | `MUS-0001` (hook_glass_air_bed v1) | hook / cold sparse | VO下ダック。蛍光灯ハム＋引き出しの閉音がhookの主役・音楽は薄い張力のみ。**悲鳴・苦痛演技音の類は全面禁止** |
| **BrandOpening sting** | ~25–28 | `MUS-0003` (opening_measured_arpeggio v1) | opening sting | 金OP着地→Act Iへ |
| **ACT I 司令官** | ~28–~350 | `MUS-0005` (explainer_bed v1) 低め | neutral / institutional | 経歴の上昇はneutralに淡々と。Holmes 1973の証言引用ビートは**音楽ほぼ無音**（言葉だけを残す）。black box登場は音楽でなくcrank-click SFX（leitmotif・使用は控えめ） |
| **ACT II 誰も聞かなかった悲鳴** | ~350–~740 | `MUS-0007` (tension_build v1) | slow_crescendo / alarms ignored | 手紙が上がって死ぬ（closingdoor）ごとにクレッシェンドを**切って**振り出しへ＝「警報が鳴っては消える」構造。Goldston「planned torture」の文字着地は音楽薄く。1993解雇＝「fired ≠ charged」の落差は低いsting的処理（`MUS-0011` 一発可） |
| **ACT III 時効の壁** | ~740–~1,130 | `MUS-0009` (somber_ledger_of_ash v1) | somber / the clock | 本作最スロー章（近4sホールドはここのみ）。時効の算術は音楽を止めない程度に最薄。2003恩赦×フロリダの split-screen は**同一曲のまま**質感で対比（音楽で温冷を分けない — 皮肉は映像が担う） |
| **ACT IV 偽証（payoff cascade）** | ~1,130–~1,620 | `MUS-0013` (reveal_verdict_at_dawn v1) → 報復の summit で `MUS-0015` (v3) に乗せ換え | reveal / measured dawn | 逮捕→2010有罪→4.5年は**冷静な**revealで（高揚させない — 54ヶ月は勝利でない）。「human vermin」引用は音楽を退かす。**May 6 2015 reparations＝全米初**から `MUS-0015` へクロスフェードし、curriculum-morning の帯とともに本作唯一の本当のswell。教科書ビートまで持続 |
| **ENDING→Endcard** | ~1,620–1,791 | **`MUS-0016`** (outro_last_frame v1・end_card) | outro / quiet resolution | **align-to-end配置**（下記）。「手紙が章になった」＝静かな解決 |

## ED＝「切りのいい所で終わる」（`bgm_ending`・チャンネル正典）
- `MUS-0016` を**フレーズ終止＝動画終端で align-to-end**、`OUTRO_FADE_DUR=3.0s` クリーンフェードで無音着地（ブツ切り禁止）。CTA「hit like…」直後にアウトロが解決して静かに終わる。**ナレ/間は不変**。
- **ending ambience は固定**：ENDING章のambience = **`amb_night_window.mp3`**（正典デフォルト・`amb_light_wind` 全編禁止）。

## ambience 配車（章ごとに別ベッド）
hook=`amb_office_hum`（タイプ用紙と引き出しの部屋）· ACT I 夜のシカゴ=`amb_rain_street` · ACT II Area 2=`amb_institutional_drone` · ACT III 時効/待合=`amb_empty_hallway` · ACT IV 連邦法廷=`amb_courtroom_room_tone` · ENDING=`amb_night_window`（固定）= 6 distinct beds ✓。蛍光灯buzzやel-train、radiator tickは**SFX/設計ambienceの追いレイヤ**（L4扱い・registry収載SFXのみ）。

## SFX意図（L4）
章境界whoosh（自動）＋ 設計SFX：紙のスライド＋引き出し（手紙の埋葬・回帰）、遠い鉄扉、crank-click（black box leitmotif・**全編で数回まで**・絵は常にinert）、タイプライター（Conroy/報告書）、法槌なし（クリシェ規制）、教室の朝の静けさ（ENDING）。**悲鳴・苦痛音・実在音声（Burge本人・サバイバー・議会・報道）は全面禁止**（BU-guardrail/DESIGN §1）。
**単調回避ノート**：Act I–IIIは意図して抑制するぶん、`check_final_acceptance` の bgm_present（>25s無音禁止）と衝突しやすい — 「音楽ほぼ無音」指定の各ビートも**glue（MUS-0020）とambienceは残す**こと（完全無音を作らない）。

## 事後mix手順（レンダ後）
1. 最終mp4取得 → 2. cue配置＋クロスフェード＋glue → 3. sidechain→2パス loudnorm -14 → 4. align-to-end＋3.0sフェード → 5. `check_final_acceptance`（bgm_present/bgm_ending/loudness/sound_layers）＋末尾10秒耳チェック。
> cue時刻は forced-align 後に再計算。**候補トラックは全て rights registry 収載の内部ライブラリのみ**（外部未検証曲の名指しなし）。EP53/54/55は近接出荷想定のため、hook/outroの v1/v2 振り分け（53=v1系・54=v2系・55=v1系＋glueのみ別系統）で連投時の既聴感を減らしている — 3話連続で同一hook曲が並ばないことをmix時に最終確認。
