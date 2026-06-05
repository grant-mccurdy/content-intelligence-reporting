# Using Information Objects

The generated objects are intended to be consumed by downstream tools rather
than read as raw files.

## Search Algorithm

A search step consumes `CorpusSegment` objects. It can rank segments by keyword,
embedding similarity, tags, or any other retrieval method while preserving
`segment_id`, `source_id`, and `citation`.

## Report Generator

A report generator consumes retrieved segments and emits `EvidenceCitation`
objects. The Markdown report is a presentation layer; `report-brief.json` is the
structured object that preserves questions, evidence, scores, and citations.

## Agent Context

An agent should consume bounded objects, not raw instructional artifacts. A
typical context package would include:

- the user question or task
- a small set of `CorpusSegment` objects
- prior `EvidenceCitation` objects when available
- public-safety or source-use constraints

The agent can then produce a draft answer, report, or next-step recommendation
while retaining auditable links back to source segments.

## Algorithmic Analysis

The same objects can support non-agentic analysis:

- count source types in a manifest
- cluster corpus segments by concept vocabulary
- audit which reports cite which source records
- detect stale or unprocessed artifacts from status fields
