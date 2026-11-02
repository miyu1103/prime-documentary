# EP56 `bgm_plan.v001` — 音楽ベッド設計（The Post Office Horizon scandal・DRAFT）

**Episode:** `PD-2026-056-postoffice` · library=`H:/pd-media/library/music/`（rights registry = `episodes/_planning/SOUND_LIBRARY_RIGHTS.v001.json`・**MUS-0001〜0021 全21曲 / ambience 11本 commercial_ok=true 確認済み**）
**目的**：`bgm_present`（連続ベッド・無音>25s禁止・VO下も可聴フロア）＋`bgm_ending`（EDが切りよく解決）を `scripts/build_case_film_audio.py` の**4層モデル**で満たす設計。**ナレ長・間は変えない**（尺は台本が主・曲を枠に収める側）。
**総尺（暫定）**：≈ **1,791.0s（29:51）** = ナレ1,600.2s（4,750語 ÷ 178.1wpm）＋ designed non-speech 181.8s ＋ endcard 9s（DESIGN §5）。★**HOOK-AUDIO**：VOは frame 0 から（先頭に無音ランウェイなし）→ **hook区間も最初からダッキング下で敷く**。**cue時刻は全てPLACEHOLDER — forced-align後の film.json で再ロック**（DESIGN §5 の re-lock 手順で総尺が動く＝EP55 は +71.2s ドリフト。ドリフトは gap budget で吸収し、本表の比率で cue を再配分する）。
**★EP56 固有の最重要差分（FINDINGS R-11・build-binding）**：**BrandOpening は ≤5.0s の被せスティング**。EP53/55 のような10s級の音楽的一段落を作らない。ループ（BUT-contradiction）が ~0:32 に立った**後**に入り、**音楽は連続のまま**、VO下 ≥12dB ダック。レンダ後に **sting 実測長 ≤5.0s** を probe すること。

## ミックス仕様（全編共通・`build_case_film_audio.py` 準拠・数値は実装値）
- **4層**：**L1** VO前面 · **L2** music（`sidechaincompress threshold=0.03 / ratio=8 / attack=25 / release=320` でVOにダック・体感フロア≈**-22**）· **L3** ambience **`AMBIENCE_FLOOR_DB = -18.0` の可聴・定常ベッド（サイドチェインしない）** · **L4** SFXワンショット（章境界 whoosh はビルダー自動配置）。
- **連続ベッド**：章の切れ目で **0.8–1.2s クロスフェード**、無音の穴を作らない（>25s 無音でゲート落ち）。`AMBIENCE_COVERAGE_FLOOR = 0.85` / `AMBIENCE_DISTINCT_FLOOR = 4`（本設計は **7 distinct** で余裕を取る）。
- **統合ラウドネス**：2パス `loudnorm` **-14 LUFS**（±0.5）、TP ≤ **-1.0 dBTP**。
- **アウトロ**：`OUTRO_FADE_DUR = 3.0s` / `OUTRO_FADE_END_MARGIN = 3.5s`（フェード完了は mix 終端の 3.5s 前＝`-shortest` トリムより手前）。全音量チョップ禁止。
- **グルー**：全編に **`MUS-0021`（ambience_paper_trail_static **v2**・document_glue）** を極薄（**-30〜-34**）で敷き、章曲の隙間を埋める。本作の主題＝**紙**（書面の警告・埋められた法的助言・「shredded」・封筒・受領書の山）に一致。EP55 が同系 v1 を使ったため **v2 を採る**（連投時の既聴感対策）。
- **★バージョン方針（EP56 = v2 セット）**：ビルダーの `CHAPTER_MUSIC` 既定は v2 ファイル群。EP53/55 が v1 系で出荷しているため、**EP56 は既定どおり v2 系で統一**＝ビルダー既定との摩擦ゼロ＋3話連続の同一曲を自動回避。

