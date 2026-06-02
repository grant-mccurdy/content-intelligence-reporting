.PHONY: demo manifest corpus report search clean

PYTHON ?= python3
QUERY ?= source grounded report citations

demo: manifest corpus report

manifest:
	$(PYTHON) scripts/build_manifest.py

corpus: manifest
	$(PYTHON) scripts/build_corpus.py

report: corpus
	$(PYTHON) scripts/generate_report.py

search: corpus
	$(PYTHON) scripts/search_corpus.py "$(QUERY)"

clean:
	rm -rf data/processed sample_outputs/demo-report.md

