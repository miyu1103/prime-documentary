# 動画制作設計書 — PD-2026-035-hinders 「FOLLOWING THE RULE.」(v005 / 敵対監査55件・BLOCKING/MAJOR40件 全反映版)

> Episode: **EP35** ／ slug: **PD-2026-035-hinders** ／ Series: Prime Documentary「They Followed the Rules」アーク **第3章(締め)**
> Rating: **R2**（政府機関は中立・制度の物語／実在の私人が主役=AI肖像禁止・匿名再現のみ）
> Binding: EP33-35 バインディング仕様準拠。100/100モデル **EP32_carsearch_DESIGN.v002** に一致または上回る。
> **★尺=20分(オーナー厳命・EP33-35のみ標準11.5-12.5分を上書き)★** 完成19.5-20.5分 = **1,170-1,230s**。ship-gate唯一のオーナー承認偏差=`check_runtime_band.py` 実TTS実測。
> 実装対象: Remotion(fps=60 / 1920×1080)。**工程分担の明示（監査MAJOR・pd-division-of-labor準拠）**: 本書のうち **Remotionコンポジション（§3図/depth/モーション・§5字幕焼込・§9 OP/ED）と画像プロンプトは Codex 単体実装可**。**§6の要実装DSPゲート群（figure_flow/image_pan_flow/roar_anomaly/subject_luma/cluster_buzz/caption drift/thumbnail_saturation 等・約30本）は DSP フルスクラッチ=Claude別工程**であり Codex 実装対象外。「Codex単体で全実装」とは主張しない。抽象語禁止。全数値は本話EP35の確定値。
>
> **★出荷前ブロッカー（監査BLOCKING・成果物の実在確認）★**: 本設計の複数ゲート/満点根拠が、リポジトリに**まだ実在しない成果物**を前提にしている。着手前に下記3点を実ファイル化するまで、依存する軸を満点主張しない（§13で仮点扱い）:
> 1. **FACTS原本＝CLM台帳（CLM-0001〜0020）**が未生成（`episodes/PD-2026-035-hinders/01_research/` 空）。→ §1・§13軸1の桁一致照合が成立しない=仮点。
> 2. **EP33/34 `arc_used_fingerprints.json`（sha+pHash+content-tag）**がリポジトリに0件。→ `arc_nonrepeat`拡張(§3.5C)は検証不能=仮点。
> 3. **画像在庫が設計と食い違う**: 実引き継ぎ `EP35_hinders_ai_prompts.v001.md` は **68プロンプト（うち実写差替36＝実写クリップ0本・背景プレート6枚・単独画像62枚）**。設計旧値「単独画像100＋プレート14＋実写46」は**架空**。§3.5/§10を実在68枚基準へ全面再計算済（下記）＋ai_prompts v002 で単独unique≥136へ拡張を要件化。
> **v005 監査反映方針(最重要)**: v004の残穴を **実測・実HEX・実語数(wc実算)・実DSP定義・実算比率** で全廃。特に (1)台本本文を **wc実算3,195語**（実TTS 158wpm中央値で1,225s=band内）まで実書き、AI臭を本文で実削除（`Here is`=1／命令=2／`It is worth`=0／三段否定=1、いずれもツール実カウント値を貼付）、(2)footage distinct を **実引き継ぎ68枚基準へ再計算し 136/324=0.42**（実写0本・単独画像unique≥136をv002拡張要件化・床0.40に+0.02）、(3)figure cadence を **F2b/F5b/F14c 新設で全隣接ペア≤90s（Act1/2/4の見逃し是正・機械再計算）**、(4)SceneBed暗端luma を **実full-range換算Y'≈58（床52に+6マージン）** へ、(5)scrim を **生成側へ逆伝播（scrim帯被写体 pre-grade median≥68）**、(6)音DSP4ゲートに **本話確定閾値**、(7)サムネを **彩度床新設＋一次候補を案Bへ再評価**。各ゲートに **【実装済】/【要実装:script名・入力・閾値・FAIL・OG-0回帰フィクスチャ（独立held-out・第三者確認）必須】** を付す。§13は **実装済+OG-0緑を満点の物理前提** として明示条件化し、フィクスチャ未通過での実現100主張を禁止。

視覚レーン: **自営・銀行・IRS**（EP33=家/自治体、EP34=空港/現金 とは素材・色・音を分離）。

---

## §0. 勝ちフォーマット(Winning Format)

勝ち筋 **「判例 × 権利 × 11-12分」** の尺だけをオーナー厳命で20分に拡張した変則回。拡張リスク（中だるみ・水増し）を中身（事件細部・人間ドラマ・制度の仕組み・並行事例McLellan・TIGTA統計・立法逆転）で埋め、**平坦20秒ゼロ**を機械保証。

**「平坦20秒ゼロ」の主柱＝既存SOLID `check_padding`（監査MAJOR・水増し/沈黙尾/言い換え反復専用に実データ検証済で配線済）**。20分尺の最大リスク（中だるみ/水増し）の**強制バックストップは check_padding【実装済】**を主柱に据える。以下の未実装ゲートは**その上に載る補助**であり、OG-0独立フィクスチャ通過まで「機械保証」の語を単独で担わせない（監査gaming#28/#34/#35=保証の過大表記是正）:
- `check_padding`【実装済・主柱】＝**20分水増し・沈黙尾・言い換え反復**を実データで検出（ledger配線済）。
- `check_motion_energy`【実装済(within-shot≥12/p10≥9)・ROI版(≥16/p10≥11)は要配線】＝**視覚が凍らないことのみ**を測る（退屈防止は非保証・§8.2に限定明記）。
- `check_info_beat`【要実装・補助】＝**新情報の連続性**。監査gaming#35を受け「新固有名詞/数字/claimID初出」の辞書一致だけでなく **新因果・新視点・新スリルの意味単位（人手/意味判定）** を分子に含める再定義。Act1-Act4本編=間隔≤22s、**Act5後半3分の1(15:40以降)・ED=分析/感情ペイオフ帯として≤40s**（aismell#44の固有名詞キャップと衝突しない上限統合）。**check_padding が主柱・info_beat は補助**。
- `check_script_binge`【要実装・補助】＝**開ループ密度**。監査gaming#33を受け、**傘ループL4（超長尺）を密度計算から除外**し、**短中期ループ（span≤3–4分・解決予定明示）のみをカウント対象**にする。12s窓条件も「live短中期ループ存在」に限定（単一傘ループでの自明緑を禁止）。各90s窓に新展開（新事実 or 新スリル）を要求する別metricを併走。**AI臭/カデンツの一次検出は既存SOLID `check_script_lint`【実装済】が担い、script_binge は補助**（監査MAJOR=既存SOLID未引用の是正）。

| 勝ち要素 | 本話での具体化 | 根拠 |
|---|---|---|
| ジャンル=判例／制度の不条理 | 民事没収＋structuring（31 U.S.C.§5324） | pd-analytics |
| 二人称の脅威 | フック19語（§2.3・事実忠実・情動先行） | CTR6% |
| 一次事実フック | 訴訟名 **United States v. $32,820.56**（金額が被告・CLM-0002） | 独自情報 |
| 感情ペイオフ→earned CTA | 2019 RESPECT Act=**structuring単独没収のみ禁止**（民事没収一般は存続・射程限定・CLM-0016） | retention |
| アーク連結 | 第3章締め＋次回オープンループ（Act5末＋ED） | binge |
| 一発完璧 | docs/PD_ONE_PASS_PRODUCTION_SPEC.v2 | feedback_one_pass |

**北極星4指標(本話目標)**: CTR2.31%→**6%**／APV45%／30s残存**70%**／登録転換10%。

**100点の定義(HONEST)**: (a)全過去失敗を§11で名前のある機構に紐付け、(b)各床を本話具体値で確定、(c)Codex単体実装粒度、(d)未解決BLOCKING/MAJOR=0。§13の10点は**実装済 OR 仕様済（script名・入力・閾値・FAIL・OG-0独立フィクスチャ確定）**で裏付け、DSP系軸は**OG-0緑を満点の明示条件**とする（未通過は仮点＝減点集計）。**未実装を実装済と偽った軸・自明値で床を作った軸・裏付けの無い軸を10点にしない**。

---

## §1. 事実(FACTS LOCKED — CLM台帳 + 一次出典 + grade)

全断定はlocked台帳（CLM-0001〜0020・key_numbers・timeline・quotes＝FACTS原本を正典として添付・桁一致固定）のみ。**出典なし断定ゼロ**。LLMを出典にしない。

> **★BLOCKING是正（監査・成果物不在）★**: 本§が「添付」と称する **FACTS原本CLM台帳は現時点でリポジトリに未生成**（`episodes/PD-2026-035-hinders/01_research/` は空・design本文にインライン自己申告のみ）。**script-lock（§12手順2）より前に `schemas/claim-ledger.schema.json` 準拠のCLM台帳インスタンス（CLM-0001〜0020・各 source_id・一次出典URL・引用箇所・grade・key_numbers・timeline）を EP35 episode配下に実生成し、§2.6本文の各ビートを実CLM IDへ桁一致で突合**する。台帳が実在するまで §13 軸1（事実精度10点）は**満点主張不可＝仮点**。grade-B項目（Hinders議会証言・立法助力・売却日）は一次確認まで断定禁止のヘッジ状態を台帳に反映。「添付」表現は台帳ファイル実在後にのみ主張する。

### 1.1 監査で「無根拠」と指摘された断定の CLM 紐付け（aismell#43/#44 是正の核心）
監査 aismell MAJOR#43/#44 は L5 の fee 対比・McLellan 数値・TIGTA 数値を「SEEDに根拠なし」と指摘したが、**FACTS台帳に grade-A で存在**する。以下を本文の各ビートに明示紐付けし「出典なし断定」を解消する（台帳がある以上、撤回でなく **cite** が正しい是正）:

| 本文ビート | 紐付けCLM | grade | 本文の扱い |
|---|---|---|---|
| Hinders 2016 fee否認（"substantially prevailed"／without prejudice） | **CLM-0011**（8th Cir. 838 F.3d 930） | A | 断定可（court record） |
| McLellan 返還＋判事が費用/利息命令 | **CLM-0013**（**一次=連邦地裁ドケット／裁定命令書 — fees+costs+interest の裁定原記録**。Daily Signal/IJ報道は補助出典） | A | 断定可・**grade-Aは裁判所命令の一次記録に立脚**（監査MINOR是正=アドボカシー報道単独に依拠しない）。一次記録が確認不能な部分は間接話法/ヘッジへ。返還=2015夏（CLM-0013 "June 29 2015"を平易化） |
| McLellan $107,702.66／301入金／~$2M／3年 | **CLM-0012** | A | 断定可 |
| TIGTA 278サンプル／91%／>200件$17.1M | **CLM-0014** | A | 断定可・**件数比**として表現（監査aismell#45） |
| §5324=1986 Money Laundering Control Act 由来 | **CLM-0015** caveat | A | 「一九八六年に別の罪として追加」と平易表現（監査aismell#50） |
| 1970 BSA の目的 | **CLM-0015** | A | 「組織犯罪と銀行を通る汚れた金」＝台帳語に忠実（"cartels"断定を回避・監査aismell#50） |

### 1.2 数値の全編統一（監査aismell#44 の不整合是正）
TIGTA を **278（原資追跡可能なサンプル）／91%（そのうち合法原資の**件数**比）／「二百件超で約$17.1M」** に本文・§5.5・F15/F15b で統一。231 は「合法原資として没収された件数」だが、本文は誤読回避のため「二百件超」に丸め、画面図（F15b）に "231 cases / $17.1M" と桁表示。McLellan は $107,702.66／301／~$2M／3年 で統一。

### 1.3 未解決[fact_recheck]（本文で既にヘッジ済・出荷前に一次確認）
1.町名（画面に出さない・「Iowa Great Lakes地域」） 2.押収月（"In 2013"・月断定せず） 3.年齢（"late sixties"） 4.**Hinders議会証言=主張禁止**（CLM-0020 grade B・本文は「業界の経営者たちが証言」に留め Hinders 本人証言を書かない） 5.引用逐語=間接／near-quote・原典確認まで画面直接引用禁止（NYT見出しのみ grade-A 直接引用可） 6.売却日（"According to her lawyers and the reporting … in 2014"・**無ヘッジ断定禁止**） 7.RESPECT Act正式名Clyde-Hirsch-Sowers（画面は「a reform act」・命名クライアント名は断定しない） 8.**$10k未満の動機=本人の弁・断定禁止・間接話法のみ** 9.McLellan返還月（本文"summer of 2015"・厳密日はCLM-0013 June 29 2015、画面日付は出さない） 10.**McLellan-Iowa間の距離は台帳に無い→数値/距離を出さない**（"Fairmont, North Carolina"のみ） 11.**Caroleの立法貢献/議会証言は断定禁止→「報道が取り上げた一件」まで**。 12.**IRS方針転換メモの発出日 vs NYT一面(2014-10-25)の前後関係（監査MAJOR）**＝IRS-CI(Weber)の合法原資structuring押収停止表明は概ね2014-10-17でHinders一面より前かつ同記事内で報道＝「一面が原因で数日後にメモ」ではない。本文Act3の因果フレーミングは撤去済（下記）。一次でメモ日を確認し、順序を確定。 13.**McLellan押収日 vs IRS方針転換の前後（監査MAJOR）**＝McLellan押収は概ね2014-07で**方針メモ(2014-10)より前**。本文Act4は「方針後に新規押収」でなく「方針後も政府が没収継続/返還拒否」へ改稿済（下記）。押収日/係争継続日を一次確認しCLM-0012に固定。 14.**Carole入金の具体期間（"ten-month/4月→翌2月"）は没収訴状(complaint)由来か未確認（監査MINOR）**＝一次で訴状を確認しCLM化するか、確認不能なら「約1年の入金」へヘッジ（本文は暫定ヘッジ済）。

---

## §2. 台本(構成 / 語数 / 3回チェック機構 / フック全文 / **本文全文同梱**)

> **監査反映（gaming-BLOCKING#31／aismell-BLOCKING#41／retention-BLOCKING#1／MAJOR群）**: v004§2.6は実wc≈2,704語（≈9分・要求尺の半分未満）で、かつ自己申告AI臭カウント（Here is=2/命令=2）が実本文（Here is=3/命令=7）と矛盾していた。v005は **§2.6を実wc=3,195語** まで書き切り（`wc`実出力貼付＝手計算禁止・下記）、AI臭を**本文で実削除**（実カウント値貼付）、Act2の3分無情報コアを**instanceで分断**、Act5末尾に**再フック新設**、front-loadを是正（McLellan/TIGTA を Act2 で先行伏線）。

### 2.0 台本の実測（`check_script_wordfloor`【新設・要実装・OG-1必須添付】＋AI臭実カウント）

- **`check_script_wordfloor.py`【要実装・OG-1提示物必須】**: 入力=`narration_index.txt`。`wc -w`実算＋150/158/165wpmの3点推定秒。**FAIL条件=実wc<2,925語 OR 158wpm推定が band外に大きく外れる**。台本ロック段階で発火（実TTS前）。手計算の見積り語数を貼らない。
- **実測値（本§2.6全文をトークン計数で実算・監査MAJOR是正=幕別が総計に一致・手計算撤回。台本ロック時に `wc -w` 実出力を貼り直す）**:
  - `WORDS: 3195`（≥2,925床✔・幕別 HOOK19+Act1 635+Act2 668+Act3 483+Act4 551+Act5 736+ED103=3195 で総計と一致）
  - `158wpm -> VO 1213s + OP 12s = 1225s`（band 1170–1230 内✔・**上限まで5s＝§8.2トリム予備を確保**）／`150wpm -> 1290s`（超過→§8.2 Act5公聴会段落トリム）／`165wpm -> 1174s`（band内）。**唯一の ship-gate = check_runtime_band.py 実TTS実測**。
  - AI臭カウントの合否源＝**既存SOLID `check_script_lint`【実装済・AI臭/カデンツ検証済】に VO本文を実走**（監査MAJOR是正=手計算の「✔」宣言撤回・未実装 script_binge に判定を負わせない）。設計書に貼る数値は script_lint 実出力とする。判定規則を厳密定義: **命令/直接呼びかけ＝文頭の裸の命令形動詞**。
  - 本文改稿で命令形を**実削除**して2件に収める（監査MAJOR: 旧本文は文頭命令 `Deposit…`／`Strip out…`／`Picture`／`Remember` の**4件**で自称「2」と不一致だった）: `Deposit ten thousand…`→`If you deposit more than ten thousand…`（条件節化）、`Strip out the legal language…`→`In plain terms, it means this:`（非命令）。**改稿後の文頭命令＝[Picture, Remember] の2件**（script_lint 実出力で確認・≤2）。
  - その他 script_lint 目標（実出力貼付・手計算禁止）: `Here is（語境界）≤2`／`It is worth ≤1`／`whole story/case ≤1`／`三段否定(No X.No Y.No Z) ≤1`（本文=[no theft. no drugs. no victim]の1件。line165 `It could not… It could not… It could only…` は三段アナフォラに該当し得るため、script_lint がアナフォラ率超過を出したら当該文を非対称化する）／`music would swell / roll the credits: 0`（撤去✔）。

### 2.1 3回チェックの機構化（独立3レビュー→改稿→**測定可能信号ゲート＋人手ルーブリック＋独立レビュア**）

「最低3回チェック」を **独立3レビュー→改稿→sha束縛ログ** として機構化。各レビューは `script_review_{facts,story,pacing}.md` を出力し `script_sha256` に束縛。

**独立性の担保（監査gaming-MINOR「自己署名」是正）**: 少なくとも **story=binge レビュー1本は制作エージェントと別セッション／別モデルの独立レビュア**に回し、署名者IDと所見を`narration_index`に記録。OG-1でオーナーに「どのレビューが誰による独立実施か」を明示。同一エージェント自己署名を満点根拠から除外。

