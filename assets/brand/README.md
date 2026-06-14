# assets/brand — Prime Documentary brand assets

Owner drops the existing PD brand assets here (one-time). Until they arrive, Remotion
renders a **vector reproduction** from the spec in `remotion/src/brand.ts`; when these
files exist they are composited on top for exact fidelity (decisions/0002 §G).

Expected files (suggested names — update `remotion/src/brand.ts` if different):

- `pd-logo.png`        — PD logo (transparent background, high-res)
- `pd-logo.svg`        — vector logo if available (preferred)
- `sunrise-banner.png` — the sunrise / horizon banner

## Palette (source of truth: `remotion/src/brand.ts`)

| token | role | hex (adjust to the real brand) |
|---|---|---|
| `ink` | base black | `#0A0A0C` |
| `navy` | deep navy ground | `#0B1A2B` |
| `electric` | primary electric blue | `#1F6BFF` |
| `silver` | silver | `#C8CDD6` |
| `gold` | accent | `#E5B53A` |

These hexes are placeholders calibrated to "black/deep-navy + electric blue + silver + gold."
Replace with the exact brand values when known; everything reads from the tokens.

Note: brand image binaries are large media — keep source masters backed up; do not assume the
repo is the only copy (docs/34).
