# Cloud Video-to-Transcript Workflow

This case study describes a public-safe version of a workflow for converting
cloud-hosted instructional videos into cleaned transcript artifacts that can be
searched, reviewed, and transformed into source-grounded reports.

The public repository intentionally uses synthetic examples. It does not contain
real lecture videos, transcript text, private folder names, cloud metadata,
participant names, or course identifiers.

## Problem

Instructional videos are useful but expensive to work with directly. They are
large, slow to download, and difficult to search. A better workflow keeps the
media private and temporary, then promotes only the smallest useful text and
metadata artifacts for corpus construction and reporting.

The working pattern is:

```text
cloud video inventory
-> select relevant media
-> download only when regeneration is needed
-> split audio into bounded chunks
-> transcribe each chunk
-> enrich transcript with domain context
-> record source manifest and processing status
-> build searchable corpus segments
-> cite transcript-derived evidence in reports
```

## Pipeline Design

1. Inventory the cloud folder recursively and filter to media extensions such as
   `.mp4`, `.mov`, `.m4a`, and `.mp3`.
2. Store a manifest with file size, content hash when available, modified time,
   stage status, and local artifact paths.
3. Download raw video only into ignored private directories when a transcript
   must be generated or repaired.
4. Extract mono audio chunks with a bounded duration so transcription requests
   are predictable and retryable.
5. Generate raw transcripts per chunk, then combine them into one raw transcript
   per video.
6. Run a cleanup/enrichment pass that sends bounded transcript chunks, domain
   context, and conservative editing rules through an OpenAI-style response
   workflow. The public demo simulates this step offline.
7. Segment cleaned transcripts into corpus records with stable source IDs.
8. Keep raw videos, audio chunks, and full transcripts private. Publish only
   synthetic examples, aggregate summaries, workflow diagrams, and reviewed
   schemas.

## Why This Belongs Here

This workflow is upstream content intelligence. It turns unstructured media into
structured text artifacts that can later support retrieval, source-grounded
analysis, and reporting. Teacher-facing rubric, feedback, and remediation flows
belong in the separate instructional workflow project.

## Public-Safe Demo

The runnable demo in `demos/cloud_video_transcription/` simulates the workflow
with fake cloud entries and synthetic transcript text:

```bash
python3 demos/cloud_video_transcription/run_demo.py
```

The demo writes:

- `sample_outputs/cloud_video_transcription/manifest.json`
- `sample_outputs/cloud_video_transcription/clean_transcript_excerpt.md`
- `sample_outputs/cloud_video_transcription/transcript_enrichment_brief.md`
- `sample_outputs/cloud_video_transcription/enrichment_packets/*.json`
- `sample_outputs/cloud_video_transcription/workflow_summary.md`
- `sample_outputs/cloud_video_transcription/corpus.json`

It requires only the Python standard library. No network access, credentials,
media files, or transcription API calls are used.

See `docs/transcript-enrichment-workflow.md` for the public-safe version of the
raw-transcript-to-clean-transcript OpenAI cleanup pattern.

The demo intentionally exposes stage-level commands (`list`, `download`,
`transcribe`, `clean`, `prepare-corpus`, and `run`) to show how a larger private
workflow can be made resumable, auditable, and idempotent without publishing the
private source material.

## Privacy Boundary

Public artifacts may include:

- synthetic media listings
- generalized workflow diagrams
- manifest schemas with fake paths
- short synthetic transcript excerpts
- aggregate counts and processing statuses

Public artifacts must not include:

- raw videos or audio
- full transcripts
- real participant names, voices, questions, or comments
- private cloud paths or access metadata
- private local paths
- source text copied from instructional material
