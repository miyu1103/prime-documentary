### 素材の反復禁止（オーナー指示 2026-07-19・機械ゲート）

**「1動画に同じ素材はなるべく繰り返し使用しない」。** 判定は `python scripts/check_asset_reuse.py <film.json>`（`preflight_render_gate.py` に配線済み・レンダー前にブロック）。

| 種別 | 同一素材の使用上限 | 理由 |
|---|---|---|
| factoryクリップ | **1回**（再使用禁止） | `H:/pd-media/assets/factory` に11,623本ある。繰り返す理由が無い |
| i2v モーション | 2回 | 1本あたり24–73 GPU分と高コスト |
| SDXL静止画 | 2回 | 生成コストはあるが安い |

さらに全体条件: **カットの70%以上が「その素材の初出」であること**（first-use share ≥ 0.70）。

**実測した現状（2026-07-19・全13本がこの基準でFAIL）:** rodriguez は62枚を188カットに回して平均3.03回、williams は73素材で344カット＝平均4.71回、EP38は平均2.12回。連続分割はゼロ＝すべて「別の絵を挟んで同じ絵が戻ってくる」真の再登場であり、これが「AIスライドショー感」の正体。最良の rolin は factory 188本を全て1回使用でクリアしており、**この基準は達成可能**（rolin の唯一の違反は静止画の3回使用）。

**設計への含意:** カット数に対して素材点数を積む。12分＝約220カットなら、初出70%＝**約155点の異なる素材**が要る。内訳の確定値は **factory 90本（各1回）＋ 静止画 68枚（平均1.47回）＋ i2v 18本（各2回）= 226カット / distinct 176 / first-use 0.779**。

**注意（私の初期配分は誤りだった）:** 「各素材を上限いっぱいまで使う」設計は原理的に first-use share を下げる。share = distinct/cuts = 1/平均使用回数 なので、**0.70を満たすには平均使用回数を1.43回以下**に抑える必要がある。旧記述の「factory50 + 静止画50×2回 + i2v15×2回」は 180カット / distinct 115 / share **0.639 = FAIL**。上限は「そこまで使ってよい」ではなく「そこが限界」と読むこと。足りなければ factory を増やす（無料・在庫11,623本）のが最も安い解。



# EP40 — Lech v. Jackson — 制作設計書 ＋ Codex引き継ぎプロンプト（v001）

- Episode ID: `PD-2026-040-lech` / slug: `lech` / EP40
- 中心の問い（英語・二人称）: **"Can the police destroy your house and pay you nothing?"**
- 答え: **場合による。そして Lech 一家は、ほぼ何も受け取らなかった。**
- 判例: **Lech v. Jackson, 791 F. App'x 711 (10th Cir. 2019)**, cert. denied (2020)
- 背景ドクトリン: Takings Clause の **police power 例外** ／ 限定免責（Pierson v. Ray, 1967 / Harlow v. Fitzgerald, 1982）
- リスク階層: **R2**（実在私人が主役 = AI肖像禁止・匿名再現のみ）
- 尺: **11–12分**（目安 11.5–12.5分 = `check_final_acceptance.py` の standard band）
- 本書の Status: **BINDING**（EP40の制作契約）。上位正典は `docs/PD_ONE_PASS_PRODUCTION_SPEC.v2.md`（v2）と `docs/PD_WINNING_PATTERN.md`。衝突時は v2 のハードGATEが勝つ。

---

# 0. 【最重要】事実の取り扱い注意 — ACCURACY LOCK

> **この節に違反した成果物は、他が全て完璧でも出荷不可。**

## 0.1 絶対条件

**Lech v. Jackson は最高裁判決ではない。**

| 項目 | 正しい記述 | 禁止される記述 |
|---|---|---|
| 判断した裁判所 | 米国 **第10巡回区控訴裁判所**（United States Court of Appeals for the Tenth Circuit） | 「最高裁が」「the Supreme Court ruled」「the Supreme Court decided」「最高裁の答えは」 |
| 年 | **2019年**（控訴審判断） | 2020年を「判決の年」として書く |
| 最高裁の関与 | **2020年に上告を受理しなかった（cert. denied）だけ**。中身の判断はしていない | 「最高裁が支持した」「the Supreme Court upheld」「最高裁も同じ結論」 |
| 引用形式 | `791 F. App'x 711 (10th Cir. 2019)`（**F. App'x = 未公刊**） | `U.S.` レポーター、`S. Ct.` を付す |

**cert. denied の正しい説明（ナレーションでもこの意味を保て）:**
> "The Supreme Court declined to hear the case. That is not an endorsement — it simply means the Tenth Circuit's decision stands."

## 0.2 波及範囲（全成果物）

この制約は **タイトル・サムネ文字・フックナレ・本編ナレ・AEビートのラベル・字幕・YouTube概要欄・Shorts** の**すべて**に適用する。

## 0.3 機械ゲート `accuracy_lock`（Codex が実装する・BLOCKING）

`scripts/check_lech_accuracy.py` を新規実装し、以下を検査して exit != 0 で出荷を止める。

**検査対象ファイル:**
- `episodes/PD-2026-040-lech/03_script/lech_slots.v001.json`（全文字列フィールド）
- `episodes/PD-2026-040-lech/03_script/script.en.v*.md`
- `episodes/PD-2026-040-lech/08_edit/ae_hero/beats.json`（`top` / `bottom` / `caption`）
- `episodes/PD-2026-040-lech/09_package/*.json`（title / description / thumbnail headlines）

**ルールR1（ゾーン全面禁止）** — 次のフィールドに `supreme court` / `最高裁` が**部分一致でも1回でも**出たら FAIL:
`title_candidates[]`, `thumb_headlines[]`, `hook.lines[]`, `beats[].top`, `beats[].bottom`, `ed.cta_line`, `package.title`

```python
BANNED_ZONE = re.compile(r"supreme\s*court|最高裁|SCOTUS", re.IGNORECASE)
```

**ルールR2（本文の文脈限定）** — 本編ナレ本文で `Supreme Court` を含む**文**は、同一文内に次のいずれかを含まねばならない。含まなければ FAIL:

```python
ALLOWED_CONTEXT = re.compile(
    r"declined to hear|refused to hear|denied review|did not take the case|"
    r"cert(iorari)?\s+(was\s+)?denied|let the ruling stand|never ruled on",
    re.IGNORECASE)
```

**ルールR3（肯定的動詞の禁止）** — 本文全体で、`Supreme Court` の後 60文字以内に次が現れたら FAIL:

```python
BANNED_VERB = re.compile(r"\b(ruled|held|decided|upheld|affirmed|found|concluded)\b", re.IGNORECASE)
```

**ルールR4（引用形式）** — `script.en.v*.md` に判例引用が現れる場合、正規表現 `Lech v\. Jackson, 791 F\. App'x 711 \(10th Cir\. 2019\)` に完全一致する行が**最低1つ**存在すること。

**ルールR5（裁判所名の明示）** — 本編ナレ本文に `Tenth Circuit` が**最低2回**出現すること（1回目は幕3の導入、2回目は結論部）。

出力: `episodes/PD-2026-040-lech/09_package/accuracy_lock.v001.json`（`{"pass": bool, "violations": [...]}`）。
このJSONが `pass: true` でない限り、`check_final_acceptance.py` の実行に進んではならない。

## 0.4 数値・事実の検証ステータス（重要）

**本設計書は、いかなる具体的数値も「確定事実」として提示しない。**
下表は「台本工程（Claude）が検証すべき候補」であり、**検証前に台本・AEビート・サムネに書いてはならない**。

| ID | カテゴリ | 検証すべき内容 | 必要な典拠 | AEビート |
|---|---|---|---|---|
| F01 | 立てこもり時間 | 事件が始まってから終わるまでの時間（時間単位） | 一次報道 or 判決文の事実認定 | b02 |
| F02 | 万引きの被害額 | 逃走した男が店から取った物の価値（ドル） | 判決文 or 一次報道 | b03（左辺） |
| F03 | 家の損害額 | 破壊された住宅の損害/再建費用（ドル） | 一家の主張額と市の評価額を**区別して**記録 | b03（右辺）/ b05 |
| F04 | 市が支払った額 | Greenwood Village が一家に提示/支払った額（ドル） | 一次報道 or 判決文 | b06 |
| F05 | 補償率 | F04 ÷ F03 ×100（%）。**計算値であることを画面に明記** | 上2つから導出 | b07 |
| F06 | 破壊手段の回数 | 撃ち込まれたガス弾/爆発物/装甲車突入の回数 | 一次資料で数が確認できる場合のみ | b04 |
| F07 | 事件発生日 | 年月日 | 判決文 | b01 |
| F08 | 一家の中にいた人 | 家にいた人数と、無事に脱出したこと | 判決文 | 幕1ナレ |
| F09 | 上告不受理の年 | cert. denied の年 | 最高裁 order list | b08 |

**運用ルール:**
1. 各 F-ID は `episodes/PD-2026-040-lech/01_research/fact_recheck.v001.md` に「値・典拠URL・引用文・確度」の4点セットで記録する。
2. **典拠が取れなかった F-ID は、対応するAEビートを削除する**（`beats.json` から外す）。コンポジタは欠損ビートを SKIP するので作品は壊れない（§6.7）。
3. 「一家の主張額」と「公的に認定された額」は**別物**。混同したら R2 リスク（実在私人の名誉）。ナレでは必ず帰属する:
   - OK: "The family said rebuilding would cost about X."
   - NG: "The house was worth X."

---

# 1. なぜこの企画か（実測データに基づく根拠）

## 1.1 実測値（2026-07-18時点・`scripts/yt_studio_ctr.py` + Analytics API）

| 指標 | 実測 | 目標（v2 フロア/Good） | 差分 |
|---|---|---|---|
| CTR | **2.31%** | フロア 4% / Good 6% | **-1.69pt** |
| 本編 APV | **15–25%** | フロア 35% / Good 45% | **-10〜20pt** |
| 登録者 | **+2** | 転換 5/1000再生 | ほぼゼロ |
| コメント | **0** | ≥1本あたり数件 | 導線が存在しない |

## 1.2 勝っている型（`PD_WINNING_PATTERN.md` §3）

> **「◯◯は、あなたに △△ できるのか？」** = ①二人称 ②自分事の脅威 ③司法の線引き

## 1.3 語り口の選択（決定的）

| 型 | 実測 視聴維持率 | 例 |
|---|---|---|
| **判例解説型** | **1.6–7.5%** | Kelo / Mapp / Gideon |
| **一人の受難型** | **24–42%** | Rodriguez / Hinton / 没収 / Williams |

→ **EP40 は 100% 「一人の受難型」で書く。** 「Takings Clause とは何か」から始めたら負ける。
**「ある日、知らない男が自分の家に逃げ込んだ」から始める。**

## 1.4 EP40 の当事者性が最強である理由

過去の勝ち筋は「あなたのスマホ」「あなたの車」「あなたの現金」だった。EP40 は **「あなたの家」**。
持ち家・賃貸を問わず、視聴者全員が「自分の生活の器」を持っている。しかも本件の一家は**何もしていない**。
落ち度がゼロの被害者 = 視聴者は自己弁護のしようがなく、**怒りが最大化する**。
→ **コメント0からの脱出を、この怒りで狙う**（§9 のED導線）。

---

# 2. 視覚・音響レーンの分離（EP39 frazier との衝突回避）

> **EP39 のファイルには一切触らない。** レーンは以下で機械的に分離する。

| 軸 | **EP39 frazier** | **EP40 lech** |
|---|---|---|
| 舞台 | 取調室 / 密室 | **郊外の一軒家 / 屋外の広がり** |
| 時間帯 | **夜** | **昼（真昼〜夕方）** |
| 支配的な出来事 | 心理的圧迫・言葉 | **物理的破壊** |
| アクセント色 | electric `#1F6BFF`（冷・EP39専用） | **gold/amber `#E5B53A`（暖・EP40専用）** |
| ベース色 | 深い navy / 黒 | **褪せた昼光の白 + コンクリート灰 + 木の裂けたタン + 埃のアンバー** |
| 影の色 | 青寄りの黒 | **わずかに緑がかった灰（屋外の日陰）** |
| コントラスト方針 | 低照度・高コントラストの点光源 | **高輝度・広い明部・粉塵で拡散した光** |
| レンズ感 | 望遠・浅い被写界深度・圧縮 | **広角気味・引き・空間の広さと"失われた体積"** |
| 音の設計 | 時計の秒針 / 空調のハム / 近接リバーブ | **低いサブ帯のインパクト / 木材の裂け / 瓦礫 / 風 / 遠くのサイレン / 屋外の広いリバーブ** |
| 楽器 | （EP39側で定義） | **ソロピアノ（疎・単音）＋低弦のサステイン＋金属的パーカッション** |
| 画像保存先 | （EP39側） | `H:\pd-media\assets\ai\lech\` |
| Remotion データ | （EP39側） | `remotion/src/data/lech_film.json` |
| Remotion コンポ | （EP39側） | `Ep40Lech` |
| AE 作業ディレクトリ | （EP39側） | `episodes/PD-2026-040-lech/08_edit/ae_hero/` |

**素材被り禁止（v2 row7 `footage_diversity`）:** EP39 と同一の factory clip / AI画像を**1点も**使わない。
Codex は生成前に `episodes/PD-2026-039-*/05_stock/stock_ledger*.json` を読み、sha256 の重複を除外すること。

---

# 3. 構成（11–12分）— EP37テンプレ準拠 + 受難型への改造

## 3.1 タイムライン全体

**★この表は 2,140語 / 178.1 wpm で組み直したもの。旧版（〜11:30終わり）は語数不足なので使うな。**

| # | ブロック | 語数 | VO秒 | 開始–終了（秒） | 役割 | v2 row |
|---|---|---|---|---|---|---|
| 0 | **HOOK** | **24** | 8.1 | 0.0 – 8.1 | 本編の最強カット3–4個 + フックナレ + 語同期字幕 | row 9 |
| 1 | **OPENING** | 0 | — | 8.1 – 11.6 | `BrandOpening`（`OPENING_SEC = 3.5`・**非VO**） | row 14 |
| 2 | **幕1 ふつうの家** | **350** | 117.9 | 11.6 – 131.5 | 家族・家・日常。**視聴者に「自分の家」を重ねさせる**（+2.0s 余韻） | row 15/16 |
| 3 | **幕2 侵入と包囲** | **505** | 170.1 | 131.5 – 303.6 | 万引き犯が逃げ込む → 包囲 → 立てこもり（+2.0s 余韻） | row 16 |
| 4 | **幕3 破壊** | **510** | 171.8 | 303.6 – 477.4 | 装甲車・爆薬・穴。**本編のクライマックス**（+2.0s 余韻） | row 8 |
| 5 | **幕4 誰も払わない** | **575** | 193.7 | 477.4 – 673.1 | 瓦礫の中の一家 → 市の回答 → 第10巡回区 → 上告不受理（+2.0s 余韻） | row 16 |
| 6 | **ENDING** | **176** | 59.3 | 673.1 – 732.4 | 感情のペイオフ → earned CTA → **問いかけ** | row 10 |
| 7 | **ENDCARD** | 0 | — | 732.4 – 741.4 | `BrandEndcard`（`ENDCARD_SEC = 9`・**非VO**） | row 14 |

### 検算（Codex は必ず自分で再計算して一致を確認すること）

```
[1] 語数の合計
    24 + 350 + 505 + 510 + 575 + 176 = 2,140 語        ✓ 目標2,140と一致（band 2,048–2,226内）