## 章立て → 曲割り（cue sheet・時刻は PLACEHOLDER／DESIGN §2 の5幕とリビール梯子に対応）
| 区間 | video時間(目安) | トラック | 役割/mood | ミックス・cue意図 |
|---|---|---|---|---|
| **HOOK（cold open・VOは0.0から）** | 0–~32 | `MUS-0002` (hook_glass_air_bed **v2**) | hook / cold sparse | VO下ダック。主役は音楽でなく **CRT whine ＋ ガラスの雨＋店のベルの減衰**。ヘルプラインで「2,000が4,000になる」ビートで薄いピッチ上昇1回。**BUT-loop（~0:32）着地の直前に音楽を一段落とし、スティングの入口を作る** |
| **BRAND STING（≤5.0s・R-11）** | ~32–37 | `MUS-0004` (opening_measured_arpeggio **v2**) | opening sting | **≤5.0s の被せのみ**・audio-continuous・VO ≥12dB ダック。曲頭の2小節だけを使い、**解決させずに** Act I ベッドへブリッジ（金OPの音楽的完結は作らない＝ここで11–43sの崖を作らないため） |
| **POST-BRAND（1文＋日付/場所）** | ~37–45 | 新規cueなし（`MUS-0004` の尾を `MUS-0006` へ 1.0s クロスフェード） | bridge | 「roughly 1,000 · one machine」の一文の下で音量を **一段だけ上げて** Act I へ落とす |
| **ACT I — 嘘をつくレジ** | ~0:45–6:00 | `MUS-0006` (explainer_bed **v2**) → 「The helpline had an answer…」で `MUS-0008` (tension_build **v2**) へ | warm-neutral → slow_crescendo | 村の店＝**この作品で唯一のあたたかい帯**（shop-lamp amber と同期・薄い高域）。Horizon 到着＝音楽は変えず **CRT whine を初提示**（ledger leitmotif）。「you are the only one」で 0.8s クロスフェードし tension へ。Bates 解雇（2003）＝クレッシェンドを**切って**無解決で残す |
| **ACT II — 雇い主が検察官** | ~6:00–12:00 | `MUS-0008` 継続（Hamilton/Thomas/Castleton/Misra の各件で loop 再入・層を1枚ずつ足す） | tension_build / machine | tally（起訴数）の打点に loop 再入を合わせ、**「同じことが何度も起きる」構造**を音で刻む。Castleton の £321,000 判決＝一瞬のブレイク。**Misra 収監ビート（11 Nov 2010）は本作の earned breath の1つ＝音楽をほぼ退け ambience＋glue のみ**（悲劇を煽らない・DESIGN の dignity discipline）。act 峰は幕末の SPLIT_COMPARE カード |
| **ACT III — 彼らは知っていた（mid reveal ~50%）** | ~12:00–18:30 | `MUS-0010` (somber_ledger_of_ash **v2**) を基調 ＋ 警報ビートに `MUS-0012` (reveal_hidden_system_clicks **v2**) を**単発 sting** | somber / ignored alarms | 本作の engine。**Ismay報告（2010年8月）／Bracknell の遠隔アクセス／Second Sight／2013年の Clarke 助言** の各「glimpse → 引き出しが閉まる」で `MUS-0012` を1発ずつ（**多用禁止・章内 最大4回**）、そのたび基調は音量を戻さず**一段ずつ暗くする**。QUOTE_CARD（"the word 'shredded' was conveyed to me"）着地は**音楽を薄くし紙・引き出しのSFXを前面**。★**Martin Griffiths の一節は音楽を付けない**（ambience＋glue のみ・上げも下げもしない・sting 禁止・SFX なし）。悲哀を演出しないことが唯一の正解 |
| **リセットビート（55–70%・20–40s）** | ~18:30–19:10 | `MUS-0006` へ短く復帰 | breather / human | **Fenny Compton の村ホール**（2009年11月）。本作で amber が触れない唯一の「人のあたたかさ」＝薄く、椅子とやかんのSFXを聴かせる。30分尺テンプレの必須ブレス（R-18） |
| **ACT IV — 555人の軍隊（primary reveal 開始 65–85%）** | ~19:10–24:30 | `MUS-0008`（2019年の消耗戦）→ Fraser判決で `MUS-0014` (reveal_verdict_at_dawn **v2**) → 和解の内訳で `MUS-0021` glue へ落とす → 2021年4月23日で `MUS-0015` (**v3**) | grind → reveal → false-relief → 唯一のswell | 「not remotely robust」「the earth is flat」の verbatim 着地で `MUS-0014` を立ち上げる。**£57.75M → 手取り約£12M（約2万ポンド/人）は false-relief の反転点：swell を切って static に落とす**（勝ったのに何も戻らない音）。**23 April 2021・39 convictions quashed ＝本作唯一の本当の swell**＝`MUS-0015` を Royal Courts の amber 復活ビート（cold-open callback ~76%：冒頭の女性が書類を持って出てくる）に同期 |
| **ACT V — 議会を動かしたドラマ（cascade・~92%で解決）** | ~24:30–29:00 | `MUS-0015` 継続 → 王室裁可カードで頂点 → Vennells/空席の証人席で `MUS-0010` へ降りる | cascade → cold | 2024年1月1日のITV放送＝`MUS-0012` 単発 sting ＋ 居間のTVの明滅（**実放送音は絶対に使わない**）→ 1.2M署名→CBE返上→**"Every conviction… is quashed"（royal assent, 24 May 2024）で音楽の頂点**。以後は上げない：**空席の証人席・"cancelled and annulled"・£1.6B MONEY_STACK は `MUS-0010` の冷たい面で**。「TO THIS DAY · NO ONE CONVICTED」のヒンジで**音楽を glue まで薄く**し、92%以降は新しい音を入れない |
| **ENDING→Endcard** | ~29:00–1,791.0 | **`MUS-0017`** (outro_last_frame **v2**・end_card) | outro / grey resolution | **align-to-end 配置**（下記）。**高揚させない**＝希望で終わらせず「静かに閉じる」。ledger screen が消灯し、赤い看板が灰色の夜明けに立っている画に、旋律が解決して終わる |

