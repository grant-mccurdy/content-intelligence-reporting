# Content Intelligence Reporting

Generalized content intelligence pipeline for turning unstructured content into a searchable corpus and producing targeted, source-grounded analytical reports.

This repository is intended to demonstrate the public-safe version of a private workflow originally developed around transcript/corpus construction and analytical reporting. The public version must use sanitized, synthetic, or public-license source material.

## What This Project Demonstrates

- Unstructured text processing
- Transcript or corpus construction
- Content extraction
- Source-grounded analysis
- AI-assisted analytical workflows
- Task-specific report generation
- Reproducible pipeline design

## Current Structure

```text
content-intelligence-reporting/
├── corpus_pipeline/
│   ├── __init__.py
│   └── common.py
├── data/
│   ├── synthetic/
│   │   └── source_docs/
│   └── processed/
│   └── public_sample/
├── scripts/
│   ├── build_manifest.py
│   ├── build_corpus.py
│   ├── search_corpus.py
│   └── generate_report.py
├── reports/
├── sample_outputs/
├── docs/
│   ├── pipeline-overview.md
│   ├── source-grounding.md
│   └── privacy-and-copyright.md
├── screenshots/
└── README.md
```

## Quick Demo

The current scaffold is offline and standard-library only.

```bash
make demo
make search QUERY="feedback rubric evidence"
```

If `make` is unavailable, run the same steps directly:

```bash
python3 scripts/build_manifest.py
python3 scripts/build_corpus.py
python3 scripts/generate_report.py
python3 scripts/search_corpus.py "feedback rubric evidence"
```

The demo builds:

- `data/processed/manifest.json`
- `data/processed/corpus.json`
- `sample_outputs/demo-report.md`

Generated outputs are reproducible and intentionally ignored where appropriate.
The committed sources use synthetic public-safe notes only.

## Public Safety Rules

Do not publish professor names, university course identifiers, private LMS links, copyrighted transcripts, raw lecture text, video URLs, private lecture manifests, or coursework-specific prompts.

Public examples should use synthetic transcripts or public-domain/public-license documents with clear source attribution.

## Portfolio Framing

This project should emphasize the transferable pipeline: ingest, normalize, segment, retrieve, cite, and report. The value is source-grounded reporting from messy unstructured content, not the private course context.

## Status

Public-safe scaffold implemented with synthetic input data, manifest creation,
corpus segmentation, transparent keyword retrieval, and a cited sample report.
