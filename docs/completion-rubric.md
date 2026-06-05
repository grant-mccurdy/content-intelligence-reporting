# Completion Rubric

This repository is complete when it works as a public, portfolio-ready example
of converting messy instructional artifacts into AI-readable information objects
and source-grounded reporting methods.

## Goal Condition

A reviewer should be able to understand, run, and evaluate the workflow without
access to private course material, private cloud storage, copyrighted
transcripts, or institution-specific context.

## Completion Criteria

| Criterion | Status | Evidence |
| --- | --- | --- |
| Public-safe source material | Complete | Synthetic source documents and demo records only. |
| Reproducible local demo | Complete | `make portfolio-demo` rebuilds the demo outputs. |
| Information object model | Complete | `docs/information-object-model.md` and `schemas/`. |
| Source manifest records | Complete | `scripts/build_manifest.py` and `data/processed/manifest.json`. |
| Corpus segments | Complete | `scripts/build_corpus.py` and `data/processed/corpus.json`. |
| Evidence-grounded report object | Complete | `scripts/generate_report.py` and `sample_outputs/report-brief.json`. |
| AI-readable method pack | Complete | `method_pack/` and `sample_outputs/analysis-method-pack.json`. |
| Media ingestion workflow | Complete | `docs/cloud-video-transcription-workflow.md` and `demos/cloud_video_transcription/`. |
| OCR cleanup workflow | Complete | `demos/ocr_document_cleanup/`. |
| Generated object validation | Complete | `scripts/validate_information_objects.py`. |
| Reviewer path | Complete | README reviewer path and `docs/workflow-diagram.md`. |

## Non-Goals

- Publishing private course notes, lecture transcripts, LMS links, or cloud
  storage paths.
- Downloading or storing large media files in the public repository.
- Building a production ingestion service.
- Replacing the transparent demo retrieval with opaque ranking logic.

## Remaining Portfolio Work

The repository itself is functionally complete. Remaining work should happen at
the portfolio layer:

- Pin the repository on GitHub.
- Reference it from a GitHub profile README or portfolio site.
- Add a short project blurb focused on information design, source grounding,
  and AI-readable analysis objects.
- Optionally add a screenshot of the generated object map or report brief if the
  portfolio surface benefits from a visual.