## ED＝「切りのいい所で終わる」（`bgm_ending`・チャンネル正典）
- `MUS-0017` を**曲自身のフレーズ終止が動画終端に一致するよう align-to-end 配置**（ループ途中でブツ切りしない）。`OUTRO_FADE_DUR=3.0s` のクリーンフェードで無音着地、フェード完了は終端 3.5s 前（`OUTRO_FADE_END_MARGIN`）。**BGM はダウンビートで終わる**（R-17・既存ED指令のゲート化）。
- **ending ambience は固定**：ENDING章の ambience ベッドは **`amb_night_window.mp3`**（正典デフォルト／`FORCED_DEFAULT_CHAPTERS` に "ending" が入っており keyword 上書きされない）。**`amb_light_wind` は全編禁止**（「飛行機の音」問題・owner 2026-07-06／07-10）。
- CTA「hit like, so the next story like this gets told…」直後にアウトロ主旋律が解決して静かに終わる。**ナレ/間は不変**。最終ナレ行→ファイル終端 ≤60s（R-17・30分尺）。

## ambience 配車（章ごとに別ベッド・distinctness をゲートが採点）
| 章 | ベッド | 理由 |
|---|---|---|
| HOOK | `amb_rain_street` | 夜明け前の英国の高街・窓ガラスの雨 |
| ACT I | `amb_office_hum` | カウンター裏／帳簿と現金の部屋 |
| ACT II | `amb_empty_hallway` | 停職・取調べ・裁判所の廊下（人を挽く場所） |
| ACT III | `amb_institutional_drone` | Bracknell のサーバ列と内部文書の側＝機械の世界 |
| ACT IV | `amb_courtroom_room_tone` | 村ホール→高等法院→Royal Courts |
| ACT V | `amb_tension_drone` | 議会・公聴会・国が動く一週間 |
| ENDING | `amb_night_window`（固定） | 正典。灰色の夜明けの静けさ |

= **7 distinct beds ✓**（floor 4）。ウェールズ海岸／河口の外景ビートは `amb_night_window` 側に寄せる（**wind系は使わない**）。

## SFX意図（L4・ワンショット）
章境界 whoosh（ビルダー自動）＋ 設計SFX：**店のベルの減衰**（Act I／ENDING で1回だけ回帰）、**レジ引き出しのスライド**、**ガラスの雨**、**CRT whine＝ledger leitmotif（全編で数回まで・常に控えめ）**、**郵便受けに落ちる封筒**（Act I→II→V の三度）、**書類の滑りと引き出しが閉まる音**（Act III の各 closingdoor）、村ホールの椅子とやかん（Act IV リセット）、法廷の扉、1月の居間のTVの明滅（音は murmur のみ）。
**HARD BAN：** 実在人物の音声（Vennells の証言・公聴会・議会・報道アナウンス）／**ITVドラマの音声**／演技の嗚咽・悲鳴／**シュレッダー音**（「shredded」ビートは引き出しとファイルの音で表す＝オンザノーズ回避）／**Griffiths の一節の周辺にバス・車両・衝撃系SFXを一切置かない**（R-SUICIDE）／**法槌（gavel）**（英国の刑事法廷に法槌は無い＝事実誤り）。

