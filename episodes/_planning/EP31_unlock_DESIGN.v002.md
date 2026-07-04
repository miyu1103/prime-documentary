# EP31 制作設計書 v002 — "Can They Force Your Phone Open?"（スマホ強制解除）

**Episode ID:** `PD-2026-031-unlock`  ·  **slug:** `unlock`
**Series arc:** *Your Rights vs Their Power*（第4/第5修正＝あなたの権利 vs 公権力）
**Duration profile:** standard — target **12:00 (720s)**, band **690–750s**
**R-rating:** **R2**（実在の判例・実在の刑事被告を扱う。全て公開の裁判記録。判旨を中立に紹介し被告の犯罪内容には深入りしない＝fact_recheck の GUARDRAILS 厳守）
**Binding spec:** `docs/PD_ONE_PASS_PRODUCTION_SPEC.v2.md`（本設計書は§A表 rows 1–16 のインスタンス）／`docs/PD_WINNING_PATTERN.md`（北極星4指標）
**分担（2026-07-04オーナー確認）:** **Codex＝ヒーロー静止画＋サムネ背景の生成のみ**。台本・Remotion組み・編集・音声・字幕・書き出し・QC は**すべて Claude**。cf. `[[pd-division-of-labor]]`

> **v002での変更点（2026-07-05）**：v001設計から実制作を進めた結果を反映。①**台本をv002へ拡張**（v001ナレ実測8.4分＝バンド3分不足→+7スパン/計2,087語で**11.56分**＝バンド内）。②**新事実2件を追加**（国境・空港例外 FR-BORDER／再起動でパスコード強制 FR-BFU）。③**画像40→42枚**（国境ビート用 IMG-41/42 空港を追加）。④**ヒーロー42枚＋サムネ5枚を Codex生成済み**（3840×2160 / 1280×720）。⑤**ElevenLabs音声マスター生成済み**。本書が最新の正典（v001は履歴）。

**現在の到達状態:** `script_verified` 済 ＋ 音声マスター済 ＋ 画像済（＝残りは Claude の字幕・組み立て・書き出し・受領ゲート）。

---

## 0. ログライン / なぜ勝てるか

> 警察に車を停められ、「スマホを見せろ」と言われる。**あなたの顔は、指は、そのロックを勝手に開けてしまう。でも——頭の中の暗証番号は、開けさせられないかもしれない。** なぜ「顔」と「番号」で結論が真逆になるのか。そして、その答えは**州境を一歩越えるだけで変わる**——空港では、さらに弱くなる。

- **データ勝ち筋との一致**：`[[pd-analytics-findings]]` の実測トップ3が全て「警察 × あなたの権利 × スマホ（第4修正）」。本作はそのど真ん中。勝ちShort（`Warrant to Search Your Phone` 199再生）と地続き。
- **驚き（オーナー要望"驚き/学び"）**：「**パスコードは守られるのに、Face ID／指紋は守られない**」逆説。誰もが使う生体認証こそ法廷で一番弱い。
- **感情設計**：不安（他人事じゃない）→ 知的興奮（からくり）→ 当事者意識（決着はまだ・次はあなたの事件かも）＋**実践で一手取り戻せる**（再起動）。
- **悪役の安全性**：悪役は「未決着のグレーな法」。特定個人を貶めない＝名誉毀損リスク低。
- **入口ショート（別制作）**：`Police Can Force Your Face — But Not Your Passcode #Shorts`

> **オーナー厳命(2026-07-04)：見ごたえ最優先。「普通の情報提供」は禁止。** 抽象的な法解説を流さない。**「あなたが車を停められる」具体シーン**を起点に緊張・謎・反転・ペイオフで引く。**台本は最低3回レビュー（§10a・v002で再確認済）**。本題材は抽象度が高く**紙芝居化リスクが最大**＝§5のモーション設計を特に厳格に。

---

## 1. 事実の骨子（★=fact_recheck で verbatim 確定済。詳細は `EP31_unlock_fact_recheck.v001.md`）

