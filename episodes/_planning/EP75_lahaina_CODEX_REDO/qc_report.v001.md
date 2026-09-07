# EP75 Lahaina CODEX redo — generation and QC report v001

Generated and checked: 2026-08-21T11:00:58+09:00  
Provider path: Codex built-in image generation, one request per plate  
Prompt registry: `plates.v001.jsonl`  
Prompt registry SHA-256: `394FEA324B1F8B8741965C1135EE7F048048FC0810EEFB7E6E113D03CE961660`  
Combined order SHA-256: `A2BA36E787FF72756B4E0F2194A555B3F60FB9976ECE16BAF3D0A4CD29742E1D`

## Japanese summary / 日本語要約

- 対象は21枚。生成成功20枚、H096はプロバイダの安全判定で拒否され、自動再試行していない。
- 技術QCでは生成20枚すべてが有効なPNG、1672 x 941、比率1.776833。発注書が16:9納品として明示的に許容する寸法。
- 目視・連続性QCを通過して指定先へ反映したものは16枚。
- H019、H020、H104、H119はステージングで保留。
- H119の新候補は指定4本に対して5本のサイレン柱が写ったため、既存H119を上書きせず保護した。
- 指定先は現在128/132枚。未配置はH019、H020、H096、H104。
- 自動再試行や別名バリアントは作成していない。

## Paths

- Destination: `E:\pd-media\assets\ai\lahaina`
- Staging candidates: `E:\pd-media\assets\ai\lahaina\_codex_redo_20260821_01`
- Pre-overwrite backup: `E:\pd-media\assets\ai\lahaina\_backup_redo_20260821_01`
- Contact sheet: `E:\pd-media\assets\ai\lahaina\_codex_redo_20260821_01\contact_sheet.v001.jpg`
  - Order, left-to-right and top-to-bottom: H002, H012, H014, H019, H020, H021, H039, H056, H057, H061, H073, H095, H103, H104, H107, H112, H118, H119, H129, H132.
  - SHA-256: `0F610C43B267AC7420B162DD03DD3B354CE632ED4AEE5C8021EE55098FA9B63A`

## Approved destination assets

| ID | SHA-256 | QC result |
|---|---|---|
| H002 | `4B531CD3DF4059C32F1BC8554DC95DB56A8D318A3C14120357489B06EE9413F7` | pass; replaced with backup retained |
| H012 | `C9B56D2EAFAF10AC54F45F00CC090B648119D3020CBD5D5D87CB9CF4341B8D7E` | pass |
| H014 | `38CBD723A2F342A6998A4AC256636B37B9B33A715710F1B3BB1971DB0807A73B` | pass; replaced with backup retained |
| H021 | `E81F226EE39C080FE34C8EBB0D51D528355A7D084AE3EBC7A8F5539DF6488CD9` | pass; continuity edit from H018 |
| H039 | `05A699C5EA23366FE45656C48D91528E91CC30CB825E25917DBEF886B17F59B0` | pass; replaced with backup retained |
| H056 | `5CD8CA1CEBBDE25BA096C7C66BDF882C5FDD8CA04556BB9475BA89C5677186A0` | pass |
| H057 | `453239D18D40E105E33D9155BA0421FB0372B79625152419EC07ED04059874E6` | pass |
| H061 | `D16453BB4C0A0D0B14F03C168F304671DBA88B5E998B449017EEFA2DFD1BB312` | pass; replaced with backup retained |
| H073 | `24FD8DF9F124A7EDF08F4C19174C93C1D7FE42F06821B8ED51928039B14AA286` | pass |
| H095 | `9DB4141DD07C2E7B43BAD861F5D4698D3AC98898C213AB1D79706D0D89905164` | pass |
| H103 | `E7D151FD66016917A85910C2A78BCC300C7487A975B3414E758ACEC542B9CD03` | pass |
| H107 | `81585E95CDA760B124EB4157F627B8068DE8FB6A7CAE0A71387A223818012805` | pass |
| H112 | `BE589BFE5AD8B4AADC42E0E5B49EF4D7E16F0B196338B66F0784CAB0A4C5B4A7` | pass; replaced with backup retained |
| H118 | `F3FD58175E686AC3610F47BA92CDEE17F34CF9F9C6801D295DC60287A4B9F907` | pass; continuity edit from H018 |
| H129 | `ECCCBC6B602161CFE6DE1AC012BD201EBA54E6E208FB26D89E21773F85B41A10` | pass; continuity edit from H120 |
| H132 | `AB651E940776355B4CCF51CC8B1526DD846EDAB1D92AD1F581CCD62FB1FD4C4B` | pass; continuity edit from H023 |

Destination hashes were read back and matched the staged hashes for all 16 copied files.

## Exception queue

| ID | Stage | Reason | Destination action |
|---|---|---|---|
| H019 | generated; technical pass | Does not preserve H018 siren geometry or fixed framing. | Held in staging; not copied. |
| H020 | generated; technical pass | Does not preserve H018 siren geometry or fixed framing. | Held in staging; not copied. |
| H096 | provider rejected | Safety system rejected the padlock-cutting image as illicit. No output file. | No retry; no destination file. |
| H104 | generated; technical pass | Dashboard numerals and vehicle marks violate the no-numerals/no-logo constraint. | Held in staging; not copied. |
| H119 | generated; technical pass | Candidate contains five siren poles, not four. | Held in staging; existing H119 retained unchanged. |

Existing H119 SHA-256 remains `41BA3D723AD9CC9CF1E748E098750FF91B177ECE29D609481D5566FD9C2B3D4C`, identical to the pre-run backup.

## Provider metadata and cost

The built-in provider did not expose a model identifier, seed, or per-image billing record in the returned metadata. No CLI/API fallback was used and no explicit paid external API was invoked.
