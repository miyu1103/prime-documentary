# 縦型ショート コード演出設計書 — 全15本（Codex渡し用 / 制作可能版）

目的：縦9:16ショート15本を「現時点での最高の設計」に引き上げる。長尺EP10で判明した教訓
（汎用テンプレ＝MovingImage/Ken Burns だけでは「意味のあるアニメ（天秤/地図/票/年表/図解）」は出ない。
良いアニメは**コード演出部品**で出す）を、縦型にも適用する。

- 本書は **`SHORTS_REMOTION_SPEC.md`（縦テンプレ仕様A）の上に乗る演出設計**。データ契約・レイアウト・音・字幕は仕様Aに従う。
- 雛形にした長尺の書き方：`episodes/PD-2026-010-kelo/08_edit/edit_design.v001.md §6`（Premium級コード演出）。
- **ビート時間表・テロップ・VO・画像割当は `SHORTS_EP1-8.md` / `SHORTS_EP9-15.md` が正**。本書はそこに**一致させて**演出だけを足す。台本は変えない。
- 部品名は `remotion/src/` 実在を確認済み（§A）。無いものは「**新規実装**」と明記した。

---

## §1 方針：縦でも“意味あるアニメ”はコード部品で出す（MovingImageだけにしない）

縦の各ビートは、原則として次の2層で構成する。

1. **背景層（ベース）**＝AI画像 + `MovingImage`（kenburns/parallax/pushin、静止禁止）。仕様A §5 のとおり。
2. **演出層（意味のあるアニメ）**＝**コード部品**を背景の上に**ラップ/重ね**て出す。これが“天秤/票/地図/年表/図解/数字”を担う。

つまり「`Short.tsx` のビート種別に応じて、背景の上にコード演出レイヤを差す」設計にする。
ビート全部にコード演出を盛る必要はない。**各ショートの“1つの驚き”（山場ビート＝多くはb2/オチ）に最低1つ**、意味あるコード演出を必ず入れる。

### 既存の長尺コード部品を縦へ流用/ラップする方法

| 部品（実在） | 実体 | 縦への流用方法 |
|---|---|---|
| `SceneArt` | `components/SceneArt.tsx`。props=`visualMode`/`motifHint`/`onScreenText`/`seed`。内部で `gavel/scales/document/room/courtroom/map/timeline` を自動選択し、`MovingStage` で動かす。**SVG中心・$0・実写と誤認しない（invariant 11）** | **そのまま縦で使える**（中央寄せ・viewBox固定SVGなので9:16でも破綻しない）。背景AI画像の代わりに、または上に半透明で重ねる。`onScreenText` は3行までだが**テロップは仕様Aの上ゾーン(y180-560)に別途出す**ので、ここは空配列 `[]` 推奨（二重表示回避） |
| `Motion`：`MovingStage`/`CameraRig`/`Particles`/`LightSweep`/`Vignette` | `components/Motion.tsx` | **縦で完全動作**（全部AbsoluteFill・解像度非依存）。`MovingImage` の代替/補強に。山場は `LightSweep color={GOLD}` で“確定”感を出す |
| `Grain` | `components/Grain.tsx`。`opacity` のみ | 全ビート最前面に薄く重ねる（0.05前後）。縦でそのまま |
| `KineticType` | `components/KineticType.tsx`。`lines:{text,emphasis?,at}[]`/`align`/`transparent` | **キーワード強打/オチの一言に最適**。`transparent` で背景AI画像に重ねられる。ただし `padding:120` 固定なので縦では文字が中央寄りに出る→**上ゾーンのテロップとぶつかる場合は `transparent` + 後述の `safeTop`/`safeBottom` 配慮版を新規ラップ**（§4） |
| `DiagramFlow` | `components/DiagramFlow.tsx`。`steps:string[]`/`stagger?` | **A→B→C の因果・手順**（例：スワブ→DNA→DB照合）。**flexDirection:'row' 固定**＝横3箱。縦では3箱が画面幅を食い切る→**2語までに絞るか、縦積み版 `DiagramFlowVertical` を新規実装**（§4） |
| `CitationLowerThird` | `components/CitationLowerThird.tsx`。`label`/`source?`/`claimIds?` | 出典/年号の焼き込み。**ただし `margin:0 0 90px 90px`（左下）＝縦の字幕ゾーン(y1280-1560)と衝突**。→ **縦では左上に出す `CitationTopLeft` を新規実装**、または `transform` で上に逃がす（§4） |

