.PHONY: validate test status package demo ui review

validate:
	PYTHONPATH=src python scripts/validate_all_v2.py

test:
	PYTHONPATH=src python -m pytest -q

status:
	python scripts/build_status_report.py examples/episode/manifest.json

package:
	python scripts/build_v2_package.py

demo:
	PYTHONPATH=src python scripts/run_demo.py

ui:
	PYTHONPATH=src python scripts/run_ui.py

review:
	python review/serve.py
