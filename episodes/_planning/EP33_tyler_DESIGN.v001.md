# 動画制作設計書 — Prime Documentary EP33（round 7・pass1監査34件＋pass2監査31件＋pass3監査25件反映・実ゲート台帳整合版）

> **pass3監査25件（BLOCKING 2／MAJOR 7／MINOR 16）反映サマリ:** (1)**機能語行末0（`_NO_DANGLE_END`）を受領側hardゲート化**＝producer自己検査だけに依存せず、`check_caption_format`を拡張して最終shipped `captions.srt`を独立再検査し`check_final_acceptance.py`に配線＋赤フィクスチャ（機能語行末SRTでexit1）＝§11#2/§13 axis6を【要実装/本話ブロッキング】へ格上げ（pass3 BLOCKING#2）。(2)**6:10二人称脅威ビート②に実インラインVOを新設**＝6:10は実体が三人称叙述だった（14:20と同型欠陥の再発）ため`[2P-THREAT]`実VOを刻み、真の二人称空白を2:40→6:10→9:00で≤5:30に接地（pass3 BLOCKING#12）。(3)**語数算術を155wpmで実際に閉じる値へ再接地**＝ブロック表が実は≈161wpmでしか閉じずAct2=168/Act3=165が上限超だった問題を、総VO≈3,050語（Act1 505/Act2 450/Act3 580/Act4 620/Act5 720＝各≤155wpm）へ下げ、ED実文を124語≒48sへ訂正、§8是正指示を「非VO遷移圧縮」→「発話語数削減」へ修正（pass3 MAJOR#6/#25/#14）。(4)**Hook/Act1の居住ドラマとCLM-0003（転居・空き家）の内部矛盾を是正**＝Act1冒頭に高齢者コミュニティ転居/コンドは思い出の空き家を早期織込み、Hookを立ち退き誤認しない言い回しへ（pass3 MAJOR#13）。(5)**asset_selection.v001.json（68行 image→cut再利用台帳）を画像生成前のブロッキング前提成果物として確定**＋画像図案の記録正典＝`ai_prompts.v001.md`（68枚確定・幕別13/10/16/9/15/5一致）を§10に明示（pass3 MAJOR#18/#21）。(6)**未実装ゲートの実効降格を正直明記**＝motion/luma per-episode override・`check_longform_drift`・caption skip封鎖・`test_gate_fixtures.py`は未実装で、実装するまで実効床は台帳既定値（motion p10≥9/body YAVG<48）で走ると降格記載し§13.2に接地（pass3 MAJOR#19）。(7)**3話アークの法廷/庁舎素材分配を§12 step7の出荷前hard前提へ格上げ**＝棚の3話分distinct QC生存数を実測するまでレーン非重複は「計画上OK・未検証」とし合格にしない（pass3 MAJOR#20）。(8)**motion_energyのstill-p10/medianを「既存床の校正」でなく「新統計の要拡張」と正直ラベル**（実ゲートはmean/p10・全body母集団を計算しstills限定p10/medianは未計算・pass3 MINOR#24）。(9)MINOR是正=§1.1にPLF推計のEst.併記カーブアウト／§3.10 preflightにマップ最低ノード・字幕safe-rect明記／structure_4partの実契約（HOOK→OP→body→ED・幕数非依存で5幕body受理）をコード確認して記載／`verify_script_lint`辞書に`never saw coming`追加＋固有名詞密度をreview_facts line-item化／§4.2のmusic存在は`SOUND_PROV_MIN_MUSIC=1`で自己申告＋sha束縛される旨に正確化／footage使用率の重複閾値を単一床へ／§3.0総尺セルを「band中央・20:00固定撤回」へ／Act4役割セルを「OL3開/OL4開閉」へ／OL2開位置と"二度"リビール順序の統一。

> **round6→round7 スコア注記:** pass3の再接地（語数≈3,050・未実装ゲートの実効降格・機能語行末hard化を要実装へ）を反映。設計完全性=98（変更なし・axis3/axis9の軽微留保据置）。実効ゲート=62は据置（機能語行末hard化・longform_drift等は依然要実装ゆえ実効点に計上しない）。

> **pass2監査31件（BLOCKING 3／MAJOR 11／MINOR 17）反映サマリ:** (1)`check_sound_layers`の能力を実挙動へ接地＝distinct SFX≥12/beds≥4は**provenance自己申告＋mux sha束縛**であって波形からのSFX個数検出ではない（"実mix解析"の過大主張を撤回・§4.1/§4.4/§6.1/§11#22/§13）。(2)`check_stem_loudness`/`check_music_coverage`/`check_motion_bbox_flow`は**"存在しない"でなく"実在するが未配線"**へ事実訂正（台帳ドロップ方針で引用はしない）。(3)§4.6(a)の「stem実測床(Music>-24/Amb>-30)で担保」＝ドロップ済ゲート閾値の残留リークを撤回し人間試聴backstopへ。(4)`beds≥4`はアンビ別ベッド数でありmusicベッドを担保しない（§4.2）。(5)実配線`check_arc_nonrepeat`は**他話film.jsonのcut src basename交差=0**を判定し`catalog_fingerprints`を読まない→「アーク共有で交差判定除外」はno-opゆえ撤回、既定=完全分離(方針A)／共有allowlistは要実装(方針B)へ（§3.6/§12/§14）。(6)`motion_energy`/`check_body_luma`の床はグローバル定数で「本話だけ校正」は不可→per-episode override機構を要実装として明記（§3.7/§3.8/§14）。(7)ED非VO約36秒の尺合わせバラストを撤回しED VOを実質増補・20:00固定撤回（§2.5/§8）。(8)`verify_sfx_manifest`の「hard化」→advisory、機能語行末0はproducer自己検査、二人称ビート採番統一、"more than a dozen"→"at least a dozen"、CLM-0014Bを1692制定法に確定、`script_lint.py`→実ファイル名`verify_script_lint.py`、再フック本数19→18、68枚per-image台帳は未作成＝画像割付未具体を正直表示、等のMINORを是正。

**Episode:** EP33 ／ **slug:** PD-2026-033-tyler ／ **Series:** They Did Nothing Wrong アーク（財産権三部作）第1章
**題材:** Tyler v. Hennepin County, **598 U.S. 631 (2023), No. 22-166**（9–0全員一致）
**視覚レーン:** 家・自治体・94歳（EP34=空港/現金、EP35=自営/銀行 と素材完全分離）
**★尺=20分（オーナー厳命）★** 完成 **19.5–20.5分＝1,170–1,230s**。合否は `check_runtime_band.py` 実測のみ。**水増し（フィラー/尺削り/装飾ループ/無音/同義反復/尺合わせ挿入尺）で尺を稼ぐのは0点＝恒久禁止。**

> **本改稿の背骨（pass1監査34件・実ゲート台帳への整合）:** round4は「実在しないゲート／偽装耐性の弱いゲート」を確実な自動保証として引用し、逆に**現に配線済みのSOLIDゲートを『要実装』と誤ラベル**していた。round5はこれを実ゲート台帳と1対1で照合し是正した。最重要の是正は次の8点。**(1) ドロップ済ゲートの引用を全撤去（pass2で"存在しない"→"実在するが未配線"に事実訂正）:** `check_stem_loudness`／`check_music_coverage`（音）と`check_motion_bbox_flow`（＝per-figure-bboxフロー・モーション）は**`scripts/`に実在するが`check_final_acceptance.py`に0回参照＝未配線・現状走らない**（round5の"存在しない"は誤り）。台帳ドロップ方針に従い自動保証として引用しない。音の保証は**配線済みSOLIDの`check_sound_layers`（distinct SFX≥12／beds≥4は provenance自己申告＋mux sha束縛、波形実測は onset密度＋ambience帯域のみ＝"実mix解析でSFX個数検出"の過大主張はpass2で撤回）**＋§6.2の音5本試聴（人間backstop）へ、モーションの保証は**配線済みSOLIDの`motion_energy`（within-shot≥12／p10≥9）**＋§6.3 motion-reel承認へ移した。bbox-localフローはadvisory（参考）に降格しhard blockerとして引用しない。**(2) SOLID/wiredゲートの誤ラベル訂正:** `check_image_cut_luma`・`check_arc_nonrepeat`・`check_footage_utilization`・`verify_onscreen_text`・`check_thumb_subject_luma`・`check_padding`・`motion_energy`・`verify_script_lint`・`verify_caption_coverage`は**全て`check_final_acceptance.py`に配線済み（SOLID）**。round4の【要実装／新規】表記は誤りで、本稿では【実装済(wired)／要校正・要拡張】に訂正（既存拡張であり新規スクリプト新設ではない＝invariant14二重実装回避）。**(3) WEAKゲートの正直降格:** `verify_sfx_manifest`／`verify_script_structure`／`check_ending_sound`は台帳でWEAK（機能はするが偽装耐性が限界・完全な自動保証として引用禁止）。POST-render hard列から外しadvisory化、最終保証は§6.2 preflight_owner_review人間試聴＋§12 step3★オーナー台本ロックへ。**(4)** 主アークOL1/OL2/OL5が3〜4幕をまたぐのに§2.7(a)が「同幕/次幕内」を強制し正典台本を自らブロックする内部矛盾を、二階建て回収規則に是正。**(5)** 「14:20二人称脅威ビート」が実体は三人称マグナカルタ叙述で、真の二人称空白が9:00→18:40＝9:40と5:30床を突破していた点を、Act4内（12:00）に二人称脅威ビートを新設して是正。**(6)** 焼込むclimax逐語（CLM-0012/0013/0014A）を§1.4 recheckに一次出典ロケータ必須で追加（onscreen_textは台本==画面しか照合せず架空引用を捕えないため）。**(7)** 語数算術（3,140 vs 3,067、ED155 vs 実60）を実全文語数に接地し、runtime_band実測を唯一合否として再ペーシング前提に一本化。**(8)** スコアの実効ゲート点を、配線済みゲートを正しく計上して再算出（round4は配線済みを0計上し過小申告していた）。

**全ゲートに3ラベル（実ゲート台帳と1対1）:**
- **【実装済(wired)】** 現行`check_final_acceptance.py`にhard配線済（台帳=SOLID）。実定数・実挙動・限界（何を測らないか/どこでskipするか）を併記。本話向けは**閾値/config校正のみ**（新規スクリプト新設でない）。
- **【WEAK(偽装耐性限界)】** 台帳でWEAK。機能はするが深い偽装耐性が限界。**完全な自動保証として引用しない。** hard保証の本体は人間試聴backstop（§6.2）＋★オーナーゲートに置く。
- **【要実装／本話ブロッキング】** EP33出荷の一部として**真に新規**な機構のみ（既存拡張はここに置かない）。ファイル名・関数名・確定閾値・配線先・入力・**赤フィクスチャ（既知バッドでexit1する証拠）**を明記。実装＋赤緑両実証まで、支える§13軸は「確定10」にしない。
- **【自己申告(sha束縛のみ)】** provenance JSON数値を読むだけで実測しない箇所。正直に降格表示。
- **🗑実在するが未配線＝ドロップ扱い（引用禁止・pass2事実訂正）:** `check_stem_loudness`／`check_music_coverage`／`check_motion_bbox_flow` は**`scripts/`に実在するが`check_final_acceptance.py`に0回参照＝現状走らない**（"存在しない"は誤り）。台帳ドロップ方針で本稿は一切hard機構として引用せず、配線済ゲート（`check_sound_layers`／`motion_energy`）か人間試聴backstopに差し替えた。配線可否はEP33臨界パス外の別ワークストリーム。

---

## §0. 勝ちフォーマット

勝ち筋（pd-analytics-findings 2026-07-04）＝「判例 × 権利 × 11–12分」。本話はオーナー厳命で20分。中核（最高裁判例・二人称の権利脅威・逆転劇）を薄めず、**20分は"物語の中身"で満たす**（人間ドラマ・並行被害者Hallの記録準拠物語・制度の仕組み・800年の歴史・全米波及）。

- **北極星4指標:** CTR 6.0%（実測2.31%）／APV 45%／30秒残存70%／登録転換10%。
- **音基準チャンネル:** 高密度志向。ただし**「Kurzgesagt級」を音"質"保証と誤読させる表現は撤回**（監査#28）。劇伴は factory棚既製ベッド6本＋2-passミックスで、密度は数値床で担保、質はラベル付き試聴オーナーゲート（§6.2）で人手承認。
- **20分は"物語"で満たす:** 統計の塊で尺を作らない。台本水増しは代理指標でなく台本linter＋独立レビュー＋**現に走るpadding検出器**で直接検出（§6.4）。
- **本話"見ごたえ"予算（確定値）:** シーン40・カット539・平均2.23s・depth **44.2%（238/539・分母=全カット・§3.5）**・動くFigureBeats **19種（各幕アクティブ≥4＋時間分布床＋【実装済(wired)】`motion_energy`実測床＋§6.3 motion-reel人間承認で担保。bbox-localフローはadvisory参考のみ）**・ヒーロー面 **6（時間分布床あり・Act3/Act4にも配置）**・distinct SFX **20（base_id≥14）は【実装済(wired)】`check_sound_layers`のdistinct≥12/beds≥4床を上回る本話目標**・遷移SFX distinct≥4・ambience base 6・music6・字幕460–500枚・Codex画像68枚。

---

## §1. 事実（FACTS LOCKED）— CLM単位・一次出典・grade

**シード誤り確定訂正（放送・画面テロップ全体に適用）:**
- **①引用 `598 U.S. 631 (2023), No. 22-166`。シードの「600 U.S. 631」誤り。画面/台本に「600」を一切使わない。**
- **②代理人 Pacific Legal Foundation（Christina Martin 弁論）。Institute for Justice ではない。**
- **③Tyler本人remand後の金銭回収額は断定しない。EDは全米ルール/原則の回復に着地。**
- **④★Hall v. Meisner は原告 Tawanda Hall（女性）が第6巡回で「勝訴」した判決。round3台本は「Hallが敗れた」と史実と逆に描いており全面書き直し（監査aismell-BLOCKING#49・§2.6/CLM-0021）。**

### 1.1 出典グレードの規律
**grade A ＝ 一次資料（SCOTUS意見本文／下級審判決文／訴訟記録／Cornell LII掲載意見）で確認できるもののみ。** Wikipedia・報道・擁護団体（PLF）は二次/三次資料で単独ではgrade Aにしない（LLMも出典にしない）。Wikipedia/報道/PLF単独クレームは grade B＋`fact_recheck` に降格し**画面焼き込み禁止**。
- **★pass3 MINOR#1カーブアウト（PLF推計の唯一の焼込許可条件＝§1.2/CLM-0017/0018/§5.4 T11/T12と統一）:** grade-BのPLF等推計は**原則 画面焼込禁止**。ただし**視認可能な "Est. — <source>" 修飾を常時併記する統計チップ（T11 `$780,000,000+`／T12 `92% PAID`/`8% DEBT` 等）としてのみ焼込可**。単独の断定的事実（Est.併記なしの数値）としては焼込まない。この一文で「§1.1の絶対禁止」と「§1.2/CLM表の Est.付き条件許可」の内部矛盾を解消する（PLF統計はナレでは自由に述べてよいが、画面ではEst.チップ形式に限る）。

| ID | 主張（要約） | 一次出典 | grade | 画面焼込 |
|---|---|---|---|---|
| CLM-0001 | 事件名・正式引用 **598 U.S. 631 (2023), No.22-166**（143 S.Ct.1369） | SCOTUS意見/Cornell/Justia | A | 可 |
| CLM-0002 | Tyler、判決時**94歳**。1999年購入・10年超一人暮らし | 94=意見/A。1999=報道/PLF→B | 94=A/1999=B | 94のみ可 |
| CLM-0003 | 約2010年、安全懸念で高齢者コミュニティへ転居、コンド空き家 | 意見background=A／引き金詳細=B | A（引き金B） | 年不可 |
| CLM-0004 | 未払い元本 **約$2,300**、利息等で**約$15,000**へ | 意見(Cornell)/A（内訳B） | A | $2,300/$15,000可 |
| CLM-0005 | 郡がコンドを**$40,000で売却**、債務消滅後も**全額保持**＝余剰~$25,000没収 | 意見(Cornell)直接引用/A | A | 可 |
| CLM-0006 | 余剰は郡・町・学区で分配、元所有者に回収手段なし | 意見(Cornell)直接引用/A | A | 可 |
| CLM-0007 | 第5修正Takings＋第8修正Excessive Fines（＋実体的DP）で提訴 | 意見/PLF/A | A | 可 |
| CLM-0008 | 地裁2020却下、第8巡回2022是認、最高裁受理 | 意見手続史＋公式リポータ/A | A（cert日B） | 年のみ可 |
| CLM-0009 | 口頭弁論 **2023-04-26**。PLFの **Christina Martin** 弁論 | PLF/意見記録/A | A | 可 |
| CLM-0010 | **2023-05-25、9–0**でTyler勝訴。**Roberts長官**執筆 | 意見/A | A | 可 |
| CLM-0011 | 判旨=債務超過分の保持は正当補償なきTaking（第5修正違反）。**第8修正は判断せず** | 意見(Cornell)/A | A | 可 |
| CLM-0012 | Gorsuch同意(Jackson同調)＝抑止的経済制裁も「別名の罰金」 | 意見(Cornell)/A | A | 可（§5.4逐語） |
| CLM-0013 | Roberts名言「…render unto Caesar what is Caesar's**,** but no more.」（カンマ・意見綴り） | 意見(Cornell)/A | A | 可（逐語） |
| **CLM-0014A** | **余剰返還=マグナカルタ(1215) ch.26。「…the residue shall be left to the executors…」（死者の債務清算で残余を遺言執行者へ）** | 意見(Cornell)直接引用/A | A | 可（逐語・**1215アイコン限定**） |
| **CLM-0014B** | **「Overplus…immediately restored to the Owner」は1692年の英議会制定法（4 W. & M., ch.1, §12・3 Eng. Stat. at Large 488–489 (1692)）由来で1215マグナカルタではない（pass2 MINOR是正：意見本文が当該句を1692制定法に明示帰属。"＋Blackstone"はこの引用句には裏付けなき付加帰属ゆえ削除。Blackstoneは一般原則の補強として別途引かれるが本句の出典ではない）** | 意見(Cornell)直接引用・1692制定法/A | A（年代=1692確定） | 可（**"English statute, 1692"ラベル必須・1215羊皮紙に載せない**） |
| CLM-0015 | 先例＝United States v. Lawton(1884)／Webb's(1980) | 意見(Cornell)直接引用/A | A | 年のみ可 |
| CLM-0016 | 判決時、意見が「一定数の州＋連邦が余剰返還を要求」と記す（**具体数「36」は放送前に意見本文で要確認**） | 意見本文に「36」が在る場合のみA。Wiki/amicus経由ならB | 要確認（暫定B） | **数の焼込は本文確認後のみ** |
| CLM-0017 | 全米 home equity theft：2014–2021に**~8,500戸以上**・**$780M超**喪失（平均86%） | PLF Size&Scope（擁護団体推計） | B（`Est.`必須） | `Est.—PLF`併記必須 |
| CLM-0018 | MNで2014–2020に**~1,200戸**、平均債務は物件価値の約8%、**~$118M**喪失 | PLF案件ページ（擁護団体推計） | B（`Est.`必須） | `Est.—PLF`併記必須 |
| CLM-0019 | 判決は遡及適用、州法改正誘発（NY/Nebraska/Montana） | Community Progress/PLF他 | B（制定法要再確認） | 州名断定不可 |
| **CLM-0020** | PLFはTyler以外も代理（**Tawanda Hall＝女性・Hall v. Meisner, 6th Cir.**） | PLF/第6巡回記録 | B（第6巡回意見で要裏取り） | 裏取り前は実名/性別/所在不可 |
| **CLM-0021（新設・監査#49）** | **Hall v. Meisner（第6巡回, 2022）で Tawanda Hall が"勝訴"＝補償なき自宅equity収奪は違憲と判示。Oakland County/Southfield(MI)がHall宅を差押後、私企業(Southfield Neighborhood Revitalization Initiative)へ$1で移転し約$308,000で転売。債務は約$22,600。Tyler(2023-05)より前の巡回勝利で、Tylerがこれを全国ルールへ確定させた** | **第6巡回意見PDF（一次）で裏取り必須** | **B（裏取り前は出荷不可・grade A化して確定）** | **裏取り後のみ・金額/所在は本文確認後** |

### 1.2 キー数値（画面焼込許可＝grade Aのみ）
`598 U.S. 631 / No.22-166`・`9–0`・`94`歳・元本`$2,300`・総債務`$15,000`・売却`$40,000`・郡保持`$40,000全額`・余剰`~$25,000`・口頭弁論`2023-04-26`・判決`2023-05-25`。**焼込禁止（B/要確認）:** 購入年1999・下級審引用番号・cert日・PLF統計（`Est.`併記なし不可）・州法改正の州名・「36」州具体数（意見本文確認まで保留）・**Hall事件の全数値/所在/性別（第6巡回意見裏取りまで）**。

### 1.3 州数フレーミング整合（50−36捏造撤回・監査#42維持）
- **主表示（grade A条件付き）:** `states + federal already required return`。「36」具体数は意見本文で majority opinion に在ると確認できた場合のみ焼込。amicus/PLF由来なら「a large majority of states already required return」へ置換。
- **保持側（StateMap点灯）:** PLF列挙「12州＋DC」（grade B・`Est.—PLF`）。**文言「AT LEAST A DOZEN STATES STILL ALLOWED IT」（点灯12ノードと一致・"more than a dozen"＝>12は点灯12と矛盾するため撤回・pass1 MINOR）。** DCは州として点灯せず注記のみ（＝"a dozen"=12は州のみ）。点灯ノード=PLF列挙12州。**「50−36=14」の算術で点灯数を導出しない。** PLFのSize&Scope基礎数字が確定的に≥13州であると§1.4 recheckで裏取りできた場合に限り、点灯ノードをその数へ増やしたうえで"more than a dozen"を採用可。
- 保持側12州と要求側36州を**補集合として提示しない**。別ソース・別チップで独立提示。

### 1.4 放送前 recheck（§12ゲートで確認）
購入年1999・売却年(~2016)・cert日(2023-01-13)・PLF統計基礎レポート照合・州法改正の制定法/施行日・「36」州が majority opinion 本文に在るか・**Tawanda Hallの身元/性別/所在/主張/第6巡回の結果（CLM-0021をgrade A化）**・**CLM-0014Bの制定法年代帰属（意見本文で1692年 4 W. & M., ch.1, §12 を確認・Blackstone付加は本句に不使用）**・Tyler本人remand後回収可否・**★Act1の居住描写がCLM-0003（約2010年に高齢者コミュニティへ転居・コンドは空き家）と齟齬しないこと＝"居住中に住処を追い出された"誤認を生む文言がHook/Act1に無いかを人手確認（pass3 MAJOR#13）**。**確認不能はgrade B＋`fact_recheck`。裏取り不能なら実名/性別/所在を出さず匿名帰属。**

**★焼込む逐語引用の一次出典ロケータ必須（pass1 BLOCKING・監査#F）:** `verify_onscreen_text` は「画面テキスト==台本quote」しか照合せず、**台本と画面が揃って誤っていても（架空/誤記憶の引用でも）検出できない**。よって画面に焼く全逐語引用を、放送前に**一次意見本文で存在確認したロケータ（slip opinionのページ/行 または Cornell LII アンカー）付き**で§1.4 recheckにgrade-A条件として明記する:
- **CLM-0013 / T19 Roberts「…render unto Caesar what is Caesar's, but no more.」** ← Tyler意見本文に当該句が実在するかを一次確認（"render unto Caesar"は特徴的表現で存在は自明でない）。カンマ・綴りまで確認。
- **CLM-0012 / T3' Gorsuch「fines by any other name」** ← Gorsuch同意意見本文に実在するか一次確認。T3'はこの完全文からの逐語断片であることを確認。
- **CLM-0014A / T15 residue句「…the residue shall be left to the executors…」** ← Tyler意見引用のMagna Carta ch.26逐語を一次確認。
- **CLM-0014B / T16 Overplus句** ← 制定法年代帰属（"English statute, 1692"＝4 W. & M., ch.1, §12）とともに一次確認。Blackstone付加は本句に不使用。
- **運用ルール:** `reviews/review_facts.md` は焼込む各引用に**解決可能な一次出典ロケータ**を必ず持つ。ロケータが解決しない引用は**焼込禁止**＝引用符を外して言い換え（paraphrase）にするか当該テロップをカット。`verify_onscreen_text`（wired）は台本quote照合に加え、**review_factsに当該CLMのロケータ・フィールドが存在しない引用の焼込をblock**する薄い前提検査を追加（要拡張）。ロケータ確認は人手（§12 step2）でも二重化する（機械照合だけでは架空引用を捕えられないため）。

---

## §2. 台本（構成・語数・独立3レビュー＝実行主体分離・本文インライン）

### 2.1 台本メタ（wpm校正＋帯外是正の正直化）
- **採用声:** ElevenLabs、過去話と同一 voice_id / stability / similarity / speed。EP33で声質・速度を変えない。
- **wpm校正（算術を155wpmで実際に閉じる値へ再接地・pass3 MAJOR#6/#25是正）:** 実測帯 150–165（中央~155）。**総尺目標=band中央~1,200s（20:00固定は撤回・§8）。**
  - **★pass3是正の背景:** round6のブロック表（Act 520/490/620/645/720＝2,995語 vs 幕tc計1,116s）は**~155wpmでは閉じず、実は≈161wpmでしか閉じなかった**（Act2=168・Act3=165が採用帯の上限を突破）。ヘッドラインの「単一wpm~155で一本化」が自らの数値で偽になり、Act2/Act3が要所を駆け足にしていた。よって**総VO語数を155wpmで幕tc内に実際に収まる値へ下げて再接地する**（option(b)採用）。
  - **再接地した設計/目標語数＝約3,050語（各幕≤155wpmで閉じる・script_final.v001の実全文で再集計する前の設計値）:** Hook18・OP40・**Act1 505（196s→154.6wpm）・Act2 450（175s→154.3wpm・168→是正）・Act3 580（225s→154.7wpm・165→是正）・Act4 620（240s→155wpm）・Act5 720（280s→154.3wpm）**・**ED VO約124（§2.5実文の実カウント＝48s@155wpm・round6の「約115語≒44s」は実文の過小カウントゆえ訂正）**。合計≈3,057→**約3,050語（丸め）**。
  - **★3,050は"確定した実全文語数"でなく"設計/目標値・再集計待ち"（pass3 MINOR#7是正）:** Act本体（505/450/580/620/720）は script_final.v001 が書き上がった時点で実語数で再集計する**設計値**であり、round6の「実全文語数で確定」「単一の実測基準語数」という断定表記は撤回する（Hook18/OP40/ED124は§2.3–§2.5の確定全文の実カウント、Act本体は目標）。round4の「≈3,140」「3,067」二値矛盾・157wpm逆算・round5の「ED約60語＋非VO約36s」も撤回。
