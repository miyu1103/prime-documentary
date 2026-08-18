# 是正台帳（累積・v005＝敵対監査55件全反映）

凡例: 対応=[修正済/仕様確定]／該当セクション。BLOCKING/MAJOR=40件は全て設計本文を直接修正。MINOR=15件も全解消。

## captions（6件）
| # | severity | 指摘要旨 | 対応 | 該当§ |
|---|---|---|---|---|
| c1 | MAJOR | onset検出トラック未指定（mux音でSFX先行→偽ラグ） | verify_caption_sync入力を分離VOステム(vo_master)に固定＋VOステム==mux VO位置突合＋OG-0偽green検証 | §4.2, §5.0, §6.1 |
| c2 | MAJOR | 測る(.srt)≠映る(.ass)不一致 | .assは.srtから機械生成(\fadのみ・event-start不変)＋event-start/行数/字数突合ゲート＋測定は.assで実施 | §5.0, §5.1, §12-4 |
| c3 | MAJOR | exact/late/driftのhard/report矛盾 | 現行実装を実査し「現hard=p50/p90/per-min/機能語/matched、exact/late/driftはreport-only」と正直確定。§IMPLEMENTED「hard配線済」を楽観過大表記と明記しOG-0でhard化 | §5.1表 |
| c4 | MAJOR | 現床がドリフトに粗すぎ | exact≥75/late≤12/§5.3 5条件/windowedをOG-0 hard物理前提へ昇格＋単調累積(0→0.45s)フィクスチャ | §5.3, §6.1 |
| c5 | MAJOR | alignment_anchors未定義 | (a)期待語(b)独立onset源(c)\|lag\|≤0.12s(d)FAIL(e)OG-0スミア発火 を完全定義 | §5.1 |
| c6 | MAJOR | 高速金額cue重なり/チラつき | 連鎖cueリード0クランプ・overlap=0・<0.80s統合・check_caption_lines機械FAIL・OG-0チラつき検証 | §5.2 |

## footage（6件）
| # | severity | 指摘要旨 | 対応 | 該当§ |
|---|---|---|---|---|
| f4 | BLOCKING | distinct0.406がプレート再分類水増し | プレート=図内包で分子分母とも除外。実写46+単独画像100=**146/324=0.451**(+0.05マージン)。床ぴったり禁止 | §3.5, §10.1 |
| f5 | MAJOR | arc_nonoverlap未実装+上流タグ未検証 | [OG-0.5]でEP33/34 content-tag列実在を物理確認・無ければ再抽出・OG-0にEP33 printing_press回帰 | §12-0.5, §14.7 |
| f6 | MAJOR | 制度素材content-tag≤1と「専用ロケ」矛盾 | アーク割当確定表(printing_press/courtroom_empty=EP33/34消費→EP35は図F10/F18代替)・制度実写10→8控除 | §3.5C |
| f7(D) | MAJOR | rendered_footage_min≥40がFederal専用ロケと矛盾 | 実写床40→**34**へ現実化・不足はCodex単独画像補填(分母一致)・Federal事前調達タスク化 | §3.5D, §12-5 |
| f9 | MINOR | 図背景プレート算入/在庫扱い | プレート=図内包(uncounted)・連続露出≤3・在庫は未QC候補プールと明記 | §3.5E |
| f10 | MINOR | 画像再利用≤3が未配線疑い | footage_diversityから分離【要配線】・個別max≤3・OG-0同一sha4回=赤 | §6.1 |

## animation（6件）
| # | severity | 指摘要旨 | 対応 | 該当§ |
|---|---|---|---|---|
| a11 | BLOCKING | cadence違反見逃し(F2→F3 105s等) | **F2b(2:10)/F5b(5:15)/F14c(13:45)新設**・全隣接ペア機械再計算(全≤90s)・手計算✔撤回 | §3.6 |
| a12 | MAJOR | motion_energy単位未定義 | **%/幅・秒に統一**(≥16px/s≈0.83%・p10≈0.57%)・depth床をp10超へ | §3.0 |
| a13 | MAJOR | depth床2.5%が低速slideshow | depth床**2.5→4.0%/幅秒**・連続depth**20→12s**・全depthに構造モーション必須・最小動き12カット自動抽出 | §3.0, §3.7, §6.2 |
| a14 | MAJOR | 要素≥6が自己申告メタデータ | **描画後独立運動要素(optical-flowクラスタ)で実測**・メタデータ非合否源・OG-0「6宣言実動2=赤」 | §3.0, §3.6 |
| a15 | MINOR | 図数22vs24・hero6vs8不整合 | **27図・hero8**で全箇所整合 | §3.0, §3.6, §13 |
| a16 | MINOR | L0正弦呼吸/L1往復ループ残置 | L0正弦・L1往復ループ**撤去**しイベント駆動/一方向ドリフトへ | §3.1 |

