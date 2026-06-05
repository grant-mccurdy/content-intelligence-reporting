#!/usr/bin/env python3
"""Run a synthetic cloud video-to-transcript workflow demo.

The private workflow this demo is based on used cloud inventory, selective
download, ffmpeg audio chunking, transcription, cleanup, and manifest updates.
This public version preserves those mechanics with synthetic data and
standard-library-only processing.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
DEMO_ROOT = Path(__file__).resolve().parent
DEFAULT_INPUT = DEMO_ROOT / "sample_cloud_listing.json"
DEFAULT_RAW_TRANSCRIPT = DEMO_ROOT / "sample_transcript_raw.txt"
DEFAULT_OUT = REPO_ROOT / "sample_outputs" / "cloud_video_transcription"
MEDIA_EXTENSIONS = {".mp4", ".mov", ".m4v", ".webm", ".mkv", ".avi", ".mp3", ".wav", ".m4a"}
CHUNK_TARGET_BYTES = 125_000_000
TRANSCRIPT_ENRICHMENT_SYSTEM_PROMPT = (
    "Clean a machine transcript for downstream analysis. Correct obvious "
    "recognition errors, preserve the speaker's meaning and sequence, keep "
    "uncertainty markers such as [unclear], and return only cleaned transcript "
    "text plus structured correction notes."
)
SYNTHETIC_DOMAIN_CONTEXT = {
    "course_context": "Public synthetic applied learning seminar.",
    "likely_terms": [
        "manifest",
        "retrieval",
        "corpus segment",
        "source-grounded report",
        "citation",
    ],
    "privacy_boundary": [
        "no private names",
        "no real course identifiers",
        "no raw private transcripts",
        "no credentials",
    ],
}


def load_json(path: Path, default: dict[str, Any] | None = None) -> dict[str, Any]:
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return default or {}


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def is_media(entry: dict[str, Any]) -> bool:
    return Path(str(entry.get("name", ""))).suffix.lower() in MEDIA_EXTENSIONS


def safe_artifact_stem(entry: dict[str, Any]) -> str:
    stem = Path(str(entry.get("name", "unnamed"))).stem.lower()
    stem = re.sub(r"[^a-z0-9]+", "_", stem).strip("_")
    return stem or "unnamed"


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def natural_sort_key(value: str) -> list[int | str]:
    return [int(part) if part.isdigit() else part.lower() for part in re.split(r"(\d+)", value)]


def select_media_entries(
    listing: dict[str, Any],
    *,
    match: str | None,
    min_size_mb: float,
    limit: int | None,
) -> list[dict[str, Any]]:
    entries = [entry for entry in listing.get("entries", []) if is_media(entry)]
    entries.sort(key=lambda item: natural_sort_key(str(item.get("path_display") or item.get("name") or "")))
    if match:
        pattern = re.compile(match, re.IGNORECASE)
        entries = [
            entry
            for entry in entries
            if pattern.search(str(entry.get("path_display", ""))) or pattern.search(str(entry.get("name", "")))
        ]
    if min_size_mb > 0:
        min_size = min_size_mb * 1024 * 1024
        entries = [entry for entry in entries if int(entry.get("size") or 0) >= min_size]
    if limit is not None:
        entries = entries[:limit]
    return entries


def manifest_path(out_dir: Path) -> Path:
    return out_dir / "manifest.json"


def load_manifest(out_dir: Path) -> dict[str, Any]:
    return load_json(
        manifest_path(out_dir),
        {
            "schema_version": 1,
            "demo": "cloud_video_transcription",
            "source": "synthetic_cloud_listing",
            "files": [],
            "public_safety": {
                "uses_synthetic_listing": True,
                "contains_real_media": False,
                "contains_real_transcripts": False,
                "requires_credentials": False,
            },
        },
    )


def manifest_by_source(manifest: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {str(item.get("source_path")): item for item in manifest.get("files", [])}


def prepare_record(entry: dict[str, Any], out_dir: Path) -> dict[str, Any]:
    stem = safe_artifact_stem(entry)
    size = int(entry.get("size") or 0)
    return {
        "source_name": entry.get("name"),
        "source_path": entry.get("path_display"),
        "server_modified": entry.get("server_modified"),
        "size_bytes": size,
        "source_hash": entry.get("content_hash"),
        "download_status": "not_started",
        "audio_chunk_count": max(1, math.ceil(size / CHUNK_TARGET_BYTES)),
        "audio_chunk_artifact": str(Path("audio_chunks") / stem),
        "transcription_status": "not_started",
        "cleanup_status": "not_started",
        "enrichment_status": "not_started",
        "corpus_status": "not_started",
        "raw_media_artifact": str(Path("working_media_stubs") / f"{stem}.placeholder.txt"),
        "raw_transcript_artifact": str(Path("transcripts_raw") / f"{stem}.raw.txt"),
        "clean_transcript_artifact": str(Path("transcripts_clean") / f"{stem}.txt"),
        "enrichment_artifact": str(Path("enrichment_packets") / f"{stem}.json"),
        "corpus_artifact": str(Path("corpus_segments") / f"{stem}.json"),
    }


def merge_record_defaults(record: dict[str, Any], entry: dict[str, Any], out_dir: Path) -> dict[str, Any]:
    merged = prepare_record(entry, out_dir)
    generated_artifact_keys = {
        "raw_media_artifact",
        "raw_transcript_artifact",
        "clean_transcript_artifact",
        "enrichment_artifact",
        "audio_chunk_artifact",
        "corpus_artifact",
    }
    merged.update(
        {
            key: value
            for key, value in record.items()
            if value is not None and key not in generated_artifact_keys
        }
    )
    return merged


def update_manifest_summary(manifest: dict[str, Any], listing: dict[str, Any], cleaned_text: str | None = None) -> None:
    files = manifest.get("files", [])
    manifest["folder"] = listing.get("folder")
    manifest["media_file_count"] = len(files)
    manifest["total_media_size_bytes"] = sum(int(file.get("size_bytes") or 0) for file in files)
    if cleaned_text is not None:
        manifest["clean_excerpt_sha256"] = sha256_text(cleaned_text)


def action_list(args: argparse.Namespace) -> int:
    listing = load_json(args.input)
    entries = select_media_entries(listing, match=args.match, min_size_mb=args.min_size_mb, limit=args.limit)
    for entry in entries:
        print(f"{entry['name']} ({int(entry.get('size') or 0):,} bytes)")
    print(f"matched {len(entries)} synthetic media files")
    return 0


def action_download(args: argparse.Namespace) -> int:
    listing = load_json(args.input)
    selected = select_media_entries(listing, match=args.match, min_size_mb=args.min_size_mb, limit=args.limit)
    manifest = load_manifest(args.out)
    by_source = manifest_by_source(manifest)
    records = []
    for entry in selected:
        source_path = str(entry.get("path_display"))
        record = merge_record_defaults(by_source[source_path], entry, args.out) if source_path in by_source else prepare_record(entry, args.out)
        media_stub = args.out / record["raw_media_artifact"]
        if media_stub.exists() and not args.force_download:
            record["download_status"] = "skipped_existing"
        else:
            media_stub.parent.mkdir(parents=True, exist_ok=True)
            media_stub.write_text(
                f"Synthetic private media placeholder for {record['source_name']}\n",
                encoding="utf-8",
            )
            record["download_status"] = "simulated_private_download"
        records.append(record)
    manifest["files"] = records
    update_manifest_summary(manifest, listing)
    write_json(manifest_path(args.out), manifest)
    print(f"wrote {manifest_path(args.out)} ({len(records)} records)")
    return 0


def action_transcribe(args: argparse.Namespace) -> int:
    manifest = load_manifest(args.out)
    raw_template = args.raw_transcript.read_text(encoding="utf-8").strip()
    for record in manifest.get("files", []):
        raw_path = args.out / record["raw_transcript_artifact"]
        if raw_path.exists() and not args.force_transcribe:
            record["transcription_status"] = "skipped_existing"
            continue
        chunks_dir = args.out / record["audio_chunk_artifact"]
        chunks_dir.mkdir(parents=True, exist_ok=True)
        chunk_texts = []
        for idx in range(1, int(record["audio_chunk_count"]) + 1):
            chunk_path = chunks_dir / f"chunk-{idx:03d}.mp3.txt"
            chunk_path.write_text(
                f"Synthetic audio chunk placeholder {idx} for {record['source_name']}\n",
                encoding="utf-8",
            )
            chunk_texts.append(f"[Chunk {idx:03d}: {chunk_path.name}]\n{raw_template}")
        raw_path.parent.mkdir(parents=True, exist_ok=True)
        raw_path.write_text("\n\n".join(chunk_texts) + "\n", encoding="utf-8")
        record["transcription_status"] = "simulated"
    write_json(manifest_path(args.out), manifest)
    print(f"updated {manifest_path(args.out)}")
    return 0


def clean_transcript(raw_text: str) -> tuple[str, list[dict[str, str]]]:
    replacements = {
        "manafest": "manifest",
        "retrival": "retrieval",
    }
    cleaned = raw_text
    corrections = []
    for old, new in replacements.items():
        matches = re.findall(old, cleaned, flags=re.IGNORECASE)
        if matches:
            corrections.append(
                {
                    "from": old,
                    "to": new,
                    "reason": "obvious synthetic transcription error",
                    "count": str(len(matches)),
                }
            )
            cleaned = re.sub(old, new, cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned.strip())
    return cleaned + "\n", corrections


def build_enrichment_packet(record: dict[str, Any], raw_text: str, cleaned: str, corrections: list[dict[str, str]]) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "object_type": "TranscriptEnrichmentPacket",
        "source_name": record["source_name"],
        "source_path": record["source_path"],
        "stage": "simulated_llm_transcript_cleanup",
        "api_pattern": "OpenAI Responses-style cleanup request, simulated offline",
        "system_prompt": TRANSCRIPT_ENRICHMENT_SYSTEM_PROMPT,
        "domain_context": SYNTHETIC_DOMAIN_CONTEXT,
        "input_contract": {
            "raw_transcript_artifact": record["raw_transcript_artifact"],
            "max_chars_per_request": 6500,
            "preserve_chunk_markers": True,
        },
        "output_contract": {
            "clean_transcript_artifact": record["clean_transcript_artifact"],
            "correction_notes": "recorded separately from cleaned transcript text",
            "allowed_changes": [
                "correct clear recognition errors",
                "normalize obvious terminology",
                "preserve sequence and uncertainty markers",
            ],
            "disallowed_changes": [
                "invent missing content",
                "add private context",
                "remove uncertainty markers",
                "publish raw private transcript text",
            ],
        },
        "corrections": corrections,
        "raw_excerpt": raw_text[:900].strip(),
        "clean_excerpt": cleaned[:900].strip(),
        "public_safety": {
            "uses_synthetic_transcript": True,
            "contains_real_api_response": False,
            "requires_credentials": False,
        },
    }


def action_clean(args: argparse.Namespace) -> int:
    manifest = load_manifest(args.out)
    excerpts = []
    for record in manifest.get("files", []):
        raw_path = args.out / record["raw_transcript_artifact"]
        clean_path = args.out / record["clean_transcript_artifact"]
        if clean_path.exists() and not args.force_clean:
            raw_text = raw_path.read_text(encoding="utf-8")
            cleaned = clean_path.read_text(encoding="utf-8")
            _expected_cleaned, corrections = clean_transcript(raw_text)
            enrichment_path = args.out / record["enrichment_artifact"]
            enrichment_existed = enrichment_path.exists()
            if not enrichment_existed:
                write_json(enrichment_path, build_enrichment_packet(record, raw_text, cleaned, corrections))
            record["enrichment_status"] = "skipped_existing" if enrichment_existed else "simulated"
            record["cleanup_status"] = "skipped_existing"
            excerpts.append(cleaned)
            continue
        raw_text = raw_path.read_text(encoding="utf-8")
        cleaned, corrections = clean_transcript(raw_text)
        clean_path.parent.mkdir(parents=True, exist_ok=True)
        clean_path.write_text(cleaned, encoding="utf-8")
        enrichment_path = args.out / record["enrichment_artifact"]
        write_json(enrichment_path, build_enrichment_packet(record, raw_text, cleaned, corrections))
        record["cleanup_status"] = "simulated_llm_enrichment"
        record["enrichment_status"] = "simulated"
        excerpts.append(cleaned)
    excerpt = excerpts[0] if excerpts else ""
    (args.out / "clean_transcript_excerpt.md").write_text(
        "# Clean Transcript Excerpt\n\n" + excerpt,
        encoding="utf-8",
    )
    write_enrichment_brief(args.out, manifest)
    listing = load_json(args.input)
    update_manifest_summary(manifest, listing, excerpt)
    write_json(manifest_path(args.out), manifest)
    print(f"wrote {args.out / 'clean_transcript_excerpt.md'}")
    return 0


def write_enrichment_brief(out_dir: Path, manifest: dict[str, Any]) -> None:
    packets = []
    for record in manifest.get("files", []):
        artifact = record.get("enrichment_artifact")
        if not artifact:
            continue
        path = out_dir / artifact
        if path.exists():
            packets.append(load_json(path))
    correction_lines = []
    for packet in packets:
        for correction in packet.get("corrections", []):
            correction_lines.append(
                f"- `{correction['from']}` -> `{correction['to']}` "
                f"({correction['reason']}, count {correction['count']})"
            )
    if not correction_lines:
        correction_lines.append("- No corrections were needed in the synthetic sample.")
    brief = (
        "# Transcript Enrichment Brief\n\n"
        "This public-safe artifact simulates the OpenAI cleanup pass used after "
        "raw machine transcription. It records the prompt contract, domain "
        "context, allowed edits, disallowed edits, and correction notes without "
        "calling an external API or exposing private transcripts.\n\n"
        "## Simulated Correction Notes\n\n"
        + "\n".join(correction_lines)
        + "\n\n## Public Boundary\n\n"
        "- Synthetic transcript text only\n"
        "- No credentials or network calls\n"
        "- No private course identifiers or private source paths\n"
        "- Raw transcript excerpts are short public-safe samples\n"
    )
    (out_dir / "transcript_enrichment_brief.md").write_text(brief, encoding="utf-8")


def segment_text(text: str, max_chars: int) -> list[str]:
    paragraphs = [para.strip() for para in re.split(r"\n\s*\n", text) if para.strip()]
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


def action_prepare_corpus(args: argparse.Namespace) -> int:
    manifest = load_manifest(args.out)
    all_segments = []
    for record in manifest.get("files", []):
        clean_path = args.out / record["clean_transcript_artifact"]
        text = clean_path.read_text(encoding="utf-8")
        segments = []
        source_id = safe_artifact_stem({"name": record["source_name"]})
        for idx, segment in enumerate(segment_text(text, args.max_chars), start=1):
            segments.append(
                {
                    "segment_id": f"{source_id}#{idx:02d}",
                    "source_id": source_id,
                    "title": str(record["source_name"]).replace("_", " "),
                    "source_type": "synthetic media transcript",
                    "text": segment,
                    "citation": f"{record['source_name']}, segment {idx}",
                }
            )
        corpus_path = args.out / record["corpus_artifact"]
        write_json(corpus_path, {"schema_version": 1, "segments": segments})
        record["corpus_status"] = "ready_for_segmentation"
        all_segments.extend(segments)
    write_json(args.out / "corpus.json", {"schema_version": 1, "segment_count": len(all_segments), "segments": all_segments})
    write_summary(args.out, manifest)
    write_json(manifest_path(args.out), manifest)
    print(f"wrote {args.out / 'corpus.json'} ({len(all_segments)} segments)")
    return 0


def write_summary(out_dir: Path, manifest: dict[str, Any]) -> None:
    summary = (
        "# Workflow Summary\n\n"
        f"- Synthetic media files selected: {manifest.get('media_file_count', 0)}\n"
        f"- Simulated total media size: {int(manifest.get('total_media_size_bytes') or 0):,} bytes\n"
        "- Stages shown: inventory, media selection, private download, audio chunking, "
        "transcription, simulated LLM transcript enrichment, manifesting, corpus preparation\n"
        "- Reuse pattern: staged CLI, idempotent skips, manifest status fields, "
        "source-preserving corpus records\n"
        "- Enrichment pattern: raw machine transcript, domain context packet, guarded "
        "cleanup prompt, correction notes, reviewed clean transcript\n"
        "- Public safety: no credentials, real media, real transcripts, or private paths\n"
    )
    (out_dir / "workflow_summary.md").write_text(summary, encoding="utf-8")


def action_run(args: argparse.Namespace) -> int:
    action_download(args)
    action_transcribe(args)
    action_clean(args)
    action_prepare_corpus(args)
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the synthetic video transcription demo.")
    parser.add_argument(
        "action",
        nargs="?",
        default="run",
        choices=["list", "download", "transcribe", "clean", "prepare-corpus", "run"],
        help="Workflow stage to run.",
    )
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--raw-transcript", type=Path, default=DEFAULT_RAW_TRANSCRIPT)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--match", help="Case-insensitive filter applied to synthetic path/name.")
    parser.add_argument("--min-size-mb", type=float, default=0)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--max-chars", type=int, default=650)
    parser.add_argument("--force-download", action="store_true")
    parser.add_argument("--force-transcribe", action="store_true")
    parser.add_argument("--force-clean", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    actions = {
        "list": action_list,
        "download": action_download,
        "transcribe": action_transcribe,
        "clean": action_clean,
        "prepare-corpus": action_prepare_corpus,
        "run": action_run,
    }
    return actions[args.action](args)


if __name__ == "__main__":
    raise SystemExit(main())