- **固定語数は帯を保証しない（正直開示）:** 150–165の全域で1,200s±30sを固定語数で保証することは数学的に不可能（floor安全側は≥3,218語、ceiling安全側は≤3,075語で両立しない）。よって**語数は期待wpm≈155でband中央を狙う設計値**にとどめ、最終合否は下記に委ねる。
- **合否:** ロック前にElevenLabsドラフト実測wpmで再算出し `check_runtime_band.py` 実測(1,170–1,230s)を**唯一の合否**。**帯外なら再ペーシング（上限超=圧縮・薄い遷移削除・同義反復除去／下限割れ=独立レビュー②③が『物語に要る』と判定した素材のみ増補＝Act3 Hall物語・Act5弁論往復の実質増、水増し禁止）。** 語数表は目安であり、runtime_band実測が支配する。
- **帯外是正＝再ペーシングのみ（尺合わせ挿入尺は撤回・監査gaming#30維持）:** 上限超は冗長圧縮・薄い遷移削除・同義反復除去。下限割れは**独立レビュー②③が「物語に要る」と判定した素材のみ**追加。**秒数を出し入れする決定論的reserve/trim表は本設計に存在しない。**各ビートの存否は「尺のため」でなく「物語に要るか」だけで決め、`review_pacing.md` が全60秒窓に「消して物語が成立するか」を適用（§6.4）。

### 2.2 構成（8秒フック→短縮OP→本編5幕→earned CTA・**離脱防止再設計・Act1圧縮**）

監査retention #54/#55/#56/#57 反映。**Act1をペイオフ前倒しで圧縮／二人称の6:16空白を2:40ビート新設で解消／OL1を系統的問いへ／中盤谷を11:15再フックで充填。**

| ブロック | 尺帯 | 語数 | 役割・オープンループ・再フック |
|---|---|---|---|
| Hook | 0:00–0:08 | 18（実全文§2.3） | 核（$40,000/$25,000）を出さず「$2,300で家が消え、しかも合法」の逆説のみ。**三人称の逆説フック（"the home this woman had spent years paying off"＝資産/家の記憶・立ち退き誤認回避#13・二人称の初出は0:24）。** |
| OP（短縮） | 0:08–0:24 | 40（実全文§2.4） | 16秒短縮・第1幕の音/絵をタイトル下にブリード・**0:24二人称賭け金"one late tax check could cost you yours"を実文へ（#15）** |
| Act1 女性 | 0:24–3:40 | 505（154.6wpm） | **1:50に「$2,300→$15,000膨張」slam一撃ペイオフ（#56）／2:40に二人称脅威ビート①（#54）**。一貫匿名フィギュア＋感覚ディテール。**★早期に安全のため高齢者コミュニティへ転居しコンドは思い出の空き家、という事実を織込む（CLM-0003整合・立ち退き誤認回避・pass3 MAJOR#13）。****OL1＝「この理不尽な仕組みを止められるのか」（系統的問い・#55）** |
| Act2 差押え | 3:40–6:35 | 450（154.3wpm・168→是正） | **EquityBarで余剰$25,000をここで初出し（4:50・Hookで開示しない）**→slam→「Nothing」。**二審の"二度敗訴"リビール（Act2末尾~6:35）→その事実を前提とするOL2を6:35以後に開く（順序統一・pass3 MINOR#17）**。**二人称脅威ビート②(6:10・実インラインVO付き・§2.2台帳＝①2:40/②6:10/③9:00/④12:00/⑤15:30と統一)**。**★pass3 MAJOR#14是正:round6の490語÷175s≈168wpmは採用帯150–165の上限超だった→450語（154.3wpm）へ約40語圧縮して幕内wpmを≤155に確定（"ロック前に再算出"の宙吊りを解消・水増しでなく冗長圧縮）。** |
| Act3 一人ではなかった | 6:35–10:20 | 580（154.7wpm・165→是正） | **Hall事件＝記録準拠のミニ物語（Hallは第6巡回で"勝訴"・#49）**。**Hall決着ビート(9:40)でループ閉**→「巡回勝利は一角のみ→Tylerが全国ルールへ」で本編へブリッジ。生統計≤45秒。**二人称脅威ビート③＝StateMap seed「あなたの州は？」(9:00・実インラインVO付き)**。**★pass3 MAJOR#6是正:round6の620語(165wpm)を580語(154.7wpm)へ圧縮して上限超を解消。** |
| Act4 闘い | 10:20–14:20 | 620（155wpm） | HOW/WHY。**11:15再フック（SplitLadder reveal・#57）**→郡の最強論→**GovtArgumentCard崩壊を13:20に感情ペイオフ確定**。**12:00に二人称脅威ビート④新設（あなたの持ち家にも同じ余剰没収が適用される・pass1 BLOCKING是正）**。マグナカルタ史をGeraldineの窓/家財とintercut。**OL3開/OL4開閉（OL3は11:00開・14:40–15:40=Act5内で閉じる二階建て長距離＝pass3 MINOR#9是正・round6の"OL3/OL4開閉"はOL3閉位置の誤記）** |
| Act5 評決 | 14:20–19:00 | 720（154.3wpm） | 史料をintercut reveal。16:40に口頭弁論の実往復1回を人間ドラマ→**9–0 slam ~18:15**→Roberts名言を二人称StateMap緑化ペイオフと融合→**coda ≤45秒（#61）** |
| ED CTA | 19:00–20:00 | VO約124（実全文§2.5・約48s @155wpm）＋非VOエンドカード≤12s | earned coda＋EP34具体ティーズ（空港/現金没収）。**★pass3 MAJOR#6/#25是正:ED実文の実カウント＝約124語（round6の"約115語≒44s"は実文の過小カウント）＝48s@155wpm。round4「155語」・round5「約60語＋非VO約36s」は撤回。ED VOを実質増補し非VO末尾を≤12sへ圧縮。20:00固定は撤回し`check_runtime_band`内自然終端。** |

**オープンループ台帳（5本・開閉tc確定・監査#53/#55）**

| ID | 問い（未知） | 開 | 閉 |
|---|---|---|---|
| OL1（**主アーク**） | **この理不尽な仕組みを止められるのか（系統的・個人回収を約束しない#55）** | **2:40**（二人称脅威①と同位置に統一・pass1 MINOR是正） | 17:50–18:40（系統的回復・個人回収は非断定） |
| OL2（**主アーク**） | 二度合法とされた差押えを最高裁は覆すのか | **6:35（"二度敗訴"リビール後に開く・pass3 MINOR#17是正。round6の6:10開は"二度"の提示(6:35)より前でループが先に開く順序矛盾だった）** | 18:15（9–0） |
| OL3（短距離ループ） | 余剰没収を違憲とする根拠はどこか | 11:00 | 14:40–15:40（マグナカルタ/Lawton） |
| OL4（短距離ループ） | 郡はなぜ余剰まで取れると確信したのか | 12:20 | 13:20（GovtArgumentCard崩壊） |
| OL5（**主アーク**） | **あなたの州も、つい最近までこれを許していたのでは（過去/普遍形・#62）** | 9:00 | 18:40（StateMap緑化＋改正州の動き） |

> **回収規則の二階建て（pass1 BLOCKING是正）:** 主アーク OL1/OL2/OL5 は映画全体をまたいで ED までに閉じる長距離ループ、短距離ループ OL3/OL4 は同幕/次幕内で閉じる。§2.7(a) の回収検査はこの二階建てで判定する（下記）。

**二人称脅威ビート台帳（pass1/pass3 BLOCKING是正・実インラインVOのある二人称ビートのみ計上）:** 0:24（OP VO賭け金・実VO） / **2:40（実VO）** / **6:10（実VO・pass3新設）** / 9:00（実VO） / **12:00（Act4・実VO）** / **15:30（Act5・実VO）** / 18:40（転回）。**全隣接差＝2:16 / 3:30 / 2:50 / 3:00 / 3:30 / 3:10 →最大3:30 ≤ 床5:30。全ビートに下記の実インラインVOを`[2P-THREAT]`アンカーで刻む（tcラベル止まり禁止）。**
- **round4の欠陥（撤回）:** round4は「14:20」を二人称脅威ビートに数えたが、14:20はAct5冒頭のマグナカルタ**三人称・歴史叙述**（§2.6『In 1215, a cornered king…』）で、視聴者自身の財産への脅威ではない＝二人称ビートに該当しない。実体のない14:20を外すと真の空白は9:00→18:40＝**9:40で床5:30を大幅突破**していた。
- **★pass3 BLOCKING#12是正（6:10が三人称叙述だった＝14:20と同型欠陥の再発）:** round6は6:10を二人称脅威ビート②に計上して最大空白3:30≤5:30を成立させていたが、6:10の実体は再フック・マップ記載どおり「裁判所は二度これを合法とした」＝**完全な三人称・事件叙述で二人称の脅威VOが一行も無かった**（実インラインVOは12:00/15:30だけ）。6:10を外すと真の二人称空白は2:40→9:00＝6:20で床5:30を突破する。よって**6:10に実インラインの二人称脅威VOを新設**（12:00/15:30と同格）:**[VO:] *The same overdue-tax rule that had just swallowed her equity was still on the books in your state, waiting for one late check of yours — until this ruling.*** ＝彼女のequityを飲み込んだのと同じ滞納ルールが、たった一度の小切手の切り忘れを待ってあなたの州にも残っていた、の趣旨（Tyler判決で違憲化した過去脅威＝"was/had"の過去形で§1『現在法を誤断定しない』規律に整合）。これで真の二人称隣接は 2:40→6:10→9:00＝各≤3:30 に接地。
- **是正（実VO付与の徹底・pass3 MINOR#15）:** 計上する全2Pビート（0:24/2:40/6:10/9:00/12:00/15:30）に検証可能な**実インライン二人称VO**を`[2P-THREAT]`アンカーで刻む（tcラベル止まりにしない）。**0:24＝OP VO**（§2.4を『…and about a right you may not know you have — the day one late tax check could quietly cost you your home.』に増補し"小切手を切り忘れたら"の二人称賭け金を実文へ・再フック・マップ0:24グロスと一致）。**2:40＝[VO:] *This was not a loophole aimed at her alone; if your own property-tax bill had ever slipped past its due date, the same machinery could have taken the equity you built.*** **9:00＝[VO:] *So look at your own state on this map, because until very recently the answer to "could it happen here?" was yes.*** Act4内 **12:00**（**[VO:] *And if you had ever been late on a single property-tax bill, this same surplus-seizure machine could have reached your house too.*** ＝pass2 MINOR是正で過去条件法"could have reached"へ統一）。Act5内 **15:30**（**[VO:] *The rule those nine justices were about to touch is the same rule that could have emptied the equity in your own home.***）。全ビートは script_final に `[2P-THREAT]` アンカーで刻み、§12 step3★オーナー台本ロックで「真に二人称VOか（三人称叙述の誤計上でないか）」を人手確認する。
- **`verify_script_structure.py`【WEAK】** が二人称脅威の**最大無出現間隔≤5:30**を**下限フラグ(advisory)として機械計測**（**紙155wpm tcで一次＋voiceレンダ後の aligned narration_index 実時刻で再判定**。現行10秒未満マージンは実尺で破綻しうるが、本是正で最大3:30まで余裕を作った）。**pass2 MINOR#31是正：WEAKゲートの出力を「hard床」と呼ばない。** 機械的間隔検査は下限フラグ(advisory)を出すのみで、**実体のある二人称VOか・真に≤5:30かのhard保証は §12 step3 ★オーナー台本ロック**（三人称叙述の誤計上でないかの意味判断を含む）に一元化する。**0:24→6:16空白は撤廃済。**

**再フック・マップ（各エントリに"約束する新規の未知"併記・OL3 11:00を正式収録・監査#59）**

| tc | デバイス | 約束する未知 |
|---|---|---|
| 0:00 | Hook | 「$2,300でどうやって全財産を失い、しかも合法だったのか」 |
| 0:24 | 二人称賭け金 | 「あなたが同じ小切手を切り忘れたら」 |
| 1:50 | **債務slamペイオフ** | 「$2,300が一夜で$15,000に膨れた」 |
| 2:40 | **二人称脅威①＋OL1開** | 「これはあなたの家でも起こりえた／止められるのか」 |
| 4:50 | EquityBar reveal | **余剰$25,000の初出し**＋「差額はNothing」 |
| 6:10 | クリフ＋二人称② | 「裁判所は二度これを合法とした」 |
| 6:35 | OL物語入口 | 「Geraldineは一人ではなかった。別の家主が違う戦い方を試した」 |
| 9:00 | StateMap seed＋二人称③ | 「あなたの州は？」 |
| 9:40 | Hall決着 | 「その勝利は一角だけ—全国を変えるのは誰か」 |
| 11:00 | **OL3開（正式収録・#59）** | 「余剰没収を違憲とする根拠はどこにあるのか」 |
| 11:15 | **SplitLadder再フック（#57）** | 「郡はなぜ勝てると確信したのか—しかも“もっともな理由”があった」 |
| 12:20 | OL4開 | 「もっともらしい理屈の正体」 |
| 13:20 | **GovtArg崩壊ペイオフ** | 「もっともらしい理屈が崩れる瞬間」 |
| 15:00 | 史料intercut | 「答えは800年前・彼女の家に効く」 |
| 16:40 | 口頭弁論の対決 | 「9人の前で郡はどう答えたか」 |
| 18:15 | **9–0 slam** | 回収 |
| 18:40 | 二人称転回 | 「あなたの州も、つい最近まで合法だったかもしれない」 |
| 19:00 | ED＋EP34ティーズ | 空港の現金没収 |

**再フック最大隣接間隔（pass1 MINOR是正・実算値へ訂正）:** 全隣接差を実算した真の最大＝**6:35→9:00=2:25**（binding gap）、次点＝**2:40→4:50=2:10**、次いで16:40→18:15=1:35・13:20→15:00=1:40・11:15→12:20=1:05・9:40→11:00=1:20。**最大2:25 ≤ 2:50床内（充足）。** round4の「最大1:35」は自表と矛盾する誤記で撤回（次点1:40が最大1:35を上回る自己矛盾も是正）。**マージンが薄い2区間（6:35–9:00／2:40–4:50）は、間隔検査を voiceレンダ後の実チャンク時刻でも再実行**して実尺での床割れを検知する。

### 2.3 フック全文（0:00–0:08・核ネタバレなし・実語≤18・監査#52/#60＋pass3 MAJOR#13是正）
> **[VO:]** *A twenty-three-hundred-dollar bill took the home this woman had spent years paying off — and every cent was legal.*

**★pass3 MAJOR#13是正:round6の"took this woman's home"は"居住中の住処を追い出された"と誤読させ、CLM-0003（約2010年に安全懸念で高齢者コミュニティへ転居・コンドは空き家）と矛盾し立ち退きドラマを暗示していた。奪われたのは"住処"でなく"生涯かけて払い終えた資産/家"である事実に整合する言い回し（"the home this woman had spent years paying off"）へ調整。** 実語18（数字口語展開込み）→~155wpmで≈6.5–7.5s（8秒枠内）。$40,000/$25,000は出さずEquityBar 4:50で初出し。「legal」タグはHookのみ（ED重複は撤去・#50）。（VIS: 灯った窓→競売札→赤SEIZED。zoompunch/ForcefulCut。SFX: sub-hit1発＋紙裂け。音楽なし。）

### 2.4 OP全文（0:08–0:24・短縮・下ブリード・**0:24二人称賭け金を実文へ・pass3 MINOR#15**）
> **[VO:]** *A true story about a small debt, a locked door, and a government that took far more than it was owed — and about a right you may not know you have, until the day one late tax check could cost you yours.*

**★pass3 MINOR#15是正:0:24は計上する二人称脅威ビート（OP末尾）ゆえ、再フック・マップ0:24の約束「あなたが同じ小切手を切り忘れたら」を実VOに盛り込む必要があった。round6のOP VOは"a right you may not know you have"で終わり二人称賭け金が実文に不在だった→"until the day one late tax check could cost you yours"を追加して0:24グロスと一致させる（実語≈40）。** （VIS: PD標準BrandOpeningタイトルT2/サブT3。第1幕の窓の絵とAMB1を先行。禁止フレーズ辞書適用済。）

### 2.5 ED全文（19:00–20:00・トリコロン/二重legalタグ撤去・**尺埋め非VO末尾の撤回・監査aismell#50/pass2 MAJOR#24**）
> **[VO:]** *Geraldine Tyler never moved back into that condo. The Court could restore the principle, but not the ten years, or the front door, or the mornings that came in through her window. What it did restore was a limit — one the country had let slip. Surplus is only one way the state can take what is yours, and it is the narrowest. Next, we follow the money that never went to court at all: you owed no one a cent, broke no law, and they still emptied your bag at the airport — cash you earned, gone in a jetway, with no charge ever filed, and a long road to get any of it back. Subscribe, and watch what a single routine flight can cost.*

round3の三段トリコロン「It happened. It's legal. And it could happen to you.」と「legal」タグ二重を削除。**★非VO尺埋めの撤回（pass2 MAJOR#24）:** round5のED VO（約62語≒24s）は19:00–20:00の60秒枠のうち約36秒を非VOエンドカードで埋め、これは実質「20:00ちょうどに到達させるための尺合わせバラスト」＝オーナー厳命『装飾ループ/無音/尺合わせで尺を稼ぐのは0点』に抵触して読めた。よって**ED VOをearned coda（Geraldineが戻れなかった具体・回復されたのは"原則"という締め）＋EP34への実質的ティーズに増補し、非VOエンドカードは≤12秒に圧縮**。**★pass3 MAJOR#6/#25是正:ED VOは上記実文の実カウント＝約124語（round6の"約115語≒44s"は実文の過小カウント）＝48s@155wpm。** **20:00ちょうどへの固定は撤回**し、総尺は`check_runtime_band`(1,170–1,230s)内の自然終端に委ねる（ED増補分だけ他幕を薄く再ペーシングして帯内維持）。**19:00–20:00のED窓も`check_padding`（60秒窓 content-novelty＋分散床）の対象＝新規性ゼロの静的窓を作らない**ことをhardで通し、`review_pacing`のkeep/cut判定にED末尾窓を明示的に含める（装飾ループ/無音で埋まっていないことを確認）。（VIS: DoorPlacardStrip＋`NOT HER WINDOW — YOURS.`→StateMap緑化→BrandEndcard(≤12s)。個人回収の画は出さない＝象徴表現。）

### 2.6 各幕の首尾2文（本文インライン・審査可能・監査#49/#50/#53是正）
- **Act1冒頭（★CLM-0003整合・pass3 MAJOR#13是正＝居住中に奪われた誤認を排除）:** *For years, this one-bedroom condo had been Geraldine's whole world — the home she had paid off, where the mornings once came in through that window. In her eighties, worried about living alone, she moved to a senior community for her own safety. She never sold the condo. She kept it, empty and paid for, the way you keep a place still full of your life.* **（"奪われたのは住処でなく、生涯かけて払い終え思い出の残る空き家＝積み上げた資産"であることを早期に明確化。ED『never moved back into that condo』の伏線とも整合。）**
- **Act1末尾（劇的アイロニー装置"had no idea the clock was still running"撤去・客観描写へ・#50）:** *By the time anyone added it up, twenty-three hundred dollars had become fifteen thousand — and across town, in a county office, the paperwork to sell her home was already moving.*
- **Act2冒頭:** *The county did not send a lawyer to her door. It did not have to.*
- **Act2末尾:** *She asked for the difference back. The answer was a single word: nothing. And when she went to court, the court agreed — not once, but twice.*
- **Act3冒頭（"Two states away"撤去・匿名帰属・Hall勝訴に修正・#49/#53＋pass3 MINOR#16是正）:** *Geraldine was not the only one. In another state, another homeowner had already carried this same fight into a federal court — and won a first round the county had assumed it could not lose.* **（★pass3 MINOR#16是正:round6の"a first round the county never saw coming"は軽度のAI常套句で`verify_script_lint`固定辞書に未収録だった→"the county had assumed it could not lose"の具体表現へ言い換え、あわせて辞書に`never saw coming`/`no one saw coming`を追加＝§2.7。）**
- **Act3決着(9:40)＋末尾（Hall勝訴を史実準拠に・#49）:** *But that win came from one appeals court, binding just one corner of the country. It proved she was right. It did not yet protect anyone else. Only the justices in Washington could make that rule the law everywhere — and Geraldine's case was the one climbing that far. Because across the country, in less than a decade — by one legal foundation's count — thousands of families had lost not just their debt, but everything above it.*
  - **（pass2 MINOR是正・CLM-0017窓整合）:** VO文言を「in just seven years」からCLM-0017のデータ窓（2014–2021）と齟齬のない「in less than a decade」に変更（2014–2021を暦年で数えると8年で「seven years」と1年ずれるため）。CLM-0017側は期間表記を「2014–2021」に統一。grade-B・画面非焼込。
- **★Hall裏取り失敗時の代替プラン（pass1 MINOR是正）:** CLM-0021（第6巡回意見PDF一次裏取り）を§12 step2の**出荷前必須ゲート**とする。Hallは中盤で主役Geraldineが画面から退く人物スイッチ（既知の離脱リスク）であり、しかも grade B 依存ゆえ、**裏取り不能なら:** (1) Hallの実名/所在/金額を出さず `another homeowner, in federal court` の匿名象徴に留め、(2) Act3のHall尺（225s/580語のうちHall固有部）を縮め、その分を Geraldine 側の闘い（＝全国ルール化の伏線）と EquityTheftTally 全米ヒーローマップへ振り替える。Hallパートは常にGeraldineの闘いへ紐づく語りに徹し、9:40決着で即Geraldineへ回帰する現行設計を厳守。
- **Act4冒頭:** *The county walked into the Supreme Court confident. And to be fair to them, they had a reason to be.*
- **Act4末尾:** *It sounded almost reasonable. Until you realize the answer was written down eight hundred years ago, on a riverbank in England.*
- **Act5冒頭（マグナカルタ矮小化"a promise about debt"是正・ch.26残余原則を具体化・#51/#53）:** *In 1215, a cornered king sealed a promise: when the crown seized a dead man's goods to settle a debt, whatever was left over had to go back to his family. The residue belonged to them, not to the king. That principle outlived him by eight hundred years.*
- **Act5末尾（pass2 MAJOR是正・"more than a dozen"→"at least a dozen"でT9/§1.3と整合）:** *Nine justices. Not one dissent. The taxpayer must render unto Caesar what is Caesar's, but no more. Her home was gone. But the rule that took it was gone too — and in at least a dozen states, a warning still stands.* **（"more than a dozen"＝>12は点灯12ノード・T9・§1.3の"AT LEAST A DOZEN"と矛盾するため"at least a dozen"へ確定。字幕はこの[VO:]行を逐語源にするので caption==graphic==事実枠が一致する。）**

**台本全文＝** `episodes/PD-2026-033-tyler/03_script/script_final.v001.md`（**約3,050語（§8表と一致・設計/目標値＝実全文で再集計待ち・pass3 MINOR#7・ED増補反映）**・上記首尾＋Hook/OP/ED全文と一字一致・**Hall=勝訴で史実準拠**・二人称ビート②6:10/④12:00/⑤15:30を`[2P-THREAT]`アンカーで含む）。字幕はこの`[VO:]`行のみを逐語源（§5.1）。

### 2.7 「最低3回チェック」の真の機構化（**独立実行主体＋機械検証可能な実質証拠**・監査gaming#39）
台本は**著者と別の実行主体**による独立3レビューを経て改稿。**同一エージェントが体裁だけ整える"model_id文字列違い"では合格させない（#39）。** 各成果物に独立provenance（`reviewer_model_id`・`timestamp`・`input_sha256`）を刻む。**`verify_script_structure.py` が model_id 差だけでなく、各レビューの実質列挙の存在・網羅・スクリプトアンカー参照を機械検査し、欠落/不完全/未参照ならexit1:**
- `reviews/review_facts.md`：**Act3の各人間ビートを CLM-ID（0021含む）へ line-item 紐付け必須**。全 grade B 事実に`recheck`状態を明示。カバレッジ（Act3の全固有事実がCLM参照を持つか）を機械検査。**★pass3 MINOR#5:『固有名詞密度／出典なし断定』の点検を review_facts の名前のある line-item にする＝画面焼込/断定するVOの数値・固有名詞が grade-A ロケータを持つか、固有名詞詰め込み文がないかをレビュアが明示チェックし、step3★オーナー台本ロックの確認対象に含める（`verify_script_lint`の固有名詞密度フラグはadvisory・意味判断のhardは此処）。**
- `reviews/review_binge.md`：**導入した全人物ループ（Hall等）を列挙し各 close tc を明記**。未回収ループがあればexit1。
- `reviews/review_pacing.md`：**全60秒窓に keep/cut 判定をログ化**（13:00–18:00最優先）。各再フックの「新規の未知か既述再述か」二値判定を**§2.2再フック・マップの正典18本（実カウント：0:00/0:24/1:50/2:40/4:50/6:10/6:35/9:00/9:40/11:00/11:15/12:20/13:20/15:00/16:40/18:15/18:40/19:00＝18エントリ）**についてログ化（**pass2 MAJOR是正：round4/round5の"19本"は実テーブルと1本ずれ。二人称脅威ビート④12:00/⑤15:30は"二人称脅威ビート台帳"側で別途keep/cut管理し再フック表には数えない＝再フックは18本で確定**）。60秒窓(20窓/1200s)のkeep/cut判定は再フック本数と独立に全窓走らせ、窓数と台本尺の整合を機械検査。
- **独立性:** 3成果物の`reviewer_model_id`が本文著者と異なること＋上記列挙が実在スクリプトアンカーを参照することの両方を機械確認（文字列違いだけでは通さない）。
- `scripts/verify_script_structure.py`【WEAK（偽装耐性限界・完全な自動保証として引用しない）】検査項目：**(a) 二階建て回収検査（pass1 BLOCKING是正）:** 全OLに`[OLn-OPEN]`/`[OLn-CLOSE]`アンカーが存在しCLOSE>OPEN、かつ **主アークOL1/OL2/OL5は ED までに閉じる**（映画全体をまたぐ長距離ループを許容）／**短距離ループOL3/OL4は同幕/次幕内で閉じる**。未回収はexit1。**round4の一律「同幕/次幕内」制約は、正典どおりの主アーク（OL1開2:40→閉18:40等）を『未回収』と誤判定し正典台本を自らブロックする内部矛盾ゆえ撤回。** OL台帳（§2.2）の閉tcと整合。／**(b)** 再フック隣接≤2:50（binding gap=6:35→9:00の2:25）／**(c)** 二人称脅威無出現≤5:30（実体のある二人称VOビートのみ・§2.2台帳）／**(d)** 8秒フック→OP→5幕→ED／**(e)** new-information-per-scene（各シーン新規事実/人物/因果≥1）／**(f)** レビュー独立性＋実質列挙（上記）／**(g) 実タイムライン再検査:** これらの間隔検査は**紙155wpm tcで一次、voiceレンダ後は aligned narration_index の実チャンク時刻で再実行**し、実尺で床違反があれば出荷ブロック。
- **WEAK降格の含意:** verify_script_structure は構成/ループ/間隔の**機械的存在確認**は行うが、「二人称ビートが真に二人称か（三人称叙述の誤計上でないか）」「ループが物語として本当に閉じたか」の**意味判断は偽装しうる**。よって未回収ループ/AI臭/構成の**hard保証の本体は §12 step3 ★オーナー台本ロック（人手）**に置き、本ゲートはその補助（advisory＋機械的下限）とする。§13 axis2の「確定10」は本ゲートの緑だけでは与えず、オーナー台本ロック承認と併せて確定。
- `scripts/verify_script_lint.py`【実装済(wired)／要拡張（新規実装でなく既存linterの辞書/検出器の拡張・pass1 MAJOR是正）・カデンツ検出を追加】：
  - 固定辞書：`the answer will surprise you`／`people just like you`／`someone like her — maybe you`／`little did she know`／`in a shocking turn`／`you won't believe`／`the part that should scare you`／`this should scare you`／`here is the part where`。
  - **劇的アイロニー言い換え群（新設）:** `had no idea`／`unaware that`／`what she didn't know`／`the clock was still running`／`never suspected`。
  - **常套句（pass3 MINOR#16新設）:** `never saw coming`／`no one saw coming`／`saw it coming`（Act3冒頭の"the county never saw coming"型を機械検出）。
  - **カデンツ検出（新設）:** 短文3連（≤4語×3・末尾同型）を機械検出しレビュー必須フラグ。
  - **同一"legality reveal"タグ（新設）:** `legal`／`perfectly legal` の作品内2回以上を検出（Hook/EDの二重を弾く）。
  - **固有名詞密度フラグ（pass3 MINOR#5新設・"AI臭い＝固有名詞詰め込み"の機械下限）:** 1文あたりの固有名詞（人名/機関名/地名/事件名）数が閾値（既定>4/文）を超える文をレビュー必須フラグとして提示（hard exit1でなくadvisory＝人名列挙が事実上必要な引用文を誤爆しないため）。**hard backstopは`review_facts.md`の line-item『固有名詞密度／出典なし断定の点検』＋§12 step3★オーナー台本ロック**（下記review_facts列挙に本項目を明記）。
  - 全インラインVO（§2.3–2.6）をこの辞書＋検出器で機械検査。**赤フィクスチャ=既知AI臭文（round3のED三段/Act1アイロニー/`never saw coming`）でexit1することを実証。**

