@echo off
rem PD-Monthly-DeepPass reminder (scheduled task target)
mshta "javascript:var s=new ActiveXObject('WScript.Shell');s.Popup('PD: 月次ディープパスの日です。\nepisodes/_planning/measurements/MONTHLY_DEEP_PASS_PROMPT.md のプロンプトをClaude Codeに貼って実行してください。',0,'Prime Documentary',64);close();"