### 長尺Premium（`CarpenterPremium.tsx`）のビズ＝縦は“要改修”

`Vote`(5–4)/`MapGrid`/`TwoColumn`/`Doors`/`BigNumber`/`CourtColumns` は**1920×1080前提のハードコード座標**（例：`Vote` は `translate(520 430)`、`TwoColumn` は `left:260 right:260 top:360`、`BigNumber` は `top:420`）。
**縦9:16にそのまま置くと位置が破綻**する。→ **縦用に座標を作り直した小コンポを新規実装**する（§4）。意匠（色・票の並べ方・等式の見せ方）は流用してよい。

> **重要**：`Vote` は **5–4 がハードコード**。ショートの評決は話ごとに違う（§3の評決欄参照。#8/#10/#13=5–4、Miranda/Gideon/Mapp/Riley/Timbs=9–0、King反対4人 等）。**必ず可変化**（`VoteVertical yes/no` props）すること。

---

## §2 縦用コード演出パレット（ビート種別 × 実在部品）

縦の構成は **フック(hook) → 展開(b1/b2) → オチ(b2末/結論) → CTA**（仕様A §1・各 `SHORTS_EP*.md` の時間表）。
ビート種別ごとに「使ってよい意味あるアニメ」を実在部品名で示す。

### hook（0:00–0:03・最初の1秒で掴む・速いカット＋SFX）
- 背景＝AI画像 `MovingImage(motion='pushin', fast=true)` ＋ `Particles`/`LightSweep`。
- 問いの一言＝`KineticType`（`emphasis:true` の1行、`transparent`）で**上ゾーンに**打つ。
- 数字フック（例 #4「80億ドル」/ #8「127日」）＝`BigNumberVertical`（新規・§4）を一瞬だけ。

### 展開（b1/b2・1カット3〜4秒・“意味”を見せる主戦場）
- 年表 = `SceneArt motifHint="timeline"`（年マーカーが進む）。年号確定は `CitationTopLeft`（新規）。
- 地図/全米波及 = `SceneArt motifHint="map"`（USマップ＋ピン波紋）。州カウントは `BigNumberVertical`。
- 天秤/比較衡量 = `SceneArt motifHint="scales"`（傾く天秤）。
- 因果・手順 A→B→C = `DiagramFlowVertical`（新規・縦積み）。
- 左右/狭義広義の対比 = `TwoColumnVertical`（新規・上下2枚 or 縦並び）。
- 図解の組み上げ（アイコン列） = `DoorsVertical`（新規・縦積み）or `DiagramFlowVertical`。
- 書類/令状/印章 = `SceneArt motifHint="document"` or `"seal"`（書類が描かれ印が押される）。

### オチ（結論ビート b2末・本話の“1つの驚き”を確定させる山場）
- 票決 = `VoteVertical`（新規・話ごとの yes/no）。`LightSweep color={GOLD}` を同期。
- キーワード確定 = `KineticType`（`emphasis:true`）で結論の一言。
- 崩落/反転（#5タワー崩壊・#15評価額崩落）= `MovingStage` + 専用SVG（`CollapseViz` 新規）。

### CTA（0:40–0:45・本編誘導・ループしやすく）
- `BrandEndcard`（`components/Bookends.tsx`）流用 or 手組みSubscribe。`ctaText` を `KineticType` で。
- 末尾は無音ぎみ→ループ。

### セーフエリア（仕様A §4 厳守・コード演出にも適用）
- **上ゾーン y180–560**＝テロップ/見出し（`KineticType`・`SceneArt`の見出し）。ここ**だけ**にテロップを置く。
- **下ゾーン y1280–1560**＝ナレ字幕（`CaptionLayer`）。**コード演出はこの帯に絶対被せない**。
- 中央 y560–1280 が**コード演出（票/地図/天秤/図解/数字）の主舞台**。
- `SceneArt`/`DiagramFlow`/`KineticType` は `padding`/中央寄せのため概ね中央に出る＝OK。だが**新規縦コンポは `top` を 600〜1240 の範囲に収める**こと（上下ゾーンを侵さない）。
- 右端120px・下端300pxは重要要素を置かない（プラットフォームUI）。
- 出典は左上（`CitationTopLeft`）。下左の `CitationLowerThird` は**縦では使わない**（字幕と衝突）。

