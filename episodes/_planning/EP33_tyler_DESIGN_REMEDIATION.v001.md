## 是正台帳（round4・監査62件×対応・該当セクション）

BLOCKING=B / MAJOR=M / MINOR=m。全62件を反映。

### 字幕（captions）
| # | 重大度 | 指摘 | 対応 | §|
|---|---|---|---|---|
| 1 | B | ドリフト検査の基準定数(-0.60 realized median)が誤りで健全話を毎分false-FAIL／「1.1s帯素通り」は虚偽 | -0.60→+0.25絶対アンカー全撤回。realized median≈-0.02(EP31)へ訂正、未カバー帯は実0.12s。check_longform_driftを基準非依存(per-window相対≤0.10/半差≤0.05/スロープ≤0.010/Act5≤0.08)に。MIN_EXACT_PCT=84(据置・下げず) | §5.0 |
| 2 | M | lag統計がmatched cueのみ→showpiece引用cue脱落で遅延region隠蔽 | showpiece-cue(T5/T7/T11/T15/T16/T18/T19/T21/T3')必須マッチ、per-window/Act最小matched_fraction、未マッチcueをreceipt出力 | §5.0/5.6 |
| 3 | M | ≤8語/≤44字がproducer(10語/50字)・check_caption_format(50字)と矛盾＋orphan退行 | ≤10語/≤50字/≤2行/≤27cpsへ整合(≤8撤回) | §5.3 |
| 4 | M | v001強制がprose、producerはv002自動選好 | v002存在exit1＋producer/verifier同一index sha assert | §5.1 |
| 5 | m | 終端のみ検査＋MP3 priming | per-chunk±30ms＋測定用WAV併置し長さ±30ms一致 | §5.1 |

### 素材（footage）
| # | 重大度 | 指摘 | 対応 | §|
|---|---|---|---|---|
| 6 | B | arc_nonrepeatが合成後aHash→グレードで指紋散り検出不能 | 指紋を元asset_id交差=0に変更、補助pHash≤6は合成前ソース | §3.6 |
| 7 | M | legal_courtは汎用象徴subtypeが大半で供給不能 | 主レーンをproperty_home＋documents_paper＋非汎用郡庁舎に、legal_courtは非汎用subtype名指し補助に降格、subtype別生存見積 | §3.6 |
| 8 | M | urban_nightフォールバックがEP34空港レーン先食い | urban_night除外、家/自治体レーン閉フォールバックに、レーン排他事前検証 | §3.6 |
| 9 | M | Codex静止画補填ではfactory_used(実映像数)が増えず偽是正 | 26床は実映像クリップのみ、Codex静止画は分母外・別調達 | §3.6 |
| 10 | M | graphic_symbol_ledgerが自己申告JSON＋反復回数を縛らない | film.json src機械集計へ、種類≤2かつ各象徴登場≤3回の二本立て | §3.6 |
| 11 | m | footage_diversity帰属誤(全cut src対象)＋命名禁止トークン不足 | 「全cut src」に訂正、禁止トークンをFOOTAGE_GENERIC_PAT全体に一致 | §3.6 |
| 12 | m | utilizationのID↔path写像未定義 | 候補にsrcパス写像必須フィールド＋正規化キー突合 | §3.6 |

### アニメーション（animation）
| # | 重大度 | 指摘 | 対応 | §|
|---|---|---|---|---|
| 13 | B | motion_energy床が「校正後確定」へ先送りで本話具体値不在 | 先送り撤回。still-p10≥16/全体median≥18/12秒窓≥8を即確定・即配線、校正は引上げのみ、未実行で出荷不可 | §3.0/3.8 |
| 14 | M | bbox-localフローに数値閾値/exit1なし | bbox中央値≥8px/frameをspan≥60%、未達exit1、§6.1独立行 | §3.2/3.8 |
| 15 | M | ヒーロー面がAct1/2/5偏在、中盤7.5分ゼロ | EquityTheftTally(Act3)/GovtArgumentCard崩壊(Act4)をhero昇格、ヒーロー時間分布床(≥1/≤6分・幕ゼロ禁止) | §3.0/3.2 |
| 16 | M | 120秒窓≥1図が緩い＋計画フラグ判定の循環 | ≥1図/≤60秒・refrain still≤25秒へ引締め、POST-render実測で二重化 | §3.2 |
| 17 | M | カード/ラダー図に持続キャリア未指定 | 各カードに恒常キャリア(パララックス/呼吸プレイヘッド/加算カウンタ)指定、reveal後ホールドはアクティブカウント除外 | §3.2 |
| 18 | m | depth40.1%が床ちょうどで余裕0 | 44.2%(238/539)へ増予算＋graphics自動付与フォールバック | §3.0/3.5 |
| 19 | m | entropy/CVが接地なし確定＋px床6-10/8-12不一致 | entropy/CVもMotionSample vs紙芝居で接地、持続px床を≥8pxに統一 | §3.8 |

### 明るさ（brightness）
| # | 重大度 | 指摘 | 対応 | §|
|---|---|---|---|---|
| 20 | M | image_cut_lumaがgraphics228/footage79を除外 | スコープを全539カット(footage65/graphics222含む)に、footage別床≥50/≥46 | §3.7 |
| 21 | M | VignetteBreath動的暗化を空間単一フレーム床が取りこぼす＋算術矛盾 | 静的≤0.09＋breath≤±0.03で合算≤0.12、暗ベッド幕はbreath=0、最暗位相フレーム測定固定 | §3.1/3.7 |
| 22 | M | bed_factor数値未確定＋grain/glow重畳が式に無し | bed_factor=1.0(screen/additive固定・multiply禁止)、grain_factor=0.98(screen/soft-light≤0.10)、式に組込 | §3.1 |
| 23 | M | check_body_luma(YAVG<30が22%=264s許容)がEP31 FAIL水準 | <38/≤8%へ再校正、body単独で出荷不可(image_cut_luma必須) | §3.7 |
| 24 | m | 冷色Act暗端47が床下回り四隅余裕2.1 | 冷色暗端hex引上げ(合成後≥52/四隅≥46余裕≥4) | §3.1 |
| 25 | m | スクリム禁止が名前になっていない | §5.5に暗化スクリム禁止明記＋字幕帯(y900-1010)輝度低下検査 | §5.5/3.7 |

### 音（sound）
| # | 重大度 | 指摘 | 対応 | §|
|---|---|---|---|---|
| 26 | M | 遷移SFXがwhip1種で40+境界単調＋SFX再利用上限なし | 遷移4系統×2ピッチ=8ファイル・ローテ、単一使用≤15%・連続同一≤2、遷移distinct≥4 | §4.4 |
| 27 | M | 音楽が実質ノーゲート(cue_count自己申告) | check_music_coverage(active≥85%/無音≤8s・stem実測sha束縛) | §4.2 |
| 28 | M | 「Kurzgesagt級」ラベルが中身伴わず密度床薄い | 密度≥6/分・主要beat≥80%、base_id≥14、参照ch級主張を満点根拠から撤回 | §4.4 |
| 29 | m | ambience distinct閾値未確定＋自己申告 | 相互相関<0.6＋源SHA相異、mux/stem実測 | §4.3 |
| 30 | m | ending検出器自己免除リスク＋代替ベッド無し | 独立校正(MB-END除外)＋MB-END-ALT常備 | §4.5 |
| 31 | m | ambience床が低域ブラインド＋stem gateがJSON読取 | 2帯(40-160Hz/1-8kHz)測定＋ebur128実走再導出 | §4.1 |

### グッドハート（gaming）
| # | 重大度 | 指摘 | 対応 | §|
|---|---|---|---|---|
| 32 | B | ~20要実装ゲートに負フィクスチャ要件なし→stub緑 | 全要実装ゲートに赤フィクスチャ(バッドでexit1)必須、test_gate_fixtures.py、緑まで出荷ブロック | §6.0/§7 |
| 33 | B | motion_energy床を自作stills値マイナス少々でフィット | 良基準の絶対分数(still-p10≥0.35×46.6=16)に接地、届かねばDepthStillHiで上げる | §3.8 |
| 34 | B | ending検出器較正にMB-END含む=自己免除 | MB-END除外の独立ラベルで凍結後にMB-END試験、トリップなら音楽再素材化 | §4.5 |
| 35 | B | padding=実装ゼロ(runtime_bandはデッドエア通す) | check_padding(60秒窓content-novelty＋分散床)を出荷前hard化、axis3を緑まで6にキャップ | §6.4/§8/§13 |
| 36 | M | utilizationの分母を過少選定で操作可 | 選定広さ≥39候補≥3テーマ＋実配置distinct≥32を利用率と別床 | §3.6 |
| 37 | M | arc aHashがregradeで defeated | asset_id指紋へ(=#6) | §3.6 |
| 38 | M | catalog空/部分でvacuous green | <200指紋/<10話でexit1＋カバーID記録 | §3.6 |
| 39 | M | 3レビュー独立性がmodel_id文字列違いのみ | 実質列挙(CLM line-item/人物ループclose/60秒窓判定)をアンカー参照で機械検査 | §2.7 |
| 40 | M | 単一100/100が自己申告完了パターン | 設計完全性(96)と実効ゲート(40)の二本立て、単一100撤回 | §13 |
| 41 | m | exact78/still床が前作・自作値マイナスの床フィット | exact≥84据置(下げ禁止)、still床は絶対アンカー | §5.0/3.8 |
| 42 | m | 構造間隔検査が紙157wpm tc | voiceレンダ後にaligned narration_index実時刻で再実行、床違反で出荷ブロック | §2.7 |
| 43 | m | -28dBまだ薄い＋flat20s vs motion12sの隙間 | -25へ＋stem gate非任意、flat窓12sへ短縮＋位相オフセット | §4.1/4.5 |

### サムネ（thumbnail）
| # | 重大度 | 指摘 | 対応 | §|
|---|---|---|---|---|
| 44 | B | 本命案Aが自床(独立金額≤1)違反で3金額 | 案Aを単一$25,000へ確定、複数金額同時表示禁止、A/B軸=$25,000 vs 合法性の1軸 | §9.2 |
| 45 | M | 案Aメインが自称≤14字を16/18字で超過・物理的に不可能 | 各行≤16字の真の短句(THEY KEPT/$25,000/YOU DIDN'T OWE)、モック320px実測後Done | §9.2 |
| 46 | M | 3案とも結果断言でcuriosity-gap欠如(合法性の逆説なし) | 案B=合法性gap(100% LEGAL)を疑問提示に、案Cをauthority当て馬昇格、最低1案は疑問 | §9.2 |
| 47 | m | 窓辺94歳女性シルエットがGeraldine本人肖像近似リスク | 非特定シルエット/象徴的家/本人非断定＋物のみ案D常備 | §9.2 |
| 48 | m | Doneがcheck_thumb_subject_luma(要実装)依存 | 実装をサムネ確定の前提にブロッキング配置、未実装は高輝度図案 | §9.2 |

### AI臭（aismell）
| # | 重大度 | 指摘 | 対応 | §|
|---|---|---|---|---|
| 49 | B | Act3 Hall物語が史実と逆(Hallは第6巡回で勝訴) | Act3全面書換(Hall勝訴・$1移転/$308k転売)、CLM-0021新設、grade A化まで出荷不可、review_facts line-item | §1/§2.6 |
| 50 | M | script_lintがカデンツ/劇的アイロニー言い換えを検出不能 | 短文3連/アイロニー言い換え群/二重legalタグ検出へ拡張、ED三段・Act1アイロニー・Hook/ED二重legalを実書換 | §2.5/2.6/2.7 |
| 51 | M | CLM-0014がMagna Carta1215とOverplus(後代制定法)を誤バンドル | CLM-0014A(residue/1215)とCLM-0014B(Overplus/後代)に分割、別チップ/別年代ラベル/別ビジュアル、Act5冒頭時系列分離 | §1/§2.6/§5.4 |
| 52 | M | Hook22トークンが≤20語床超過・rushed | 実語14≤18に短縮、ElevenLabs実尺≤8s確認 | §2.3 |
| 53 | m | "Two states away"(未確認地理)＋"a promise about debt"(矮小化) | 匿名帰属へ、Magna Carta ch.26残余原則を具体化 | §2.6 |

### 離脱防止（retention）
| # | 重大度 | 指摘 | 対応 | §|
|---|---|---|---|---|
| 54 | B | 二人称0:24→6:40=6:16が自床5:30超過(Act1最遅ゾーン覆う) | 2:40に二人称脅威①新設、全隣接差最大5:20へ、間隔表に0:24→2:40→6:10行明記 | §2.2 |
| 55 | M | OL1(個人回収)をEDが答えられずbait-and-switch | OL1を系統的問い(止められるか)に開き替え、個人回収非約束 | §2.2 |
| 56 | M | Act1 3:46実ペイオフ無し(Hook既にオチ開示) | 1:50に$2,300→$15,000 slam早期ペイオフ、Act1を196s(3:16)へ圧縮 | §2.2/3.2 |
| 57 | M | 9:45→12:30=2:45が床際＋説明谷 | 11:15にSplitLadder再フック、OL3 11:00正式収録で谷充填 | §2.2 |
| 58 | M | verify_script_structure未実装で床実効ゼロ＋設計自体が5:30破る | 出荷ブロッキング化＋机上で床通過証明後ロック(#54で床是正済) | §2.7 |
| 59 | m | OL3開11:00が再フックマップに不在(二表不整合) | 11:00エントリ追加、二表を単一ソース化 | §2.2 |
| 60 | m | Hook実発話≈9.5sで8s超過(=52) | Hook短縮(=52対応) | §2.3 |
| 61 | m | climax後2:05の下り坂崖 | coda≤45s・9-0 slam18:15で勝利〜終幕≤1:45、EP34ティーズ連結 | §2.2/9.1 |
| 62 | m | OL5ペイオフが抽象(州名なし)で二人称回収弱い | OL5を過去/普遍形に開き替え、改正州の動きを追加 | §2.2/5.4 |

**累積:** round1/2/3の是正(598訂正・PLF代理人・Hall女性化・50-36捏造撤回・skip穴・自己申告降格・サブピクセル呼吸撤回等)を維持しつつ、round3で新たに突かれた「詐称・算術破綻・循環逆算・床未定義・stub緑・Hall事実誤り・サムネ自床違反」を全是正。BLOCKING/MAJOR 42件＝0残、MINOR 20件も全解消。