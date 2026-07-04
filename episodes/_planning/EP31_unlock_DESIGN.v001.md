# EP31 制作設計書 — "Can They Force Your Phone Open?"（スマホ強制解除）

**Episode ID:** `PD-2026-031-unlock`  ·  **slug:** `unlock`
**Series arc:** *Your Rights vs Their Power*（第4/第5修正＝あなたの権利 vs 公権力）
**Duration profile:** standard — target **12:00 (720s)**, band **690–750s**
**R-rating:** **R2**（実在の判例・実在の刑事被告を扱う。ただし全て公開の裁判記録。判旨を中立に紹介し、被告の犯罪内容には深入りしない＝fact_recheck の GUARDRAILS 厳守）
**Binding spec:** `docs/PD_ONE_PASS_PRODUCTION_SPEC.v2.md`（本設計書は§A表 rows 1–16 のインスタンス）／`docs/PD_WINNING_PATTERN.md`（北極星4指標）
**分担（2026-07-04オーナー確認）:** **Codex＝ヒーロー静止画＋サムネ背景の生成のみ**。台本・Remotion組み・編集・音声・字幕・書き出し・QC は**すべて Claude**。cf. `[[pd-division-of-labor]]`

---

## 0. ログライン / なぜ勝てるか

> 警察に車を停められ、「スマホを見せろ」と言われる。**あなたの顔は、指は、そのロックを勝手に開けてしまう。でも——頭の中の暗証番号は、開けさせられないかもしれない。** なぜ「顔」と「番号」で結論が真逆になるのか。そして、その答えは**州境を一歩越えるだけで変わる**。

- **データ勝ち筋との一致**：`[[pd-analytics-findings]]` の実測トップ3が全て「警察 × あなたの権利 × スマホ（第4修正）」。本作はその**ど真ん中**。既出の勝ちShort（`Warrant to Search Your Phone` 199再生）と地続きで、連動Shortも作りやすい。
- **驚き（オーナー要望"驚き/学び"）**：「**パスコードは守られるのに、Face ID／指紋は守られない**」という逆説。誰もが使っている生体認証こそ、法廷では一番弱い——という反直感が強フック。
- **感情設計**：不安（他人事じゃない）→ 知的興奮（からくりが分かる）→ 当事者意識（決着はまだ・次はあなたの事件かも）。
- **悪役の安全性**：悪役は「未決着のグレーな法」そのもの。特定個人を貶めないので名誉毀損リスク低。
- **入口ショート（別制作）**：`Police Can Force Your Face — But Not Your Passcode #Shorts`

> **オーナー厳命(2026-07-04)：見ごたえ最優先。「普通の情報提供」は禁止。** 抽象的な法解説をそのまま流さない。**「あなたが車を停められる」具体シーン**を起点に、緊張・謎・反転・ペイオフで引く（row15/16 を満たさない台本は不合格）。**台本は最低3回レビュー（§10a）**。本題材は抽象度が高く**紙芝居化リスクが最大**＝§5のモーション設計を特に厳格に。

---

## 1. 事実の骨子（★=fact_recheck で verbatim 確定。詳細は `EP31_unlock_fact_recheck.v001.md`）

米国憲法：**スマホの強制解除**を巡る第4修正（捜索）と第5修正（自己負罪拒否）の対立。

- ★ **Riley v. California (2014)**：逮捕に伴う捜索でも、**スマホの中身を見るには令状が必要**（全員一致）。＝ただし「**見る**権限」と「**開けさせる**権限」は別問題。
- ★ 第5修正は「**供述的（testimonial＝頭の中の中身を明かす）**」な強制だけを守る。**記憶した暗証番号＝供述的（＝守られやすい）**／**指紋・顔＝物理的な行為で"頭の中"を明かさない＝守られにくい**（金庫の「暗証番号」は言わなくてよいが「鍵」は渡せ、の比喩）。
- ★ **United States v. Payne (9th Cir. 2024)**：警察が**指を押し当てて解除**させたのは第5修正**違反ではない**（供述的でない）。ただし判決自身が「**どの指か本人に選ばせていたら結論は違ったかも**」と留保。
- ★ **United States v. Brown (D.C. Cir. 2025)**：**指紋解除は供述的＝違反**と逆の結論。＝**生体認証も裁判所が割れている**。
- ★ **暗証番号**：守られる側＝Pa. *Davis*(2019)/Ind. *Seo*(2020)/Utah *Valdez*(2023)。強制できる側＝N.J. *Andrews*(2020)/Ill. *Sneed*(2023)。分かれ目は「**foregone conclusion（既知の結論）**」法理を**番号そのもの**に当てるか**中のデータ**に当てるか。
- ★ **最高裁は決着させていない**：Davis / Andrews / Sneed で**上告不受理を繰り返し**、統一ルールなし＝**州境で権利が変わる**。

