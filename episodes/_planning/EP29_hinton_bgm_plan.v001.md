# EP29 `bgm_plan.v001` — 音楽ベッド設計（無実の死刑囚）

**Episode:** `PD-2026-029-hinton` · library=`H:/pd-media/library/music/` (registry v001, 21曲)
**目的**：`bgm_present`（連続ベッド・無音>25s禁止・VO下も可聴フロア）＋`bgm_ending`（EDが切りよく解決）を**事後ffmpegダッキングmix**で満たす設計。**ナレ長・間は変えない**（尺は台本が主・曲を枠に収める側）。
**総尺**：706.8s… ではなくEP29は**696.8s**（hook8＋opening3.5＋ナレ676.3＋endcard9）。video_time = **11.5 + narration_time**（bodyはBrandOpening後に開始）。

## ミックス仕様（全編共通）
- **連続ベッド**：章の切れ目で**0.8–1.2sクロスフェード**、無音の穴を作らない（>25s無音でゲート落ち）。
- **ダッキング**：VO区間はベッドを**-22 LUFS フロア**へサイドチェイン（VO前面）。ナレの無い hook/opening/endcard はベッドを前に出す（-16〜-14）。
- **統合ラウドネス**：最終 **-14 LUFS**（±0.5）、TP ≤ -1.0 dBTP。
- **グルー**：全編に `MUS-0018`(subliminal_drone, e1) を極薄（-30〜-34）で敷き、章曲の隙間を埋め連続性を担保。

## 章立て → 曲割り（cue sheet）
| 区間 | video時間(目安) | トラック | 役割/mood | ミックス |
|---|---|---|---|---|
| **Hook montage** | 0–8s | `MUS-0002` | hook / tense_sparse (e4) | 前面(-15)。パンチ編集に緊張 |
| **BrandOpening** | 8–11.5s | `MUS-0003` | opening / confident_clear | 金OP着地に合わせ swell、bodyへブリッジ |
| **ACT I 逮捕** | ~11.5–~180 | `MUS-0005` | explainer_bed / neutral (loop) | VO下-22。アリバイ→"一致した弾" |
| **ACT II 崩れた裁判** | ~180–~360 | `MUS-0007` | tension_build / slow_crescendo | 不正義の高まり。片目の鑑定→死刑へ crescendo |
| **ACT III 30年** | ~360–~560 | `MUS-0009`→`MUS-0010` | somber / dignified_sparse (human_cost) | **感情の核**。死刑房の年月・尊厳・54処刑。最も静かに |
| **ACT IV 光** | ~560–~688 | `MUS-0013`(→`MUS-0015`) | reveal / warm_brass_swell | 9–0最高裁→釈放の**逆転**。温かいブラスの解決 |
| **ENDING→Endcard** | ~688–696.8 | **`MUS-0016`** | outro / **hopeful_resolved (end_card)** | **切りのいい終止**（下記） |

## ED（末尾9秒 Endcard）＝"切りのいい所で終わる"（`bgm_ending`＋オーナー指示）
- Endcard枠を**アウトロ専用**にし、`MUS-0016`（hopeful_resolved・159.68s）を**"曲自身の終止/フレーズ終わり"が動画終端に一致するよう align-to-end 配置**（ループ途中でブツ切りしない）。
- 最後は拍/終止に合わせ**1.5–2sクリーンフェードで無音着地**（全音量チョップ禁止＝`bgm_ending`）。
- ナレCTA「hit like…」の直後にアウトロ主旋律が**解決**して静かに終わる。**ナレ/間は不変**。

## 事後mix手順（レンダ後・画像→組立→レンダの後に実行）
1. Remotion最終mp4（VO込み）を取得。
2. 上表の各章トラックを video 時間へ配置＋クロスフェード＋グルー drone。
3. サイドチェインでVO下-22フロアにダッキング → 2パス loudnorm で **-14 LUFS**。
4. Endcardは align-to-end＋クリーンフェード。
5. `check_final_acceptance` の `bgm_present`/`bgm_ending`/`loudness` で検証＋**末尾10秒を耳チェック**（musicalな収まりは機械で測れない）。

> ※長尺用BGM mixスクリプトは未整備（ショートは`build_short_mix.py`）。本プランはその実装/手動mixの確定入力。EP28/EP30も同構造（somber核＋reveal逆転＋outro解決）で流用可。
