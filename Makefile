.PHONY: validate test status package

validate:
	PYTHONPATH=src python scripts/validate_all_v2.py

test:
	PYTHONPATH=src python -m pytest -q

status:
	python scripts/build_status_report.py examples/episode/manifest.json

package:
	python scripts/build_v2_package.py
