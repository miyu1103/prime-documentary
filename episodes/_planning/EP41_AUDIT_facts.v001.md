# EP41 (thompson) — 事実・R1・整合 監査レポート (facts) v001

- 監査日: 2026-07-20
- 対象:
  - 台本 `episodes/_planning/EP41_thompson_script.en.v001.md`
  - 設計書 `episodes/_planning/EP41_thompson_DESIGN_and_CODEX_PROMPTS.v001.md`
  - スペック `episodes/_planning/EP41_thompson_PRODUCTION_SPEC.v001.json`
- 判定サマリ: **BLOCKER 0 / MAJOR 1 / MINOR 5**（＋裏取り未完 5項目・R1違反 0）
- 計器についての自己疑い: 全件一致/全件FAILは出ていない（SPEC照合は全件一致だが図種で1件不一致、事実は一部裏取り不能）。計器（WebFetch/検索）側の制約でレンズ1が部分的に未完である点を明記する。

---

## レンズ1: 事実の裏取り（一次資料）

### 計器の制約（重要）
- WebSearch予算はセッション開始時点で枯渇（200/200使用済み）。本監査中に新規検索は不可。
- 一次判例本文（supremecourt.gov PDF / justia / cornell LII / findlaw / courtlistener / loc.gov）は
  すべて WebFetch で **403 / 404 / 空テンプレ** を返し取得不能だった（実出力は下記evidence）。
- 取得できた権威情報源は **Wikipedia の判例記事**（`en.wikipedia.org/wiki/Connick_v._Thompson`）のみ。
  これは判例本文を引用する二次だが listicle ではない。中核の帰属・票数はこれで確認できた。

### ✓ 確認できた事実（Wikipedia判例記事、判決本文を引用）
| 事項 | 台本/設計の記述 | 裏取り結果 |
|---|---|---|
| 票数 | 5対4 (C03) | **5–4** ✓ |
| 判決日 | March 29, 2011 (N10) | **March 29, 2011** ✓ |
| 口頭弁論 | October 2010 (C02/N10) | **October 6, 2010** ✓ |
| 多数意見執筆 | Thomas ＋ Roberts/Scalia/Kennedy/Alito (C03) | **Thomas。Roberts, Scalia, Kennedy, Alito が同調** ✓ |
| Scalia同意 | 「故意の不正の可能性」(C04/C19) | **Scalia が同意意見、Alito 同調** ✓ |
| 反対意見 | Ginsburg ＋ Breyer/Sotomayor/Kagan (C05) | **Ginsburg 反対、Breyer, Sotomayor, Kagan 同調** ✓ |
| 収監/死刑囚房 | 18年収監・うち14年死刑囚房 (C13/N03/N04) | **18年収監・14年死刑囚房** ✓ |
| 血液型 | 加害者の血=B / Thompson=O (C09/N02) | **被害者衣類の血=type B、Thompson=type O** ✓ |
| 陪審評決 | $14M (C17/N08) | **$14 million** ✓ |
| 判旨 | 単一Brady違反では failure-to-train §1983 責任を負わせられない／類似違反のパターン要／deliberate indifference (C06/C18) | **「単一のBrady違反に基づく failure-to-train で §1983 責任は負えない」「類似の憲法違反のパターン」要求** ✓ |

→ **R1で最重要の「実在の最高裁5–4判決・多数意見/反対意見の帰属」は一次引用で確認済み**（EP40 Lech の逆ケースを正しく扱えている）。

### △ 裏取り未完（矛盾は無いが独立確認できず）— 5項目
Wikipedia判例記事は背景の細部を欠き、判例本文PDFは取得不能だったため、以下は**本セッションでは独立確認できなかった**。
いずれも台本の claim 台帳（C-ledger）に紐づき、**どの情報源とも矛盾はしていない**。script_verified 台帳を権威とすること。

1. **Gerry Deegan の実名・1994年の死の床の告白（→Riehlmann）・「9年間」保持** (C14/N05)。
2. **処刑予定日 1999年5月20日 / 期日設定日 1999年4月16日 の分離** (C12/N06)。※設計は「4/16=設定日、5/20=実施予定日」と正しく分離しており、この区別自体は台本内で自己整合。
3. **「4人の検事が血液型を知っていた」** (C15/N11)。※台本はこれを Ginsburg 反対意見に帰属させており帰属は適正。
4. **「14年間隠されていた」の厳密値** (C09)。1985→1999 と算術的に整合するが独立ソース未取得。
5. **Resurrection After Exoneration 設立・2017年死去** (C26)。※設計書自身が C26 を「低確度（企画ブリーフ準拠）」と明示済み。

補足（裏取り不要）: 監査項目の「処刑日の回数」について、**台本は処刑期日の“回数”を数値主張していない**（「a schedule」等の表現のみ）。よって検証対象クレーム無し＝FAIL対象外。

---

