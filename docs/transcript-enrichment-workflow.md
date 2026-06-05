# Transcript Enrichment Workflow

This workflow shows how raw machine transcripts become cleaner, more useful
information objects before they enter search, analysis, or reporting systems.
It is based on a private workflow that used OpenAI transcription and a second
OpenAI cleanup pass, but this public repository uses only synthetic offline
artifacts.

## Pattern

```text
raw machine transcript
-> bounded transcript chunk
-> domain context packet
-> guarded cleanup prompt
-> cleaned transcript
-> correction notes
-> normalized artifact
-> corpus segments
```

## Why The Enrichment Pass Matters

Raw transcripts are often technically complete but analytically weak. They may
contain repeated recognition errors, inconsistent terminology, dropped
punctuation, and ambiguous phrases. The enrichment step improves downstream
utility while preserving the original meaning and uncertainty.

The cleanup pass is intentionally conservative:

- correct clear transcription errors
- normalize known domain terms
- preserve speaker sequence
- keep `[unclear]` markers
- record correction notes separately from the transcript text
- avoid adding facts that are not present in the source

## Public-Safe Demo Artifact

Run the media demo:

```bash
python3 demos/cloud_video_transcription/run_demo.py
```

Then inspect:

- `sample_outputs/cloud_video_transcription/transcript_enrichment_brief.md`
- `sample_outputs/cloud_video_transcription/enrichment_packets/*.json`
- `sample_outputs/cloud_video_transcription/clean_transcript_excerpt.md`

The enrichment packet mirrors the useful structure of an OpenAI Responses-style
cleanup call: system prompt, domain context, input contract, output contract,
correction notes, raw excerpt, clean excerpt, and public-safety metadata.

## Portfolio Claim

The important skill is not simply calling a transcription API. The useful
workflow is turning a noisy generated transcript into a reviewed, bounded,
source-preserving information object that can safely support retrieval,
analysis, and reporting.