---

## §3. ビジュアル/モーション設計（数値予算・レンダ後実測を明示）

**確定基準:** `fps=30 / 1920×1080`（`remotion/src/brand.ts`）。基盤＝`CaseFilm.tsx`。専用図＝`remotion/src/components/tyler/`、再利用＝`motionkit/`。計画正典＝`04_scenes/scene_plan.v001.json`＋`remotion_plan.v001.json`。

### 3.0 確定予算値（depth余裕確保・ヒーロー時間分布床・監査#13/#15/#18）

| 指標 | 本話確定値 | 床(binding) | 算出根拠・監査対応 |
|---|---|---|---|
| 総尺 | **≈1,200s（band中央・20:00固定は撤回・pass3 MINOR#8）** | 1,170–1,230s | check_runtime_band実測（ヘッダ/§8と整合＝20:00は設計中央であり固定確定値ではない） |
| シーン数 | 40 | 34–40 | §3.4 |
| 総カット | 539 | ≥450 | §3.4 |
| 平均カット長 | 2.23s | ≈2.3s | 1,200÷539 |
| **depth処理率** | **44.2%（238/539・分母=全カット）** | **≥40%（分母=全カット・余裕4.2pt・#18）** | stills 252のうち depth付与=238（still比94.4%）。graphics/footageに深度なし。238は再生成でフラット化が数枚起きても40%を割らない予算 |
| 動くFigureBeats | 19種（distinct 18・§3.2） | ≥10・**各幕アクティブ≥4** | §3.2。時間分布床＋`motion_energy`実測（wired・再校正）＋§6.3 motion-reel人間承認で担保（bbox-localフローはadvisory参考のみ） |
| **ヒーロー面** | **6** | **≥3・かつ時間分布床（≥1ヒーロー/≤6分・いずれの幕もゼロ禁止）（#15）** | Act1=TaxDebtメーター／Act2=EquityBar三連／**Act3=EquityTheftTally全米ヒーローマップ（昇格）**／**Act4=GovtArgumentCard崩壊Trailヒーロー（昇格）**／Act5=MagnaCartaScroll・VoteTally 9–0 |
| 転換 | ForcefulCut(push/slide/zoompunch/whip) | — | 金縦スイープ・既定crossfade禁止 |
| motion_energy（**wired床＋新統計は要拡張・pass3 MINOR#24**） | **配線済み実床＝body within-shot mean≥12／全body p10≥9（この2つが実ゲートの実測統計）。本話の追加目標＝still限定p10≥17=⌈0.35×46.6⌉／全体分布median≥18／12秒窓median≥8** | wired床=mean≥12/p10≥9・追加=要拡張 | **pass3 MINOR#24是正:実ゲート`check_motion_energy`が計算するのは body within-shot MEAN・全body P10・per-12s窓MEANであり、"stills限定p10"も"median統計"も未計算＝これらは既存床の"校正/引上げ"でなく`measure_motion_energy`への新統計追加（要拡張）。⌈16.31⌉=17。round6の"引上げ再校正"表記は統計種別の相違（mean/p10↔median・全body↔stills限定）を秘していたため訂正。 |

### 3.1 レイヤー構成＋SceneBed輝度を最暗端・最暗隅・**breath最暗位相**から逆算（監査brightness#17/#21/#24）

**暗端側から逆算。四隅/5パーセンタイルに床。VignetteBreathの動的暗化を減衰式に取り込む。**

| Act | 用途 | 再確定グラデ(hex・**暗端引上げ**) | 素材YAVG(暗端→明端) | 合成後(bed+texture+grain・§3.7式) 暗端→明端 | 床判定 |
|---|---|---|---|---|---|
| Act1 | 家・温色 | `#3C4E64 → #52708E` | 62 → 82 | 52 → 68 | 暗端≥52/四隅≥46/明端≥52 |
| Act2–4 | 制度・冷色（**暗端引上げ#24**） | `#3C4D66 → #4E6485` | 62 → 79 | **52 → 65** | 暗端≥52/四隅≥46/図は明端側 |
| Act5 | 法史・羊皮紙金 | `#584C28 → #7A6C3C` | 60 → 80 | 50 → 66 | 暗端≥50/四隅≥46/明端≥52 |

- **減衰バジェット式（**bed_factor/grain確定・監査#22）:** `合成後 = source_YAVG × 0.92(grade) × (1−vignette_peak) × bed_factor × grain_factor`。
  - **`bed_factor = 1.00`**（L0/L1ベッド合成は **screen/additive に固定・multiply系禁止をhard化**。減光しないので=1.0）。
  - **`grain_factor = 0.98`**（FilmGrainを **screen/soft-light に固定・不透明度≤0.10**。平均輝度低下を≤2%に束縛）。
  - **`vignette_peak ≤ 0.12`（breath込み最悪値・#21）:** 静的ビネット ≤0.09、VignetteBreath振幅 ≤±0.03、**合算最暗位相で ≤0.12** を保証。暗ベッド幕（Act2–4／Act5夜）は**VignetteBreath振幅=0**（周期的暗化を作らない）。
  - `source_YAVG` は SceneBed=設計hex、Codex画像=**生成後実測YAVG**（仮定値禁止・#32）。
- **四隅/最暗域床（#17）:** 合成後の**5パーセンタイルYAVG≥46 かつ 固定4隅サンプル領域YAVG≥46**。単一mean/medianでなく min-region床を `check_image_cut_luma`（§3.7）に含める。
- **L0 背景(SceneBed):** 上表。`GridWarp`/`AuroraField` は -0.6EVベッド限定＋blend=screen/additive固定。
- **L1 中景:** `DepthParticles`(90–140)＋`LightRays`(弱・screen)。
- **L2 主役:** 専用図／再現stills（DepthStillパララックス）／実写。
- **L3 前景OL:** `SoftGlow`（additive）＋`FilmGrain`（screen・不透明度≤0.10）＋`VignetteBreath`（暗ベッド幕は振幅0）、`KineticCaptions`、`LowerThird`/`CitationLowerThird`。**下部暗化スクリム禁止（#25・§5.5）。**

### 3.2 専用の動く図 19種（リビール＋持続モーション・持続の**hard保証は`motion_energy`＋motion-reel人間承認**・監査animation#12/#14/#17／pass1 BLOCKING是正）

**サブピクセル呼吸は撤回。各図に方向性の実運動（パララックス/プレイヘッド走行/カウンタ加算/バーセトリング）を持たせる。**
- **紙芝居の hard 保証（pass1 BLOCKING是正・pass2で"実在しない"→"未配線"訂正）:** round4は「各図bbox内ローカル光学フロー実測ゲート（＝`check_motion_bbox_flow`）」を持続モーションの一次防御にしていたが、これは**`scripts/`に実在するが`check_final_acceptance.py`に0回参照＝未配線・現状走らない**（"実在しない"は誤り）。台帳ドロップ方針でhard引用しない。よって紙芝居の hard 保証は、**配線済みSOLIDの`motion_energy`（within-shot≥12／p10≥9・本話は§3.8で校正して引上げ）＋ §6.3 motion-reel（全19図網羅・非hero無作為抽出）のオーナー承認**に接地する。
- **per-figure bbox-localフローは advisory（参考）に降格。** hard blocker として引用しない。図が「実際に動いているか」の最終担保は motion-reel 人間確認（各図の持続モーション区間を編集して提示）に置く。参考指標として bbox中央値≥8px/frameを計測・提示はするが、これ単独では出荷可否を決めない。
- **リビール後ホールドのみのカードはアクティブFigureBeat床のカウント対象から除外（#17）。**

