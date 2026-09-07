## 是正台帳（累積・round 4＝敵対監査54件）

### captions（字幕）
| 指摘 | 対応 | 該当§ |
|---|---|---|
| captions-1(MAJOR) onset検出の入力信号未指定 | onset計測をVO単独ステム`vo_stem.wav`(de-esser/comp後・SFX/アンビ/劇伴含まない)に固定するhard規定。ミックス測定はFAID・レジストリ照合対象。VO収録でステム保持を§12 step5に追加 | §5.2/§6.0/§12/§14 |
| captions-2(MAJOR) WhisperX confidence閾値未定義 | score<0.5をflag・1文中flag語≥1 or 全体flag率>1.0%でFAIL。ASR語誤り率>1.5%とのOR合否論理を明記 | §5.1/§6.1 |
| captions-3(MINOR) lead0.12sでexact帯が構造的に≥75% | 独立残差指標(script align時刻 vs 独立ASR/energy時刻)のp50/p90を追加・代表語(先頭+末尾)評価。残差p90≤0.15s | §5.2/§5.7 |
| captions-4(MINOR) ≤32cpsフォールバック選択規則未定義 | ≤32cps許容は総計≤6s/連続1キューまで・超過は台本trim→再収録に決定論確定。preflight一覧提示 | §5.3 |
| captions-5(MINOR) 章境界6点は7点 | HOOK→OP含む全頭transition7点に訂正・§3.4頭trans表と突合 | §5.4(d) |

### footage（素材）
| 指摘 | 対応 | 該当§ |
|---|---|---|
| footage-5(BLOCKING) distinct床24がreuse≤4と矛盾(188cut要47種) | distinct床を≥47種へ・調達84本の実採用率≥85%(≥71種)をhard追加・「素材数×4≥必要cut」「実採用≥調達×0.85」「screen-time≥35%」の3条件をレジストリで相互突合 | §3.0/§3.5-B/§6.1 |
| footage-6(MAJOR) スチル代替の抜け道(床下方再計算) | 35%(≥420s)を絶対不変量に固定・下方再計算禁止・スチル代替≤2タグ/screen-time控除≤5%・超過はshipブロック・理由記録＋owner確認 | §3.5-A |
| footage-7(MAJOR) 現金カテゴリが排他予約から欠落 | cash_bundles/cash_on_table/hands_counting_cash/evidence_bag_cash を排他予約追加・tag内排他予約をfail-closed強制 | §3.5-C |
| footage-8(MAJOR) arc fingerprintがEP33完成依存で片肺 | 台帳にversion/status付与・`check_arc_conflict.py`(EP33確定時に再突合)追加・EP34完成条件をstatus=確定 or 凍結にhard化・下流は上流暫定を上書きしない | §3.5-C/§14 |
| footage-9(MINOR) generic_symbols 4種のみ | evidence_bag/courthouse_columns/courthouse_steps/handcuffs/cash_on_table/federal_seal追加・アーク横断(3話合算)≤2・Codexプロンプト禁止列に追記 | §3.5-D |
| footage-10(MINOR) evidence bag棚ラベル破損トラップ | evidence bagはCodex専用生成・factory棚evidence_bagタグ使用禁止・footage_signoffでカートゥーン検出FAIL | §3.5-E/§10.1 |

### animation（モーション）
| 指摘 | 対応 | 該当§ |
|---|---|---|
| animation-11(BLOCKING) タイトルビート#24-26を降格ルール違反で分子算入 | #24-26をキネティック度床未達で補助降格・返還新figure#27追加・幕4の60秒窓固有figure≥1を余剰充足・実キネティック分子23に再カウント | §3.3 |
| animation-12(MAJOR) ゲート通過でも「アニメ少ない」 | 60秒窓キネティック被覆≥40%(被覆率床に格上げ)＋真アニメ/動く実写の合計screen-time≥全体40%＋motion_energy p50≥13追加 | §3.0/§3.2/§3.7 |
| animation-13(MAJOR) 実証2カット・ツール未実装 | 代表窓(連続スチルワースト窓含む)を実レンダしwindow motion_energy添付・全画像カット併走モーション必須フィールド・check_flat_windows/motion_energy改修をハードブロック | §3.7/§12 |
| animation-14(MINOR) hero面5未割付・走光反復 | 5面を具体figure名/尺≥12s/占有≥45%で§3.4割付・走光主運動は分子外・主運動は物体実移動を必須フィールド宣言 | §3.3/§3.4/§3.7 |