> **不変項1/10/13：** 上記★はすべて公開判例から**逐語ロック**するまで本文化しない。**判旨は中立に**紹介し、各事件の被告の犯罪内容（児童ポルノ・薬物等）には**深入りしない**（誤導・不要な印象操作を避ける）。「最高裁が決めた」等の断定は禁止（§fact_recheck の MYTHS）。

---

## 2. 4部構成 — 秒割タイムライン（fps=60 / 全長 720s / 数値は定数）

| Part | 区間(s) | 尺 | 役割 | ナレ語数(≈173wpm) |
|---|---|---|---|---|
| **HOOK** | 0.0–8.0 | 8.0s | フラッシュフォワード：夜の車内・窓を叩く光・顔スキャン・割れる合衆国地図。開く問い | ~23w |
| **BrandOpening** | 8.0–11.5 | 3.5s (`OPENING_SEC`) | 金の `BrandOpening`（フックの後）。シリーズ名+タイトル | 0（音楽のみ） |
| **ACT I スマホ＝あなた** | 11.5–~180 | ~2.8min | 中身の重さ／Riley＝令状は要る／**だが"見る"と"開けさせる"は別** | ~480w |
| **ACT II 心 vs 体** | ~180–~360 | ~3.0min | 第5修正の"供述的"／暗証番号＝守られる・生体＝守られにくい／Payne の強制指紋 | ~520w |
| **ACT III アメリカは割れている** | ~360–~560 | ~3.3min | 州で真逆（地図）／foregone conclusion の断層／Brown で生体も対立／最高裁は逃げ続ける | ~575w |
| **ACT IV 未決の一線+ペイオフ** | ~560–711 | ~2.5min | 実務の真実（番号＞顔・ただし州次第）／**フック回収**／「次に決めるのはあなたの事件かも」／稼いだLikeへCTA | ~430w |
| **BrandEndcard** | 711–720 | 9.0s (`ENDCARD_SEC`) | `BrandEndcard`（CTA/cadence）。末尾 | 0 |

**ナレ合計 ≈ 2,030w**（10.5–11分の実音声）。実測後に語数を band 内へ微調整。
**リテンション（row16）**：フックの問い（**開けさせられるのか？**）を**ラストまで開いたまま保持**。オープンループ「令状で"見る"ことはできる。だが、あなた自身に"開けさせる"となると——話は一変する」を ACT I 末で。**再フックを ~2:30 ごと**（ACT境界＝新しい問い/反転）。20秒を超える平坦説明を作らない（法理は必ず"見せる/たとえる"で動かす）。

---

## 3. HOOK（0:00–0:08）— 最後に書く・ペイオフ検証必須（row 9）

- **画**：4カット×~2.0s のパンチ編集（本編の最強ビート先出し）。
  1) 夜の車内、助手席に伏せて光るスマホ、窓の外で回る赤青の光（フッテージ＋Codex静止画、暗め＋ネイビー）
  2) センサーに押し当てられる親指のマクロ（ロックが解ける瞬間の光）
  3) 顔に走る青いスキャングリッド（モーショングラフィックス）
  4) 合衆国の地図が州境でパキッと**2色に割れる**（キネティック地図・"守られる州/守られない州"）
- **フック文（★暫定・確定は台本ロック時）**：`The police can make your thumb open your phone. Your mind might be the only thing they can't touch.`
- **ペイオフ**：ACT IV で「暗証番号＝頭の中＝守られやすい／顔・指＝守られにくい・ただし州とその日次第」を明確に回収（promise-payoff QC = true）。

---

## 4. FILM BIBLE（Academy 級・row 15/16）— 要点（詳細は `EP31_unlock_FILM_BIBLE.v001.md`）