米国憲法：**スマホの強制解除**を巡る第4修正（捜索）と第5修正（自己負罪拒否）の対立。**判例は一次確認済**。

- ★ **Riley v. California (2014)**：逮捕付随でも**中身を見るには令状**（全員一致）。＝「見る」権限と「開けさせる」権限は別。（FR-R）
- ★ 第5修正は「**供述的**」な強制だけを守る。**記憶した暗証番号＝供述的（守られやすい）**／**指紋・顔＝物理的（守られにくい）**。金庫の暗証番号vs鍵の比喩（Doe 1988）。（FR-T）
- ★ **Payne (9th Cir. 2024)**：指を押し当てての解除は違反でない。ただし「**どの指か選ばせたら別**」の留保あり。（FR-P）
- ★ **Brown (D.C. Cir. 2025)**：指紋解除は供述的＝違反（Payneと対立）。＝**生体も裁判所が割れる**。（FR-B）
- ★ **暗証番号**：守る側＝Pa. Davis(2019)/Ind. Seo(2020)/Utah Valdez(2023)。強制側＝N.J. Andrews(2020)/Ill. Sneed(2023)。分かれ目は foregone conclusion を「番号」か「データ」に当てるか。（FR-PC-prot/comp・FR-FC）
- ★ **最高裁は未判断**：Davis/Andrews/Sneed で上告不受理を繰り返し＋Valdez(2024/6/24 不受理)＝**州境で権利が変わる**。（FR-SC）
- ★ **【v002追加】国境・空港例外**：国境では令状なし捜索を主張、巡回で嫌疑水準が分裂、Smith(S.D.N.Y. 2023, Rakoff)が令状要と判断した初例だが未確定。（FR-BORDER）
- ★ **【v002追加】端末仕様の事実**：完全に電源を切って再起動した最初の解除は生体無効＝パスコード必須（iOS "Before First Unlock"／Android同様）。**法的助言でなく端末仕様の事実**。（FR-BFU）

> **不変項1/10/13：** ★は一次確認済。判旨は**中立**、被告の犯罪内容には**深入りしない**。「最高裁が決めた」等の断定は禁止（§fact_recheck の MYTHS）。

---

## 2. 4部構成 — 秒割タイムライン（fps=60 / 全長 ~715s / 数値は定数）

**実測（v002）**：ナレ音声マスター **693.8s（11.56分）**／実効179wpm／**2,087語・33スパン**。OP(3.5s)+ED(9s)込みで**最終 ≈ 706–715s＝band 690–750 内**。

| Part | 区間(s)概算 | 役割 | ナレ語数(≈179wpm) | v002追加ビート |
|---|---|---|---|---|
| **HOOK** | 0–8 | 夜の車内・顔スキャン・割れる地図。開く問い（最後に書く） | ~55w | — |
| **BrandOpening** | 8–11.5 | 金 `BrandOpening`（フックの後）。3.5s | 0（音楽） | — |
| **ACT I スマホ＝あなた** | ~11.5–190 | 中身の重さ／Riley＝令状は要る／"見る"と"開けさせる"は別 | ~560w | **SPN-0028** 最も親密な証人／**SPN-0032** 頻度で自分事化 |
| **ACT II 心 vs 体** | ~190–370 | 供述的の線引き／金庫vs鍵／暗証番号は守られ生体は守られにくい／Payne | ~590w | **SPN-0029** "指を選ばせたら別"留保 |
| **ACT III 割れている** | ~370–560 | Brown対立／州で真逆（地図）／foregone conclusion／**国境例外**／最高裁は逃げる | ~640w | **SPN-0033** 実例の人間の顔／**SPN-0021 国境・空港**／**SPN-0031** 沈黙への再フック |
| **ACT IV 未決の一線+ペイオフ** | ~560–697 | 実務の真実（番号＞顔・州次第）／**再起動で一手取り戻す**／フック回収／稼いだLikeへCTA | ~490w | **SPN-0030 再起動でパスコード強制（実践）** |
| **BrandEndcard** | 697–706 | `BrandEndcard`（CTA/cadence）。9s | 0 | — |

