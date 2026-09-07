# EP54 `bgm_plan.v001` — 音楽ベッド設計（Curtis Flowers・DRAFT）

**Episode:** `PD-2026-054-flowers` · library=`H:/pd-media/library/music/`（rights registry = `episodes/_planning/SOUND_LIBRARY_RIGHTS.v001.json`・MUS-0001〜0021 全21曲 commercial_ok=true 確認済み）
**目的**：`bgm_present`＋`bgm_ending` を `build_case_film_audio.py` の**4層モデル**で満たす。**ナレ長・間は変えない**。
**総尺（暫定）**：≈ **1,783s（29:43）** = ナレ1,579.3s ＋ designed non-speech 195s ＋ endcard 9s（DESIGN §5）。★**HOOK-AUDIO**：VOはframe 0から。BrandOpeningは被せスティング（≥12dBダック）。**cue時刻は全てPLACEHOLDER — forced-align後に再ロック。**

## ミックス仕様（全編共通・build_case_film_audio.py準拠）
- **4層**：L1 VO前面 · L2 music（sidechaincompress threshold=0.03/ratio=8/attack=25/release=320・体感フロア≈-22）· L3 ambience **-18dB定常ベッド（非サイドチェイン）** · L4 SFXワンショット（章境界whoosh自動）。
- **連続ベッド**：章境界0.8–1.2sクロスフェード・無音>25s禁止・ambience coverage ≥0.85。
- **統合ラウドネス**：2パス loudnorm **-14 LUFS**、TP ≤ -1.0。
- **グルー**：`MUS-0019`（ambience_empty_hall v2・glue）を極薄（-30〜-34）で全編に（EP53はv1を使用 — 連投時の使い回し感を減らすため各話でv1/v2を振り分け）。

## 章立て → 曲割り（cue sheet・時刻はPLACEHOLDER）
| 区間 | video時間(目安) | トラック | 役割/mood | ミックス・cue意図 |
|---|---|---|---|---|
| **HOOK（cold open）** | 0–~25 | `MUS-0002` (hook_glass_air_bed v2) | hook / tense_sparse | VO下ダック。「Six trials. Four death sentences.」の数字連打に合わせ、ローマ数字の焼き付き打点は木のknock SFXが主・音楽は張力のみ |
| **BrandOpening sting** | ~25–28 | `MUS-0004` (opening_measured_arpeggio v2) | opening sting | 金OP着地swell→Act Iへ |
| **ACT I 犯行と「選ばれ方」** | ~28–~380 | `MUS-0006` (explainer_bed v2) | neutral / dry heat | 被害者4人のビート（earned breath #1）は**音楽を退かせambienceのみ**。「薄い事件」の列挙は乾いたneutralで淡々と |
| **ACT II 裁判・破棄・反復** | ~380–~720 | `MUS-0007` (tension_build v1) | machine / slow_crescendo | counter I→II→III の各着地で再入。破棄（数字が割れる）ごとに一段薄く戻して再クレッシェンド＝機械の反復感。Miss. S. Ct. QUOTE_CARDは音楽薄く |
| **ACT III 評決不能の年月と嘘つき** | ~720–~1,120 | `MUS-0009` (somber_ledger_of_ash v1) → Hallmon暴露で `MUS-0012` (reveal_sting v2) | somber / human_cost + sting | Bibbs手錠ビートは音楽を薄くしSFX前面。Hallmonの2016（3人の被害者）は**最も静かに**（dignity・earned breath #2は「That was a lie.」着地後）。録音テープの waveform ビートでsting一発 |
| **ACT IV 9回裏（数字のカスケード）** | ~1,120–~1,600 | `MUS-0014` (reveal_verdict_at_dawn v2) | reveal / dawn swell | In the Darkのデータ組み上がり→SCOTUS「41 OF 42」→保釈（free-air blue初登場）→with prejudiceで最大swell。70–30の投票はswellを引き継ぎつつ軽く。ライセンス請願は**解決させない**（swellを切り、保留の静けさで置く） |
| **ENDING→Endcard** | ~1,600–1,783 | **`MUS-0017`** (outro_last_frame v2・end_card) | outro / unresolved-hopeful | **align-to-end配置**（下記）。本作のEDは「未解決の誠実さ」＝高揚させ過ぎない |

## ED＝「切りのいい所で終わる」（`bgm_ending`・チャンネル正典）
- `MUS-0017` を**フレーズ終止＝動画終端で align-to-end**、`OUTRO_FADE_DUR=3.0s` クリーンフェードで無音着地（ブツ切り禁止）。DESIGN §5の指定どおり「BGM resolves on a musical phrase boundary — never mid-bar」。
- **ending ambience は固定**：ENDING章のambience = **`amb_night_window.mp3`**（正典デフォルト）。**`amb_light_wind` 全編禁止**。
- **gospel hum について（権利ノート）**：DESIGNのENDING「gospel thread（賛歌のハム）」に該当する内部トラックは現状ライブラリに**無い**。実在ゴスペル録音・外部曲の使用は不可（権利未検証の外部曲は名指ししない）。対応は次のどちらか：(a) `MUS-0017` のみで代替し「hum」はambienceレイヤの低い人声風パッドを**新規Suno生成→registry登録後に**充てる、(b) mood指定のCUEとして発注：**warm hymn-like sustained vocal pad · 60–70 BPM · major · ルバート可・歌詞なし・ソロ人声にならない**。※(a)(b)どちらも registry 追記まで本mixには入れない。

## ambience 配車（章ごとに別ベッド）
hook=`amb_tension_drone` · ACT I 店/町=`amb_office_hum` · ACT II 法廷=`amb_courtroom_room_tone` · ACT III Parchman=`amb_institutional_drone` · ACT IV 記録庫/大理石=`amb_empty_hallway` · ENDING=`amb_night_window`（固定）= 6 distinct beds ✓。※「灼熱の蝉」ベッドはライブラリに無い — wind系は禁止のため代替導入しない（SFXワンショットの遠い環境音で示唆する程度に留める）。

## SFX意図（L4）
章境界whoosh（自動）＋ 設計SFX：木のknock（ローマ数字 I–VI 着地・ガベル型クリシェは全編≤2）、紙をなぞるstrike線（陪審ストライク）、遠い手錠（Bibbs・off-screen）、テープレコーダの起動（Hallmon）、投票ブースのカーテン（2022）。**実録音（本物のHallmon通話・報道・法廷音声・実在ゴスペル）は全面禁止**。

## 事後mix手順（レンダ後）
1. 最終mp4取得 → 2. cue配置＋クロスフェード＋glue → 3. sidechain→2パス loudnorm -14 → 4. align-to-end＋3.0sフェード → 5. `check_final_acceptance`（bgm_present/bgm_ending/loudness/sound_layers）＋末尾10秒耳チェック。
> cue時刻は forced-align 後に再計算。**候補トラックは全て rights registry 収載の内部ライブラリのみ**（外部未検証曲の名指しなし）。
