# Pipeline Overview

This public demo turns messy source text into a cited report using only
synthetic material.

```text
source documents
-> manifest with checksums and source metadata
-> normalized corpus
-> source-preserving segments
-> keyword retrieval
-> cited report
```

The private `ms-statistics` workspace proved the value of a manifest-driven
workflow for media transcription, transcript cleaning, and source indexing. This
repo keeps the transferable architecture while removing private course content,
private Dropbox paths, raw transcripts, and course-specific prompts.

## Scripts

- `scripts/build_manifest.py` records source IDs, titles, source types,
  licenses, file paths, checksums, and status.
- `scripts/build_corpus.py` strips demo metadata, normalizes whitespace, and
  creates citation-preserving text segments.
- `scripts/search_corpus.py` performs simple keyword retrieval over segments.
- `scripts/generate_report.py` creates a short cited report from the corpus.

## Run

```bash
make demo
make search QUERY="feedback rubric evidence"
```

Direct Python equivalent:

```bash
python3 scripts/build_manifest.py
python3 scripts/build_corpus.py
python3 scripts/generate_report.py
python3 scripts/search_corpus.py "feedback rubric evidence"
```

The current demo does not call external APIs. Future private adapters can add
Dropbox, OpenAI transcription, OCR, or embedding search behind explicit
configuration and approval.