**リテンション（row16）**：フックの問い（開けさせられるのか）を**ラストまで開いたまま保持**。オープンループ「令状で"見る"ことはできる。だが"開けさせる"は別」を ACT I 末。**再フック ~2:30 ごと**（ACT境界＝新しい問い/反転／v002で SPN-0031 追加）。20秒超の平坦説明なし（法理は必ず"見せる/たとえる"）。

---

## 3. HOOK（0:00–0:08）— 最後に書く・ペイオフ検証済（row 9）

- **画**：4カット×~2.0s。①夜の車内で光るスマホ＋窓外の赤青（IMG-01）②センサーに押し当てる親指（IMG-14）③顔に走る青スキャン（IMG-15）④州境で2色に割れる合衆国地図（IMG-22）。
- **フック文（★暫定・SPN-0001）**：`The police can make your thumb open your phone. Your mind might be the only thing they can't touch.`（音声生成済）
- **ペイオフ**：ACT IV で「暗証番号＝頭の中＝守られやすい／顔・指＝守られにくい・州とその日次第」を回収（promise-payoff = true）。

---

## 4. FILM BIBLE（Academy 級・row 15/16）— 要点（詳細は `EP31_unlock_FILM_BIBLE.v002.md`）

- **コールドオープンの問い**：警察はあなたにスマホを**開けさせられる**のか。そして"顔"と"番号"でなぜ答えが違うのか。
- **三幕の上げ**：中身の重さ（ACT I）→ 心と体の線引き（ACT II）→ 割れる国と逃げる最高裁＋**国境**（ACT III）→ 未決の一線＋**実践で取り戻す**（ACT IV）。
- **人間の縦糸**：**"あなた"**（二人称）。特定被告でなく視聴者自身が主人公。
- **モチーフ**：**鍵 vs 金庫の暗証番号**／**光（覗く権力）と頭の中の暗がり（聖域）**／**割れる地図**（州で動く）＋**空港の検査台**（国境で弱まる）。
- **テーマ**：「**あなたの体は、あなたを裏切る。**」最後に残る自由は"沈黙"かもしれない——でも再起動で、その錠を自分の手で心に戻せる。

---

## 5. ビジュアル/アニメ・システム（row 8・`MotionSample.tsx` 準拠＝**紙芝居禁止**・本作は特に厳格）

**土台テンプレ**：`remotion/src/compositions/CaseFilm.tsx`（`data/unlock_film.json` 駆動）。承認済み `MotionSample` の作り。ショットリスト＝`EP31_unlock_shotlist.v002.json`（33ショット）。

- **カット**：平均 **2.5–3.0s**。ハードカット裸禁止＝**0.35s クロスディゾルブ**で重ねる。
- **静止画を動かす手法をローテーション**（同一連続禁止）：`bleed`(2.5Dパララックス)／`scan`(走査光)／`duotone`(ネイビー雰囲気)／`focus`(ラックフォーカス)／`motion_graphics`(比喩アニメ)。斜め"card"は稀のみ。
- **モーショングラフィックス（本作の主役級・法理を"見せる"）**：金庫vs鍵／割れる合衆国地図／foregone conclusion の断層（番号 or データで反転）／最高裁の扉が3回閉じる／**空港の検査台と国境ライン（v002）**／**電源オフ→パスコード復帰（v002）**。大型キネティックタイポ＋spring＋scale＋Trail。上部1/5レイヤー。`on_screen_text`/`visual_intent` を**必ず実装**。
  - **要注意（review_log申し送り）**：`SPN-0018`（foregone conclusion・~31s）が唯一"講義"に寄る危険区間。フォーク型キネティック図で必ず動かす（静止解説にしない）。