**ヒーロー面6（Trail=@remotion/motion-blur, lag0.35, layers6・時間分布床#15）:**
1. **TaxDebtメーター(`tax_debt_meter`)**(Act1・hero) — リング枠→桁マウント→桁ロール。中間実額出さず`$2,300`/`$15,000`のみ。**1:50 slam（#56）。持続＝針オービット8–12px＋桁ロール継続。**
2. **EquityBar**(Act2・hero) — 三連:灰"DEBT $15,000"→緑"SALE $40,000"slam→赤"SURPLUS $25,000"slam＋Trail。**余剰$25,000は4:50初出し。持続＝減衰オシレーション8–10px。**
3. **EquityTheftTally 全米ヒーローマップ**(Act3・**hero昇格#15**) — 走行カウンタ`$780,000,000+`＋全米ドット集積アニメ＋Trail。中盤7.5分のヒーロー空白を解消。`Est.—PLF`。**持続＝ドット連続集積＋カウンタ加算。**
4. **GovtArgumentCard崩壊**(Act4・**heroTrail昇格#15**) — 郡の最強論を積層カード→**13:20に構造破断＋Trail＋zoompunch崩壊**（感情ペイオフ）。**持続＝崩壊粒子ドリフト＋残響振動。**
5. **MagnaCartaScroll**(Act5・hero) — 巻物unfurl＋ラテン字stroke-trace→訳文TerminalType。**1215アイコン限定（Overplusは別チップ・#51）。持続＝連続パララックス8–12px＋インクtrace進行。**
6. **VoteTally 9–0**(Act5・hero) — **~18:15初オンスクリーン化**。弁論進行で席が方向性充填→9席同時発火＋単一hard impact。

**動く図（残り13・各持続 bbox中央値≥8px実運動・カードは恒常キャリア指定#17）:** 7.HomeSeizedIcon/SEIZED札 8.SurplusSplitDonut(county/town/school・元所有者ウェッジ欠落) 9.**StateMap（保持側点灯=PLF12州`Est.`／緑ペイオフ側=required-return・§1.3）** 10.FeltComparison 92/8(`Est.`・**恒常キャリア=加算カウンタ＋背景パララックス**) 11.CaseTimeline(**恒常キャリア=呼吸プレイヘッド走行**) 12.PropertyRedefine(キネティック取消線) 13.QuoteCard(Roberts/Gorsuch・**恒常キャリア=緩push＋背景パララックス**) 14.AuctionGavel(graphic-symbol ledgerで別カウント・§3.6) 15.DoorPlacardStrip(`NOT HER WINDOW — YOURS.`) 16.OralArgQuestionTally(**恒常キャリア=席方向性充填**) 17.SplitLadder(District→8th Cir→SCOTUS・**恒常キャリア=段上昇プレイヘッド**) 18.HallEquityLadder(Act3・Hall宅$1移転→約$308k転売→債務約$22,600の段・**史実準拠#49／★裏取り後のみ（CLM-0021をgrade-A化後）金額を焼込む・未裏取りは金額を出さず匿名象徴の段のみ（T10と同じ焼込禁止ゲート・pass1 MINOR是正）**・恒常キャリア=段展開＋数値ロール) 19.郵便受け物理カウンタ（Act1・**TaxDebtメーター#1の早期seedゆえ本来#1と同一コンポーネント。distinct図の実数は18種。19はカウント表示上の別ID扱いにとどめ、FigureBeat床（≥10・各幕≥4）は#19を#1へ畳んだ18種で充足する**・pass1 MINOR是正）。

> **HallEquityLadderの金額焼込は`verify_onscreen_text`（wired）のグリフ照合対象**にT10と同様に含め、CLM-0021がgrade-A化されるまで$1/$308k/$22,600のグリフ焼込をblockする。§3.2/§10のHall画像仕様も同caveatに従う。

**幕別アクティブFigureBeat床＝各幕≥4（カード除外規則適用後の実カウント・#15/#17）:** Act1=5・Act2=4・Act3=4・Act4=4・Act5=5。カウント対象は**方向性の実運動を持つ図**（リビール後ホールドのカードは非対象）で、**その実運動は`motion_energy`実測＋§6.3 motion-reel人手確認で担保**（bbox-localフローはadvisory参考のみ・hard判定に使わない）。

- **時間分布床（引き締め・#16）:** **各60秒窓にアクティブFigureBeat≥1、図間の最大無図区間≤60秒。窓辺リフレインstill連続露出≤25秒**、間に必ず方向性モーションのある図/実写を挟む。冒頭4分(0:24–3:40)を**motion-reel必須収録区間**。**この時間分布床は計画フラグでなくPOST-render実測（ローカルフロー≥床の区間が総尺に占める割合）で再定義し、preflightの計画レベル判定と二重化（#16）。**

> 朝の光の窓リフレイン＝一貫した匿名フィギュアの視覚アイデンティティ（同じシルエット/コート/手元/部屋）でAct1・Act3・Act5・EDに再登場。

### 3.3 再利用motionkit部品（二重実装禁止）
`VoteTally`・`NumberTicker`・`DonutReveal`・`StackedProportion`・`RegionHighlightMap`/`StateMap`・`QuoteCard`・`KineticCaptions`・`TerminalType`・`ActTitle`・`LowerThird`/`CitationLowerThird`・`Atmospherics`・`DepthParticles`/`LightRays`/`AuroraField`/`GridWarp`。新規（OralArgQuestionTally/SplitLadder/GovtArgumentCard/HallEquityLadder/EquityTheftTally hero版）は`components/tyler/`。

### 3.4 幕ごとのカット割付（`cut_plan`要約・全40行はJSON）

| 幕 | 尺帯 | シーン | 尺(s) | カット | 主図(アクティブ≥4) | 転換 |
|---|---|---|---|---|---|---|
| Hook | 0:00–0:08 | S001 | 8 | 4 | HomeSeizedIcon(zoompunch) | black→whip |
| OP | 0:08–0:24 | S002 | 16 | 7 | BrandOpening＋窓ブリード | zoompunch→push |
| Act1 | 0:24–3:40 | S003–S009 | 196 | 88 | TaxDebtメーター(1:50 slam)/郵便受けカウンタ/EquityBar seed/HomeSeized | push/slide、slam=zoompunch |
| Act2 | 3:40–6:35 | S010–S016 | 175 | 80 | AuctionGavel→EquityBar三連slam(4:50余剰初出)→SurplusSplitDonut→CaseTimeline短 | 各slam=ForcefulCut hit |
| Act3 | 6:35–10:20 | S017–S024 | 225 | 101 | Hall物語→HallEquityLadder→StateMap seed→**EquityTheftTally heroマップ**→FeltComparison（生統計≤45秒） | whip/push |
| Act4 | 10:20–14:20 | S025–S031 | 240 | 107 | SplitLadder→OralArgQuestionTally→**GovtArgumentCard崩壊hero**→VoteTally方向性→史料intercut | push、scroll intercut |
| Act5 | 14:20–19:00 | S032–S038 | 280 | 126 | MagnaCartaScroll(intercut)→CaseTimeline長→**VoteTally 9–0 slam(~18:15)**→Roberts×StateMap緑融合→DoorPlacard | zoompunch着弾＋温色解決 |
| ED | 19:00–20:00 | S039–S040 | 60 | 26 | EP34ティーズ→BrandEndcard | クリーンフェード |

**カット構成比(539・監査#13算術整合):** 再現/静止stills=**252**（うちdepth付与=238＝still比94.4%・残14はKen Burns/フラット）／グラフィック図=222（dpt-large深度なし）／実写footage=65（深度なし）。**depthカット総数=238＝全カット比44.2%（≥40%・余裕4.2pt）。** フラット2D Ken Burnsのみのカットは総カットの≤8%（≤43）にhard制限。**単一フレーム完全ホールドのシーンゼロ。**

### 3.5 depth計画（分母・内訳・実数一致＋自動是正・監査#13/#18）
- **分母=全カット539／閾値=≥40%／本話=238/539=44.2%。** stills 252のうち238（94.4%）にdpt-large深度、graphics222・footage65は深度対象外。
- `build_case_film_assets.py` が計画JSONの`depth:true`実数を数え、**内訳合計(238)と一致しない計画を出力前exit1**。深度欠落は出力前hard-fail。
- **自動是正（余裕確保・#18／pass1 MINOR是正）:** POST-renderで depth カットがフラット再生成へ差し替わり40%接近した場合、**stillsバッファから未depthのstillカットをdpt-large深度付与へ昇格**して40%を下回らせない（stills 252のうちdepth付与238＝残14のslack stillsを昇格対象にする）。マージンは**stills由来のみで再計算**する。**round4の「graphics適格カットへdpt-large深度を自動付与」フォールバックは撤回:** graphics(222)は合成2Dデータ図で depth対象外（§3.5冒頭）であり、平坦な合成グラフィックへの単眼dpt-largeは有意なパララックスを生まず（no-op/アーティファクト）depth分母ロジックとも矛盾する。graphics に擬似奥行きを与えたい場合は**dpt-largeでなくレイヤ・パララックスとして明示定義**し、depth分母には算入しない。長尺WebGL/depthは`--concurrency=4`。DepthStill振幅=前後レイヤ差±(50–80)px、ズーム1.0→1.06（§3.8の`motion_energy`床充足に必要な実px/frameへ引上げた`DepthStillHi`を既定採用）。

### 3.6 実写footage＋多様性＋話またぎ非重複（監査footage#5–#11・gaming#36–#38）

- **棚抽出コマンドの実挙動是正（#5）:** `select_factory_assets.py` の `--theme` はカンマ複数不可の単一完全一致。テーマ個別実行してマージ。**legal_court は汎用象徴subtypeが大半（監査#7）ゆえ主レーンから外し、非汎用subtypeを名指し抽出:**
  ```
  for t in property_home documents_paper ; do \
    python scripts/select_factory_assets.py --theme "$t" --kind video --json ; done > 05_visuals/pool.jsonl
  # legal_court は非汎用subtypeのみ個別抽出（補助）
  for s in courtroom_interior federal_building government_building record_office ; do \
    python scripts/select_factory_assets.py --theme legal_court --subtype "$s" --kind video --json ; done >> 05_visuals/pool.jsonl
  ```
- **供給計画の主レーン確定（監査footage#7）:** need=26（=render_dur//45）＋余剰は **home/自治体レーン（`property_home`＋`documents_paper`＋郡庁舎系non-generic）だけで満たす**供給計画。legal_court は汎用象徴除外後の生存が薄いため補助に降格。**各subtypeのQC生存見積を`asset_selection.v001.json`に subtype別本数で記載**（架空の候補数を確定値にしない）。
- **フォールバックのレーン排他検証（監査footage#8）:** EP33棚不足フォールバック順＝(1)`documents_paper`（納税通知/記録）→(2)`property_home`の`suburb/main_street/rural_road`→(3)Codex 4K再現。**`urban_night`（airport/city/subway/parking含む）はEP34主レーンを先食いしcatalog指紋でEP34を弾くため除外（#8）。** フォールバックthemeも3話レーン分離表に照らし事前排他検証。
- **Codex静止画は factory-clip供給床の分母に数えない（監査footage#9）:** `check_factory_used`／`check_footage_utilization` は remotion/public/<slug>/factory/ 配下の**実映像クリップ数**を数える。**供給床（QC生存distinct clip ≥32・pass1整合）は必ず実映像クリップで満たす**（近縁theme個別抽出＋商用OK無料API追加取得を§12 step7に明記）。Codex静止画はimages側で別カウント、footage枠(65カット)を静止画で埋めない。
- **多様性ゲート【実装済（実定数）・単一話専用・帰属訂正#11】:** `check_footage_diversity` は`<slug>_film.json`の**全cuts src（グラフィック・still含む）**をCounterし distinct≥0.40／再利用≤4／`FOOTAGE_GENERIC_PAT=scale|gavel|hourglass|clock|stopwatch|balance` マッチ≤2。**round3の「footage src限定」記述は誤りで、全cut srcが対象と訂正。命名衝突除去の禁止トークンを FOOTAGE_GENERIC_PAT 全体（gavel/hourglass/stopwatch含む）と一致させる。**
- **話またぎ非重複ゲート【実装済(wired)＝`check_arc_nonrepeat`本体はSOLID配線済／ただしアーク共有除外は"実装済拡張"でなく真に新規＝要実装・pass2 BLOCKING是正】`scripts/check_arc_nonrepeat.py`:**
  - **★実配線ゲートの実挙動に接地（pass2 BLOCKING是正・最重要）:** 配線済`check_arc_nonrepeat.evaluate(epdir, *, data_dir, public_dir)` は **`catalog_fingerprints.json` を一切読まない**。比較ユニバースは**他話の `*_film.json` の cut `src` basename ＋ `remotion/public/<slug>/` 配下メディア**から構築し、**本話が同じ source basename を cut に置くと交差でHARD FAIL**する（除外/allowlist/アーク共有の引数も概念も持たない）。よって round4/round5の「`catalog_fingerprints`に記録する/しないで交差判定を制御する」設計は**実ゲートに対して no-op（＝実行不能な機構引用）**であり撤回する。**指紋台帳（asset_id集合）は本ゲートの入力ではなく、三部作の事前クリップ分配を人手/preflightで管理する"計画台帳"にすぎない**と正直に格下げする。
  - **★三部作の希少法廷/庁舎素材の分配＝二択で明示スコープ化（pass2 BLOCKING是正）:** 3話（EP33家・EP34空港/現金・EP35銀行）は法廷/連邦庁舎素材を共通に要するが、実ゲートは basename 交差=0 を無条件hardで強制するため、header 行5「EP34/35 と素材完全分離」と実ゲートは**完全分離を要求する**。二択のどちらかを取る:
    - **(A・既定＝実ゲートに素直):** EP33/34/35 は**法廷/庁舎素材も別クリップにして完全分離**（共有しない。header完全分離を守る）。棚が**法廷/庁舎の QC生存 distinct clip を 3話分（≥3×）**保持するかを EP33 消費前に §12 step7 で先に検証し、不足なら近縁theme再抽出＋**Codex 4K再現**で各話別ショットに分ける。既存gateの basename 交差=0 がそのまま守りになる（新規実装不要）。
    - **(B・共有したい場合＝真に新規の要実装):** identical な institutional クリップを3話で共有したいなら、`check_arc_nonrepeat.evaluate()` に **arc-shared allowlist 引数（除外 basename 集合）を新規実装**し、**共有IDは交差判定から除外／事件固有IDの再利用はFAIL**を赤緑実証してから配線する。これは§14-3の**『要実装（真に新規）』に列挙する作業**であり、round5の「要拡張（軽微）」表記は過小ゆえ訂正。EP33出荷では既定(A)を採り、(B)は別ワークストリーム。
  - **指紋の頑健化（(B)採用時のみ）:** allowlist実装時は、グレード/ビネット/オーバーレイで basename が散らないよう **film.json cut src の `/factory/<id>` 正規化＋合成前ソースフレームpHash≤6** を交差キーに併用する。
  - **catalog完全性の前提条件（#38・計画台帳側）:** 事前分配の計画台帳（`catalog_fingerprints.json`）は**既定本数/話数未満で warn** するが、これは**実ゲートの合否入力ではない**（実ゲートは他話 film.json を直接読む）。空集合比較の偽緑封鎖は、実ゲートが他話 film.json を実際に列挙できているか（比較対象話数のログ）で確認する。
  - `check_arc_nonrepeat` は `check_final_acceptance`/`preflight_owner_review` へ既配線（SOLID）。**赤フィクスチャ=他話 film.json に在る cut src basename を1件本話に混入した合成でexit1することを実証（#32）。(B)採用時は追加で「共有allowlist ID は通す/事件固有IDの再利用は落とす」赤緑両実証。**
  - **EP33はアーク第1章だが、既公開群の film.json を横断比較するのでvacuousでない（axis9に正直明記）。**
- **選定footageの実使用率＋選定広さ床【実装済(wired)／要拡張（`check_footage_utilization`は`check_final_acceptance.py`に配線済＝SOLID・pass1 MAJOR是正。突合キー/選定広さの拡張のみ）・監査footage#8/gaming#36】`scripts/check_footage_utilization.py`:**
  - 旧`check_factory_used`は staged n≥26 と cutlistに`/factory/`1件で緑になる穴があったため、実配置突合へ拡張。
  - **突合キー確定（#12）:** `asset_selection.v001.json` の各footage候補に**最終src相対パス（asset_id→パスの決定的写像）を必須フィールド**で持たせ、film.json cuts と**正規化キー（小文字/拡張子除去/区切り統一）**で突合。
  - **選定広さ床（分母操作封鎖・#36）:** `asset_selection` は **≥39 distinct候補（=26×1.5）を≥3テーマ**にわたり保持。かつ**最終film.jsonに実配置された distinct source clip ≥32**（過少選定で100%利用を偽装させない）。
  - **使用率（単一binding床へ整理・pass3 MINOR#10是正）:** 選定候補の**未使用candidate≤20%（＝使用率≥80%）を唯一の拘束床**とする。round6の「使用率≥70%・未使用≤20%」は同一candidate母集団に対して"使用≥80%"と"使用≥70%"の二重表記で、≥80%が≥70%を含意し混乱を招くため≥70%数値は撤回（未使用≤20%へ一本化）。未達exit1。§6.1/§11#4へ配線。**赤フィクスチャ=候補50本中20本のみ配置した計画（使用率40%）でexit1を実証。**
  - **★供給床の整合（dead-zone解消・pass1 MAJOR是正）:** 本ゲートは**実配置distinct source clip ≥32**を要求するのに対し、§3.6末尾の preflight/供給床は「最小生存footage下限=26」だった。**生存distinct clip が [26,31] に落ちると preflight は通る（≥26）が本POST-render utilizationゲートが落ちる（<32）デッドゾーン**が生じる。よって**preflight/供給床を utilization 実配置床に引上げて統一＝「QC生存distinct clip ≥32 かつ 選定候補≥39/≥3テーマ、下回れば preflight でFAIL」**とし、[26,31]のギャップを消す（26床は撤回）。
- **棚ラベル破損の供給計画（#9／pass1 MAJOR整合）:** QC後生存footageが供給床＋余剰を満たさない場合の決定論的フォールバック（上記レーン排他順）＋**最小生存footage下限=QC生存distinct clip ≥32（utilization実配置床と統一・旧26床は撤回・[26,31]デッドゾーン解消）を数値床にしてpreflightでFAIL**。need算出（render_dur//45≒26）は下限でなく参考、実際の供給床は32。
- **グラフィック象徴 ledger【要実装・自己申告→機械集計に是正・監査footage#10/#11】:** round3の手書きJSON自己申告を撤回。**`preflight_render_gate` が film.json 全cut src の汎用トークン一致を機械集計**し、**(a)汎用象徴の種類≤2 かつ (b)各汎用象徴の総登場回数≤3** の二本立てhard化（反復露出を縛る）。本話はAuctionGavel 1種のみ＝graphic側1/2・登場回数≤3。**`tax_debt_meter`は誂えデータ図ゆえsrc命名に generic トークンを含めず非汎用扱い（意味的除外を命名規則で担保）。**
- **命名衝突除去（#11）:** 図/stillのsrcパスに `clock/scale/balance/gavel/hourglass/stopwatch` トークンを含めない（FOOTAGE_GENERIC_PAT全体と一致）。AuctionGavel graphic の src 命名と使用回数を`FOOTAGE_GENERIC_MAX_USES`に照らし事前検証。
- **目視QC(必須):** `build_footage_contact_sheet.py` ラベル付きコンタクトシートを初回レンダ前に目視。**`asset_selection.v001.json`の「不足0」はQC生存クリップ数で再計算**、不足時は§12 step7再抽出＋フォールバックループ。

### 3.7 明るさ計画（測定段＝レンダ後・per-cut全539・監査brightness#18/#19/#20/#23）
- グレード`GRADE=0.92`／footage`0.9`／ビネット静的≤0.09＋breath≤±0.03（暗ベッド幕は0）。§3.1減衰式（bed_factor=1.0/grain_factor=0.98）で暗端/四隅/breath最暗位相から逆算済。
- **本編輝度【実装済（実定数）・再校正の実装粒度をpass2 MAJOR是正・#23】`check_body_luma`:** 現行 median YAVG≥48・暗フレーム率(YAVG<`BODY_LUMA_DARK_YAVG`=30.0)≤`BODY_LUMA_DARK_FRAC_MAX`=0.22。20分で最大264sの暗フレームを許容しEP31 FAIL水準ゆえ`YAVG`を38.0・`FRAC`を0.08へ引き上げたい。**★実装粒度の是正（pass2 MAJOR）:`BODY_LUMA_DARK_YAVG`/`BODY_LUMA_DARK_FRAC_MAX` は `check_final_acceptance.py` のモジュール定数（L229-230）で、`check_body_luma(path,dur,epdir)` は episode 引数から閾値を読まない。よって「本話だけ38/0.08に校正」は現状の機構では不可能**（定数を書き換えれば標準11.5–12分話や過去話の再検査にも同時適用される）。二択で明示する:(1)`manifest.json` に `luma_floor_override`（YAVG/FRAC）フィールドを追加し `check_body_luma` がそれを読むよう拡張＝**これ自体が要実装作業**（本話だけ厳格化・過去話不変）／(2)グローバル定数を恒久的に 38/0.08 へ引き上げ、**全話（過去受領書の再現性含む）に適用する影響を §7/§14 に記載して選択**。invariant15上「より厳しく」は許容だが、per-episodeか全話かを未指定のまま「本話校正」とは書かない。**グローバル中央値ゆえ「一部が真っ暗」は捕えない→下記per-cutで別途。body_luma単独では出荷可としない（#23）。**
- **per-image/per-figure/四隅輝度ゲート【実装済(wired)／要拡張（`check_image_cut_luma`は`check_final_acceptance.py`に配線済＝SOLID・pass1 MAJOR是正。全539スコープ/四隅/breath位相/スクリム検査への拡張・閾値校正のみ）・POST-render・#17/#18/#20】`scripts/check_image_cut_luma.py`:** **測定段をレンダ後の最終MP4/PNG連番に固定**（preflightは書き出し前で最終合成フレーム不在＝#18）。**スコープ=全539カット（stills238＋graphics222＋footage65＋SceneBed各シーン）（#20是正・round3の「216+68+bed」限定は撤回）。** 各カットで **(a)カット別YAVG≥52、(b)図/被写体bbox領域YAVG≥46、(c)5パーセンタイル/四隅YAVG≥46、(d)連続暗カット最大連鎖長≤6s、(e)VignetteBreath最暗位相フレームを測定対象に固定（#21）**。1カットでも割ればexit1→再レンダ/再生成（再試行上限つき）。**footageは素材特性別床（カット別≥50かつ主要領域≥46）、達成不能な暗footageは採用不可→近縁theme再抽出/Codex再現に置換（#20）。** preflightは計画レベル（枚数/解像度/深度フラグ数）のみ担当。**赤フィクスチャ=中央明・四隅潰れの合成カット1枚でexit1を実証（#32）。**
- **低キー許容の再設計（EP31の穴を再開しない・#19）:** `check_body_luma`の分母から暗カットを除外しない。`05_visuals/lowkey_whitelist.json`は3条件全課す：**(1)** whitelist低キー総尺≤6%（≤72s）・最大連続暗連鎖≤6s、**(2)** 各whitelistカットは被写体bbox YAVG≥46の正の床、**(3)** グローバル暗フレーム率ゲート(`check_body_luma`)は全フレーム100%に常時走らせる。

### 3.8 ForcefulCut転換規律＋**motion_energy床の再校正（配線済みSOLIDゲートの引上げ・pass1 BLOCKING是正）**
- 全40シーン境界=`ForcefulCut`。`WipeTransition`(金縦スイープ)・既定crossfade禁止。図内slamはzoompunch。
- 周回/lissajous淡い光・単調等速グローを単独モーション源にすることを禁止。`AuroraField`/`LightRays`はL0/L1ベッド限定（screen）。各シーンに正の方向性モーション（パララックス/プレイヘッド/カウンタ加算/バーセトリング）を1つ以上。
- **motion_energy＝配線済みwired床（mean≥12/p10≥9）＋新統計の要拡張（pass3 MINOR#24是正・"校正"表記の訂正）:** `motion_energy`（`measure_motion_energy`/`check_motion_energy`）は`check_final_acceptance.py`に**配線済み（SOLID）**で、**実ゲートが実測する統計＝body within-shot MEAN≥12／全body P10≥9／per-12s窓 MEAN≥8**。本話の下記床のうち **(1)still限定p10 と (2)median統計 は実ゲートが計算していない別統計＝"既存床の校正/引上げ"ではなく`measure_motion_energy`への新統計追加（要拡張）** であることを正直ラベルする（round6の「引上げ再校正」表記は統計種別の相違＝mean/p10↔median・全body↔stills限定 を秘していたため撤回）。基準アンカー＝MotionSample≈46.6（良）／紙芝居≈3.5（悪）:
  1. **still限定 p10 床 = ⌈0.35 × 46.6⌉ = ⌈16.31⌉ = 17（新統計・要拡張＝現ゲートは"全body p10"しか出さないため stills サブセットの p10 計算を`measure_motion_energy`に追加する）**。現DepthStillが17に届かなければ**振幅/zoomを引上げた`DepthStillHi`で17達成まで上げる**（床を下げてstillsを認証しない）。§3.0/§6.1/§13の全参照を**17**に統一。
  2. **全体分布 median ≥ 18（新統計・要拡張＝現ゲートは mean を出すため median 追加が要る）**、**12秒窓ごとの実フロー中央値 ≥ 8（新統計・現ゲートは per-12s MEAN）**。実ゲートの現行 wired 統計へ写像する場合は「全body p10≥9＋per-12s MEAN≥8」をそのまま使い、17/18/median は override＋新統計拡張後に有効化。
  3. **within-shot=カット±8フレーム除外**（切替スパイクの誤合格封鎖）。
  4. **未拡張時の実効挙動（正直開示）:** 上記新統計（still-p10≥17・median≥18）は`measure_motion_energy`の統計追加＋per-episode override（下記(5)）を実装するまで走らない。**未実装のまま出荷する場合、実効の紙芝居床は台帳既定＝body mean≥12／全body p10≥9 で判定される**（本話の見ごたえ目標17/18には未達＝§13 axis4は確定10にしない・§13.2実効点でも新統計は計上しない）。
  5. **★実装粒度の是正（pass2 MAJOR）:`MOTION_ENERGY_BODY_MEAN_MIN`/`MOTION_ENERGY_P10_MIN`/`MOTION_ENERGY_SEGMENT_MEAN_MIN` は `check_final_acceptance.py` のモジュール定数（L134-148）で、`check_motion_energy(path,dur,epdir)` は episode 引数から閾値を読まない。よって「本話だけ 17/18/8 に引き上げる」は body_luma と同じく現状不可能。** body_luma と同一方針で二択する:(1)`manifest.json` に `motion_floor_override`（p10/median/segment）を追加し `check_motion_energy` がそれを読むよう拡張＝**要実装作業**（本話のみ厳格化）／(2)グローバル定数を恒久引上げし全話適用の影響を §7/§14 に記載。still-p10≥17 等を「本話校正」と書く場合は override 実装が前提。
- **motion-variety検査【motion_energyの補助指標・アンカー接地・#16/#19】:** ショット内フローベクトルの**方向ヒストグラムのエントロピー≥1.5 bit かつ 時間軸フロー大きさのCV≥0.25**。**この2閾値もMotionSample（良・多方向/変動大）vs 紙芝居（悪・一様/静止）の実測分離で凍結前に接地**（motion_energyと同基準・#19の自己矛盾是正）。motion_energyの拡張指標として配線し、単一の新ゲートとしては提示しない。
- **per-figure bbox-localフロー＝advisory（参考）に降格（pass1 BLOCKING是正・pass2で"実在しない"→"未配線"訂正）:** round4は各図bbox内ローカルフローゲート（＝`check_motion_bbox_flow`）を各図持続の**hard exit1**にしていたが、これは**`scripts/`に実在するが`check_final_acceptance.py`に0回参照＝未配線・現状走らない**（"実在しない"は誤り）。台帳ドロップ方針でhard引用しない。よって各図が「実際に動いているか」の**hard保証は`motion_energy`（上記校正）＋§6.3 motion-reel人間承認**に置き、bbox中央値≥8px/frameは**計測・提示する参考値**にとどめ出荷可否を決めない。
- **持続px床の統一（#19）:** 設計全体で持続実運動の**目標**下限を **≥8 px/frame** に統一。ヒーロー図は目標8–12px。これは advisory 目標であり hard gate は motion_energy。
- **赤フィクスチャ（#32/#33）:** 緩慢一様パン（entropy低）でmotion-variety拡張がexit1、紙芝居フリーズ分布で再校正後motion_energy（p10<17/median<18）がexit1することを実証。
- 再校正床は実測後にscene_plan/check_final_acceptanceへ書込み、§13 axis4はmotion-reel承認＋motion_energy実測校正で確定。

### 3.9 見切れ／疎な図／暗い図の禁止機構
- **lowerthird左見切れ:** 字幕セーフ矩形 x∈[160,1760]＋`safeInset=96`。bbox外はpreflight FAIL。最大2行。
- **疎な図禁止:** マップ/分布図の最低ノード数を機械チェック。**StateMap保持側点灯=12（≥12）。** ノード<6の図は不採用。
- **暗い図背景禁止:** 図背景YAVG≥46（§3.1で図は明端側・§3.7 per-figureゲート・POST-render全539）。

### 3.10 レンダ前/レンダ後の役割分離
- **preflight_render_gate.py（レンダ前・計画レベル）の列挙チェックリスト（★pass3 MINOR#3是正で(i)(j)を明示追加）:** (a)全参照S0NN存在＋≥3840px／(b)深度フラグ数=238一致／(c)FigureBeats≥10かつ各幕アクティブ≥4／(d)時間分布床（60秒窓≥1図・無図≤60秒）／(e)ヒーロー面≥3かつヒーロー時間分布床／(f)平均カット2.0–2.6s／(g)全span束縛／(h)グラフィック象徴 種類≤2・各≤3回／**(i) 疎な図禁止＝全マップ/分布図の描画ノード数≥6 かつ StateMap点灯ノード数≥12（<6のマップ/2ノードマップはexit1・§3.9の散文をpreflight enumeratedチェックへ配線）／(j) 字幕/lowerthird セーフ矩形＝全キャプション/lower-third bbox が x∈[160,1760] 内・`safeInset=96`・≤2行（左見切れ/範囲外はexit1・§3.9の散文をpreflight enumeratedチェックへ配線）**。未達exit1。**赤フィクスチャ=(i)2ノードのマップ／(j)x=160を越えて見切れるlower-third でそれぞれexit1を実証（round6は§3.9が散文で約束するのみでpreflight列挙に無く未強制だった）。**
- **POST-render acceptance（実バイト測定）:** `check_image_cut_luma`（全539・per-image/per-figure/四隅/breath最暗位相）／`motion_energy`実測（wired床mean≥12/p10≥9＋要拡張新統計）＋motion-variety（bbox-localフローはadvisory参考のみ・hard判定に使わない）／時間分布POST-render実測／`check_arc_nonrepeat`（basename交差0）／`check_footage_utilization`（未使用≤20%＋選定広さ）／`check_sound_layers`（distinct SFX≥12/beds≥4/mux sha・wired）／`check_padding`／`caption_sync`＋`check_caption_format`（機能語行末0の受領側再検査含む・要拡張）＋`check_longform_drift`。**WEAK（`verify_sfx_manifest`/`verify_script_structure`/`check_ending_sound`）は hard 列でなく advisory とし、最終保証は §6.2 人間試聴/オーナー承認。** 未達は再レンダ/再生成。
- 続いて**motion-reel（§6.3・全19図網羅＋非hero無作為抽出）**をオーナー提示。

---

## §4. 音設計（4層・高密度志向・自己申告を実測化・監査sound#22–#31/gaming#34/#43）

最終尺≈1,200s・最終**I=-14 LUFS / TP=-1.0 dBTP**。VOアンカーだが痩せさせない。装飾フィラーSFX恒久禁止。

### 4.1 4層のラウドネス・ターゲット（実測は`check_sound_layers`(wired)＋人間試聴backstop・pass1 BLOCKING是正）

| 層 | VO発話中 | VO無し/間 | 備考 |
|---|---|---|---|
| L1 VO | short-term -15〜-14 LUFS、瞬時ピーク≤-3dBFS | — | de-esser5–8kHz、HPF80Hz |
| L2 Music | -22〜-20 LUFS | -18〜-16 LUFS | EQくぼみ(-2dB)で明瞭度確保 |
| L3 Ambience | -32〜-29 LUFS | -27〜-25 LUFS | 幕ごと真の別ベッド base6 |
| L4 SFX | インパクト瞬時-12〜-8 dBTP、連続テクスチャ-22〜-20 | 同左 | base distinct20 |

- **🗑`check_stem_loudness` の引用を全撤回（pass1 BLOCKING・pass2で"実在しない"を"未配線"に事実訂正）:** round4はVO区間の相対音量（Music>-24/Amb>-30）を`check_stem_loudness.py`で塞いでいた。**pass2事実訂正:`check_stem_loudness.py`は`scripts/`に実在する。ただし`check_final_acceptance.py`の`_ext_gate`ループに未配線（0回参照）＝現状の受領ゲートでは走らず自動保証に効かない。**「実在しない」は誤りで「実在するが未配線・本アークでは配線しない方針」と訂正する。実ゲート台帳のドロップ方針に従い**hard自動保証としては引用しない**（配線可否はEP33出荷の臨界パス外・別ワークストリーム）。VO区間の相対音量は下記の人間試聴backstopで担保。
- **音の自動保証の本体＝配線済みSOLIDの`check_sound_layers`（pass2 BLOCKING是正・能力を実挙動に接地）:** 4層音の**現に走るhard自動ゲートは`check_sound_layers`（`check_final_acceptance.py` L1086に配線済＝SOLID）**。ただしその実挙動は二部構成で、**PART1＝レンダ音声の onset密度＋ambience帯域(500Hz HP/帯域dB)を波形で実測**、**PART2＝`_sound_mix_binding` が `06_audio/audio_provenance` の `layers.sfx.distinct_files`／`density_gate.ambience_distinct_beds` を読み、`audio_mix_sha256` で最終muxに束縛**する。したがって **distinct SFX≥12／beds≥4 は provenance JSONの自己申告値＋mux sha束縛（＝孤児mix・未muxプランを弾く）であって、混合波形からSFXイベント個数を検出しているのではない**（波形実測されるのは onset密度＋ambience帯域のみ）。round4の「provenance JSONを読むだけ」を"誤り"として撤回し「実mix解析でdistinct SFXを判定」と書いたのは過大主張ゆえ、本稿で再訂正する。本話はこの床（distinct SFX≥12/beds≥4・自己申告＋sha束縛）を満たしつつ本話目標（SFX distinct20/beds6）を上回るが、**SFXが最終mixで実際に可聴/区別可能かの保証は §6.2 音5本試聴（人間backstop）が唯一のhard保証**。
- **VO区間の相対音量・アンビの薄さは人間試聴backstopで担保（正直開示）:** VO発話区間でMusic/Ambが痩せていないか、アンビの中高域空気感が薄くないかの**自動保証は現状の実ゲートにはない**。よって §6.2 `preflight_owner_review` の**音5本試聴＋stem実測LUFS/TP/LRA提示（人手）**をhard backstopとし、「自動で保証される」とは主張しない。参考として stem WAV から ebur128 short-term 系列と Amb の 40–160Hz/1–8kHz 2帯レベルを**計測・提示**するが、これは advisory であり出荷可否は人間承認が決める。
- バス: VO/Music/Amb/SFX→busMaster。busMasterでのみ最終loudnorm。

### 4.2 劇伴(L2)6ベッド＋Bookend（music密度の自動床は無い＝人間試聴backstop・pass2 MINOR是正）
MB0 title→MB1 quiet-life(Act1)→MB2 the machine(Act2)→MB3 the others(Act3・Hall物語ピアノ独奏)→MB4 the argument(Act4)→MB5 vindication(Act5・古楽→長調解決)→**MB-END(固定・オンビートクリーンフェード)**。
- **🗑`check_music_coverage` の引用を全撤回（pass1 BLOCKING・pass2で"実在しない"を"未配線"に事実訂正）:** round4は「中盤music drop/薄い音」を`check_music_coverage.py`（music active≥85%/無音≤8s）で塞いでいた。**pass2事実訂正:`check_music_coverage.py`は`scripts/`に実在し `evaluate(epdir, render)` を実装済み（＝`_ext_gate`の標準コントラクト形）だが、`check_final_acceptance.py`に未配線（0回参照）＝現状の受領では走らない。**「実在しない」は誤りで「実在するが未配線・本アークでは配線しない方針」と訂正する。実ゲート台帳のドロップ方針に従い自動保証として引用しない（配線可否はEP33臨界パス外の別ワークストリーム。将来配線するなら赤フィクスチャ＋緑実証を要する）。
- **music"存在"は自動床あり／music"カバレッジ時系列の質"は自動床なし（pass3 MINOR#23是正）:** ★round6の「劇伴ベッドが実mixに存在するか…を自動で保証する実ゲートは存在しない」は誤り。配線済`check_sound_layers`の`_sound_mix_binding`（L1070-1071）は`audio_provenance`の`layers.music`トラック数を読み、**`music_tracks < SOUND_PROV_MIN_MUSIC(=1)`でhard問題を出す＝「連続music層が最低1本存在する」ことは provenance自己申告＋`audio_mix_sha256`束縛のhard床として現にenforceされる**（孤児/未muxを弾く）。よって**music"存在"（≥1トラック）は自動保証される**。ただし`beds≥4`は別物で**`ambience_distinct_beds`（アンビ別ベッド数）を数える床であって music ベッド数ではない**（L1059）。**自動床が無いのは「中盤music dropなどカバレッジ時系列の質」**であり、これは §6.2 の**音5本試聴＋music stem のアクティブ率タイムライン提示（人手）**をhard backstopとする（music stemのアクティブ率/最大無音区間は計測・提示するが advisory）。「beds≥4がmusic密度を担保」とは書かない。
- **正直化（#28）:** 劇伴はfactory棚（ラベル破損既知）既製ベッド選定で専属スコアではない。質/一体感は**6ベッドのラベル付き試聴QCをオーナーゲート化**（§6.2）。§13 axis5満点根拠から「専属スコア級の一体感」を外す。

### 4.3 章別アンビエンス(L3) base distinct6・**distinct実測化（監査sound#29）**
AMB0 cold/vacant(Hook)／AMB1 the empty home(Act1)／AMB2 courthouse corridor(Act2)／AMB3 the wider country(Act3)／AMB4 argument-room(Act4)／AMB5 the vindication(Act5)／AMB-END(固定)。
- **distinct閾値＋実測の帰属（pass1整合・pass2で"beds=ambience"を明記）:** アンビ**別ベッド数**が provenance に申告され最終muxに束縛されているかの**自動床は配線済み`check_sound_layers`の `ambience_distinct_beds`≥4（wired・本話6・＝この床の実体はアンビ別ベッド数）**。ただしこれは provenance自己申告＋mux sha束縛であって波形からのベッド分離実測ではない（§4.1）。round4の「相互相関係数<0.6 かつ 素材源SHA相異」の分離度実測は`verify_sfx_manifest.py`【WEAK・偽装耐性限界】のアンビブランチで**計測・提示するadvisory**とし、完全な自動保証としては引用しない。分離度/空気感の最終判断は §6.2 ラベル付き試聴オーナーQC（人手）。全て商用OK棚。

### 4.4 SFXレジストリ(L4) base distinct20（base_id≥14）＋**"数を実測化"＋遷移SFX多様性（監査sound#23/#26/#27/#28）**
- **音の自動床は`check_sound_layers`（wired）だが distinct/beds は provenance自己申告＋mux sha束縛（pass2 BLOCKING是正）:** SFX distinct数／beds数が**provenanceに申告され最終muxに束縛されている事実**は`check_sound_layers`のPART2が確認（`distinct_files`≥12／`ambience_distinct_beds`≥4／`audio_mix_sha256`一致）。`SOUND_PROV_MIN_SFX_FILES=12`はまさにこの provenance自己申告値の下限であり、**`check_sound_layers`は distinct SFX を波形から個数計数してはいない**（波形実測は onset密度＋ambience帯域のみ・§4.1）。round4の「provenanceを読むだけ」を"誤り"とした撤回は行き過ぎで、**distinct/beds床は『自己申告＋sha束縛（＝孤児/未muxを弾く強度）』であって『実mix波形からのSFXイベント検出』ではない**と再訂正する。本話SFX distinct20/beds6はこの申告床を上回るが、SFXが実際に可聴/豊かかは §6.2 音5本試聴が唯一のhard保証。
- **【WEAK（偽装耐性限界・完全な自動保証として引用しない）】`verify_sfx_manifest.py`（#23/#28）:** (a) cue_sheet参照の**実SFXファイル内容ハッシュをディスク上で数えdistinct導出**、(b) **マスターWAVのonset/スペクトル解析で意味アクセント数・平均間隔を計測**、(c) スペクトル/クロス相関で**区別可能なSFXイベント数**を計測。**目安＝意味アクセント密度 ≥6/分・主要reveal/slam/転換の≥80%にSFX配置・平均間隔≤10秒。** 無タグ・無イベント束縛SFXは検出（必須フィールド`{semantic_tag, bound_event, tc, level, base_id}`）。**ただし本ゲートはWEAK（台帳）＝深い偽装耐性が限界ゆえ、SFXの豊かさ/フィラー混入の最終保証は §6.2 preflight_owner_review の音5本試聴（人手）に置き、POST-render hard列でなくadvisoryとする。** 赤フィクスチャ（無タグcue/単一音40回で検出）は補助実証にとどめ、これで確定10にしない。
- **base_id会計（#27）:** distinct床の判定は**distinct_files=20（bar_impact3変種も各ファイル計上）**で説明。**加えてピッチ変種を除いた base_id 単位でも ≥14**（変種水増しを密度カウントから除外・コードのfiller除外方針と一致）。`base_id`は`sfx_manifest`付記メタでなくゲート判定に配線。
- **遷移SFX多様性（監査sound#26・pass2 MAJOR是正でWEAK gateを"hard化"表記から降格）:** §3.8で全40境界＋539カットがpush/slide/zoompunch/whipのForcefulCut。round3は`whip_transition`1種のみ＝単一whooshを40+境界に貼る欠陥。**遷移SFXを転換種別ごと≥4系統（push/slide/zoompunch/whip）×各2ピッチ=8ファイル以上に分割し境界ごとローテーション。** `verify_sfx_manifest`【WEAK】が**(1)遷移distinct≥4、(2)単一base_id/単一ファイル使用回数≤全SFXイベントの15%、(3)遷移音の連続同一≤2回**を**advisoryで計測・提示**する（round4/round5の「hard化」表記は撤回。WEAKゲートの出力を自動hard保証として引用しない）。**「20分同一遷移音の耳障り＝単調遷移」のhard backstopは §6.2 音5本試聴のオーナー承認**（§6.1・§11#13とラベル一致）。
- **フィラー再導入防止（#24＋pass3 MAJOR#22是正）:** 実装コードはfiller transient_bed/tick-bedをdistinct_filesから明示除外。**密度床≥6/分のカウント対象から連続テクスチャ床(roll/hum/tick bed)を除外**（コードのdistinct定義と一致）。連続テクスチャ床(roll/hum/tick)の**上限≤3種・総尺占有率≤15%**は**`verify_sfx_manifest`【WEAK】がadvisoryで計測・提示**する（★pass3 MAJOR#22是正:round6の「`verify_sfx_manifest`でhard化」はWEAKゲート（台帳・偽装耐性限界・完全な自動保証として引用禁止）を確実保証と偽る残留＝直前の遷移多様性advisory降格・pass2 item(8)と矛盾していたため撤回。§4.4内の全「hard化」表記をWEAK=advisoryへ統一）。**連続床の≤3種/≤15%占有の最終hard保証は §6.2 音5本試聴のオーナー承認（人間backstop）**に置く。EquityTheftTally走行/CaseTimelineプレイヘッドの連動音は**離散アクセント（加算節目/reveal毎）でカウント、連続humは装飾扱いで密度非算入。**
- **「Kurzgesagt/Veritasium級」の正直化（#28）:** コード注記の"Kurzgesagt-Veritasium level"は数値ラベルであり実測でない。§13 axis5満点根拠から「参照ch級の豊かさ」を外す。**音の自動保証は配線済み`check_sound_layers`（distinct SFX≥12/beds≥4/mux sha）で担保し、豊かさ/一体感/カバレッジ質は §6.2 音5本試聴のオーナー承認（人間backstop）で確定する。** WEAK（`verify_sfx_manifest`/`check_ending_sound`）とドロップ済（`check_stem_loudness`/`check_music_coverage`）を確定10の根拠にしない。
- 主要（離散意味アクセント）: subhit_seize／paper_tear／title_stinger／mailbox_thunk／debt_slam_15k(1:50)／bar_impact×3(distinct files)／surplus_drain／institutional_stamp／heartbeat_stat／redline_scratch／govt_card_break(13:20)／whip/push/slide/zoompunch遷移各2ピッチ／gavel_rap_muffled／scroll_unfurl／timeline_playhead_tick／counter_roll節目tick／vote_slam_9_0(本編最大-7)／kinetic_type_tick／placard_release。連続床(密度非算入)=counter_roll_bed／timeline_hum／court_room_tone。

### 4.5 EDの固定ベッドと「変な音」禁止機構（**検出器を自己免除しない・独立校正・監査sound#30/gaming-BLOCKING#34**）
MB-END＋AMB-END固定。低域上昇ロー・ジェット/飛行機様whoosh・サブうねり・トレーラーブームを素材レベルで禁止。切りよくフェード＝解決コード頭基準にオンビート4拍直線フェード。
- **roar自動チェック【WEAK（台帳・偽装耐性限界・完全な自動保証として引用しない）】`check_ending_sound.py`（#34）:** 「40–200Hz低域エネルギー勾配＋高調波欠如＋帯域幅膨張」の複合条件でED終盤の不快低域膨張（トレーラーブーム/ジェットwhoosh）を**advisoryに検出**。検出器閾値は"MB-ENDを含まない"独立ラベル済データで凍結してから通す（自己免除の循環回避）。**ただし本ゲートはWEAKゆえ、「終盤の変な音を出さない」hard保証の本体は §6.2 preflight_owner_review でED低域スペクトログラムを含む音5本をオーナーが実際に試聴して承認する人間backstop**に置く（機械判定だけを完成根拠にしない）。MB-ENDが検出でトリップしたら閾値を緩めず音楽を再素材化。
- **ED代替ベッド（#30）:** MB-ENDがFAIL/オーナー否認の場合の**MB-END-ALTを最低1本用意**し§4.5/§12にフォールバック明記（「変な音のまま出荷」か「ED無し」の二択を回避）。
- **平坦窓検出（advisory・粒度是正・#43）:** `check_ending_sound.py`に**「12秒窓ごとの音エネルギー変動が閾値未満の窓が連続12秒でフラグ」**（motion window同粒度）。音の平坦窓と`motion_energy`窓を位相オフセットさせ鈍区間の両窓盲点を消す。**これもWEAKゲートの一部＝advisory**で、鈍い終盤の最終判断はオーナー試聴。
- EDは投入前に低域スペクトログラムを`preflight_owner_review`でオーナー試聴・目視必須（＝hard backstop）。

### 4.6 ミックス機構
- **(a)サイドチェイン:** busVOをキーにbusMus -5dB / busAmb -4dB / SFXテクスチャ -3dB。インパクトSFXはダッキング対象外。**VO発話区間はサイドチェインで Music/Amb を §4.1表のターゲット帯（Music -22〜-20 / Amb -32〜-29 LUFS）へ寄せる。この -22/-32 等は設計ターゲット値（advisory）であって"床で担保"ではない（pass2 BLOCKING是正）。** round4/round5がここで書いた「§4.1のstem実測床（Music>-24/Amb>-30）で担保」は**ドロップ済`check_stem_loudness`由来の閾値を自動保証として再導入する残留リーク**であり撤回する（§4.1本文とも矛盾・-30と§4.1表の-32も不整合）。**VO発話区間の相対音量のhard保証は §6.2 音5本試聴のオーナー承認**で、stem LUFS/TP系列は同席でadvisory提示するのみ。
- **(b)意図的沈黙（尺稼ぎ無音でない）:** 設計沈黙2箇所（Act2「Nothing」直前、Act4「It sounded almost reasonable.」後）。音楽のみ落とし、Amb/ルームトーンはL3床で継続、完全無音を作らない、≤1.2s。
- **(c)2-pass loudnorm:** Pass1 measured→Pass2 `I=-14:TP=-1.0:LRA=11:linear=true`。最終 I=-14(±0.3)/TP≤-1.0/LRA9–12 を`check_final_acceptance`【実装済】が実測合格判定。48kHz/32bit float WAV→AAC320k。
- **(d)mux刻印【実装済】:** 最終WAVのSHA-256を`audio_mix_sha256`としてコンテナメタ＋provenance JSONに刻印、ゲートがprovenance shaと実mux音声shaの一致を確認。

### 4.7 成果物
`audio/beds/`(MB0–5,END,END-ALT)・`audio/ambience/`(base6)・`audio/sfx/`(20 distinct files＋遷移8＋変種＋`sfx_manifest.json`)・`audio/stems/`(VO/Music/Amb/SFX個別WAV＋各sha)・`audio/cue_sheet.csv`・`audio/master_-14LUFS.wav`＋`provenance.json`。**マスターは§5.0の理由で `media_root/episodes/PD-2026-033-tyler/06_voice/master/vc_master_v001.wav`（測定用）と `vc_master_v001.mp3`（resolve_master解決用）の両方を配置し wav↔mp3 の長さ ±30ms 一致をassert（#5のMP3 priming対策）。** 実装後`preflight_owner_review.py`で章境界＋終盤含む音5本試聴＋実測LUFS/TP/LRA＋stem実測（`check_sound_layers`結果）＋music stemアクティブ率タイムライン提示（advisory・人間承認がhard）。

---

## §5. 字幕・画面内テキスト設計（逐語源・強制整列・区間ドリフト・**基準定数是正・skip穴封鎖**）

### 5.0 verify_caption_sync の実装状態と**基準定数の是正＋skip→PASS穴の封鎖（監査captions-BLOCKING#1）**
**【実装済（実定数）・現行】** `scripts/verify_caption_sync.py`：`FAIL_P90_LAG=0.35` / `FAIL_MEDIAN_LAG=0.10` / `FAIL_SEGMENT_DRIFT=0.50`（per-minute median の最大値のみ+0.50sと比較）/ `MIN_MATCHED_FRACTION=0.60` / `EXACT_TOL=0.15`（`exact_pct`は算出・報告のみでゲート化されていない）。

**★基準定数の是正（監査captions-BLOCKING#1・最重要）:** round3は「実測 per-minute median は約 -0.60 に居る」と述べ drift-FAILを lead_baseline(-0.60)+0.25=-0.35 に置いたが、**これは誤り**。verify_caption_sync のground truth自体がドリフトフリーなwindowed medium.en であり、**本設計自身が引用するEP31実測（p50=-0.02s・exact84%）が示す通り、realized median は ~-0.02（≒0）であって -0.60 ではない**。よって：
- **(i) -0.60→+0.25 の絶対アンカーを全撤回。** これは健全話（EP31の-0.02≫-0.35）を毎分false-FAILさせる。
- **(ii) round3が主張した「約1.1s帯の後半ドリフトが素通り」は虚偽。** 実realized median≈-0.02＋既存 FAIL_MEDIAN_LAG=+0.10/FAIL_SEGMENT_DRIFT=+0.50 で実効的に未カバーな帯は約**0.12s**。
- **(iii) ドリフト検査は"基準非依存の相対量"に接地する（下記 check_longform_drift）。**

**skip→偽の緑の封鎖（#1・オーナー最優先#1の防御）:** 実コード確認：**(i)** `check_caption_sync`は `evaluate()` が `skipped:True` を返すと `{ok:True, hard:False}`＝非hard PASSにマップ。**(ii)** `resolve_master()`はoverride無しだと `06_voice/master/vc_master_v*.mp3` のみ解決。→ マスター誤配置/whisper不在で字幕ゲート全体が1キューも測らず緑になる未束縛不変条件＝水増し。二段で塞ぐ：
- **(A) マスター配置の束縛【要実装／配線】:** マスターを `media_root/episodes/PD-2026-033-tyler/06_voice/master/vc_master_v001.mp3`（resolve_masterがglobする正確パス）に配置＋測定用WAVも併置（§4.7）。`check_final_acceptance`に`--master`/`--srt`明示overrideを通す。
- **(B) skip穴の封鎖【要実装／本話ブロッキング】:** `check_caption_sync`をラップし、**`skipped==True`はhard FAIL（`ok:False, hard:True`）**。さらに**`reliability=='windowed'`かつ`not skipped`かつ`matched_fraction≥0.75`**（long-form床・#4）を出荷のhard条件にassert。**赤フィクスチャ=マスター欠落状態でexit1を実証。**

**【要実装／本話ブロッキング】`verify_caption_sync.py`に`check_longform_drift()`追加（基準非依存・監査#1/#3是正）:**
- (a) **exact率hard化（ratchet up・監査gaming#41）:** `MIN_EXACT_PCT=84`（EP31達成84%を下げず据置＝床下げ禁止。旧78は床フィット）で `exact_pct<84→FAIL`。
- (b) **per-window相対:** 各60秒窓 `|median − global_median| ≤ 0.10`（**測定した全体中央値からの逸脱**で締める・絶対-0.35アンカーは撤回）。
- (c) **前半/後半median差 ≤0.05**（基準非依存）。
- (d) **単調悪化スロープ ≤0.010 s/分**（per-minute median の線形回帰の傾き・基準非依存）。
- (e) **Act5サブバンド(14:20–19:00) `|median − global_median| ≤ 0.08`**。
- **CAPTION_LEAD_SECONDS(-0.60) 基準の絶対アンカーは一切使わない（#1）。** §5.0narrativeの「realized median -0.60」記述を撤回し「realized median ≈ -0.02（windowed ground truth比）」に訂正。

**showpiece-cueマッチ強制ゲート【要実装・監査captions-MAJOR#2】:** lag統計は matched cue のみで算出され unmatched cue は分子分母から脱落する（実コード確認）。faster-whisperが誤認しやすい引用/数字語（T5 `$2,300`口語・T7・T11・T15 Latin residue・T16 Overplus・T18・T19 Roberts・T21・T3' Gorsuch）が丸ごと除外され、それらで構成された遅い区間が matched_fraction 全体では隠れる。**指定showpiece-cueリスト（T5/T7/T11/T15/T16/T18/T19/T21/T3'）は各々matched集合に在ること（第一内容語がalign）を必須とし、欠落でFAIL。** 加えて**per-minute/per-Act窓ごとに最小 matched_fraction を課す**（区間のcueを落として遅延region隠蔽を封鎖）。**未マッチcueリストを acceptance receipt に出力**（preflightだけでなく）。**赤フィクスチャ=showpiece cueを故意desyncでexit1を実証。**

実装完了まで§5.2該当閾値・§6.1・§13-6は設計完全性点のみ、実装＋赤緑両実証で確定。

### 5.1 源泉と生成パイプライン（**ドリフトフリー不変条件＋v001強制＋MP3 priming・監査captions#2/#4/#5**）
**唯一の源泉=台本`[VO:]`行を連結したnarration_index（逐語）。要約・言い換え・意訳を字幕にすることを禁止。**
1. `build_narration_index.py`→`narration.tokens.json`。
2. **`06_audio/narration_index.v001.json`（`chunks[]` with numeric `start/end`）を必ず生成。** 無いと`load_windows()`が`[]`を返しwhole-fileフォールバック。
3. **v001強制を機構化（監査#4・v002自動選好の穴）:** 実producer`gen_captions_forced`はv002が在ると自動選好する（実コード確認）。**(a) preflight/shipゲートで `narration_index.v002.json` が存在すればexit1**（本エピソードで不良変種を排除）、**(b) producerと`verify_caption_sync`が同一index fileを解決したことを run manifest の sha一致でassert**（producerがv002・verifierがv001の二重基準を封鎖）。**赤フィクスチャ=ダミーv002を置いた状態でexit1を実証。**
4. **ドリフトフリー不変条件（carsearch実績`concat_master`を鏡写し・#2）:**
   - (a) 各narration chunkを個別音声ファイルとしてレンダ（1本の長尺マスターを後からwhisper/wpmで区切らない）。
   - (b) マスターは個別chunkファイルを固定・列挙済み無音ビート（0.6s/2.5s等）で連結。
   - (c) narration_index の start/end ＝ 累積 ffprobe実測 chunk長 ＋ その無音ビート（wpm推定/whisper推定window禁止）。
   - (d) 既存不良変種`narration_index.v002.json`を使わない（上記(3)で機構化）。
   - **(e) per-chunk整合assertion（終端のみ検査の穴是正・#5）:** narration_index.v001 の**各chunk window duration = 対応source chunk fileのffprobe実測長 ±30ms**（終端累積±50msだけでなく各内部境界を検査）。
   - **(f) MP3 priming対策（#5）:** 測定は`vc_master_v001.wav`で行い、resolve_master用mp3とは長さ±30ms一致をassert（MP3 encoder/decoder priming ~20–50msが±50ms budgetを食う問題を回避）。
5. ElevenLabsマスター（過去話と同一voice_id/stability/similarity/speed）を(a)(b)で構成。
6. faster-whisper `medium.en`で強制整列（`--word_timestamps True --vad_filter False`）→語ごとonset/offset。
7. `pack_captions.py`→`captions.srt`＋`captions.meta.json`。

**数値床:** 総VO約3,050語（§8設計/目標値・再集計待ち）→字幕**460–500枚**（平均6.2–6.8語/枚）。

### 5.2 タイミング規律
- リード0.60s: `caption_in = word_onset−0.60s`。
- 表示終了は語オフセット由来を一次定義: `caption_out = last_word_offset + 0.30s`。durのclampは最小可読時間下限保証のみ（0.90s未満のときだけ延長）。隣接ギャップ≥0.08s。
- **合否しきい値の帰属:** **【実装済で担保・caption_sync=タイミング】** p90≤0.35／median≤0.10／per-minute median max≤0.50／matched≥0.60。**【実装済・check_caption_format=フォーマット】** ≤10語/≤50字/≤2行/≤27cps/≤7s。**★機能語行末0（`_NO_DANGLE_END`）＝【要実装／本話ブロッキング】受領側hardゲート化（pass3 BLOCKING#2）:** オーナー最頻失敗『字幕が変な所で切れる』（pd-ep21-24-incident#2・feedback_anim_caption_polish）はround6ではproducer側`pack_captions`生成時の自己検査`_NO_DANGLE_END`だけが担保で、**shipped `captions.srt`を独立に再検査する受領側ゲートが無かった**。配線済`check_caption_format`（≤10語/≤50字/≤2行/≤27cps/≤7s）は機能語行末を見ないため、`the/and/to/of`で終わる字幕が全wiredゲートを通過しうる＝トップ被害の自己申告依存。**是正:`check_caption_format`を拡張（または`check_caption_dangle`を新設）して最終shipped SRTの各行末を機能語辞書（the/a/an/and/or/but/to/of/in/on/for/with/that/as/at/by/is/was/…）で再検査し、機能語行末が1件でもあればexit1。`check_final_acceptance.py`に配線＋§7 step13 POST-render hard列に追加。赤フィクスチャ=機能語行末のSRT行→exit1を`test_gate_fixtures.py`に同梱。****【要実装で担保】** skip=hard-fail＋reliability=windowed＋matched≥0.75／exact≥84／per-window `|median−global_median|`≤0.10／前半後半差≤0.05／単調悪化≤0.010s分／Act5≤0.08／showpiece-cue必須マッチ／**機能語行末0の受領側再検査**。上限（下記§5.3）は`pack_captions`＋`check_caption_format`自己検査＋受領側再検査。
- **「またぎ禁止」の対象限定:** hard切り（またぎ禁止）は**シーン/幕境界（40シーン切替）に限定**。シーン内部の高速カットは字幕境界を強制せず、字幕は§5.3の文法/タイミング分割のみに従う。

### 5.3 行分割規則（**producer整合・監査captions-MAJOR#3是正**）
**round3の「≤8語/≤44字」を撤回。** 実producer`gen_captions_forced`は`SEG_MAX_WORDS=10`/`SEG_MAX_CHARS=50`（8→10へ引上げは中間節の8語境界orphan切断＝「字幕が変な所で切れる」対策と明記）、ゲート`check_caption_format`は`MAX_LINE_CHARS=50`/≤2行/≤27cps/≤7s。**設計を実producer/実ゲートに整合:**
- 上限（全hard・1枚）: **≤10語・≤50字/行・≤2行・≤27cps**（`check_caption_format`＋`gen_captions_forced`と一致）。**round3の≤8語はorphan切断退行リスクゆえ採らない（#3）。**
- 分割優先: ①文末②句読点直後③前置詞・接続詞直前④最近接内容語境界。機能語行末0件（`_NO_DANGLE_END`）。逐語一致（数字も話し言葉のまま）。

**Hookサンプル（逐語・話し言葉綴り・監査aismell#44準拠）:**
```
1  A twenty-three-hundred-dollar bill               (逐語・数字は話し言葉)
2  took the home this woman had paid off —          (ダッシュ・#13整合)
3  and every cent was legal.                        (文末・legalタグはHookのみ)
```
（★pass3 MAJOR#13整合:Hook VO実文を"took the home this woman had spent years paying off"へ改めたため、caption逐語源もこれに一致させる。round6サンプルの"took this woman's home"は立ち退き誤認語で撤回。）
※ `$2,300`のグリフ表記はグラフィック層(T5)のみ。字幕にデジタル通貨文字列を入れない。`caption_narration_match`＋`verify_onscreen_text`が「VOが語で話す金額を字幕にデジタル表記しない」を自己検査。

### 5.4 主要画面内テキスト（表記凍結・監査#42/#44/#45/#47/#51）
原則: グラフィックテキストと字幕を同時刻に二重表示しない。`598 U.S. 631`（`600`禁止）／PLF統計は`Est.`必須／州名断定禁止／保持側StateMap点灯=PLF列挙12州・文言**"at least a dozen"（pass2 MAJOR是正：round5がここに残していた"more than a dozen"はT9(§5.4)・§1.3・§2.6 Act5末尾VOの"AT LEAST A DOZEN"と矛盾するため撤回）**。

| # | 時刻 | 部品 | 確定テキスト | 注記 |
|---|---|---|---|---|
| T1 | 0:00 | SEIZED札 | `SEIZED` | 赤札zoompunch |
| T2 | 0:08 | OPタイトル | （§9確定タイトルに一致） | PD標準 |
| T3 | 0:08 | OPサブ | `Tyler v. Hennepin County · 598 U.S. 631` | **600不使用** |
| T5 | 1:20 | 債務メーター | `$2,300`→`$15,000` | `tax_debt_meter`・中間額出さず・1:50 slam |
| T7 | 4:50 | EquityBar三段 | `DEBT $15,000`→`SALE $40,000`→`SURPLUS $25,000` | **余剰初出し**・各ForcefulCut着弾 |
| T8 | 5:40 | 分配図 | `COUNTY`／`TOWN`／`SCHOOL DISTRICT` | 元所有者ウェッジ欠落 |
| T10 | 8:20 | ソースチップ | **裏取り後のみ**`Hall v. Meisner, 6th Cir. (2022)`／未裏取りは`another homeowner, in federal court` | **金額/性別/所在なし・勝訴の事実はCLM-0021裏取り後** |
| T11 | 9:00 | EquityTheftTally | `$780,000,000+`＋`Est. — Pacific Legal Foundation` | 走行カウンタ・heroマップ |
| T12 | 9:20 | 体感比較 | `92% PAID`／`8% DEBT`＋`Est. — PLF` | 8%赤 |
| T13 | 10:00 | 定義書換 | `PROPERTY`→赤ペン取消 | キネティック |
| T9 | 11:20 | StateMap保持側 | `AT LEAST A DOZEN STATES STILL ALLOWED IT`（点灯**12**＝PLF列挙・`Est.—PLF`） | 州名なし・**"more than a dozen"(>12)は点灯12と矛盾ゆえ"at least a dozen"へ是正(pass1 MINOR)** |
| T15 | 14:40 | MagnaCartaScroll | `…AND THE RESIDUE SHALL BE LEFT TO THE EXECUTORS…` | **Magna Carta 1215 ch.26・逐語・1215アイコン限定（#51）** |
| T16 | 15:20 | Overplus引用 | `any "Overplus"… "immediately restored to the Owner."` | **`— English statute, 1692`ラベル（pass2 MINOR是正：CLM-0014Bの出典＝1692年英制定法 4 W. & M., ch.1, §12 に確定・Blackstoneはこの句の出典ではない）・羊皮紙/1215に載せない（#51）** |
| T17 | 16:00 | CaseTimeline長 | `1215`·`1884`·`1980`·`2023` | プレイヘッド走行 |
| T18 | 18:15 | VoteTally着弾 | `9–0`＋`598 U.S. 631` | slam・単一hard |
| T19 | 18:30 | Roberts引用 | `"The taxpayer must render unto Caesar what is Caesar's, but no more."` | **カンマ・StateMap緑化と融合** |
| T21 | 18:40 | StateMap緑化 | **意見本文で「36」確認後**=`36 states + federal already required return`／未確認=`A large majority of states already required return` | 州名断定なし・二人称ペイオフ |
| T3' | 18:50 | Gorsuch | `"fines by any other name"`（CLM-0012の逐語断片・**verify_onscreen_text逐語照合対象**／#45） | 1.5s単一キネティックキャプション |
| T22 | 19:20 | EDメッセージ | `NOT HER WINDOW — YOURS.` | 象徴表現 |

**引用綴り凍結（1字違えばFAIL・`verify_onscreen_text.py`が台本quotesと逐語照合）:** T19 Roberts（カンマ形・CLM-0013）・T15 residue（CLM-0014A/1215）・T16 Overplus（CLM-0014B/English statute 1692・**年代帰属ラベル照合**）・T3' Gorsuch（CLM-0012完全文からの逐語断片であることを確認・#45）・T21州フレーミング（数値焼込は§1.3の本文確認後のみ）・**T10 Hall（CLM-0021裏取り後のみ勝訴の事実を出す）**。

### 5.5 スタイル・レイアウト（左見切れ＋**スクリム禁止・監査brightness#25**）
1920×1080。字幕セーフ矩形 x∈[160,1760]（幅1600px）・baseline y=980。太字サンセリフ700・54px・白#FFFFFF・黒アウトライン4px＋ドロップシャドウ。行間1.15。グラフィックは上〜中段、字幕は下段固定。
- **暗化スクリム禁止（#25）:** 字幕/lower-third背景に全幅・部分の暗化スクリム（黒グラデ帯/半透明黒板）を敷くことを禁止。可読性はアウトライン＋ドロップシャドウ＋グロー（発光側）のみで確保。`check_image_cut_luma`が**字幕帯領域(y≈900–1010)の下段バンドサンプル輝度低下**を検査し、スクリム由来の暗化を検出。

### 5.6 品質ゲート配線
**【実装済(wired)hard】** `check_caption_sync`(p90/median/segment_drift max/matched/exact報告＝**タイミングのみ・pass2 MINOR是正：機能語行末はここに含めない**)、`check_caption_format`(≤10語/≤50字/≤2行/≤27cps/≤7s＝**フォーマット・配線済 L1569**)、**`verify_caption_coverage`（下記・全ナレchunk字幕化＝『字幕が飛ぶ』の名前のある機構）**、`caption_narration_match`(語一致)、`verify_onscreen_text.py`(T群照合・`600`不在・州名断定0・引用逐語含T3'/T16年代ラベル・`Est.`・字幕内デジタル通貨0・**pass1 MAJOR是正：本ゲートは配線済SOLID＝新規実装でない。要拡張はreview_factsロケータ前提検査(§1.4)のみ**)、`verify_script_lint.py`(§2.7・wired要拡張)、`check_caption_format`/`pack_captions`自己検査。
- **★『字幕が飛ぶ(未字幕chunk)』の名前のある機構＝`verify_caption_coverage`（wired・pass1 MAJOR是正）:** round4はこの配線済SOLIDゲートを一度も引用せず、`matched_fraction≥0.75`とshowpiece-cueマッチで代替していたが、それは**matched cueの遅延統計**であって『全ナレchunkが字幕化されたか』の被覆保証ではない（unmatched cueは分母から脱落しうる）。`verify_caption_coverage`（`check_final_acceptance.py`に配線済）が**全narration chunkがSRTで字幕化されているかをhard判定**する。§11に未字幕chunk専用行を追加。matched_fractionは補助と位置づける。
**【要実装hard】** skip=hard-fail＋reliability/matched床(§5.0-B)、`check_longform_drift`(exact≥84/per-window相対/半差/スロープ/Act5・caption_syncの真に新規な拡張)、showpiece-cue必須マッチ、v002存在exit1＋index sha一致、per-chunk±30ms＋MP3 priming、**★機能語行末0の受領側再検査＝`check_caption_format`拡張（or `check_caption_dangle`新設）で最終shipped SRTを独立に再検査しexit1・pass3 BLOCKING#2＝『字幕が変な所で切れる』のproducer自己申告依存を受領側hardゲートへ格上げ**。**【WEAK】** `verify_script_structure.py`(§2.7・意味判断はオーナー台本ロックがbackstop)。
**偽の緑回避:** 字幕はマスター音声shaに紐付け、音声再生成時は必ず再整列(`freshness`)。

---

## §6. 品質ゲート（Done=動く実物確認・自己申告完了禁止・**赤フィクスチャ必須**）

**すべてのhardゲートが緑＋実物目視/試聴/motion-reel＋オーナー確認**の三点で初めて「完成」。緑≠完成／偽の緑／薄い音で緑／skip偽緑／**stub緑**を封じる。

### 6.0 全要実装/要拡張ゲートの赤フィクスチャ必須（**stub緑封鎖・監査gaming-BLOCKING#32**）
真に新規な要実装ゲート（caption skip=hard-fail/longform_drift/showpiece必須マッチ/v002封鎖）と、配線済SOLIDの**要拡張/再校正**（onscreen_text/image_cut_luma/arc_nonrepeat/footage_utilization/verify_script_lint/thumb_subject_luma/check_padding/motion_energy再校正）は、**stub（exit0を返すだけ）や緩い閾値でも緑に見える**。よって：（**🗑ドロップ済のstem_loudness/music_coverage/bbox-flowは赤フィクスチャ対象から除外＝そもそも機構として引用しない。WEAKのverify_sfx_manifest/verify_script_structure/check_ending_soundは赤フィクスチャを補助実証にとどめ、確定10の根拠にせず人間backstopで担保**）
- **各要実装ゲートに committed 赤フィクスチャ（意図的バッド成果物：desynced SRT／無音stem／再利用clip ID／誤州数／暗カット／紙芝居フリーズ図）を同梱し、ゲートが必ずexit1することを実証。**
- **出荷ブロック:** 各ゲートが「バッドでexit1」かつ「実成果物で緑」の両方を示すまで出荷不可。`scripts/test_gate_fixtures.py`が全赤フィクスチャを走らせ、1つでもexit1しなければ§12 step13前でship-block。
- **§13の設計完全性10は、赤フィクスチャを"設計として明記(SPECIFY)"していないゲートには与えない（pass2 MINOR#13是正）。** 赤フィクスチャの**コミット（`test_gate_fixtures.py`への実装）**は実装フェーズの確定条件であり、設計書段階では「どのバッド成果物でexit1するかを具体的に指定していること」を満たせば設計完全性10を認める。よって§13.1のaxis6(字幕)/axis7(品質ゲート)等が「要実装ゲートの赤フィクスチャ未コミット」でも、設計が赤フィクスチャを具体指定していれば設計完全性10で矛盾しない（実効ゲート点＝§13.2側では未コミットゆえ計上しない）。

### 6.1 hardゲート一覧（実装状態を正直に三分・赤フィクスチャ列追加）

**（実装状態は実ゲート台帳と1対1。SOLID=wired／WEAK=偽装耐性限界・人間backstop併用／要実装=真に新規。🗑ドロップ済は本表から除去。）**

| ゲート | 状態 | 本話の合否値／限界／赤フィクスチャ |
|---|---|---|
| `check_runtime_band.py` | 実装済(wired) | 実測1,170–1,230s（唯一のship-gate尺基準）。**density測らず（#35）** |
| `preflight_render_gate.py`（計画レベル） | 実装済(wired・要拡張) | 深度フラグ数=238／FigureBeats≥10かつ各幕≥4／時間分布(60s窓≥1図/無図≤60s)／ヒーロー≥3＋時間分布床／平均2.0–2.6s／全S0NN≥3840px／span束縛／グラフィック象徴 種類≤2・各≤3回。**最終合成輝度は測らない** |
| `check_image_cut_luma.py`（POST-render・全539） | **実装済(wired・要拡張/校正)** | per-cut≥52／per-figure≥46／四隅・5%tile≥46／暗連鎖≤6s／breath最暗位相／字幕帯スクリム検査。**pass1 MAJOR是正:配線済SOLID・新規でない。** 赤=中央明四隅潰れカット |
| `check_body_luma`（再校正） | 実装済(wired・要再校正) | median YAVG≥48・暗フレーム率(YAVG<**38.0**)≤**0.08**（#23再校正）。body単独では出荷可としない |
| `motion_energy`（wired・再校正で引上げ） | **実装済(wired・要校正)** | 台帳実床=within-shot≥12/p10≥9→本話再校正でstill-p10≥**17**(=⌈0.35×46.6⌉)/全体median≥18/12秒窓≥8＋motion-variety(entropy≥1.5/CV≥0.25)。**pass1 BLOCKING是正:新規でなく引上げ再校正。** 赤=紙芝居フロー≈0 |
| ~~per-figure-bboxフロー~~ | 実在するが未配線→advisory | **`check_motion_bbox_flow`は`scripts/`に実在するが`check_final_acceptance`に0回参照＝未配線（"存在しない"は誤り・pass2訂正）。台帳ドロップ方針でhard引用しない。各図の実運動hard保証は上記motion_energy＋§6.3 motion-reel人間承認。bbox中央値≥8pxは参考計測のみ。** |
| `check_footage_diversity` | 実装済(wired・単一話専用) | distinct≥0.40／再利用≤4／汎用象徴(全cut src)≤2。話またぎ/象徴反復回数は測らない |
| `check_arc_nonrepeat.py`（basename交差） | **実装済(wired)＋共有allowlistは要実装** | **実挙動＝他話`*_film.json` cut src basename＋public メディアと交差=0をhard（`catalog_fingerprints`は読まない）。既定=法廷/庁舎も完全分離(方針A)。identical共有はallowlist引数の新規実装(方針B・§14-3要実装)後のみ。round5の"アーク共有で交差判定除外"はno-opゆえ撤回（pass2 BLOCKING）。** 赤=他話basename混入でexit1／(B)時は共有ID通す・事件固有ID再利用落とす |
| `check_footage_utilization.py` | **実装済(wired・要拡張)** | 未使用≤20%（=使用率≥80%・単一床へ整理#10）／選定広さ≥39候補≥3テーマ／実配置distinct≥32（#36）。供給床も32に統一（[26,31]デッドゾーン解消）。赤=過少選定 |
| `check_sound_layers`（wired） | **実装済(wired)** | **PART1=onset密度＋ambience帯域を波形実測／PART2=provenanceの`distinct_files`≥12・`ambience_distinct_beds`≥4を読み`audio_mix_sha256`で最終muxに束縛（＝自己申告＋sha束縛・孤児/未muxを弾く）。distinct SFXを波形から個数計数はしない（pass2 BLOCKING是正）。本話SFX20/beds6で申告床超。** SFXの可聴性/豊かさ/VO区間相対音量/musicカバレッジ質は測らず→§6.2人間試聴backstop |
| `SOUND_PROV_MIN_SFX_FILES=12`／`ambience_distinct_beds` | 実装済(自己申告sha束縛のみ) | provenance数値の下限＋mux sha束縛。**波形からの個数計数ではない。beds床の実体は"アンビ別ベッド数"でありmusicベッド数ではない** |
| `verify_sfx_manifest.py` | **WEAK(偽装耐性限界)** | distinct/base_id/密度/遷移多様性/無タグ0をadvisory計測。**完全な自動保証にしない→SFXの豊かさ/フィラーは§6.2音5本試聴でhard承認。** 赤=補助実証のみ |
| 🗑`check_stem_loudness.py` | **実在するが未配線＝ドロップ扱い(引用禁止)** | **pass2事実訂正:`scripts/`に実在するが`check_final_acceptance`に0回参照＝未配線・現状走らない（"存在しない"は誤り）。台帳ドロップ方針で自動保証に引用しない。VO区間相対音量は§6.2人間試聴backstopで担保** |
| 🗑`check_music_coverage.py` | **実在するが未配線＝ドロップ扱い(引用禁止)** | **pass2事実訂正:`scripts/`に実在し`evaluate(epdir,render)`実装済(＝1行で配線可能)だが0回参照＝未配線（"存在しない"は誤り）。台帳ドロップ方針で自動保証に引用せず。musicカバレッジ質/中盤dropは§6.2人間試聴backstop（beds≥4はアンビ床でありmusicを担保しない）** |
| `check_ending_sound.py` | **WEAK(偽装耐性限界)** | roar複合/平坦12秒窓をadvisory検出＋MB-END-ALT。**終盤音のhard保証は§6.2 ED音オーナー試聴。** 赤=補助実証のみ |
| `check_final_acceptance`(音実測LUFS) | 実装済(wired) | I=-14(±0.3)/TP≤-1.0/LRA9–12 |
| `audio_mix_sha256`一致 | 実装済(wired) | provenance sha=実mux音声sha |
| `check_caption_sync` | 実装済(wired) | p90≤0.35／median≤0.10／per-min max≤0.50／matched≥0.60／exact報告（**タイミングのみ**）。skip→非hard PASSの穴は下記で封鎖 |
| `check_caption_format`（wired・L1569） | 実装済(wired)＋**機能語行末は要実装/本話ブロッキング** | ≤10語/≤50字/≤2行/≤27cps/≤7s（フォーマット床・配線済）。**★pass3 BLOCKING#2:機能語行末0（`_NO_DANGLE_END`）を『producer自己検査のみ』から『受領側hardゲート』へ格上げ＝本ゲートを拡張（or `check_caption_dangle`新設）して最終shipped `captions.srt`の各行末を機能語辞書で再検査しexit1、`check_final_acceptance.py`配線＋赤フィクスチャ（機能語行末SRT→exit1）。オーナー最頻失敗『字幕が変な所で切れる』を自己申告依存から独立検査へ。** |
| `verify_caption_coverage`（**未字幕chunk・wired**） | **実装済(wired)** | **全narration chunkが字幕化されているかhard判定＝『字幕が飛ぶ』の名前のある機構（pass1 MAJOR是正・round4未引用）。** matched_fractionは補助 |
| caption skip=hard-fail＋reliability床 | **要実装(真に新規)** | skipで出荷不可＋windowed＋matched≥0.75（#1/#4）。赤=マスター欠落 |
| `check_longform_drift`（caption_syncの新規拡張） | **要実装(真に新規)** | exact≥84／per-window相対≤0.10／半差≤0.05／スロープ≤0.010／Act5≤0.08／showpiece必須マッチ（#1/#2/#3）。赤=showpiece desync |
| narration v002存在/ index sha一致 | **要実装(真に新規)** | v002在ればexit1＋producer/verifier同一index（#4）。赤=ダミーv002 |
| `caption_narration_match` | 実装済(wired) | 語一致100%＋字幕内デジタル通貨0（#44） |
| `verify_onscreen_text.py` | **実装済(wired・要拡張)** | T群照合（`600`不在・州名断定0・引用逐語含T3'・T16年代ラベル・`Est.`・Hall/HallEquityLadder金額はCLM-0021裏取り後）＋review_factsロケータ前提検査(§1.4)。**pass1 MAJOR是正:配線済SOLID・新規でない。台本==画面しか照合せず架空引用は捕えない→§1.4一次ロケータ＋人手で二重化** |
| `verify_script_structure.py` | **WEAK(偽装耐性限界)** | OL二階建て開閉・再フック≤2:50・二人称≤5:30・new-info・実タイムライン再検査(#42)。**意味判断は偽装可→未回収ループ/構成のhard保証は§12 step3★オーナー台本ロック** |
| `verify_script_lint.py` | **実装済(wired・要拡張)** | 禁止フレーズ＋カデンツ＋二重legalタグ（§2.7/#50）。**pass1 MAJOR是正:配線済SOLID・辞書拡張のみ。** 赤=AI臭文 |
| `check_padding.py` | **実装済(wired)** | 最終レンダの各60秒窓に content-novelty＋audio/motion-energy分散の床、下回る窓でexit1。**pass1 MAJOR是正:配線済SOLID＝『現に走る検出器が皆無』は事実誤りで撤回。** 赤=デッドエア20分 |
| `structure_4part`／`op_ed_bookends` | 実装済(wired) | **★pass3 MINOR#4＝コード実契約を確認して記載（check_final_acceptance.py L432-471）:`structure_4part`は承認済narration section ラベルが HOOK→OPENING→body→ENDING の順で走ることを検証し、body=HOOK/OPENING/ENDING以外の全section（＝幕数非依存）で"body非空"を要求するのみ。したがって本話の5幕body（Act1–Act5）はそのまま受理され false-FAIL しない（4幕ハードコードではない）。film-data jsonがあれば hookSeconds≥8＋hookLine非空も確認。** 8秒フック→OP→body(5幕可)→ED CTA |
| `image_resolution` | 実装済(wired) | 全Codex画像≥3840px |
| `thumbnail_visibility` | 実装済(wired) | サムネYAVG≥33。被写体bbox≥50は下記で別途 |
| `check_thumb_subject_luma` | **実装済(wired・要拡張)** | 被写体bbox YAVG≥50・核トークン可読（§9.2）。**pass1 MAJOR是正:配線済SOLID・新規でない。** 赤=夜間沈みサムネ |
| `freshness` | 実装済(wired) | 全成果物sha≠前回＋mtime |

### 6.2 実物確認（機械緑の後に必須）
`preflight_owner_review.py`で **16枚コンタクトシート＋body_luma＋caption_sync（p50/p90/exact%/per-window median系列＋showpiece手動＋未マッチcueリスト）＋`verify_caption_coverage`未字幕chunk一覧＋章境界と終盤含む音5本試聴＋stem実測LUFS（`check_sound_layers`結果）＋music stemアクティブ率タイムライン（advisory）＋劇伴6ベッド試聴QC＋画像平均輝度＋サムネ縮小プレビュー＋★OP/EDテイスト横並び比較**を生成。**数値＋現物を提示してオーナー承認**（緑≠完成）。**音の相対音量/musicカバレッジ/終盤音/SFXの豊かさは、ドロップ済/WEAKゲートでなくこの人間試聴がhard backstop。**
- **★OP/EDテイスト忠実性の名前のある人間backstop（pass2 MINOR是正・#8）:** `op_ed_bookends`(wired)はBookendの**構造/存在**しか検査せず"既存話と同じテイストか"という質は測らない。よって本review に**参照話（直近published EP）のOP/EDと本話OP/EDを横並びレンダで並置し、オーナーがテイスト一致（配色/タイポ/リズム/ブランド音）を承認**する項目を追加。テイストのhard保証は構造ゲートでなくこの横並びオーナー承認＋`BrandOpening`/`BrandEndcard`再利用コンポーネントに置く（名前のある工程として明示）。

### 6.3 動く実物の必須提示（チェリーピック防止・監査#14/#34）
静止16枚と数値ではモーションの豊かさ・持続性を確認できない。`preflight_owner_review`に：
- **motion-reel（実尺レンダ動画）:** **全19図を最低1回ずつ持続モーション区間ごと**＋各幕先頭＋冒頭4分（0:24–3:40）＋**非hero・非幕頭からの無作為抽出カット一定数**を編集（ヒーローだけの良いとこ取り禁止）。
- **motion_energyの時系列プロット**（12秒窓・p10ライン・全カット母集団・hero除外下位分位）。
静止コンタクトシートだけで「紙芝居でない」と宣言することを禁止。§13 axis4=確定10はこのmotion-reel承認＋motion_energy実測校正で確定。

### 6.4 台本水増しの直接検出（**`check_padding`は配線済み・pass1 MAJOR是正**）
motion_energy/音エネルギーは「フリーズ検出」専用と明記し、20分水増し検出の唯一の裏付けにしない。**pass1是正:round4は「水増し検出が全て要実装で"現に走る"防御がゼロ」と述べていたが、これは事実誤り。`check_padding`は`check_final_acceptance.py`に配線済み（SOLID）＝現に走るpadding検出器は存在する。**
- **`check_padding.py`【実装済(wired)／出荷前hard】が現に走る padding ブロッカー**（§6.1）。最終レンダの各60秒窓に content-novelty（字幕n-gram新規率）＋audio/motion-energy分散の床、下回る窓でexit1。**赤フィクスチャ=デッドエア20分でexit1を実証。** 本話向けは閾値校正のみ（新規実装でない）。
- **new-information-per-scene:** `verify_script_structure.py`【WEAK】が各幕/シーンに新規事実・人物・因果≥1、既出言い換え再掲でフラグ（意味判断はオーナー台本ロックがbackstop）。
- **近接反復検出:** n-gram/文埋め込みで近接反復（同じ主張の再述）を検出。
- **review③全区間適用＋独立実行主体:** `review_pacing.md`の「この60秒を消して物語が成立するか」を著者と別モデル/別サブエージェントが判定し独立provenanceを刻む（§2.7/#33/#39）。
- **§13 axis3のキャップ是正（pass1 MAJOR）:** `check_padding`が配線済みで現に走る以上、axis3を「6(実効未担保)」に据え置く根拠（＝padding検出器の不在）は誤り。**axis3のキャップは撤回し、実在の限界（閾値校正が本話未確定であること）だけを理由に必要なら控えめに留保する。** §13.1で反映。

---

## §7. レンダ規律（reference_remotion_render_ops準拠）
- 仕上げ/書き出しは本Windows PC・クオリティ最優先・CPU(libx264)。NVENC不使用。
- 1本ずつ直列。長尺WebGL/depthは`--concurrency=4`。完走までkillしない。`tail`で進捗を隠さない。健全性はheadless chrome数とCPU。
- レンダ順: ①`test_gate_fixtures.py`（全赤フィクスチャexit1確認・§6.0）→②`preflight_render_gate.py`（計画レベル・未達exit1）→③本レンダ→④**POST-render acceptance（hard=wired）**（`check_image_cut_luma`全539／`motion_energy`実測（wired床mean≥12/p10≥9＋要拡張新統計・bbox-flowはadvisory参考）／`check_arc_nonrepeat`／`check_footage_utilization`／`check_sound_layers`／`check_final_acceptance`音LUFS／`caption_sync`＋`check_caption_format`（機能語行末0の受領側再検査含む・pass3 BLOCKING#2）＋`verify_caption_coverage`＋`check_longform_drift`／`check_padding`）→⑤**WEAK/advisory＋人間backstop**（`verify_sfx_manifest`/`verify_script_structure`/`check_ending_sound`はadvisory、最終は§6.2音5本試聴＋motion-reel＋step3★オーナー台本ロック）→⑥受領書。**🗑ドロップ済(stem_loudness/music_coverage/bbox-flow)は実行しない。**
- Composition基準(brand.ts): fps30/1920×1080。png連番→libx264 CRF16/yuv420p/bt709→AAC320k mux。mux時`audio_mix_sha256`刻印、`freshness`で全成果物sha≠前回確認。
- Git: pull at start／各ステップcommit+push／SSD媒体(H:)・runs/はコミットしない。

---

## §8. 尺の予算（20分・runtime_band 1,170–1,230s）

| 区間 | 尺帯(tc枠) | 秒(tc枠) | VO語数(設計/目標・再集計待ち) | 幕内wpm | 累積 |
|---|---|---|---|---|---|
| Hook | 0:00–0:08 | 8 | 18（§2.3実全文） | — | 0:08 |
| OP | 0:08–0:24 | 16 | 40（§2.4実全文） | — | 0:24 |
| Act1 | 0:24–3:40 | 196 | 505 | 154.6 | 3:40 |
| Act2 | 3:40–6:35 | 175 | 450 | 154.3 | 6:35 |
| Act3 | 6:35–10:20 | 225 | 580 | 154.7 | 10:20 |
| Act4 | 10:20–14:20 | 240 | 620 | 155.0 | 14:20 |
| Act5 | 14:20–19:00 | 280 | 720 | 154.3 | 19:00 |
| ED | 19:00–20:00 | 60（VO約48s＋非VOエンドカード≤12s） | 約124（§2.5実全文） | ~155 | ~20:00 |
| **計** | | **≈1,200s（band中央・20:00固定は撤回）** | **約3,057語（≈3,050・設計/目標）** | **≈155（実際に閉じる）** | band内 |

- **★算術を155wpmで実際に閉じる値へ再接地（pass3 MAJOR#6/#14/#25是正）:** round6のブロック表（Act 520/490/620/645/720＝2,995語 vs 幕tc計1,116s）は~155wpmでは閉じず**実は≈161wpmでしか閉じなかった**（Act2=168・Act3=165が採用帯150–165の上限を突破）。ヘッドラインの「単一wpm~155一本化」が自らの数値で偽になっていた。**是正＝option(b):幕語数を各幕tc内で155wpmに収まる値へ下げる（Act1 505/Act2 450/Act3 580/Act4 620/Act5 720＝各154–155wpm）。** これで幕発話計＝(505+450+580+620+720)/155×60＝**約1,111s**（幕tc計1,116s内）。総VO≈3,057語（Hook18＋OP40＋Act2,875＋ED124）。round4「3,140 vs 3,067二値矛盾」「ED155語」「157wpm逆算」、round5「ED約58語＋非VO約36s」は全撤回。**約3,057は"確定した実全文語数"でなく設計/目標値（script_final.v001の実全文で再集計・§2.1）。**
- **ED実文の再カウント（pass3 MAJOR#6/#25）:** §2.5のED VO実文は約124語＝48s@155wpm（round6「約115語≒44s」は実文の過小カウントで訂正）。
- **非VO予算の単一wpm整合:** 非VOは Hook のSFXブリード＋OP下ブリード＋設計沈黙2×≤1.2s＋エンドカード≤12s＝合計おおむね≤22s。期待wpm≈155で約3,057語＝発話時間≈1,183s＋非VO≤22s＝**≈1,205s（band中央~1,200s近傍・上限1,230s余裕あり）**。**★§8是正指示の訂正（pass3 MAJOR#6）:round6は「Act2/Act5の薄い遷移を圧縮して発話時間を収める」と書いたが、遷移（非VO）の圧縮は"発話時間"を減らせない（発話時間は語数と話速のみで決まる）。是正:帯外なら発話語数を削る（冗長・同義反復のカット）か話速を調整する。** `check_runtime_band.py`実測(1,170–1,230s)を唯一の合否とする。
- **固定語数は帯を保証しない（正直開示）:** 150–165全域を固定語数で保証はできない（floor安全≥3,218/ceiling安全≤3,075で両立不能）ため語数は設計値。帯外は§2.1再ペーシング（上限=発話語数圧縮/同義反復除去、下限=独立レビュー②③が『物語に要る』と判定した素材＝Act3 Hall物語/Act5弁論往復の実質増のみ追加＝水増し禁止）。秒数を出し入れする決定論的reserve/trim表は存在しない（#30撤回済）。
- **20分は物語で満たす。平坦窓ゼロ**を「`motion_energy`12秒窓（凍結専用・wired再校正）＋音の平坦12秒窓検出(§4.5・WEAK advisory)＋台本linter(§6.4 new-info/近接反復)＋**`check_padding`（出荷前hard・配線済SOLID・pass1 MAJOR是正で『現に走る検出器ゼロ』撤回）**」で強制。設計沈黙は2箇所×≤1.2sのみ。9–0を~18:15へ後ろ倒し・coda≤45秒。

---

## §9. OP/ED・サムネ

### 9.1 OP/ED Bookend
- **OP(0:08–0:24・短縮):** PD標準BrandOpening。タイトルT2・サブT3(`598 U.S. 631`)、第1幕の窓の絵/AMB1を先行ブリード。`op_ed_bookends`ゲート。
- **ED(19:00–20:00):** PDクロージング＋登録プロンプト。**earned coda＋EP34具体ティーズのVO（約124語≒48s・§2.5・pass3#6再カウント）でED窓の大半を満たし、静的BrandEndcardは≤12sに圧縮（pass2#24：非VO尺埋めバラストを撤去・20:00固定撤回）。** MB-END/AMB-END固定、切りよくフェード（`check_ending_sound.py`・低域スペクトログラムをオーナー試聴必須）。DoorPlacardStrip＋`NOT HER WINDOW — YOURS.`＋EP34具体ティーズ。**ED末尾窓も`check_padding`（content-novelty＋分散床）と`review_pacing`keep/cut対象＝新規性ゼロの静的窓を作らない。** **coda≤45s・9–0 slam~18:15で勝利〜終幕≤1:45（監査retention#61）。**

### 9.2 サムネイル/CTR設計（実測2.31%→目標6.0%・**単一数字確定・curiosity-gap・監査thumbnail#36–#40/#44–#48**）

**共通ハード床:** 1280×720 PNG24bit／全体YAVG≥33／**被写体bbox局所YAVG≥50【実装済(wired)`check_thumb_subject_luma`・pass1 MAJOR是正:配線済SOLID・新規でない・#48】**（夜間で家が沈むのを検出）／メインコピー白極太≥150px／各テキスト行≤16字／外側黒縁12–16px＋ドロップシャドウ／数字≥190px・コントラスト≥7:1／**320px縮小で「メイン＋数字1つ＋核トークン」判読**／**文字塊≤3・独立金額≤1（画面上の金額表示は最大1つ・#44）**／被写体は物＋匿名フィギュア可（実在肖像のみ禁止）／数字は`$2,300/$25,000/$40,000/9-0`のみ・`600 U.S.`不使用。配色: 警告レッド`#E8341C`／ネイビー`#101A2E→#1E3358`／ゴールド`#F4B63A`／オフホワイト`#F2F0EA`。

**核トークンの単一確定（#39/#44）:** サムネの核＝**`$25,000`（払っていないのに奪われた余剰）**の一点。**複数金額の同時表示は禁止（独立金額≤1）。**

**3案（**単一数字＋curiosity-gap・監査thumbnail-BLOCKING#44/#46**）:**
- **案A【本命・単一数字$25,000】:** メイン`THEY KEPT`（9字）＋巨大`$25,000`（黄・単一独立数字）＋下部赤帯`YOU DIDN'T OWE`（13字）。左35%＝暖色ライトで浮かせた家＋equityバー→赤矢印で$25,000が引き抜かれる図。**独立金額=1（$25,000のみ）で共通床充足。** 二人称`YOU`。（round3案Aの3金額違反を撤回し単一数字へ確定・#44。）
- **案B【A/B当て馬・legality-gap curiosity・#46】:** メイン`THEY TOOK HER HOME`（2行・各≤16字）＋数字近傍に小スタンプ`OVER $2,300 — 100% LEGAL`（単一金額$2,300）。「え、それ合法なの？」の未解決の疑問を作る（事実の断言でなく疑問の提示）。左＝家＋SEIZED札。**curiosity-gap（合法性の逆説）を前面化。**
- **案C【当て馬・authority】:** 巨大`9–0`＋`THE GOVERNMENT LOST`（単一トークン9-0）。全員一致で違憲＝強い可読トークン。予備兼authority軸当て馬。

**A/B軸（1軸に確定・#40）:** primary=案A（$25,000 outrage/二人称）、challenger=案B（合法性paradox curiosity）。**単一の被験変数＝「奪われた金額の理不尽 vs 合法性の逆説」というフック型の1軸**（両案とも独立金額1つ・二人称寄り）。案C予備。

**肖像近似回避（監査thumbnail#47）:** 案の人物シルエットは(1)Geraldine個人を特定させない完全な影/逆光で顔・髪型・体型を判別不能に、(2)実在1999年コンド/実在窓の再現でなく象徴的な家、(3)キャプション/alt/文脈で本人と断定しない。**案D【肖像リスクゼロのフォールバック】=物＋SEIZED札＋$25,000のみ（人物なし）を1案常備。**

**レイアウト実証（#38/#45）:** メインは真の短句（各行≤16字・案Aは"THEY KEPT"9字/"$25,000"7字/"YOU DIDN'T OWE"13字）に固定（round3案Aの16/18字違反を撤回）。**実寸1280×720モックを各案1枚作り、320px縮小で「メイン＋核トークン」判読・字高≥150px/数字≥190px/黒縁≥12pxを実測してからDone。**

**選定・A/B（#40/#48）:** 一次採用=案A、当て馬=案B（1軸）。**`check_thumb_subject_luma`（配線済SOLID）緑をサムネ確定の前提（§12 step15の前）にブロッキング配置。** 被写体が暗背景に沈まない配色（案Aのequityバー＝図形で高輝度）。YouTube Studio Test&Compareを統計的有意（有意水準/最小インプレッション閾値）到達まで走らせ、72h固定確定は撤回。CTRスクレイパーは監視補助。

**タイトル案3（サムネと役割分担・数字重複回避・#40）:**
1. `They Took a 94-Year-Old's Home Over a $2,300 Tax Bill — Then Kept the Rest`（タイトル=人物＋文脈・数字は$2,300のみ、$40,000/$25,000はサムネ側）
2. `The Government Can Legally Keep Your Home Equity — Until One Woman Fought Back`（二人称脅威）
3. `A Small Tax Debt Cost Her Everything. The Supreme Court Ruled 9–0.`
※ タイトル=人物/二人称、サムネ=数字の理不尽 と訴求点を分離し情報重複をなくす。

**Done定義:** 案A/B/D 320px縮小で「メイン＋核トークン」判読／全体YAVG≥33＋被写体bbox≥50実測（`check_thumb_subject_luma`緑）／黒縁≥12px・文字≥150px・数字≥190px／文字塊≤3・独立金額≤1／数字FACTS一致(600不使用)／実在肖像ゼロ・肖像近似回避／`preflight_owner_review`に3枚+輝度数値+320pxプレビュー同梱しオーナー承認。

---

## §10. Codex画像（1話 約64–72枚・狙い68枚・4K）
**根拠:** EP32の40枚/12.5分≈3.2枚/分×20分。EP32据え置き40枚は20分では過少＝禁止。SDXLを勝手に起動しない（画像はCodex／pd-division-of-labor）。
- **枚数確定:** 68枚（±4）。`asset_selection.v001.json`に要枚数/在庫/**QC生存後の不足0**を明記。
- **★画像図案の記録正典＝`EP33_tyler_ai_prompts.v001.md`（68枚確定・存在する・pass3 MINOR#21是正）:** round6は「68枚の図案・割付はまだ具体化されていない／散文の生成対象列挙のみ」と記したが、**実際には完成した姉妹ファイル `episodes/_planning/EP33_tyler_ai_prompts.v001.md`（63KB）が IMG-001–068 を S001–S040 へ割付け、各画像に構図・レンズ・パレット(hex)・ライティング・invariant11準拠の免責を備えた具体プロンプトを持ち、幕別配分も設計の 13/10/16/9/15/5 と厳密一致している**。よって**画像"図案"は具体化済み（ほぼ生成可能）＝設計書だけを読んで「画像未定義」と誤認しないよう、画像図案の記録正典を ai_prompts.v001.md と明示する**。残る真のギャップは image→scene 粒度でなく **image→252 個別still-cut の再利用台帳（`asset_selection.v001.json`）** のみに限定される。
- **★真に残るギャップ＝`asset_selection.v001.json`（68行 image→cut再利用台帳）は未作成＝画像生成前のブロッキング前提成果物（pass3 MAJOR#18・Claude側で先に作る）:** episode配下（`05_visuals`等）は空で、**下流の決定的実装（252 still-cutのcut配置・footage突合キー・preflight/utilization起動）の唯一の束縛入力である `asset_selection.v001.json` が実在しない**。ai_prompts.v001.md（image→scene）だけでは preflight_render_gate が要求する「252 still-cut すべてが有効 image_id にマップ／未マップは exit1」の **image→個別cut 再利用台帳**と、`check_footage_utilization` の final-src 突合キーが欠落する。よって**`ai_prompts.v001.md`（68プロンプト）＋§3.4 cut_plan（539cut）から `asset_selection.v001.json` を実際に列挙生成する**のを画像生成・編集アセンブリの**前**の必須成果物とする（pd-division-of-labor上、これはCodexでなくClaude側の前提成果物）:
  - 各 image_id に **composition/subject/act・割り付く全cut・still→cut再利用数・最終src相対パス**を非空で持たせ、**幕別合計13/10/16/9/15/5と252 still-cutの全マップを機械validate**（252 still-cut はこの68画像から引く・平均~3.7 cut/image・全cutが実在 image_id を参照）。
  - `preflight_render_gate` が **(a) 画像行数=68±4、(b) 幕別合計一致、(c) 252 still-cut すべてが有効 `image_id` にマップ（未マップ still-cut は exit1）、(d) 各 `image_id` の composition/subject フィールド非空、(e) 各footage候補の最終src相対パス非空（utilization突合キー）**を出力前に検証。未達 exit1。
  - `asset_selection.v001.json` が存在・validate するまで画像生成・編集アセンブリに進まない（この台帳が下流の唯一の束縛入力）。
- **規格:** 全4K(3840×2160)・`image_resolution`hard。匿名フィギュア/再現のみ・**実在肖像なし（Geraldine/Hall/判事の実顔は生成しない）**・画面内テキスト無・題材一致・**per-image mean-luma床は生成後の実測YAVGで`check_image_cut_luma`（全539スコープ）がPOST-render判定→未達再生成（#32）。source_YAVGを仮定値で埋めない。**
- **主な生成対象:** 1999年風コンド外観・一貫した匿名高齢女性の窓辺（朝の光リフレイン複数）・空き部屋の郵便受け・senior community・Hennepin郡庁舎/競売・匿名弁護士(PLF長机)・**Hall事件の匿名フィギュア（性別中立/別視覚アイデンティティ・裏取り後にCLM-0021整合・勝訴の文脈）**・Southfield風の家と$1移転/$308k転売の象徴・Runnymedeの草原・マグナカルタ巻物(1215)・後代英議会制定法の象徴（Overplus・1215と別ビジュアル・#51）・大理石法廷・全米各地の匿名の家々のドア(SEIZED札着脱)・StateMap下地。
- **幕別配分(目安):** Act1 ~13／Act2 ~10／Act3 ~16／Act4 ~9／Act5 ~15／Hook+OP+ED ~5。graphics図は別カウント。
- **3話アーク:** 本話画像・footageの元アセットIDを計画台帳`catalog_fingerprints.json`（advisory・ゲート入力でない）に記録して三部作のクリップ分配を管理。実際のレーン分離hardは、EP34/EP35のacceptance時に`check_arc_nonrepeat`が本話確定`tyler_film.json`の cut src basename と交差=0を判定して担保（§12 step13.5・pass2 BLOCKING是正）。
- **中立性:** 郡/裁判所は中立・事実記述の説明ビジュアル。本物の記録として提示しない。

---

## §11. 失敗モード → "名前のある機構"（**実装状態を三分＋赤フィクスチャ・過去失敗＋20分水増し＋round3新規**）

| # | 過去失敗 | 名前のある止める機構 |
|---|---|---|
| 1 | 字幕≠ナレ/遅い | 逐語narration_index源＋強制整列＋【実装済(wired)】`caption_narration_match`＋`verify_caption_sync`(p90/median/matched)＋【要実装】skip=hard-fail＋`check_longform_drift`exact≥84（§5.0） |
| 1b | **字幕が飛ぶ(未字幕chunk)** | **【実装済(wired)】`verify_caption_coverage`＝全ナレchunk字幕化のhard判定（pass1 MAJOR是正・round4未引用）。matched_fractionは補助（§5.6）** |
| 2 | 字幕が変な所で切れる | 【実装済(wired)】`check_caption_format`≤10語/≤50字/≤2行/≤27cps/≤7s＋**【要実装/本話ブロッキング・pass3 BLOCKING#2】機能語行末0を受領側hardゲート化＝`check_caption_format`拡張(or `check_caption_dangle`)で最終shipped SRTを独立再検査しexit1＋赤フィクスチャ（producer自己検査`_NO_DANGLE_END`だけに依存しない）**＋またぎ禁止をシーン境界に限定（§5.2/5.3） |
| 3 | 8:45以降ドリフト | 【実装済】per-min median max≤0.50＋【要実装】`check_longform_drift`基準非依存(per-window相対/半差/スロープ/Act5/showpiece必須)＋narration_index ドリフトフリー不変条件＋v002封鎖（§5.0/5.1・**-0.60誤アンカー撤回#1**） |
| 4 | DL素材が使われない | 【実装済(wired)】span束縛＋`footage_diversity`＋`check_footage_utilization`(配線済・要拡張)未使用≤20%(=使用率≥80%・単一床#10)＋選定広さ≥39/実配置≥32（分母操作封鎖#36）＋供給床も32に統一（[26,31]解消・#9） |
| 5 | 構成ズレ | 【実装済(wired)】`structure_4part`＋`op_ed_bookends`＋【WEAK】`verify_script_structure`（実タイムライン再検査#42・意味判断はstep3★オーナー台本ロックがbackstop） |
| 6 | OP/EDが違う | 【実装済(wired)＝構造のみ】`op_ed_bookends`（テイスト質は測らない）＋`BrandOpening`/`BrandEndcard`再利用＋**★§6.2で参照話OP/EDとの横並び比較をオーナー承認（テイスト忠実性のhard backstop・pass2 MINOR是正・#8）**（§9.1/§6.2） |
| 7 | 紙芝居(図少ない) | FigureBeats≥10かつ各幕≥4＋時間分布床＋ヒーロー時間分布床＋【実装済(wired)再校正】`motion_energy`(still-p10≥17=⌈0.35×46.6⌉・台帳床≥12/≥9の引上げ)＋§6.3 motion-reel全図網羅の人間承認（**bbox-localフロー＝ドロップ済`check_motion_bbox_flow`ゆえhard保証にせずadvisory参考のみ・pass1 BLOCKING是正**）（§3.2/3.8/6.3） |
| 8 | 周回淡い光うざい | Aurora/LightRaysをL0/L1ベッド限定・各シーン方向性モーション必須＋motion-variety(entropy≥1.5/CV≥0.25接地)＋VoteTally薄暗ホールド撤廃（§3.8） |
| 9 | lowerthird左見切れ | セーフ矩形x∈[160,1760]＋`safeInset=96`bbox外FAIL（§3.9/5.5） |
| 10 | 疎な図 | 最低ノード機械チェック、StateMap点灯12（≥12）（§3.9） |
| 11 | 図背景/画面が暗い | SceneBed hex暗端/四隅/breath最暗位相逆算＋bed_factor/grain_factor確定＋【実装済(wired)再校正】`check_body_luma`(YAVG<38,≤8%)＋【実装済(wired)要拡張】`check_image_cut_luma`全539(per-cut≥52/四隅≥46/暗連鎖≤6s/スクリム検査・pass1 MAJOR是正:配線済SOLID)（§3.1/3.7・#17-25） |
| 12 | 無意味フィラーSFX | 【WEAK】`verify_sfx_manifest`無タグ検出＋連続テクスチャ床を密度カウントから除外（advisory）＋**§6.2音5本試聴でフィラー混入をオーナーがhard承認**（§4.4） |
| 13 | SFX種類少ない/違和感/単調遷移 | 【実装済(wired)】`check_sound_layers`distinct SFX≥12/beds≥4＋本話distinct20/base_id≥14／遷移distinct≥4×2ピッチ・単一使用≤15%・連続同一≤2は【WEAK】`verify_sfx_manifest`advisory＋音5本試聴（#26）（§4.4） |
| 14 | 終盤の変な音 | 【WEAK】`check_ending_sound`roar複合/平坦12秒窓(advisory)＋MB-END-ALT＋**§6.2 ED音オーナー試聴がhard backstop**（§4.5） |
| 15 | 天秤等汎用素材再利用 | 【実装済(wired)】`footage_diversity`(全cut src≤2)＋`--exclude-subtype`＋graphic_symbol機械集計(種類≤2・各≤3回#10)＋抽出後人手全削除（§3.6） |
| 16 | 棚ラベル破損 | ラベル付きコンタクトシート初回目視＋QC後縮小前提の決定論的供給フォールバック(レーン排他#8)＋供給床=QC生存distinct≥32(実映像・#9整合)（§3.6） |
| 17 | サムネ地味 | **単一数字$25,000案A（3金額違反撤回#44）**＋curiosity-gap案B(合法性#46)＋文字塊≤3・独立金額≤1＋各行≤16字＋320px実測＋被写体bbox≥50＋A/B有意到達（§9.2） |
| 18 | AI臭い | 【実装済(wired)要拡張】`verify_script_lint`(カデンツ3連/劇的アイロニー言い換え/二重legalタグ#50・辞書拡張のみ)＋独立実行主体3レビュー(実質列挙#39)＋台本首尾インライン＋ED三段/Act1アイロニー書換＋step3★オーナー台本ロック（§2.5/2.6/2.7） |
| 19 | SDXL勝手起動 | 画像はCodexのみ（§10） |
| 20 | 緑≠完成 | hardゲート緑＋**全要実装/要拡張ゲート赤フィクスチャexit1実証(#32)**＋動く実物motion-reel(全図網羅)＋実物目視/試聴＋オーナー確認（§6.0/6.2/6.3） |
| 21 | 偽の緑(古い良品) | 【実装済(wired)】`freshness`＋`audio_mix_sha256`一致＋字幕をマスターshaに紐付け再整列（§4.6d/5.6） |
| 22 | 薄い音で緑 | 【実装済(wired)】`check_sound_layers`(distinct SFX≥12/beds≥4は**provenance自己申告＋mux sha束縛**・波形実測はonset/ambienceのみ・pass2 BLOCKING是正)＋`check_final_acceptance`2-pass -14実測＋**VO区間相対音量/musicカバレッジ/SFX可聴性は§6.2音5本試聴＋stem実測提示の人間backstop（stem_loudness/music_coverageは実在するが未配線ゆえ引用しない）**（§4.1/4.2） |
| 23 | 尺外れ | 【実装済(wired)】`check_runtime_band`実測1,170–1,230s（§8） |
| 24 | ゲート最適化(グッドハート) | `motion_energy`再校正で引上げ(#33)＋±8f除外＋`check_padding`配線済出荷前hard(#35)＋音実測は`check_sound_layers`＋exact床下げ禁止(#41)（§3.8/6.4/4.4） |
| 25 | 20分を水増しで稼ぐ | 【実装済(wired)/出荷前hard】`check_padding`(60秒窓content-novelty＋分散床・デッドエア検出・**pass1 MAJOR是正:配線済＝『現に走る検出器ゼロ』撤回・axis3キャップ撤回**)＋`verify_script_structure`new-info＋近接反復＋review③独立主体全区間（§6.4/§8） |
| 26 | 誤情報(600/IJ/州名/州数捏造) | 【実装済(wired)要拡張】`verify_onscreen_text`(`598`存在/`600`不在/counsel=PLF/州名0/PLF=Est.・配線済SOLID)＋StateMap点灯=PLF実列挙12(50−36撤回)＋「36」は意見本文確認後のみ＋**焼込逐語は§1.4一次ロケータ必須（架空引用対策）**（§1/§5.4/#42） |
| 27 | 個人回収の誤断定 | EDは全米ルール回復に着地、`NOT HER WINDOW — YOURS.`、Tyler本人回収非断定＋OL1を系統的問いへ(#55)（§2.5/§2.2/§5.4） |
| 28 | 三人称サムネ | 案A=$25,000二人称＋案B=合法性curiosity・タイトル一次案も人物/二人称（§9.2） |
| 29 | 話またぎ素材被り | 【実装済(wired)】`check_arc_nonrepeat`(**他話film.json cut src basename交差=0・`catalog_fingerprints`は読まない**・配線済SOLID)＝**既定は法廷/庁舎も完全分離(方針A・棚に3話分distinct確保を§12 step7で先に検証)**。identical共有が要るならallowlist引数を新規実装(方針B・要実装)。**round5の"アーク共有で交差判定除外"はno-opゆえ撤回・pass2 BLOCKING是正**＋footage_diversityは単一話専用と正直注記（§3.6） |
| 30 | climax後の離脱崖 | 9–0を~18:15後ろ倒し・coda≤45秒・13:20 GovtArg崩壊hero/史料をGeraldine具体とintercut/16:40口頭弁論対決を前倒し（§2.2/#61） |
| 31 | Act3中だるみ | Hall記録準拠ミニ物語(**勝訴・史実準拠#49**)＋決着ビート9:40でループ閉＋EquityTheftTally heroマップ(Act3昇格#15)＋生統計≤45秒（§2.2/§3.0） |
| 32 | 偽サスペンス(9–0既出) | Act4をHOW/WHY・郡の最強論を一瞬信じさせGovtArgumentCard崩壊で崩す（§2.2） |
| 33 | 30秒窓を非物語で消費 | OP16秒短縮＋下ブリード＋Hookは核ネタバレせず前半ミステリー温存(#52)＋**Act1 1:50 slam早期ペイオフ(#56)**（§2.2/2.3） |
| 34 | 匿名で人物愛着が薄い | 一貫匿名フィギュア＋感覚ディテール＋Act1に感情ミニペイオフ（§3.2/§10） |
| 35 | Hall事実誤り(実在私人不正確) | 【本文全面書換】**Hall=第6巡回で勝訴に修正(#49)**・CLM-0021新設・裏取り前は`another homeowner`匿名・review_facts line-item照合（§1/§2.6） |
| 36 | Hookネタバレ/語数超過 | Hookは$40,000/$25,000を出さずEquityBar 4:50初出し＋**実語≤18(#52/#60・#13で立ち退き誤認語も撤去)**＋ElevenLabs実尺≤8s確認（§2.2/2.3） |
| 37 | ペイオフ飢餓(13–18分) | 13:20崩壊/intercut個人化/16:40対決＋SplitLadder 11:15再フック(#57)＋review③最優先適用（§2.2） |
| 38 | 二人称休眠 | 二人称ビート台帳 0:24(賭け金)/**①2:40**/**②6:10**/**③9:00**/**④12:00(Act4新設)**/**⑤15:30(Act5新設)**/18:40(転回)＝**脅威ビートは①〜⑤の5本（§2.2と同一採番・pass2 MINOR是正：round5でここが①0:24〜⑦18:40と別採番になり"新設④⑤"がずれていた不整合を統一）**＋**14:20マグナカルタ三人称叙述の誤計上撤回・真の空白9:40を解消(pass1 BLOCKING)**＋【WEAK】`verify_script_structure`無出現≤5:30(実タイムライン再判定・advisory)＋step3★オーナー確認（§2.2） |
| 39 | 未回収ループ(Hall/OL5) | OL5本の`[OLn-OPEN/CLOSE]`ペア＋**二階建て回収検査(主アークOL1/OL2/OL5はEDまで/短距離OL3/OL4は同幕内・pass1 BLOCKING是正で正典台本を自らブロックしない)**＋Hall決着9:40＋【WEAK】verify_script_structure＋step3★オーナー確認（§2.2/2.7/#53） |
| 40 | マグナカルタ誤帰属 | 【本文分割】CLM-0014A(residue/1215 ch.26)とCLM-0014B(Overplus/後代制定法)を別チップ・別年代ラベル(#51)＋Act5冒頭時系列分離＋verify_onscreen_text年代照合（§1/§2.6/§5.4） |
| 41 | 個人回収bait-and-switch | OL1を系統的問い(#55)に開き替え、個人回収を約束しない・EDは全米ルール回復（§2.2/2.5） |
| 42 | stub緑(要実装ゲートの空実装) | 【出荷前hard】全要実装ゲートに赤フィクスチャ＋`test_gate_fixtures.py`(#32)（§6.0/§7） |
| 43 | 床フィット(自作物/前作に合わせた床) | `motion_energy`は台帳床(≥12/≥9)からの引上げ再校正(#33)＋exact床≥84据置(#41)＋ending検出器は独立ラベルで凍結(WEAK・#34)（§3.8/§5.0/§4.5） |
| 44 | **ドロップ/WEAKゲートを自動保証と誤引用** | **実ゲート台帳と1対1照合。stem_loudness/music_coverage/motion_bbox_flowは"実在するが未配線"＝引用禁止→`check_sound_layers`(distinct/bedsは自己申告＋sha束縛)/`motion_energy`(wired)＋人間試聴/motion-reelに差替。WEAK(sfx_manifest/script_structure/ending_sound)は完全自動保証にせず人間backstop併用（pass1 BLOCKING×3＋pass2で"存在しない"→"未配線"事実訂正・sound_layers能力の過大主張撤回）** |
| 45 | **配線済ゲートを『要実装』と誤ラベル→二重実装/過小申告** | **image_cut_luma/arc_nonrepeat/footage_utilization/onscreen_text/thumb_subject_luma/check_padding/motion_energy/verify_script_lint/caption_coverageは全て配線済SOLID＝【実装済(wired)要拡張/校正】に訂正（invariant14二重実装回避・§13.2実効点も再計上・pass1 MAJOR是正）** |
| 46 | **焼込逐語が架空/誤記憶でも出荷** | **onscreen_textは台本==画面しか照合せず架空引用を捕えない→CLM-0012/0013/0014Aを§1.4 recheckに一次出典ロケータ必須で追加、ロケータ未解決は焼込禁止（引用符外し/カット）・人手二重化（pass1 BLOCKING是正）** |

---

## §12. 実行順序（決定論＋オーナーゲート）
★=オーナーゲート。

1. **リポジトリ同期:** git pull。
2. **§1事実確定:** grade B/要確認をrecheck(§1.4)。`600→598`・`IJ→PLF`・**Hall=勝訴/女性/匿名(CLM-0021裏取り)**・**CLM-0014A/B分割**・州数「36」意見本文確認・StateMap=PLF12州を全参照に反映。**★焼込逐語(CLM-0012 Gorsuch/CLM-0013 Roberts/CLM-0014A residue)を一次意見本文で存在確認し、review_factsにロケータを刻む。ロケータ未解決の引用は焼込禁止＝言い換えかカット（pass1 BLOCKING）。**
3. **★台本ロック:** script_final.v001（**約3,050語・設計/目標値＝実全文で再集計待ち（pass3 MINOR#7）**・**独立実行主体3レビュー成果物（別モデルprovenance＋実質列挙#39）**・首尾インライン・Hall勝訴史実準拠・二人称ビート②6:10/④12:00/⑤15:30の実インラインVO含む）をオーナー確認。`verify_script_lint.py`（wired・カデンツ/アイロニー/二重legalタグ）/`verify_script_structure.py`（WEAK・OL二階建て開閉・二人称間隔・new-info・レビュー独立性）緑＋赤フィクスチャexit1。**★このstep3オーナー台本ロックが、WEAKなverify_script_structureでは保証しきれない『未回収ループ/構成/二人称ビートが真に二人称か/AI臭』のhard backstop（機械緑だけで通さない）。**
4. **narration生成（ドリフトフリー不変条件）:** chunk個別レンダ→固定無音ビートでmaster concat→`narration_index.v001.json`(累積ffprobe実測+ビート)→**per-chunk±30ms＋v002不在＋producer/verifier同一index sha**assert。
5. **ElevenLabsドラフト:** 実測wpm→§8再算出→`check_runtime_band`帯内確認。帯外は§2.1再ペーシングでstep3へ。**verify_script_structure間隔検査を実タイムラインで再実行(#42)。**
6. **scene_plan/remotion_plan生成:** 40シーン・539カット・19図・**depth 238（内訳フラグ実数一致）**・各幕アクティブ図≥4・ヒーロー6＋時間分布・時間分布床をJSON化。
7. **素材抽出＋★目視QC:** テーマ個別実行(`property_home`/`documents_paper`＋legal_court非汎用subtype補助)→マージ→**gavel/scale系人手全削除**→`build_footage_contact_sheet.py`オーナー目視→**QC生存数で不足0再計算・不足時レーン排他フォールバック（供給床=QC生存distinct≥32・実映像・[26,31]デッドゾーン解消）**。選定広さ≥39/≥3テーマ確認。
   - **★法廷/庁舎共通institutional素材の3話分配＝EP33が消費する前の出荷前hard前提（pass3 MAJOR#20是正・"未検証で合格"を禁止）:** 実配線`check_arc_nonrepeat`は他話 film.json の cut src basename と交差=0を無条件hard強制し、header行5「EP34/35と素材完全分離」も完全分離を要求する。EP33/34/35は3話とも法廷/連邦庁舎/最高裁b-rollを必要とする同種被写体で、MEMORY『factory棚ラベル全面破損(evidence_bag=カートゥーン)』かつ§3.6が legal_court を汎用象徴飽和で補助降格している以上、**3話分＝QC生存 distinct clip を≥3×保持しているかは現実にリスクがあり未検証**。よって**EP33が共有系institutionalテーマを消費する前に、ラベル付きコンタクトシートで目視QC後の distinct 生存数を実測し、3話分（法廷/庁舎で各≥3×）を満たすかを先行検証する（step7のこの実測を出荷前ブロッキング前提とする）。満たさなければ各話別ショット（近縁theme再抽出＋Codex 4K再現）を EP33/34/35 に事前割当してから着手する。実データで≥3×を確認するまで、レーン非重複は『計画上OK・未検証』とし合格にしない**（共有allowlistの方針Bを採る場合のみ§14-3の要実装作業として別途）。
8. **Codex画像生成:** 68枚・4K・匿名/肖像なし/画面内テキスト無。**生成後実測YAVGを減衰式に投入。**
9. **音制作:** MB0–5/END/END-ALT・AMB base6・SFX 20 distinct(base_id≥14)＋遷移8＋変種。`sfx_manifest.json`(base_id/tag/bound_event)。stem個別WAV＋sha。2-pass -14 master・provenance＋`audio_mix_sha256`。**マスターを`06_voice/master/vc_master_v001.mp3`＋測定用`.wav`に配置（§5.0-A）。**
10. **字幕強制整列:** faster-whisper medium.en→`pack_captions.py`→captions.srt。`check_caption_sync`＋skip=hard-fail＋`check_longform_drift`(exact≥84/showpiece必須)＋`check_caption_format`(≤10語/≤50字＋**機能語行末0の受領側再検査・pass3 BLOCKING#2**)＋`caption_narration_match`＋`verify_onscreen_text`緑。
11. **★赤フィクスチャ検査＋preflight_render_gate:** `test_gate_fixtures.py`全緑(全要実装ゲートがバッドでexit1・§6.0)→preflight(深度238/各幕図≥4/ヒーロー時間分布/平均2.23s/span束縛/象徴種類≤2・各≤3回)。未達exit1。
12. **本レンダ:** §7規律。mux＋sha刻印。
13. **★POST-render acceptance（実バイト測定・hard=wired）:** `check_image_cut_luma`全539(per-cut/四隅/breath)／`motion_energy`(wired床mean≥12/p10≥9＋要拡張新統計)＋motion-variety（bbox-flowはadvisory参考）／`check_arc_nonrepeat`(他話film.json basename交差=0・catalog_fingerprintsは読まない)／`check_footage_utilization`／`check_sound_layers`／`check_final_acceptance`音LUFS／`caption_sync`＋`check_caption_format`(機能語行末0の受領側再検査・pass3 BLOCKING#2)＋`verify_caption_coverage`＋`check_longform_drift`／**`check_padding`(デッドエア検出・配線済#35)**。**WEAK(verify_sfx_manifest/verify_script_structure/check_ending_sound)はadvisory。🗑stem_loudness/music_coverage/bbox-flowは実行しない。** 未達→再レンダ/再生成。全hardゲート緑＋`freshness`。
13.5 **クリップ分配台帳の更新（実ゲート挙動に接地・pass2 BLOCKING是正）:** 実配線`check_arc_nonrepeat`は**他話の`*_film.json` cut src basename＋`remotion/public/<slug>/`メディアを直接読んで交差=0を判定し、`catalog_fingerprints.json`は読まない**。よって「catalog_fingerprintsに加算→EP34/35が読む」という round5のデータフローは実ゲートと不一致ゆえ撤回。実際の話またぎ保証は、**EP34/EP35のacceptance時に`check_arc_nonrepeat`がEP33の確定`tyler_film.json`を比較対象として列挙し、同一 cut src basename があればFAIL**することで成立する（EP33側は最終`tyler_film.json`をpushして参照可能にするだけでよい）。`catalog_fingerprints.json`は**三部作のクリップ事前分配を人手管理する計画台帳（advisory）**として維持し、ゲート合否入力とはしない。
14. **★preflight_owner_review提示（音/構成/終盤のhard backstop）:** 16枚コンタクト＋**motion-reel(全19図＋非hero無作為)＋motion_energy時系列**＋body_luma＋caption_sync(p50/p90/exact%/per-window＋showpiece手動＋未マッチcue)＋`verify_caption_coverage`未字幕chunk＋音5本試聴＋stem実測(`check_sound_layers`)＋music stemアクティブ率(advisory)＋劇伴6ベッド試聴＋輝度＋サムネ3枚320px。**数値＋動く現物を提示してオーナー承認**（緑≠完成）。**ドロップ/WEAKゲートで塞げない音・構成・終盤・SFX豊かさは此処が人間backstop。**
15. **サムネ確定＋A/B:** `check_thumb_subject_luma`(配線済SOLID)緑を前提に案A一次・案B当て馬。Studio Test&Compareを有意到達まで。
16. **★公開/予約:** オーナーGO後。ショート切出し1本(YT/TikTok 2版・1日1本12:00 JST・空き日監査)。
17. **retro:** 公開後CTR＋scene-level retention→pd-retro学習ルール。

---

## §13. honest スコアカード（**設計完全性と実効ゲートの二本立て・単一100/100撤回・監査gaming-MAJOR#40**）

**採点原則: 裏付けの無い軸を確定10点にしない。水増しは0点。各軸の根拠を【実装済(wired)/WEAK/要実装/自己申告/🗑ドロップ済】の実ゲート台帳ラベルで明示し（ドロップ済は根拠にしない・WEAKは人間backstop併用）、実装/校正待ちの軸は「10(設計完全性・実行前)」と表記。単一の"100/100"を看板にせず、以下の二つの総合点を並記する。**

### 13.1 設計完全性スコア（この設計書という成果物の完成度）

| # | 軸 | 満点根拠（本話具体値＋機構・実装状態） | 設計完全性 | 確定条件 |
|---|---|---|---|---|
| 1 | 事実正確性 | CLM台帳・一次出典・grade・シード誤り訂正(598/PLF/**Hall=勝訴CLM-0021**)・**CLM-0014A/B分割(#51)**・州数「36」焼込は本文確認後・StateMap=PLF12(捏造撤回・"a dozen"整合)・【実装済(wired)要拡張】`verify_onscreen_text`＋**焼込逐語の一次ロケータ必須(§1.4・架空引用対策)** | 10 | recheck完了＋一次ロケータ解決＋onscreen_text緑 |
| 2 | 台本品質 | 約3,050語(実全文接地)・独立実行主体3レビュー(別モデルprovenance＋実質列挙#39)・首尾/Hook/OP/EDインライン・OL二階建て開閉・再フック≤2:50・二人称≤5:30(実体ビートのみ)・【実装済(wired)要拡張】`verify_script_lint`(カデンツ#50)＋【WEAK】`verify_script_structure`＋step3★オーナー台本ロック(意味判断のhard backstop)・AI臭句撤去 | 10 | linter/structure＋赤緑＋オーナー台本ロック＋wpm帯内 |
| 3 | 尺の正しさ | 約3,050語・~155wpm校正・再ペーシング(尺合わせ撤回)・【実装済(wired)】`check_runtime_band`・**【実装済(wired)/出荷前hard】`check_padding`(配線済＝現に走る・pass1 MAJOR是正でキャップ撤回)** | **9→10(条件)** | **check_padding閾値を本話校正して緑まで軽微留保(round4の6キャップは『検出器不在』の誤前提ゆえ撤回)** |
| 4 | モーション/見ごたえ | シーン40・カット539・平均2.23s・depth44.2%(238/539余裕#18)・FigureBeats19(distinct18)/各幕≥4/ヒーロー6時間分布(#15)・【実装済(wired)】`motion_energy`引上げ再校正(still-p10≥17・台帳床≥12/≥9)/motion-variety/§6.3 motion-reel全図網羅(bbox-flowはadvisory参考・ドロップ済ゲート引用せず) | 10 | motion_energy再校正＋motion-reel承認 |
| 5 | 音設計 | 4層・distinct20/base_id≥14・遷移distinct≥4(#26)・ambience6・【実装済(wired)】`check_sound_layers`(distinct≥12/beds≥4は**provenance自己申告＋mux sha束縛**・波形実測はonset/ambienceのみ＝pass2 BLOCKINGで"実mix解析"の過大主張撤回)＋`check_final_acceptance`2-pass -14・**SFX可聴性/豊かさ/VO区間相対音量/musicカバレッジ/終盤音は§6.2音5本試聴の人間backstop（axis5の10はこの人間承認＋自己申告sha束縛が根拠であり"実mix波形解析"に依拠しない）**・「専属スコア級」撤回(stem_loudness/music_coverageは実在するが未配線ゆえ引用撤回・WEAKの sfx_manifest/ending_soundは補助) | 10 | `check_sound_layers`緑＋音5本試聴オーナー承認 |
| 6 | 字幕 | 逐語源＋ドリフトフリー不変条件(v002封鎖/per-chunk±30ms/MP3 priming)＋強制整列・【実装済(wired)】p90/median＋**`verify_caption_coverage`(未字幕chunk・pass1 MAJOR是正で明示)**・**【要実装/本話ブロッキング】機能語行末0の受領側hardゲート化(`check_caption_format`拡張・pass3 BLOCKING#2＝producer自己検査依存から独立検査へ)＋skip=hard-fail＋`check_longform_drift`基準非依存(-0.60誤アンカー撤回#1)＋showpiece必須(#2)＋≤10語producer整合(#3)** | 10 | 機能語行末受領側再検査＋skip封鎖＋longform_drift＋caption_coverage緑＋赤緑両実証 |
| 7 | 品質ゲート/Done | §6.1三分表(実ゲート台帳と1対1)＋**§6.0赤フィクスチャ(#32)**＋動く実物motion-reel＋実物目視/試聴＋オーナー確認＋`freshness`＋台本水増し直接検出＋ドロップ/WEAK/自己申告ゲートの正直降格 | 10 | 要実装/要拡張ゲート＋赤緑両実証＋人間backstop |
| 8 | サムネ/CTR | 単一数字$25,000案A(3金額違反撤回#44)・curiosity-gap案B(#46)・各行≤16字(#45)・文字塊≤3/独立金額≤1・320px実測・【実装済(wired)】`check_thumb_subject_luma`被写体bbox≥50・肖像近似回避(#47)・A/B有意到達 | 10 | モック320px実測＋thumb_subject_luma緑 |
| 9 | Codex画像 | 68枚(**per-image台帳は未作成＝画像割付は未具体・pass2#35正直表示**)・4K・全span束縛・匿名/肖像なし・【実装済(wired)】`check_image_cut_luma`per-image実測POST-render(全539#20)・【実装済(wired)】`check_arc_nonrepeat`他話film.json basename交差=0(既定=完全分離方針A・catalog_fingerprintsは読まない・共有allowlistは要実装方針B)・SDXL不使用 | 9(設計・asset_selection未作成/arc allowlist要実装で軽微留保) | asset_selection 68行台帳作成＋image_cut_luma校正＋赤緑両実証 |
| 10 | 失敗モード網羅 | §11に46失敗モード×名前のある機構(過去全＋20分水増し＋Hall事実誤り＋stub緑＋床フィット＋マグナカルタ誤帰属＋bait-and-switch＋**ドロップ/WEAKゲート誤引用＋配線済誤ラベル＋架空焼込引用**)・実ゲート台帳と1対1で実装状態を明示 | 10 | — |

**設計完全性 総合 ＝ 98/100（axis3を本話閾値校正待ち・axis9をasset_selection未作成/arc allowlist要実装で各軽微留保・残8軸=10・round7でも据置）。** **pass3監査25件（BLOCKING2＋MAJOR7＋MINOR16）を追加反映＝機能語行末0の受領側hardゲート化(要実装昇格)／6:10二人称ビートの実VO新設／語数を155wpmで実際に閉じる約3,050語へ再接地(Act2 168/Act3 165の上限超解消・§8是正指示を発話語数削減へ訂正)／Hook・Act1の居住ドラマをCLM-0003へ整合／ai_prompts.v001.md=画像図案正典＋asset_selection.v001.json=画像生成前ブロッキング前提の明確化／未実装ゲートの実効降格の正直明記／法廷庁舎素材3話分配のstep7出荷前hard前提化／motion_energyのstill-p10/medianを新統計要拡張と正直ラベル／§1.1 PLF-Est.カーブアウト／§3.10 preflightにマップ最低ノード・字幕safe-rect明示／structure_4part実契約(5幕body受理)確認記載／verify_script_lint辞書拡張＋固有名詞密度／§4.2 music存在=SOUND_PROV_MIN_MUSIC=1で担保の正確化／footage使用率単一床化／§3.0総尺セル・Act4役割セル・OL2順序の整合。** pass2監査31件（BLOCKING3＋MAJOR11＋MINOR17）を反映し、**`check_final_acceptance.py`の実挙動（L1086 sound_layers=自己申告＋sha束縛／L134-148 motion_energy定数／L229-230 body_luma定数／arc_nonrepeat=basename交差・catalog非読取／_ext_gate配線リスト）に接地して**、sound_layers能力の過大主張・ドロップ済ゲートの"存在しない"誤断定・per-episode校正の実装不能・ED尺埋め・arc共有除外のno-opを是正した。pass1監査34件（BLOCKING/MAJOR20＋MINOR14）を該当セクションに反映し、**実ゲート台帳と1対1で照合**して、(a) ドロップ済ゲート(stem_loudness/music_coverage/motion_bbox_flow)の引用を全撤去し実在の`check_sound_layers`/`motion_energy`＋人間試聴/motion-reelへ差替、(b) 配線済SOLIDゲート(image_cut_luma/arc_nonrepeat/footage_utilization/onscreen_text/thumb_subject_luma/check_padding/motion_energy/verify_script_lint/caption_coverage)の『要実装』誤ラベルを『実装済(wired)要拡張/校正』へ訂正、(c) WEAKゲート(sfx_manifest/script_structure/ending_sound)を完全自動保証から降格し人間backstop併用、(d) OL回収の内部矛盾・二人称ビートの実体欠落・焼込逐語の一次ロケータ欠落・語数算術破綻を是正した。**round4の「axis3を6にキャップ」は『padding検出器が現に走っていない』という事実誤りに基づくため撤回（`check_padding`は配線済）。**

### 13.2 実効ゲートスコア（"今この瞬間に現に走って測る"ゲートだけで採点・配線済ゲートを正しく計上）

**pass1是正:round4は配線済SOLIDゲートを『要実装』と誤ラベルして実効点をゼロ計上し過小申告していた。実ゲート台帳の配線済ゲートを正しく計上して再算出:**

| 軸 | 現に走る実測ゲート(wired) | 実効点/10 |
|---|---|---|
| 1 事実 | **`verify_onscreen_text`(配線済・600不在/州名/Est.)** | 6 |
| 2 台本 | structure_4part/op_ed_bookends＋**`verify_script_lint`(配線済)** | 6 |
| 3 尺 | check_runtime_band＋**`check_padding`(配線済・pass1是正)** | 7 |
| 4 モーション | **`motion_energy`(配線済・要引上げ校正)** | 6 |
| 5 音 | **`check_sound_layers`(配線済・distinct≥12/beds≥4は自己申告＋mux sha束縛、波形実測はonset/ambienceのみ)**＋2-pass LUFS実測 | 6 |
| 6 字幕 | check_caption_sync＋**`verify_caption_coverage`(配線済)**(exact/sk12は要拡張) | 7 |
| 7 Done | freshness/mux sha一致＋**`check_padding`/`check_image_cut_luma`(配線済)** | 6 |
| 8 サムネ | thumbnail_visibility＋**`check_thumb_subject_luma`(配線済)** | 6 |
| 9 画像 | image_resolution＋**`check_image_cut_luma`/`check_arc_nonrepeat`(配線済)** | 7 |
| 10 失敗網羅 | 設計＋配線済ゲート群 | 5 |
| **実効合計** | | **62/100** |

**この62/100が"今の配線済ゲートで現に走る守り"（round4の40はSOLIDを0計上した過小申告で誤り）。98と62の差＝要実装(caption skip/longform_drift/showpiece/v002封鎖＋motion/luma override＋機能語行末受領側再検査＋arc allowlist採用時)の実装＋配線済ゲートの本話閾値校正/拡張＋赤フィクスチャ＋人間backstopで埋める。単一の"100/100"は掲げない（#40）。**

**★未実装ゲートの実効降格の正直明記（pass3 MAJOR#19）:** 本設計が語る"本話だけの厳しい床"の幾つかは**現状のacceptanceでは走らない**。出荷前にClaude側で実装・赤緑両実証しない限り、実レンダは以下の**より緩い実効床**で判定される事実を降格記載する:
- **motion_energy:** 本話目標 still-p10≥17/median≥18 は `measure_motion_energy` への新統計追加＋`manifest.json` の `motion_floor_override` 実装（未着手）が前提。未実装なら**実効は台帳既定＝body within-shot mean≥12／全body p10≥9**で走る（stills限定p10・medianは未計測）。
- **check_body_luma:** 本話目標 YAVG<38/FRAC<0.08 は `luma_floor_override` 実装（未着手）が前提。未実装なら**実効は median≥48／暗フレーム率(YAVG<30)≤0.22**の緩い床で走る。
- **verify_caption_sync の skip穴:** `skipped==True → {ok:True,hard:False}` の偽緑穴は現に開いており、封鎖ラップ（§5.0-B・skip=hard-fail）は**要実装/未着手**。マスター誤配置/whisper不在で1キューも測らず緑になりうる。
- **check_longform_drift.py:** 現状**存在せず**（acceptanceから0回参照）＝後半ドリフト保証・exact≥84は未起動。
- **機能語行末0の受領側再検査（pass3 BLOCKING#2）:** 現状producer自己検査のみ＝shipped SRTの独立hard検査は未起動。
- **test_gate_fixtures.py（赤フィクスチャ）:** 現状**存在せず**＝stub緑封鎖（§6.0・#42）は未実証。
- **結論:** これら要実装ゲートを実装＋赤緑両実証してから受領するのが原則。未実装のまま受領する場合は、設計本文の「17/38/18・ドリフト・skip封鎖・機能語行末」を『**実効は 9/48・skip偽緑・ドリフト未起動**』と正直降格して読み、§13.2実効ゲート62に**上乗せしない**（実装完了で初めて実効点が上がる）。オーナー最優先『緑≠完成／床を騙さない』はこの正直降格＋§6.2人間backstopで担保する。

---

## §14. 既知の実行前提（設計外・実行時に確定/確認する事項）
1. **ドラフト音声実測wpm:** ~155中央逆算・約3,050語。ロック前に実測再算出し`check_runtime_band`(1,170–1,230s)を唯一合否。固定語数は150–165全域で帯を保証しない→帯外は再ペーシング（尺合わせ挿入尺でない）。**verify_script_structure間隔(WEAK)は実タイムラインで再検査(#42)＋step3★オーナー確認。**
2. **担当分担の正直化（pass1 MINOR是正）＝pd-division-of-labor:** **Codexは画像生成のみ。ゲートスクリプト/Remotionコンポーネント/校正はClaudeが実装する**（round4の「Codexが単体で実装できる粒度」はpd-division-of-labor（Codex=画像のみ）と矛盾するため訂正）。かつ**再利用プラットフォーム作業（新ゲート/新コンポーネントの汎用化/他話流用）は本話とは別ワークストリームで追跡**する。ただし**★pass2 MINOR#30是正:5新規Remotionコンポーネントのうち EP33 のヒーロー面/FigureBeat床の充足に必須のもの（`GovtArgumentCard`崩壊=Act4ヒーロー／`HallEquityLadder`=Act3／`EquityTheftTally` heroマップ=Act3）は、`preflight_render_gate`のヒーロー≥3＋各幕ヒーロー時間分布床（Act3/Act4にヒーロー配置）を満たすため本エピソードのレンダ臨界パス上にあり、存在しなければEP33がpreflightで落ちる＝実質EP33ブロッキング**。よって**EP33ブロッキング＝真に新規な要実装(caption skip/longform_drift/showpiece/v002封鎖＋arc-shared allowlist採用時)＋配線済SOLIDの本話閾値校正/override実装＋上記ヒーロー必須3コンポーネント**とし、`OralArgQuestionTally`/`SplitLadder`の汎用化・他話流用のみを別ワークストリーム扱いにする。
3. **要実装/要拡張ゲートの配線＋赤フィクスチャ（🗑ドロップ済は除外）:**
   - **真に新規（要実装・本話ブロッキング）:** caption skip=hard-fail＋reliability床／`check_longform_drift`(基準非依存・-0.60撤回)／showpiece必須マッチ／v002封鎖＋index sha／per-chunk±30ms＋MP3 priming／**★機能語行末0の受領側再検査（`check_caption_format`拡張 or `check_caption_dangle`新設・最終shipped SRTを独立hard再検査・pass3 BLOCKING#2＝方針B条件でなく無条件の本話ブロッキング）**／`manifest.json`のmotion/luma per-episode override機構（本話だけ床を引上げるため・pass2 MAJOR是正で"要拡張"から昇格）＋`measure_motion_energy`へのstill限定p10・median新統計追加（pass3 MINOR#24）／`test_gate_fixtures.py`（全要実装ゲートの赤フィクスチャ）／**（方針B採用時のみ）`check_arc_nonrepeat.evaluate()`のarc-shared allowlist引数**。
   - **配線済SOLID(要拡張/校正・新規実装でない):** `verify_onscreen_text`(＋一次ロケータ前提検査)／`check_image_cut_luma`(全539/四隅/breath)／`check_arc_nonrepeat`(既定=basename交差=0の完全分離・拡張不要／共有allowlistを採る場合のみ下記要実装へ)／`check_footage_utilization`(選定広さ/供給床32)／`verify_script_lint`(カデンツ)／`check_thumb_subject_luma`／`check_padding`(閾値校正)／`verify_caption_coverage`／`check_sound_layers`／`--exclude-subtype`／graphic_symbol機械集計。
   - **配線済だが閾値override機構が要実装（本話だけ厳格化には新規作業・pass2 MAJOR是正）:** `motion_energy`／`check_body_luma` の本話閾値引上げ（still-p10≥17・YAVG38/FRAC0.08等）は現状モジュール定数ゆえ、`manifest.json`のper-episode override フィールド＋ゲート読取り拡張を実装しない限り「本話だけ校正」は不可（さもなくば全話同時に基準が動く）。motion-variety拡張も同様。
   - **WEAK(完全自動保証にしない・人間backstop併用):** `verify_sfx_manifest`／`verify_script_structure`／`check_ending_sound`。
   - **🗑実在するが未配線＝ドロップ扱い(引用禁止・本アークで配線しない):** `check_stem_loudness`／`check_music_coverage`（`evaluate(epdir,render)`実装済で1行配線可能）／`check_motion_bbox_flow`（＝bbox-localフローゲート）。**3本とも`scripts/`に実在するが`check_final_acceptance`に0回参照＝現状走らない（"存在しない"は誤り・pass2 MAJOR是正）。** 台帳ドロップ方針で自動保証に引用せず、音は`check_sound_layers`＋音5本試聴、モーションは`motion_energy`＋motion-reelで担保。将来配線する場合は実挙動・閾値を実走で確認し赤フィクスチャ＋緑実証を要する（別ワークストリーム）。
   - **各要実装/要拡張ゲートは`test_gate_fixtures.py`で赤フィクスチャexit1を実証してから出荷。**
4. **grade B/要確認事実のrecheck(§1.4):** 購入年1999・売却年・cert日・PLF統計・州法改正・**Hall身元/性別/所在/結果(第6巡回・CLM-0021をgrade A化)**・**CLM-0014B制定法年代**・「36」州が意見本文に在るか・**焼込逐語(CLM-0012/0013/0014A)の一次ロケータ**・Tyler本人回収可否。未確認は画面に断定しない。
5. **PLF統計の帰属:** 全米$780M/~8,500戸・MN$118M/~1,200戸は擁護団体推計。`Est.`必須・VO注記1回。
6. **州数フレーミング:** 主表示は「a large majority / 36(本文確認後) states + federal required return」、StateMap保持側=PLF実列挙12州(`Est.`・"a dozen"=12)、算術一致を演出しない。
7. **環境前提:** 本Windows PC・CPU libx264・NVENC不使用。fps30/1920×1080。長尺WebGL/depth`--concurrency=4`。画像はCodexのみ。
8. **3話アーク素材分離（実ゲート挙動に接地・pass2 BLOCKING是正）:** 既定=完全分離方針A。実配線`check_arc_nonrepeat`は他話`*_film.json` cut src basename＋public メディアを直接読んで交差=0をhard判定する（`catalog_fingerprints.json`は読まない＝計画台帳advisory）。法廷/庁舎素材も含めEP33/34/35で別クリップにし、棚の3話分distinct確保を§12 step7で先に検証。identical共有が必要なら`check_arc_nonrepeat.evaluate()`にallowlist引数を新規実装（§14-3要実装・方針B）してから配線。
9. **中立性/権利:** 政府機関は中立・事実記述。生成ビジュアルは再現/説明。実在私人主役ゆえAI実在肖像禁止・肖像近似回避。
10. **ショート/予約:** 切出し1本(YT/TikTok 2版)・1日1本12:00 JST・空き日監査後。本編公開はオーナーGO後。

---

*正典ファイル:* `episodes/PD-2026-033-tyler/` 配下（`03_script/script_final.v001.md`・`03_script/reviews/{review_facts,review_binge,review_pacing}.md`(独立provenance＋実質列挙)・`04_scenes/scene_plan.v001.json`・`remotion_plan.v001.json`・`asset_selection.v001.json`(footage候補にsrcパス写像/選定広さ)・`05_visuals/{catalog_fingerprints(asset_id),graphic_symbol_ledger,lowkey_whitelist,pool.jsonl}.json`・`06_audio/narration_index.v001.json`・`audio/stems/`・`audio/provenance.json`・`audio/sfx_manifest.json`）／マスター音声`media_root/episodes/PD-2026-033-tyler/06_voice/master/vc_master_v001.mp3`＋測定用`.wav`／専用図`remotion/src/components/tyler/`（新規: OralArgQuestionTally/SplitLadder/GovtArgumentCard/HallEquityLadder/EquityTheftTally hero版）／再利用`motionkit/`／要実装/要拡張ゲート`scripts/`（§14-3）＋`scripts/test_gate_fixtures.py`（赤フィクスチャ）。**担当分担（pd-division-of-labor）＝Codexは画像生成のみ、ゲート/コンポーネント/校正はClaude。** 本設計書は全数値床を本話具体値で確定し、**実ゲート台帳と1対1で実装状態（実装済wired/WEAK/要実装/自己申告/🗑ドロップ済）を照合して詐称せず**、ドロップ済ゲートの引用を実在機構＋人間試聴backstopへ差し替え、配線済SOLIDの誤ラベルを訂正し、§11で全過去失敗＋20分水増し＋pass1監査新規失敗（ドロップ/WEAK誤引用・配線済誤ラベル・架空焼込引用）に名前のある機構を紐付けた。**『敵対監査の未解決BLOCKING/MAJOR=0』の自己認証は撤回**し、最終的な完全性は独立再監査が全ゲート名を`check_final_acceptance.py`の配線と再照合した上で確定する（pass1 MINOR是正）。スコアは設計完全性98/実効ゲート62（配線済ゲートを正しく計上）の二本立てで単一100/100を掲げない。**pass2監査31件（BLOCKING3/MAJOR11/MINOR17）を`check_final_acceptance.py`実挙動に接地して反映済み＝sound_layersのdistinct/beds床は自己申告＋sha束縛（波形個数検出でない）／stem_loudness・music_coverage・motion_bbox_flowは実在するが未配線／arc_nonrepeatはbasename交差=0でcatalog非読取（既定=完全分離）／motion・luma床は本話override機構が要実装／ED尺埋め撤回。**