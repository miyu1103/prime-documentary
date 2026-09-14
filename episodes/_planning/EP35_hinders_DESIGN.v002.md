# EP35（hinders）制作設計書 v002 — 3回点検 検証サインオフ層

- **binding正典（不変・invariant6）**: `EP35_hinders_DESIGN.v001.md`（本文はこちらが正典。v002はその上の検証・是正層）
- **超激重アニメ素材（別スレ制作）**: `EP35_hinders_ANIMATION_ASSETS.v001.md` / 引き継ぎ `EP35_hinders_ANIMATION_HANDOFF_PROMPT.md`
- **3回点検（corner-to-corner・実コード実測照合）**: pass別 [{'pass': 1, 'findings': 34, 'majors': 16}, {'pass': 2, 'findings': 31, 'majors': 16}, {'pass': 3, 'findings': 22, 'majors': 9}]
- **正直スコア**: 43/100 ／ **真の未解決BLOCKING**: 4件
- **注（スコア43の理由）**: 低スコアは設計不良でなく、点検が『topic承認段階では未作成が正常な下流成果物（claims台帳/film.json/asset_selection/ai_prompts/arc指紋）』を厳密に要求したため。これらは制作段/別スレで作る＝設計の穴ではない（下記残課題の性質分類参照）。

---

## A. サインオフ監査（実ゲート実測照合の結論）

# 最終サインオフ監査 — PD-2026-035-hinders (v007 pass3) 監査官所見

## 判定: 条件付き不合格（着手前ブロッカー未解決）＝ SHIP不可・設計文書としては合格水準

v007 pass3 は前パス22件を実質処理済みで、**新規BLOCKING/MAJORは検出せず**。数値整合・ゲート台帳整合・工程分担・ドロップ/WEAKゲートの扱いはいずれもGATE REALITY台帳と矛盾しない。ただし設計が自認する通り**着手前ブロッカー4件（成果物不在＋一次未確認）が未解決**で、この状態での「完成」宣言は禁止。

## リポジトリ実照合（load-bearing主張の裏取り）

| 設計の主張 | 実測結果 | 判定 |
|---|---|---|
| pass3#20: depth基盤は横長export部品 `DepthStill` | `CaseFilm.tsx:273` に `export const DepthStill: React.FC<{src;seed;dir;dur}>` 実在・props一致 | 正 |
| pass3#20: `DepthImageV` は縦Short専用・流用不能 | `Short.tsx:232` に非export `const DepthImageV`（`ShortBeat['motion']`型結合）実在 | 正 |
| pass3#21: ai_prompts.v001 = 68プロンプト基準 | `EP35_hinders_ai_prompts.v001.md` 行頭 S0NN = 68件 | 正 |
| BLOCKING(B): `arc_used_fingerprints.json` 0件 | ファイル自体が不在（Globヒット0） | 不在確認＝BLOCKING実在 |
| ドロップゲート引用禁止 | `check_stem_loudness`/`check_motion_bbox_flow` は本文非引用、`check_music_coverage` は「DROPPED・引用禁止」注記のみ | 遵守 |

## 内部整合の再検算（監査官が独立に検算）
- 語数: 19+630+660+490+555+700+95 = 3149（≈3150と一致）
- 秒(158wpm): 7+12+241+254+183+209+262+39 = 1207s（band 1,170–1,230 中央・+37/−23）
- depth: 1+1+46+56+44+45+45+2 = 240（Act5=106×0.42≈45 で pass3#10 の45%矛盾は解消）
- カット総数: 4+4+100+116+88+100+106+10 = 528
- distinct: 162/324 = 0.50（床0.40 +0.10マージン）
- TIGTA算術不整合(91%×278≈253≠231): VOを "roughly 280 / about nine in ten / more than 200 cases / around 17M" にヘッジ＋分母整合＋画面焼込保留で解消