### brightness（明るさ）
| 指摘 | 対応 | 該当§ |
|---|---|---|
| brightness-16(BLOCKING) 計測ROI自己矛盾(帯除外 vs 全フレーム) | 計測量を全合成フレームmedian(プレート帯/ビネット込み)に一本化・帯除外計測を恒久禁止・precomposeも全フレーム | §3.1 |
| brightness-17(MAJOR) SceneBed≥42 vs per-cut≥48矛盾 | SceneBed地色ローカル最小をRec709 Y≥48へ・または明部占有≥55%+median≥48 | §3.1 |
| brightness-18(MAJOR) footage net~0.99で持ち上げゼロ | brightness1.25×multiply0.90=net1.125を明示・夜タグにsource luma下限+per-cut median≥48 | §3.1 |
| brightness-19(MAJOR) 最悪例をaverageで計算(ゲートはmedian)・治療luma未計上 | median計算に統一・二峰フレーム明示ケース・duotone/bleed/parallax治療別luma係数を予算に組込み治療別納品下限 | §3.1 |
| brightness-20(MAJOR) 字幕/ロワーサード帯でスクリム重畳 | ビネットcosine falloff開始を短辺0.80へ延長し下14%帯無減光・字幕帯ビネット非適用・当該帯median≥40追加 | §3.1/§3.6/§5.5 |
| brightness-21(MAJOR) 実装済はbody_lumaのみ・過去失敗指標 | check_image_cut_lumaを最優先ビルド・暫定でbody_lumaに12秒窓median≥44/連続暗≤1.5s追加・暗frame率≤15%へ厳格化 | §3.1/§3.7/§6.1 |
| brightness-22(MINOR) 前景ROI OR条件で黒潰れシルエット通過 | median≥40を必須(AND)・5%ile床+輪郭エッジ強度床をAND追加・完全潰れは機械FAIL | §3.1 |
| brightness-23(MINOR) 納品YAVG≥68がムードと衝突・フォールバック未規定 | 暗シーン例外パス=納品下限下げる代わりに合成側multiply/vignette減弱でpre-composite median≥48・再生成上限3回 | §10.2 |

### sound（音）
| 指摘 | 対応 | 該当§ |
|---|---|---|
| sound-21(MAJOR) L2-25 vs audible_floor・ミュート/近無音窓で矛盾 | 3LUマージンを定常部のみに限定・L2ミュート窓はL3持ち上げ・HOOK/OPを除外窓と明文化 | §4.0/§4.5 |
| sound-22(MAJOR)→既反映(round3) 低域roar | check_lowfreq_rumble二重判定(単調増加+絶対上限+重心)・120Hz HPF (維持) | §4.1 |
| sound-23(MAJOR)→既反映 パレット運用可能化 | spectral-tilt実測照合・参照帯 (維持) | §4 |
| sound-24(MAJOR) SFX供給台帳が無い | sfx_inventory.json新設・≥18-20 distinctを{tag/source/秒/cut_id}列挙・不足0のhardゲート | §4.2/§6.1 |
| sound-25(MAJOR) 1:1束縛がファイル数のみ検査 | check_sfx_distributionに束縛検査追加・各SFXがcut_id+意味タグ必須参照・未束縛FAIL | §4.2 |
| sound-26(MINOR)+gaming-36 40秒床の可聴変化未定義/密度骨抜き | 可聴変化を測定可能定義(cue遷移 or 帯域≥3dB変化)・L2/L3のみ充足は連続≤3窓・各幕L4≥6・60秒窓新規はL4のみカウント | §4.2 |
| sound-27(MAJOR) bed distinctnessが幕1除外・幕1/幕3近似 | 対象を全ベッド(幕1/HOOK/ED)へ拡張・幕3を純データトーンへ再設計 | §4.1 |
| sound-28(MINOR) L2/L3変化のみ連鎖充足 | 連続40秒窓のL2/L3のみ充足≤3個上限 | §4.2 |
| sound-29(MINOR) 60秒窓新規distinct vs床18の整合 | 「新規distinct=当該窓にL4イベント存在」に一意確定・全編distinct床≥20へ整合 | §4.2 |