- **コールドオープンの問い**：警察はあなたにスマホを**開けさせられる**のか。**そして"顔"と"番号"でなぜ答えが違うのか。**
- **三幕の上げ**：中身の重さ（ACT I：スマホ＝人生の全部）→ 心と体の線引き（ACT II：頭の中だけが聖域）→ 割れる国と逃げる最高裁（ACT III：あなたの権利は州境で変わる）→ 未決の一線（ACT IV：決めるのは次の"あなた"かも）。
- **人間の縦糸**：**"あなた"**（二人称）。特定被告でなく、視聴者自身を主人公にする。
- **モチーフ**：**鍵 vs 金庫の暗証番号**（渡せる鍵＝生体、明かさなくていい番号＝記憶）。**光（覗く権力）と、頭の中の"暗がり"（唯一の聖域）**。**割れる地図**（一線が州で動く）。
- **ナレの節度**：法律用語を最小限に、比喩と具体で。断定は事実(★)のみ。
- **テーマ**：「**あなたの体は、あなたを裏切る。**」——顔も指も差し出させられる時代に、最後に残る自由は"沈黙"かもしれない、という問い。

---

## 5. ビジュアル/アニメ・システム（row 8・`MotionSample.tsx` 準拠＝**紙芝居禁止**・本作は特に厳格）

**土台テンプレ**：`remotion/src/compositions/CaseFilm.tsx`（`data/unlock_film.json` 駆動）。承認済み `MotionSample` の作り。

- **カット**：平均 **2.5–3.0s**（速いテンポ・常に画が変化）。ハードカット裸禁止＝**0.35s クロスディゾルブ**でシーケンスを重ねる（1フレーム黒/ジャンプを作らない）。
- **静止画（Codex生成）を動かす手法をローテーション**（同一手法の連続禁止）：
  - `bleed`＝2.5Dパララックス（手前=スマホ/親指、背景=夜の街を別速度）
  - `scan`＝走査光/微グリッド（顔スキャン・書類・地図の情報系質感）
  - `duotone`＝ネイビー基調の雰囲気ショット（車内・法廷）
  - `focus`＝ラックフォーカス送り（親指→画面、番号パッド→目）
  - 斜め2.5D "card" は**稀に**のみ。
- **モーショングラフィックス（本作の主役級・法理を"見せる"）**：
  - **金庫 vs 鍵**の比喩アニメ（暗証番号＝閉じた金庫の中／指紋＝手渡しできる鍵）。
  - **割れる合衆国地図**：州が2色に分岐（守られる/強制できる）。Pa/In/Ut ↔ NJ/Il を**点で立てる**（★確定後、州名ラベルは on-image テキスト回避のため Remotion 側で載せる）。
  - **"foregone conclusion" の断層線**：分かれ目が「番号 or データ」で結論が反転する図。
  - **上告不受理の連打**：最高裁の扉が3回閉じるモーション（Davis/Andrews/Sneed）。
  - すべて**大型キネティックタイポ＋spring＋scale＋Trailモーションブラー**、上部1/5レイヤー（下部字幕と別）。`script.annotated` の `on_screen_text`/`visual_intent` を**必ず実装**。
- **フッテージ（factory棚）**：夜の道路・パトランプ・法廷・スマホ操作の手元。**強め暗く＋ネイビー寄せ＋ビネット**で統一。featureless クリップ除外。
- **オーバーレイ**：フィルムグレイン／画面の青いにじみ／揺らぐ照明を薄く常時。
- **Runway（契約内・点で使用）**：フック冒頭 or ACT IV の決定的1–2カットのみ img2vid。使いすぎない。
- **禁止エフェクト**：金の縦スイープ（`WipeTransition`）／黄・金の全画面ウォッシュ・フラッシュ／ただのズーム・左右パン（`CameraRig`）。`StyleTest` は手本にしない。

> **不変項11＋オーナー指示(2026-07-04)**：**匿名の人物の姿はOK**（車内の運転者、顔スキャンされる人、法廷に並ぶ所有者＝匿名）。むしろ人を映して画面を生かす。**禁じるのは実在・特定できる本人の肖像だけ**（実在被告・判事の顔の再現）。**実在のスマホ機種ロゴ・OS UI・企業商標は出さない**（抽象化した端末/パッド/センサーで描く）。実写の本人アーカイブは権利未クリアで不使用（factory棚＝権利クリア汎用のみ）。