[2] VO秒（各ブロック = words / 178.1 × 60）
    HOOK  24 /178.1×60 =   8.1 s
    幕1  350 /178.1×60 = 117.9 s
    幕2  505 /178.1×60 = 170.1 s
    幕3  510 /178.1×60 = 171.8 s
    幕4  575 /178.1×60 = 193.7 s
    ED   176 /178.1×60 =  59.3 s
    VO合計                720.9 s      ✓ = 2,140/178.1×60 = 720.9 と一致

[3] 総尺
    VO 720.9
  + OPENING 3.5 + ENDCARD 9.0        （Bookends・非VO） = 12.5
  + 幕間の余韻 2.0 × 4               （リビール後の間・§3.3） =  8.0
  ------------------------------------------------------------
    合計 741.4 秒 = 12:21             ✓ band 690–750秒 の内側（上限まで 8.6秒）
```

> **band上限までの余裕は 8.6秒しかない。** これは意図的（尺不足が本チャンネル最大の反復失敗）。
> ただし**語数を 2,226 を超えて増やすと band を突き抜ける**。増量したくなったら幕間の余韻を削るのではなく、
> `check_script_length.py` を再実行して band 内に収まることを確認してから増やすこと。

**`lech_film.json` に入る値（`caseFilmDurationInFrames` の計算に直結）:**
```
hookSeconds       =   8.1
OPENING_SEC       =   3.5   （Bookends 定数・変更しない）
narrationSeconds  = 720.8   （= 幕1〜ED の VO 712.8 + 幕間の余韻 8.0）
ENDCARD_SEC       =   9.0   （Bookends 定数・変更しない）
------------------------------------------------------
合計                741.4 秒
```

**尺の算数 ★2026-07-19 実測にもとづき改訂（旧値 173wpm / 1,850–1,950語 は使うな）:**

旧記述は尺不足を再発させる。2026-07-19に **31話分の実TTS音声**（`H:\pd-media\episodes\*\06_voice\draft\VC-*.mp3` の実時間合計）と台本語数を突き合わせて実測した結果:

> **ナレーション速度の実測中央値 = 178.1 wpm**（範囲 163.7–237.4）

- 目標総尺 11.5–12.5分（690–750秒）→ HOOK 8s + OPENING 3.5s + ENDCARD 9s = 20.5s
- **確定: 目標語数 2,140語 / 許容band 2,048 – 2,226語**（これを `lech_slots.v001.json` の契約に入れる）
- 判定は **`python scripts/check_script_length.py <script>` が唯一の正**。「だいたい12分ぶん書けた」という自己申告は禁止。このゲートは `preflight_render_gate.py` の最初のチェックとして配線済みで、**ElevenLabsのTTSとレンダーに課金する前にブロック**する。
- ゲートは総尺を丸ごとナレ時間として計算するため、実測の非ナレ余剰（約20秒 / EP38: VO 543.5s → 完成 563.9s）のぶん **約60語ぶん厳しめ**に出る。尺不足が本チャンネル最大の反復失敗である以上、長い側に倒すのは意図的。

**根拠**: 過去38話中**30話**が宣言した目標尺に未達。EP009–015は1,503–1,565語で8.4–8.8分、EP38は1,675語で**9.4分**（ゲート予測9.4分と完成尺9.40分が一致）。1,850–1,950語で書くと**約10.5分**で終わり、また band を外す。

**水増し禁止**: 言い換え反復・冗長な接続・無意味な間で語数を稼ぐと `check_padding` でFAILする。増やすのは中身だけ — 破壊の場面のディテール、市の回答の逐語、第10巡回区の論理と反対の論理、一家のその後、限定免責が生まれた経緯、数字の出所。

## 3.2 リテンション設計（v2 row16）— 再フックの位置を確定

**コールドオープンの未解決の問い（0:08 で開き、11:20 まで閉じない）:**
> "Who pays for a house the police destroyed?"

**再フック（★新タイムライン 12:21 に合わせて再配置。間隔はすべて3分未満）:**

| 時刻 | 秒 | 再フックの機能 | 内容の型 |
|---|---|---|---|
| 2:12 | 132 | 状況の反転 | 「この家に、この家族とは何の関係もない男が入った」 |
| 4:05 | 245 | 規模の跳ね上がり | 「警察が持ち出したのは、拳銃ではなかった」 |
| 6:45 | 405 | 予想の裏切り | 「そして家は、事件が終わったあとに壊された部分がある」 |
| 7:57 | 477 | 制度の壁 | 「市の回答は、一行だった」 |
| 9:45 | 585 | **最大の転回** | 「法律上、これは"収用"ではない。だから、払われない」 |

**間隔の検算:** 0:00→2:12（2:12）/ →4:05（1:53）/ →6:45（2:40）/ →7:57（1:12）/ →9:45（1:48）/ →12:21（2:36）
→ **最大間隔 2:40 < 3:00** ✓（v2 row16「2〜3分ごとに再フック」を満たす）

**開いたまま持ち越すオープンループ（3本）:**
1. L1「一家はいくら受け取ったのか」→ **10:05（605s）で開示**（AEビート **b06** と同期）
2. L2「なぜ壊す必要があったのか」→ **8:40（520s）で開示**（police power の説明）
3. L3「この判断は最終なのか」→ **10:55（655s）で開示**（第10巡回区 + cert. denied ／ AEビート **b08** と同期）

## 3.3 幕間の余韻（8.0秒の内訳・水増しではない）

§3.1 の総尺計算に入っている「余韻 2.0秒 × 4」は、**リビール直後に画と音だけで持たせる意図的な間**。
無音ではなく、BGM と環境音は鳴り続ける（`bgm_present` の 25秒無音ルールに抵触しない）。

| 位置 | 秒 | 内容 |
|---|---|---|
| 幕1 → 幕2 | 2.0 | 平穏な家の最後のカット。次の破局の前の静けさ |
| 幕2 → 幕3 | 2.0 | 装甲車が据えられた画。破壊が始まる直前 |
| 幕3 → 幕4 | 2.0 | 崩れた家の全景。事件が終わった後の静止 |
| 幕4 → ED | 2.0 | 空き地の画。判決の重みを置く間 |

> **`check_padding.py` の DEAD AIR 検出との関係:** この4箇所はすべて**セクション境界**（幕の変わり目）に置く。
> `check_padding` はセクション境界の間（BEAT_MAX まで）を「良いペーシング」として許容し、
> **セクション内部**の長い間だけを水増しとして罰する。**幕の途中に2秒の間を作ってはならない。**

**「20秒以上の平坦な説明区間」を作らない。** ドクトリン説明（police power / 限定免責）は**一箇所にまとめず**、幕4に3分割して差し込む。

---

# 4. 台本スロット契約（台本は別プロセス・ここは機械契約）

> 台本本文は別プロセスで制作中。**Codex は台本本文を待たずに、以下の契約を満たす空スロットで全パイプラインを組み上げる。**
> 台本が確定したら、**`lech_slots.v001.json` を1個埋めるだけ**で全工程が通る状態にしておくこと。

## 4.1 契約ファイル

**パス:** `episodes/PD-2026-040-lech/03_script/lech_slots.v001.json`
**スキーマ版:** `lech_slots.v1`
**このファイルの生成者:** Claude（台本工程）
**このファイルの消費者:** `build_lech_film_data.py`（Remotion用 `lech_film.json` を生成）、`build_lech_hero_jsx.py`（AEビート）、`build_lech_thumbnails.py`、`check_lech_accuracy.py`

## 4.2 スキーマ（厳密）

```jsonc
{
  "schema_version": "lech_slots.v1",          // 固定文字列。異なれば全ツールが exit 2
  "episode_id": "PD-2026-040-lech",           // 固定文字列
  "slug": "lech",                             // 固定文字列

  "accuracy_lock": {                          // §0。全フィールド必須・固定値
    "court": "United States Court of Appeals for the Tenth Circuit",
    "court_short": "Tenth Circuit",
    "decision_year": 2019,
    "citation": "Lech v. Jackson, 791 F. App'x 711 (10th Cir. 2019)",
    "cert_denied_year": 2020,
    "is_supreme_court_decision": false        // 必ず false。true なら即 FAIL
  },

  "title_candidates": [                       // 長さ = ちょうど 2（v2 row13 A/Bテスト）
    { "text": "string",                       // 1..60 文字。二人称必須（"you"/"your" を含む）
      "variant": "A" }                        // "A" | "B"
  ],

  "thumb_headlines": [                        // 長さ = ちょうど 3（§8のサムネ3案に1:1対応）
    { "concept_id": "T1",                     // "T1" | "T2" | "T3"
      "text": "string" }                      // 全て大文字。単語数 1..4。禁止語チェック対象
  ],

  "hook": {                                   // 0:00–0:08
    "seconds": 8.0,                           // 6.0 <= x <= 10.0
    "lines": ["string"],                      // 長さ 2..4。合計語数 23..31（8秒 @178.1wpm・実測）
    "source_cut_ids": ["string"]              // 長さ 3..4。本編 cuts[].id を参照（新規制作禁止）
  },

  "acts": [                                   // 長さ = ちょうど 4
    { "act": 1,                               // 1..4
      "title_ja": "string",                   // 内部管理用（画面に出さない）
      "start_sec": 0.0,                       // ナレ開始からの秒（単調増加・重複不可）
      "narration": "string",                  // 幕のナレ本文（英語・改行なし1文字列）
      "rehook_sec": [0.0],                    // その幕に含まれる再フックの絶対秒。1..2 個
      "open_loop_close": ["L1"]               // この幕で閉じるループID（"L1"|"L2"|"L3"）。0..3個
    }
  ],

  "narration_total_words": 2140,              // ★確定: 2048 <= x <= 2226。目標2140（§3.1）
                                              // hook.lines + acts[].narration + ed の全語数の合計
  "wpm_assumed": 178.1,                       // 固定 178.1。他の値なら validate_lech_slots.py が exit 1
  "act_word_targets": [350, 505, 510, 575],   // 幕1..幕4。各 ±8% まで許容。合計は上の総語数と整合必須
  "ed_word_target": 176,                      // ED（payoff+cta+question+next_hook の合計）。±8%

  "beats": [                                  // §6。長さ 6..8。詳細は §6.3 のビート契約
    { /* BeatSlot — §6.3 参照 */ }
  ],

  "ed": {
    "payoff_line": "string",                  // 感情のペイオフ1文。1..180文字
    "cta_line": "string",                     // earned CTA。1..140文字。§9.2の文言を使う
    "question_line": "string",                // コメント誘導の問い。1..120文字。必ず "?" で終わる
    "next_hook": "string"                     // 次回引き。1..120文字
  },

  "facts": {                                  // §0.4 の F-ID → 検証結果
    "F01": { "value": 0, "unit": "hours", "verified": false, "source_url": "", "quote": "" }
    // F01..F09 すべてのキーが存在すること。verified:false のものは beats から自動除外される
  }
}
```

## 4.3 バリデータ（Codex が実装・BLOCKING）

`scripts/validate_lech_slots.py` を実装する。上記の型・長さ・範囲・単調増加をすべて検査し、
違反を `{"field": "...", "rule": "...", "actual": "..."}` の配列で出力し exit 1。
加えて次の**2つの既存ゲートを内部から呼び**、すべて pass で exit 0:

| 呼ぶゲート | コマンド | 落ちる条件 |
|---|---|---|
| **語数** | `scripts/check_script_length.py <script> --json` | 総語数が **2,048–2,226** の外（`wpm_assumed = 178.1` は同スクリプトの `WPM_MEDIAN` と一致） |
| **事実性** | `scripts/check_lech_accuracy.py --json` | §0.3 の R1–R5 に違反 |

**加えて `validate_lech_slots.py` 自身が検査すること:**
- `narration_total_words` が `hook.lines` + `acts[].narration` + `ed.*` の**実測語数の合計と一致**する
  （宣言値と実文の乖離を許さない。宣言だけ2,140にして中身が1,700語、を防ぐ）
- `wpm_assumed == 178.1`
- `sum(act_word_targets) + ed_word_target + hook語数 == narration_total_words`
- 各幕の実語数が `act_word_targets` の **±8%** 以内

> **`check_script_length.py` の判定が唯一の正。** 「だいたい12分ぶん書けた」という体感・自己申告は禁止。
> このゲートは `preflight_render_gate.py` の最初のチェックとして配線済みで、
> **ElevenLabs の TTS とレンダーに課金する前にブロックする。**

## 4.4 台本未確定時の動作（重要 — Codexはこれで着手できる）

**`lech_slots.v001.json` が存在しない、または `verified: false` が多数の場合でも、Codex は止まらない。**

1. `scripts/make_lech_slots_stub.py` を実装し、**契約と同じ形の stub** を生成する。
   - 文字列フィールドは `"[[SLOT:hook.lines[0]]]"` のようなマーカー文字列
   - 数値は範囲の中央値
   - `facts.*.verified` は全て `false`
2. stub でパイプライン全体（Remotion レンダ → AE ビート → コンポジット）を**通しで1回走らせ、動くことを実証する**（ドライラン）。
3. ドライランの出力は `episodes/PD-2026-040-lech/08_edit/_dryrun/` 配下に置き、**本番ファイル名を使わない**。
4. 台本確定後は `lech_slots.v001.json` を差し替えて同じコマンドを再実行するだけ。
   **stub と本番でコードパスが分岐してはならない**（分岐したらドライランの意味がない）。

---

# 5. ビジュアル — 画像プロンプト群

## 5.1 素材の積算（★2,140語＝12:21 前提で再計算。1,675語前提の数字は使うな）

> 台本語数が従来比 約1.3倍になったため、**必要な素材点数も2〜3割増える。**
> 下表は EP38 の実績を 741.4秒 にスケールしたもの。

### 5.1.1 EP38 実績 → EP40 目標

| 素材 | EP38 実績（563.9秒） | 秒あたり | **EP40 目標（741.4秒）** | ゲート下限 |
|---|---|---|---|---|
| 静止画（**cut内で使う distinct 枚数**） | 40 | 0.0709 | **53** → 安全側に **60** | 静止画占有率 ≤45% |
| i2v（AI動画クリップ） | 12 | 0.0213 | **16** | — |
| factory 実写クリップ | 41 | 0.0727 | **54** | **≥25本**（30秒に1本 = 741.4/30 = 24.7） |
| **総カット数** | 172 | 0.3050 | **226** | 平均ショット長 ≤6秒 |
| **MGビート** | 27 | 0.0479 | **36** | **≥2.5/分** かつ **種類3以上** |

### 5.1.2 カット内訳と検算

```
総カット 226 = factory 54 + i2v 16 + 静止画カット 156

