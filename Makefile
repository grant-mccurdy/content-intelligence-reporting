.PHONY: demo manifest corpus report search media-demo ocr-demo object-map validate portfolio-demo clean

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

media-demo:
	$(PYTHON) demos/cloud_video_transcription/run_demo.py

ocr-demo:
	$(PYTHON) demos/ocr_document_cleanup/run_demo.py

object-map: report media-demo ocr-demo
	$(PYTHON) scripts/build_information_object_map.py

validate:
	$(PYTHON) scripts/validate_information_objects.py

portfolio-demo: demo media-demo ocr-demo object-map validate

clean:
	rm -rf data/processed sample_outputs/demo-report.md sample_outputs/report-brief.json sample_outputs/information-object-map.json sample_outputs/cloud_video_transcription sample_outputs/ocr_document_cleanup
