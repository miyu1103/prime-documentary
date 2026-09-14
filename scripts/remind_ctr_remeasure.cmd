@echo off
rem PD-CTR-Remeasure-0808 reminder (scheduled task target)
mshta "javascript:var s=new ActiveXObject('WScript.Shell');s.Popup('PD: 8/8 CTR再測定の日です。\n手順書: episodes/_planning/measurements/RUNBOOK_CTR_REMEASURE_0808.md\n(cookieエクスポート → 3スクリプト即実行 → Claudeで分析)',0,'Prime Documentary',64);close();"