[1] 平均ショット長
    絵が必要な区間 = 741.4 − OPENING 3.5 − ENDCARD 9.0 = 728.9 秒
    728.9 / 226 = 3.23 秒/カット           ✓ ≤6秒（v2 row8）

[2] 静止画占有率（≤45%）
    静止画カット 156本 × 平均 2.05秒 = 319.8 秒
    319.8 / 741.4 = 43.1%                  ✓ ≤45%（目標42–43%で設計）
    → 動画（factory+i2v）が 728.9 − 319.8 = 409.1 秒を担当
    → 70カットで 409.1秒 = 平均 5.84秒/カット  ✓ ≤6秒

[3] footage_diversity（distinct/total ≥0.40・単一クリップ再利用 ≤4回）
    distinct = 静止画60 + i2v16 + factory54 = 130
    130 / 226 = 0.575                      ✓ ≥0.40
    静止画の再利用率 = 156カット / 120枚 = 1.3回  OK (check_asset_reuse 上限2.0回)
    ※旧記述「60枚 = 2.6回 ✓ ≤4回」は check_asset_reuse の上限2回を超過しFAIL。上の是正節が優先。

[4] MGビート密度（≥2.5/分・種類3以上）
    741.4秒 = 12.36分 → 下限 12.36 × 2.5 = 30.9 → ≥31ビート
    設計値 36 = AEヒーロービート 8（§6）+ Remotion FigureBeats 28（§6.10）
    36 / 12.36 = 2.91 /分                  ✓ ≥2.5
    種類 = AE側4レイアウト + Remotion側7種 = 11種  ✓ ≥3

[5] factory 下限
    54本 ≥ 25本                            ✓
    741.4 / 54 = 13.7秒に1本（下限は30秒に1本）

[6] 5秒超の長止め ≤8箇所
    設計上ゼロを狙う。全静止画に Ken Burns ≥6% ズームまたはパララックスを付ける（v2 row8）
```

### 5.1.3 生成プールと使用枚数の区別（重要）

- **生成プール = 132枚**（22シーン × 6バリエーション）
- **本編で実際に使う distinct 静止画 = 60枚以上**（プールから選抜。残りはサムネ/Shorts/差し替え用）
- プールを使用枚数より多く作る理由: 構図違いの中から**意味の合うもの**を選ぶため（§5.7）。
  枚数ぴったりに生成すると「合わない画を仕方なく使う」＝紙芝居の原因になる。

**Codexへの指示:** 各プロンプトを **構図 / カメラ角度 / 寄り引き / 光の向き / 被写体位置 を変えて6枚ずつ**出力。
`<SPN-ID>.png`, `<SPN-ID>_02.png` … `<SPN-ID>_06.png` と連番保存。

## 5.2 保存先とレジャー

- 保存: `H:\pd-media\assets\ai\lech\<SPN-ID>.png`（`import_to_remotion.py` が取り込む）
- 各画像 1行を `episodes/PD-2026-040-lech/05_stock/stock_ledger.v001.json` に記録
  （`source=ai_codex` / `commercial_use=allowed` / `sha256`）
- 解像度: **長辺 3840px 以上**（v2 row5 `image_resolution` ゲート）

## 5.3 共通スタイル接尾（各プロンプト末尾に必ず付ける）

```
, cinematic still, harsh midday sunlight and airborne dust, wide-angle sense of open suburban space, bleached daylight whites with concrete grey, splintered pale wood and warm amber dust motes, faintly green-grey outdoor shadows, deep shadow detail retained, shallow-to-medium depth of field, ultra-detailed, photoreal, 4K, 16:9, fine film grain, no text, no watermark, no logo
```

> **EP39 との分離:** 上記接尾には `navy`, `electric blue`, `night`, `interrogation`, `low-key` を**一切含めない**。EP39 のプロンプト接尾と1語も共有しないこと。

## 5.4 共通ネガティブ（各プロンプトに必ず付ける）

```
text, words, letters, numbers, captions, watermark, logo, street address, house number, license plate, real celebrity, recognizable real person, identifiable face, portrait, mugshot, cartoon, illustration, low quality, blurry, deformed, extra limbs, gore, blood, corpse, night scene, dark navy interior, interrogation room
```

## 5.5 R2 安全ルール（絶対）

1. **実在の Lech 一家・逃走した男・個々の警察官の肖像は作らない。** 人物は必ず後ろ姿・シルエット・顔の外れた構図・手元のみ。
2. **実在の住所を再現しない。** 番地・表札・道路標識・郵便受けの文字は生成しない（ネガティブに `street address`, `house number` を入れている理由）。
3. **読める公文書・判決文を作らない。** 書類は雰囲気のみ（文字は判読不能）。
4. **流血・遺体・生々しい暴力を描かない。** 破壊は**建物に対してのみ**描く。
5. AI画像は概要欄で **AI生成であることを開示**する。

## 5.6 シーンプロンプト（S01–S22）

**S01 — ふつうの郊外の家（幕1の基調）**
An ordinary two-story American suburban house on a quiet residential street in warm late-morning light, neat lawn, a basketball hoop over the garage, a bicycle lying on its side, utterly peaceful and lived-in, no people, generic architecture with no visible address + [共通スタイル]

**S02 — 家の中の生活の痕跡**
Interior of a lived-in family home in soft daylight through a window, a kitchen table with an unfinished breakfast, a child's drawing taped to the fridge, worn furniture, a sense of ordinary life interrupted mid-moment, no people, no readable text + [共通スタイル]

**S03 — 平穏な午後の通り**
A wide empty suburban street at midday, long clean sidewalks, parked cars, heat shimmer on the asphalt, an american flag hanging still, deep quiet before something happens, no people + [共通スタイル]

**S04 — 走って逃げる匿名の人影**
A distant anonymous figure in a hooded jacket running across a sunlit suburban lawn, seen from far behind, motion blur on the figure, faceless and unidentifiable, sense of sudden intrusion into calm + [共通スタイル]

**S05 — 破られた裏口**
A residential back door standing open with the frame splintered near the lock, bright daylight flooding into a dim interior, a single overturned potted plant, tension of a violated threshold, no people + [共通スタイル]

**S06 — 最初のパトカー**
A single police cruiser stopped at an angle across a suburban street in flat midday sun, its lights on but pale against the daylight, doors open, empty of people, the beginning of an escalation + [共通スタイル]

**S07 — 包囲が広がる**
A wide high-angle view of a suburban block with many police vehicles converging from several directions, yellow tape stretched across lawns, neighbors' houses looking on, small human silhouettes at a distance, faces unreadable + [共通スタイル]

**S08 — 装甲車の到着**
A heavy armored police vehicle parked on a residential lawn under a bright afternoon sky, its bulk absurdly out of scale against a family house and a mailbox, dust hanging in the air, no people visible + [共通スタイル]

**S09 — 待つ時間（長時間の経過）**
A suburban street at the golden hour of a long day, long stretched shadows from parked emergency vehicles, an abandoned coffee cup on a car hood, the exhaustion of many hours passing, no people + [共通スタイル]

**S10 — 破壊の瞬間（壁）**
An exterior house wall being torn open, splintered timber and drywall bursting outward in a cloud of pale dust, harsh sunlight cutting through the new opening, violent and structural, no people, no blood + [共通スタイル]

**S11 — 屋根の穴**
A residential roof with a large ragged hole punched through it, shingles scattered across the lawn, bright sky visible through the breach, seen from a slight low angle, no people + [共通スタイル]

**S12 — 粉塵と光**
A dense cloud of pale construction dust hanging in a shaft of hard sunlight inside a wrecked room, particles suspended and glowing amber, abstract and beautiful and terrible, no people + [共通スタイル]

**S13 — 家の中から見た外**
Interior view from inside a destroyed living room looking out through a wall that is no longer there, blinding daylight where the wall used to be, a sofa covered in debris, devastating and quiet, no people + [共通スタイル]

**S14 — 崩れた家の全景**
Wide establishing shot of a suburban house reduced to a partially collapsed shell in flat afternoon light, walls open to the air, the neighboring houses untouched and pristine on both sides, brutal contrast, no people + [共通スタイル]

**S15 — 瓦礫の中の私物**
Close-up of ordinary personal belongings half-buried in household debris — a framed photograph face-down, a shoe, a coffee mug, a child's toy — covered in white dust, sunlight raking across, deeply human, no faces, no readable text + [共通スタイル]

**S16 — 立ち尽くす家族（匿名）**
Two adult silhouettes standing at a distance with their backs to camera, looking at a wrecked house across a lawn in late-afternoon light, small against the damage, entirely unidentifiable, no faces + [共通スタイル]

**S17 — 重機と解体**
A yellow excavator arm poised over the remains of a suburban house against a wide pale sky, the finality of demolition, dust and shadow, no people + [共通スタイル]

**S18 — 空き地**
An empty flat lot of bare dirt between two intact suburban houses under a wide bright sky, a concrete foundation outline still visible, the absence where a home was, no people + [共通スタイル]

**S19 — 市庁舎（制度の側）**
A modest American municipal building exterior in flat daylight, clean symmetrical facade, an empty flagpole shadow across the steps, institutional and impersonal, no people, no readable signage + [共通スタイル]

**S20 — 控訴裁判所（第10巡回区）**
A stone federal appellate courthouse facade in strong afternoon sun, tall columns casting hard shadows, monumental and unmoved, seen from a low angle, no people, no readable inscriptions + [共通スタイル]

**S21 — 法の線（テーマの象徴）**
A stark line of bright sunlight falling across a bare concrete floor, a single small pile of household rubble on one side and clean empty floor on the other, minimal and symbolic of a legal boundary, no people + [共通スタイル]

**S22 — ED / 余韻**
A new house frame of raw timber standing on an empty lot in warm low evening sun, unfinished and skeletal against a wide sky, quiet and open-ended, hopeful and unresolved, no people + [共通スタイル]

*(S01–S22 を各6枚 = 132枚)*

## 5.7 ナレとの意味一致（binding・EP37から継承）

**汎用B-rollの流し込みは禁止。** `04_scenes/scene_plan.v001.json` で 1ビート（1文）ごとに次を必ず埋める:
`visual_question / visual_verb / start_state / end_state / eye_target / sync_words / source_type / truth_status`

**語同期の決め所（faster-whisper の語タイムに合わせる）:**
`"your house"` / `"nothing"` / `"nineteen hours"`（F01確定後）/ `"police power"` / `"the Tenth Circuit"` / `"declined to hear"` / `"zero"`
→ その語が発せられた**そのフレーム**で対応するリビールが出る。

---

# 6. After Effects ヒーロービート設計（今回の主要要求）

## 6.1 パイプラインの原則（EP38で measured 済み・2026-07-18）

```
[1] Remotion で本編を完成 → lech_final_bgm.v002.mp4（音声ミックス済み）
[2] build_lech_hero_jsx.py（Python）が beats.json と lech_hero.jsx を生成
[3] AfterFX -noui -r lech_hero.jsx  →  各ビートを 1920x1080@30fps の不透明 mp4 で書き出し
[4] composite_lech_hero.py が ffmpeg overlay + enable='between(t,start,end)' で焼き込み
[5] 出力 → lech_final_bgm.v003_ae.mp4（v002 は絶対に上書きしない）
```

**なぜこの形か:** Remotion を再レンダリングしない。AEビートは元の図版を**完全置換**するので二重描画がない。音声は `-c:a copy` で無傷。

## 6.2 スロット設計（**8スロット**・うち必須6・条件付き2）

**★挿入位置は §3.1 の新タイムライン（総尺 741.4秒）に合わせて確定済み。**

| ID | 見せる数値カテゴリ | F-ID | レイアウト | カウント型 | 区間長 | **start–end（秒）** | 位置 | 必須 |
|---|---|---|---|---|---|---|---|---|
| **b01** | 事件が起きた年 | F07 | **C: DATE_STAMP** | CT_DATE | 5.0s | **136.0 – 141.0** | 幕2冒頭 2:16 | 必須 |
| **b02** | 立てこもり時間（時間） | F01 | **A: CENTER_STACK** | CT_INT | 6.0s | **252.0 – 258.0** | 幕2後半 4:12 | 必須 |
| **b03** | 万引きの被害額 **vs** 家の損害額 | F02+F03 | **B: SPLIT_COMPARE** | CT_MONEY×2 | 7.0s | **312.0 – 319.0** | 幕3冒頭 5:12 | 必須 |
| **b04** | 破壊手段の回数（ガス弾/爆発物/突入） | F06 | **A: CENTER_STACK** | CT_INT | 5.5s | **412.0 – 417.5** | 幕3中盤 6:52 | **条件付き**（F06 verified 時のみ） |
| **b05** | 家の損害額（単独・大きく） | F03 | **A: CENTER_STACK** | CT_MONEY | 6.0s | **492.0 – 498.0** | 幕4冒頭 8:12 | 必須 |
| **b06** | 一家が受け取った額 | F04 | **A: CENTER_STACK** | **CT_COUNTDOWN** | 6.5s | **605.0 – 611.5** | 幕4 10:05（**L1 のペイオフ**） | 必須 |
| **b07** | 補償率（計算値・%） | F05 | **D: RATIO_BAR** | CT_PCT | 6.0s | **620.0 – 626.0** | 幕4 10:20 | **条件付き**（F03とF04が両方 verified） |
| **b08** | 判断した裁判所と年（+ 上告不受理） | F09 | **C: DATE_STAMP** | CT_DATE | 6.0s | **655.0 – 661.0** | 幕4末 10:55（**L3 のペイオフ**） | 必須 |

**検算:**
```
[1] 区間の重なりなし・昇順
    136.0<141.0 < 252.0<258.0 < 312.0<319.0 < 412.0<417.5
  < 492.0<498.0 < 605.0<611.5 < 620.0<626.0 < 655.0<661.0     ✓ 単調増加・重複ゼロ

[2] 全区間がナレ区間の内側（HOOK 0–8.1 と ENDCARD 732.4–741.4 に重ねない）
    最小 136.0 > 11.6（幕1開始）  ✓
    最大 661.0 < 673.1（ED開始）   ✓ ED のペイオフに図版をかぶせない

[3] b06 と b07 の間隔 = 620.0 − 611.5 = 8.5秒 ✓（連続したデータカードにならない）