---

## §3 全15本 per-short モーション設計表

各ショートに、各ビートの「意味あるアニメ（具体・実在部品）」を1行で割り当てる。
**ビート時間/テロップ/画像は `SHORTS_EP*.md` の時間表に一致**（左欄に再掲）。「演出（コード部品）」が本書の追加指定。
評決欄＝`VoteVertical` に渡す yes/no（票割れの話だけ）。

### SHORT #1 Miranda（なぜ警官は“権利”を読む？）評決=9–0
| ビート(時間/テロップ) | 画像 | 意味あるアニメ（コード部品） |
|---|---|---|
| hook 0:00 なぜ警官は“権利”を読む？ | 01 取調ランプ | `MovingImage pushin/fast` + `SceneArt motifHint="room"`(ランプ明滅) + `KineticType`(問い1行) |
| b1 0:03 警告なしの密室 | 02,03 | `SceneArt motifHint="room"` 光コーン呼吸 + 時計パララックス（長時間） |
| b2 0:12 1966 最高裁が線を引く | 04,05 | `SceneArt motifHint="timeline"`(1966へ) + `CitationTopLeft`(Miranda v. Arizona, 1966) |
| オチ 0:28 警告なし＝自白は無効 | 06,07 | `DiagramFlowVertical`(["警告なし","自白は証拠から除外"]) + `LightSweep gold` |
| CTA 0:40 本編はチャンネルへ | 07止め | `BrandEndcard` + `KineticType`(ctaText) |

### SHORT #2 Gideon（鉛筆1本で全法廷を変えた）評決=9–0
| hook 0:00 払えなければ弁護士は付く？ | 01 空の弁護人席 | `MovingImage pushin/fast` + `KineticType`(問い) |
| b1 0:03 弁護士を断られ有罪 | 02,03 | `SceneArt motifHint="courtroom"` 光スイープ + 閉じる扉パララックス |
| b2 0:12 独房から鉛筆で嘆願 | 04,05 | `SceneArt motifHint="document"`(手書き嘆願が線で描かれる) |
| オチ 0:26 9-0 全法廷を変えた | 06,07 | `VoteVertical yes=9 no=0` + `CitationTopLeft`(Gideon v. Wainwright, 1963) + `LightSweep gold` |
| CTA 0:40 | 07止め | `BrandEndcard` |

### SHORT #3 Mapp（違法な捜索の“証拠”は使える？）評決=（排除法則・9-0扱いでなくテーマは天秤）
| hook 0:00 違法な家宅捜索の証拠は？ | 01 こじ開く扉 | `MovingImage pushin/fast` + `KineticType`(問い) |
| b1 0:03 令状なしで押し入る | 02,03 | `SceneArt motifHint="document"`(令状の“不在”＝空白書類) + 扉パララックス |
| b2 0:12 目当て不在→別件で起訴 | 04,05 | `DiagramFlowVertical`(["違法捜索","別件の本","別件で起訴"]) |
| オチ 0:26 証拠は排除される | 06,07 | `SceneArt motifHint="scales"`(天秤が“警察を律する”側へ傾く) + `CitationTopLeft`(Mapp v. Ohio, 1961) |
| CTA 0:40 | 07止め | `BrandEndcard` |

### SHORT #4 FTX（80億ドルはどこへ？）※本人非描画
| hook 0:00 80億ドルはどこへ？ | 01 取引所ネオン | `MovingImage pushin/fast` + `BigNumberVertical top="$8B" bottom="消えた"` |
| b1 0:03 信頼の暗号資産取引所 | 02,03 | `SceneArt motifHint="document"` + コイン流入パララックス（顔なし） |
| b2 0:12 コードの“抜け穴” | 04,05 | `DiagramFlowVertical`(["顧客の預金","秘密の例外","私的トレード会社へ"]) |
| オチ 0:26 2023 有罪 | 06,07 | `SceneArt motifHint="timeline"`(2023) + `SceneArt motifHint="document"`(有罪) + 空の金庫リビール |
| CTA 0:40 | 07止め | `BrandEndcard` |