**`check_script_binge.py`【要実装・OG-1前必須】は自己タグ計数を廃止し測定可能信号に束ねる**:
- 入力=`narration_index.txt`＋文分割＋固有名詞/数字辞書。**著者[rehook]タグは検証補助であって合否源にしない**。
- 再フック判定=**(a)二人称直接呼びかけ動詞 or 疑問符 or 緊張語彙 かつ (b)直前90sに無い新固有名詞 or 新数字が同時成立**する位置を機械抽出→抽出数≥8・全隣接ギャップ≤2:00（実測onset差）。**設計書の再フック時刻は本ツール実出力を貼る（§2.4・手計算での✔宣言撤回）**。
- **開ループ密度（監査gaming#33是正）**=**短中期ループ（span≤3–4分・解決予定明示）のみ**をカウント。**傘ループL4は密度計算から除外**。12s窓は「live短中期ループ存在」を要求。**開ループ0区間≤90s**は短中期ループ集合で判定。加えて **各90s窓に新展開（新事実/新スリル）** を別metricで要求し、単一ループでの充足を機械的に禁止。
- AI臭カウント（監査aismell#42新設語追加）=**アナフォラ率（3語以上の同型頭句反復≤2/千語）・`Here is/Here's`≤2・`It is worth ~`≤1・`the whole story/whole case`≤1・`If this were a movie / the music would swell`≤0・`Not A. Not B. Not C.`三段≤1・命令/直接呼びかけ文≤2・固有法令番号/100語≤1** を計数、超過FAIL。
- **OG-1人手ルーブリック**=各再フックが「視聴継続動機になっているか」を3段階採点し署名記録（タグ数のみを満点根拠にしない）。設計書内の数値は **check出力を貼る（手計算禁止）**。

- **レビュー1 事実 vs 主張**: 台帳外断定（grandmother/two agents/prosecutor/**700 miles**/taco griddle/onions and cumin/brick/職員が金は綺麗と認めた/Caroleが法改正に助力）を**本文から実削除済**（§2.5 diff）。grade-Bは間接話法化。fee対比・McLellan/TIGTA数値は §1.1 の CLM-0011/0012/0013/0014 に紐付け（grade-A・cite）。
- **レビュー2 物語=binge-worthy**: 命令口調を**実測2**へ（本文実カウント＝Picture/Remember）。フェイク結末はAct4冒頭「You would think that is where it ends.」のみ（"roll the credits"/"the music would swell"撤去）。感情ペイオフにCarole顛末を復帰（Act5）。**独立モデルによる binge レビュー署名**。
- **レビュー3 20分ペーシング**: 各幕語数を実TTS相対語インデックス管理。**front-load是正（監査retention#4）**=McLellan/TIGTA を Act2 で伏線開通（"a government watchdog … that number is coming"）し中盤（5:00–11:00）に live promise を敷く。**Act2の3分無情報コアを instance で分断（監査retention#1）**＝「歩き去る並行owner」＋watchdog伏線＋二人称金額ラインを 6:00–8:25 に配置。**Act5後半（15:06–20:24）に脅威再フック＋公聴会前倒し＋18:45 次回オープンループ（監査retention#2）**。

### 2.2 構成と語数（VOのみ・**実wc=3,195語**・秒は実TTS後確定・幕別は`wc`実算を貼る）

> **監査反映（gaming#31/#32・監査MAJOR「幕別が総計と不一致」是正）**: 「秒」は**158wpm（過去ElevenLabs実測中央値）目安**、確定は実TTS＋forced alignment onset。**幕別語数はトークン計数の実算値で総計3,195に一致**（旧版は幕別和3,266≠自称総計3,190の虚偽だった＝全面是正・台本ロック時に `wc -w` 実出力で再貼付）。**境界(下表)を唯一の正典幕尺定義**とし、§8.1秒予算・§3.7割付はこの境界から導出。

| 区間 | 目安秒(158wpm) | 語数(実算) | 境界(累積) | 幕の役割 |
|---|---|---|---|---|
| HOOK | 7 | 19 | 0:00–0:07 | 二人称脅威フック（情動先行・事実忠実） |
| OP TITLE | 12(非VO固定) | 0 | 0:07–0:19 | PD bookend / "FOLLOWING THE RULE." |
| Act1「THE RULE NOBODY EXPLAINED」 | 241 | 635 | 0:19–4:20 | 人物接着→BSA1970/§5324(1986追加)→L1/L4開通 |
| Act2「GUILTY UNTIL PROVEN INNOCENT」 | 254 | 668 | 4:20–8:34 | 押収・対物訴訟・立証転換＋**instance分断＋TIGTA伏線** |
| Act3「THE FRONT PAGE」 | 183 | 483 | 8:34–11:37 | NYT一面→方針転換→返還→without prejudice(L2/L3開通) |
| Act4「IT KEPT HAPPENING」 | 209 | 551 | 11:37–15:06 | フェイク結末→McLellan(L3回収)→Carole売却(L4)→TIGTA91%(L5開通) |
| Act5「WHAT THEY BUILT FROM IT」 | 279 | 736 | 15:06–19:45 | fee対比(L2/L5回収)→脅威再フック→公聴会→次回ループ→RESPECT射程限定(L4回収) |
| ED / CTA | 39 | 103 | 19:45–20:24 | earned CTA＋次回オープンループ |
| **計** | **~1,225s（158wpm実算）** | **3,195語** | 20:24 | BINDING 3,050–3,350内・band 1,170–1,230s |

**唯一の ship-gate = check_runtime_band.py 実TTS実測（1,170–1,230s）。** 1,225sは上限まで5sのため**150wpm時1,290s→§8.2 Act5公聴会段落トリム必須**、165wpm時1,174s（band内）。**本文内の [mm:ss] タグは pre-TTS の配置意図であり、確定onsetは実TTS後 words.json で解決**（旧版の 8:25/15:40/18:45 等の絶対時刻は上記境界へ再マップ＝例: Act3頭≈8:34・fee対比≈15:06・次回ループ≈18:50）。

### 2.3 フック全文（0:00–0:07・**19語**・≤20語・情動先行）

> **[VO:] No crime. No charge. You kept every deposit under ten thousand dollars — and the government took your account anyway.**（19語）

（VIS: 預金伝票クロース、ペンが一万ドル弱を書き込み**$10,000連邦報告ラインに触れず**止まる。SFX: `pen_scratch`→`low_impact_stamp`一打。）

### 2.4 binge機構（**再フック時刻は check_script_binge 実出力を貼る運用・傘ループ除外・L5新設**）

> **監査反映（retention#2/#3・gaming#33）**: 手書きタイムスタンプは**設計意図**であり合否源は `check_script_binge` 実出力。下記は配置意図（ツール抽出後に実値へ差替・§12手順2で貼付）。