[4] 合計 48.0秒 / 741.4秒 = 6.5%    ✓ 図版として過剰でない密度
```

## 6.3 ビート契約（`beats.json` のスキーマ — 台本確定後に埋まる）

**パス:** `episodes/PD-2026-040-lech/08_edit/ae_hero/beats.json`
**生成者:** `scripts/ae/build_lech_hero_jsx.py`
**消費者:** `lech_hero.jsx`（AE）と `scripts/ae/composite_lech_hero.py`

```jsonc
{
  "schema_version": "lech_beats.v1",
  "episode_id": "PD-2026-040-lech",
  "fps": 30,                                  // 固定 30。本編 mp4 と一致必須
  "width": 1920, "height": 1080,              // 固定
  "beats": [
    {
      "id": "b01",                            // ^b0[1-8]$
      "layout": "CENTER_STACK",               // "CENTER_STACK"|"SPLIT_COMPARE"|"DATE_STAMP"|"RATIO_BAR"
      "count_type": "CT_INT",                 // §6.5 の型ID
      "fact_id": "F07",                       // §0.4 の F-ID。facts[F-ID].verified が false ならこのビートを出力しない
      "required": true,                       // false のビートは verified でなければ静かに省略

      "start": 125.400,                       // 本編mp4 上の絶対秒。小数第3位まで。単調増加・重複禁止
      "end": 130.400,                         // start < end。end-start は §6.2 の区間長 ±0.2s 以内
      "dur": 5.000,                           // = round(end-start, 3)

      "still": "H:/pd-media/assets/ai/lech/S03_04.png",  // 絶対パス・スラッシュ区切り。存在必須
                                                          // 本編の同区間で使っている画像と重複しないこと

      "top": "GREENWOOD VILLAGE",             // 上ラベル。全て大写文字。1..24文字。§0.3 R1 の検査対象
      "bottom": "AN ORDINARY TUESDAY",        // 下ラベル。全て大文字。1..28文字。§0.3 R1 の検査対象
      "caption": "string",                    // ナレ字幕1行。**改行を含めないこと**（AE制約）。最大50文字

      "value": 2015,                          // 主数値。CT_DATE は年、CT_MONEY はドル、CT_PCT は%
      "value_b": null,                        // SPLIT_COMPARE のときのみ数値。それ以外は null
      "decimals": 0,                          // 0..2
      "thousands": true,                      // 3桁区切りの有無。CT_DATE のときは必ず false
      "prefix": "",                            // "" | "$"
      "suffix": "",                            // "" | "%" | " HOURS" | " ROUNDS" | "M"

      "label_a": null,                        // SPLIT_COMPARE 左辺のラベル。それ以外は null。1..20文字
      "label_b": null,                        // SPLIT_COMPARE 右辺のラベル。それ以外は null。1..20文字
      "ratio_note": null,                     // RATIO_BAR のときのみ。例 "CALCULATED FROM THE TWO FIGURES ABOVE"

      "numKeys": [[0.55, "0"], [0.61, "312"]],// Python で全事前計算した (時刻, 表示文字列) のホールドキー
                                              // JS 側で数値整形を一切しないこと（EP38の確定ルール）
      "numKeys_b": null,                      // SPLIT_COMPARE のときのみ配列。それ以外は null
      "numReveal": 0.45,                      // 数値レイヤーの不透明度が立ち上がる時刻
      "head": 0.1333,                         // = 4/30。頭の黒シーム
      "tail": 0.1333,                         // = 4/30。尻の黒シーム
      "out": "C:/.../08_edit/ae_hero/render/b01.mp4"
    }
  ]
}
```

**契約の不変条件（`validate_lech_beats.py` が検査・BLOCKING）:**
1. `beats[].start` は昇順で、区間同士が**重ならない**
2. すべての `start`/`end` が本編ナレーション区間内（HOOK と ENDCARD には**絶対に重ねない**）
3. `end <= narrationSeconds + hookSeconds + OPENING_SEC`
4. `still` が実在し、長辺 ≥ 3840px
5. `top` / `bottom` / `caption` が §0.3 の accuracy_lock を通る
6. `facts[fact_id].verified == false` かつ `required == false` → そのビートを出力から**除外**
7. `facts[fact_id].verified == false` かつ `required == true` → **exit 1**（台本工程に差し戻し）

## 6.4 レイアウト定義（4種・すべて EP38 の実証レイヤースタックから派生）

**共通レイヤースタック（下 → 上）。EP38 `build_kfc_hero_jsx.py` で動作実証済みの構成を踏襲する:**

| L | 内容 | 実装 |
|---|---|---|
| L9 | 黒ソリッド背景 | `addSolid([0,0,0])` |
| L8 | 静止画（fill スケール + イーズ付きプッシュイン + ドリフト） | scale `fill → fill*1.08`（0→dur・ease 25）、position `[W/2-18, H/2+10] → [W/2+18, H/2-10]`（ease 20） |
| L7 | グレードウォッシュ | **EP40 は暖色**: `addSolid([0.14,0.11,0.06])` / MULTIPLY / opacity **30**（EP39の寒色ウォッシュと分離） |
| L6 | 羽根付き楕円ビネット | 黒ソリッド + SUBTRACT マスク・feather `[260,260]`・opacity 62 |
| L5 | グロー（下中央からの ADD ランプ） | Ramp: start `[W/2, H*0.42]` GOLD → end `[W/2, H*0.95]` 黒 / radial(2) / opacity 0→22→14 |
| L4 | ライトスイープ | 白ソリッド 360×H*1.6 / ADD / `"ADBE Rotate Z"` = 18 / position `-300 → W+300`（0.5s→1.25s・ease 45）/ opacity 0→18→0 |
| L3 | 上ラベル（Oswald） | §6.4.1〜4 の座標 |
| L2b | アクセントライン（GOLD・scaleX ワイプ） | `[0,100] → [100,100]`（0.55s→1.05s・ease 90）/ `motionBlur = true` |
| L2 | 主数値（Anton・GOLD） | §6.5 のカウントアップ / `motionBlur = true` |
| L1b | 下ラベル（Oswald・WHITE） | reveal 1.15s |
| L1 | 字幕ロワーサード（暗バー + Oswald） | バー `[0.02,0.04,0.08]` W×130 / opacity 0→64→0 |
| L0 | 黒シームディップ（head/tail 各4フレーム） | opacity 100→0（head）/ 0→100（tail）・ease 40 |

**色定数（0..1 float・EP40）:**
```python
GOLD   = [0.898, 0.710, 0.227]   # #E5B53A  — EP40 アクセント
WHITE  = [0.961, 0.969, 0.980]
SILVER = [0.588, 0.627, 0.682]
DUST   = [0.827, 0.769, 0.667]   # EP40 追加: 埃のアンバー（SPLIT_COMPARE の左辺・弱い側に使う）
```

**フォント:** 数値 = **Anton Regular** / ラベル・字幕 = **Oswald Medium**
（`C:\Users\aab15\AppData\Local\Microsoft\Windows\Fonts\Anton.ttf` / `Oswald.ttf` に**実在を確認済み**）
必ず EP38 と同じ `psName()` ランタイム解決を使い、無言の代替フォント置換を防ぐ。

### 6.4.1 LAYOUT A — CENTER_STACK（b02 / b04 / b05 / b06）

| 要素 | 位置 | フォント/サイズ | トラッキング | 色 |
|---|---|---|---|---|
| 上ラベル | `[W/2, H*0.205]` | Oswald 44 | 340 | SILVER |
| アクセントライン | `[W/2, H*0.485]`・460×6 | — | — | GOLD |
| 主数値 | `[W/2, H*0.42]` | Anton **250** | 0 | GOLD |
| 下ラベル | `[W/2, H*0.60]` | Oswald 64 | 120 | WHITE |
| 字幕バー | `[W/2, H*0.90]`・W×130 | Oswald 42 | 20 | WHITE |

### 6.4.2 LAYOUT B — SPLIT_COMPARE（b03 のみ）

「万引きの被害額」対「家の損害額」の**桁違い**を1画面で殴る。**EP40で最も重要な1枚。**

| 要素 | 位置 | フォント/サイズ | 色 |
|---|---|---|---|
| 上ラベル（共通） | `[W/2, H*0.16]` | Oswald 40 / tracking 340 | SILVER |
| 縦の分割線 | `[W/2, H*0.50]`・4×H*0.42 | — | SILVER opacity 40 |
| 左ラベル `label_a` | `[W*0.27, H*0.31]` | Oswald 38 / tracking 180 | SILVER |
| 左数値（万引き額） | `[W*0.27, H*0.46]` | Anton **150** | **DUST** |
| 右ラベル `label_b` | `[W*0.73, H*0.31]` | Oswald 38 / tracking 180 | SILVER |
| 右数値（家の損害額） | `[W*0.73, H*0.46]` | Anton **210** | **GOLD** |
| 下ラベル | `[W/2, H*0.66]` | Oswald 56 / tracking 120 | WHITE |
| 字幕バー | LAYOUT A と同一 | | |

**タイミング（コンプ内ローカル秒・区間長 7.0s）:**
- 0.15s: 上ラベル reveal（`revealUp`）
- 0.35s: 縦分割線が `scaleY [0,100] → [100,100]`（0.35→0.85s・ease 85）
- 0.50–1.30s: **左（小さい額）を先に**カウント。確定後に 0.20s の「間」
- 1.50–2.50s: **右（大きい額）**をカウント。左より**長い時間かけて**桁が伸びる = 桁違いの体感
- 2.70s: 下ラベル reveal
- **左数値は右のカウント開始と同時に opacity 100→55 に落とす**（0.15s・ease 60）= 主役の切替

### 6.4.3 LAYOUT C — DATE_STAMP（b01 / b08）

数値を主役にせず、**事実の刻印**として見せる。b08 は accuracy_lock の主戦場。

| 要素 | 位置 | フォント/サイズ | 色 |
|---|---|---|---|
| 上ラベル | `[W/2, H*0.30]` | Oswald 44 / tracking 340 | SILVER |
| 年（主数値） | `[W/2, H*0.46]` | Anton **190** | GOLD |
| 横罫（年の下） | `[W/2, H*0.545]`・620×4 | — | GOLD opacity 92 |
| 下ラベル | `[W/2, H*0.63]` | Oswald 52 / tracking 120 | WHITE |
| 字幕バー | LAYOUT A と同一 | | |

**b08 のラベル確定値（accuracy_lock 準拠・この文字列を使う）:**
```
top    = "THE TENTH CIRCUIT"
value  = 2019
bottom = "NO COMPENSATION OWED"
```
**b08 の直後（同一コンプ内 3.6s 地点）に、追加の小テキストを1行出す:**
```
位置 [W/2, H*0.72] / Oswald 34 / tracking 90 / SILVER / opacity 0→88（3.6→3.9s・ease 70）
文字列 = "THE SUPREME COURT DECLINED TO HEAR IT"
```
> この文字列は §0.3 R1 のゾーン外（`beats[].top`/`bottom` ではなく専用フィールド `footnote`）に置く。
> `footnote` は R2 の文脈規則を適用し、`DECLINED TO HEAR` を含むため pass する。
> **`footnote` フィールドを beats スキーマに追加すること**（`"footnote": "string|null"`, 最大44文字）。

### 6.4.4 LAYOUT D — RATIO_BAR（b07）

補償率を**横棒の長さ**で見せる。数字より棒の短さが効く。

| 要素 | 位置 | サイズ/色 |
|---|---|---|
| 上ラベル | `[W/2, H*0.22]` / Oswald 44 / tracking 340 / SILVER |
| 棒の「全体」枠 | `[W/2, H*0.44]`・1200×26 / SILVER outline opacity 45 |
| 棒の「支払われた分」 | 枠の左端から / GOLD / **幅 = 1200 × (value/100)** |
| 主数値（%） | `[W/2, H*0.58]` / Anton **160** / GOLD |
| 下ラベル | `[W/2, H*0.70]` / Oswald 52 / tracking 120 / WHITE |
| `ratio_note` | `[W/2, H*0.78]` / Oswald 28 / tracking 60 / SILVER opacity 75 |

**タイミング（区間長 6.0s）:**
- 0.20s: 上ラベル reveal
- 0.45s: 枠が `scaleX [0,100] → [100,100]`（0.45→1.05s・ease 90）
- 1.15–2.15s: GOLD の棒が `scaleX 0 → (value/100)*100`（`transformOrigin` は左端 = anchor point を左端に置く）
- 1.15–2.15s: 数値が同期してカウントアップ（CT_PCT）
- 2.45s: 下ラベル reveal / 2.75s: `ratio_note` reveal
- **`ratio_note` は必須。** 計算値であることを画面上で明示しないと事実性違反になる。

## 6.5 カウントアップ型（すべて Python 側で全キーを事前計算）

EP38 で実証済みの `count_keys()` を踏襲（18キー・ease-out cubic・最後に正確値へ settle）。

| 型ID | 用途 | decimals | thousands | prefix | suffix | キー数 | 窓 |
|---|---|---|---|---|---|---|---|
| `CT_INT` | 時間・回数 | 0 | false | "" | " HOURS" / " ROUNDS" 等 | 18 | 0.55→1.55s |
| `CT_MONEY` | ドル（大） | 0 | **true** | `"$"` | "" | **24** | 0.55→1.85s |
| `CT_MONEY_M` | ドル（百万単位） | 1 | false | `"$"` | `"M"` | 18 | 0.55→1.55s |
| `CT_PCT` | 率 | 1 | false | "" | `"%"` | 18 | 1.15→2.15s |
| `CT_DATE` | 年 | 0 | **false** | "" | "" | **12** | 0.55→1.25s |
| `CT_COUNTDOWN` | **b06 専用** | 0 | true | `"$"` | "" | **28** | 0.55→2.35s |

**`CT_DATE` の注意:** `thousands=false` 必須。`2,019` と出たら即バグ。

**`CT_COUNTDOWN`（b06・EP40の感情のピーク）の仕様:**
- **b05 で表示した損害額（F03）から出発し、一家が受け取った額（F04）まで減っていく。**
- ease は `ease_out_cubic` ではなく **`ease_in_out_cubic`** を使う（急落してから減速 = 落下の体感）:
  ```python
  def ease_in_out_cubic(p): return 4*p**3 if p < 0.5 else 1 - ((-2*p+2)**3)/2
  ```
- 到達後 0.35s のホールドを挟み、**下ラベルを reveal**（この間、画面はほぼ静止 = 沈黙の演出）
- 数値の色は GOLD → **到達の 0.10s 後に WHITE へ切り替え**（別レイヤーを重ねて opacity で入れ替える。テキストカラーのキーフレームは使わない = AE の TextDocument で色をアニメすると不安定）
- **`bottom` の確定文字列 = `"WHAT THE FAMILY RECEIVED"`**（帰属を保つ。「補償額」と断定しない）

## 6.6 各ビートのカウント窓と区間の関係（必ず守る）

```
0.000                      dur
|--head--|--reveal--|--count--|--hold--|--tail--|
  4/30s              §6.5の窓          ≥1.20s   4/30s
