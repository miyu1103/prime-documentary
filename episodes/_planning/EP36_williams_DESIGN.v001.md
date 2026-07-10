# EP36 「THE ALGORITHM SAID IT WAS YOU.」— 動画設計書 v001
**Episode:** PD-2026-036-williams · **Risk:** R2 · **Runtime target:** 11.5–12.5 min (standard) · **状態:** script_verified
**正典参照:** `docs/PD_ONE_PASS_PRODUCTION_SPEC.v2.md`(拘束) / OP・ED正典=`remotion/src/components/Bookends.tsx`(**invariant 14 = 作り直さない**) / モーション文法=`docs/motion-design-language.md` / モーション部品=`remotion/src/components/motionkit/CATALOG.md`
**この設計書の約束:** 抽象語で逃げない。要素・方向・秒数・イージング種別・移動量・damping/stiffness を数値で書く。等速線形は禁止。opacity単独禁止。速い動きは `@remotion/motion-blur` の `Trail`。主役の裏に最低3レイヤー。テキストは `overflow:hidden`＋`translateY` のマスク切れ上がり。秒は fps から算出（フレーム直書き禁止）。

---

## §0. 環境・Remotion設定（正典に一致・新規設定を作らない）
- **Composition:** `fps=30`, `width=1920`, `height=1080`（`remotion/src/brand.ts` の `BRAND.video`）。長尺エンジン=`CaseFilm`。`durationInFrames = caseFilmDurationInFrames(data, fps)`（= hook + OPENING_SEC + body + ENDCARD_SEC）。
- **依存パッケージ（既存・追加インストール不要）:** `remotion@^4`, `@remotion/cli`, `@remotion/motion-blur`（Trail）, `@remotion/three`＋`@react-three/fiber`＋`three`（3Dヒーロー）。**新規に npm i するものは無い**（正典部品で足りる）。
- **`remotion/remotion.config.ts`（既存・変更しない）:** `png` 中間フレーム / `h264`(libx264 CPU) / `crf=16` / `x264Preset=slow` / `pixelFormat=yuv420p` / `colorSpace=bt709` / `aac 320k` / `concurrency=os.cpus().length` / `gl=angle`（motion-blur/glow/gradient安定化）。**NVENCへ切替えない**（品質最優先・メモリ project_render_quality_first）。
- **重量WebGL/3Dのみ** `--concurrency=4 --gl=angle` で ~3000フレーム分割レンダ→無損失concat（`render_rolin_chunked.sh` パターン）。
- **ブランドトークン（`brand.ts`・唯一のソース）:** ink `#0A0A0C` / navy `#0B1A2B` / electric `#1F6BFF` / gold `#E5B53A` / white `#F5F7FA` / silver `#C8CDD6`。display=Impact系, body=Trebuchet系。
- **EP36アクセントの扱い:** 本編（本体）モチーフ＝**顔スキャンの cyan（`BRAND.color.electric #1F6BFF` を基調）× 冷たいスレート**。ただし **OP/ED は正典ゴールド固定**（§7）。cyan は本体レイヤーだけに使う（OP/EDのゴールドは変えない＝invariant 14＋メモリ feedback_opening_ending_taste「深海シアン独自OPは未採用／既存テイストのブラッシュアップのみ」）。

---

## §1. 事実の骨子（`claims.v001.json` に固定・逐語）
| # | 事実 | grade | claim |
|---|---|---|---|
| 1 | 無実の父が2020年1月、自宅ドライブウェイで妻子の前で逮捕・約30時間拘束 | A | CLM-0001 |
| 2 | 唯一の根拠は顔認識「一致」。他に証拠なし。釈放・起訴取下げ・検察が非を認める | A | CLM-0002 |
| 3 | 発端は2018年の時計店(Shinola)窃盗。報道で約$3,800/約5個（**B級→ナレのみ・画面焼き禁止**） | B | CLM-0003 |
| 4 | ぼやけた防犯写真→顔認識ソフト(DataWorks Plus)→州の免許/前科DB→古い免許写真が一致→動画しか見ていない店舗委託者にラインナップ提示 | A | CLM-0004 |
| 5 | NIST(2019)：偽陽性がアジア系/アフリカ系で白人の10〜100倍。1対多で黒人女性最悪。**反証=アジア製アルゴリズムは差が消える（学習データ問題）＝必須** | A | CLM-0005 |
| 6 | Gender Shades(2018)：性別分類（**別タスク**）で肌の濃い女性最大34.7% vs 薄い男性0.8% | A | CLM-0006 |
| 7 | 顔一致は「捜査の手がかり」に過ぎない（2024和解が明文化） | A | CLM-0007 |
| 8 | 2021年4月 ACLU等が市を提訴 | A | CLM-0008 |
| 9 | 2024年6月和解：一致のみでの逮捕禁止/手がかり限定/2017年以降の全件監査/裁判所4年監督 | A | CLM-0009 |
| 10 | 和解金 約$300,000（**B級→ナレのみ・画面焼き禁止**） | B | CLM-0010 |
| 11 | 「公に報じられた**最初**」＝時系列の最初ではない（Oliver/Parksが先）。**"first ever"禁止** | A | CLM-0011 |
| 12 | 最後でもない：妊娠8ヶ月の女性含む。ACLU集計「a dozen超」（**集計はB級→ナレ帰属**） | A/B | CLM-0012 |
| 13 | ガードレール（肖像禁止/生成物を本物扱いしない/officer名指し禁止/人種差は測定値＋反証） | A | CLM-0013 |