- **フッテージ（factory棚）**：夜の道路・パトランプ・法廷・**空港/検査台**・スマホ操作の手元。強め暗く＋ネイビー＋ビネット。
- **Runway（契約内・点で使用）**：フック冒頭 or ACT IV の1–2カットのみ。
- **禁止**：金の縦スイープ／黄・金の全画面ウォッシュ／ただのズーム・左右パン。`StyleTest` は手本にしない。

> **不変項11＋オーナー指示**：**匿名の人物OK**（車内の運転者・顔スキャン・法廷/空港の人＝匿名）。**禁じるのは実在本人・判事の肖像だけ**。**実機ロゴ・OS UI・企業商標は出さない**（抽象端末で描く）。factory棚＝権利クリア汎用のみ。

---

## 6. 素材プラン（row 7・**集めて未使用ゼロ**）

- **ヒーロー静止画（Codex生成・完了）**：**42枚**（IMG-01〜42／v002で国境用 IMG-41/42 空港を追加）。**生成済み 2026-07-05**、`H:\pd-media\episodes\PD-2026-031-unlock\05_visuals\selected\PD-2026-031-S###-IMG-0##.png`、**3840×2160**（長辺≥3840クリア）、匿名人物・実機ロゴ/OS UIなし。
- **密度**：`distinct_factory_used ≥ runtime/30` → **≥ 24 distinct クリップ**。単一クリップ再利用 **≤ 3回**（機械フロア≤4）。空スパン 0。
- **画像:フッテージ ≒ 4:6**。no-repeat（MIN_GAP~22）。**天秤等の汎用象徴 ≤2**（`footage_diversity`）。cf. `[[feedback_footage_diversity]]`。
- **factory 抽出テーマ**（`select_factory_assets.py --theme`）：`crime`（夜道/パトランプ/職質）, `legal`（法廷/ガベル/書類）, `tech`（スマホ操作/センサー/サーバ光）, `finance`（金庫）, **空港/国境**。cf. `[[reference_factory_shelf]]`。

---

## 7. OP/ED（row 14・**正典 Bookends・作り直さない**）

- `remotion/src/components/Bookends.tsx` の **`BrandOpening{seriesLabel,title,subtitle}` / `BrandEndcard{channel?,ctaLine?,cadenceLine?}`**（`OPENING_SEC=3.5` / `ENDCARD_SEC=9` 固定）。フォーク禁止（不変項14）。
- 金 `BrandOpening` は**フックの後**（8.0s〜）、`BrandEndcard` は末尾。
- `seriesLabel="Prime Documentary"` / `title="CAN THEY FORCE YOUR PHONE OPEN?"` / `subtitle="Your face, your thumb, your mind"`。
- **ED CTA（稼いだ Like・row10・SPN-0027）**：`If you just learned your passcode protects you more than your face — hit like, so more people know before it happens to them.`

### 7a. 音声エンディング（オーナー指示・row1関連）
- EDのBGMは**切りのいい終止**で無音着地。末尾9秒 `BrandEndcard` をアウトロ専用枠に、エンディング用キューを align-to-end 配置、1.5–2sクリーンフェード。**ナレ長・間は変えない**。ゲート＝`bgm_ending`＋末尾10秒耳チェック。

---

## 8. サムネ（rows 11–13・派手・CTR最優先・肖像なし）

> **CTR現状 2.31%（実測）→ 目標6%**（`docs/PD_WINNING_PATTERN.md`）。二人称の脅威1アイデア・320pxで可読を最優先。

**背景アート（Codex生成・完了）**：**5案 T1〜T5**、`H:\pd-media\episodes\PD-2026-031-unlock\10_thumbnail\backgrounds\PD-2026-031-THUMB-T#.png`、**1280×720**、文字なし（見出しはRemotion `<Still>` で載せる）。詳細は `EP31_unlock_thumb_prompts.v001.md`。