---

## 6. 素材プラン（row 7・**集めて未使用ゼロ**）

- **密度**：`distinct_factory_used ≥ runtime/30` → **≥ 24 distinct クリップ**。単一クリップ再利用 **≤ 3回**（機械フロアは≤4）。空スパン 0。
- **画像:フッテージ ≒ 4:6**。全素材を no-repeat（MIN_GAP~22）で散らす。**天秤等の汎用象徴は ≤2**（`footage_diversity`）。cf. `[[feedback_footage_diversity]]`。
- **factory 抽出テーマ**（`select_factory_assets.py --theme`）：`crime`（夜の道路/パトランプ/職務質問）, `legal`（法廷/ガベル/書類/最高裁の外観）, `tech`（スマホ操作の手元/センサー/サーバの光）, `finance`（金庫）。cf. `[[reference_factory_shelf]]`。
- **Codex 生成ヒーロー静止画**（`ai_prompts.v001`・**計40枚**・1画像=1プロンプト・長辺≥3840・**匿名人物OK/実在本人・実機ロゴなし**）：夜の車内で光るスマホ／センサーに押し当てる親指／顔に走る青スキャン／閉じた金庫と手渡しの鍵／数字パッドと目のラックフォーカス／並ぶ所有者の待合／閉じる最高裁の扉／2色に割れる地図の質感。各プロンプトに negative（specific real person / celebrity / judge likeness, brand logo, phone-OS UI, on-image text, bad anatomy…）と upscale≥3840 を明記。

---

## 7. OP/ED（row 14・**正典 Bookends・作り直さない**）

- `remotion/src/components/Bookends.tsx` の **`BrandOpening{seriesLabel,title,subtitle}` / `BrandEndcard{channel?,ctaLine?,cadenceLine?}`** を import（`OPENING_SEC=3.5` / `ENDCARD_SEC=9` 固定）。フォーク禁止（不変項14）。
- 金 `BrandOpening` は**フックの後**（8.0s〜）に着地、`BrandEndcard` は末尾。
- `seriesLabel="Prime Documentary"` / `title="CAN THEY FORCE YOUR PHONE OPEN?"`（短縮）/ `subtitle="Your face, your thumb, your mind"`。
- **ED CTA（稼いだ Like・row10）**：`If you just learned your passcode protects you more than your face — hit like, so more people know before it happens to them.`（汎用のお願いにしない）。

### 7a. 音声エンディング（オーナー指示2026-07-04・row1関連）
- EDのBGMは**切りのいい終止**で終わる。末尾9秒 `BrandEndcard` をアウトロ専用枠に。
- エンディング用キュー（自然に解決する曲）を **align-to-end 配置**（ループを途中でブツ切りしない）。最後は拍/終止に合わせ**1.5–2sのクリーンフェードで無音着地**。
- **ナレ長・間は一切変えない**（尺は台本が主）。ゲート＝`bgm_ending`＋末尾10秒の耳チェック。

---

## 8. サムネ（rows 11–13・派手・CTR最優先・肖像なし）3案

> **CTR現状 2.31%（実測）→ 目標6%**（`docs/PD_WINNING_PATTERN.md`）。二人称の脅威1アイデア・320pxで可読を最優先。

全案：1280×720、UPPERCASE ≤4語、巨大主題、超高コントラスト、黒/ネイビー背景＋**gold `#E5B53A` or electric `#1F6BFF`**、白/銀文字。Codex で背景アート事前生成、`selected` を1つ。詳細は `EP31_unlock_thumb_prompts.v001.md`。

1. **`THEY CAN FORCE YOUR THUMB`** — 手錠の手が親指をスマホのセンサーへ押し当て、画面が青く光る。
2. **`FACE ID = NO RIGHTS?`** — 顔に走る青スキャングリッド、片側に大きな余白。
3. **`YOUR PASSCODE > FACE ID`** — 左に光る顔、右に閉じた金庫のダイヤル、gold の不等号。