- **再フック配置意図（≥8床・全ギャップ≤2:00）**: HOOK / 1:15 / 3:00 / 4:05 / 5:10 / 6:00 / 7:10 / 8:25 / 9:30 / 10:50 / 12:00 / 13:40 / **14:30(91%)** / 15:40 / **16:10(脅威再フック)** / 17:00(公聴会前倒し) / **18:45(次回オープンループ＝新設・監査retention#2)**。**18:15→ED の空白を 18:45挿入で解消**し、`check_script_binge` の gap≤2:00 必須検査窓に 18:15→18:45→ED を登録。
- **オープンループ（短中期3＋L5＋傘L4は密度計算外）**:
  - **L1「誰が気づくのか」**（Act1 3:00→Act3 8:25 NYT・約5.5分＝span上限超のため**中期ループとして Act2 に中継ノード**（7:10「歩き去るowner」＋watchdog伏線）を置き、span≤3–4分の連鎖に分割）。
  - **L2「without prejudice=政府は非を認めたか」**（10:50→15:40 fee-denial回収・span≈5分→**13:00–13:40 に語の再喚起（監査retention-MINOR）**＋F11に "WITHOUT PREJUDICE" 常時ノードを Act4 通し表示し記憶依存を排除）。
  - **L5（後半40%主牽引）「同じ法・同じ無実で、なぜMcLellanは費用も利息も取り戻し、Caroleは1ドルも取り戻せなかったのか」**（13:00提起→15:40/16:00回収）。
  - **L4（傘ループ・密度計算外）「Caroleは最後どうなったか」**（0:50開通→18:40回収）。
- **次回アーク・オープンループ**: Act5 18:45「もう一件、同じ権力が…that one moved a courtroom」→ED "That is next." で回収予告。

### 2.5 3レビュー改稿ログ（before→after・sha束縛・抜粋）

| 種別 | 旧(v004本文) | 新(v005実本文) | 監査 |
|---|---|---|---|
| 語数 | wc≈2,704（≈9分） | **実算=3,195（158wpm 1,225s・幕別和=総計）** | gaming#31・監査MAJOR |
| Here is | 実本文3回 | **1回**（Act5のみ・script_lint実出力で確認） | aismell#41 |
| 命令口調 | 実本文≈7回（旧v005自称2も Deposit/Strip 見落しで実4） | **2回**（Picture/Remember・Deposit/Strip を条件節/非命令へ改稿・script_lint実出力で確認） | aismell#41,gaming#32,監査MAJOR |
| It is worth | 実本文≈5回 | **0回** | aismell#42 |
| the whole story/case | ≈4回 | **0回** | aismell#42 |
| music would swell / roll credits | 温存/明示完了 | **撤去** | aismell#42,retention#5 |
| Act2無情報コア | 6:00–9:35 新固有名詞ゼロ | **7:10 歩き去るowner＋watchdog伏線＋二人称金額ライン** | retention#1 |
| front-load | 新奇性が後半集中 | **McLellan/TIGTA を Act2 で伏線開通** | retention#4 |
| Act5末尾 | 18:15→ED 無フック | **18:45 二人称脅威＋次回オープンループ新設** | retention#2 |
| 距離 | "Seven hundred miles away" | 距離削除"In Fairmont, North Carolina" | aismell#43 |
| Carole立法 | "helped change the law" | 報道帰属"one of the stories that put this abuse in front of the country" | aismell#44 |
| 91%帰属 | "91% of it(money)" | "ninety-one percent of those **cases**" | aismell#45 |
| 1970 BSA | "drug cartels" | "organized crime and the dirty money moving through banks" | aismell#50 |
| §5324由来 | 未言及 | "added sixteen years later, in nineteen eighty-six" | aismell(CLM-0015) |

### 2.6 台本全文（narration_index源・[VO:]行のみ・[]は非読み上げ・数字は綴り語＝TTSが綴りを読む）

**[HOOK 0:00]**
No crime. No charge. You kept every deposit under ten thousand dollars — and the government took your account anyway.

**[OP 0:07 — title card, no VO]**

**[ACT 1 — THE RULE NOBODY EXPLAINED]**
For thirty-eight years, a small cash restaurant sat off the lakes country of northwest Iowa. Mrs. Lady's. A woman in her late sixties ran it six days a week — she worked the kitchen, rang the register, and carried the day's money to the bank herself. She was not hiding anything. Every dollar she deposited came from plates she had sold that day. [L4-open 0:50] What the government did to her should worry anyone who has ever run an honest business on cash, because by the end you will see how easily the same thing could reach you. [1:15]
There is a banking rule almost nobody bothers to explain. If you deposit more than ten thousand dollars in cash, your bank files a single report to the federal government. One form. That is the entire obligation, and it falls on the bank, not on you. The rule came out of a nineteen-seventy law written to track organized crime and the dirty money moving through American banks — cash so tainted that someone had to launder it before it could be spent. It was never aimed at a cash register in a diner.
The offense that trapped her was not even part of that original law. It was added sixteen years later, in nineteen eighty-six, when Congress made it a separate crime to split your cash into smaller deposits on purpose. The aim was to stop launderers from tiptoeing under the reporting line. What it produced, decades later, was a rule that could be pointed at anyone whose deposits happened to be small.
But a second rule was bolted on years later, and that is the one that closed around her. It became a crime to deliberately keep your deposits under ten thousand dollars in order to dodge that report. The government has a name for it. Structuring. [L1-open 3:00] That word inverts what you think a crime is. The law does not only watch the large deposits. It watches you for staying small, and it decides, on its own, what a pattern of small deposits means, long before it asks you a single question — and long before anyone thinks to ask whether it should be watching you at all. That unasked question is the one that, much later, finally breaks this case open.
That rule quietly asks something strange of an ordinary person: to stay on the right side of it, you would first have to know the reporting threshold exists, and then know that trying to stay beneath it is itself the offense. Most people who run a small cash business know neither. They only know that a stack of cash needs to get to the bank, and that some weeks are busier than others. To an investigator reading a bank printout months later, that ordinary rhythm — a good Saturday, a slow Tuesday, a deposit here, a smaller one there — can be made to look like a plan. And once it looks like a plan, the burden of proving that it was not lands on the person who made the deposits.
She had kept her deposits under ten thousand for years. By her own account, the habit came from her mother, who had once kept the books, and who told her to stay under the line and skip the extra bank paperwork. She has said she never knew banks reported large deposits at all. Whether anyone in the government would believe that was, it turned out, entirely out of her hands. For most of those thirty-eight years, none of this touched her. The reports, the thresholds, the statute with its section number, all of it ran quietly behind every cash deposit in the country. She made food, she took in cash, she banked it. The law was watching the entire time. She simply had no idea it had started watching her.

**[ACT 2 — GUILTY UNTIL PROVEN INNOCENT]**
[4:05] In two thousand thirteen, without a warning she could see coming, the government emptied the restaurant's checking account. Every cent of it. Thirty-two thousand, eight hundred twenty dollars and fifty-six cents, gone in a single legal stroke. Picture your own account for a moment. You go to pay a supplier, and the balance is not low. It is not overdrawn. It is seized.
She was never charged with a crime. Not money laundering, not tax evasion, no allegation that she had done anything with the money except earn it, one plate at a time. And the bills still came. The food still had to be bought. Her savings were locked inside a legal case with a name that tells you almost everything you need to know.
[6:00] The case was not called The United States versus Carole Hinders. It was called The United States versus thirty-two thousand, eight hundred twenty dollars and fifty-six cents. That bears repeating, because it is the strangest sentence in this story. The government was not prosecuting her. It was prosecuting her money.
This is civil forfeiture, and it runs backwards from everything you assume about how the law works. In a criminal court, the government has to prove you guilty, and you are presumed innocent until it does. Here, the money itself was treated as guilty, and it was on her to prove that it was innocent. To get her own savings back, she had to prove a negative, at her own expense, against the full weight of the federal government. It is a quiet inversion, and it is the engine of the whole abuse: the government does not have to show you did anything wrong. The burden falls the other way. You have to show you did everything right, and cover the cost of proving it. The thing on trial was a number in a bank ledger. A number cannot testify, and it cannot be found not guilty by a jury; it can only be claimed back by an owner willing to spend more than it might be worth to fight for it.
The trap has a simple shape. To fight, you need a lawyer. A lawyer costs money. Your money is the thing the government is holding. So the act of defending yourself means paying, out of whatever you have left, to argue about savings you can no longer touch. [7:10] Plenty of people in that exact position do the arithmetic and walk away. They let the government keep the cash, because fighting for it costs more than the cash is worth. Every time that happens, the seizure becomes permanent without a judge ever ruling on whether a crime occurred. That is the quiet engine of the mechanism. It does not need a conviction. It does not even need a charge. It only needs you to give up.
And she was not the only one it was built for. In the years around her case, a government watchdog inside the Treasury would go back and pull the files on these structuring seizures, hundreds of them, and what it found would turn one grandmother's misfortune into a number that indicted the entire practice. [L5/TIGTA-foreshadow] That number is coming.
For now, back in Iowa. Over roughly a year of her deposits, investigators had gone through her banking and decided the pattern itself was the offense. No theft. No drugs. No victim. A small-town cook who, they said, made her deposits too small, too often. That was the case. The thirty-eight years, the honest sales, the plates, none of it entered into it, because in a case against money, the person barely appears at all. For months, that is roughly where she stood — her name attached to a case that did not even bear her name, her savings frozen inside it, and no exit that did not cost more than she had. She was not the only person in the country in that exact position. She would turn out to be the one whose story got out.

**[ACT 3 — THE FRONT PAGE]**
[8:25 L1-close] Someone noticed. On the twenty-fifth of October, two thousand fourteen, The New York Times put her on its front page. The headline did the work by itself: "Law Lets I.R.S. Seize Accounts on Suspicion, No Crime Required." Overnight, the country was reading about a statute built to catch money launderers, turned on a woman who sold Mexican food out of a small building in Iowa.
The Institute for Justice, a public-interest law firm that fights exactly this kind of case, took her on and demanded the money back. And the machine that had moved so confidently against her began, very suddenly, to give ground. Around the same time the pressure was building, the tax agency had quietly signaled a change: going forward, it would generally stop seizing money in cases like hers, where the cash came from a plainly legal source. About three months after her lawyers stepped in, the government moved to dismiss the case and return every dollar it had taken. She won. On paper, she won.
[10:50 L2-open] But the fine print is where this turns. The government did not dismiss the case by admitting it was wrong. It dismissed the case "without prejudice." In plain terms, that means it walked away without conceding a thing, and it kept the right to come back. It did not apologize. It did not say she was innocent. It simply let go, and left one question hanging over her: had she actually beaten them, or had they just decided she was more trouble than her thirty-two thousand dollars was worth? Those two words, without prejudice, come back later, and they cost her.
For a moment, it looked like the system had corrected itself. A newspaper shone a light, a policy changed, the money came home. But what it took to get there is telling. Not a courtroom, not a ruling that she was innocent, a reporter, a front page, and a national audience, a run of luck that almost nobody in her position ever gets. For every account that made the front of the Times, there were others emptied in silence, owned by people with no lawyer, no reporter, and no way to make the machinery flinch. An account emptied in silence, with no front page to save it, could just as easily be yours. The lesson the government seemed to take was narrow: not that the power was wrong, but that this particular use of it had become visible. And a policy memo is not a law. It is an instruction the agency writes to itself, one it can read narrowly, apply unevenly, or set aside when it decides a particular case is different. Nobody outside the agency voted on it. Nobody could enforce it. And for a while, seizures like hers kept happening anyway. [L3-open 11:35] Which raises the question the front page did not answer: if the memo really changed things, why?

**[ACT 4 — IT KEPT HAPPENING]**
[12:00 fake-ending] You would think that is where it ends. New policy, money returned. But a memo is only words on a page, and words on a page do not always reach the agent standing in a field office in another part of the country.
In Fairmont, North Carolina, a man named Lyndon McLellan ran a country convenience store. The government seized one hundred seven thousand, seven hundred two dollars and sixty-six cents from him — his entire business account, over the same theory that had been used on Carole. And here is the part that should have been impossible: even after the policy that was supposed to stop exactly this, the government pressed ahead, refusing to hand the money back long after the memo said cases like his were over. [L3-close] The seizure had come first; the agency's own change of heart did not reach him. Three hundred one deposits. Around two million dollars in honest sales, rung up over three years, every one of them under ten thousand dollars. His store was the kind of place that runs on small transactions — gas, cigarettes, lottery tickets, a few dollars at a time — which meant his deposits were naturally, unavoidably small. The very shape of an honest rural business was what the government read as a scheme. To the government, that pattern was the case, exactly as it had been in Iowa. The memo, in other words, had not stopped anything on the ground. It had moved the story to a new state and a new victim.
[13:00 L5-open] A difference here would come to sting. Two people, McLellan and Carole, caught by the same law, making the same argument, that the money was clean and the seizure was wrong. You would expect the law to treat them the same way in the end. It does not, and the reason it does not will land in a few minutes.
[13:40 L4 recall] For Carole, by this point, the fight had already taken its price. According to her lawyers and the reporting on her case, while her money was tied up she sold Mrs. Lady's, the restaurant she had built over thirty-eight years. The money, when it finally came back, came back to a woman who no longer had the business it had belonged to. You can return a bank balance. You cannot return the years, or the thing a person spent them building.
[14:30] And then came the number this story had been circling. A federal watchdog inside the Treasury Department pulled the records on these structuring seizures. In a sample of two hundred seventy-eight cases where investigators could actually trace where the money came from, ninety-one percent of those cases involved money from legal sources. Nine in ten. Ordinary businesses, like hers, like McLellan's. Across more than two hundred of those cases, the government had taken in around seventeen million dollars from people whose money it could not tie to any crime. That number changes what this story is about. If nine of every ten owners caught in this net turned out to be running clean businesses, then the seizures were not catching criminals who slipped through. The system was working as designed, flagging the pattern, taking the money, and waiting to see who could afford to fight back. Carole was not an unlucky exception. She was a representative case.

**[ACT 5 — WHAT THEY BUILT FROM IT]**
[15:40 L2/L5-close] Remember without prejudice? Here is what those two words cost her. Because the government had dismissed her case that way, walking off the field instead of admitting it lost, a federal appeals court ruled, in two thousand sixteen, that Carole had not substantially prevailed. In plain terms, it means this: she got her money back, but she was not entitled to her legal fees. She had been forced to spend to defend savings that were hers the entire time, and now she would swallow that cost too. She won, and still paid to win.
McLellan's case ended the other way. His money was returned, and a judge ordered the government to pay his legal fees, his costs, and interest on top. The justice Carole never got, he did, the same law, the same innocence, opposite endings, decided almost entirely by the procedural wording of how each case was closed. His money came back in the summer of two thousand fifteen, and the ruling in his favor read almost like an apology the government would never say out loud.
[16:10] And this is not ancient history that got quietly fixed. The power that reached into her account is still on the books, and the honest question a story like this leaves you with is who it reaches for next. By two thousand fifteen, the pressure had moved to Congress. [17:00] Lawmakers held hearings on these structuring seizures, and business owners who had lived through them came and testified about what it had done to their companies and their families. The stories landed. It is one thing to read a policy memo; it is another to sit in a hearing room and listen to ordinary people describe having their accounts emptied over deposits that broke no law. And the pressure did not fade when the headlines did. It built. Before the reform, an owner could lose every dollar of working capital and simply wait, sometimes a year or more, while the case ground on. The reform put a clock on the government for the first time.
[18:15] In two thousand nineteen, it became law. A reform act, signed that July, made the change permanent. From then on, the government could no longer take a legal-source account just because the deposits happened to stay under ten thousand dollars, and if it does seize an account, the owner now gets a hearing within thirty days, instead of being left to twist for a year. The act carries the names of business owners who fought their own seizures, people who turned the worst year of their lives into a wall standing between that power and yours. [18:40 L4-close] As for Carole: by the time the law changed, according to her lawyers and the reporting on her case, she had long since sold the restaurant. Her case, the reporting makes clear, had become one of the stories that put this abuse in front of the country in the first place. She did not get her fees back, and she did not get the business back. What she got is harder to put on a balance sheet, the knowledge that what happened to her had not stayed hidden, and that somewhere in the language of a new federal law was a door being shut so it could not happen to the next person the same way.
[18:45 threat-rehook / next-arc open loop] And that is the uneasy part. The reform that grew out of her year of hell protects you from the exact trap she fell into, and from almost nothing else. That same power to seize first and make you prove your innocence later is still reaching for someone's account right now. There is one more case in this series where it did, and that one did what Carole's never could: it moved a courtroom to the edge of saying the practice had gone too far.
But the honest ending matters more than the triumphant one. That reform closed one door; it did not close the hallway. The specific trick that trapped Carole, treating small, legal deposits as a crime, is off the table now. But civil forfeiture itself, the power to put your property on trial instead of you, is still very much alive, in drug cases and highway stops and tax files across the country. The law that took Carole's account was reformed. The idea behind it was not, and somewhere tonight it is reaching for another account, under another name.

**[ED / CTA 19:40]**
So the next time someone tells you the rules exist to protect you, the sharper question is whose rules, and who decides what your pattern means. Carole followed the rule. It still cost her the account, the restaurant, and a year of her life. She got the money back. She never got the year. If the machinery running quietly behind your own bank account is worth twenty honest minutes of your attention, then you already understand why this series exists. There is one more account this same power emptied, and that case is the one that finally moved a courtroom. That is next.

> **ED終端アンカー**: 本文最終VO語=**"That is next."**。§4.8/§9.1のフェードは**この語尾にアンカー**。

---

## §3. ビジュアル / モーション設計(数値予算)

### 3.0 全体モーション予算（**単位を確定・cadence全ペア機械再計算・depth床引上げ・要素≥6を実測へ・図数/hero数整合**）

> **監査反映（animation-BLOCKING#11／MAJOR#12-14／MINOR#15,#16）**。

| 指標 | 本話の確定値 | 対応ゲート |
|---|---|---|
| 総尺 | 1,170–1,230s | `check_runtime_band.py`【実装済】 |
| シーン数 | **38** | scene_count ≥34【要確認: 実ゲート台帳のSOLID列に scene_count 単体は無い→`structure_4part`【実装済】で幕数のみ強制。シーン数34は preflight 目視項目】 |
| カット総数 | **528**（平均2.32s） | cut_count ≥450【要確認: 同上・台帳SOLID列に cut_count 単体無し→preflight/motion_energy 併用で担保】 |
| depth処理カット比率 | **45%（239カット）** | depth ratio【要確認: 台帳SOLID列に depth_ratio 単体無し→`check_image_pan_flow`【要実装】＋preflight で担保。旧「【実装済】」表記は過大→訂正】 |
| **カット毎の暗さ（監査MINOR）** | 各カット輝度床 | **`image_cut_luma`【実装済SOLID】＝カット毎輝度**（全動画median が隠す個別暗カットを捕捉）。subject_luma(ROI)【要実装】は追加補助 |
| 動くFigureBeats | **27図**（§3.6・ヒーロー**8**・幕別新規≥3・新規hero全幕≥1） | `check_figure_cadence`【要実装】 |
| ヒーロー面 | **8面**: BSAOriginFlow(F2)/ThresholdMeter(F3)/FrozenAccount(F5)/PolicyReversalTimeline(F11)/McLellanParallel(F14)/McLellanLedger(F14b)/TIGTA-Dots(F15)/CaroleAfterCard(F20) | hero≥3 |
| **motion_energy単位確定（監査#12）** | **%/幅・秒に統一**。within-shot平均**≥16（=≥16px/s@1920幅≈0.83%/幅・秒）**／p10**≥11（≈0.57%/幅・秒）**／全12s窓**≥8**・**主役ROI/前景プレーン限定測定** | `check_motion_energy`【実装済・ROI版＋単位配線】 |
| **図ROIフロー** | ROI内の**≥30%画素が≥3.5%/幅・秒（≈67px/s）**以上。微振動・微速ken-burns除外 | `check_figure_flow`【要実装】 |
| **depth画像フロー（監査#13 引上げ）** | depth画像ROIの**≥25%画素が≥4.0%/幅・秒（≈77px/s、旧2.5%→4.0%へ引上げ）**。**motion_energy p10（0.57%/幅・秒）を確実に上回る値**。ken-burns単独では未達。**全depth画像カットに構造モーション（前景プレーン実移動/走行光/図オーバレイ）を1つ以上必須** | `check_image_pan_flow`【要実装】 |
| **プレイヘッド系別基準** | 横断走行図は面積平均でなく**可動サブROI局所フロー≥5%/幅・秒＋走査完了時間≤カット尺** | `check_figure_flow --sub-roi`【要実装】 |
| **ROI連続フリーズ** | 任意の図/主役ROIでフロー閾値未満が**連続40f（0.67s）超=FAIL**。全図は主要モーション完了後も別種構造モーションをカット終端まで継続 | `check_freeze_frames`【要実装】 |
| **連続depth画像上限（監査#13 短縮）** | depth画像カットのみ連続**≤12s（旧20s→12s）**、その間に図/実写/キネティック字幕を差込む | `check_image_pan_flow`＋割付検査 |
| **要素密度（監査#14 実測化）** | 各図**レンダ済フレーム上で独立に動く/弁別可能な視覚要素≥6**を**optical-flowクラスタ数＋実描画サブ要素数**で実測（自己申告メタデータは合否源にしない・ヒント止まり） | `check_figure_cadence`副検査（描画後実測）【要実装】 |
| 転換 | ForcefulCut4種のみ（§3.2）・金縦スイープ/周回淡光/lissajous/定位置グロー呼吸/明滅禁止 | — |
| 本編中央値/平均輝度 | §3.3・最終mux後・mean AND median床・subject-ROI別途 | `check_body_luma`＋`check_subject_luma`【後者要実装】 |

**床値キャリブレーション**: figure_flow床≥3.5%/幅・秒はEP32実測（手続き図の実移動トラベル平均~4.1%/幅・秒）で逆証明し、微速ken-burns（near28px÷2.3s≈12px/s≈0.6%/幅・秒）が自動では満たさない水準。**depth画像床4.0%/幅・秒は motion_energy p10（0.57%/幅・秒）を約7倍上回り、239カット(下記分類)が両ゲートを同時充足**（OG-0低速slideshowフィクスチャ=赤で検証）。

**depth処理カットの分類確定（監査MAJOR「236が他節と非整合」是正・サブ計数が総和）**: 「depth処理カット」＝**DepthImageV(dpt-large深度マップ)適用の単独画像カットのみ**と定義。内訳=Act別加重(§3.7)の総和 1+1+46+56+44+45+45+2＝**239**。**これは§3.5の単独画像placement 324 のうち 239（=74%）＝§10.1「image-cut の depth必須カバレッジ≥70%」を満たす同一集合**。**図F1-F21(204カット)はL3 near/mid/far 層パララックス=DepthImageVと別機構でモーション床を充足し、239には非算入**（§3.6のdepth✔列は「層パララックス有り」を指し、DepthImageV適用ではない）。よって「全図depth✔(204)＋image70%(154)＝358」という旧矛盾は解消（図は別機構・非算入）。

### 3.1 レイヤー構成（**装飾ループ撤去＝監査animation-MINOR#16**）

奥→手前: **L0 SceneBed**（レーン別グラデ・§3.3で暗端luma≥58保証・**±3%正弦呼吸は撤去**し**リビール駆動の一方向スロードリフト or 静的**に置換）／**L1 テクスチャ/ライン**（**6-10px/s往復ループは撤去**し**イベント駆動の一方向ドリフト**に置換・残す場合±1%以下の知覚不能水準でコンタクト確認）／**L2 グロー/被写界**（リビール時の1回減衰パルスのみ・呼吸ループ/明滅=禁止）／**L3 主役**（depth near/mid/far 3プレーン）／**L4 lowerthird/キネティック字幕**（translateYマスク・scrim仕様§3.3E）。

**depthパララックス（L3・239カット）**: near24–28px/mid14–18px/far6–8px、Easing.out(cubic)。L3全体scale1.03→1.08。**depth画像カットは加えて前景プレーンの実移動 or 図オーバレイで被覆率床（≥25%画素≥4.0%/幅・秒）を満たす**。DepthImageV／dpt-large流用。WebGL長尺`--concurrency=4`。

### 3.2 ForcefulCut（4種のみ・freeze整合）

| 種別 | 尺 | 用途 | パラメータ | Trail |
|---|---|---|---|---|
| push | 8f | 幕・シーン移動 | 旧画面進行方向100%押出＋新押込・Easing.out(cubic) | λ0.75/8 |
| slide | 7f | 書類→書類 | 横100%・Easing.inOut(quad) | λ0.6 |
| zoompunch | 5f | 統計/見出し/図リビール | scale1.0→1.12→1.0＋縦ブラー | 必須λ0.9/10 |
| whip | 4f | レーン切替 | 横ブラーwipe | 必須λ1.0 |

**freeze整合規定**: 図の主要モーション完了後、(a)別種構造モーション（パララックス継続/プレイヘッド走行/下線帯左→右描画/スローケンバーンズ）をカット終端まで継続、**または**(b)完了から0.67s以内に必ずForcefulCut遷移。ROI連続40f静止を発生させない。「固定/静止一定」表記は§3.6から全撤回。

### 3.3 明るさ・グレード・レーン色（**実full-range換算Y'で暗端≥58・レンジ規約pin・scrim逆伝播・mean床生成側追加**）

> **監査反映（brightness-BLOCKING#17,#18／MAJOR#19,#20／MINOR#21／gaming#36）**。

**(A) 測定ステージ＋レンジ規約pin（監査#20=BLOCKING）**: luma床は**grade+vignette+SceneBed+glow+scrim重畳後の最終レンダ（mux後）mp4フレーム**を測る。**レンジ規約を一意にpin**: `ffmpeg -i out.mp4 -vf "scale=in_range=tv:out_range=full,signalstats" ... の YAVG`（＝limited[16,235]格納Yを full-range[0,255] へ線形変換後に YAVG）。全ゲート（body_luma/subject_luma/figure_luma）同一規約。**OG-0に full=128 mid-gray フレームを入れ、実測YAVGが期待スケール（≈128）に一致することを回帰確認**。

**(B) SceneBed実HEX再指定（監査#20 検算是正・BLOCKING#17）**: v004検算表はレンジ取り違えで過少申告だった。**BT.709 full-range Y'（=0.2126R'+0.7152G'+0.0722B'）を実算し暗端Y'≈58（床52に+6マージン、監査gaming#36の「暗端≥56」要求を満たす）へ全レーン再指定**:

| レーン | 明端HEX（Y'実算） | 暗端HEX（Y'実算） | 検算（実算値） |
|---|---|---|---|
| Iowa(暖) | #3E4A66（**73.5**） | #333B4E（**58.7**） | 暗端≥58 ✔（床52に+6.7） |
| Federal(冷) | #3A4762（**70.2**） | #313A50（**57.7**） | 暗端≈58（拘束床52に+5.7 ✔・目安58には-0.3＝実質達成）。厳密に≥58を要すなら暗端を #323B51（Y'≈58.2）へ微調整 |
| NC(冷緑) | #3C4740（**68.2**） | #343C38（**58.0**） | 暗端≥58 ✔（床52に+6.0） |

面積支配的なSceneBedが暗端でもY'≈58→**vignette不透明≤0.10（周縁×0.92）後も 58.7×0.92=54.0 ≥52**（実算）。図面カット最終median≥52 を達成可能。**「実測確認」表記は全て「目標値（未レンダ）」へ訂正**（監査gaming#36）。実測はmux後mp4でのみ主張（§6.2）。

**(B2) 写真支配フレームの別系統証明（監査brightness-MAJOR#19）**: depth写真カット（239＝45%）はSceneBedが不可視で(B)の証明が転用不可。**別系統でワーストケース算出**: pre-grade median≥54（§10.3）×grade0.98×vignette周縁0.92 = コーナーROI 48.6 ≥48。夜/逆光シーン（夜食堂内観・控訴審冷光・厨房）は §10.3 の**pre-grade mean≥56・dark(<44)率≤25%**（後述(D2)）で生成段FAILさせ、暗転素材を上流で排除。

**(C) grade/vignette逆算**: 合成後mean/median実写≥48・図面≥52を満たすようgain/vignette逆算。確定値=**実写gain0.98/brightness1.00/vignette不透明≤0.10・半径1.5**、**図面vignette不透明≤0.08**。

**(D) check_body_luma正直配線＋mean復活＋dim率（監査#18）**: 実装済`check_body_luma`が現に強制=**median≥48・dark(<YAVG30)率≤22%**【実装済】。派生 **`check_body_luma --mean-floor 48 --figure-median-floor 52 --figure-mean-floor 50 --dark 0.18 --dim-threshold 40 --dim-rate 0.30`**【要配線】=**mean AND median**・dim閾値は**知覚基準 full-range Y<40（監査brightness-MINOR#21・SceneBed床から独立）**。

**(D2) 生成側mean/dim床（監査brightness-BLOCKING#18）**: §10.3の生成目標にmedianだけでなく **pre-grade mean≥56・dark-pixel(<44)率≤25%** を追加。`build_footage_contact_sheet` にmean・dim率の合否列を追加し**生成段で機械FAIL**（mux後の事後waiveを禁止）。

**(E) subject-ROI輝度＋scrim逆伝播（監査brightness-BLOCKING#17／MAJOR#20）**: 新ゲート`check_subject_luma`【要実装】=depth L3 near/midプレーン（店/手元/凍結通帳/図描画マスク）を切出し**ROI内 mean≥48 AND median≥48・暗率≤22%**（逆光/夜も背景明部で稼ぐ禁止）。**scrim を生成側へ逆伝播（監査#17 の核心是正）**:
- 本文字幕scrim=**不透明度≤0.28（旧0.35→引下げ）・下1/3のみ・上端50pxグラデ**。数値グラフィックscrim=**≤0.28**。
- **scrim帯に入る被写体ROIは pre-grade median≥68**（=48÷0.98÷0.72、実算下記）を§10.3に明記し逆算数値を提示。
- **併用規則（監査#17 二択）**: (a)被写体が下1/3に来るカットは字幕を**上段配置に強制**（scrim帯とsubject-ROIの重なりを設計上禁止・§3.4/§5.5）、(b)重なり不可避カットのみ pre-grade≥68 を要求。preflight16枚にscrim込みsubject-ROI輝度数値を併記。

（scrim逆算実算: post = pre×0.98×(1−0.28)=pre×0.706。post≥48 → pre≥**68.0**。旧0.35なら pre≥75.4 が必要だったため、scrim引下げ＋上段配置優先で現実的な pre≥68 に収束。）

| レーン | 幕 | SceneBed(§3.3B) | アクセント | テキスト |
|---|---|---|---|---|
| Iowa | Act1/Act3前半/ED | #3E4A66→#333B4E | アンバー#F4B24A | 暖白#F6EFE2 |
| Federal/Court | Act2/Act5 | #3A4762→#313A50 | スチール#6FA8DC | 冷白#E8EEF6 |
| NC | Act4 | #3C4740→#343C38 | 田舎緑#7FB77E | #EDF2EC |

機能色: 押収=警告赤#E5534B／合法原資=緑#58C08A（TIGTA）／ゴールド#E8C36B=RESPECT最終ノードのみ。

**3話アーク レーン色の定量分離（監査MINOR「背景トーンが寒色navyに密集」是正）**: EP33(tyler)/EP34(rolin) の実HEXと本話を併記し弁別を実証:

| 話 | SceneBed実HEX | 主アクセント | 弁別軸 |
|---|---|---|---|
| EP33 | #101A2E→#3C4D66（青H≈212°） | 警告赤 #E8341C | 深い青・低明度 |
| EP34 | #12303a（ティール寄りnavy H≈194°） | 警告赤 #E4342B＋現金クリーム #E9C46A | ティール＋クリーム |
| **EP35** | Iowa #3E4A66(H≈222°)／Federal #3A4762(H≈223°)／NC #3C4740(H≈120°田舎緑寄り) | **アンバー #F4B24A／スチール #6FA8DC／田舎緑 #7FB77E** | **暖アンバー＋田舎緑でEP33/34の寒色＋赤/クリームと弁別** |

背景navyは3話とも近接し得る（arc_footage_nonoverlap は色を測らない）ため、**弁別はアクセントで担保**: EP35=アンバー/スチール/田舎緑 vs EP34=警告レッド/現金クリーム vs EP33=警告レッド/深青。NCレーン(#3C4740・H≈120°)は3話で唯一の**暖緑寄り**背景でトーン差を明示。必要なら Iowa SceneBed をさらにウォーム（R成分+8）へ寄せEP34寒色と差を拡大。

### 3.4 lowerthird/キネティック字幕（左見切れ対策＋scrim帯回避）
セーフエリア左右96px・上下54px。テキストボックス**x_start≥120px固定**、左スライドイン禁止（動きはY方向のみ）。`overflow:hidden`行マスク＋translateY(+64→0,8f,Easing.out(cubic))。opacity単独禁止。キネティック数字は一語ずつzoompunch・行末幅≤1200px。**被写体が下1/3に来るカットは字幕を上段配置に強制（§3.3E）**。

### 3.5 footage・多様性・3話アーク非重複（**実写0本＝生成静止画基準・distinct=136/324=0.42実算・content-tag dedup・footage_utilization主柱**）

> **監査反映（footage-BLOCKING#4／MAJOR#5,#6,#7,#8／MINOR#9,#10）**。

**distinct定義確定**: `footage_diversity` の distinct = **unique(単独露出画像資産)/total(単独露出placement)**、手続き図F1-F21は分子分母とも除外。**図背景プレートは図の一部＝分子・分母どちらからも除外**。床≥0.40。

> **★BLOCKING是正（監査・設計 vs 実引き継ぎ物の食い違い）★**: 実 `EP35_hinders_ai_prompts.v001.md` は **68プロンプト（S001–S068）＝単独画像62＋背景プレート6・実写クリップ0本（36枚が"実写差替"）**。設計旧値「実写46＋単独画像100＋プレート14」は**架空**で、distinct=0.451は水増しだった。以下、実在物へ全面再計算＋**不足を ai_prompts v002 拡張要件**として固定する。

**(A) 資産会計を実在68枚基準へ再計算＋v002拡張要件（監査#4=BLOCKING）**:

- **実写クリップ=0本**（ai_promptsが実写を全て生成静止画で差替）。よって `footage_diversity`/`footage_utilization` は**生成静止画資産に対して**適用し、「実写素材」という語は本設計から撤回。
- **単独画像 unique を現行62 → v002で≥136へ拡張**（distinct床0.40を+0.02マージンで満たす最小数）。ai_prompts v002 に不足74枚を追記（レーン別配分§10.2を実在化）。

| カット源 | 独立資産(v002確定) | 割当placement | 平均再利用 | 上限 |
|---|---|---|---|---|
| Codex単独画像（静止/depth・実写差替含む） | **136 unique**（現行62→+74拡張要件） | 324 | 2.38 | **≤3（個別max・監査gaming#36）** ✔（136×3=408≥324） |
| 手続き図F1-F21＋背景プレート | 27図＋**6プレート**（実在数・不足図分は v002 で追加） | 204（対象外） | — | 対象外 |
| **計（非図・単独露出）** | **136 unique** | **324** | distinct=**136/324=0.42** | ≥0.40（+0.02） ✔ |

（実在プレートは6枚。§3.6の27図のうちプレート裏面を要する図は6を超えるため、**v002で不足プレートを追記**。distinct=136/324=0.42。数枚QC落ちでも≥0.40を保つよう v002は140枚目標で発注。**0.42は実在物起点の再計算値であり、旧0.451の水増しを撤回**。）

> **過去失敗#4（DL素材が1つも使われない）の構造的リスクをオーナーに明示**: 本話は**実写クリップ0本＝全カットが生成静止画/図/depth**。「本物の実写footageが1本も無い＝紙芝居寄り」という知覚リスクが残る。緩和=(1)`footage_utilization`【実装済SOLID】で136生成資産の各々が最終mp4に≥1回出現を強制、(2)depth/層パララックス/構造モーションで"動く写真"化、(3)[OG-3]でオーナーに「実写0本・生成のみ」を明示承認。実写を一部でも調達する場合は v002 で置換。

**(B) civic B-roll話またぎ除外**: 3話最頻の「制度/報道/公聴会」（輪転機/新聞一面/公聴会証人席）を除外リスト化。EP35は**新聞=NYT一面固有（CLM-0007）に限定**。法廷=**N.D.Iowa専用ロケ**。

**(C) content-tag dedup＋アーク割当確定表（監査footage-MAJOR#7,#9＋BLOCKING「指紋台帳不在」）**: **基盤＝既存SOLID `arc_nonrepeat`【実装済・実データ検証済】（話またぎ素材再利用を検出）**。本話はその上に **sha256＋pHash（ハミング≤6）＋content-tag** 照合を拡張（既存拡張＝二重実装でない・監査MINOR是正）: (1)EP33/34使用クリップ指紋衝突→FAIL、(2)**内容タグの3話横断再使用≤1/アークを機械FAIL**、(3)欠落=**FAIL停止（vacuous除外禁止）**。

> **★BLOCKING是正（監査・指紋台帳が0件）★**: `arc_used_fingerprints.json` はリポジトリに**1件も存在しない**（EP33/34は topic/manifest/approvals のみ・レンダ資産も指紋も未生成）。設計自身の§14.7が「EP33/34未レンダ欠落=FAIL停止」と規定するため、**現状 arc拡張ゲートは必ず停止＝arc_nonrepeat拡張は「検証不能」であり §13 の満点根拠にできない＝仮点**。**[OG-0.5]（着手前ブロッカー）でEP33/34の実レンダ＋指紋台帳(sha+pHash+content-tag列)を実ファイル化**するまで本話を先に進めない。下記割当表は content-tag を全使用タグへ拡張（printing_press/hearing_room/courtroom/gas_pump に加え diner/register/bank/federal_building/newspaper も3話横断で照合）:

| content-tag | EP33 | EP34 | EP35 | EP35の扱い |
|---|---|---|---|---|
| printing_press（輪転機） | — | 使用(1) | **不使用** | 実写捨て→**F10 HeadlineKinetic 図で代替** |
| hearing_room（公聴会室） | — | — | **使用(1)** | EP35専用ロケ可（33/34未消費） |
| courtroom_empty（空法廷） | 使用(1) | — | **不使用** | 実写捨て→**F18 CongressHearingCard/法廷図で代替** |
| gas_pump（給油） | — | — | **使用(1)** | NC専用（EP35固有） |

EP33/34が既消費のタグ（printing_press/courtroom_empty）はEP35で**実写を起用せず手続き図で完全代替**し、制度/報道実写要本数から差引き（§3.5表で10→8へ）。「専用ロケで回避可」の記述は撤回。

**(D) 生成資産の実使用床（監査footage-MAJOR#10・BLOCKING「実写≥34不能」是正）**: **主柱＝既存SOLID `footage_utilization`【実装済・実データ検証済】（DL/生成素材が最終mp4で未使用＝過去失敗#4を検出）**。本話は実写0本のため **`check_rendered_footage_min` の「実写実レンダ≥34」を撤回**し、ゲート定義を**「QC通過・起用確定した生成静止画独立資産≥34 が スパンID→sha突合で最終mp4に各1回以上出現、かつ136 unique の全数が footage_utilization で使用確認」**へ整合。手続き図で全スパンを埋めない（画像スパンは生成画像で埋める）。過去失敗#4再発リスク（実写0）は§3.5A末の通りオーナー明示。

**(E) 生成画像レーン別 要unique数（実写0本・全て生成静止画・監査「44 vs 46 不整合」是正）**: **実写クリップは0本のため「実写要本数」枠は撤廃**。distinct分子=単独画像136 unique を下記レーンへ配分（v002発注表＝§10.2と一致）。「独立資産46/要本数44」の旧二枠の食い違いは**単独画像unique数に一本化**して解消。プレートは図内包（footage対象外・実在6＋v002で図に応じ追加・同一プレート連続露出≤3カット）。

| レーン | 単独画像 unique(v002) | 内容(顔なし) | content-tag(arc照合) |
|---|---|---|---|
| Iowa/店 | 42 | 外観朝光・網戸・鉄板・レジ・現金勘定・空席・FOR SALE/SOLD | diner/register/bank |
| Federal/法廷(EP35専用) | 34 | 連邦地裁・空法廷・被告席・書類束・控訴審冷光・無人判事席 | federal_building/courtroom |
| NC/田舎店 | 24 | 路傍コンビニ・給油ポンプ・冷蔵ケース・農村ハイウェイ | gas_pump/roadside |
| 制度/報道 | 36 | 70年代組織犯罪資金・NYT一面固有・公聴会室(EP35専用) | newspaper/hearing_room |
| **計** | **136 unique** | 汎用象徴=gavel≤1・天秤/女神/hourglass=0 | distinct=136/324=0.42 ✔ |

（実写0本。全て生成静止画で136 unique を確保し distinct 0.42。EP33/34既消費タグ（printing_press/courtroom_empty）は本話で**起用せず手続き図F10/F18で代替**し content-tag 3話横断再使用≤1を維持。[OG-3]で実QC通過枚数を数値提示。）

### 3.6 FigureBeats一覧（**27図・ヒーロー8・cadence全隣接ペア≤90s機械再計算・「固定」全撤回・要素≥6は描画後実測**・★=ヒーロー）

> **監査反映（animation-BLOCKING#11・MINOR#15）**: v004はAct1(F2→F3=105s)/Act2(F5→F6=95s)/Act4(F14b→F15=95s)の違反を見逃していた。**F2b/F5b/F14c を新設し全ペアを機械再計算**。図数・hero数の内部不整合（22 vs 24／6 vs 8）を **27図・hero8** で全箇所整合。

| # | 図ID | 幕 | リビール(目安) | 持続モーション（flow床充足・freeze整合） | hero | depth |
|---|---|---|---|---|---|---|
| F1 | Register38Years | Act1 0:35 | 数字ホイール減速回転＋near札/far厨房パララックス（終端までドリフト） | | ✔ |
| F2 | **BSAOriginFlow** | Act1 1:20 | 流体連続流下＋細枝が小店へ滴下トラベル | ★ | ✔ |
| **F2b** | **StructuringExplainer(新設・cadence#11)** | Act1 2:10 | 入金列を$10k線下で反復→「小さく保つ＝罪」ラベル充填走行 | | ✔ |
| F3 | **ThresholdMeter** | Act1 3:05 | 入金ブロック継続積上げ＋完了後ゲージ微光走行 | ★ | ✔ |
| F4 | ThresholdBreach | Act1 4:00 | 亀裂が線沿い継続伝播＋0.5s以内push遷移 | | ✔ |
| F5 | **FrozenAccount** | Act2 4:25 | 氷亀裂継続伝播＋near通帳パララックス | ★ | ✔ |
| **F5b** | **BurdenShiftScale(新設・cadence#11)** | Act2 5:15 | 証明責任の天秤が政府側→市民側へ実回転＋"PROVE IT INNOCENT"充填 | | ✔ |
| F6 | CaseCaptionNameplate | Act2 6:00 | 訴訟名一語ずつzoompunch＋空被告席midパララックス連続ドリー | | ✔ |
| F7 | WalkAwayTally | Act2 7:10 | 「歩き去る所有者」列が逐次グレーアウト走行（retention instance可視化） | | ✔ |
| F8 | CivilForfeitureInvert | Act2 7:20 | バー継続回転＋下線帯左→右描画継続 | | ✔ |
| F9 | CoinFlip | Act2 8:05 | 着地後ぐらつき→平落ち→0.5s以内whip遷移 | | ✔ |
| F10 | HeadlineKinetic | Act3 8:35 | NYT一面見出し一語ずつzoompunch＋紙面奥へ連続後退トラベル | | ✔ |
| F11 | **PolicyReversalTimeline** | Act3 9:30→12:40→18:15 | **可動サブROI=プレイヘッド常時右滑走（局所flow≥5%/幅・秒）＋"WITHOUT PREJUDICE"常時ノードをAct4通し表示（監査retention-MINOR）** | ★ | ✔ |
| F12 | SeizureVsReturn | Act3 10:20 | 両側slide-in中央衝突→両束が実押込±10px継続 | | ✔ |
| F13 | DismissedStamp | Act3 11:30 | 二語zoompunch着弾→下線帯左→右描画トラベル継続 | | ✔ |
| F14 | **McLellanParallel** | Act4 12:20 | 左Iowa/右NC横開き＋両景パララックス＋F11遠景赤マーカー右進行 | ★ | ✔ |
| F14b | **McLellanLedger** | Act4 12:55 | 301入金逐次点灯＋累計~$2Mカウントアップ走行＋年ラベル横スクロール（サブROI基準） | ★ | ✔ |
| **F14c** | **McLellanStore(新設・cadence#11)** | Act4 13:45 | 田舎店内奥→手前ドリー＋レジ小額連続点灯（「小さな取引の店」可視化） | | ✔ |
| F15 | **TIGTA-Dots** | Act4 14:30 | 278ドット組成→91%が緑へ波状逐次反転トラベル→完了後スローパララックス | ★ | ✔ |
| F15b | LegalSourceBars | Act4 15:05 | 231件$17.1M横棒実伸長→到達後カウンタ微走行＋0.5s以内push | | ✔ |
| F16 | FeeDeniedCard | Act5 15:55 | 宙吊りカード着地→半緑/半グレー境界線左→右描画継続 | | ✔ |
| F17 | ThreatReframeCard | Act5 16:10 | "STILL ON THE BOOKS"パネル＋二人称脅威＋背景制度スパイン奥スロードリフト | | ✔ |
| F17b | FeeContrastCard | Act5 17:20 | McLellan"FEES PAID"／Carole"FEES DENIED"対比二段＋両段充填バー左→右伸長（L5視覚回収） | | ✔ |
| F18 | CongressHearingCard | Act5 17:40 | 公聴会室・証人席・無人シルエット（逐語引用出さない）＋書類実捲れトラベル継続 | | ✔ |
| F19 | RESPECTActNode | Act5 18:15 | Timeline最終ノード金点灯＋スパイン全体を左→右に一度確定走査トラベル（サブROI）・金グロー=1回減衰パルスのみ | | ✔ |
| F20 | **CaroleAfterCard** | Act5 18:50 | 空Mrs.Lady's店内→"SOLD"札（L4回収）＋店内奥→手前ドリートラベル継続 | ★ | ✔ |
| F21 | InfoDensitySpine(ED橋) | ED 19:40 | プレイヘッド走査トラベル→end-card | | ✔ |

**図数=27（ヒーロー8）**。§3.0/§13/§11 全箇所で 27図・hero8 に整合（監査#15）。
**幕別新規図**: Act1=5(F1,F2,F2b,F3,F4)／Act2=6(F5,F5b,F6,F7,F8,F9)／Act3=4(F10-F13)／Act4=5(F14,F14b,F14c,F15,F15b)／Act5=6(F16,F17,F17b,F18,F19,F20)＝全幕≥3 ✔。
**新規hero幕別**: Act1=F2,F3／Act2=F5／Act3=F11／Act4=F14,F14b,F15／Act5=F20＝全幕≥1 ✔。
**全隣接ペア リビール間隔（機械再計算・監査#11）**: 0:35→1:20=45／1:20→2:10=50／2:10→3:05=55／3:05→4:00=55／4:00→4:25=25／4:25→5:15=50／5:15→6:00=45／6:00→7:10=70／7:10→7:20=10／7:20→8:05=45／8:05→8:35=30／8:35→9:30=55／9:30→10:20=50／10:20→11:30=70／11:30→12:20=50／12:20→12:55=35／12:55→13:45=50／13:45→14:30=45／14:30→15:05=35／15:05→15:55=50／15:55→16:10=15／16:10→17:20=70／17:20→17:40=20／17:40→18:15=35／18:15→18:50=35／18:50→19:40=50。**全ペア≤90s ✔**（v004のAct1/2/4違反をF2b/F5b/F14c新設で解消）。`check_figure_cadence`【要実装】が幕別新規≥3・hero≥1・間隔≤90s・**各図要素≥6（描画後実測）** を強制。設計書の✔は手計算でなく**ツール実出力を貼る**（§12手順7）。

**図の実装決定論（監査MAJOR「27図が部品/データ/座標未定＝決定論再現不可」是正）**: 各図は**新規実装せず MOTIONKIT CATALOG.md の既存部品/プリセットへ写像**（二重実装禁止・CLAUDE invariant14）。**hero8図は独立運動要素≥6を実体列挙＋部品ID＋data-driven props＋座標/値/easing/移動量まで数値化**（残19図も同形式で図別シートに展開・Codexは列挙要素をそのまま実装）:

| hero図 | MOTIONKIT部品/プリセット | 独立運動要素≥6（実体・座標/値） | 主要フレーム/easing/移動量 |
|---|---|---|---|
| F2 BSAOriginFlow | `FluidStreamFlow`＋`BranchDripV` | ①主流下降(x960,y0→1080) ②分岐枝(x760/1160) ③滴下トラベル(→小店ROI x1500,y820) ④店輪郭パルス ⑤背景プレート far ドリフト(6px) ⑥流量ゲージ微光走行 | 0–48f 流下 Easing.out(cubic)・滴下 λ0.9 Trail・far 8px/s |
| F3 ThresholdMeter | `StackMeterV`＋`GaugeSweep` | ①入金ブロック積上げ(10列) ②$10k線パルス ③ゲージ針(0→95%) ④完了後ゲージ微光走行 ⑤near札パララックス24px ⑥far厨房6px | 積上げ 0–60f stagger6f・針 Easing.inOut(quad)・微光 5%/幅秒 |
| F5 FrozenAccount | `IceCrackPropagate`＋`DepthPlanes` | ①氷亀裂線沿い伝播 ②near通帳24px ③mid手元16px ④far店6px ⑤凍結色被り遷移 ⑥終端push | 亀裂 0–40f λ0.75 Trail・push 8f |
| F11 PolicyReversalTimeline | `PlayheadTrackV`＋`NodeLatch` | ①プレイヘッド右滑走(サブROI局所flow≥5%/幅秒) ②ノード点灯×3 ③"WITHOUT PREJUDICE"常時ノード ④スパイン奥ドリフト ⑤マーカー右進行 ⑥年ラベル横スクロール | 走査 完了≤カット尺・zoompunch λ0.9/10 |
| F14 McLellanParallel | `SplitCompareV`＋`DepthPlanes` | ①左Iowa/右NC横開き ②左景パララックス ③右景パララックス ④中央境界線描画 ⑤F11遠景赤マーカー右進行 ⑥両見出しzoompunch | 横開き 0–24f Easing.out(cubic)・マーカー等速禁止spring |
| F14b McLellanLedger | `LedgerCountUp`＋`ScrollAxisV` | ①301入金逐次点灯 ②累計~$2Mカウントアップ ③年ラベル横スクロール(サブROI) ④行ハイライト走行 ⑤near伝票16px ⑥合計バー伸長 | 点灯 stagger4f・カウント 0–90f・スクロール局所5%/幅秒 |
| F15 TIGTA-Dots | `DotMatrixReveal`＋`WaveFlip` | ①278ドット組成 ②91%緑へ波状反転トラベル ③残9%赤保持 ④完了後スローパララックス ⑤カウンタ278→231走行 ⑥$17.1M帯伸長 | 組成 0–40f・波反転 40–90f stagger2f・パララックス 4%/幅秒 |
| F20 CaroleAfterCard | `RoomDollyV`＋`SignLatch` | ①空店内奥→手前ドリー ②"SOLD"札着地 ③near椅子24px ④mid窓16px ⑤far通り6px ⑥埃/光条スロードリフト | ドリー 0–72f Easing.out(cubic)・札 λ0.75 Trail |

MOTIONKITに完全一致部品が無い図は**最寄りプリセット＋data props差分**で構成し、新規フルスクラッチを避ける（CATALOG.md参照を§12手順7の前提に追加）。

### 3.7 幕ごと割付（**連続depth画像≤12s**）

> 境界は§2.2正典から導出（監査MAJOR是正）。depthカット=DepthImageV適用の単独画像カット（§3.0分類・図の層パララックスは非算入）で、Act別加重の総和=239。

| 区間 | 目安秒 | 境界 | シーン | カット | depth% | 割付図 | レーン |
|---|---|---|---|---|---|---|---|
| HOOK | 7 | 0:00–0:07 | 1 | 4 | 25% | 伝票→凍結 | Iowa |
| OP | 12 | 0:07–0:19 | 1 | 4 | 25% | bookend | Iowa |
| Act1 | 241 | 0:19–4:20 | 6 | 100 | 46% | F1-F4,F2b | Iowa |
| Act2 | 254 | 4:20–8:34 | 7 | 116 | 48% | F5,F5b,F6,F7,F8,F9 | Federal |
| Act3 | 183 | 8:34–11:37 | 6 | 88 | 50% | F10-F13 | Iowa→Federal |
| Act4 | 209 | 11:37–15:06 | 7 | 100 | 45% | F14,F14b,F14c,F15,F15b | NC |
| Act5 | 279 | 15:06–19:45 | 9 | 106 | 42% | F16-F20 | Federal→Iowa |
| ED | 39 | 19:45–20:24 | 1 | 10 | 20% | F21 | Iowa |
| **計** | **~1,225s** | 20:24 | **38** | **528** | **45%(239)** | 27図 | 3レーン分離 |

（Act2割付図は F5,F5b,F6,F7,F8,F9 の6図＝§3.6幕別新規Act2=6と一致。旧「F5-F9,F5b,F7」はF7重複表記だった＝監査MINOR是正。）全windowに構造モーション/実移動を敷設。**depth画像カットのみ連続≤12s**。平坦20秒ゼロの主柱＝**`check_padding`【実装済SOLID】**＋`check_motion_energy`【実装済】、補助＝`check_image_pan_flow`／`check_freeze_frames`／`check_novelty_beat`／`check_info_beat`【要実装】。黒画面ゼロ（`footage_utilization`【実装済】＋rendered_footage_min）。

---

## §4. 音設計(Sound Design・4層)

### 4.0 原則・パレット
**Kurzgesagt/Veritasium型**。**恒久禁止**: fillerSFX・whoosh連発・終盤ジェット様轟き・持続広帯域roar・ED roar系ライザー・逆再生スウッシュ・278離散tickのブザー化・**gavel（本話に木槌イベント無し・監査sound#23）**。48kHz/24bit、最終AAC320k。

### 4.1 4層と基準（-14 LUFS integrated ±0.5 / TP≤-1.0dBTP）

| 層 | 内容 | VO区間 | VOなし | タグ |
|---|---|---|---|---|
| L1 VO | ElevenLabs同一声・同速 | 基準 | — | narration |
| L2 music | パッド/ピアノ/制度パルス | -23〜-20(VO下-7〜-9) | -16〜-15 | score |
| L3 ambience | 幕ごと別ベッド | -30〜-27 | -24 | roomtone |
| L4 SFX | 意味タグ付き | ヒット-12〜-8/持続≤2.0s・-18床 | -8 | event |

各Actに L2/L3/L4実素材最低1本ずつ束縛。真無音≤**0.8s**（Hook直後尾のみ≤0.6s例外）。VOレス総≤**75s**・単一VOギャップ≤**6s**。

### 4.2 L1 VO処理（話またぎ固定・字幕整列の逐語源）
HPF80→De-esser(6.5k,-4)→EQ(200-1.5/3.2k+1.5/10k+1)→Comp(3:1,8ms,120ms,GR-4)→VO単体-16 LUFS。**この分離VOステム(vo_master)が §5.0 字幕onset検出の唯一の入力**（監査captions#1）。

### 4.3 L2 劇伴（7cue・**調性/楽器/モチーフ数値化＝監査sound-MINOR**・MUS-05改名）
各cueに**調・テンポ・主要楽器・反復動機・和声変化点**を明記（Kurzgesagt水準の作編曲を引用倒れにしない）。アーク共通の回想モチーフ（第3章締めとして第1-2章と関連付く3-4音動機）を1つ定義。62–72BPM。継ぎ目クロスフェード800ms。VOで-7ダック。各cueステムsha256を`arc_used_fingerprints.json`に記録しEP33/34衝突除外。

| cue | 調/テンポ | 楽器 | 動機/和声 |
|---|---|---|---|
| MUS-01 warm_home | D dorian/64 | ピアノ＋温チェロ | 回想動機提示・和声変化~2/分 |
| MUS-02 institution_pulse | A minor/68 | 低弦パルス＋シンセベル | 単一持続ペダル・変化~1/分 |
| MUS-03 cold_seizure | C phrygian/62 | 低弦＋金属パッド | 半音下降動機 |
| MUS-04 press_momentum | E minor/72 | ピアノ刻み＋弦 | 上昇分散・変化~3/分 |
| MUS-05 **data_reveal**（旧data_verdict改名・監査sound#23） | A minor/66 | ベル＋パッド | 統計提示・**gavelへ上昇させない**(§4.8) |
| MUS-06 resolution | D major/64 | ピアノ＋弦 | 回想動機の長調解決 |
| MUS-07 endcard_bed | D major/一定 | 温パッド（旋律なし） | ED固定・§4.8 |

### 4.4 L3 章別アンビ（**distinct=5・素材長≥Act尺・低域予算**）
同一ベッドを2幕にまたがせない。各**Act尺以上**の非ループ・ランダムスタート。`check_bed_loop`【要実装】。AMB-01 diner(≥245s)／AMB-02 federal_cold(≥260s・120Hzハム)／AMB-03 press_hall(≥205s)／AMB-04 roadside(≥225s)／AMB-05 courtroom_still(≥245s)／AMB-06 endcard_warm(AMB-01由来=distinct非計上)。**distinct=5**。全ベッドHPF≥40Hz・summed<120Hzエネルギーを-24 LUFS帯にキャップ・低域モノ化。

### 4.5 L4 SFX（**21種・gavel削除・意味タグ1:1・sfx_density床新設・rendered_sfx_min・≤3反復/幕**）

> **監査反映（sound-MAJOR#23,#24,#25／MINOR#26,#27・gaming#34）**。

**gavel削除（監査sound#23）**: 本話は刑事訴追ゼロ・木槌イベント無し。`gavel_sharp`を**削除**。2016控訴審 fee-denial（§2.6 15:40・判決グラフィック有）にのみ中立な **`low_ruling_stamp`（低打点・木槌連想なし）** を使用。Act4統計リビールの句読点は`data_assembly_swell`単独に統一。

**SFX事象密度床（新設・監査sound-MAJOR#25）**: `check_sfx_density`【要実装】=**各Actで distinct SFX事象≥6 かつ 可聴SFX事象レート≥1本/25s**。非食堂Act（Act2/Act5）に制度系テクスチャSFX（書類/印章/空調ハム点/椅子/歩行）を追加し**17→21種**へ。生活音の反復キャップは**同一ワンショットの機械コピー≤3**に限定（バリエーション素材register_key A/B/Cは別distinct扱い＝薄さの機械許容を排除）。

**同族percussive分離（監査sound-MINOR#27）**: スタンプ系を音色分離（中心周波数帯・アタック時定数を付す）。同族間隔≥8s。

主要21種（各SFXに**対応画面事物ID**を rendered_sfx_min署名に明記・空欄/汎用連想=FAIL）: `pen_scratch`(-14/伝票) `low_impact_stamp`(-8/紙印) `diner_pour`(-20/店) `griddle_spatula`(-18/鉄板) `register_key`(-14/レジ・A/B/C変種) `pipe_drip`(-18) `threshold_tick`(-16/$10k停止) `threshold_breach_hit`(-10/F4破断・打撃でなくクラック) `ice_crack_freeze`(-12/F5) `paper_drop_stamp`(-13/落下＋軽打) `coin_spin_settle`(-14/F9) `deposit_slip_circle`(-17) `press_stamp`(-14〜-16/金属輪転・<120Hzカット・≤2.0s・旧press_roar廃止) `headline_punch`(-11/短打＋残響・tick床から除外・監査sound#26) `ice_thaw_return`(-16/実録滴下＋着地・逆再生禁止・≤1.2s) `data_assembly_swell`(統計/単一スウェル＋≤6tickアルペジオ) `low_ruling_stamp`(-9/2016判決のみ・gavel置換) ＋制度系4種 `doc_shuffle`(-16/書類) `hvac_hum_point`(-20/空調) `chair_creak`(-18/公聴会) `footstep_hall`(-19/廊下)。`tension_note`は画面事物非紐付け→L2/L3へ移動しSFX distinctから除外。

**rendered_sfx_min（監査sound-MAJOR#24）**: `check_rendered_sfx_min`【要実装】=**≥12 distinct SFXの各々が最終音声タイムラインに1回以上出現（event-map→mux突合）＋標準SFX同一反復≤3回/幕を機械強制＋各SFXの対応画面事物IDが署名に存在（空欄/汎用連想=FAIL）**。folderに置くだけの「薄い音で緑」を封じる。

### 4.6 ミックス（低域予算=steady buildup検出）
VOサイドチェーンL2-7/L3-4/L4持続-3dB。Actハードカット4点断面設計。ミックスバスTP-1.5dB・リミッタceiling-1.0dBTP・モノ互換±3dB。**per-Act<120Hz RMS ceiling=各Act中央値+4dB超区間ゼロ（監査sound#24数値化）**。

### 4.7 幕タイムライン（Act2/Act5にSFXレーン実配置＝監査sound#25）
HOOK: pen_scratch→low_impact_stamp尾0.6s無音。Act1: 生活音→pipe_drip→threshold_tick($10k停止)→threshold_breach_hit→準無音。**Act2（非食堂）**: ice_crack_freeze→無音0.5s→doc_shuffle(6:10)→chair_creak(6:40)→coin_spin_settle(8:05)→hvac_hum_point点在（distinct≥6/≥1本25s床充足）。Act3: press_stamp律動＋headline_punch→ice_thaw_return→低ドローン(上昇させない)。Act4: AMB-04総入替→data_assembly_swell(14:30)。**Act5（制度）**: low_ruling_stamp(15:40・1回)→doc_shuffle/footstep_hall(17:00公聴会)→18:15 spine_lock＋MUS-06 payoff→18:50温room回帰。

### 4.8 ED固定ベッド＋全編roar/tonal riser検出（**閾値数値確定＝監査sound#24／ED VOダック＝監査sound-MINOR**）
AMB-06＋MUS-07（旋律なし温パッド）。**ED VO区間（103語・§2.2実算に統一）はMUS-07を-23〜-21へダック（監査sound-MINOR・§4.6サイドチェーン適用）、最終VO語"That is next."語尾以降のみ-18へ戻す2段**。上昇ライザー・咆哮・逆再生なし。ED終端は**"That is next."語尾から0.6s以内に1.8sリニアフェード→-inf→0.3s完全無音でファイル終端**。

> **WEAK ゲートの正直表記（gate reality）**: `check_ending_sound`／`verify_sfx_manifest`／`verify_script_structure` は**機能はするが深い偽装耐性が限界**＝「完全自動保証」として引用しない。EDの音終端・SFX実在は **`roar_anomaly`(要実装)＋`preflight_owner_review.py`【実装済】の人間試聴backstop（音5本＝roar/ED"That is next."語尾/低域ceiling/ED VO対劇伴S/N）** で担保する。

**`check_roar_anomaly`【要実装】本話確定閾値（監査sound#24）**: 3秒窓走査で**(a)低域<160Hz短期RMS単調上昇≥3dB かつ <300Hzエネルギー比≥0.6（tonal riser）／(b)広帯域flatness上昇／(c)短期LUFS crescendo≥3dB** のいずれかでFAIL＋逆再生スウッシュ（上昇エンベロープ＋プリエコー）検出。**OG-0にtonalドローンriser試験クリップで発火検証**。

### 4.9 ラウドネス2-pass
Pass1測定→Pass2 linear=true I=-14/TP=-1.0/LRA=11。12s窓短期LUFS-16〜-12帯・VO谷≥-18。

### 4.10 mux刻印＋DSPゲート閾値（監査sound#24 全数値確定）
out_master.wav sha256を`audio_mix_sha256`【実装済】刻印・再レンダ後照合。**要実装DSPゲート確定閾値**: `check_bed_loop`=20-90sラグの正規化自己相関ピーク**≤0.35**／`check_cluster_buzz`=自己相関第一ピーク/平均比**≥3.0** または狭帯域ピーク対平均**≥8dB**をブザー判定（flatness上限は廃止＝周期tick buzzを捕捉）／`check_low_band_ceiling`=per-Act <120Hz短期RMSが**Act中央値+4dB**超区間ゼロ／`check_roar_anomaly`=§4.8。各数値はEP31/32実測 or 合成フィクスチャで逆証明（OG-0）。記録: audio_mix_sha256/integrated_lufs/true_peak/distinct_sfx(21)/distinct_bed(5)/music_cue(7)/ending_bed_id/ambience_bed_sha[]・music_cue_sha[]/rendered_sfx_usage_map。

---

## §5. 字幕・画面内テキスト(機構)

### 5.0 逐語源一本化＋**VOステムonset固定＋.ass=.srt機械生成＋windowed narration_index（監査captions#1,#2,#3）**
S1 台本[VO:]→`narration_index.txt`／S2 ElevenLabs**chunk単位TTS**→`vo_master.wav`（分離VOステム・VO単体-16LUFS）＋各chunk窓確定／**S2.5 `06_audio/narration_index.v001.json`生成**=各chunk窓付き＝`verify_caption_sync`のdrift-free地上真実源（whole-fileフォールバック=停止）／S3 **narration_index拘束forced alignment（WhisperX align/wav2vec2）**→`words.json`／**S3.5 照合＋独立anchor検証**（下記）／S4 §5.2分割→captions.srt→**captions.ass（.srtから機械生成・\fadのみ付与・event-start不変）**／S5 ゲート群。

**onset検出入力の固定（監査captions-MAJOR#1）**: `verify_caption_sync`のonset検出は**最終muxでなく分離VOステム(vo_master)に固定**（MUS/SFX/アンビのアタックがVO語頭より先に立つ偽値を排除）。**「VOステムのサンプル位置==最終mux内VOのサンプル位置（muxで遅延/リサンプルを入れない）」を1本のゲートで突合**。OG-0に「VO語頭直前に大音量SFXを置いたクリップ」で偽green不発を検証。

**測る成果物=映る成果物（監査captions-MAJOR#2）**: sync/行長測定は**mp4へ焼き込む字幕=.assに対して実施**。`.ass`は`.srt`から機械生成し**全cueで .ass event-start==.srt cue-start、行数/文字数一致を突合するゲート**を追加（.ass生成バグでの出荷ずれを排除）。

### 5.1 タイミング規律（**実装状態を実査して確定・独立検証器・行長ゲート新設**）
> **監査反映（captions-MAJOR#3,#4,#1／MINOR#5・gaming「自己一致」）**。

**現行実装の実査結果（監査captions#3の矛盾解消・正直確定）**: `verify_caption_sync` の**現hard配線 = p50≤0.10・p90≤0.35・per-min≤0.50・機能語行末0・matched≥60%**。**exact帯≥75%・late%・区間ドリフトは現状 report-only（非強制）**＝§IMPLEMENTED記述の「hard配線済」は**楽観的過大表記**であり、本書では**exact/late/driftを【要実装hard化】と正直表記**（EP31 exact84%は稼働“計測”確認であって hard-FAIL配線ではない）。この不一致を OG-0 で hard化して解消。

**自己一致の排除（監査gaming「near-tautological」）**: **整列に使う検出器（wav2vec2 forced alignment）と、ラグを測る検出器（独立エネルギーonset）を別系統**にする。srt-startを測定検出器出力に一致させる自己一致を禁止。**matched床は≥60%据置**（誤FAIL回避の正規化差問題を実データで切り分け後、目標≥85%へ戻す方針を§14に明記）。ナレ一致は別ゲート`caption_narration_match`【実装済100%】が担う。

| 項目 | 【実装済】現hard | 【要実装】v2（OG-0でhard化・物理前提） |
|---|---|---|
| p50 | ≤0.10s | ≤0.08s |
| p90 | ≤0.35s | ≤0.22s |
| per-min中央 | ≤0.50s | §5.3 20ビン5条件へ差替 |
| 機能語行末 | =0 | 据置＋**every追加** |
| matched(独立faster-whisper) | ≥60% | 根本原因是正後≥85%目標 |
| exact帯\|lag\|≤0.15s | **report-only（非強制）** | **≥75%（目標82%）hard FAIL化** |
| late率>0.12s | **report-only** | **≤12% hard FAIL化** |

**行長ゲート新設（監査captions-MAJOR#1・v004致命穴）**: `check_caption_lines.py`【要実装・OG前必須】=入力captions.ass、**各cue 語数≤8・文字数≤44・行数≤2・cps≤27をhard FAIL＋cue間overlap=0・隣接最小ギャップ規定（監査captions#6）**。**未配線でexact/late/ドリフト/行長を「hardゲート値」と称さない**。最小/最大表示0.80s/5.0s・リード目標-0.06s±0.10s（.srtのstart＝可読onset・0.60sフェードは.assの\fadで視覚pre-rollのみ・.srt startは動かさない）。

**数値/固有名詞アンカー検証の完全定義（監査captions-MAJOR#5）**: `verify_alignment_anchors`【要実装】=各アンカー（$32,820.56/$107,702.66/301/$2M/91%/278/NYT/RESPECT）に (a)期待語 (b)**独立onset源（VOステムのエネルギー or 音素モデル・forced alignmentと別系統）** (c)許容**|anchor_lag|≤0.12s** (d)FAIL挙動 (e)OG-0フィクスチャ（数値早口で境界スミアを起こしたクリップで発火）を明記。forced alignmentの自己充足（均等割りスミア）で緑にしない。

### 5.2 行分割規則＋綴り語金額cue分割表（**高速列挙のチラつき規則＝監査captions#6**）
上限（check_caption_lines強制）: ≤8語・≤44字・≤2行・≤27cps。分割優先: 文末＞句読点前＞等位接続詞前＞前置詞前＞関係詞前。機能語行末禁止(a/an/the・to/of/on/in/for/under/with/at/into/from/by・and/but/or/so/that/which・is/was/would/could/must/had・no/every)。

**綴り語金額アンカーcue分割（"and"を行頭・境界を verify_alignment_anchors と一致）**:

| 元文 | cue分割（各≤8語/≤44字） |
|---|---|
| Thirty-two thousand, eight hundred twenty dollars and fifty-six cents | `Thirty-two thousand,`／`eight hundred twenty dollars`／`and fifty-six cents.` |
| one hundred seven thousand, seven hundred two dollars and sixty-six cents | `one hundred seven thousand,`／`seven hundred two dollars`／`and sixty-six cents.` |
| Three hundred one deposits / around two million dollars | `Three hundred one deposits.`／`Around two million dollars`／`in honest sales.` |

**高速列挙チラつき規則（監査captions#6）**: 連鎖cueでは**リードを0にクランプ（前cue終端=次cue開始）・cue重なり禁止・実発話<0.80s時は隣接cueへ食い込ませず必要なら44字内で1cueに統合**。`check_caption_lines`にcue間overlap=0・隣接ギャップを機械FAILとして追加。OG-0で高速金額列挙のチラつきを検証。

### 5.3 20分区間ドリフト検査（**OG-0のhard物理前提へ昇格＝監査captions#4**）
runtimeを1分=20ビン。pass条件（全て・OG-0でhard）: ①全ビン|lag|≤0.15s ②傾き≤0.010s/分 ③後半10−前半10≤0.08s ④15:00–20:24各ビン≤0.12s ⑤単調増加連続ビン≤3、3連続悪化で累積+0.06s超は前半でもFAIL。**OG-0フィクスチャ=「後半へ単調に遅延累積する合成トラック（前半0s→終盤0.45s）」で per-min≤0.50は緑だがドリフトゲートが赤になることを実証してから本レンダ**（監査captions#4）。落ちたら拘束アライン＋数値アンカーで再整列（同一ASR戻しループを断つ）。尺削りで通す禁止。

### 5.4 ナレ逐語一致QC＋全chunk字幕化
`caption_narration_match`【実装済hard】=全語列正規化しnarration_indexと完全一致(100%)・順序一致。**テキスト一致はタイミング非保証**→§5.0照合＋`verify_alignment_anchors`で時刻desync別検出。

**「字幕が飛ぶ（未字幕chunk）」の専用バックストップ＝既存SOLID `caption_coverage`【実装済・実データ検証済】（監査MAJOR是正）**: 全ナレchunkが**各々≥1つのタイミング付き字幕cueとして描画**されることを機械強制。**caption_narration_match（語列連結一致）は chunk がマージ/スキップされても連結語が合えば緑になり得るため、chunk単位のカバレッジ保証は caption_coverage が担う**（語一致とは別ゲート）。より厳密な windowed narration_index（§5.0・要実装）はその上乗せ。人手最終=`preflight_owner_review.py`【実装済】でAct2金額/Act3 NYT/Act4 91%・301・$2M/Act5 fee対比の5か所目視・試聴。

### 5.5 主要画面内テキスト（別レイヤー・locked桁一致・scrim組込・数値統一）
章タイトル/数値/タイムラインは別レイヤー。数値は**§1.2統一**（278/91%/231件$17.1M/$107,702.66/301/~$2M）。引用: **NYT見出しのみ画面直接引用可**。Hinders引用/NYT paraphrase/公聴会証言逐語(F18)は**画面直接引用不可・間接話法のみ**。固有法令番号は**ナレ非読み上げ・画面のみ**（ナレは「一九八六年の法律」等）。**scrim(§3.3E ≤0.28)込みで全画面テキストtitle-safe（左右96/上下54）・lower-third左端x≥120px**。

---

## §6. 品質ゲート(Done=実物確認・**実装済/要実装＋OG-0独立回帰フィクスチャ**)

**hard緑＋実物目視/試聴＋オーナー確認**の三点で初めて「完成」。

> **v005核心（監査gaming#34, animation#16）**: 要実装ゲート（DSP系含む）は**§12 OG-0で「既知の紙芝居/薄い音/暗い/desync/ブザー/tonal riser/低コントラストサムネ=赤、既知良品=緑」の独立held-out回帰フィクスチャ通過を物理的完了条件**。**フィクスチャは実装者と別に用意した独立held-outセットにし、各DSPゲートが既知不良を実際に赤にすることを第三者（別セッション/別モデル）が確認**（甘いゲート＋それに通る甘いフィクスチャの両方緑を排除）。DSP系（figure_flow/image_pan_flow/roar_anomaly/subject_luma/cluster_buzz/caption drift）は**入力信号・アルゴリズム・閾値校正データを本書に明示**。§13は**フィクスチャ緑を満点の明示条件**とし、未通過は仮点（減点）集計。

### 6.1 hardゲート一覧（全緑必須・実装状態明示）

| ゲート | 実装状態 | 本話閾値 |
|---|---|---|
| runtime_band | 【実装済】 | 1,170–1,230s（唯一のオーナー承認偏差） |
| **script_wordfloor（新設）** | 【要実装・OG-1】 | 実wc≥2,925（本話3,195）＋3点wpm推定 |
| caption_sync基本 | 【実装済】 | p50≤0.10・p90≤0.35・per-min≤0.50・機能語行末0・matched≥60% |
| **caption_sync v2** | 【要実装・OG-0 hard】 | exact≥75%・late≤12%・p50≤0.08・p90≤0.22・§5.3ドリフト5条件 |
| **caption_lines（監査#1）** | 【要実装・OG前】 | 語≤8・字≤44・行≤2・cps≤27・cue間overlap=0 |
| **alignment_anchors（監査#5）** | 【要実装】 | 独立onset源・\|anchor_lag\|≤0.12s・OG-0スミア発火 |
| **VOステムonset固定＋mux突合（監査#1）** | 【要実装】 | VOステム==mux VO位置・偽green不発 |
| **narration_index.v001 windowed（監査#3）** | 【要実装】 | reliability=='windowed'確認・wholefileフォールバック=停止 |
| **.ass=.srt突合（監査#2）** | 【要実装】 | event-start一致・行数/字数一致 |
| caption_narration_match | 【実装済hard】 | 語一致100%・順序一致 |
| **caption_coverage（監査MAJOR・字幕飛び）** | 【実装済SOLID】 | 全ナレchunkが≥1タイミング付きcueとして描画（未字幕chunk=FAIL） |
| body_luma(大域) | 【実装済】 | 最終mux後median≥48・dark≤22% |
| **image_cut_luma（監査MINOR・カット毎暗さ）** | 【実装済SOLID】 | カット毎輝度床（全動画medianが隠す個別暗カットを捕捉） |
| **body_luma派生（監査#18）** | 【要配線】 | mean AND median・図面52/50・dim(<40)率≤30% |
| **subject_luma＋scrim逆伝播（監査#17,#20）** | 【要実装】 | 主役ROI mean/median≥48・scrim込み・pre-grade≥68紐付け |
| **生成側mean/dim床（監査#18）** | 【要配線】 | pre-grade mean≥56・dark(<44)≤25% |
| **luma range pin（監査#20）** | 【要配線】 | scale=in_range=tv:out_range=full後YAVG・mid-gray128回帰 |
| motion_energy(既存SOLID) | 【実装済SOLID】 | **within-shot≥12・p10≥9（台帳配線済の実値）** |
| motion_energy(ROI版・%/幅秒) | 【要配線・OG-0】 | within-shot≥16・p10≥11（ROI/%幅秒換算は未配線＝満点根拠にしない） |
| **figure_flow（監査#11）** | 【要実装】 | ROI≥30%画素≥3.5%/幅・秒・sub-roi≥5% |
| **image_pan_flow（監査#12,#13）** | 【要実装】 | depth≥25%画素≥4.0%/幅・秒・連続depth≤12s |
| **freeze_frames** | 【要実装】 | ROI連続40f超=FAIL |
| **figure_cadence＋要素≥6実測（監査#11,#14）** | 【要実装】 | 幕別新規≥3・hero≥1・間隔≤90s・描画後独立運動要素≥6 |
| **novelty_beat（格下げ）** | 【要実装】 | 視覚変化床≤12s（退屈防止の十分条件でない） |
| **info_beat（再定義・監査#35）** | 【要実装】 | 意味単位（新固有名詞/数字/因果/視点/スリル）本編≤22s・Act5後半/ED≤40s |
| scene/cut count | 【要確認】 | 台帳SOLID列に単体ゲート無し→`structure_4part`【実装済】＋preflight目視で担保（scene38/cut528は設計値） |
| depth ratio | 【要実装/preflight】 | 台帳SOLID列に単体ゲート無し→`image_pan_flow`【要実装】＋preflightで担保（45%/239は設計値・旧【実装済】表記は過大→訂正） |
| sound_layers | 【実装済hard】 | 4層・各Act L2/L3/L4・真無音≤0.8s |
| sound distinct | 【実装済】 | SFX≥12(21)・beds≥4(5)・music≥1(7) |
| **sfx_density（新設・監査#25）** | 【要実装】 | 各Act distinct SFX事象≥6・≥1本/25s |
| **rendered_sfx_min＋≤3反復＋画面ID（監査#24）** | 【要実装】 | 各≥12 SFX最終mp4出現・反復≤3/幕・画面事物ID署名 |
| **bed_loop（監査#24）** | 【要実装】 | 自己相関ピーク≤0.35 |
| **cluster_buzz（周期性・監査#23,#24）** | 【要実装】 | 第一ピーク/平均≥3.0 or 狭帯域≥8dB |
| **low_band_ceiling（監査#24,#27）** | 【要実装】 | per-Act<120Hz RMS≤Act中央値+4dB |
| loudness 2-pass | 【実装済】 | I=-14±0.5・TP≤-1.0・VO谷≥-18 |
| **roar_anomaly（全編・tonal・監査#24）** | 【要実装】 | 3秒窓 低域上昇≥3dB&<300Hz比≥0.6 OR flatness OR crescendo=FAIL＋逆再生 |
| audio_mix_sha256 | 【実装済】 | mux直前ミックスと刻印一致 |
| footage_diversity | 【実装済hard】 | distinct≥0.40（本話136/324=0.42実算）・再利用≤4・画像個別≤3 |
| **footage_utilization（監査MAJOR・DL/生成素材未使用）** | 【実装済SOLID】 | 136生成unique資産の各々が最終mp4に≥1回出現（未使用=FAIL・過去失敗#4主柱） |
| **画像個別再利用≤3（監査#gaming36）** | 【要配線】 | 個別max≤3（平均でなく）・同一sha4回=赤 |
| **arc_nonrepeat＋pHash/内容タグ拡張（監査#7,#8・BLOCKING指紋不在）** | 基盤【実装済SOLID】＋拡張【要実装】 | EP33/34指紋衝突/同一内容タグ=FAIL・上流タグ実在検証・**指紋台帳不在の現状は検証不能=[OG-0.5]で実ファイル化するまで仮点** |
| **rendered_footage_min（監査#6,#10・実写0本是正）** | 【要実装】 | **生成静止画独立≥34**が最終mp4出現（旧「実写≥34」撤回）・footage_utilizationと整合 |
| freshness | 【実装済hard】 | sha≠前回＋mtime新 |
| structure_4part / op_ed_bookends | 【実装済hard】 | 4-5幕・OP≤12s・PD bookends |
| **check_padding（監査MAJOR・20分水増し主柱）** | 【実装済SOLID】 | 20分水増し/沈黙尾/言い換え反復を実データ検出（水増し防御の主柱） |
| **script_lint（監査MAJOR・AI臭主柱）** | 【実装済SOLID】 | AI臭/カデンツ検出（Here is/命令/三段/アナフォラの合否源・手計算✔撤回） |
| **script_binge（補助・傘ループ除外・監査#33）** | 【要実装・補助】 | 再フック信号≥8・短中期open-loop referent解決・ギャップ≤2:00・開ループ0区間≤90s（script_lint/check_paddingの上乗せ） |
| thumbnail_visibility | 【実装済】 | フレーム平均Y≥33 |
| **thumbnail_saturation（新設・監査#35）** | 【要実装】 | 画面≥20%画素が彩度S≥0.5（地味さ検出・Y≥33を鮮やかさに流用しない） |
| **thumbnail_text_contrast（監査#36,#38）** | 【要実装・OG前】 | テキストROIコントラスト≥4.5・320px字高≥30px・$0/$32,820個別ROI実測 |
| image_resolution | 【実装済hard】 | 全画像≥3840px |
| preflight_render_gate | 【実装済】 | レンダ前健全性 |

**要実装ゲート計（OG前配線＋OG-0独立held-out回帰フィクスチャ必須）**: script_wordfloor / caption_sync v2 / caption_lines / alignment_anchors / VOステム突合 / narration_index.v001 windowed / .ass突合 / body_luma派生 / subject_luma / 生成側mean/dim / luma range pin / motion_energy配線 / figure_flow / image_pan_flow / freeze_frames / figure_cadence / novelty_beat / info_beat / sfx_density / rendered_sfx_min / bed_loop / cluster_buzz / low_band_ceiling / roar_anomaly / 画像個別再利用 / arc_footage_nonoverlap / rendered_footage_min / script_binge / thumbnail_saturation / thumbnail_text_contrast。**未配線・フィクスチャ未通過での「完成」宣言禁止**。

### 6.2 制作前owner-review（実装済・完成前提・**最暗＋最小動きワースト自動抽出**）
`preflight_owner_review.py`【実装済】実行後のみ完成:
- 16枚コンタクト（最終mux後）＋**最暗ワースト12枚＋最小動き12カット自動抽出（監査animation#13）**を強制表示
- 字幕ラグ&ドリフト20ビン＋数値/固有名詞アンカー＋reliability=='windowed'確認＋.ass=.srt突合
- 章境界4点＋終盤の音5本（roar_anomaly全編・ED"That is next."アンカー・低域ceiling・**ED VO対劇伴S/N**）
- 輝度（body_luma大域mean/median/図面52/subject-ROI/scrim込み・**pre-grade mean/dim合否**）
- サムネ3案320px縮小＋**彩度床実測＋テキストROIコントラスト（$0/$32,820個別）＋赤占有率＋320pxフィード並置（地味さ目視）**
- **台本本文§2.6＋3レビューdiff§2.5＋script_binge/script_wordfloor実出力＋独立モデルbinge署名**
- arc_footage_nonoverlap照合（sha+pHash+内容タグ＋上流EP33/34タグ実在提示）

自己申告禁止・緑≠完成。

---

## §7. レンダ規律
### 7.1 Composition / remotion.config.ts
1920×1080/fps=60/durationInFrames=実TTS同期/id=Ep35Hinders。`npm i @remotion/motion-blur`＋DepthImageV。png/concurrency最大（WebGL長尺`--concurrency=4`）/libx264/CRF16/yuv420p/bt709/aac320k/GPU=angle。**CPU(libx264)・NVENC切替禁止**。
### 7.2 実務規律
tailで隠さない・完走まで殺さない・1本ずつ直列。再レンダ後audio_mix_sha256照合＋freshness。順: **要実装ゲート配線＋OG-0独立フィクスチャ→**VO→字幕拘束アライン→図/depth→音2-pass→mux→preflight。**輝度は最終mux後mp4で測定（range pin適用）**。SSD(H:)/runs/コミットしない。

---

## §8. 尺の予算(1,170–1,230s)
### 8.1 予算表（目安秒158wpm・確定は実TTS・語数はwc実算）

> 秒予算は§2.2の正典境界（158wpm）から導出。累積終端＝1,225s（20:24）で§2.2境界と一致（監査MAJOR「境界と秒予算の二重定義」是正）。

| 区間 | 目安秒(158wpm) | 語数(実算) | 累積 |
|---|---|---|---|
| HOOK | 7 | 19 | 7 |
| OP | 12(非VO) | 0 | 19 |
| Act1 | 241 | 635 | 260 |
| Act2 | 254 | 668 | 514 |
| Act3 | 183 | 483 | 697 |
| Act4 | 209 | 551 | 906 |
| Act5 | 279 | 736 | 1,185 |
| ED | 39 | 103 | 1,224 |
| **計** | **~1,225s(158wpm)** | **3,195語(実算)** | band 1,170–1,230s内（上限まで5s） |

### 8.2 ship-gateと超過処理＋水増し検出の実体化（監査gaming#28,#34,#35, retention#4）
- 唯一のship-gate=`check_runtime_band.py`実TTS実測。
- 1,230s超（150wpm時1,290s想定）トリム順: ①Act5「公聴会」段落の30日ルール解説の冗長部 → ②ED末尾。**感情ペイオフ・フック・オープンループ回収・Carole POV(L4)・18:45再フックは削らない**。
- 1,170s未満（165wpm時1,174s想定・10s）: Act1人間ディテール or Act4 McLellan文脈を中身で追加（水増し厳禁）。
- **水増し検出（主柱＝既存SOLID・監査MAJOR是正）**: **`check_padding`【実装済SOLID】が主柱**＝20分水増し/沈黙尾/言い換え反復を実データで検出（この用途専用に検証済で配線済のゲートを引用＝未実装ゲートで「機械保証」と称した過大表記を撤回）。補助＝`check_motion_energy`【実装済】(視覚凍結のみ・限定明記)／`check_novelty_beat`【要実装・補助】(視覚変化床≤12s・十分条件でない)／`check_info_beat`【要実装・補助・意味単位再定義・監査#35】(本編≤22s・Act5後半/ED≤40s)／`script_binge`開ループ0区間≤90s(傘ループ除外)。info_beat/novelty_beat/script_binge は **OG-0独立フィクスチャ通過まで「補助」表記**。**5:00–11:00帯（中だるみ危険帯・監査retention#4）は per-window 結果を個別報告**（whole-runtime集計でなく）。

---

## §9. OP / ED・サムネ
### 9.1 OP / ED（PD bookends hard）
- **OP(0:07–0:19)**: 食堂ネオン点灯→連邦紋章にじみ→Title 3モーションビート。ロゴ静止禁止（motion窓≥8）。
- **ED(19:45–20:24・103語)**: PD bookend close＝暗い食堂ネオンが暖かく灯り直しend-card（連続グロー・F21走査）。ED固定ベッド（§4.8・VOダック2段）=roar禁止・"That is next."語尾から1.8sフェード。earned CTA（RESPECT射程限定「一つの扉を閉じた・民事没収一般はまだそこにある」→次回オープンループ→"That is next."）。過大な安心を与えない。

### 9.2 サムネ（**彩度床新設・一次候補を案Bへ再評価・320px実測添付・数字主役・$0コントラスト床・IRS印撤去**）
> **監査反映（thumbnail-BLOCKING#35／MAJOR#36,#37,#38／MINOR#39）**。

基準1280×720・**320px実縮小モックで実測（自己申告禁止）**。実在肖像禁止。全案床: 平均Y≥33【実装済】／**彩度床=画面≥20%画素が彩度S≥0.5【要実装 thumbnail_saturation】（地味さ検出・監査#35）**／**テキストROIコントラスト≥4.5・320px字高≥30px【要実装 thumbnail_text_contrast】**／全テキスト端64px内禁止／二人称／赤占有率≥8%。

| 案 | 概要 | 主コピー | 数字 | 平均Y | 彩度 | gap |
|---|---|---|---|---|---|---|
| **B（一次・監査#35で再評価）** | 太い**警告レッド**基準線＋線下に積む入金＋線上に×。高彩度・単純・即読 | `STAYED UNDER THE LIMIT.`＋`SO WHY IS IT GONE?` | `$10,000`ライン | 52 | S≥0.5が赤帯で≥22% | ○即成立 |
| A（対抗・テキスト2ゾーンへ削減） | 官僚グレー背景＋**赤塗り**の$32,820（白でなく警告レッド＝彩度確保・監査#35）＋通帳残高欄を**空欄/斜線で暗示**（$0.00文字依存を排除・監査#36,#37） | `YOU BROKE NO LAW.` | **$32,820**(赤・画面高の1/3=240px厳守・監査#36) | 46 | 赤数字で≥20% | ○ |
| C（保険・二人称化＋IRS印撤去・監査#39） | 匿名の**官製封筒/汎用スタンプ**（IRS実在記章は描かない）が通帳を掴む | `THEY CAN EMPTY YOURS.` | `$0 LEFT?` | 44 | 差込色で確保 | ○ |

**案A矛盾の実寸是正（監査thumbnail-MAJOR#36）**: 主コピー`YOU BROKE NO LAW.`は**4語**。$32,820は**画面高の1/3=720の1/3=240px厳守**（v004の「字高392px」と「1/3」の矛盾を撤回し240pxに統一）→320px縮小で60px≥30px床✔。主コピー字高は1280px原寸120px→320px縮小30px≥床✔。テキストゾーンを**2つ以内**（$32,820＋二人称1行）に削減し、残高は文字でなくビジュアル状態（空欄/斜線）で暗示（合成推論の認知負荷を排除・監査#36,#37）。

**彩度床の機械検出（監査thumbnail-BLOCKING#35）**: `thumbnail_saturation`【要実装】=画面≥20%画素が彩度S≥0.5。**Y≥33を鮮やかさ根拠に流用しない**。3案の実測彩度を§9.2に添付。EP33青レーン（H≈210°）との非重複=案A/Bの有彩色は警告レッド（H≈4°）中心で206°差。

**320px実測添付（監査#36,#38）**: `thumbnail_text_contrast`をOG-0（低コントラスト灰-on-灰=赤/高=緑）込みで先行実装し、**3案全テキストROIの実コントラスト値＋320px字高＋案Aの$32,820個別ROI実測を§9.2に貼ってからサムネ承認**（未実装ゲートを合格根拠に引用しない）。

**選定（監査#35で再評価）**: **一次=案B**（最も高彩度・警告レッド基準線・gap即読「限度未満なのに、なぜ消えた?」）。案Aは赤塗り数字化＋テキスト2ゾーン＋$0ビジュアル暗示に修正のうえ対抗。**A/B運用**: (a)YouTube Test & Compare自動勝者採用に一本化＋(b)CTRスクレイパー各≥1,000imp後参照。全変更owner-gate・差替72h/24hの2回まで。preflightに320pxフィード3案並置＋彩度/コントラスト実測＋地味さ目視をオーナー確認項目に追加。
**タイトル**: `Can the IRS Empty Your Bank Account for Following the Bank's Own Rule?`

---

## §10. Codex画像(生成計画)
**画像はCodex生成（SDXL勝手起動禁止）。それ以外は全部Claude。**
### 10.1 必要枚数
- **本話 単独画像 unique≥136（footage_diversity対象・counted・v002拡張要件＝現行62から+74）＋図背景プレート≥6（図内包・uncounted）**（監査BLOCKING=実引き継ぎ68枚基準へ再計算・distinct136/324=0.42達成）。**実写クリップ0本（全て生成静止画・過去失敗#4リスクをオーナー明示）**。**EP32据置40枚は禁止**。
- シーン38の全image-spanに1枚以上＋余剰。**`footage_utilization`【実装済SOLID】で136生成unique各々が最終mp4≥1回出現を強制**＋`check_rendered_footage_min`（生成静止画独立≥34・旧「実写≥34」撤回）。**画像個別再利用≤3・depth必須カバレッジ=単独画像image-cutの≥70%（239/324=74%・§3.0分類）**。
- 全4K(3840×2160)・匿名/実在肖像なし・画面内テキスト無・レーン色準拠。
- **命名注記（監査「シーン38 vs S001-S068 矛盾」是正）**: ai_prompts の `S0NN` は**画像プロンプトID（1プロンプト=1画像）**であってシーンID(§4 scenes の S001 等)ではない。**画像資産は38シーンに複数枚割当**（38シーン ≠ 画像枚数）。命名衝突を避けるため生成物ファイル名は `PD-2026-035-S0NN-IMG-0NN.png`（プロンプト由来）で固定し、シーン割当は別途 scene_plan で管理。

### 10.2 レーン別配分（`asset_selection`に要枚数/在庫/不足0）

> v002 発注表（§3.5E と一致）。実写0本＝全て生成静止画。unique≥136。

| レーン | 単独画像 unique(v002) | 内容 |
|---|---|---|
| Iowa/店 | 42 | レンガ小店・厨房・レジ・空席・FOR SALE/SOLD窓・朝光通り(顔なし) |
| Federal/法廷 | 34 | 連邦地裁・空法廷・被告席・書類束・控訴審冷光・無人判事席・公聴会室(EP33/34と別ロケ) |
| NC/田舎店 | 24 | 路傍コンビニ・給油ポンプ・冷蔵ケース・農村ハイウェイ |
| 制度/報道 | 36 | 70年代組織犯罪資金・新聞組版・NYT一面・公聴会 |
| 図背景プレート(uncounted) | ≥6(実在)＋不足図分を v002 追記 | 各図の裏面専用(footage対象外・同一連続露出≤3・pre-grade median≥58) |
| **計** | **136 counted + プレート(uncounted)** | 実写0本・distinct136/324=0.42・現行62→v002で+74拡張 |

### 10.3 明るさ床（**生成側 median＋mean＋dim・scrim帯逆算＝監査brightness#17,#18**）
pre-grade目標=**生成静止画median≥54／図面背景median≥58／pre-grade mean≥56／dark(<44)率≤25%**（実写0本＝全カット生成）。**scrim帯（下1/3字幕重なり）に入る被写体ROIは pre-grade median≥68**（=48÷0.98÷0.72）。夜/逆光もキーライト面=主役ROI median≥48。生成後`build_footage_contact_sheet.py`（mean/dim合否列付き）／preflight16枚（最終mux後・range pin）で目視QC。
### 10.4 Codex引き継ぎ
本§10＋§3.6（frame/easing/flow床≥3.5%/幅・秒の構造モーション）＋§5.5（画面内テキストはRemotion側）＋レーン色＋pre-grade輝度目標（median/mean/dim/scrim帯≥68）を渡す。フレーム時刻はnarration_index相対で渡し実TTS後words.json onsetで解決。

---

## §11. 失敗モード → 止める機構(表・全過去失敗+20分水増し禁止・実装状態明示)

| # | 過去失敗 | 名前のある機構(実装状態) |
|---|---|---|
| 1 | 字幕≠ナレ/遅い | §5.0逐語一本化＋caption_narration_match【済】＋verify_caption_sync【済】＋**VOステムonset固定**【要実装】＋windowed narration_index【要実装】＋独立検証器 |
| 1b | **字幕が飛ぶ(未字幕chunk)** | §5.4 **caption_coverage【実装済SOLID】=全ナレchunk≥1cue描画**（語連結一致では chunk skip を見逃す）＋windowed narration_index【要実装】上乗せ |
| 2 | 字幕が変な所で切れる | §5.2分割＋機能語行末0(every追加)【済】＋**check_caption_lines(語≤8/字≤44/行≤2/cps≤27/overlap=0)**【要実装】＋高速金額チラつき規則 |
| 3 | 8:45以降ドリフト | §5.3 20ビン5条件v2＋windowed地上真実【要実装・OG-0 hard昇格】＋**単調累積フィクスチャ** |
| 4 | DL素材が使われない | §3.5D **footage_utilization【実装済SOLID】=136生成unique各々が最終mp4≥1回出現（主柱）**＋rendered_footage_min(生成静止画≥34)【要実装・上乗せ】。**実写0本の構造リスクは§3.5Aでオーナー明示** |
| 5 | 構成ズレ | structure_4part＋op_ed_bookends【済】＋**script_binge測定可能信号(傘ループ除外)**【要実装】 |
| 6 | OP/EDが違う | §9.1 PD bookends【済】＋§4.8 ED固定ベッド(VOダック2段)＋"That is next."終端アンカー |
| 7 | 紙芝居(図少ない) | §3.6 27図＋figure_cadence(全ペア≤90s機械再計算/要素≥6描画後実測)【要実装】＋freeze_frames＋figure_flow＋**image_pan_flow(4.0%/幅秒・連続depth≤12s)**【要実装】 |
| 8 | 周回淡い光うざい | §3.1 **L0正弦呼吸/L1往復ループ撤去**・周回/lissajous/グロー呼吸/明滅全禁止・「固定」表記全撤回 |
| 9 | lowerthird左見切れ | §3.4/§5.5 始点x≥120固定・左スライドイン禁止 |
| 10 | 疎な図(2点地図) | §3.6 各図**要素≥6を描画後独立運動要素で実測**(自己申告メタデータ非合否源・監査#14) |
| 11 | 図背景/画面が暗い | §3.3 **実full-range換算で暗端Y'≈58＋range pin＋mean AND median＋dim(<40)率＋scrim逆伝播(pre-grade≥68)＋生成側mean/dim床**・**image_cut_luma【実装済SOLID】=カット毎暗さ主柱**＋body_luma(大域)【済+配線】＋subject_luma(ROI)【要実装・上乗せ】 |
| 12 | 無意味フィラーSFX | §4.5 全SFX意味タグ・画面事物ID署名・filler除外【済+要実装rendered_sfx_min】 |
| 13 | SFX種類少ない/違和感 | §4.5 21種＋**gavel削除・tension_note除外・sfx_density床・rendered_sfx_min＋≤3反復・同族間隔≥8s**【要実装】 |
| 14 | 終盤の飛行機みたいな変な音 | §4.5 press_roar廃止→press_stamp＋§4.8 **roar_anomaly全編＋tonal riser(≥3dB&<300Hz比≥0.6)＋逆再生検出**【要実装】 |
| 15 | 天秤等汎用素材再利用 | §3.5 汎用象徴≤2(gavel≤1)・再利用≤4・画像個別≤3【済+要配線】 |
| 16 | 棚ラベル破損 | §3.5E 内容ベース選別＋build_footage_contact_sheet【済】＋在庫ステータス化 |
| 17 | サムネ地味 | §9.2 **彩度床thumbnail_saturation新設・一次を案Bへ再評価・赤塗り数字・320px実測**・Y≥33【済】＋thumbnail_text_contrast【要実装】 |
| 18 | AI臭い | §2 独立3レビュー(1本別モデル)＋**script_lint【実装済SOLID】=AI臭/カデンツ合否源(Here is≤2/It is worth≤1/whole story≤1/命令≤2=Deposit/Strip改稿後Picture/Remember/三段≤1/アナフォラ率・実出力貼付・手計算✔撤回)**＋script_binge補助＋700マイル/grandmother/taco/職員告発を本文実削除 |
| 19 | SDXL勝手起動 | §10 画像Codexのみ |
| 20 | 緑≠完成 | §6.2 機械緑＋実物＋オーナーGO＋**要実装ゲートOG-0独立held-outフィクスチャ第三者確認** |
| 21 | 偽の緑(古い良品) | §4.10/§7.2 audio_mix_sha256＋再レンダ後照合＋freshness【済】 |
| 22 | 薄い音で緑 | §4.1/§4.5 各Act L2/L3/L4＋**sfx_density≥6/Act・≥1本25s＋rendered_sfx_min**＋VO谷≥-18＋bed_loop【要実装】 |
| 23 | 尺外れ | §8 check_runtime_band実TTS【済】＋**script_wordfloor(wc実算3,195)**【要実装】 |
| 24 | ゲート最適化(グッドハート) | §6/§8 **要実装を実装済と偽らない・自明値床廃止・novelty格下げ＋info_beat意味単位＋script_binge傘ループ除外・独立held-outフィクスチャ・尺削り字幕禁止** |
| 25 | 話またぎ被り | §3.5C **arc_nonrepeat【実装済SOLID】基盤＋pHash/内容タグ拡張(アーク割当確定表・上流タグ実在検証・欠落FAIL停止)**【要実装】。**EP33/34指紋台帳が0件＝現状検証不能=[OG-0.5]で実ファイル化するまで仮点** |
| 26 | 20分を水増しで稼ぐ | §8.2 **check_padding【実装済SOLID】=水増し/沈黙尾/言い換え反復の主柱**＋info_beat(意味単位≤22s)/script_binge開ループ≤90s(傘除外)【要実装・補助】＋中身充填(3,195語実書) |
| 27 | 開ループ0の中だるみ | §2.4 短中期ループ連鎖＋**L5(fee対比)後半牽引**＋script_binge【要実装】＋5:00-11:00 per-window報告 |
| 28 | 主人公を後半で放棄 | §2.4 L4＋§3.6 F20 CaroleAfterCard＋Act5 Carole POV |
| 29 | 微振動で凍ってないだけ | §3.0 figure_flow≥3.5%/幅・秒＋被覆率30%・微速ken-burns除外・depth床4.0%へ引上げ【要実装】 |
| 30 | Act5尻すぼみ | §2.4/§2.6 15:40脅威再フック＋17:00公聴会前倒し＋**18:45次回オープンループ新設**＋RESPECT射程限定 |
| 31 | フェイク結末の退出許可 | §2.6 「You would think that is where it ends.」のみ・roll credits/music swell撤去 |
| 32 | front-load露出/back-load新奇(中だるみ) | §2.3/§2.6 McLellan/TIGTA を Act2 で伏線開通＋Act1圧縮で押収~4:05 |

---

## §12. 実行順序(決定論 + オーナーゲート・**OG-0独立フィクスチャ**)

0. **[OG-0] 要実装ゲート配線＋独立held-out回帰フィクスチャ（物理的前提）**: §6.1要実装群を実装・単体テスト。**フィクスチャは実装者と別に用意した独立held-outセット（別セッション/別モデルが「既知の紙芝居/薄い音/暗い/desync/ブザー/tonal riser/低彩度サムネ/単調累積字幕遅延=赤、既知良品=緑」を確認）**。DSP系（figure_flow/image_pan_flow/roar_anomaly/subject_luma/cluster_buzz/caption drift）は入力信号・アルゴリズム・閾値校正データ確定。**未配線・フィクスチャ未通過のゲートに依存する完成宣言を禁止**。
0.5. **[OG-0.5・BLOCKING] 上流アーク指紋台帳の実在化（監査BLOCKING）**: EP33/34 を実レンダし `arc_used_fingerprints.json`(sha+pHash+**content-tag列**)を**実ファイルとして生成**、開いてオーナー提示。**現状0件のため未生成なら本話をここで停止**（arc_nonrepeat拡張は検証不能=仮点のまま先へ進めない）。
1. **FACTS確定＋CLM台帳実生成（監査BLOCKING）**: §1.3 recheck **14項目**を一次確認（特にIRSメモ日 vs NYT一面順序・McLellan押収日 vs 方針・10か月レンジ）。**`schemas/claim-ledger.schema.json`準拠のCLM-0001〜0020を `01_research/` に実ファイル化**（各 source_id/一次URL/grade/quote/key_numbers/timeline）。確認不可はヘッジ維持。**台帳未生成なら §13軸1は仮点**。
2. **台本ロック**: §2.6全文(実算3,195・3レビュー済・1本別モデル)を`narration_index.txt`化。**`check_script_lint`【実装済】＋`check_padding`【実装済】緑**＋`check_script_wordfloor`緑（実出力貼付・手計算撤回）。各ビートを実CLM IDへ桁一致突合。**[OG-1] 台本本文§2.6＋3レビューdiff§2.5＋script_lint/padding/wordfloor実出力＋独立モデル署名＋CLM台帳をオーナー提示・承認**。
3. **VO生成**: ElevenLabs同一声・同速→chunk単位で`vo_master.wav`（分離VOステム）＋`narration_index.v001.json`(窓付き)。`check_runtime_band`実測。**[OG-2] runtime_band緑**。
4. **字幕整列**: narration拘束forced alignment→照合→独立onset`verify_alignment_anchors`→§5.2分割→captions.srt→.ass機械生成。caption_narration_match＋caption_sync v2＋caption_lines＋§5.3ドリフト＋windowed確認＋.ass=.srt突合＋VOステムonset固定。
5. **arc非重複プレフライト**: `check_arc_footage_nonoverlap`(sha+pHash+内容タグ・割当確定表・欠落FAIL停止)。**Federal専用ロケ実写事前調達可否**。**[OG]** footage候補承認。
6. **Codex画像（v002拡張）**: ai_prompts を**v002へ拡張＝単独画像 unique 62→≥136（＋不足プレート）**し4K生成(pre-grade median/mean/dim/scrim帯≥68)→build_footage_contact_sheet目視QC。**[OG-3] コンタクト＋輝度＋各レーン実QC通過枚数＋実写0本(生成のみ)の明示＋distinct0.42実測を承認**。
7. **図/depth**: §3.6の27図＋depth239カット(--concurrency=4)。figure_flow/image_pan_flow/freeze_frames/figure_cadence(実出力貼付)/novelty_beat/info_beat自己検査。
8. **音ミックス**: §4の4層(VO/7cue/5bed/21SFX)→2-pass I=-14→roar_anomaly全編/bed_loop/cluster_buzz/low_band_ceiling/sfx_density/rendered_sfx_min→audio_mix_sha256。
9. **mux**: CRF16/libx264/1本直列・audio_mix_sha256刻印。**輝度最終mux後mp4測定(range pin)**。rendered_footage_min突合。
10. **サムネ**: §9.2 3案4K＋320px縮小コンタクト＋thumbnail_saturation＋thumbnail_text_contrast＋$0/$32,820個別ROI＋赤占有率実測。
11. **preflight_owner_review.py**: §6.2全項目(最暗12＋最小動き12自動抽出含む)を数値+画像提示。
12. **§6全hard緑確認＋実物目視/試聴**。**[OG-4] 完成オーナー承認**(緑≠完成)。
13. **公開**: サムネ=案B・Test&Compare登録。予約はオーナーGO待ち。

git: 各ステップcommit+push(SSD/runs除外)。

---

## §13. honest スコアカード(10軸 × 満点根拠・**実装済/仕様済＋OG-0独立フィクスチャ条件・水増しゼロ**)

各10点は §6 の**実装済(【済】) OR 仕様済(【仕】=script名・入力・閾値・FAIL確定＋OG-0独立held-out回帰フィクスチャ緑を物理前提)**で裏付ける。**未実装を実装済と偽った軸・自明値床・裏付け無し軸を10点にしない**。DSP系軸(3/4/5/6/9)は**OG-0独立フィクスチャ緑を満点の明示条件**とし、未通過は仮点として集計・実現100を主張しない（監査gaming#34）。

| 軸 | 点 | 満点根拠(機構名＋実装状態) |
|---|---|---|
| 1. 事実精度 | **仮点(CLM台帳実生成まで満点不可)** | §1全断定CLM＋一次出典＋grade。fee対比/McLellan/TIGTA を CLM-0011/0012/0013/0014(grade-A・McLellan費用は裁判所命令一次記録へ立脚)に明示紐付け。数値§1.2統一。700マイル/grandmother/taco/職員告発を本文実削除。**IRSメモ日 vs NYT一面/McLellan押収日 vs 方針の因果を本文で是正・recheck14項目**。**★CLM台帳が未生成のため桁一致照合が未成立＝[OG-1]で台帳実ファイル化まで満点主張不可＝仮点** |
| 2. 台本(binge/3回) | 10(OG条件) | §2.6 **全文wc3,195同梱**＋§2.5 3レビューdiff(1本別モデル署名)＋`check_script_binge`/`check_script_wordfloor`【仕】(AI臭実カウント貼付=Here is1/命令2/It is worth0/三段1)＋OG-1ルーブリック。再フックは実出力貼付・傘ループ除外・オープンループ短中期3＋L5・front-load是正・Act2 instance分断・18:45再フック。**自己申告排除・自己矛盾撤回** |
| 3. モーション/紙芝居根絶 | 10(OG条件) | §3.6 27図(hero8・幕別新規≥3・**要素≥6を hero8図で実体列挙＋MOTIONKIT部品ID/座標/easing数値化**・描画後実測)・**motion_energy 既存SOLID(≥12/p10≥9)は実装済**／ROI版(≥16/≥11・%幅秒)は要配線・figure_flow(≥3.5%/幅秒)【仕】・image_pan_flow(depth4.0%/連続≤12s)【仕】・freeze_frames【仕】・figure_cadence(**全ペア≤90s機械再計算・F2b/F5b/F14c新設**)【仕】。**床値EP32逆証明・OG-0低速slideshow=赤フィクスチャ前提** |
| 4. 音設計(4層) | 10(OG条件) | §4 distinct SFX21・bed5・cue7・2-pass I=-14【済】・audio_mix_sha256【済】＋**gavel削除・sfx_density・rendered_sfx_min＋≤3反復・画面ID署名**【仕】・roar_anomaly全編(≥3dB&<300Hz比≥0.6)・cluster_buzz(第一ピーク/平均≥3.0)・bed_loop(≤0.35)・low_band(中央値+4dB)【仕・全数値確定】・cue調性/楽器/動機明記・ED VOダック2段。**OG-0 tonal riser=赤フィクスチャ前提** |
| 5. 字幕機構 | 10(OG条件) | §5 逐語一本化＋caption_narration_match【済】＋verify_caption_sync基本【済】＋**VOステムonset固定・.ass=.srt突合・windowed narration_index・alignment_anchors(独立onset・\|lag\|≤0.12s)・caption_lines(行長・overlap=0)・v2(exact≥75/late≤12/ドリフト5条件)**【仕・現行実装状態を実査して正直表記】。**自己一致排除・matched据置(根本是正後85目標)**。OG-0単調累積フィクスチャ前提 |
| 6. 品質ゲート(Done) | 10(OG条件) | §6全hard列挙＋実装状態明示＋preflight_owner_review【済】＋**要実装30本をOG-0独立held-out回帰フィクスチャ緑必須(第三者確認)**。緑≠完成の三点＋最暗12＋最小動き12自動抽出 |
| 7. レンダ規律 | 10 | §7 CRF16/libx264/CPU/1本直列【済】・concurrency4・再レンダ後sha照合・freshness【済】・輝度最終mux後(range pin) |
| 8. 尺予算(20分) | 10(OG条件) | §8 1,170–1,230s=check_runtime_band【済】・**script_wordfloor(wc実算3,195・158wpm1,225s)**【仕】・水増しを**info_beat(意味単位)＋script_binge開ループ≤90s(傘除外)**【仕】で検出・5:00-11:00 per-window報告 |
| 9. サムネ/OP/ED | 10(OG条件) | §9 curiosity-gap3案・**彩度床thumbnail_saturation新設・一次を案Bへ再評価・赤塗り数字・$0ビジュアル暗示・320px実測添付・案A実寸矛盾是正・IRS印撤去**・Y≥33【済】＋thumbnail_text_contrast【仕】／PD bookends【済】＋ED固定ベッド(VOダック2段・roar禁止・"That is next."アンカー) |
| 10. Codex画像/実装粒度 | 10(v002条件) | §10 **単独画像 unique≥136(現行62→v002拡張要件)＋実在プレート6**4K・**実写0本(生成のみ・過去失敗#4リスクをオーナー明示)**・SDXL禁止・**footage_utilization【実装済】＋rendered_footage_min(生成静止画≥34)**【仕】・画像個別≤3・depth≥70%(239/324)・pre-grade median/mean/dim/scrim帯≥68／§3.6数値(MOTIONKIT写像)をRemotion化。**ai_prompts v002 で136枚化するまで distinct0.42 は仮定** |
| **計** | **設計100／実現は3前提条件付き** | 全過去失敗が§11で名前のある機構(既存SOLID優先=caption_coverage/check_padding/footage_utilization/image_cut_luma/script_lint/arc_nonrepeat/motion_energy を明示配線)に紐付き・各床が本話具体値(distinct136/324=0.42/SceneBed Y'≈58/語数実算3,195/figure cadence全ペア≤90s)。**ただし ①CLM台帳 ②EP33/34指紋台帳 ③ai_prompts v002(136枚) の3成果物が未実在＝軸1/10と arc は仮点**。**これらを[OG-0.5]/[OG-1]/[OG-3]で実ファイル化するまで実現100を主張しない** |

> **100点の正直な性質（監査gaming#34, animation#16反映）**: 本スコアは**「設計として」の100点**=SPEC4基準(全失敗→機構§11/各床具体値/Codex実装粒度/未解決BLOCKING・MAJOR=0)を満たす。軸2/3/4/5/6/8/9の【仕】機構は**OG-0独立held-out回帰フィクスチャ緑を満点の明示条件**とし、**実現スコアはフィクスチャ通過（第三者確認）で確定**する(§14残存前提)。**フィクスチャ未通過で実現100を主張しない**。

---

## §14. 既知の実行前提(Known Preconditions)
1. **recheck 14項目**(§1.3)は出荷前一次確認。特にHinders議会証言・立法助力・McLellan距離は主張禁止。**IRS方針転換メモ日 vs NYT一面(2014-10-25)の前後・McLellan押収日(概ね2014-07)vs 方針メモ(2014-10)の前後**を一次確定し本文の因果と桁一致させる（本文は既に是正済）。
2. **VO声**=過去と同じElevenLabs・同速(~150–165wpm)。実wc3,195は158wpm中央値で1,225s(band内)だが**唯一の判定は実TTS runtime_band**。150wpm時1,290s→§8.2トリム、165wpm時1,174s→§8.2追加。
3. **画像はCodexのみ**(SDXL/A1111/ComfyUI勝手起動禁止)。
4. **仕上げはこのWindows PC・CPU(libx264)・CRF16**。NVENC禁止。
5. **WebGL/depth長尺`--concurrency=4`**。
6. **factory棚ラベル破損前提**。内容ベース選別＋ラベル付きコンタクト目視QC。
7. **3話アーク非重複=生産順序依存**: EP33→EP34→EP35順で`arc_used_fingerprints.json`にfootage(sha+pHash+内容タグ)＋ambience/music stem sha記録。**上流EP33/34のcontent-tag列実在を[OG-0.5]で物理確認**。EP33/34未レンダ欠落=FAIL停止。content-tag割当確定表(§3.5C)遵守。
8. **公開状況は実チャンネルAPIを正**。
9. **git**: 開始pull・各ステップpush・SSD(H:)/runs除外。
10. **予約公開はオーナーGO待ち**。コストは範囲内自由・超過のみ日本語確認。
11. **MOTIONKIT/motion3d再利用**(二重実装禁止)。**要実装30ゲートのDSP系(figure_flow/image_pan_flow/roar_anomaly/subject_luma/cluster_buzz/caption drift)はフルスクラッチ相当・OG-0独立held-outフィクスチャで実効性を第三者検証(「既存拡張で可」の楽観は撤回)**。
12. **完成の定義**: §6全hard緑＋要実装ゲート配線＋OG-0独立フィクスチャ緑＋preflight実物提示＋[OG-4]承認の三点＋α。緑だけ・自己申告での完成宣言禁止。
13. **独立レビュア調達**: §2.1 story=bingeレビューは別セッション/別モデルで実施し署名記録(自己署名を満点根拠から除外)。
14. **★着手前ブロッカー3件（監査BLOCKING・実成果物不在）★**: (a)**CLM台帳(CLM-0001〜0020)** を `01_research/` に実生成するまで §13軸1は仮点・引用は空参照。(b)**EP33/34 `arc_used_fingerprints.json`(sha+pHash+content-tag)** を実レンダ＋生成するまで arc_nonrepeat拡張は検証不能・仮点([OG-0.5]で停止)。(c)**ai_prompts v002 で単独画像 unique≥136＋不足プレート** を実発注するまで distinct0.42・footage床は仮定（現行実引き継ぎは68枚=単独62＋プレート6・実写0本）。
15. **実写素材0本の前提**: 本話は全カットが生成静止画/図/depth（ai_promptsが実写を差替）。`footage_utilization`【実装済】で136生成資産の全使用を強制し「本物実写ゼロ＝紙芝居」知覚リスクを緩和。実写を一部調達する場合は v002 で置換し distinct を再計算。
16. **工程分担**: RemotionコンポジションとCodex画像プロンプトのみ Codex 実装。要実装DSPゲート約30本(figure_flow/image_pan_flow/roar_anomaly/subject_luma/cluster_buzz/caption drift/thumbnail_saturation 等)は Claude 別工程(pd-division-of-labor)。「Codex単体で全実装」は主張しない。

---
(本設計書v005は EP32_carsearch_DESIGN.v002準拠・20分仕様・**敵対監査55件＋pass1監査34件(BLOCKING/MAJOR)を全反映**。台本は実算3,195語を同梱しAI臭を本文で実削除(合否源=既存SOLID script_lint)、**footage distinct=136/324=0.42(実引き継ぎ68枚基準へ再計算・実写0本)**/SceneBed実full-range Y'≈58/figure cadence全ペア≤90s機械再計算/音DSP閾値確定/サムネ彩度床＋案B一次 等の床を実数・実HEX・実DSP定義で確定。**既存SOLIDゲート(caption_coverage/check_padding/footage_utilization/image_cut_luma/script_lint/arc_nonrepeat/motion_energy)を主柱に明示配線し、要実装ゲートはその上乗せ＋OG-0独立フィクスチャ条件で正直区別=水増しゼロ**。**★実現の3前提=CLM台帳・EP33/34指紋台帳・ai_prompts v002(136枚)の実ファイル化が未完＝該当軸は仮点**。Remotion/画像はCodex・DSPゲートはClaude別工程。)