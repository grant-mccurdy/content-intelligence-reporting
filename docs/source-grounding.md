# Source Grounding

Every generated segment carries:

- `segment_id`
- `source_id`
- source title
- source type
- citation label
- original segment text

Reports should cite the segment that supports each claim. A report generator
should not make claims that cannot be traced back to retrieved source material.

For a production version, the next step would be stronger retrieval: embeddings,
hybrid keyword/vector search, reranking, and passage-level citation spans. The
public scaffold starts with keyword search because it is transparent and easy to
audit.

