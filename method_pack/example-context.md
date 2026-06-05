# Example AI Context

An AI or algorithm should receive bounded context like this:

```text
Task: Produce a source-grounded instructional analysis brief.

Inputs:
- CorpusSegment objects relevant to the question
- SourceManifestRecord objects for provenance
- public-safety constraints

Output:
- ReportBrief with EvidenceCitation objects
```

The AI should answer from the supplied objects, cite supporting segments, and
state when evidence is insufficient.