---

## §2. 4部構成 秒割タイムライン（fps=30・正典スパイン hook→OPENING→body→ending）
| 区間 | 秒 | フレーム | 中身 | 部品 |
|---|---|---|---|---|
| **HOOK** | 0:00–0:08 | 0–240 | 脅威コールドオープン（19語VO）＋ぼやけ写真→ドア | `CaseFilm` hook層（`data.hook[]`） |
| **OPENING** | 0:08–0:11.5 | 240–345 | 正典ブックエンド・タイトルカード（**OPENING_SEC=3.5s**・**フックの後**） | `BrandOpening{seriesLabel,title,subtitle}`（§7） |
| **BODY** | 0:11.5–≈11:55 | 345–… | ACT I–IV（16 span・§5の運動設計で駆動） | `CaseFilm` body（`data.cuts[]`） |
| **ENDING** | 末尾 9.0s | | 正典エンドカード＋CTA＋次回ループ（終語="next"） | `BrandEndcard`（固定） |
- OPENINGのVO（命題）はタイトルカードの上に被せる。タイトルカード自体の**視覚アニメは3.5s**で完結し、以降は本体モチーフ背景に溶ける。
- ED は全話共通・不変（`BrandEndcard` デフォルト：`▶ SUBSCRIBE — LANDMARK RIGHTS CASES` / `New episodes every week`）。尺は切りよく（メモリ feedback_pd_craft_directives「EDのBGMは切りよく」）。

---

## §3. HOOK（最後に書く・約束→回収）
- 19語・約7.1s（ship-gate `HOOK_MAX_S=8.0` 内）。VO＝「A blurry photo. A computer's guess. A knock at your door — arrested for a crime you did not commit.」
- 視覚：低解像の防犯フレーム（暗い帽子の人物・**意図的に判読不能な再現**＝本物のexport扱い禁止）が郊外のドアへ収束。顔なし匿名。
- 約束＝「機械の一致だけで逮捕される」→ ACT II で回収。SFXシャッター＋2ノック＋sub。

---

## §4. FILM BIBLE（アカデミー級クラフト・要点）
- **スパイン:** 普通の父（＝視聴者の分身）× 見えないアルゴリズム。コールドオープンの問い「なぜ彼が？」→中盤で「なぜ"彼のような顔"が？」に格上げ→測定された偏りで回収→「次はあなたの顔」で個人化。
- **モチーフ:** 「顔＝変えられないパスワード」。ぼやけフレームがフック→ED で"ひとつの匿名の顔"に解像して閉じる（ブックエンド）。
- **turn:** ①ドライブウェイ逮捕 ②「A computer did」 ③循環ラインナップ ④NIST 10–100倍 ⑤「あなたも登録済み」 ⑥和解＝一都市のみ ⑦最初でも最後でもない。
- **R2中立:** 機関は事実記述、officer名指し無し、人種差は測定値＋アジア製反証、生成物は再現であって証拠でない。

---

