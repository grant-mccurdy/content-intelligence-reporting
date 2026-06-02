#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from corpus_pipeline.common import read_text, slugify, write_json


def parse_metadata(text: str) -> dict[str, str]:
    metadata: dict[str, str] = {}
    for line in text.splitlines():
        if not line.strip():
            break
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        metadata[key.strip().lower().replace(" ", "_")] = value.strip()
    return metadata


def build_manifest(source_dir: Path) -> dict:
    records = []
    for path in sorted(source_dir.glob("*.txt")):
        text = read_text(path)
        digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
        metadata = parse_metadata(text)
        title = metadata.get("title") or path.stem.replace("-", " ").title()
        source_id = slugify(title)
        records.append(
            {
                "source_id": source_id,
                "title": title,
                "source_type": metadata.get("source_type", "text"),
                "license": metadata.get("license", "unknown"),
                "path": str(path),
                "sha256": digest,
                "status": "identified",
            }
        )
    return {"schema_version": 1, "source_count": len(records), "sources": records}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a public-safe source manifest.")
    parser.add_argument("--source-dir", default="data/synthetic/source_docs")
    parser.add_argument("--out", default="data/processed/manifest.json")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    manifest = build_manifest(Path(args.source_dir))
    write_json(Path(args.out), manifest)
    print(f"wrote {args.out} ({manifest['source_count']} sources)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