### SHORT #5 Madoff（安定リターン、取引はゼロ）※本人非描画
| hook 0:00 安定リターン、取引はゼロ | 01 滑らか上昇曲線 | `MovingImage pushin/fast`（“出来すぎ”の曲線） + `KineticType`(矛盾の一言) |
| b1 0:03 最も信頼された名前 | 02,03 | `SceneArt motifHint="courtroom"`(=権威の象徴) 光スイープ |
| b2 0:12 取引はほぼ無し | 04,05 | `DiagramFlowVertical`(["新規投資家の金","古い投資家へ"]) ＝ポンジの環 |
| オチ 0:26 崩壊→150年 | 06,07 | `CollapseViz`(新規・積み木タワー崩落) + `SceneArt motifHint="timeline"`(2008) + `BigNumberVertical "150年"` |
| CTA 0:40 | 07止め | `BrandEndcard` |

### SHORT #6 Terry（逮捕なしで“止めて触る”）評決=（容認・基準の天秤）
| hook 0:00 逮捕なしで“止めて触る” | 01 夜の路上の制止 | `MovingImage pushin/fast` + `KineticType`(問い) |
| b1 0:03 必要なのは“合理的な疑い” | 02,03 | `SceneArt motifHint="scales"`（“勘”と“証拠”の間で中央に止まるゲージ＝天秤流用） |
| b2 0:12 1968 店を下見する二人 | 04,05 | `SceneArt motifHint="timeline"`(1968) + 店先を行き来する影パララックス → 拳銃リビール |
| オチ 0:28 路上の“低い基準”が誕生 | 06,07 | `DiagramFlowVertical`(["逮捕の基準","より低い基準＝stop & frisk"]) + `CitationTopLeft`(Terry v. Ohio, 1968) |
| CTA 0:40 | 07止め | `BrandEndcard` |

### SHORT #7 Riley（逮捕されてもスマホは見られない）評決=9–0
| hook 0:00 スマホは“例外” | 01 証拠トレイの施錠スマホ | `MovingImage pushin/fast` + `KineticType`(“例外”) |
| b1 0:03 昔は持ち物は何でも | 02,03 | `SceneArt motifHint="document"`(旧来の身体検査＝物の列挙) |
| b2 0:12 スマホ＝人生が丸ごと | 04,05 | `DoorsVertical`(["メッセージ","写真","居場所","人生"]) ＝スマホの中身が組み上がる |
| オチ 0:26 2014 全員一致「令状を取れ」 | 06,07 | `VoteVertical yes=9 no=0` + `SceneArt motifHint="document"`(令状スクロール) + `CitationTopLeft`(Riley v. California, 2014) |
| CTA 0:40 | 07止め | `BrandEndcard` |

### SHORT #8 Carpenter（スマホは、あなたを追跡し続ける）評決=**5–4**
| hook 0:00 127日分の位置を令状なしで | 01 位置の軌跡マップ | `MovingImage pushin/fast` + `BigNumberVertical top="127日" bottom="令状なし"` |
| b1 0:03 数分ごとに位置を記録 | 02,03 | `SceneArt motifHint="map"`(基地局へ ping・点が灯る) |
| b2 0:12 数か月分を会社から入手 | 04,05 | `SceneArt motifHint="map"` 位置ドット蓄積 → `DiagramFlowVertical`(["通信会社","数か月の履歴","現場近くに被疑者"]) |
| オチ 0:26 2018「位置情報も令状」 | 06,07 | `VoteVertical yes=5 no=4` + `SceneArt motifHint="timeline"`(2018) + `CitationTopLeft`(Carpenter v. US, 2018) |
| CTA 0:40 | 07止め | `BrandEndcard` |

### SHORT #9 Timbs（有罪じゃなくても財産を奪える）評決=9–0
| hook 0:00 民事没収：有罪は不要 | 01 赤い証拠タグの鍵 | `MovingImage pushin/fast` + `KineticType`(逆説) |
| b1 0:03 遺族保険で買った車 | 02,03 | `SceneArt motifHint="document"`(保険証書) + SUVパララックス |
| b2 0:12 罰金の4倍を没収 | 04,05 | `SceneArt motifHint="scales"`(SUVが小銭を圧倒する不均衡な天秤) + `BigNumberVertical "4倍"` |
| オチ 0:26 9-0「過大な罰金は禁止」 | 06,07 | `VoteVertical yes=9 no=0` + `CitationTopLeft`(Timbs v. Indiana, 2019) + `LightSweep gold` |
| CTA 0:40 | 07止め | `BrandEndcard` |