## §5. ビジュアル / アニメ・システム（本体・数値指定／紙芝居禁止）
**原則（全カット共通・root CLAUDE.md品質規則をコードで満たす）**
1. **全モーションにイージング。** `spring`（damping/stiffness/mass指定）または `Easing.out(Easing.cubic)` / `Easing.inOut(Easing.sin)`。**等速線形 interpolate 禁止**（背景ドリフト等も `Easing.inOut(Easing.sin)` を付ける）。
2. **opacity単独禁止。** 出現は必ず `translateY`(16–120px or %) か `scale`(0.55–1.18) と併用。
3. **複数要素はスタッガー。** 文字=0.03–0.06s／要素=0.08–0.15s ずつディレイ。
4. **速い動きに `Trail`。** タイトル切れ上がり・キネティック字幕・数字ティッカー・スキャン線に `<Trail layers={6–7} lagInFrames={1.2–1.5} trailOpacity={0.4–0.45}>`。
5. **主役の裏に最低3レイヤー。** 例：`AuroraField`/冷スレートのグラデ背景 ＋ `GridWarp`（顔スキャン・データグリッド）＋ `SoftGlow`/`LightRays`（cyanグロー）。
6. **テキストはマスク切れ上がり。** `<span overflow:hidden><span translateY(110%→0)>`。字幕は `KineticCaptions` の `maskslide`（既存・二重実装禁止）。
7. **秒→フレームは `f=(s)=>Math.round(s*fps)`。** 数値は定数化。

**部品は motionkit を流用（invariant 14・`CATALOG.md` を先に見る）**
| 用途 | 部品 | 備考 |
|---|---|---|
| 顔一致グリッド | `motionkit/…` グリッド＋`DepthParticles` | 匿名ポートレート枠のみ。UI/実在顔を焼かない |
| 類似度メーター | `NumberTicker`（既存・damping付き上昇） | 0→スコア。数値は装飾（実測値ではない） |
| 偏りバーチャート | `motionkit` バー＋`YearSweep` | 2本・広いギャップ。`10–100× / NIST 2019` はキネティック型 |
| 2018→2020→2024 年表 | `YearSweep`＋`KineticType` | grade-A の年号のみ（§6の焼き込み規約） |
| 章タイトル | `ActTitle{kicker,title}` | 各ACT頭 |
| 引用/事件カード | `EvidenceCard`/`StampReveal` | スラム・イン＋Trail |
| 地図ピン（一都市） | `prototypes/motion3d/map`（d3 US地図・深度パララックス） | WebGL＝`--concurrency=4 --gl=angle` |
| 背景BED | `AuroraField`/`GridWarp`/`LightRays`/`Atmospherics` | 冷スレート×cyan。常時ゆるく動かす |

**紙芝居/知覚モーション予算（機械ゲート・メモリ feedback_perceptual_motion_and_verify）**
- 静止(near-still)≤10%尺／単一ホールド≤3s／`motion_present` coverage≥40%／`animation_density` 緑。
- ヒーロー面（大きな動き）を各ACTに**2つ以上**、`FigureBeats`≥6、深度パララックス面≥40%。
- **カット刻み ~2.2s**・素材被り禁止（`footage_diversity` distinct≥0.40／再利用≤4／汎用象徴 天秤/砂時計≤2）。
- **禁止手:** 周回する淡い光の等速床（メモリ feedback_anim_caption_polish）／左右スイープ線／黄ウォッシュ／ただのズームのみ／紙芝居。

**per-ACT 運動メモ（例・数値）**
- ACT I ドライブウェイ：暖色ポーチ光→冷ヘッドライトの色温度スイープ（`interpolate` に `Easing.inOut(Easing.sin)`・6s）。手錠カットは 0.6s の速い寄り＋`Trail`。
- ACT II 一致：グリッド組み上げ（枠ごと `spring` damping18 stagger0.10s）→ 1枠 ring（`spring` damping10 stiffness120）→ 類似度 `NumberTicker`。循環図はループ矢印が閉じる（`Easing.out(cubic)` 0.8s）。
- ACT III 偏り：バーが `spring`(damping20) で伸び、ギャップに低音ヒット。反証カット「Asia-built systems」で対比。文字は maskslide。
- ACT IV 年表：`YearSweep` で 2018→2020→2024、マーカーが順にスタッガー着地。地図は一都市ピンが点灯、周囲は暗いピン群（深度パララックス）。

---