```
**カウント終了から区間終端まで最低 1.20 秒のホールドを確保する。** これが無いと数字が読めない。
`dur < (count_end + 1.20 + tail)` になったら `build_lech_hero_jsx.py` は **exit 1**（黙って詰めない）。

## 6.7 コンポジタ（`scripts/ae/composite_lech_hero.py`）

EP38 の `composite_kfc_hero.py` をベースに、パスと定数のみ差し替える。**SKIP ロジックは1行も削らない。**

```
BASE = episodes/PD-2026-040-lech/08_edit/lech_final_bgm.v002.mp4
OUT  = episodes/PD-2026-040-lech/08_edit/lech_final_bgm.v003_ae.mp4
FFMPEG   = C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe
FFPROBE  = C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffprobe.exe
W, H, FPS = 1920, 1080, 30
```

**SKIP条件（この4つを必ず実装する。1つでも欠けると作品が壊れる）:**
1. `render/<id>.mp4` が存在しない → SKIP
2. 解像度が `1920x1080` でない → SKIP
3. 実測尺 `< dur - 0.3` → SKIP
4. `beat.end > base_dur` → SKIP

**ffmpeg 呼び出し（実証済みの形）:**
```
[k:v] setpts=PTS-STARTPTS+<start>/TB, format=yuv420p [bk]
[prev][bk] overlay=0:0:eof_action=pass:enable='between(t,<start>,<end>)' [vk]
-map [vN] -map 0:a -r 30 -c:v libx264 -preset medium -crf 16 -pix_fmt yuv420p -c:a copy
```

**出荷済みファイルを絶対に上書きしない。** 出力は必ず `_v003_ae` サフィックス。

## 6.8 【Codexが踏まないための注意】このマシン固有の罠

> **EP38 で実際に踏んで潰した罠。1つでも忘れると無言で品質が落ちるか、ビルドが止まる。**

| # | 罠 | 正しい対処 |
|---|---|---|
| 1 | **イーズが無言で効かず等速になる** | `setTemporalEaseAtKey` の配列次元は spatial プロパティ（Position）では**1個**。`var dim = prop.isSpatial ? 1 : (prop.value instanceof Array ? prop.value.length : 1);` |
| 2 | **テンプレート名が英語だと失敗する** | AE 2026・日本語ロケール。RS = **`"最良設定"`** / OM = **`"H.264 - レンダリング設定を一致 - 15 Mbps"`**。英語名は try/catch のフォールバックに置くだけ |
| 3 | **字幕に `\n` を入れると literal で表示される** | AE の TextDocument の改行は `\n` ではない。**字幕は1行に保つ**（§6.3 で `caption` 最大50文字・改行禁止としている理由）。どうしても必要なら `\r` |
| 4 | **`app.newProject()` が headless でハングする** | `-noui` では保存プロンプトで固まる。**使うな。** 代わりに既存の同名コンプを防御的に削除: `for (i=numItems; i>=1; i--) if (item instanceof CompItem && name.indexOf("LECH_")===0) item.remove();` |
| 5 | **ビルドが遅く、早期killしてしまう** | ビルド ~100–120秒 / レンダは速い（6コンプ ~21秒）。**jsx 末尾が書く完了マーカー `render/_build_ok.txt` をポーリングせよ。** タイムアウトは最低 300秒 |
| 6 | **AfterFX/aerender の起動がブロックする** | **デタッチ起動 + 出力ファイルのポーリング**。jsx の末尾で必ず `app.quit()` |
| 7 | **モーションブラーが効かない** | コンプの `comp.motionBlur = true` **だけでは無効**。動かすレイヤー個別に `layer.motionBlur = true`（数値・アクセントライン・分割線・棒） |
| 8 | **`"ADBE Rotation"` が null を返す** | 2Dレイヤーの回転は **`"ADBE Rotate Z"`**（ライトスイープの 18度で使う） |
| 9 | **レイヤーの outPoint がコンプ末尾に残る** | `inPoint` だけ設定すると尻が残る。**inPoint と outPoint の両方を設定する** |
| 10 | **画像シーケンスの fps が 30 にならない** | AE は prefs 既定（30fps）で読むが、prefs が変わると**全ビートの timing が無言でズレる**。読み込み後に必ず `item.mainSource.conformFrameRate = 30;` |
| 11 | 実行パス | `C:\Program Files\Adobe\Adobe After Effects 2026\Support Files\AfterFX.exe` / `aerender.exe`（**実在を確認済み**） |
| 12 | GPU | RTX4090 だが**ソフトウェアレンダで固定**（`proj.gpuAccelType = GpuAccelType.SOFTWARE`）。安定性優先。EP38で実証 |

## 6.9 実行コマンド（そのまま使える形）

```bash
# [1] beats.json と jsx を生成
"C:/Users/aab15/Documents/prime-documentary/.venv/Scripts/python.exe" \
  "C:/Users/aab15/Documents/prime-documentary/scripts/ae/build_lech_hero_jsx.py"

# [2] AE でビルド＋レンダ（デタッチ起動。マーカーをポーリングする）
"C:/Program Files/Adobe/Adobe After Effects 2026/Support Files/AfterFX.exe" -noui \
  -r "C:/Users/aab15/Documents/prime-documentary/episodes/PD-2026-040-lech/08_edit/ae_hero/lech_hero.jsx"
# → episodes/PD-2026-040-lech/08_edit/ae_hero/render/_build_ok.txt が出るまで待つ（最大300秒）
# → 続いて render/b0*.mp4 が揃うまで待つ（最大600秒）

# [3] 本編に焼き込み（v002 は不変・v003_ae を新規作成）
"C:/Users/aab15/Documents/prime-documentary/.venv/Scripts/python.exe" \
  "C:/Users/aab15/Documents/prime-documentary/scripts/ae/composite_lech_hero.py"
```

## 6.10 Remotion 側 MGビート 28枠（`figures` 契約）— AEの8枠と合わせて36枠

> **AEヒーロービート8枠だけでは MGビート密度ゲート（≥2.5/分 = ≥31枠）に届かない。**
> 残り28枠を Remotion の `FigureBeats`（`lech_film.json` の `figures[]`）で埋める。

**実装:** 既存の `remotion/src/components/FigureBeats.tsx` の `FigureSpec` をそのまま使う（**新規コンポーネントを作らない**）。
`lech_film.json` の `figures[]` に 28要素を入れる。

### 6.10.1 種類の配分（種類3以上のゲートに対し **7種**）

| kind | 枠数 | EP40 での用途 |
|---|---|---|
| `ActTitle` | 4 | 幕1〜幕4の幕頭 |
| `timeline` | 4 | 事件当日の時系列 / 訴訟の経過（提訴→地裁→第10巡回区→上告不受理） |
| `stat` | 6 | AE の8枠に載せない副次的な数値（年数・人数・回数） |
| `bar` / `ComparisonBars` | 4 | 対比（市の評価額 vs 一家の主張額 など） |
| `QuoteCard` | 4 | 判決文・市の回答・反対の論理の**逐語引用** |
| `MechanismReveal` | 4 | **police power 例外と Takings Clause の分岐**／限定免責の重なり（EP40のドクトリン説明の主役） |
| `RouteMap` / `PinDropMap` | 2 | 逃走経路 / 家の位置関係 |
| **合計** | **28** | |

### 6.10.2 配置ルール（AEビートと衝突させない）

1. **AEの8区間（§6.2）と1秒でも重ならないこと。** `validate_lech_beats.py` が両方を突き合わせて検査する。
2. 幕あたりの目安: 幕1 = 5枠 / 幕2 = 7枠 / 幕3 = 7枠 / 幕4 = 8枠 / ED = 1枠
3. **同じ kind を連続させない**（`ActTitle` の直後に `ActTitle` は不可）。
4. 1枠の長さは **4.0–8.0秒**。28枠 × 平均5.5秒 = 154秒 = 全体の20.8%。
   §5.1.2 の「静止画カット156本」はこの図版区間を除いた残りに配置する。
5. `QuoteCard` の引用文は **§0.3 の accuracy_lock 検査対象**（`figures[].text` を対象パスに含めること）。

### 6.10.3 密度の最終検算

```
AEヒーロービート        8
Remotion FigureBeats   28
------------------------
合計                   36 枠

36 / 12.36分 = 2.91 /分     ✓ ≥2.5/分
種類 = AE 4レイアウト + Remotion 7種 = 11種   ✓ ≥3種
```

> **台本未確定時（§4.4 stub）の扱い:** 28枠は「区間と kind だけ確定・テキストはマーカー文字列」で
> stub を生成する。ドライランでは中身が `[[SLOT:...]]` のまま描画されるが、
> **区間・kind・密度は本番と同一**なので、密度ゲートの通過をドライラン時点で実証できる。

---

# 7. オープニング（OP）設計 — 完全仕様

> **この節は Codex が単体で読んで実装できるように、解釈の余地なく書いてある。**
> 正典の下敷き: `C:\Users\aab15\Documents\pino-channel\remotion\src\Opening.tsx`（読了済み）。
> 構造・レイヤー・イージング種別はそれを踏襲し、**色・文字サイズ・追加レイヤーだけを EP40 用に差し替える**。

## 7.0 【重要】v2 row14 との関係 — 二重OPを作らない

`docs/PD_ONE_PASS_PRODUCTION_SPEC.v2.md` row14 は「本編内のOP/EDの正典は `remotion/src/components/Bookends.tsx`（`BrandOpening` / `OPENING_SEC=3.5`）」と定めており、フォーク禁止（invariant 14）。

**したがって EP40 での位置づけを次のように確定する:**
- **本編（`Ep40Lech` コンポジション）のOPは `BrandOpening` のまま。変更しない。** `op_ed_bookends` ゲートを通すため。
- 本節で定義する `OpeningLech` は、**独立したタイトルバンパー成果物**（`out/lech_opening.mp4`）である。用途は (a) 本節の品質ルールを満たす再利用可能部品、(b) Shorts / 予告 / SNS 用の頭。
- **`OpeningLech` を本編に ffmpeg で焼き込んではならない**（オーナー承認なしに row14 の見え方を変えない）。

## 7.1 セクション0 — 環境・Remotion設定

### Composition 設定

| 項目 | 値 |
|---|---|
| `id` | **`OpeningLech`** |
| 解像度 | **1920 × 1080** |
| `fps` | **60** |
| `durationInFrames` | **180**（= 3.0秒 @ 60fps） |
| component | `OpeningLech`（`remotion/src/compositions/OpeningLech.tsx`） |

**Root.tsx への登録（`remotion/src/Root.tsx` に追記する。既存の `Opening` composition とはIDが別なので衝突しない）:**

```tsx
import {OpeningLech, openingLechDurationInFrames} from './compositions/OpeningLech';
import lechOpeningProps from '../props/lech.json';

<Composition
  id="OpeningLech"
  component={OpeningLech}
  width={1920}
  height={1080}
  fps={60}
  durationInFrames={openingLechDurationInFrames(60)}
  defaultProps={lechOpeningProps}
/>
```

### 必要な依存パッケージ

```bash
cd C:\Users\aab15\Documents\prime-documentary\remotion
npm i @remotion/motion-blur
```

> **確認済み:** `remotion/package.json` に `"@remotion/motion-blur": "^4.0.476"` が既に存在し、`node_modules/@remotion/motion-blur` も実在する。**上記コマンドは未導入時のみ実行**。既に入っている場合は何もしなくてよい。

### remotion.config.ts

**確認済み:** `remotion/remotion.config.ts` は既に下記の正典値で設定されている。**内容が下記と一致していることを確認するだけでよく、書き換えてはならない。**

```ts
import {Config} from '@remotion/cli/config';
import os from 'os';

Config.setVideoImageFormat('png');            // 中間フレームはロスレスPNG
Config.setCodec('h264');                      // H.264 / libx264（CPU）
Config.setCrf(16);                            // CRF 16（ほぼ視覚的ロスレス）
Config.setX264Preset('slow');                 // NVENC/高速プリセットへ逃がさない
Config.setPixelFormat('yuv420p');             // 全プレーヤー互換
Config.setColorSpace('bt709');                // 色域を明示
Config.setAudioCodec('aac');
Config.setAudioBitrate('320k');               // 音声 AAC 320k
Config.setConcurrency(os.cpus().length);      // 全CPUコア = 最大並列
Config.setChromiumOpenGlRenderer('angle');    // GPU合成をANGLEで安定化
Config.setOverwriteOutput(true);
```

## 7.2 セクション1 — 秒数ベースのタイムライン（全区間）

**fps = 60。以下の「フレーム」は全て `Math.round(fps * 秒)` で算出されるもので、コード内にフレーム数を直書きしてはならない。**

| 秒 | フレーム | 起きること |
|---|---|---|
| **0.00–0.10** | f0–f6 | 画面は `#0d0b08`（EP40の暖色寄りの黒）。**レイヤー1** グラデ背景の opacity が 0→（0.40秒かけて）1へ、同時に scale 1.08 が 180フレームかけて 1.00 へ動き出す（`Easing.out(Easing.cubic)`）。**opacity 単独ではなく scale と併用**。 |
| **0.10–0.15** | f6–f9 | **ロゴ**（`hasLogo` が true のとき）が左上 `top:64 / left:72` に spring で出現。scale 0.4→1.0・opacity 0→1（**併用**）。 |
| **0.15–0.25** | f9–f15 | **レイヤー2** グリッドが spring（`damping:200, mass:1`, `durationInFrames = round(fps*0.8) = 48`）で reveal。最終 opacity = `gridReveal * 0.18`。同時にグリッド全体が 180フレームかけて `translateY 0→48px`（`Easing.inOut(Easing.sin)`）でドリフト。 |
| **0.25–0.30** | f15–f18 | **レイヤー3** グローが spring（`damping:18, mass:1.2`）で立ち上がる。scale 0.6→1.15 / opacity 0→0.85（**併用**）。サイズは `width*0.62 × height*0.36`、`filter: blur(28px)`。 |
| **0.30–0.86** | f18–f52 | **レイヤー4 主役タイトル**が1文字ずつ切れ上がる。各文字 spring（`damping:16, mass:1`）で `translateY 110% → 0`、`opacity` は spring 値 `[0, 0.25] → [0, 1]`（clamp）。**スタッガー = `Math.max(1, round(fps * 0.04)) = 2フレーム/文字**。`title = "LECH"`（4文字）なら 最終文字の開始は f18 + 3×2 = **f24**、収束は約 f52。全体を `@remotion/motion-blur` の `Trail`（`layers=6, lagInFrames=1.2, trailOpacity=0.45`）で包む。 |
| **0.55–1.15** | f33–f69 | **レイヤー2b（EP40 追加）フラクチャーライン**。画面中央からタイトル背後を横切る細い亀裂状の線が `scaleX 0→1` + `opacity 0→0.55` で開く（spring `damping:22, mass:1.1`、`transformOrigin: 'center'`）。**破壊のモチーフ**。opacity 単独禁止のため scaleX と併用。 |
| **0.95–1.35** | f57–f81 | **レイヤー5a** アクセント下線が左から `scaleX 0→1` にワイプ（spring `damping:16, mass:0.8`、`transformOrigin: 'left center'`）。幅 240px・高さ 6px・`boxShadow: 0 0 24px ${accent}aa`。 |
| **1.10–1.55** | f66–f93 | **レイヤー5b** サブタイトルが `translateY 24px→0` + `opacity 0→1`（spring `damping:20, mass:1`・**併用**）。 |
| **1.55–2.20** | f93–f132 | 全要素が settle。背景 scale は依然 1.02 付近を緩やかに進行中（等速に見えない・`Easing.out(Easing.cubic)` の減速域）。グリッドのドリフトも継続。**完全な静止フレームが1枚も無いこと。** |
| **2.20–3.00** | f132–f180 | ホールド。背景 scale が 1.00 に着地、グリッド translateY が 48px に着地。**フェードアウトはしない**（後段の編集で繋ぐ前提）。 |

## 7.3 セクション2 — 各要素のイージング・ディレイ・移動量・damping（数値表）

**タイミング定数（すべて秒。`const T = {...} as const;` で定数化し、`sec(fps, T.x)` でフレーム化する。フレーム直書き禁止）:**

```ts
const T = {
  bgIn:        0.00,  // 背景フェード/ズーム開始
  logoIn:      0.10,  // ロゴ
  gridIn:      0.15,  // グリッド出現
  glowIn:      0.25,  // グロー出現
  titleIn:     0.30,  // タイトル切れ上がり開始
  charStagger: 0.04,  // 1文字ごとのディレイ（60fps で 2フレーム）
  fractureIn:  0.55,  // EP40追加: フラクチャーライン
  accentIn:    0.95,  // アクセント下線ワイプ
  subIn:       1.10,  // サブタイトル
} as const;

