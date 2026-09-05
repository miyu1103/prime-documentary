# EP75 Lahaina CODEX redo — generation and QC report v003

Generated and checked: 2026-08-22T04:15:52.6201294+09:00  
Provider path: Codex built-in image generation, one request per plate  
Prompt contract: `EP75_lahaina_CODEX_REDO_ALL.txt`  
Prompt contract SHA-256: `E76E2263BF4AFEE1D1DAA3E123F44FA72200530A318BFB8A0A481557F041D6B7`

## Japanese summary / 日本語要約

- 今回の正典6枚を、1プロンプト＝1枚で全件生成した。自動リトライはしていない。
- 6枚ともPNG `1672x941`、比率 `1.776833` で技術QCを通過。完全重複は0。
- 目視・意味・連続性QC合格は4枚: `H006`, `H058`, `H077`, `H099`。
- 合格4枚は既存版をバックアップして本番棚へ反映し、stagingとのSHA-256一致を確認した。
- `H104` は車両プレート/バッジ形状が残るため保留。本番棚には未配置。
- `H119` は遠景を含めるとサイレンが4本を超えるため保留。既存H119は上書きせず保持した。
- 本番棚はH001–H135の134枚。未配置はH104だけ。

## Paths

- Destination: `E:\pd-media\assets\ai\lahaina`
- Staging: `E:\pd-media\assets\ai\lahaina\_codex_redo_20260822_02`
- Pre-overwrite backup: `E:\pd-media\assets\ai\lahaina\_backup_redo_20260822_02`
- Contact sheet: `E:\pd-media\assets\ai\lahaina\_codex_redo_20260822_02\contact_sheet.v003.png`
- Contact sheet SHA-256: `5939A37C9477F58ABC99F1258F603C62DE77D79467662CC12274A856B4BBDE93`

## Deployed assets

| ID | Action | Dimensions | SHA-256 | QC result |
|---|---|---:|---|---|
| H006 | replacement | 1672x941 | `E8DBBA0C503ADD0CAFA3F7C495BEB50EE7E62E97ECE61D77F0FCF9CEB408A8AB` | pass; low wind-flattened smoke over dry grassland, no flame or palms |
| H058 | replacement | 1672x941 | `E7AED6DAB4B9C3951C9E71D0294D023EBA0FAC57FE19E44DC79C839C7ED30BD1` | pass; one rear-view driver stands in the open door, no readable marking |
| H077 | replacement | 1672x941 | `DE91EA2ED02FD6EC2C068FFE49EE2BB497F0863C925B487434FDB693584EF2BC` | pass; intact vehicles, blistered paint, empty cabs and open doors |
| H099 | replacement | 1672x941 | `4F3ED5B6BE657A6D10F8AD76627B28FC7152413B14CE0BB48962AE41C863419D` | pass; rear-view figure holds the gate, cars move away, no palms |

## Backups

| ID | Preserved SHA-256 |
|---|---|
| H006 | `271899F8BCC03E1B6E999B4B86891011CA85FDAB628F06267548514A816D0B4A` |
| H058 | `7D40A634187C55DE06262795FF451DBF88547622D46F9137EDCFBC83FCB46B7F` |
| H077 | `8B2D3FDEDC8FBE15DEE2F610FA65E416954789245C0A7E1903BE233B214C8345` |
| H099 | `05E4FAF5F9B1CC8ED7A8F439A3BE6C993F5316F38C18A19B5F592BD905F9715A` |
| H119 | `41BA3D723AD9CC9CF1E748E098750FF91B177ECE29D609481D5566FD9C2B3D4C` |

## Exception queue

| ID | Stage | Reason | Destination action |
|---|---|---|---|
| H104 | visual QC | Registration plates and vehicle badge/model markings remain visible. | Held in staging; destination remains missing. |
| H119 | visual QC | More than four siren poles are visible when distant roadside poles are counted. | Held in staging; existing H119 preserved unchanged. |

## Provider metadata and cost

The built-in provider exposed no model identifier, seed, or per-image billing record. No CLI/API fallback and no separately billed external API were used.

## Remaining gate

The six-plate redo is partial: four replacements were delivered, H104 remains missing, and the new H119 candidate was not accepted. No retry should occur without a new explicit image-generation instruction.