## ドロップ/WEAK是正の確認
- **DROPPED** 3ゲートを機構として引用する箇所は無い。音楽被覆は `sound_layers` に帰属させず preflight人間試聴＋cue-stem sha に差し替え済。
- **WEAK** 3ゲート(`verify_sfx_manifest`/`verify_script_structure`/`check_ending_sound`)は「完全自動保証」として引用せず preflight backstop併記。
- **SOLID誤格上げ無し**: `verify_onscreen_text` は film/claims両不在で soft-skip・omission非検出＝台帳生成後発火の照合と格下げ済(pass3#22)。`arc_nonrepeat` は生成静止画で vacuous PASS＝保護根拠に数えないと明記。`motion_energy` ROI版(≥16/p10≥11)は「要配線」と正しくラベル。

## 監査官が加える最小是正（テキスト修正は不要・運用条件のみ）
新規のBLOCKING/MAJORは無いため本文改稿は課さない。ただし SHIP 条件として以下を[OG-0]〜[OG-1]の物理前提に固定する（設計§12/§14と同義・再掲）:
1. CLM台帳(0001–0020＋分割0013a/b/c＋新設0018/0019)を `01_research/` に実生成するまで §13軸1は仮点。
2. `arc_used_fingerprints.json`(sha+pHash+content-tag) を EP33/34 実レンダから実ファイル化するまで [OG-0.5] で本話停止。
3. ai_prompts v002 を単独unique≥162＋レーンBASE分離＋electric-blue撤去＋汎用象徴禁止＋SOLD描写禁止で実発注するまで distinct 0.50 は仮定。
4. Carole 店舗処分(CLM-0019=UNVERIFIED) の一次確認までVO/画面で売却を断定しない。
5. `check_script_lint`/`check_padding`/`check_script_wordfloor` の**実出力**（reversal-couplet数・メタ語0・三段否定=1・アナフォラ解体・quiet=0・実wc）を貼付するまで台本合格を主張しない。

## 総括
設計文書としては、全過去失敗を名前のある機構へ紐付け、ドロップ/WEAKゲートを正直に扱い、Codex実装粒度をpd-division-of-labor逐語（画像のみ）へ是正し、水増しを実装済SOLID `check_padding` を主柱に据えた点で高水準。**減点要因は、(1)保護機構の多数が「要実装」（33本のDSP/字幕/図ゲートがOG-0未配線・未通過）で現時点では実在機構でない、(2)着手前BLOCKING4件が未解決、(3)実在私人の店舗処分が一次未確認**。よって裏付けスコアは設計自認の≈40/100圏。フラット100は撤回済で、この正直さ自体は適切。


---

## B. 過去失敗 × 塞ぐ実在機構 点検表

# 点検表 — 過去失敗 × 塞ぐ実在機構 × 設計§ × 状態

凡例: **SOLID**=実装済・配線済・実データ検証済 ／ **要実装+backstop**=専用ゲート未実装、現時点の実在担保は preflight人間試聴/目視のみ ／ **WEAK+backstop**=弱ゲート＋preflight人間 ／ **process**=工程規約（ゲートでない）

| # | 過去失敗 | 塞ぐ実在機構（ファイル名） | 設計§ | 状態 |
|---|---|---|---|---|
| 1 | 字幕がナレと不一致 | `caption_narration_match.py`（語列100%一致・順序一致） | §5.0/§5.4/§11-1 | SOLID |
| 2 | 字幕が遅い | `caption_sync`（exact帯・p50/p90/機能語行末0） | §5.1/§11-1 | SOLID（v2閾値引上げは要実装+backstop） |
| 3 | 字幕が変な所で切れる（機能語行末） | `caption_sync`機能語行末=0（SOLID）＋`check_caption_lines.py`（≤8語/≤44字/≤2行/cps≤27） | §5.1/§5.2/§11-2 | 一部SOLID＋要実装+backstop |
| 4 | 8:45以降ドリフト | `caption_sync`exact帯（SOLID配線）＋§5.3 20ビン5条件＋windowed narration | §5.3/§11-3 | SOLID(exact帯)＋要実装+backstop(ドリフト専用) |
| 5 | 字幕が飛ぶ（未字幕chunk） | `caption_coverage`（全ナレchunk≥1cue描画） | §5.4/§11-1b | SOLID |
| 6 | DL/生成素材が1つも使われない | `footage_utilization`（162生成unique各々が最終mp4≥1回）＋`check_rendered_footage_min`（≥34） | §3.5D/§10.1/§11-4 | SOLID＋要実装。実写0本リスクは[OG-3]でオーナー明示 |
| 7 | 素材の話またぎ&話内被り | pHash(≤6)＋content-tag照合＋EP33/34指紋台帳。`arc_nonrepeat`はvacuous PASS＝根拠に数えない | §3.5C/§11-25 | 要実装+backstop（**指紋台帳0件＝BLOCKING[OG-0.5]で停止**） |
| 8 | 天秤等の汎用象徴の乱用 | `build_footage_contact_sheet` content-tag辞書のhard FAIL列（天秤/女神/hourglass=0・gavel≤1）＋preflight実本数確認 | §3.5C/§10.2/§11-15 | 要実装+backstop（pass3#7） |
| 9 | factory棚ラベル破損で場違い素材 | 内容ベース選別＋`build_footage_contact_sheet`（レーン基調色列＋汎用象徴FAIL列）＋preflight目視 | §10.2/§11-16 | preflight backstop＋要実装列 |
| 10 | フック8s→OP→本編4幕→ED構成でない | `structure_4part`＋`op_ed_bookends` | §9.1/§11-5 | SOLID |
| 11 | OP/EDがいつものテイストでない | `op_ed_bookends`（SOLID）＋§9.1 PD bookends＋§4.8 ED固定＋preflight試聴 | §9.1/§4.8/§11-6 | SOLID＋preflight backstop |
| 12 | アニメが無く紙芝居 | `motion_energy`（within-shot≥12/p10≥9・SOLID＝凍結検出のみ）＋ROI版≥16/p10≥11＋`check_freeze_frames`/`check_figure_cadence` | §3.0/§3.6/§11-7 | SOLID(凍結)＋要実装+backstop(豊かな動き) |
| 13 | 図が少ない/疎（2点地図） | `check_figure_cadence`（幕別新規≥3・hero≥1・間隔≤90s・描画後要素≥6）＋preflight | §3.6/§11-10 | 要実装+backstop |
| 14 | 周回する淡い光がうざい | `check_glow_periodicity`（L0/L1/L2低周波自己相関ピーク=FAIL）＋preflight人間 | §3.1/§11-8 | 要実装+backstop |
| 15 | 図/lowerthird左見切れ | `check_titlesafe`（全lowerthird/図onsetでROI bbox x≥120/上下54px内）＋preflight onset基準抽出 | §3.4/§5.5/§11-9 | 要実装+backstop（pass3#8新設） |
| 16 | 図背景が暗い | `image_cut_luma`（SOLID・カット毎輝度床）＋body_luma派生（図面52/50） | §3.3/§11-11 | SOLID＋要配線 |
| 17 | 画面が暗くて画像が見えない | `body_luma`（median≥48・SOLID）＋`image_cut_luma`（SOLID）＋`check_subject_luma`（ROI）＋luma range pin | §3.3/§11-11 | SOLID＋要実装(subject-ROI) |
| 18 | 効果音が無意味なフィラー | 全SFX意味タグ1:1＋`check_rendered_sfx_min`（画面ID署名・空欄=FAIL）。`verify_sfx_manifest`はWEAK | §4.5/§11-12 | 要実装＋WEAK+backstop |
| 19 | SFX種類少ない/違和感 | `sound_layers`（distinct SFX≥12・SOLID）＋`check_sfx_density`（各Act≥6・≥1本/25s） | §4.5/§11-13 | SOLID(≥12)＋要実装(per-Act密度) |
| 20 | 終盤の飛行機みたいな変な音 | `check_roar_anomaly`（低域上昇≥3dB&<300Hz比≥0.6/flatness/crescendo/逆再生）＋`check_ending_sound`(WEAK)＋preflight音5本 | §4.8/§11-14 | 要実装＋WEAK+backstop |
| 21 | サムネが地味でCTR低い | `thumbnail_visibility`（平均Y≥33・SOLID）＋`thumb_subject_luma`（SOLID）＋`thumbnail_saturation`/`thumbnail_text_contrast` | §9.2/§11-17 | SOLID＋要実装(彩度/コントラスト) |
| 22 | AI臭い（定型句/固有名詞詰め/出典なし断定） | `script_lint`（SOLID・実走必須＝Here is1/命令2/quiet0/engine1/三段否定1/アナフォラ解体/reversal-couplet≤4/メタ語0）＋独立3レビュー | §2.0/§2.5/§11-18 | SOLID（但し**実走・実出力未貼付＝(E)未解決**） |
| 23 | SDXLを勝手に起動 | 画像はCodexのみ（ai_prompts＋サムネ背景）・図は全てClaude工程 | §10/§11-19 | process |
| 24 | 緑なのに完成でない（自己申告） | `preflight_owner_review.py`（16枚コンタクト＋音5本＋caption_sync＋luma＋SUMMARY）＋[OG-4]owner承認 | §6.2/§11-20 | SOLID(preflight)＋human gate |
| 25 | 偽の緑（古い良品） | `freshness`（sha≠前回＋mtime新・SOLID）＋`audio_mix_sha256`（mux直前刻印一致） | §4.10/§11-21 | SOLID |
| 26 | 薄い音で緑 | `sound_layers`（beds≥4/distinct≥12・SOLID）＋loudness 2-pass＋VO谷≥-18＋`check_sfx_density` | §4/§11-22 | SOLID＋要実装(密度) |
| 27 | 尺外れ | `check_runtime_band.py`（1,170–1,230s・実TTS・SOLID＝唯一のship-gate）＋`check_script_wordfloor` | §8.2/§11-23 | SOLID＋要実装(wordfloor) |
| 28 | 20分を間・水増しで稼ぐ | `check_padding`（水増し/沈黙尾/言い換え反復・SOLID＝主柱）＋`check_info_beat`/`check_script_binge`補助 | §0/§8.2/§11-26 | SOLID(主柱)＋要実装(補助) |
| 29 | ゲート最適化（グッドハート） | OG-0独立held-outフィクスチャ（第三者確認）＋要実装を実装済と偽らない表記＋`preflight_owner_review` | §12/§13/§11-24 | process＋human backstop |
| 30 | 実在私人の不正確記述（売却断定） | CLM-0019=UNVERIFIED束縛＋preflight「売却断定ゼロ確認」＋TIGTA/入金数VOヘッジ | §1.1/§2.5/§6.2/§11-33 | 要実装+backstop（**一次未確認＝(D)未解決**） |
| 31 | 立法史の誤記（§5324第二の罪） | CLM-0015束縛（1986単一罪へ一本化）＋CLM-0018（30日hearing）＋recheck18/19 | §1.1/§2.5/§11-34 | 要実装+backstop（**CLM台帳未生成＝(A)未解決**） |

**ドロップゲート引用**: `check_stem_loudness`/`check_motion_bbox_flow`/`check_music_coverage` を機構として引用する箇所は残存せず（音楽被覆は `sound_layers` 非帰属＋preflight＋cue-stem sha へ是正済）。


---

## C. 残課題（性質別分類・**どれも設計本文の穴ではない**）

### 下流成果物（制作段/別スレで作る・設計の穴でない）
- (A) FACTS原本CLM台帳（0001–0020＋分割0013a/b/c＋新設0018/0019）が未生成。§13軸1は台帳実生成まで満点不可＝仮点。実在私人の断定がCLMへ桁一致で束縛されるまで事実精度は検証不能。
- (B) BLOCKING: EP33/34 `arc_used_fingerprints.json`(sha+pHash+content-tag) がリポジトリに不在（Globヒット0で実確認）。話またぎ被り防御は pHash+content-tag+指紋台帳のみが実防御で、台帳0件＝arc拡張は検証不能。[OG-0.5]で実ファイル化まで本話停止。
- (C/E/F) ai_prompts v002 未発注（単独unique≥162・レーンBASE分離・汎用象徴禁止・SOLD描写禁止）でdistinct 0.50は仮定。script_lint/padding/wordfloor の実出力（reversal-couplet数・メタ語・三段否定=1・実wc）未貼付で台本合格は暫定。DepthStill ease改修（linear→Easing.out(cubic)）はClaude NEW-BUILDとして未実施でdepth 240カットのeasing要求が未充足。
- verify_onscreen_text はSOLID配線だが film json と claims.v*.json 両不在で soft-skip・数値未配置(omission)非検出。画面内grade-A数値の正確性は台帳/film生成後に発火する照合＋§1手動桁一致＋preflight目視に依存し、生成前は inert。

### 人間backstopのみ（自動ゲート原理的に不能）
- (D) Carole 店舗処分(CLM-0019=UNVERIFIED) が一次未確認。売却断定は全編削除済だが、情動ペイオフの一次確認が未了のためVO/画面での売却断定禁止を運用backstopに依存。
- 保護機構の多数（33本のDSP/字幕/図ゲート＝caption_sync v2・caption_lines・figure_cadence・glow_periodicity・check_titlesafe・roar_anomaly・sfx_density等）が『要実装』で、OG-0独立フィクスチャ未配線・未通過。現時点では実在機構でなく preflight人間backstopのみが担保。紙芝居・字幕ドリフト・周回グロー・図見切れ・変な終盤音の防御は自動保証未達。