const sec = (fps: number, s: number) => Math.round(fps * s);
export const openingLechDurationInFrames = (fps: number) => Math.round(fps * 3.0);  // = 180 @60fps
```

| 要素 | 開始 | 終了 | 手法 | 移動量 / 変化量 | イージング・パラメータ |
|---|---|---|---|---|---|
| 背景 scale | f0 | f180 | `interpolate` | **1.08 → 1.00** | `Easing.out(Easing.cubic)`・両端 clamp |
| 背景 opacity | f0 | f24 | `interpolate` | 0 → 1 | 両端 clamp（**scale と併用**） |
| グリッド translateY | f0 | f180 | `interpolate` | **0 → 48px** | `Easing.inOut(Easing.sin)` |
| グリッド reveal | f9 | f57 | `spring` | opacity 0 → **0.18** | `damping: 200, mass: 1`, `durationInFrames: sec(fps, 0.8) = 48` |
| グロー scale | f15 | — | `spring` → `interpolate` | **0.6 → 1.15** | `damping: 18, mass: 1.2` |
| グロー opacity | f15 | — | 同 spring | 0 → **0.85** | 同上（**scale と併用**） |
| タイトル各文字 translateY | f18 + i×2 | — | `spring` | **110% → 0** | `damping: 16, mass: 1` |
| タイトル各文字 opacity | 同上 | — | `interpolate(springVal, [0,0.25],[0,1])` | 0 → 1 | clamp（**translateY と併用**） |
| タイトル Trail | 全域 | — | `@remotion/motion-blur` `Trail` | — | `layers={6} lagInFrames={1.2} trailOpacity={0.45}` |
| **フラクチャー scaleX** | f33 | — | `spring` | **0 → 1** | `damping: 22, mass: 1.1`・`transformOrigin: 'center'` |
| **フラクチャー opacity** | f33 | — | 同 spring | 0 → **0.55** | 同上（**scaleX と併用**） |
| アクセント下線 scaleX | f57 | — | `spring` | **0 → 1** | `damping: 16, mass: 0.8`・`transformOrigin: 'left center'` |
| サブタイトル translateY | f66 | — | `spring` | **24px → 0** | `damping: 20, mass: 1` |
| サブタイトル opacity | f66 | — | 同 spring | 0 → 1 | 同上（**translateY と併用**） |
| ロゴ scale | f6 | — | `spring` | **0.4 → 1.0** | `damping: 14, mass: 0.9` |
| ロゴ opacity | f6 | — | 同 spring | 0 → 1 | 同上（**scale と併用**） |

> **等速線形は1箇所も使わない。** すべて `spring` か `Easing.out(Easing.cubic)` / `Easing.inOut(Easing.sin)`。
> **opacity 単独の演出は1箇所も無い。** 全ての opacity が translateY / scale / scaleX と対になっている。

## 7.4 セクション3 — レイヤー構成（重なり順・下 → 上）

| L | 名前 | 内容 | EP40 の値 |
|---|---|---|---|
| **L0** | ルート背景 | `AbsoluteFill` 単色 | `backgroundColor: '#0d0b08'`（暖色寄りの黒。EP39 の `#05070d` 系と分離） |
| **L1** | **グラデ背景** | 放射グラデーション + scale + fade | `radial-gradient(120% 120% at 50% 35%, #3a2f1c 0%, #1c1710 45%, #0d0b08 100%)` |
| **L2** | **グリッド/ライン** | 縦横 64px の繰り返し線 + 放射マスク + ドリフト | `repeating-linear-gradient(0deg / 90deg, ${accent}22 0px 1px, transparent 1px 64px)`、`maskImage: radial-gradient(120% 90% at 50% 45%, black 35%, transparent 80%)` |
| **L2b** | **フラクチャーライン**（EP40追加） | 中央を横切る亀裂状のグラデ線 | 幅 `width*0.78` / 高さ 3px / `background: linear-gradient(90deg, transparent 0%, ${accent}00 8%, ${accent}cc 34%, ${accent}55 52%, ${accent}cc 71%, ${accent}00 92%, transparent 100%)` / `transform: translateY(-6px) scaleX(...)` |
| **L3** | **グロー** | タイトル裏の放射グロー | `width*0.62 × height*0.36`、`radial-gradient(closest-side, ${accent}88 0%, ${accent}22 45%, transparent 75%)`、`filter: blur(28px)` |
| **L4** | **主役タイトル** | `Trail` で包んだ文字スタッガー。各文字は `overflow:hidden` の span + 内側 span を `translateY` | `fontFamily: 'Inter, system-ui, sans-serif'` / `fontWeight: 800` / **`fontSize: 150`** / `letterSpacing: -2` / `color: '#ffffff'` / `lineHeight: 1.05` / 外側 `transform: translateY(-70px)` / 各 span に `paddingBottom: '0.12em'` |
| **L5** | **アクセント下線 + サブタイトル** | 縦並び（`flexDirection: 'column'`, `gap: 18`）、`transform: translateY(55px)` | 下線 240×6・`borderRadius: 3`。サブタイトル `fontWeight: 500` / `fontSize: 38` / `letterSpacing: 6` / `textTransform: 'uppercase'` / `color: '#c8d2e6'` |
| **L6** | **ロゴ**（`hasLogo` 時のみ） | 左上のバッジ | `top:64 / left:72 / 84×84 / borderRadius:20`、`background: linear-gradient(135deg, ${accent}, #ffffff22)`、`border: 2px solid ${accent}`、`boxShadow: 0 0 30px ${accent}66` |

> **主役（L4）の裏に最低3レイヤー**という要件: L1（グラデ背景）/ L2（グリッド）/ L2b（フラクチャー）/ L3（グロー）= **4レイヤー**で満たす。

**テキストのマスク切れ上がり（基本形・必ずこの構造）:**
```tsx
<span style={{display:'inline-block', overflow:'hidden', paddingBottom:'0.12em'}}>
  <span style={{display:'inline-block', transform:`translateY(${y}%)`, opacity:charOpacity, whiteSpace:'pre'}}>
    {ch}
  </span>
</span>
```

## 7.5 セクション4 — props 定義と型

```ts
export type OpeningLechProps = {
  title: string;      // 主役タイトル。1文字ずつスタッガーで切れ上がる。推奨 3–8文字（fontSize 150 前提）
  subtitle: string;   // サブタイトル。UPPERCASE 表示（CSS で変換されるので入力は任意ケース）
  accent: string;     // アクセントカラー（HEX 6桁・"#" 込み）。グリッド線/フラクチャー/グロー/下線/ロゴに波及
  hasLogo: boolean;   // true のとき左上にロゴバッジを出す
};
```

**EP40 の確定 props（`remotion/props/lech.json` に保存する）:**

```json
{
  "title": "LECH",
  "subtitle": "POLICE POWER",
  "accent": "#E5B53A",
  "hasLogo": true
}
```

> `accent` の `#E5B53A` は §2 の EP40 専用アクセント（gold/amber）。
> **EP39 では `#1F6BFF` を使うこと。`props/` 配下でファイルを分けるので衝突しない。**

## 7.6 セクション5 — 確認方法と量産レンダリング

**プレビュー（Remotion Studio）:**
```bash
cd C:\Users\aab15\Documents\prime-documentary\remotion
npm run studio
```
→ ブラウザで composition `OpeningLech` を選び、タイムラインを 0→180 フレームでスクラブして
§7.2 の各時刻に指定の動きが起きていることを目視確認する。

**単体レンダリング:**
```bash
cd C:\Users\aab15\Documents\prime-documentary\remotion
npx remotion render OpeningLech out/lech_opening.mp4 --props=./props/lech.json
```

**props 差し替えによる量産（再利用部品としての運用）:**
```bash
npx remotion render OpeningLech out/lech_opening.mp4     --props=./props/lech.json
npx remotion render OpeningLech out/lech_short_op.mp4    --props=./props/lech_short.json
npx remotion render OpeningLech out/lech_teaser.mp4      --props=./props/lech_teaser.json
```

**props ファイルの例（`remotion/props/lech_short.json`）:**
```json
{ "title": "LECH", "subtitle": "THE TENTH CIRCUIT", "accent": "#E5B53A", "hasLogo": false }
```

> `subtitle` に入れる文字列も §0.3 の accuracy_lock 検査対象に含めること
> （`props/*.json` を `check_lech_accuracy.py` の対象パスに追加する）。

---

# 8. サムネイル3案（CTR 2.31% → 目標 4%）

**共通要件（v2 row11–12）:**
- Remotion `<Still>` で **1280×720** レンダ。`remotion/src/compositions/LechThumbnails.tsx` に3案を実装
- **見出しは全て大文字・4語以内**・320px で判読可能
- **実在人物の肖像は使わない**
- **「最高裁 / Supreme Court / SCOTUS」を書かない**（§0.3 R1）
- `thumbnail_visibility` ゲート（selected の luma 平均 ≥ 33 + コントラスト下限）を通す
  → **EP40 は昼のシーンなので luma は余裕がある。むしろ白飛びに注意**し、ハイライトを 245 以下に抑える

## T1 — 「穴の空いた家」（最推奨・情報量最小）

| 項目 | 内容 |
|---|---|
| 主被写体 | 郊外の一軒家の**壁に開いた巨大な穴**を、家の全体が入る引きで。穴の中は暗く、周囲は白飛び寸前の昼光 |
| 構図 | 家は**画面の右 60%** を占める。左 40% に文字。穴が画面のほぼ中心に来るよう配置 |
| 文字 | **`YOUR HOUSE. THEIR CALL.`**（4語） |
| 文字スタイル | Anton・白 `#F5F7FA`・下端に `#E5B53A` の太い下線。文字高 = 画面高の 19% |
| 色/コントラスト | 昼光の白 + コンクリート灰 + **穴の中の黒**（最大コントラスト点）+ 金の下線1本のみ |
| 狙い | 「家に穴」という**説明不要の異常**。二人称の "YOUR" で自分事化 |

## T2 — 「額の対比」（数字勝負）

| 項目 | 内容 |
|---|---|
| 主被写体 | 崩れた家を背景に暗く落とし、前面に**2つの数字**（左＝万引きの被害額 / 右＝家の損害額） |
| 構図 | 左右分割。中央に細い金の縦線。数字は Anton・右の数字が左の **2.2倍の文字高** |
| 文字 | **`HE STOLE THIS. THEY DESTROYED THIS.`** は長すぎるため → **`STOLEN vs DESTROYED`**（3語） |
| 数字 | F02 と F03 の**検証済み値**。未検証なら **この案は使用しない**（T1/T3 から選ぶ） |
| 色/コントラスト | 背景を輝度 25% まで落とし、数字を白 + 右側だけ金。**最も明るい点が数字**になるようにする |
| 狙い | 桁違いの理不尽を1秒で伝える。数字系サムネは検証依存なので**フォールバックを必ず用意** |

## T3 — 「請求書ゼロ」（怒りのトリガー）

| 項目 | 内容 |
|---|---|
| 主被写体 | 瓦礫の上に置かれた**1枚の紙**（文字は判読不能）。紙の上にだけ強い日光が当たり、周囲は影 |
| 構図 | 紙は画面下 1/3・中央。上 2/3 に破壊された家のシルエットと空 |
| 文字 | **`THEY PAID NOTHING`**（3語） |
| 文字スタイル | Anton・白・`NOTHING` だけ `#E5B53A` の金。文字は画面上部に配置 |
| 色/コントラスト | 昼だが**沈んだ露出**（家は影）＋ 紙のハイライトだけ明るい。金は1語のみ |
| 狙い | 「NOTHING」の一語で怒りを起こす。コメント誘導（§9）と直結 |

**A/B タイトル候補（`title_candidates` に入れる。60字以内・二人称必須）:**
- **A:** `Police Destroyed Their House. Nobody Paid For It.` （50字）
- **B:** `Can Police Destroy Your Home And Pay You Nothing?` （49字）

> 両案とも「最高裁」を含まない。B案は §1.2 の勝ちパターン（「◯◯はあなたに△△できるのか？」）に完全一致。

---

# 9. コメント誘導導線の設計（現在コメント0）

## 9.1 なぜ今までゼロだったか

**問いかけが1度も無かった。** 動画が「説明」で終わり、視聴者に**渡されるもの**が無い。
EP40 は「落ち度ゼロの家族が全てを失った」＝**怒りが自然に湧く題材**。この感情を必ず言語化の出口へ導く。

## 9.2 ED の確定文言（`ed` スロットに入れる）

**[1] 感情のペイオフ（`payoff_line`）— 幕4の結論直後、10:30 付近:**
> "The family did nothing wrong. A stranger chose their house. And when it was over, the law said the loss was theirs to carry."

**[2] earned CTA（`cta_line`）— ペイオフの直後（v2 row10・懇願しない）:**
> "If this changed how you think about who pays when the state breaks something — hit like. That's how these cases find people."

**[3] コメント誘導の問い（`question_line`）— CTA の直後。ここが最重要:**
> "So here's the question we want you to answer: if it were your house, who should pay — the city, or you?"

