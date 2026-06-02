#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from corpus_pipeline.common import load_json, normalize_whitespace, read_text, write_json


def body_without_metadata(text: str) -> str:
    parts = text.split("\n\n", 1)
    return parts[1] if len(parts) == 2 else text


def segment_text(text: str, max_chars: int) -> list[str]:
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    segments: list[str] = []
    buffer: list[str] = []
    size = 0
    for paragraph in paragraphs:
        if buffer and size + len(paragraph) + 2 > max_chars:
            segments.append("\n\n".join(buffer))
            buffer = []
            size = 0
        buffer.append(paragraph)
        size += len(paragraph) + 2
    if buffer:
        segments.append("\n\n".join(buffer))
    return segments


def build_corpus(manifest_path: Path, max_chars: int) -> dict:
    manifest = load_json(manifest_path)
    records = []
    for source in manifest["sources"]:
        text = normalize_whitespace(body_without_metadata(read_text(Path(source["path"]))))
        for idx, segment in enumerate(segment_text(text, max_chars), start=1):
            segment_id = f"{source['source_id']}#{idx:02d}"
            records.append(
                {
                    "segment_id": segment_id,
                    "source_id": source["source_id"],
                    "title": source["title"],
                    "source_type": source["source_type"],
                    "text": segment,
                    "citation": f"{source['title']}, segment {idx}",
                }
            )
    return {"schema_version": 1, "segment_count": len(records), "segments": records}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Normalize and segment source text.")
    parser.add_argument("--manifest", default="data/processed/manifest.json")
    parser.add_argument("--out", default="data/processed/corpus.json")
    parser.add_argument("--max-chars", type=int, default=550)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    corpus = build_corpus(Path(args.manifest), args.max_chars)
    write_json(Path(args.out), corpus)
    print(f"wrote {args.out} ({corpus['segment_count']} segments)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