### gaming（グッドハート）
| 指摘 | 対応 | 該当§ |
|---|---|---|
| gaming-27(BLOCKING) レジストリがスタブ/no-opを検出しない | 負のフィクスチャ回帰検証追加・各ゲートが不良でFAIL+良品でPASSの両方を実証・回帰コーパスをtests/fixturesに固定commit・オーナー抜き取り | §6.0/§7/§12 |
| gaming-28(BLOCKING) content_densityが自己参照床 | 絶対床に固定(133語/60秒窓・180秒≥400語・VO active≥0.80)・幽霊参照削除 | §8 |
| gaming-29→既反映 スコアカード偽満点 | 各軸を実装済/公開後に分離・honest減点 (維持) | §13 |
| gaming-30(MAJOR) check_reviews非空≠妥当・AI自己採点 | レンジ検査追加(facts.unbound=0/story全カウント≤閾値/pacing 14:00以降窓fail=0)・OL状態遷移必須・13フックをオーナー1本ずつサインオフ | §2.1/§6.3 |
| gaming-31(MAJOR)=footage-6重複 スチル代替で床可変 | 35%不変量固定(footage-6と同一是正) | §3.5-A |
| gaming-32→既反映 増補/トリム | 実測後適用・無音/スロー禁止 (維持) | §2.6 |
| gaming-33(MAJOR) §2.5実書換の実カウント未添付 | §2.7に手計算カウント表添付・story_review再出力・check_rhetoric_counts緑まで固定しない順序に | §2.3/§2.7/§12 |
| gaming-34(MINOR)=animation-11 タイトルビート水増し | #24-26補助降格(animation-11と同一是正) | §3.3 |
| gaming-35(MINOR) 150wpmで115語削減要だがトリム60語 | EP31実測158wpm基準を引用・≥115語トリム事前確保・遅端は再収録確定を明記 | §2.6/§8 |
| gaming-36(MINOR)=sound-26 40秒床緩和 | フィラー禁止＞密度床の優先を数値で両立(sound-26と同一是正) | §4.2 |

### thumbnail（サムネ）
| 指摘 | 対応 | 該当§ |
|---|---|---|
| thumbnail-35(BLOCKING) 本命案A非二人称が全案二人称床/スコアカードと矛盾 | 案Aを二人称paradox「THEY TOOK YOUR CASH.」へ書換・床/本命/スコアカードを一致 | §9.2/§13 |
| thumbnail-36(MAJOR) 3語床がparadoxの核を殺す | paradox本命に限り4-5語緩和・逆説語(NO CRIME/ANYWAY)必須・断定案は≤3語・逆説語有無を手動QC | §9.2 |
| thumbnail-37(MAJOR)→既反映(round3のparadox昇格を維持しつつ) | 案A=paradox本命 (維持・二人称化) | §9.2 |
| thumbnail-38(MAJOR) 機械ゲートが輝度のみ・地味検出ゼロ | check_thumbnail_saliency.py新設(面積≥35%/エッジ密度/色数≤4/文字bbox≤3)を機械床に昇格・手動QCは最終確認 | §9.2/§6.1 |
| thumbnail-39(MAJOR) 最強gap+二人称の案Cを保留に降格 | 案Cを初期A/B対抗へ昇格・案Bを保留・初期組合せ=案A×案C | §9.2/§12 |
| thumbnail-40(MINOR) 人間要素なし冷たいマネー静物 | 本命に匿名の手/保安の手が奪う構図を組込み(人間ドラマ+二人称脅威) | §9.2 |

