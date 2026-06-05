# Reporting Rules

Reports should be evidence-first. The reporting process is:

```text
question
-> retrieve CorpusSegment objects
-> produce EvidenceCitation objects
-> write ReportBrief narrative
-> preserve citation links
```

Rules:

- Every substantive claim needs cited evidence.
- Inference must be labeled as inference.
- Missing evidence should be reported as a gap, not filled in.
- The Markdown report is presentation; `ReportBrief` is the structured output.
