# EP82 · VALDEZ — IMAGE ORDER (BATCH B) v001 — 未着1枚

**1 plate, `V079`.** BATCH A の184枚のうち **V079 だけが未着**です（実測: V001–V184 のうち
183枚が `E:\pd-media\05_visuals\valdez\img\` にあり、欠番は V079 の1つ）。

## サイズ

- **長辺 3840 px 以上・16:9 ちょうど**（幅÷高さ = 1.778）。
- Codex の生成は 1672×941 固定です。native-4K が使えないなら
  **Real-ESRGAN x4plus → 6688×3764 → LANCZOS で 3840×2160 ちょうど**。2倍拡大では床を越えません。
- 納品先 `E:\pd-media\05_visuals\valdez\img\V079.png`。**既存ファイルは上書きしないこと。**

## 発注

| ID | セクション | subject（`[STYLE]` と `[NEG]` を後ろに付けて生成） |
|---|---|---|
| V079 | ACT_3 | A pair of dividers stepping off a distance on a lit sea chart, close-up, drawn lines only |

**海図の文字・数字は一切解像させないこと。** 線と等深線だけです（`[NEG]` に入っていますが、
この板は「読める文書」に一番近いので特に注意してください）。

## [STYLE]

```
cinematic documentary reconstruction, one practical light source visible in the frame, high contrast, photorealistic, 16:9,
```

## [NEG]

```
Avoid: text, lettering, handwriting, cursive, signature, numerals, numbers, seals, emblems, logos, badge, insignia, human face, facial features, portrait, identifiable person, ship name, funnel marking, company colour, low-resolution.
```