## レンズ2: R1制約 — **違反 0件**

| 検査 | 結果 |
|---|---|
| 実在人物の認識可能な顔/肖像を出す指示 | **無し。** §9.2 の全SDXL正プロンプトが `no face / no people / silhouette / cropped so no face / unidentifiable`。`portrait/mugshot/likeness` は §5.6 の Avoid（ネガティブ）のみ。R1-D/E 準拠 ✓ |
| 実在検察官が法廷記録の認定事実のみか | ✓ 検察官を人物として描かない指示（§1.2.2）。台本の "hid/buried" は Deegan本人の告白＝認定事実の範囲。動機は "A conviction is a weapon" と一般化され、特定検事の内心を断定していない |
| 読める偽の判決文/公文書 | **無し。** 全書類プロンプトが `completely illegible / no readable text / no legible`。数値は AE/figures のタイポで出す方針（§1.2.3）✓ |
| ★5–4 の正誤・両論の中立帰属 | **正しい。** 台本 "Five to four. The Court reverses."（4-5/9-0 等の誤記なし）。Thomas/Scalia→「the majority」/「he writes」、Ginsburg→「the dissent」「she says」。争点は多数/反対に中立帰属（R1-A準拠）✓ |
| Thompson の有罪/無実の断定 | 断定なし。「2003 再審で not guilty」「血は type B≠O＝彼のものではない（認定事実）」に留める（R1-B準拠）✓ |

---

## レンズ3: スペック↔設計書 整合 — **MAJOR 1 / MINOR 5**

### 数値の全件照合（設計「唯一の真実」ブロック vs SPEC JSON）= 全件一致
`words 2026 / narration 682.5 / scenes 46 / cuts 214 / still 80·96 / factory 88·88 / motion 15·30 /
distinct 183 / first_use 0.8551 / still_share 0.4486 / beats_floor 29 / mean_shot 3.19 / wpm 178.1 / max_shot 6.0`
→ **設計書は SPEC を忠実に転記。捏造数値なし。**（`check_script_length.py` 実測も words=2026・band内 PASS）
→ AEカード b01–b08 のラベル数値・figures の stat も、後述 m3 を除き **§1.4 台帳(N01–N12)内**。EP40 の $580,000/架空間取りのような台帳外焼き込みは**無し**。

### 【MAJOR-1】figure kind `comparebars` は FigureBeats.tsx に存在しない
- 設計書 §7.2（521,525,535行）が figure kind **`comparebars`** を3枠指定。
- しかし `remotion/src/components/FigureBeats.tsx` の実在小文字値は **`compbars`**（`kind === 'compbars'` / `ComparisonBars`）。`comparebars` は未定義。
- 影響: Codex が film.json にそのまま `comparebars` を書くと当該3ビートが**無描画**。density 33→30（≥29なので下限は割らないが）、比較ビートが無言で消え、variety 主張(8種)も崩れる。
- 対処: 設計の `comparebars` を **`compbars`** に統一。
- 他の figure kind（`acttitle/timeline/stat/quote/votetally/numberticker/pindropmap`）＋ graphics の `kinetic` は**すべて実在**。無効値は `comparebars` のみ。

### 【MINOR-1】§3.2 の「still-primary 39 / factory-primary 7」が下流と矛盾
- §3.2 本文冒頭が「still-primary 39シーン / factory-primary 7シーン」と書くが、直後の確定文・表・§9.2 は
  **factory-primary 10シーン(S03/07/08/21/25/27/29/34/42/44) / SDXL-primary 36シーン**。46−10=36 で下流は一貫。
- 「39/7」は取り残しの誤記。運用値(10/36)は §9.2 の36プロンプト・i2v15本と整合済み。文言修正のみ。

### 【MINOR-2】`measure_vo_wpm.py` が実在せず、受入コマンドが参照
- `ls scripts/` で **未存在**（別名でも無し）。§13 受入 step4・§12.3 D2 が gate として起動。§12.2 C14 は「既存があれば流用」。
- 実体は Codex-B 新規実装物。だが受入コマンド行が非存在スクリプトを指す点は明記が必要。
- （`check_thompson_accuracy.py`/`validate_thompson_beats.py` も未存在だが、C3/C13 の**新規実装成果物**として明示されており想定内。既存参照スクリプト `check_script_length/motion_density/final_acceptance/generate_sdxl_4k/build_production_spec/build_footage_contact_sheet/check_animation_mix/check_asset_reuse` は**全て実在**。）

### 【MINOR-3】台帳ギャップ: §7.2 の figures が §1.4(N01–N12) 外の数値を表示指示
- §1.3 R1-C は「画面に出す数値は §1.4 の確定表に存在するものだけ」。しかし §7.2 は次を画面表示に回す:
  - `timeline`: **1994**（Deegan告白年）… §1.4 に N-id 無し
  - `stat`: **約1か月 / one month**（残り時間）… §1.4 に無し
  - `comparebars`/`quote`: **four prior reversals・ten years**（過去10年に4件破棄）… §1.4 に無し