**設計上の必須条件（すべて満たすこと）:**
1. **二択にする。** 「どう思いますか？」は答えにくい。「the city, or you?」は 1語で答えられる
2. **"your house" と言う。** 二人称で当事者にする
3. **問いは1つだけ。** 複数出すと誰も答えない
4. **CTA より後、エンドカードより前**に置く（`BrandEndcard` の 9秒の直前）
5. 画面には**問いの文字を焼く**（下部の字幕帯ではなく**中央〜上部のテロップゾーン**。VIDEO_RULES §13 のゾーン分離を守る）

## 9.3 固定コメント（オーナーが公開時に投稿・パッケージに文面を用意しておく）

`episodes/PD-2026-040-lech/09_package/pinned_comment.v001.txt` に以下を生成:

> Two things this case turns on, and neither is obvious:
> (1) The Tenth Circuit held this was an exercise of **police power**, not a taking — so the Takings Clause never kicks in.
> (2) The Supreme Court declined to hear the appeal in 2020. That is not agreement; it just means the ruling stands.
>
> If it were your house — should the city pay, or should you?

> **注意:** この文面も §0.3 の accuracy_lock 検査対象。`09_package/*.txt` を対象パスに含めること。

## 9.4 概要欄と Shorts の導線（`PD_WINNING_PATTERN.md` §4）

- 概要欄 **1行目 = 問い**（`question_line` と同一文）。2行目に判例引用（`Lech v. Jackson, 791 F. App'x 711 (10th Cir. 2019), cert. denied (2020)`）
- 連動 Shorts: 同じ問いの 35–45秒版。**CTA は1つだけ**＝「続きは本編で」。Shorts の固定コメントにも同じ二択の問いを置く
- 終了画面 = 次の本編 + 登録

---

# 10. 工程分担 — Codex単体で可能な範囲 / Claude別工程

## 10.1 Codex が**台本を待たずに今すぐ着手できる**範囲

| # | 作業 | 成果物 | 依存 |
|---|---|---|---|
| C1 | エピソードディレクトリの作成 | `episodes/PD-2026-040-lech/{00_topic,01_research,03_script,04_scenes,05_stock,05_visuals,06_audio,08_edit,09_package,approvals,events}` + `manifest.json`（`target_duration_minutes: 12`） | なし |
| C2 | **画像生成 132枚**（§5.6 の S01–S22 × 6） | `H:\pd-media\assets\ai\lech\*.png`（長辺 ≥3840）+ `05_stock/stock_ledger.v001.json` | なし（プロンプト確定済み） |
| C3 | **サムネ実装**（T1/T3 のレイアウト。T2 は数値待ち） | `remotion/src/compositions/LechThumbnails.tsx` + Root.tsx に3 Still 登録 | なし |
| C4 | **OP実装**（§7 全仕様） | `remotion/src/compositions/OpeningLech.tsx` + `remotion/props/lech.json` + Root.tsx 登録 + `out/lech_opening.mp4` | なし |
| C5 | **スロット契約の実装** | `scripts/validate_lech_slots.py` / `scripts/make_lech_slots_stub.py` | なし（§4.2 に schema 確定） |
| C6 | **accuracy_lock ゲート** | `scripts/check_lech_accuracy.py`（§0.3 の R1–R5） | なし |
| C7 | **AEビルダ実装** | `scripts/ae/build_lech_hero_jsx.py`（4レイアウト・6カウント型・§6.8 の罠12件すべて対処） | なし |
| C8 | **AEコンポジタ実装** | `scripts/ae/composite_lech_hero.py`（SKIP 4条件） | なし |
| C9 | **beats バリデータ** | `scripts/validate_lech_beats.py`（§6.3 の不変条件7件） | なし |
| C10 | **stub での通しドライラン** | `episodes/PD-2026-040-lech/08_edit/_dryrun/` に AE 8ビート + コンポジット結果 | C1,C5,C7,C8 |
| C11 | factory 素材の選定（EP39 と sha256 重複除外） | `05_stock/factory_selection.v001.json` | なし |

**→ C1–C11 は台本本文を1文字も必要としない。** C10 のドライランが通れば、台本確定後は**データ差し替えだけ**で完成する。

## 10.2 Claude 別工程（台本パイプライン・並行進行中）

| # | 作業 | 成果物 |
|---|---|---|
| A1 | リサーチ + claim台帳（1文1典拠） | `01_research/claims.v001.json` |
| A2 | **F01–F09 の事実検証**（§0.4） | `01_research/fact_recheck.v001.md` |
| A3 | FILM BIBLE + 台本3稿（初稿→批評→改稿・**目標2,140語 / band 2,048–2,226語 @178.1wpm**）。各稿ごとに `check_script_length.py` を走らせ、**最終稿は exit 0 必須** | `03_script/EP40_lech_FILM_BIBLE.v001.md` / `script.en.v003.md` |
| A4 | **`lech_slots.v001.json` の生成**（§4.2 契約） | `03_script/lech_slots.v001.json` |
| A5 | scene_plan（1ビートごとの意味一致 §5.7） | `04_scenes/scene_plan.v001.json` |
| A6 | shotlist（全カットに motion/transition/keywords） | `04_scenes/shotlist.v001.json` |

## 10.3 Claude 別工程（DSP / ゲート・台本後）

| # | 作業 | 備考 |
|---|---|---|
| D1 | ナレーション生成（ElevenLabs `nPczCjzI2devNBz1zQrb` / `eleven_multilingual_v2` / stability 0.35 / similarity_boost 0.80） | **有料。オーナー承認済みの範囲でのみ実行**。本設計フェーズでは起動しない |
| D2 | 強制アラインメント字幕（faster-whisper 語タイム・ズレ ≤120ms） | `caption_narration_match` ≥99% |
| D3 | 4層ミックス（ナレ / BGM / SFX / 環境音・ダッキング・-16〜-12 LUFS） | §2 の EP40 音響レーン |
| D4 | 全ゲート実行 | `motion_density` / `animation_mix` / `caption_integrity` / `visual_asset_qc` / `footage_diversity` / `accuracy_lock` |
| D5 | 最終受入 | `check_final_acceptance.py 40 --render <final> --emit-receipt` → exit 0 |
| D6 | アップロード / 予約 | **オーナー操作のみ**（invariant 2） |

## 10.4 禁止事項（本フェーズ）

- **有料プロバイダジョブを起動しない**（画像生成の課金APIジョブ・TTS・アップロード）。
  §10.1 C2 の画像生成は、**オーナーが明示的にGOを出した後**に実行する。設計段階では**プロンプトの確定まで**。
- 公開済み mp4 を再レンダリング/上書きしない（invariant 6）。
- EP39 のファイルに触れない。

---

# 11. 受入基準（EP40 の Definition of Done）

**ゲートは以下の順で走らせる。★語数ゲートが最初** — TTS とレンダーに課金する前に落とすため。

```bash
# 0. ★語数ゲート（最優先。課金の前に必ずここで止める）
./.venv/Scripts/python.exe scripts/check_script_length.py \
  episodes/PD-2026-040-lech/03_script/script.en.v003.md --json
#    → 2,048–2,226語の外なら exit != 0。「だいたい12分ぶん」という自己申告は無効。

# 1. 水増しゲート（語数を中身以外で稼いでいないか）
./.venv/Scripts/python.exe scripts/check_padding.py --ep lech --json

# 2. 事実性ゲート（EP40 固有）
./.venv/Scripts/python.exe scripts/check_lech_accuracy.py --json

# 3. スロット/ビート契約（内部で 0 と 2 を再実行する）
./.venv/Scripts/python.exe scripts/validate_lech_slots.py
./.venv/Scripts/python.exe scripts/validate_lech_beats.py

# 4. レンダ前プリフライト（素材の実在・モーション予算。0 が最初のチェックとして配線済み）
./.venv/Scripts/python.exe scripts/preflight_render_gate.py --ep lech

# 5. 本編の最終受入（v2 の全ハードゲート）
./.venv/Scripts/python.exe scripts/check_final_acceptance.py 40 \
  --render episodes/PD-2026-040-lech/08_edit/lech_final_bgm.v003_ae.mp4 --emit-receipt
```

**全て exit 0 でなければ `package_ready` にしない。** 自己申告のQCは無効（v2 THE ONE RULE）。

| ゲート | EP40 での目標値 |
|---|---|
| **`check_script_length`（★最優先）** | **総語数 2,048–2,226（目標2,140）／`wpm_assumed` 178.1** |
| **`check_padding`** | **dead air / 言い換え反復の violation = 0。幕内部に2秒超の間を作らない（§3.3）** |
| `runtime_band` | 11.5–12.5分（standard）。設計値 **741.4秒 = 12:21** |
| `animation_density` | near-still ≤10% / 単一ホールド ≤3秒 / **5秒超の長止め ≤8箇所** |
| **MGビート密度** | **≥2.5/分 かつ 種類3以上** → 設計値 **36枠 / 2.91per分 / 11種**（§5.1.2・§6.10） |
| **factory クリップ** | **≥25本**（30秒に1本）→ 設計値 **54本** |
| **静止画占有率** | **≤45%** → 設計値 **43.1%** |
| `footage_diversity` | distinct/total ≥0.40（設計値 **0.575**）・単一クリップ再利用 ≤4回（設計値 **2.6回**）・**EP39 との sha256 重複 0** |
| `image_resolution` | 全使用静止画 長辺 ≥3840px |
| `caption_narration_match` | ≥99% |
| `thumbnail_present` / `thumbnail_visibility` | 3案 @1280×720 + selected・luma平均 ≥33 |
| `op_ed_bookends` | `BrandOpening` / `BrandEndcard` を import（フォークしない） |
| `structure_4part` | hook / opening / body / ending が順に存在 |
| loudness | -16〜-12 LUFS |
| **`accuracy_lock`（EP40固有）** | **violations = 0** |

---

# 12. リスクと事前対処（premortem）

| リスク | 兆候 | 事前対処 |
|---|---|---|
| **「最高裁が決めた」と書いてしまう** | 台本/サムネ/タイトルに Supreme Court | §0.3 の機械ゲート。人間の注意力に頼らない |
| 数値が検証できず AE ビートが空になる | `facts.*.verified: false` が多い | `required: false` のビートは自動除外・コンポジタが SKIP（§6.3 / §6.7） |
| EP39 と素材が被る | `footage_diversity` が落ちる | §2 のレーン分離 + sha256 重複除外（C11） |
| AE のイーズが効かず等速になる | 動きが機械的に見える | §6.8 罠#1。実装後に1ビートを目視確認する |
| AE ビルドを早期 kill する | ビートが揃わない | §6.8 罠#5。`_build_ok.txt` をポーリング・タイムアウト300秒以上 |
| 出荷済みファイルを上書き | 復旧不能 | 出力は必ず `_v003_ae` の新規名（§6.7） |
| 昼のシーンで白飛び | サムネ/本編のハイライトが潰れる | ハイライトを 245 以下にクランプ。`thumbnail_visibility` は暗さのゲートなので**白飛びは検出されない** — 目視確認を工程に入れる |
| 台本が来ないまま止まる | 進捗ゼロ | §4.4 の stub ドライラン。コードパスを分岐させない |
| **★尺不足で出荷（過去38話中30話で発生）** | 台本が 1,700語前後で「書けた気がする」 | **`check_script_length.py` を台本の各稿ごとに走らせる。** 2,048語未満なら書き足す。体感で判断しない |
| **語数を水増しで埋める** | 同じ主張の言い換えが増える | `check_padding.py`。増やすのは §3.1.2 の6カテゴリ（ディテール/二つ目の事例/その後の人生/反対の論理/制度の仕組み/数字の出所）だけ |
| **語数が band 上限を突き抜ける** | 2,226語超 → 12.5分超 | 設計の余裕は **8.6秒しかない**（§3.1 検算[3]）。増量時は必ず `check_script_length.py` を再実行 |
| **実測ペースが遅い側（163.7wpm）に振れる** | 2,140語 → 785秒 = 13.1分で band 超過 | ナレ生成後に**実尺を必ず測る**。`runtime_band` はオーナーが唯一許容した逸脱項目だが、**まず声のスピードを固定して回避する**（v2 row2 の設定値を変えない） |
| **★実測ペースが速い側（237.4wpm）に振れる** | 2,140語が **9.0分** で終わり、floor を割る。**williams / florence で実際に発生した** | `check_script_length.py` が実際にこの警告を出す（2026-07-19 に本設計値で実行して確認済み）。対処は**声のスピードを固定すること**であって語数を2,730語に増やすことではない（増やすと中央値ペースで band 上限を突き抜ける）。**ナレ生成直後に実尺を測り、9〜10分台なら編集に進む前に差し戻す**（TTS課金済み・レンダ前が最後の安全な戻り点） |
| **素材が 1,675語前提のまま足りない** | カット220本に対し素材が160本しかない | §5.1 は **741.4秒前提で積算済み**（静止画60/i2v16/factory54/カット226/MG36）。EP38 の実績値をそのまま流用しない |

---

# 13. 参照した正典（すべて実読済み）

- `docs/PD_WINNING_PATTERN.md`（BINDING）
- `docs/PD_ONE_PASS_PRODUCTION_SPEC.v2.md`（BINDING・row 1–16 / A–E）
- `episodes/_planning/EP37_florence_DESIGN_and_CODEX_PROMPTS.md`（11–12分テンプレ）
- `episodes/_planning/VIDEO_RULES.md`
- `scripts/ae/build_kfc_hero_jsx.py` / `scripts/ae/composite_kfc_hero.py`（EP38 実証パイプライン）
- `remotion/remotion.config.ts`（正典レンダ設定・確認済み）
- `remotion/src/compositions/CaseFilm.tsx`（`FilmData` 型 / `caseFilmDurationInFrames`）
- `remotion/src/components/FigureBeats.tsx`（`FigureSpec`）
- `C:\Users\aab15\Documents\pino-channel\remotion\src\Opening.tsx`（OP正典実装）

---
---

# ## Codex引き継ぎプロンプト（そのまま貼る）