## brightness（5件）
| # | severity | 指摘要旨 | 対応 | 該当§ |
|---|---|---|---|---|
| b17 | BLOCKING | scrimが生成側へ逆伝播せず字幕下潰れ | scrim0.35→**0.28**・scrim帯被写体**pre-grade median≥68**逆算明示・被写体下1/3は字幕上段強制 | §3.3E, §10.3 |
| b18 | BLOCKING | mean床が生成側に無い | §10.3に**pre-grade mean≥56・dark(<44)≤25%**追加・build_footage_contact_sheetにmean/dim合否列 | §3.3D2, §10.3 |
| b19 | MAJOR | SceneBed輝度証明が図フレームのみ | 図支配/写真支配の二系統証明・写真はコーナーROIワーストケース算出 | §3.3B2 |
| b20 | MAJOR | signalstats range取り違え・HEX過少 | range pin(in_range=tv:out_range=full後YAVG)・全HEX**full-range Y'実算**で暗端≈58へ再指定・mid-gray128回帰 | §3.3A, §3.3B |
| b21 | MINOR | dim閾値44がSceneBed床にGoodhart較正 | dim閾値を知覚基準**Y<40**へ独立化 | §3.3D |

## sound（6件）
| # | severity | 指摘要旨 | 対応 | 該当§ |
|---|---|---|---|---|
| s23 | MAJOR | gavelが民事案に意味的不整合 | **gavel削除**・2016 fee判決のみ中立low_ruling_stamp・MUS-05 data_verdict→**data_reveal**改名・画面ID署名 | §4.5, §4.3 |
| s24 | MAJOR | DSP4ゲート閾値未確定 | roar≥3dB&<300Hz比≥0.6／bed_loop≤0.35／cluster_buzz第一ピーク/平均≥3.0／low_band中央値+4dB を確定 | §4.8, §4.10 |
| s25 | MAJOR | SFX事象密度床欠如(薄い音) | **check_sfx_density新設(各Act≥6・≥1本/25s)**・17→21種・Act2/Act5にSFXレーン実配置 | §4.5, §4.7 |
| s26 | MINOR | ED MUS-07 -18でVO競合 | ED VO区間-23〜-21ダック・"That is next."後-18・サイドチェーン適用 | §4.8 |
| s27a | MINOR | スタンプ同族6種が単調 | 音色分離(中心周波数/アタック)・同族間隔≥8s | §4.5 |
| s27b | MINOR | Kurzgesagt引用倒れ | 各cue調/テンポ/楽器/動機/和声・アーク回想モチーフ定義 | §4.3 |

## gaming（10件）
| # | severity | 指摘要旨 | 対応 | 該当§ |
|---|---|---|---|---|
| g31 | BLOCKING | 台本実wc2,704(要求の半分) | **本文をwc3,190まで実書**(BSA1986/instance/McLellan/公聴会/30日ルール)・check_script_wordfloor新設・wc実出力貼付 | §2.6, §2.0 |
| g32 | MAJOR | 「実測2」架空値 | check_script_binge実装後に実出力貼付・命令/Here is/三段を**本文実カウント**(命令2/Here is1/三段1) | §2.0, §2.5 |
| g33 | MAJOR | 開ループ密度が傘ループL4で自明緑 | **傘ループを密度計算から除外**・短中期(span≤3-4分)のみカウント・12s窓はlive短中期・90s窓新展開別metric | §0, §2.1, §2.4 |
| g34 | MAJOR | OG-0フィクスチャが同一実装者(水増し可) | **独立held-outセット・第三者(別セッション/別モデル)確認**・§13未通過は仮点(実現100不主張) | §6, §12-0, §13 |
| g35 | MAJOR | info_beat≤22sが辞書一致で終盤衝突 | 意味単位(新因果/視点/スリル)へ再定義・Act5後半/ED≤40s・aismell固有名詞キャップと統合 | §0, §8.2 |
| g(cap) | MAJOR | srt-start自己一致+matched95→60弱体化 | 整列(wav2vec2)と検証(独立onset)を別系統・matched≥60据置(根本是正後85目標) | §5.1 |
| g(hex) | MAJOR | 未レンダで「実測確認」偽測定 | 全「実測確認」→「目標値(未レンダ)」・実測はmux後のみ・暗端Y'≈58マージン確保 | §3.3B, §6.2 |
| g36a | MINOR | 要素≥6メタデータcount-gaming | 描画後実測へ(a14と同) | §3.6 |
| g36b | MINOR | distinct0.406綱渡り | 0.451へ(+0.05マージン)・pHash近接除外 | §3.5A |
| g36c | MINOR | 3レビュー自己署名 | story=bingeを別モデル独立実施・署名ID記録 | §2.1, §14.13 |