- いずれも台本内に文言はあるが、**§1.4 表には未登録**。`accuracy_lock`(R1-C) がこれらを FAIL する恐れ、または表に登録すべき。
- 対処: §1.4 に「1994 / ~1 month / four prior reversals(10yr)」を追記するか、当該 figure を落とす。

### 【MINOR-4】§7.2 quote⑤「修正第14条デュープロセス系の逐語」の出所が不明
- R1-A は「引用符内は逐語のみ（要約不可）」。だが台本は修正第14条/デュープロセスを**逐語引用していない**。
- 「台帳内」とあるが台本本文に該当逐語が無く、Codex が文言を創作すると R1-A 違反化するリスク。
- 対処: quote⑤ を台本/台帳の実在逐語行に差し替え（例: 台本の Brady 定義文・"a dissent frees no one and pays no one"）。

### 【MINOR-5】graphics variety ラベル `kinetic_typography` と実装 kind `kinetic`
- §7.1/§7.4 が graphics[] を「kinetic typography」「kinetic_typography」と表記。FigureBeats の実在テキスト種は **`kinetic`**。
- 記述的ラベルであり致命ではないが、film.json の JSON kind は必ず `kinetic` にする旨を明記推奨。

### 情報（欠陥ではない）
- SPEC 自身の acts 語数合計（本文1966＋タイトル/サムネ43＝2009）と `words_total 2026` に 17語差。これは SPEC のパーサ由来の内部差であり、設計書は 2026 と 682.5マスターを忠実に使用（§3.1 で 662.3 vs 682.5 の差も明記済み）。設計側の捏造ではない。
- シーン→幕割当（S01-02/03 HOOK, S04 OP, S05-14 幕1, S15-24 幕2, S25-37 幕3, S38-42 幕4, S43-46 ENDING）は台本の幕構成（HOOK/OP/幕1-4/ENDING）に1:1対応。番号ズレ・別体系(SSxx)の発明なし ✓。

---

## evidence（実行コマンドと実出力の要点）
```
# figure kind 実在確認
$ grep -niE "comparebars|compbars" remotion/src/components/FigureBeats.tsx
107:  | {... kind: 'compbars'; items:...}
439:  {b.kind === 'compbars' && <ComparisonBars .../>}
# → comparebars はゼロ件、compbars のみ存在

$ grep -n "comparebars" EP41_..._DESIGN_....md
521,525,535 行で comparebars を使用   # ← 無効値

# 参照スクリプト存在
FOUND  check_script_length.py / check_motion_density.py / check_final_acceptance.py /
       generate_sdxl_4k.py / build_production_spec.py / build_footage_contact_sheet.py /
       check_animation_mix.py / check_asset_reuse.py
MISSING check_thompson_accuracy.py(=C3新規) / validate_thompson_beats.py(=C13新規) /
       measure_vo_wpm.py(=C14・受入が参照するが未存在)

# 数値照合（SPEC JSON パース）: 設計「唯一の真実」ブロックと全件一致
words 2026 / narr 682.5 / scenes 46 / cuts 214 / still 80·96 / factory 88·88 /
motion 15·30 / distinct 183 / first_use 0.8551 / still_share 0.4486 / beats_floor 29

# 語数ゲート実測
$ python scripts/check_script_length.py .../EP41_thompson_script.en.v001.md --json
{"ok":true,"words":2026,"words_required":[1575,2141],...}   # PASS

# 一次判例本文の取得可否（すべて失敗）
WebFetch supremecourt.gov/opinions/10pdf/09-571.pdf   -> 403
WebFetch supreme.justia.com/.../563/51/               -> 403
WebFetch law.cornell.edu/supremecourt/text/563/51     -> 404
WebFetch caselaw.findlaw.com/us-supreme-court/563/51  -> 404
WebFetch courtlistener.com/opinion/214599/...         -> 空
WebFetch tile.loc.gov/.../usrep563051.pdf             -> 403
WebFetch oyez.org/cases/2010/09-571                   -> 空テンプレ
WebFetch en.wikipedia.org/wiki/Connick_v._Thompson    -> 取得成功（中核帰属を確認）
```

---

## 結論
- **裏が取れなかった項目: 5**（Deegan/1994/9年・5/20↔4/16分離・4検事・14年隠匿の厳密値・RAE設立/2017死去）。いずれも矛盾なし＆台帳紐付きだが、一次本文が全滅・検索枯渇のため本セッションで独立確認不可。
- **R1違反: 0件**（5–4正記・中立帰属・顔なし・illegible・検察官非描写、すべて適正）。
- **スペック不整合: MAJOR 1（`comparebars`→`compbars`）＋ MINOR 5**。数値の全件はSPECと一致し捏造なし。最優先修正は figure kind の `compbars` 統一。