### SHORT #10 Kelo（家を私企業のために？）評決=**5–4**・更地のオチ
| hook 0:00 家を私企業のために？ | 01 更地に孤立する家 | `MovingImage parallax/fast`（孤立の家へ寄る） + `KineticType`(問い) |
| b1 0:03 荒れていない“ピンクの家” | 02,03 | ピンクの家へ `MovingImage pushin` + ラベル吹き出し（手組み・小） |
| b2 0:12 “公共の用”と言える？ | 04,05 | `TwoColumnVertical`(上="公共が使う(狭義)" 下="公共目的(広義)") + ガラス塔模型が小さな家に迫る |
| オチ 0:26 5-4 容認→更地のまま | 06,07 | `VoteVertical yes=5 no=4` + `SceneArt motifHint="timeline"`(2005) → **更地リビール**（雑草の空き地・静寂） + `CitationTopLeft`(Kelo v. New London, 545 U.S. 469) |
| CTA 0:40 | 07止め | `BrandEndcard` |

### SHORT #11 Mahanoy（校外の投稿で罰せる？）※本人非描画・罵倒語なし。評決=8–1
| hook 0:00 校外の投稿で学校が罰する？ | 01 消えるアイコンのスマホ | `MovingImage pushin/fast` + `KineticType`(問い) |
| b1 0:03 消えるはずの投稿 | 02,03 | `SceneArt`風の消滅ピクセル（画像パララックス） + 落胆する観客席の影 |
| b2 0:12 スクショは消えない | 04,05 | `DiagramFlowVertical`(["消えるはずの投稿","スクショが残る","コーチに届く"]) |
| オチ 0:26 2021 校外の愚痴は罰せない | 06,07 | `VoteVertical yes=8 no=1` + `BoundaryVertical`（家と学校の“ぼやけた境界線”＝新規 or `SceneArt`代替） + `CitationTopLeft`(Mahanoy v. B.L., 2021) |
| CTA 0:40 | 07止め | `BrandEndcard` |

### SHORT #12 仲裁（“同意”で訴権を放棄）※中立。評決=**5–4**
| hook 0:00 細字が訴える権利を奪う | 01 “agree”ボタン | `MovingImage pushin/fast`（流れる細字） + `KineticType`(逆説) |
| b1 0:03 契約の細字の一文 | 02,03 | 終わらない細字スクロール（パララックス）＋一文ハイライト（手組み下線） |
| b2 0:12 $30から始まった | 04,05 | `BigNumberVertical top="$30"` + `DiagramFlowVertical`(["小さな被害","束ねられない","事実上ゼロ"])（鎖が人を分断） |
| オチ 0:26 2011→2018 職場へ拡大 | 06,07 | `VoteVertical yes=5 no=4` + `SceneArt motifHint="timeline"`(2011→2018) + 閉じる法廷の扉 + `CitationTopLeft`(AT&T Mobility v. Concepcion, 2011) |
| CTA 0:40 | 07止め | `BrandEndcard` |

### SHORT #13 King（逮捕でDNAを採られる）※本人非描画。評決=**5–4**（反対4）
| hook 0:00 逮捕≠有罪。でもDNAは採られる | 01 頬の綿棒 | `MovingImage pushin/fast` + `KineticType`(逆説) |
| b1 0:03 bookingで頬をスワブ | 02,03 | 綿棒→`DiagramFlowVertical`(["綿棒(swab)","DNA二重らせん","全国DB照合"])（**話の核**） |
| b2 0:12 未解決事件と一致 | 04,05 | `SceneArt motifHint="map"`風のDBグリッドで1ノード点灯（=ヒット） + 体の輪郭スキャン |
| オチ 0:26 2013 合法／だが反対4人 | 06,07 | `VoteVertical yes=5 no=4`（反対4を強調・色分け） + `CitationTopLeft`(Maryland v. King, 2013) |
| CTA 0:40 | 07止め | `BrandEndcard` |

