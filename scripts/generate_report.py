#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from search_corpus import search


DEFAULT_QUESTIONS = [
    "What source-grounding and citation practices does the workflow need?",
    "What workflow controls should remain under teacher or reviewer judgment?",
    "What public safety rules govern the demo corpus?",
]


def result_to_evidence(question: str, result: dict, rank: int) -> dict:
    return {
        "object_type": "EvidenceCitation",
        "question": question,
        "rank": rank,
        "segment_id": result["segment_id"],
        "source_id": result["source_id"],
        "citation": result["citation"],
        "score": result["score"],
        "excerpt": result["text"],
    }


def write_report_brief(path: Path, questions: list[str], evidence: list[dict]) -> None:
    brief = {
        "object_type": "ReportBrief",
        "schema_version": 1,
        "title": "Source-Grounded Content Intelligence Demo Report",
        "questions": questions,
        "evidence_citations": evidence,
        "public_safety": {
            "uses_synthetic_sources": True,
            "contains_private_content": False,
        },
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(brief, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"wrote {path}")


def generate_report(corpus_path: Path, out_path: Path, json_out_path: Path | None) -> None:
    lines = [
        "# Source-Grounded Content Intelligence Demo Report",
        "",
        "This sample report is generated from synthetic public-safe source documents.",
        "It demonstrates retrieval with visible citations rather than private content.",
        "",
    ]
    evidence_citations = []
    for question in DEFAULT_QUESTIONS:
        results = search(corpus_path, question, limit=2)
        lines.append(f"## {question}")
        lines.append("")
        if not results:
            lines.append("No supporting passage found in the demo corpus.")
            lines.append("")
            continue
        for rank, result in enumerate(results, start=1):
            excerpt = result["text"].replace("\n", " ")
            if len(excerpt) > 360:
                excerpt = excerpt[:357].rstrip() + "..."
            lines.append(f"- **{result['citation']}**: {excerpt}")
            evidence_citations.append(result_to_evidence(question, result, rank))
        lines.append("")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {out_path}")
    if json_out_path:
        write_report_brief(json_out_path, DEFAULT_QUESTIONS, evidence_citations)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a cited demo report.")
    parser.add_argument("--corpus", default="data/processed/corpus.json")
    parser.add_argument("--out", default="sample_outputs/demo-report.md")
    parser.add_argument("--json-out", default="sample_outputs/report-brief.json")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    generate_report(Path(args.corpus), Path(args.out), Path(args.json_out) if args.json_out else None)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