## §6. 素材プラン
- **Codexヒーロー静止画 30枚（S001–S030・オーナー指定）:** `episodes/_planning/codex_prompt_ep36.md` の SHOT INDEX＋本文プロンプト `EP36_williams_ai_prompts.v001.md`（ドライブウェイ再現／防犯フレーム再現／顔グリッド素材／booking再現／DMV／裁判所内外／case board／妊婦シルエット／家族の家／CCTV／解像する顔 等＋非被りバリアント）。18→30に増やしてb-roll依存を下げ `footage_diversity` に余裕。**肖像禁止・文字/数値焼き込み禁止・本物のexport/mugshot/記録に見せない（invariant 11）。** 生成は Codex（rule 19・SDXL勝手起動禁止）。
- **コミット済み棚のb-roll:** 商用OK factory（テーマ抽出）。**出荷前に必ず目視QC**（メモリ pd-factory-shelf-mislabeled：ラベル破損・場違い素材混入の実績）。
- **モーショングラフィック（コード生成・Claude）:** 顔グリッド／類似度メーター／偏りバー／年表／地図ピン／キネティック字幕／引用・事件カード。**画面の数値焼き込みは grade-A のみ**：`JANUARY 2020` `≈30 HOURS` `APRIL 2021` `JUNE 2024` `SINCE 2017` `4 YEARS` `10–100× · NIST 2019` `2018`(年号のみ・NYT裏付けA級)。**焼き込み禁止**：`$300,000`／`$3,800`／`5 watches`／`a dozen`／`34.7% / 0.8%`。

---

## §7. OP / ED（正典ブックエンド・**作り直さない**／signature・定数は不変）
**正典＝`remotion/src/components/Bookends.tsx`（invariant 14・row 14）。フォーク禁止。EP36は props を差し替えるだけ。**
```tsx
// CaseFilm 内で（フックの後に）:
<Sequence from={hook} durationInFrames={round(OPENING_SEC*fps)} name="Opening">
  <BrandOpening
    seriesLabel="YOUR RIGHTS VS. THE MACHINE"
    title="The Algorithm Said It Was You"
    subtitle="Facial recognition · a wrongful arrest · one city's new rules"
  />
</Sequence>
// … body …
<Sequence from={hook+op+body} durationInFrames={round(ENDCARD_SEC*fps)} name="Endcard">
  <BrandEndcard />   {/* 全話共通・不変 */}
</Sequence>
```
**props型（不変）:** `BrandOpening: {seriesLabel: string; title: string; subtitle?: string}` / `BrandEndcard: {channel?; ctaLine?; cadenceLine?}`。**`accent`/`hasLogo`は存在しない**（accentは常にBRANDゴールド、PDモノグラム常時描画）。定数 `OPENING_SEC=3.5` / `ENDCARD_SEC=9`。

**正典OPの技術（数値・root CLAUDE.md規則をコードで充足済み＝これを下敷きに数値は触らない）**
- レイヤー：①日の出背景 `Img(banner_sunrise.png)` zoom `1.28→1.06`(`Easing.out(cubic)`)＋rise `34→-6` ②ゴールド放射bloom（`spring` damping60 stiffness30・`0.82+0.18·sin` パルス・`mixBlendMode:screen`）③ink縦グラデ ④主役（`Trail layers=7 lag=1.5 trailOpacity=0.42` 内）＝PDモノグラム(`spring` stiffness70 damping11・y40→0/scale0.55→1)＋seriesLabel(letter-spacing 46→10)＋ゴールド線(width 0→560・移動グロー点)＋**タイトル単語スタッガー・マスク切れ上がり**(`spring` damping10 stiffness120・y120%→0/scale1.18→1・stagger `f(0.06)`・titleHit `f(1.1)`)＋subtitle(y16→0) ⑤着地の光streak＋白flash(peak0.26) ⑥`Particles(26,gold)`＋`Vignette`＋`Grain(0.06)`。fade `f(0.35)`/out `f(0.5)`。
- **なぜ新規に作らないか:** 上記が既にイージング必須／opacity単独なし／文字スタッガー／Trail残像／裏3層以上／マスク切れ上がり／定数化を**全て**満たす“正典”。EP36で必要なのは title/subtitle/seriesLabel の差し替えのみ。独自シアンOPは未採用（メモリ）。
- **EP36ブラッシュアップ（任意・テイスト内・フォーク無し）:** どうしても顔スキャン色を足す場合は、**Bookendsを改変せず**、`CaseFilm` のOPシーケンス背後に薄い cyan スキャン線オーバレイを**合成**（`mixBlendMode:screen`, opacity≤0.12, `Easing.inOut(sin)`）。既定は正典ゴールドのまま（オーナー承認前は足さない）。

**ED（不変）:** `BrandEndcard` 9.0s・購読CTAパルス＋ゴールド基線成長。尺は切りよく（BGMを途中で切らない）。終語="next" に ending ambience をアンカー。

---

## §7a. 音声・エンディング
- ナレ=ElevenLabs master（キーは `.env`）。字幕=息継ぎ単位・リード0.60s・medium.en・`_smart_split`（メモリ feedback_anim_caption_polish）。
- 音量=終始一定（speechnorm＋グルー圧縮＋2パス静的-14／必要なら）。BGM可聴フロア確保。ED ambience 固定。