### SHORT #14 Lange（警官は家まで追える？）評決=9–0
| hook 0:00 警官は家の中まで追える？ | 01 ガレージ扉に挟まる足 | `MovingImage pushin/fast`（**降りる扉に足**＝象徴ショット） + `KineticType`(問い) |
| b1 0:03 軽い違反→自宅ガレージへ | 02,03 | 追跡パララックス（夜道） → 自宅ガレージへ車が入る |
| b2 0:12 降りる扉に足を入れて | 04,05 | 玄関の敷居に光る一線（`BoundaryVertical`/手組み）＝家の境界を可視化 |
| オチ 0:24 自動立入は不可 | 06,07 | `DiagramFlowVertical`(["軽罪の追跡だけ","自動立入は不可"]) + `TwoColumnVertical`(上="令状" 下="本当の緊急") + `CitationTopLeft`(Lange v. California, 2021) |
| CTA 0:40 | 07止め | `BrandEndcard` |

### SHORT #15 Theranos（約束はいつ“犯罪”に？）※R3・**実在人物非描画**・公開前に法務レビュー必須
| hook 0:00 大胆な約束はいつ犯罪に？ | 01 一滴の血 | `MovingImage pushin/fast`（一滴の血） + `KineticType`(問い) |
| b1 0:03 装置は動かなかった | 02,03 | 中身が空の黒箱デバイス（パララックス）＋雑誌風フレーム（**顔・文字なし**） |
| b2 0:12 他社機器・精度に問題 | 04,05 | `DiagramFlowVertical`(["指先の一滴","精度に問題","他社機器で実施"]) |
| オチ 0:26 2022 投資家詐欺で有罪 | 06,07 | **`CollapseViz`（$9B 評価額の崩落・新規）** + `SceneArt motifHint="timeline"`(2022) + `KineticType`(“故意＝知って欺く”) + `CitationTopLeft`(U.S. v. Holmes, 2022) ※中立アイコン |
| CTA 0:40 | 07止め | `BrandEndcard` |

> R3注意：#15 は**実在人物の肖像・氏名強調を避け**、評決は中立アイコンで。公開前に法務レビュー（MEMORY: EP15 Theranos=R3）。

---

## §4 新規に要る小コンポ（縦用・実装一覧）

既存の長尺Premiumビズは横1080前提のため、**縦9:16用に座標を作り直した小コンポ**を新規実装する。
配置は全て**中央ゾーン y≈600–1240** に収め、上ゾーン(180-560)・下ゾーン(1280-1560)を侵さないこと。意匠（色/票/等式/箱）は `CarpenterPremium.tsx` を流用してよい。

| 新規コンポ | 役割 | 実装メモ（必須仕様） |
|---|---|---|
| **`VoteVertical`** | 評決の票（縦） | **props=`{yes:number; no:number}`（5–4ハードコード厳禁）**。9マスとは限らない（9-0/8-1/5-4を表現）。賛成=BLUE+GOLD枠、反対=グレー。中央に「yes–no」を大表示。`CarpenterPremium` の `Vote` を可変化＋縦座標化 |
| **`BigNumberVertical`** | 数字フック/カウント | props=`{top:string; bottom:string}`。`top` を中央 y≈760 に巨大表示。`BigNumber` の縦座標版 |
| **`DiagramFlowVertical`** | A→B→C を**縦積み** | props=`{steps:string[]; stagger?}`。既存 `DiagramFlow` は `flexDirection:'row'` 固定で縦に不適 → **縦並び**＋下向きコネクタに改修。3箱まで |
| **`TwoColumnVertical`** | 狭義/広義・令状/緊急の対比 | props=`{top,bottom,topSub?,bottomSub?}`。`TwoColumn`(横2枚)を**上下2枚**に。中央ゾーンに収める |
| **`DoorsVertical`** | アイコン列の組み上げ | props=`{labels:string[]}`。`Doors`(横grid)を**縦積み or 2×2**に。順次フェードイン |
| **`CitationTopLeft`** | 出典/年号の焼き込み（縦） | props=`{label; source?; claimIds?}`。`CitationLowerThird` を**左上（y≈180 付近・字幕ゾーンと非衝突）**へ。**縦では `CitationLowerThird` を使わない** |
| **`CollapseViz`** | 崩落/反転（#5タワー・#15評価額） | 積み木/数値が崩れ落ちるSVGアニメ。`MovingStage` + 落下トランスフォーム。$0コード |
| **`BoundaryVertical`**（任意） | ぼやけた/明確な境界線（#11/#14） | `CarpenterPremium` の `Boundary`（横）を縦座標化。家と学校・敷居の一線。`SceneArt` で代替可なら省略可 |
| **`KineticTypeSafe`**（任意ラッパ） | 上ゾーン限定の一言 | `KineticType` を `transparent` + 上ゾーン(y180-560)に固定するラッパ。`padding:120` 固定の中央寄りを避けたい場合のみ |

