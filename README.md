# Content Intelligence Reporting

Generalized content intelligence pipeline for turning unstructured instructional
artifacts into analysis-ready information objects, searchable corpora, and
source-grounded analytical reports.

Primary artifact: an AI-readable analysis method pack for turning instructional
information objects into source-grounded reports.

This repository is intended to demonstrate the public-safe version of a private workflow originally developed around transcript/corpus construction and analytical reporting. The public version must use sanitized, synthetic, or public-license source material.

## What This Project Demonstrates

- Unstructured text processing
- Transcript or corpus construction
- Media-to-transcript ingestion
- OCR cleanup and document-to-corpus ingestion
- Content extraction
- Source-grounded analysis
- Analysis-ready information objects
- AI-assisted analytical workflows
- Task-specific report generation
- Reproducible pipeline design

## Featured Workflow

The core project pattern is:

```text
instructional artifacts
-> source manifest records
-> normalized artifacts
-> corpus segments
-> evidence citations
-> report briefs / agent-ready context
```

See `docs/information-object-model.md` for the object model and `schemas/` for
public-safe JSON examples.

## Primary Artifact

The canonical artifact is `sample_outputs/analysis-method-pack.json`: an
AI-readable method pack that tells an agent or algorithm how to consume the
information objects, cite evidence, preserve uncertainty, and avoid private
source leakage.

The source method pack lives in `method_pack/` with human-readable companions:

- `method_pack/reporting-rules.md`
- `method_pack/source-use-policy.md`
- `method_pack/example-context.md`

## What To Inspect First

- `sample_outputs/analysis-method-pack.json`: AI-readable reporting method contract.
- `docs/information-object-model.md`: the reusable object model.
- `docs/using-information-objects.md`: how algorithms, reports, and agents use the objects.
- `sample_outputs/information-object-map.json`: object counts across all demos.
- `sample_outputs/report-brief.json`: structured report output with cited evidence.
- `demos/cloud_video_transcription/`: staged media-to-corpus simulation.
- `demos/ocr_document_cleanup/`: OCR cleanup-to-corpus simulation.

### Cloud Video-to-Corpus Ingestion

`docs/cloud-video-transcription-workflow.md` documents a public-safe version of
a real workflow for turning cloud-hosted instructional videos into cleaned,
searchable transcript artifacts. The demo uses synthetic filenames and sample
text, but preserves the transferable engineering pattern:

```text
cloud video inventory
-> media selection
-> temporary private download
-> audio chunking
-> transcription
-> transcript cleanup
-> manifest and corpus-ready artifacts
```

Run the synthetic demo:

```bash
python3 demos/cloud_video_transcription/run_demo.py
```

### OCR Notes-to-Corpus Cleanup

`demos/ocr_document_cleanup/` demonstrates the adjacent workflow for turning
OCR text from document images into cleaned, citation-ready corpus records.

```bash
python3 demos/ocr_document_cleanup/run_demo.py
```

Build the full object map:

```bash
make portfolio-demo
```

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
│   ├── generate_report.py
│   ├── build_information_object_map.py
│   └── build_analysis_method_pack.py
├── demos/
│   ├── cloud_video_transcription/
│   └── ocr_document_cleanup/
├── reports/
├── sample_outputs/
├── docs/
│   ├── information-object-model.md
│   ├── pipeline-overview.md
│   ├── cloud-video-transcription-workflow.md
│   ├── cleanup-policy.md
│   ├── using-information-objects.md
│   ├── source-grounding.md
│   └── privacy-and-copyright.md
├── schemas/
├── method_pack/
├── screenshots/
└── README.md
```

## Quick Demo

The current scaffold is offline and standard-library only.

```bash
make demo
make search QUERY="feedback rubric evidence"
make validate
make portfolio-demo
```

If `make` is unavailable, run the same steps directly:

```bash
python3 scripts/build_manifest.py
python3 scripts/build_corpus.py
python3 scripts/generate_report.py
python3 scripts/search_corpus.py "feedback rubric evidence"
python3 scripts/build_analysis_method_pack.py
python3 scripts/validate_information_objects.py
```

The demo builds:

- `data/processed/manifest.json`
- `data/processed/corpus.json`
- `sample_outputs/demo-report.md`
- `sample_outputs/report-brief.json`
- `sample_outputs/analysis-method-pack.json`

Generated outputs are reproducible and intentionally ignored where appropriate.
The committed sources use synthetic public-safe notes only.

## Public Safety Rules

Do not publish professor names, university course identifiers, private LMS links, copyrighted transcripts, raw lecture text, video URLs, private lecture manifests, or coursework-specific prompts.

Public examples should use synthetic transcripts or public-domain/public-license documents with clear source attribution.

## Portfolio Framing

This project should emphasize the transferable pipeline: ingest, normalize,
segment, retrieve, cite, and report. The value is converting messy instructional
artifacts into reusable information objects, not the private course context.

## Status

Public-safe scaffold implemented with synthetic input data, manifest creation,
corpus segmentation, transparent keyword retrieval, and a cited sample report.
