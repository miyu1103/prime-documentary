# EP45 cleveland — 設計書＆Codex A/B 共有ブリーフ

> 単一の真実源。EP43/44 の同名ファイルを構造テンプレとして踏襲し、下記 EP45 差分で差し替える。ここに無い数値は SPEC JSON から転記。

## 0. 同定
- episode_id: `PD-2026-045-cleveland` / slug: `cleveland` / EP45
- 台本(確定): `episodes/_planning/EP45_cleveland_script.en.v001.md`（2,119語・median 11.9分）
- SPEC: `episodes/_planning/EP45_cleveland_PRODUCTION_SPEC.v001.json`
- タイトルA/B（≤60字・二人称・CTR・★"合法"と書かない）:
  - A: `Jailed for Being Too Poor to Pay a Fine. It's Unconstitutional.`
  - B: `The Supreme Court Banned Debtors' Prisons in 1983. This City Kept One.`

## 1. 1シーン1枚・バリエーション0
- still distinct を固有プロンプトで各1枚。--variants 1。ai_prompts still84＝84行＋i2v種16＝shots 100。factory 92本は在庫選抜。

## 2. SPEC 確定値（出典 SPEC JSON）
- narration 713.9s(11.9分)@178.1wpm / words 2,119 / 視覚シーン48 / 総カット**224** / 平均3.19s
- still **84 / 100 / 1.19x(cap2)** ／ factory **92 / 92 / 1.0x(cap1)** ／ motion(i2v) **16 / 32 / 2.0x(cap2)**
- distinct **192 / 224 = first-use 0.8571** ／ still-share **0.4464(cap0.45)** ／ motion coverage 0.553
- MG(FigureBeats)ビート floor **30**（AEカードは数えない）

## 3. ★正確性6制約（全出力に適用・違反はBLOCKER）
1. 「合法(legal/lawful)」と言わない。払えないだけの投獄は Bearden(1983)以降 憲法違反(違法)。主題は"違法なのに実務で続く(enforcement failure)"。「もう完全に無くなった」も誤り。
2. Bearden(1983)＝最高裁の線。Cleveland の救済は下級審の訴訟/和解(2014)であって最高裁判決でない。「最高裁が Cleveland を救った」と書かない。
3. Bearden の holding を正確に: 収監前に「支払い能力」と「代替手段」を検討する義務。Bearden は罰金・手数料そのものを禁じていない(「全罰金違憲」に過大化しない)。
4. Harriet Cleveland は R2(存命私人)。顔・肖像・身体を描かない。象徴のみ(督促状の束・停止された免許証・空の財布・裁判所廊下・留置場の扉・時計・バス停・支払台帳)。家庭・子どもを扇情化しない・尊厳をもって(poverty porn禁止)。
5. 制度・営利保護観察(JCS=Judicial Correction Services)を説明。特定個人を攻撃しない(判事Harringtonの公開判決の逐語引用は可)。
6. 数値(罰金$1,554/31日/$200月/$40がJCS/約38,000人4州)は原典一致・捏造ゼロ。confidence:medium のものはヘッジ維持。

## 4. ビジュアル方針
- レーン色(★EP41 gold/EP42 blue/EP43 amber/EP44 teal と区別): **EP45 accent = crimson `#B23A48`**(督促の朱)。INK `#0A0A0C`。CODEX_B は OP props/AEカード/サムネ accent を必ず #B23A48 に。
- 反復モチーフ: **督促状の束(輪ゴム)**・**停止された免許証(伏せ置き)**・**空の財布**・**留置場の扉/booking の時計**・**支払台帳・請求書(会社ロゴはぼかし)**・**裁判所の長い廊下**・**バス停(車社会の孤立)**・**空席の弁護人席**(counsel不在)。
- 人物は影/後ろ姿/手元/象徴のみ。顔なし。扇情化しない。
- Act別トーン: HOOK(督促の束・免許・空の財布・閉じる留置扉)／ACT1(最短・罰金の雪だるま→能力審査なしの収監)／ACT2(営利保護観察JCS・$40 skim・counsel不在)／ACT3(Bearden判例核・能力＋代替の義務・最も遅い)／ENDING(数字への回帰・違法なのに続く余韻・988でなく legal-aid/権利の一行を概要欄)。

## 5. 技術ゴッチャ（EP39-44の事故から）
- ★**dochighlight figure（黒バー/box/underline）を使わない**（バグに見える＝3回指摘）。figures[] に "kind":"dochighlight" を入れない(grepで0)。
- FigureBeats kind 全小文字。read_prompts 2行形式。--only S01 で shots=100 確認。
- film.json ビルダー `scripts/build_cleveland_film.py`(EP44 build_tekoh_film.py 複製・slug/EP/paths を cleveland に・実素材のみstub禁止)。
- ゲート入力 `--ep PD-2026-045-cleveland`。`--json` は出力→入力に使わない。
- asset_manifest は A↔B で counts/role enum/overlay枚数一字一致・role=thumb/still_thumb 不使用(サムネ=also_thumb 6枚)。
- durationInFrames 4項関数＋hookSeconds明示＋total≤750s assert。AEレイアウト名は実装済み集合のみ・DESIGN↔CODEX_B一字一致。正確性ゲート名 check_cleveland_facts.py に統一。composition id Ep45Cleveland。
- AE: フォント厳格解決・sourceRectAtTime実測・ローカライズOM/RS・.aep>.jsx assert。
- レンダ: `remotion render Ep45Cleveland ... --public-dir=public_slim`。完成後 build_cleveland_bgm(EP42 build_young_bgm_real 複製)→composite_cleveland_hero(EP42 複製・film_offset適用)→全ゲート＋全編アイボール。

## 6. AEヒーローカード（6-8枚・値は台帳照合・6制約順守）
- 候補: `$1,554 OR 31 DAYS`(裁判所命令) / `NO HEARING`(能力審査なし＝Bearden違反) / `BEARDEN v. GEORGIA · 1983`(date) / `"...ability to pay..."`(Bearden逐語 quote) / `$200 / $40 → JCS`(skim・compbars) / `~38,000 · 4 STATES`(JCS規模・"rolls across four states"の限定) / `UNCONSTITUTIONAL SINCE 1983`(＋サブ"yet it continued") / `SETTLED 2014`(下級審・最高裁でない旨サブ)。
- カード文言に「legal」「最高裁がClevelandを救った」を書かない。数値・引用は AE ledger 一致必須。

## 7. 完了条件
- DESIGN: 0〜713.9s全区間タイムライン・各アニメ数値明記・48シーン絵コンテ(象徴・6制約・扇情化なし)・FigureBeats設計(≥30・小文字kind・変種≥3・dochighlight不使用)・AEカード表(§6・accent #B23A48)・Composition設定(1920x1080/fps EP44同値/id=Ep45Cleveland/durationInFrames4項)。
- CODEX_A: ai_prompts 84本(1枚ずつ)＋i2v16＋factory92選定＆全点目視QC(select_cleveland_factory.py・--exclude-used --ep PD-2026-045-cleveland・EP39-44 sha256被り検証)＋asset_manifest(EP44同型・counts を EP45 値に)。★84本全部書く。
- CODEX_B: build_cleveland_film.py(実素材・dochighlight不使用)・captions・figures(小文字kind・MG≥30)・Root.tsx登録・AEカード(実測幅・ledger照合・accent #B23A48)・bgm→composite(film_offset適用)・レンダ・全ゲート(--ep・check_cleveland_facts.py)・全編アイボール。
- A↔B 接続点は asset_manifest.v001.json ただ1ファイル(スキーマ一字一致)。
