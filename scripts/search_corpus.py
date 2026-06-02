#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from corpus_pipeline.common import load_json, tokenize

STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "by",
    "for",
    "from",
    "in",
    "is",
    "it",
    "of",
    "or",
    "that",
    "the",
    "to",
    "with",
}


def score_segment(query_terms: list[str], text: str) -> int:
    counts = Counter(tokenize(text))
    return sum(counts[term] for term in query_terms)


def search(corpus_path: Path, query: str, limit: int) -> list[dict]:
    corpus = load_json(corpus_path)
    query_terms = [term for term in tokenize(query) if term not in STOPWORDS]
    scored = []
    for segment in corpus["segments"]:
        score = score_segment(query_terms, segment["text"])
        if score > 0:
            scored.append((score, segment))
    scored.sort(key=lambda item: (-item[0], item[1]["segment_id"]))
    return [{"score": score, **segment} for score, segment in scored[:limit]]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Keyword search over the demo corpus.")
    parser.add_argument("query")
    parser.add_argument("--corpus", default="data/processed/corpus.json")
    parser.add_argument("--limit", type=int, default=5)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    for result in search(Path(args.corpus), args.query, args.limit):
        print(f"[{result['score']}] {result['segment_id']} - {result['citation']}")
        print(result["text"].replace("\n", " "))
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