## §8. サムネ（後工程・CTR最優先）
- 1280×720・**肖像禁止**（匿名シルエット/象徴）。案：暗い顔スキャングリッドに1枠だけ赤リング＋大文字「THE COMPUTER PICKED YOU?」。3案＋A/B。タイトル≤60字。

## §9. 通過必須ゲート（出荷前）
- 台本：`validate_episode.py` PASS／`verify_script_structure`／`verify_script_lint`／`verify_onscreen_text`（film.json生成後）。**現状すべてPASS**。
- 動画：`check_final_acceptance.py <ep> --render <mp4> --emit-receipt`＝緑受領書（`video_sha256`一致）。`animation_density`／`motion_present`／`footage_diversity`／caption_sync／mean-luma。
- OP/ED：`op_ed_bookends` ゲート（正典使用の確認）。
- 目視QC：factory棚コンタクトシート（場違い素材・ラベル破損）。肖像・生成物の本物誤認チェック。

## §10. 工程ステータス
- [x] topic承認 / research / claims / **script_verified（3回レビュー済）**
- [x] Codex引き継ぎ（18ショット）
- [x] **本設計書 v001**
- [x] **OPENINGアニメ（正典BrandOpening・EP36 props）を描画・検証済み** — `remotion/src/ep36_opening_preview.tsx`（共有Root.tsxを触らない独立エントリ）で3.5s/105fをレンダ（`out/ep36_opening.mp4`）。実フレーム目視QC：f09=モノグラム着地のみ／f42=単語スタッガーのマスク切り上がり進行中（THE ALGORITHM着地・SAID着地中・IT上昇中）＋光streak＋Trail残像／f72=全要素着地（PDモノグラム／YOUR RIGHTS VS. THE MACHINE／ゴールド線／THE ALGORITHM SAID IT WAS YOU／サブタイトル）。品質規則充足＝全モーションにイージング・opacity単独なし・スタッガー・Trailモーションブラー・裏3層以上・マスク切れ上がり・肖像なし。**invariant 14遵守（正典フォークなし）**。
- [x] **重いモーショングラフィックを先行構築・描画検証済み**（画像非依存）— `remotion/src/components/williams/`（FaceMatchGrid／BiasBars／CaseTimeline＝EP36新規）＋流用（NumberTicker=30 HOURS／PinDropMap=ONE CITY）。独立プレビュー `ep36_motion_preview.tsx` で各シーンをレンダし実フレーム目視QC（顔一致グリッド/偏りバー[10–100×・NIST 2019のみ・捏造%なし]/年表[grade-Aマーカー]/カウンター/マップ）。全モーションにイージング・Trail・裏3層・マスク切れ上がり・肖像なし・共有Root.tsx不変。
- [x] **モーショングラフィック10種を先行実装・描画検証**（自作5=FaceMatchGrid/BiasBars/CaseTimeline/LineupLoop/DatasetImbalance＋流用5=NumberTicker/PinDropMap/ActTitle/StampReveal/KineticCaptions）。`remotion/src/components/williams/`＋独立プレビュー。
- [x] **組み立て青写真 `04_scenes/scene_plan.v001.json`**（全16 span↔S001–S030・各spanにMG配線・on-screenはgrade-A逐語・SFXアンカー・尺=ナレ待ちTBD）。tyler形状準拠・grade-B数値の画面焼き0を機械確認。
- [x] **factory b-roll計画 `05_visuals/broll_plan.v001.json`**（テーマ/キーワード/被り回避・実ゲート footage_diversity 算数で ≥60 QC済クリップ目標・棚目視QC必須）。
- [ ] **Codex画像30枚（GateB停止）→ 目視QC** ← ここがクリティカルパス
- [ ] 深度マップ（画像到着後）／factory実選定＋コンタクトシート目視QC（Claude）
- [ ] narration(ElevenLabs)＋字幕（**台本オーナー承認後**に生成＝有料/やり直し回避のため保留）
- [ ] `williams_film.json` → CaseFilm組み立て（scene_planの配線を焼く）→ 本レンダ → 受領書 → オーナー承認
- **現状=「画像待ち＋組み立てだけ」に到達**：台本(3回レビュー済・全ゲート緑)＋正典OP検証＋重いMG10種＋設計書＋Codex30枚プロンプト＋scene_plan＋broll計画が揃い、残るクリティカルパスはCodex画像→(深度/factory選定)→組み立て→レンダ。narrationは台本承認待ち。