> いずれも `remotion/src/components/shorts/` 配下に置き、`Short.tsx` のビート種別から差す想定。**型チェック必須**。

---

## §5 受け入れ基準（仕様A §11 を踏襲＋コード演出）

仕様A §11 の全項目に加えて、本書は次を必須とする。

- [ ] 1080×1920 / 30fps / 35〜45秒（仕様A）。
- [ ] **どのカットも動く**（静止なし）。フックは速いカット＋SFX（仕様A）。
- [ ] **字幕がナレと同期**し、**テロップ（上）／字幕（下）／出典（左上）が位置で分離**し一度も被らない。**コード演出は中央ゾーン(y600-1240)に収まり、上下ゾーンを侵さない**。
- [ ] **音4層（ナレ＋BGM＋環境音＋SFX）**＋ナレ中ダッキング（仕様A §6）。
- [ ] **各ショートの“1つの驚き”ビートに、意味あるコード演出が最低1つ**入っている（票/地図/天秤/年表/図解/数字/崩落のいずれか・§3表のとおり）。MovingImageだけのビートで山場を終えない。
- [ ] **`VoteVertical` は話ごとの評決（§3の評決欄）で表示**（5–4ハードコードでない）。
- [ ] **実在人物の肖像なし**・中立・広告安全・ブランド配色（#4/#5/#11/#13/#15は特に厳守）。
- [ ] **#15 Theranos は R3**：実在人物非描画・中立・公開前に法務レビュー。
- [ ] サムネ（縦・大文言）あり。CTAは本編リンク（URLはオーナー差し込み）。公開は6/24以降・各ゲートで停止。

---

## §A 参照した実在コード部品（確認済み）

| 部品 | パス | 主要props |
|---|---|---|
| `SceneArt` | `remotion/src/components/SceneArt.tsx` | `visualMode`,`motifHint`,`onScreenText:string[]`,`seed?`。motif=gavel/scales/document/room/courtroom/map/timeline |
| `MovingStage`/`CameraRig`/`Particles`/`LightSweep`/`Vignette` | `remotion/src/components/Motion.tsx` | `seed`,`intensity?`,`color?` 等 |
| `Grain` | `remotion/src/components/Grain.tsx` | `opacity?` |
| `KineticType` | `remotion/src/components/KineticType.tsx` | `lines:{text,emphasis?,at}[]`,`align?`,`transparent?` |
| `DiagramFlow` | `remotion/src/components/DiagramFlow.tsx` | `steps:string[]`,`stagger?`（横並び固定→縦版要） |
| `CitationLowerThird` | `remotion/src/components/CitationLowerThird.tsx` | `label`,`source?`,`claimIds?`（左下固定→縦は要 `CitationTopLeft`） |
| `BrandOpening`/`BrandEndcard` | `remotion/src/components/Bookends.tsx` | CTA/エンドカード |
| `Vote`/`MapGrid`/`TwoColumn`/`Doors`/`BigNumber`/`CourtColumns` | `remotion/src/compositions/CarpenterPremium.tsx`（**横1080座標ハードコード・Vote=5–4固定**）→ 縦版を§4で新規実装 |

> 雛形：長尺 Premium は `CarpenterPremium.tsx` / `RileyPremium.tsx` / `MadoffPremium.tsx` / `KeloPremium.tsx`。縦ショートも同思想で、ベースは仕様Aの `Short.tsx`、山場だけ§4の縦コンポを差す。
