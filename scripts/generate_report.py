#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from search_corpus import search


DEFAULT_QUESTIONS = [
    "What source-grounding and citation practices does the workflow need?",
    "What workflow controls should remain under teacher or reviewer judgment?",
    "What public safety rules govern the demo corpus?",
]


def generate_report(corpus_path: Path, out_path: Path) -> None:
    lines = [
        "# Source-Grounded Content Intelligence Demo Report",
        "",
        "This sample report is generated from synthetic public-safe source documents.",
        "It demonstrates retrieval with visible citations rather than private content.",
        "",
    ]
    for question in DEFAULT_QUESTIONS:
        results = search(corpus_path, question, limit=2)
        lines.append(f"## {question}")
        lines.append("")
        if not results:
            lines.append("No supporting passage found in the demo corpus.")
            lines.append("")
            continue
        for result in results:
            excerpt = result["text"].replace("\n", " ")
            if len(excerpt) > 360:
                excerpt = excerpt[:357].rstrip() + "..."
            lines.append(f"- **{result['citation']}**: {excerpt}")
        lines.append("")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {out_path}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a cited demo report.")
    parser.add_argument("--corpus", default="data/processed/corpus.json")
    parser.add_argument("--out", default="sample_outputs/demo-report.md")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    generate_report(Path(args.corpus), Path(args.out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
