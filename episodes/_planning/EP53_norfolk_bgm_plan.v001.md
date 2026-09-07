# EP53 `bgm_plan.v001` — 音楽ベッド設計（The Norfolk Four・DRAFT）

**Episode:** `PD-2026-053-norfolk` · library=`H:/pd-media/library/music/`（rights registry = `episodes/_planning/SOUND_LIBRARY_RIGHTS.v001.json`・MUS-0001〜0021 全21曲 commercial_ok=true 確認済み）
**目的**：`bgm_present`（連続ベッド・無音>25s禁止・VO下も可聴フロア）＋`bgm_ending`（EDが切りよく解決）を `build_case_film_audio.py` の**4層モデル**で満たす設計。**ナレ長・間は変えない**（尺は台本が主・曲を枠に収める側）。
**総尺（暫定）**：≈ **1,799.6s（30:00）** = ナレ1,564.9s×gap1.150 ＋ endcard 9s（DESIGN §5）。★**HOOK-AUDIO**：VOはframe 0から（EP29と違い先頭に無音ランウェイなし）→ **hook区間も最初からダッキング下で敷く**。BrandOpeningは~2.0–2.5sの被せスティング（VOの下、≥12dBダック）。**cue時刻は全てPLACEHOLDER — forced-align後のfilm.jsonで再ロック。**

## ミックス仕様（全編共通・build_case_film_audio.py準拠）
- **4層**：L1 VO前面 · L2 music（sidechaincompress threshold=0.03 / ratio=8 / attack=25 / release=320でVOにダック・体感フロア≈-22）· L3 ambience **-18dBの可聴・定常ベッド（サイドチェインしない）** · L4 SFXワンショット（章境界にwhoosh自動配置）。
- **連続ベッド**：章の切れ目で**0.8–1.2sクロスフェード**、無音の穴を作らない（>25s無音でゲート落ち）。ambience coverage ≥0.85。
- **統合ラウドネス**：2パス loudnorm **-14 LUFS**（±0.5）、TP ≤ -1.0 dBTP。
- **グルー**：全編に `MUS-0018`（ambience_empty_hall v1・glue_texture）を極薄（-30〜-34）で敷き、章曲の隙間を埋める。

## 章立て → 曲割り（cue sheet・時刻はPLACEHOLDER）
| 区間 | video時間(目安) | トラック | 役割/mood | ミックス・cue意図 |
|---|---|---|---|---|
| **HOOK（cold open）** | 0–~22 | `MUS-0001` (hook_glass_air_bed v1) | hook / tense_sparse | VO下ダック。電球点灯＋タリー4本のスタッガーに冷たい緊張。チョーク音SFXは音楽より前 |
| **BrandOpening sting** | ~22–25 | `MUS-0003` (opening_measured_arpeggio v1) | opening sting | 金OPに合わせ短くswell→即Act Iへブリッジ（VO≥12dBダック維持） |
| **ACT I 最初の自白** | ~25–~360 | `MUS-0005` (explainer_bed v1) → 後半 `MUS-0007` (tension_build v1) | neutral bed → slow_crescendo | 港と日常はneutral。取調室に入る「What happened in that room…」(~1/3地点)で0.8sクロスフェードしtensionへ。自白成立＝タリー1本目の打点で一瞬ブレイク |
| **ACT II ドミノ** | ~360–~700 | `MUS-0007` 継続 → 反復ごとにレイヤ感を上げる（同曲の再入でOK・loop点をDNA除外ビートに合わせる） | tension_build / machine | 「除外→新suspect→自白」3周の加速をループ再入で刻む。act峰「7 CHARGED · 0 MATCHES」カードで最も厚く |
| **ACT III 手紙** | ~700–~1,080 | `MUS-0009` (somber_ledger_of_ash v1) ＋ DNA一致の瞬間だけ `MUS-0011` (reveal_sting v1) | somber / human_cost + 単発sting | 真実が届いて何も起きない章＝最も静かに。Ballard QUOTE_CARD着地は音楽を薄くしSFX（紙・封筒）前面。家族への1ビートは**音楽ほぼ無音・ambienceのみ**（本作の earned breath） |
| **ACT IV 長い undoing** | ~1,080–~1,600 | `MUS-0013` (reveal_verdict_at_dawn v1) → Ford帰結は `MUS-0020` (paper_trail_static v1) に落とす | reveal / warm swell → cold procedural | Gibney「By any measure…」→絶対恩赦→$8.4Mのカスケードで唯一のswell（cream点灯と同期）。**Fordの結末は温かくしない**：ブラス的高揚を切り、紙のstaticな冷たい質感で「制度の文法が閉じる」音に |
| **ENDING→Endcard** | ~1,600–1,799.6 | **`MUS-0016`** (outro_last_frame v1・end_card) | outro / hopeful_resolved | **align-to-end配置**（下記） |

## ED＝「切りのいい所で終わる」（`bgm_ending`・チャンネル正典）
- `MUS-0016` を**曲自身のフレーズ終止が動画終端に一致するよう align-to-end 配置**（ループ途中でブツ切りしない）。ビルダーの `OUTRO_FADE_DUR=3.0s` クリーンフェードで無音着地（全音量チョップ禁止）。
- **ending ambience は固定**：ENDING章のambienceベッドは **`amb_night_window.mp3`**（正典デフォルト）。**`amb_light_wind` は全編禁止**（「飛行機の音」問題・owner 2026-07-06/07-10）。
- CTA「hit like…」直後にアウトロ主旋律が解決して静かに終わる。**ナレ/間は不変**。

## ambience 配車（章ごとに別ベッド・distinctness をゲートが採点）
hook/ACT I 取調室=`amb_institutional_drone` · ACT II ラボ/署=`amb_office_hum` · ACT III 手紙/獄=`amb_empty_hallway` · ACT IV 法廷=`amb_courtroom_room_tone` · ENDING=`amb_night_window`（固定）。= 5 distinct beds ✓。港の外景ビートは`amb_night_window`側に寄せる（wind系禁止）。

## SFX意図（L4・ワンショット）
章境界whoosh（ビルダー自動）＋ 設計SFX：チョークのタリー（各自白）、蛍光灯ハム点灯（hook）、紙・封筒（Act III）、ゲートの半開（2009）、独房ドア（Ford）。**実在人物音声・悲鳴・報道音声は全面禁止**（DESIGN §5 real-audio constraint）。

## 事後mix手順（レンダ後）
1. Remotion最終mp4（VO込み）取得 → 2. 上表を video時間へ配置＋0.8–1.2sクロスフェード＋glue drone → 3. sidechainダッキング → 2パス loudnorm -14 → 4. Endcard align-to-end＋3.0sフェード → 5. `check_final_acceptance` の `bgm_present`/`bgm_ending`/`loudness`/`sound_layers` ＋ **末尾10秒を耳チェック**。
> ※cue時刻は forced-align 後に必ず再計算（本表は語数比例のPLACEHOLDER）。EP29プランと同構造（somber核＋reveal逆転＋outro解決）。**トラックは全て rights registry 収載の内部ライブラリのみ**（外部曲の名指しなし）。
