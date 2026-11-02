# PD Visual System control scripts

- `phase_gate.py`: Phaseのassert/start/candidate-complete/advanceを管理します。
- `validate_kit.py`: Claude Code構成、Phase、Component registry、Markdown、JSONを検証します。
- `validate_examples.py`: JSON Schemaとサンプルを検証します。`jsonschema`が必要です。

## Typical commands

```bash
python scripts/pd-visual-system/phase_gate.py assert --phase P00
python scripts/pd-visual-system/phase_gate.py start --phase P00
python scripts/pd-visual-system/validate_kit.py --project-root .
python scripts/pd-visual-system/validate_examples.py
```