1. **`THEY CAN FORCE YOUR THUMB`**（T1）— 手錠の手が親指をセンサーへ。
2. **`FACE ID = NO RIGHTS?`**（T2）— 顔に走る青スキャン。
3. **`YOUR PASSCODE > FACE ID`**（T3）— 顔 vs 金庫ダイヤル、gold の不等号。
4. `YOUR PHONE. THEIR RULES.`（T4）／`THE MIND IS THE LAST LOCK`（T5）。

**selected（初期推奨）**：背景=T1／見出し=`THEY CAN FORCE YOUR THUMB`／タイトル=A。A/Bは T1×A と T3×`YOUR PASSCODE > FACE ID`×B。
タイトル（≤60字・フック先頭・A/B）：A `Police Can Force Your Thumb — But Maybe Not Your Mind` ／ B `Can the Police Force You to Unlock Your Phone?`

---

## 9. 通過必須ゲート（Done の定義・§D）

`./.venv/Scripts/python.exe scripts/check_final_acceptance.py 31 --json` が **exit 0**。ハードゲート（実ファイル測定）：
- `runtime_band` 690–750s / `render_resolution` ≥1920×1080 / `images_present` / `motion_present`（紙芝居検出）/ `bgm_present`（無音>25s なし・VO下 -22 LUFS 可聴）
- `voice_is_master`（ElevenLabs `nPczCjzI2devNBz1zQrb`・SAPI不可）/ `captions_final`（≥95%カバー）/ `caption_format`（1息継ぎ=1cue・≤42字/行・≤17cps）/ `caption_narration_match`（≥90%）
- `structure_4part`（HOOK→OPENING→body→ENDING＋`unlock_film.json` 実フック）/ `op_ed_bookends`
- `thumbnail_ready`（≥3×1280×720＋selected）/ `image_resolution`（長辺≥3840・**実測3840×2160で充足済**）/ `factory_used`（≥runtime/30）/ `footage_diversity`（distinct≥0.40・再利用≤4・汎用象徴≤2）

**手動実測（未コード化・飛ばさない）**：row5 画質・row12 サムネ派手/可読・row13 タイトル≤60/A-B・row15 film-bibleクラフト・**目視で失敗1〜9消滅**・**法的断定に MYTHS 混入なし**。

---

## 10. 工程ステータス（§B左工程ゲート・現況）

> 本作の分担：**Codex は 3 の画像生成のみ（完了）**。1・2・4・5・6 と Remotion 組み立て〜書き出し〜QC は**全部 Claude**。

| # | 成果物 | 状態 |
|---|---|---|
| 5 | `fact_recheck.v001`（R2・判例一次確認＋MYTHS/GUARDRAILS＋FR-BFU/BORDER） | ✅ 確定 |
| 1 | `FILM_BIBLE.v002` + `script.annotated.v002.json`（2,087語・4部・on_screen_text付） | ✅ 済 |
| 10a | 台本3パスレビュー（事実/クラフト/リテンション） | ✅ 全通過（`review_log.v001` v002追記） |
| 2 | `shotlist.v002.json`（33ショット・motion/keyword/AI対応） | ✅ 済 |
| 3 | `ai_prompts`（42枚）→ **Codex 画像生成** | ✅ **生成済**（42+サムネ5・3840×2160/1280×720） |
| 4 | `thumb_prompts.v001` + 見出し/A-B | ✅ 済 |
| — | **ElevenLabs 音声マスター v002**（11.56分） | ✅ 生成済（H:・非コミット） |
| 6 | `manifest.target_duration_minutes = 12` | ⏳ エピソード作業フォルダ本ブート時に設定 |

**残（Claude）**：①字幕＝音声マスターに息継ぎ単位で強制アライメント → ②Remotion組み立て（`CaseFilm`＋`unlock_film.json`・SPN-0018のmotion最優先）→ ③書き出し（libx264/CRF16）→ ④`check_final_acceptance.py 31` exit0 → 目視で失敗1〜9＋MYTHS点検 → first-cut / title-thumb / pre-publish の各オーナーゲート → `package_ready`。