## thumbnail（5件）
| # | severity | 指摘要旨 | 対応 | 該当§ |
|---|---|---|---|---|
| t35 | BLOCKING | 案Aグレースケール地味・Y≥33が地味さ非検出 | **thumbnail_saturation新設(≥20%画素S≥0.5)**・**一次を案B(赤基準線)へ再評価**・案A数字を赤塗り | §9.2, §6.1 |
| t36 | MAJOR | 案A 3テキストゾーン+字高/面積矛盾 | テキスト2ゾーンへ削減・$32,820を画面高1/3=240pxに統一(392px撤回)・320px実測 | §9.2 |
| t37 | MAJOR | $0.00に字高/コントラスト床なし | 残高を空欄/斜線ビジュアルで暗示(文字依存排除)・使う場合≥30px/≥4.5 | §9.2 |
| t38 | MAJOR | thumbnail_text_contrast未実装を合格根拠に引用 | OG-0で先行実装・3案$0/$32,820個別ROI実測を承認前提に | §9.2, §6.1 |
| t39 | MINOR | 案C二人称欠如+IRS印リスク | 案C主コピー二人称化`THEY CAN EMPTY YOURS.`・IRS実在記章→匿名官製封筒 | §9.2 |

## aismell（10件）
| # | severity | 指摘要旨 | 対応 | 該当§ |
|---|---|---|---|---|
| ai41 | BLOCKING | 自己申告カウントが本文と矛盾 | 本文で実削減(Here is3→1・命令7→2)・実カウント貼付・§13は実緑後のみ満点 | §2.0, §2.6 |
| ai42 | MAJOR | 未追跡定型(It is worth×5等) | script_binge計数に It is worth≤1/whole story≤1/music swell=0 追加・本文実削除(0/0/撤去) | §2.1, §2.6 |
| ai43 | MAJOR | L5 fee対比が無根拠断定 | **CLM-0011/0013(grade A)に明示紐付け=cite**(撤回でなく)・700マイル削除 | §1.1, §2.6 |
| ai44 | MAJOR | McLellan/TIGTA数値が無根拠 | CLM-0012/0014(grade A)紐付け・278/91%/231件/$17.1M/$107,702.66/301/$2M統一 | §1.1, §1.2 |
| ai45 | MINOR | 91%「金額」vs件数混同 | 本文「ninety-one percent of those **cases**」・「money it could not tie to any crime」 | §2.6 |
| ai46 | MINOR | BSA1970「cartels」時代錯誤 | 「organized crime and dirty money moving through banks」(台帳語) | §2.6 |
| ai47 | MINOR | 否定アナフォラ多用 | アナフォラ率≤2/千語をscript_binge計数・一部通常文化(三段=1に抑制) | §2.1, §2.6 |
| (ai職員) | 内包 | 職員が金綺麗と認めた断定 | 本文削除・「業界の経営者たちが証言」(個人告発なし・政府中立) | §2.5 |
| (ai売却) | 内包 | 売却無ヘッジ | 「According to her lawyers and the reporting」ヘッジ | §2.6 |
| (ai立法) | 内包 | Carole立法助力 | 「one of the stories that put this abuse in front of the country」報道帰属 | §2.6 |

## retention（5件）
| # | severity | 指摘要旨 | 対応 | 該当§ |
|---|---|---|---|---|
| r1 | BLOCKING | Act2 3分無情報コア(info_beat FAIL) | 7:10「歩き去るowner」F7＋watchdog伏線＋二人称金額ラインでinstance分断・info_beat実走査 | §2.6 Act2, §8.2 |
| r2 | MAJOR | Act5末尾18:15→ED無フック | **18:45 二人称脅威＋次回オープンループ新設**・rehook config追加・gap≤2:00検査窓登録 | §2.4, §2.6 |
| r3 | MAJOR | rehook配置が条件(b)新固有名詞未充足 | check_script_binge実出力を貼る運用・不足位置に新数字/名追加 or 削除 | §2.4 |
| r4 | MAJOR | front-load露出/back-load新奇 | McLellan/TIGTA を Act2 伏線開通・Act1圧縮で押収~4:05・5:00-11:00 per-window報告 | §2.6, §8.2 |
| r5 | MINOR | without prejudice 5分記憶依存 | 13:00-13:40再喚起＋F11に"WITHOUT PREJUDICE"常時ノードをAct4通し表示 | §2.4, §3.6 F11 |

## 反映サマリ
- BLOCKING 8件（f4/a11/b17/b18/g31/t35/ai41/r1）＝全て設計本文を直接修正し数値・実HEX・実wc・実DSP定義で確定。
- MAJOR 32件＝全て該当§を修正、未実装ゲートは【要実装】＋OG-0独立フィクスチャ条件で正直明示。
- MINOR 15件＝全解消。
- 水増し是正の核心: 台本wc3,190実書／distinct0.451実算(プレート撤廃)／cadence全ペア機械再計算／HEX full-range実算／音DSP全閾値確定／「実測確認」→目標値訂正／OG-0独立held-out第三者確認。