タイトル（≤60字・フック先頭・A/B 2案）：
- A `Police Can Force Your Thumb — But Maybe Not Your Mind`
- B `Can the Police Force You to Unlock Your Phone?`

---

## 9. 通過必須ゲート（Done の定義・§D）

`./.venv/Scripts/python.exe scripts/check_final_acceptance.py 31 --json` が **exit 0**。ハードゲート（実ファイル測定）：
- `runtime_band` 690–750s / `render_resolution` ≥1920×1080 / `images_present`（黒過多なし）/ `motion_present`（freeze なし＝紙芝居検出）/ `bgm_present`（無音>25s なし・VO下も可聴フロア -22 LUFS）
- `voice_is_master`（ElevenLabs `VOICE_ID=nPczCjzI2devNBz1zQrb`・SAPI不可）/ `captions_final`（≥95%カバー）/ `caption_format`（1息継ぎ=1cue・≤42字/行・≤17cps）
- `caption_narration_match`：焼き込み字幕 ↔ narration `spoken_text` トークン一致 **≥90%**
- `structure_4part`：narration が **HOOK→OPENING→body→ENDING**＋`unlock_film.json` に実フック（hookSeconds≥5・hookLine非空）
- `op_ed_bookends`：正典 `BrandOpening`+`BrandEndcard` を使用
- `thumbnail_ready`（≥3×1280×720＋selected）/ `image_resolution`（長辺≥3840）/ `factory_used`（≥runtime/30 かつ参照）/ `footage_diversity`（distinct≥0.40・再利用≤4・汎用象徴≤2）

**手動実測（未コード化・飛ばさない）**：row5 画質/sharpness・row12 サムネ派手/可読・row13 タイトル≤60/A-B・row15 film-bible クラフト・**目視で失敗1〜9が消えたか**（MotionSample と並べて見比べ／on_screen_text 全実装確認）・**法的断定に MYTHS 混入なし**（§fact_recheck）。

---

## 10. Codex 前に Claude がロックする成果物（§B・左工程ゲート）

> 本作の分担：**Codex は 3 の画像生成のみ**。1・2・4・5・6 と、その後の Remotion 組み立て〜書き出し〜QC は**全部 Claude**。

1. `EP31_unlock_FILM_BIBLE.v001` + `script.annotated.v001.json`（Academy級・フック最後・4部ロール・語数173wpm band・`on_screen_text`/`visual_intent` 付き）
   - **§10a 台本レビュー＝最低3パス（オーナー指示2026-07-04・全パス通過まで先へ進めない）**：
     - **Pass 1 — 事実/因果(R2)**：全★を出典で逐語ロック・判旨を中立化・存命人物/被告の扱いを法務チェック・**「最高裁が決めた」等の MYTHS ゼロ**・捏造ゼロ。
     - **Pass 2 — ドラマ/クラフト(row15)**：コールドオープンの問い→三幕の上げ→ペイオフ。**「普通の情報提供（法解説）」になっていないか**を1文ずつ点検し、平板箇所を"あなた"の具体シーン/比喩に書き直す。
     - **Pass 3 — リテンション/字幕(row16)**：再フック~2:30ごと・20秒超の平坦なし・オープンループ回収・語数173wpm band・**息継ぎ単位で字幕分割**できる文か。
2. `shotlist.v001.json`（全スパン：asset_type+motion+transition+factory `search_keywords`・平均≤6s・0.35s クロスフェード・法理カットは motion-graphics 指定）
3. `ai_prompts.v001`（1画像1プロンプト・肖像/実機ロゴなし・≥3840）← **Codex 生成対象**
4. `thumb_prompts.v001` + 見出し/キッカー候補
5. **`fact_recheck.v001`（R2）**：★の判例名・年・裁判所・判旨・上告不受理を逐語ロック＋ MYTHS/GUARDRAILS
6. `manifest.target_duration_minutes = 12`（standard band）

> **順序**：まず **fact_recheck（R2）** で★を確定 → FILM_BIBLE/script（3パスレビュー）→ shotlist/prompts → **Codex 画像生成** → **Remotion 組み立て（Claude）** → acceptance exit0 →**目視で失敗1〜9消滅＋MYTHS点検** → first-cut / title-thumb / pre-publish の各オーナーゲート → `package_ready`。**1本ずつ**。
