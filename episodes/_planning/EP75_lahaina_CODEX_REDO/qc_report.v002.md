# EP75 Lahaina CODEX redo — generation and QC report v002

Generated and checked: 2026-08-22T01:48:51+09:00  
Provider path: Codex built-in image generation, one request per plate  
Prompt contract: `EP75_lahaina_CODEX_REDO_ALL.txt`  
Prompt contract SHA-256: `A39B3E4B183F19EDBEE74404ECD986B132590AC24687AAF04DCF083BCE46C793`

## Japanese summary / 日本語要約

- 対象14枚を、1プロンプト＝1枚で全件生成した。自動リトライはしていない。
- 生成成功14枚。技術QCは13枚通過、目視・意味・連続性QCまで通過したのは8枚。
- 本番反映: `H010`, `H019`, `H020`, `H095`, `H096`, `H133`, `H134`, `H135`。
- H010とH095は既存版をバックアップして置換。残り6枚は新規配置。
- 保留: `H006`, `H058`, `H077`, `H099`, `H104`, `H119`。既存のあるIDは上書きしていない。
- 本番棚はH001–H135の134枚。未配置はH104だけ。
- 全反映ファイルはステージングと本番のSHA-256が一致した。

## Paths

- Destination: `E:\pd-media\assets\ai\lahaina`
- Staging: `E:\pd-media\assets\ai\lahaina\_codex_redo_20260822_01`
- Pre-overwrite backup: `E:\pd-media\assets\ai\lahaina\_backup_redo_20260822_01`
- Contact sheet: `E:\pd-media\assets\ai\lahaina\_codex_redo_20260822_01\contact_sheet.v002.jpg`
- Contact sheet SHA-256: `130415AFF0C4A417CFBD87CF86278120B697A3BAE2A8EA9C91028D4FEBA04DEA`

## Deployed assets

| ID | Action | Dimensions | SHA-256 | QC result |
|---|---|---:|---|---|
| H010 | replacement | 1672x941 | `7E41A93575E3F6B6BF46D5D7C76328C7AD198E8250F64BD68F2F5FDAFFE5FDD1` | pass; H009 siren continuity retained |
| H019 | new | 1672x941 | `4E2D1CFA519C4BFC3195105D6ED36D7B93D0A6EA256C0D4608470FADF37FFE45` | pass; H018 fixed framing retained, harder light |
| H020 | new | 1672x941 | `85B3ABA019AD1FBD156BE4E106E0A54EFF3806D057433B490A73CA947D1CBB9B` | pass; H018 fixed framing retained, overcast |
| H095 | replacement | 1672x941 | `657BF6511B578251F0D23BCEB2784EFF7677ABF9A21D248BB40751DD85A775BA` | pass; intact queue, face hidden |
| H096 | new | 1672x941 | `42DC70D62414FB3E587A8D181E1F911ABC20D4DB1459EE22A46B580D8EEE3441` | pass; provider accepted authorized-maintenance framing |
| H133 | new | 1672x941 | `3D31A32805514FBAFC977434DE4E756850635E93AB34A1A92815D31CB99F4068` | pass; anonymous figure, mauka view |
| H134 | new | 1672x941 | `CADB2F84BED51D0417BB522621A3AE4D3D11B1D23B0A3EC70ABD753492C69EF0` | pass; anonymous lineman, no insignia |
| H135 | new | 1672x941 | `478A08803269FEE2E7D5E05F46031507EA743067E3D720DAC9BAD84FECD7EC7B` | pass; blank folder and desk |

## Backups

| ID | Preserved SHA-256 |
|---|---|
| H010 | `20E8E63AC9D6A3B7CFA378E0F306B25E7E1CFB06AD704576A2F4036D9DCA7EDD` |
| H095 | `9DB4141DD07C2E7B43BAD861F5D4698D3AC98898C213AB1D79706D0D89905164` |

## Exception queue

| ID | Stage | Reason | Destination action |
|---|---|---|---|
| H006 | visual QC | Palm trees; town foreground dominates instead of smoke moving low across grassland. | Held in staging; existing destination preserved. |
| H058 | visual QC | Vehicle emblem and numeral-like mark remain visible. | Held in staging; existing destination preserved. |
| H077 | semantic QC | Reads as burned-out aftermath, not paint blistering while smoke passes. | Held in staging; existing destination preserved. |
| H099 | visual QC | Palm trees visible. | Held in staging; existing destination preserved. |
| H104 | visual/semantic QC | Palm trees and vehicle markings; viewpoint is not behind the driver's seat. | Held in staging; destination remains missing. |
| H119 | technical QC | Exactly four siren poles and no palms, but 1881x836 = 2.25:1, not 16:9. | Held in staging; existing H119 preserved unchanged. |

## Provider metadata and cost

The built-in provider exposed no model identifier, seed, or per-image billing record. No CLI/API fallback and no separately billed external API were used.

## Remaining gate

The order is still partial. H104 is the only missing destination ID. Five other requested replacements remain held because their new candidates failed QC, while their prior destination files remain protected. No retry should occur without a new explicit image-generation instruction.
