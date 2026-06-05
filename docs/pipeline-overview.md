# Pipeline Overview

This public demo turns messy instructional artifacts into analysis-ready
information objects using only synthetic material.

```text
instructional artifacts
-> source manifest records
-> normalized artifacts
-> corpus segments
-> evidence citations
-> report briefs
```

A private prototype proved the value of a manifest-driven workflow for media
transcription, transcript cleaning, and source indexing. This repo keeps the
transferable architecture while removing private course content, private cloud
paths, raw transcripts, and course-specific prompts.

## Scripts

- `scripts/build_manifest.py` records source IDs, titles, source types,
  licenses, file paths, checksums, and status.
- `scripts/build_corpus.py` strips demo metadata, normalizes whitespace, and
  creates citation-preserving text segments.
- `scripts/search_corpus.py` performs simple keyword retrieval over segments.
- `scripts/generate_report.py` creates a short cited report from the corpus.
- `scripts/build_information_object_map.py` summarizes the generated object
  families across the text, media, and OCR demos.
- `demos/cloud_video_transcription/run_demo.py` shows staged media-to-transcript
  ingestion with synthetic cloud records.
- `demos/ocr_document_cleanup/run_demo.py` shows OCR cleanup and corpus
  preparation with synthetic page records.

## Run

```bash
make demo
make portfolio-demo
make search QUERY="feedback rubric evidence"
```

Direct Python equivalent:

```bash
python3 scripts/build_manifest.py
python3 scripts/build_corpus.py
python3 scripts/generate_report.py
python3 scripts/build_information_object_map.py
python3 scripts/search_corpus.py "feedback rubric evidence"
```

The current demo does not call external APIs. Future private adapters can add
Dropbox, OpenAI transcription, OCR, or embedding search behind explicit
configuration and approval.
