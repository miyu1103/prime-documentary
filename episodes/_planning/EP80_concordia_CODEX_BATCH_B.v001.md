# EP80 · CONCORDIA — IMAGE ORDER (BATCH B) v001 — 差し替え3枚

**3 plates: `N001` `N104` `N141`. 番号は元のまま**（BATCH A の同じIDを置き換えます）。

## なぜ作り直すか

3枚とも **傾斜計（クリノメーター）は正しい**。この船が傾いていく話なので、この計器はこの作品の
背骨です。**問題は、その隣で燃えている石油ランプだけ**です。

元のプロンプトに `a bright brass lamp burning beside it` と書いてあり、それが**裸火のオイル
ランタン**になりました。コスタ・コンコルディア号は **2006年就航**で、裸火の照明はありません。

**証拠は同じセットの中にあります。** `N116` は同じ真鍮の傾斜計ですが、プロンプトにランプの
記述が無く、時代のずれも起きていません。だから N116 は合格にしています。今回の3枚も
**「ランプの記述を消す／現代の照明に置き換える」だけ**で直ります。

## 番号について

**元と同じ `N001` `N104` `N141` で納品してください。** この3枚は `episode_spec.v001.json` の
`mandatory_stills`（必ず本編に入れる指定）に載っているため、番号を変えると仕様と食い違います。
まだ何も組み立てていないので、同一IDでの置き換えが正しい手順です。
旧ファイルは `remotion/public/concordia/img/rejected/` に退避済みです。

## サイズ

- Codex の生成サイズ **1672×941 のままで構いません**（4K化はこちらでやります）。
- **16:9 ちょうど**（幅÷高さ = 1.778）。
- **1プロンプト＝1枚。**
- 納品先 `E:\pd-media\05_visuals\concordia\img_raw_codex_batch_b_v001\`。**既存ファイルは上書きしないこと。**

## 発注表

| ID | セクション | subject（`[STYLE]` と `[NEG]` を後ろに付けて生成） |
|---|---|---|
| N001 | HOOK | Extreme macro of a **modern** ship's brass clinometer mounted on a painted steel bulkhead, the pendulum hanging dead centre at rest, lit by a **recessed white LED bulkhead light**, no numerals on the arc |
| N104 | ACT_3 | A **modern** ship's brass clinometer with the pendulum swung far over, on a painted steel bulkhead, lit by a **white LED bulkhead light**, no numerals |
| N141 | ENDING | Extreme macro of a **modern** ship's brass clinometer, the pendulum hanging dead centre at rest, lit by a **cool white LED strip**, no numerals |

**裸火・オイルランタン・ケロシンランプを画面に入れないでください。** 照明は現代の電灯です。

## [STYLE]

```
present day, 2010s, modern vessel, cinematic documentary reconstruction, one practical light source visible in the frame, high contrast, photorealistic, 16:9,
```

## [NEG]

BATCH A の NEG に、今回の原因である裸火の語を追加しています。

```
Avoid: oil lantern, kerosene lamp, gas lamp, open flame, candle, hurricane lamp, storm lantern, vintage, antique, sepia, 1900s, 1912, period piece, steamship, riveted bulkhead, text, lettering, handwriting, cursive, signature, numerals, numbers, seals, emblems, logos, badge, insignia, human face, facial features, portrait, identifiable person, airline livery, airline tail markings, ship funnel markings, company colour scheme, low-resolution.
```

## 納品後

設計レーンが3枚を判定し、合格分を 4K化 → 深度生成 → `remotion/public/concordia/img/` へ配置します。
