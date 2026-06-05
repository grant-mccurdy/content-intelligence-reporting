#!/usr/bin/env python3
"""Run a synthetic OCR cleanup to corpus demo."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
DEMO_ROOT = Path(__file__).resolve().parent
DEFAULT_INPUT = DEMO_ROOT / "sample_ocr_pages.json"
DEFAULT_OUT = REPO_ROOT / "sample_outputs" / "ocr_document_cleanup"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def clean_ocr_text(text: str) -> str:
    replacements = {
        "manafest": "manifest",
        "errrors": "errors",
        "segmnts": "segments",
        "retrival": "retrieval",
    }
    cleaned = text
    for old, new in replacements.items():
        cleaned = re.sub(old, new, cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"[ \t]+", " ", cleaned)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned.strip())
    return cleaned


def build_outputs(payload: dict[str, Any]) -> tuple[dict[str, Any], str, dict[str, Any]]:
    document = payload["document"]
    cleaned_pages = []
    segments = []
    for page in payload["pages"]:
        cleaned = clean_ocr_text(page["ocr_text"])
        cleaned_pages.append(f"## Page {page['page']}\n\n{cleaned}")
        segment_id = f"synthetic-notes#p{int(page['page']):03d}"
        segments.append(
            {
                "segment_id": segment_id,
                "source_id": "synthetic-notes",
                "title": document["title"],
                "source_type": document["source_type"],
                "text": cleaned,
                "citation": f"{document['title']}, page {page['page']}",
            }
        )

    cleaned_notes = "# Cleaned Synthetic Notes\n\n" + "\n\n".join(cleaned_pages) + "\n"
    manifest = {
        "schema_version": 1,
        "demo": "ocr_document_cleanup",
        "source": payload["source"],
        "document": document,
        "page_count": len(payload["pages"]),
        "cleaned_sha256": sha256_text(cleaned_notes),
        "pages": [
            {
                "page": page["page"],
                "image_artifact": page["image_artifact"],
                "ocr_status": "simulated",
                "cleanup_status": "simulated_conservative_cleanup",
            }
            for page in payload["pages"]
        ],
        "public_safety": {
            "uses_synthetic_pages": True,
            "contains_real_notes": False,
            "requires_credentials": False,
        },
    }
    corpus = {"schema_version": 1, "segment_count": len(segments), "segments": segments}
    return manifest, cleaned_notes, corpus


def write_outputs(out_dir: Path, manifest: dict[str, Any], cleaned_notes: str, corpus: dict[str, Any]) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    write_json(out_dir / "manifest.json", manifest)
    (out_dir / "cleaned_notes.md").write_text(cleaned_notes, encoding="utf-8")
    write_json(out_dir / "corpus.json", corpus)
    summary = (
        "# Workflow Summary\n\n"
        f"- Synthetic pages processed: {manifest['page_count']}\n"
        "- Stages shown: source page inventory, OCR text capture, conservative cleanup, "
        "manifesting, corpus segmentation\n"
        "- Reuse pattern: image/PDF OCR can feed the same corpus and reporting pipeline "
        "as transcripts\n"
        "- Public safety: no real notes, private images, credentials, or copyrighted source text\n"
    )
    (out_dir / "workflow_summary.md").write_text(summary, encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the synthetic OCR cleanup demo.")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    payload = load_json(args.input)
    manifest, cleaned_notes, corpus = build_outputs(payload)
    write_outputs(args.out, manifest, cleaned_notes, corpus)
    print(f"wrote {args.out / 'manifest.json'}")
    print(f"wrote {args.out / 'cleaned_notes.md'}")
    print(f"wrote {args.out / 'corpus.json'}")
    print(f"wrote {args.out / 'workflow_summary.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