```
あなたは Prime Documentary（YouTubeドキュメンタリーチャンネル）の制作エンジニアです。
リポジトリ: C:\Users\aab15\Documents\prime-documentary
Python: ./.venv/Scripts/python.exe

# 担当エピソード
EP40 / Episode ID: PD-2026-040-lech / slug: lech
題材: Lech v. Jackson, 791 F. App'x 711 (10th Cir. 2019), cert. denied (2020)
万引き犯が無関係の一家の家に立てこもり、警察が装甲車と爆薬でその家を全壊させたが、
Takings Clause の「police power」例外により、一家はほぼ何の補償も受けられなかった事件。

# 設計書（唯一の仕様。全て読んでから着手すること）
episodes/_planning/EP40_lech_DESIGN_and_CODEX_PROMPTS.v001.md

# ★★★ 最優先の絶対条件（違反したら他が完璧でも出荷不可）★★★
Lech v. Jackson は「最高裁判決」ではない。第10巡回区控訴裁判所の2019年の判断であり、
最高裁は2020年に上告を受理しなかった（cert. denied）だけで、中身の判断はしていない。
「最高裁が決めた / the Supreme Court ruled / upheld / held」と書いたら FAIL。
設計書 §0 の accuracy_lock（R1〜R5）を機械ゲートとして実装し、必ず通すこと。
「Supreme Court」は cert. denied を説明する文脈でのみ使用可。

# 台本の状態（重要）
台本は別プロセスで並行制作中。**あなたは台本本文を待たない。**
設計書 §4 に台本スロットの厳密な JSON 契約（lech_slots.v1）が定義してある。
台本が無い状態では §4.4 の stub を生成し、パイプライン全体を通しでドライランして
「動くこと」を実証すること。stub と本番でコードパスを分岐させてはならない。

# ★★★ 尺と語数の確定値（これを間違えると尺不足が再発する）★★★
2026-07-19 に31話分の実TTS音声を実測した結果に基づく確定値。
古い資料に出てくる「150 wpm」「173 wpm」「1,700〜1,950語」は **すべて誤り。使うな。**

  ナレーション速度        = 178.1 wpm（実測中央値。範囲 163.7–237.4）
  目標語数                = 2,140語
  許容band                = 2,048 – 2,226語
  設計総尺                = 741.4秒 = 12:21（band 690–750秒の内側）

背景: 過去38話中30話が目標尺に未達で出荷されている。EP38は1,675語で9.4分しかなかった。
原因は spec が wpm を更新したのに台本の語数が150wpm時代のまま据え置かれたこと。
声でも構成でもなく、語数の問題。

判定は `python scripts/check_script_length.py <script> --json` が唯一の正。
「だいたい12分ぶん書けた」という自己申告・体感による判断は禁止。
このゲートは preflight_render_gate.py の最初のチェックとして配線済みで、
TTSとレンダーに課金する前にブロックする。

水増し禁止: 言い換え反復・冗長な接続・無意味な間で語数を稼ぐと check_padding.py で FAIL する。
増やしてよいのは中身だけ（場面のディテール／二つ目の事例／その後の人生／反対意見の論理／
制度の仕組み／数字の出所）。

注意（2026-07-19 に本設計値でゲートを実行して確認した挙動）:
2,140語は PASS するが、ゲートは同時に「声が速い側（237.4wpm・williams/florenceで実発生）に
振れると9.0分になる」と警告を出す。これへの対処は**声のスピードを固定すること**であって、
語数を2,730語まで増やすことではない（増やすと中央値ペースで band 上限を突き抜ける）。
ナレ生成直後に必ず実尺を測り、9〜10分台なら編集に進む前に差し戻すこと。

# ★素材点数も2,140語＝12:21前提で積算し直してある（EP38の実績をそのまま流用するな）
  静止画 distinct     60枚（生成プールは132枚 = 22シーン×6）
  i2v                 16本
  factory実写クリップ  54本
  総カット数          226
  MGビート            36枠 = AEヒーロー8 + Remotion FigureBeats 28

  ゲート下限: factory ≥25本（30秒に1本）／ MGビート ≥2.5per分 かつ 種類3以上 ／
              静止画占有率 ≤45% ／ 5秒超の長止め ≤8箇所
  設計値の検算は設計書 §5.1.2 にある。必ず自分でも再計算して一致を確認すること。

# 今すぐ着手する作業（設計書 §10.1 の C1〜C11）
C1  episodes/PD-2026-040-lech/ のディレクトリと manifest.json を作成
    （target_duration_minutes: 12。既存 EP38/EP37 のディレクトリ構成に合わせる）
C3  remotion/src/compositions/LechThumbnails.tsx にサムネ3案を実装（設計書 §8）
    T1/T3 は今すぐ実装可。T2 は数値が検証待ちなのでレイアウトのみ用意。
    1280x720 の <Still> を3つ Root.tsx に登録。
C4  remotion/src/compositions/OpeningLech.tsx を実装（設計書 §7 の全仕様）
    - Composition id="OpeningLech" / 1920x1080 / fps=60 / durationInFrames=180
    - props: {title, subtitle, accent, hasLogo}
    - remotion/props/lech.json = {"title":"LECH","subtitle":"POLICE POWER","accent":"#E5B53A","hasLogo":true}
    - 設計書 §7.2 の秒数タイムライン、§7.3 のイージング数値表、§7.4 のレイヤー構成を
      **数値そのまま**実装すること。等速線形は1箇所も使わない。opacity単独の演出も禁止。
    - タイトルは @remotion/motion-blur の Trail(layers=6, lagInFrames=1.2, trailOpacity=0.45) で包む
    - 秒数は fps から算出（フレーム直書き禁止）。T定数を as const で定義
    - 下敷きの正典実装: C:\Users\aab15\Documents\pino-channel\remotion\src\Opening.tsx を読むこと
    - ★注意: 本編内のOPは Bookends.tsx の BrandOpening のまま変更しない（設計書 §7.0）。
      OpeningLech は独立したバンパー成果物であり、本編に焼き込まない。
C5  scripts/validate_lech_slots.py と scripts/make_lech_slots_stub.py（設計書 §4.2/§4.4）
C6  scripts/check_lech_accuracy.py（設計書 §0.3 の R1〜R5・BLOCKING）
C7  scripts/ae/build_lech_hero_jsx.py（設計書 §6）
    - 8ビートスロット（b01〜b08）/ 4レイアウト（CENTER_STACK, SPLIT_COMPARE, DATE_STAMP, RATIO_BAR）
    - 6カウント型（CT_INT, CT_MONEY, CT_MONEY_M, CT_PCT, CT_DATE, CT_COUNTDOWN）
    - beats.json を出力（設計書 §6.3 のスキーマ厳守）
    - ベースにする実証済み実装: scripts/ae/build_kfc_hero_jsx.py を必ず読むこと
C8  scripts/ae/composite_lech_hero.py（設計書 §6.7）
    - ベース: scripts/ae/composite_kfc_hero.py。SKIP 4条件を1つも削らない
    - 出力は lech_final_bgm.v003_ae.mp4。既存ファイルを絶対に上書きしない
C9  scripts/validate_lech_beats.py（設計書 §6.3 の不変条件7件）
    - AEの8区間と Remotion FigureBeats 28枠が1秒でも重ならないことも検査する（設計書 §6.10.2）
C10 stub で通しドライラン（出力は 08_edit/_dryrun/ 配下。本番ファイル名を使わない）
    - stubの figures[] は「区間とkindだけ本番と同一・テキストはマーカー」で作る。
      これによりMGビート密度ゲート（≥2.5per分）の通過を台本確定前に実証できる
C11 factory素材の選定（EP39 の stock_ledger と sha256 が重複するものを除外）
    - 選定本数は 54本（下限25本）。EP38実績の41本ではない

# 画像生成（C2）— GO が出るまで実行しない
設計書 §5.6 に S01〜S22 のプロンプトが確定済み（各6枚 = 132枚）。
共通スタイル接尾（§5.3）と共通ネガティブ（§5.4）を必ず全プロンプトに付ける。
保存先 H:\pd-media\assets\ai\lech\<SPN-ID>.png、長辺 3840px 以上。
**課金が発生する画像生成ジョブは、オーナーの明示的なGOがあるまで起動しないこと。**
今のフェーズではプロンプトファイルの用意までにとどめる。

# After Effects の罠（このマシン固有。設計書 §6.8 に全12件。必ず読む）
特に危険な5つ:
1. setTemporalEaseAtKey の配列次元は Position など spatial プロパティでは1個。
   dim = prop.isSpatial ? 1 : (value.length||1)。間違えるとイーズが無言で効かず等速になる
2. テンプレート名はローカライズ済み。RS="最良設定" / OM="H.264 - レンダリング設定を一致 - 15 Mbps"
3. app.newProject() は -noui でハングする。使うな。既存同名コンプを防御的に削除せよ
4. ビルドは遅い(~100-120s)がレンダは速い。render/_build_ok.txt をポーリングし、早期killしない
5. 2Dレイヤーの回転は "ADBE Rotate Z"（"ADBE Rotation" は null）。
   layer.motionBlur はレイヤー個別に設定が必要。画像は item.mainSource.conformFrameRate = 30 が必須

実行パス:
  AE: C:\Program Files\Adobe\Adobe After Effects 2026\Support Files\AfterFX.exe / aerender.exe
  ffmpeg: C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe
  ffprobe: C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffprobe.exe
  フォント: Anton.ttf / Oswald.ttf（C:\Users\aab15\AppData\Local\Microsoft\Windows\Fonts に実在確認済み）
  必ず psName() ランタイム解決を使い、無言のフォント置換を防ぐこと

# 絶対にやらないこと
- EP39（frazier）のファイルに一切触らない。素材・色・音のレーンも分離する（設計書 §2）
  EP39 = 取調室/夜/密室/electric blue #1F6BFF
  EP40 = 郊外の一軒家/昼/破壊/gold-amber #E5B53A
- 有料ジョブ（画像生成API・ElevenLabs TTS・YouTubeアップロード）を勝手に起動しない
- 公開済み・出荷済みの mp4 を上書き・再レンダリングしない
- 「最高裁が判断した」という趣旨の記述をどこにも書かない
- 設計書に無い数値を自分で決めない。不明な数値は beats.json の契約に従い
  facts[F-ID].verified=false として扱い、該当ビートを除外する
- 尺・語数・素材点数を「だいたいこのくらい」で決めない。上の確定値と設計書 §3.1 / §5.1 の
  検算をそのまま使う。自分で計算し直して合わなければ、実装ではなく設計書の側を疑って報告する

# 受入（自分で走らせて exit 0 を確認してから完了報告すること）
# ★語数ゲートが最初。TTSとレンダーに課金する前にここで落とす
./.venv/Scripts/python.exe scripts/check_script_length.py \
  episodes/PD-2026-040-lech/03_script/script.en.v003.md --json
./.venv/Scripts/python.exe scripts/check_padding.py --ep lech --json
./.venv/Scripts/python.exe scripts/check_lech_accuracy.py --json
./.venv/Scripts/python.exe scripts/validate_lech_slots.py
./.venv/Scripts/python.exe scripts/validate_lech_beats.py
./.venv/Scripts/python.exe scripts/preflight_render_gate.py --ep lech
# 台本・ナレ確定後:
./.venv/Scripts/python.exe scripts/check_final_acceptance.py 40 \
  --render episodes/PD-2026-040-lech/08_edit/lech_final_bgm.v003_ae.mp4 --emit-receipt

「動いたと思う」は完了ではない。ゲートが exit 0 を返して初めて完了。
自分でQC基準を書き換えて通すことは禁止。
```
### ★素材構成の是正（オーナー指摘「全て画像じゃなくてもいい。大量の素材があるからね」）

SDXL生成に寄せすぎていた。**実測した在庫（2026-07-19・`H:\pd-mediassets`）:**

| カテゴリ | 実測本数 | 使い方 |
|---|---|---|
| `factory/backgrounds` | **11,623** | 実写クリップ。**動いている**ので motion coverage に直接効く |
| `factory/light_assets` | 1,401 | 合成レイヤー（光） |
| `factory/particle_assets` | 1,225 | 合成レイヤー（粒子） |
| `factory/vfx_overlays` | 1,196 | 合成レイヤー |
| `factory/loops` | 454 | ループ素材 |
| `ai`（既存生成物） | 1,287 | 流用可 |
| `stock` | 235 | — |

**空のフォルダ（存在するが中身0）:** `diagram_assets` / `transitions` / `typography_assets` / `parallax_layers` / `lottie_assets` / `ai_video_shots` / `sfx`。図解・トランジション・タイポは**自作が必要**（Remotion/AE側の担当）。

**確定する素材構成（226カット / distinct 約155点）:**

| 種別 | distinct 点数 | 使用回数 | 調達 |
|---|---|---|---|
| SDXL静止画 | **60–70枚** | ≤2回 | 生成。**この作品にしか無い絵**だけに使う（主役の顔が映らない再現、固有の場所、象徴カット） |
| factory backgrounds | **80–90本** | **1回** | 在庫から選抜。空気・情景・質感・繋ぎ |
| i2v モーション | 15–20本 | ≤2回 | 上のSDXLから動きが意味を持つものを選んで生成 |
| 合成レイヤー（light/particle/vfx） | 随時 | — | **distinct素材に数えない。**静止画の上に重ねて「止まっていない」状態を作る |

**要点:** SDXL生成枠は120枚→**60–70枚に半減**させ、その分を無料の実写在庫（11,623本）で埋める。実写は動いているぶん `animation_mix` の motion coverage にも効くので、静止画を増やすより有利。合成レイヤー3,822点は**同じ静止画を別物に見せる**ために使う（反復対策として枚数を増やすより安い）。

**ただし実写選抜には必ず目視QCを通すこと。** EP36で「city_surveillance_camera_dome」という名のクリップが実際にはベオグラードの大聖堂だった、EP38で牛の映像が「documents_on_desk」というラベルで入っていた、という実例がある。**factoryのファイル名とサブタイプは信用できない。** `check_visual_asset_qc` のコンタクトシートで全点を目で見てから使うこと（80–90本ぶんの確認時間を工程に見込め）。

### ★シーン数の是正（オーナー指摘 2026-07-19「20枚じゃ足りない」）— 旧値を上書きする

**旧設計（20–22シーン × 5–6バリエーション）は不足。** 画像は110–132枚あっても、**視聴者が見る「別の被写体」は20種類しかない**。同じ取調室を6アングルで撮っても、観る側には同じ部屋。反復感の原因は総枚数ではなく**シーン数**。

**確定値: 48–50シーン × 2–3バリエーション = 生成プール 120–150枚。本編で使う distinct 静止画 = 約120枚。**

積算（226カット / 静止画が156カットを担当する前提）:

| 静止画 distinct | 1枚あたり使用回数 | 判定 |
|---|---|---|
| 39枚 | 4.0回 | 旧仕様の上限。**反復が露骨に見える** |
| 60枚（旧設計値） | 2.6回 | `check_asset_reuse` の上限2回を**超過＝FAIL** |
| 78枚 | 2.0回 | ゲート最低ライン |
| **120枚** | **1.3回** | **確定値。反復を実感させない水準** |
| 156枚 | 1.0回 | 完全に反復なし（余力があればここへ） |

**バリエーションは「同じ被写体の別アングル」ではなく、別の被写体を増やす方向に使うこと。** 1シーンあたり2–3枚に抑え、浮いた生成枠をシーン数に回す。オーナーはSDXLの大量生成を明示的に許可している（「複数の素材が必要ならSDXLで大量の素材を作って動かすのもあり」）ので、枚数をケチる理由はない。

**生成は冪等に。** 既存ファイルをスキップして再開できるバッチにし、中断しても作り直しにならないこと。強い絵から順に生成し、途中で止まっても使える状態を保て。