### aismell（AI臭）
| 指摘 | 対応 | 該当§ |
|---|---|---|
| aismell-41(BLOCKING) §2.5がmeta8-9/対句3/aphorism超過で確定稿不成立 | §2.5を実書換(meta2/対句1/aphorism≤1/幕)・§2.7手計算カウント表添付・§12 step4順序をrhetoric緑後にnarration固定へ | §2.3/§2.5/§2.7/§12 |
| aismell-42(BLOCKING)=aismell-41核 | 同上(実書換+カウント添付) | §2.7 |
| aismell-43(MAJOR) 修辞疑問+数字クリフハンガー定型がカウンタ未検出 | interrogative-cliffhanger≤2をcheck_rhetoric_countsに追加・Act1末/Act2末を書換(§2.7=2件) | §2.3/§2.5/§2.7 |
| aismell-44(MAJOR) 「designed to run」「very good at taking cash」narrator評価断定 | critics帰属/「by the numbers reported」帰属へ書換(§2.7 narrator評価=0件) | §2.5/§2.7 |
| aismell-45(MAJOR) エピグラム決め台詞残存 | 「badges changed;pattern did not」等を具体描写化・「a floor rather than a ceiling」→「a low-end figure」・asyndeton四連は全編1回を台帳固定 | §2.5/§2.7 |
| aismell-46(MINOR) 二人称感情命令 | 「It could happen to yours」→事実接地・「that is the right response」削除・感情命令最小化 | §2.5 |
| aismell-47(MINOR) 「a claim worth sitting with」narrator肯定 | 削除し「weigh their claim as one side.」で停止 | §2.5/§2.7 |
| aismell-48(MINOR) Act4-5機関略称スタック | 固有名密度1分窓実測・機関総称へ集約・HSI/CBP等は画面ロワーサードへ委譲 | §2.3/§5.6 |

### retention（視聴維持）
| 指摘 | 対応 | 該当§ |
|---|---|---|
| retention-48(MAJOR) 最長フック間隔が最退屈な法制度解説の上 | 幕2内部間隔≤1:30重み付け・~5:10フック追加・follow-the-money前倒し | §2.4/§2.5 |
| retention-49→既反映 統計を人間ビートで分断 | 4大数字を人間ビートで分断 (維持) | §2.5 |
| retention-50(MAJOR) クライマックス後30%離脱の機構が幽霊参照 | 14:00以降各60秒窓pass/failをpacing_review.json必須フィールドに実ゲート化・scorecardを第二クライマックス~16:00に固定 | §2.1/§2.4/§6.1 |
| retention-51(MAJOR) 維持ゲート全未実装 | retention_dryrun.json(飛ばしたくなる30秒マーキング)をpreflight必須添付・VO後に暫定TC→実TC差替再判定 | §6.3 |
| retention-52(MAJOR) OL④が禁止クリフハンガーに解決 | フィナーレをOL④に賭けず解決ペイオフ(返還/プログラム停止/scorecard)主役・OL④は部分回収+次話ティーザー降格 | §9.1/§2.5 |
| retention-53(MINOR) 中核gap消費後の後半牽引欠如 | OL⑤収益ループを幕2で張り幕5 scorecardで回収 | §0/§2.4/§2.5 |
| retention-54(MINOR) 増補が最密統計幕に統計追加 | 増補は統計でなく人間物語・幕3に5つ目総額を追加しない・幕1/幕4優先 | §2.6 |

**累積サマリ**: BLOCKING 8/8・MAJOR 30/30・MINOR 16/16 反映済み。round 3残存の設計内矛盾(footage算術・輝度ROI・サムネ二人称・OL④潜脱・レジストリスタブ穴・台本未書換)を実是正。過去失敗38項に名前のある機構を§11で紐付け。