## 補助素材：新規取り込みの CC0/PD 音源棚（supplementary・SFXのみ・**登録済み＝使用可**）
- 台帳 **`H:\pd-media\assets\archive\_ledger\freesound.jsonl`**（**取り込み継続中／本稿執筆時点 132件**・実体は `D:\pd-archive\sfx_environment\`）。実測内訳：**`license_decision` は全件 `cc0`**、`usage_tag` は全件 `sfx`、`theme` は全件 `sfx_environment`。キーワード分布は rain / thunder / water / wind / fire / room-tone 系が中心。
- **★権利登録は完了済み（2026-07-28）**：`scripts/register_freesound_sfx.py` で **132件を `SOUND_LIBRARY_RIGHTS.v001.json` へ登録**（id=`FSX-<freesound id>`・`commercial_ok:true`・`attribution_required:false`・`file_sha256_recorded`・`source_url`・`fetched_at` を収載）。台帳は 61 → **193 assets**、`all_commercial_ok:true` 維持。**これで「registry 収載の内部ライブラリのみ」という本プランの拘束を満たす。**
- **★L4 で実際に鳴らすには「2段階」が必要（重要）**：権利登録だけでは**ビルダーから見えない**。`build_case_film_audio.py` は SFX を **`lib / "sfx" / filename`**（=`H:\pd-media\library\sfx\`）で解決するが、CC0 棚の実体は `D:\pd-archive\` にあり **library_root の外**。
  1. **権利登録** — `python scripts/register_freesound_sfx.py --apply` （**実施済み**・`.bak` 自動保存・再実行は冪等）
  2. **ライブラリへの staging** — `python scripts/register_freesound_sfx.py --stage FSX-158691,FSX-407204` で**必要な clip だけ**を `H:\pd-media\library\sfx\` へコピー（一括コピー禁止＝ライブラリを汚さない）。staging 済みかは registry の **`build_visible: true`** で判定でき、`--apply` 再実行でフラグが再同期される。
  - 検索は `python scripts/register_freesound_sfx.py --list rain` / `--list "room tone"`。整合性は `--verify-sha N`（ledger の sha256 と実ファイルを突合。**FSX-0087/0093/0130/0005/0031/0080 の6件で PASS 実測済み**）。
- **EP56 に効く候補**（すべて CC0・雰囲気レイヤ用）：**`FSX-158691` / `FSX-158692`** "Distant Thunder and Rain from Half Open Window"（**半開きの窓の雨＝本作の店内ビートに最適**・158691 は **staging 済み**）、**`FSX-778366`–`FSX-778368`** "Heavy Urban Rain With Distant Thunder"（夜の高街）、**`FSX-407204` / `FSX-407205` / `FSX-407207`** "room tone small with door and window open … distant traffic"（狭い部屋の room tone＝カウンター裏・取調べ・407204 は **staging 済み**）。
- **使用ルール（拘束）**：① これは **L4（SFX／薄い追いレイヤ）専用**。**L3 の正典 ambience ベッド集合（`AMBIENCE_BEDS`）は置き換えない**（ビルダーが固定・distinctness 採点の対象）。② 上記の**2段階（--apply → --stage）を通っていないファイルは出荷ミックスに入れない**。③ **wind 主体のファイルは採らない**（`amb_light_wind` の「飛行機の音」前例）— 該当行は registry の `pd_use_note` に **WIND/WAVE-HEAVY** 警告が自動で入るので、ナレ下で必ず試聴してから採否を決める。④ 雷は**遠雷のみ**（近接の落雷は本作の抑制トーンに合わない）。⑤ CC0 のため attribution 不要だが、provenance（source_url・fetched_at・sha256）は registry に残したまま運用する。⑥ 取り込みは継続中のため、**新しい行が増えたら `--apply` を再実行**すれば追加分だけが登録される（id は freesound の source id 由来＝**連番ではないので既存 id は決してズレない**）。

## 事後mix手順（レンダ後）
1. Remotion最終mp4（VO込み）取得 → **総尺を ffprobe で実測**し、本表の cue を比率で再配分（forced-align 後の film.json が正）。
2. 上表を video 時間へ配置＋**0.8–1.2s クロスフェード**＋glue（`MUS-0021` -30〜-34）。
3. sidechain ダッキング（threshold=0.03/ratio=8/attack=25/release=320）→ 2パス `loudnorm` **-14 LUFS**。
4. Endcard **align-to-end** ＋ 3.0s フェード（完了は終端 3.5s 前）。
5. `check_final_acceptance 56` の **`bgm_present` / `bgm_ending` / `loudness` / `sound_layers`** ＋ **sting 実測長 ≤5.0s の probe**（R-11）＋ **末尾10秒を耳チェック**。
6. 「音楽ほぼ無音」指定のビート（Misra 収監・Griffiths の一節・shredded の QUOTE_CARD）でも **glue と ambience は必ず残す**＝完全無音を作らない（>25s 無音でゲート落ち）。

> ※ cue 時刻は forced-align 後に必ず再計算（本表は語数比例の PLACEHOLDER）。**候補トラックは全て rights registry 収載の内部ライブラリのみ**（外部の未検証曲は名指ししない）。必要な mood に検証済みトラックが無い場合は**曲名でなく mood/tempo/key で CUE を指定する**方針 — 本作でその扱いになるのは次の1点のみ：**Act IV の「false-relief の反転」に専用の“熱を抜く”キューが無い**ため、`MUS-0021`（document_glue）への降下で代用している。専用キューを起こす場合の仕様＝**60–66 BPM・短調（D minor 想定）・旋律なし・低弦とテープノイズのみ・8–12秒・解決しないまま消える**（新規生成する場合も rights registry へ登録してから使用）。
