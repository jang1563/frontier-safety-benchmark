#!/usr/bin/env python3
"""Validate and summarize coverage for v0.2 public item files."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from validate_scaffold import PUBLIC_ITEM_SCHEMA_PATH, read_json, read_jsonl, validate_against_schema


def load_items(paths: list[Path]) -> list[dict]:
    schema = read_json(PUBLIC_ITEM_SCHEMA_PATH)
    records = []
    seen_ids: set[str] = set()
    for path in paths:
        for record in read_jsonl(path):
            validate_against_schema(record, schema, f"{path.name}:{record.get('item_id', '<unknown>')}")
            item_id = record["item_id"]
            if item_id in seen_ids:
                raise ValueError(f"Duplicate item_id across input files: {item_id}")
            seen_ids.add(item_id)
            records.append(record)
    return records


def summarize(items: list[dict]) -> dict:
    by_split = Counter(item["evaluation_split"] for item in items)
    by_release_status = Counter(item["public_release_status"] for item in items)
    by_domain = Counter(item["domain_family"] for item in items)
    by_reasoning = Counter(item["reasoning_type"] for item in items)
    by_mitigation = Counter(item["mitigation_relevance"] for item in items)
    by_ambiguity = Counter(item["ambiguity_level"] for item in items)

    warnings = []
    if len(by_domain) < 4:
        warnings.append("Fewer than 4 domain families represented.")
    if len(by_reasoning) < 5:
        warnings.append("Fewer than 5 reasoning types represented.")
    if by_split.get("public_dev", 0) < 8:
        warnings.append("Fewer than 8 public_dev items.")
    if by_split.get("public_eval", 0) < 12:
        warnings.append("Fewer than 12 public_eval items.")

    return {
        "total_items": len(items),
        "by_split": dict(sorted(by_split.items())),
        "by_release_status": dict(sorted(by_release_status.items())),
        "by_domain_family": dict(sorted(by_domain.items())),
        "by_reasoning_type": dict(sorted(by_reasoning.items())),
        "by_mitigation_relevance": dict(sorted(by_mitigation.items())),
        "by_ambiguity_level": dict(sorted(by_ambiguity.items())),
        "warnings": warnings,
    }


def to_markdown(summary: dict) -> str:
    lines = [
        "# v0.2 Coverage Report",
        "",
        f"- Total items: {summary['total_items']}",
        "",
        "## By Split",
        "",
    ]
    for key, value in summary["by_split"].items():
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## By Release Status", ""])
    for key, value in summary["by_release_status"].items():
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## By Domain Family", ""])
    for key, value in summary["by_domain_family"].items():
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## By Reasoning Type", ""])
    for key, value in summary["by_reasoning_type"].items():
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## By Mitigation Relevance", ""])
    for key, value in summary["by_mitigation_relevance"].items():
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## By Ambiguity Level", ""])
    for key, value in summary["by_ambiguity_level"].items():
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## Warnings", ""])
    if summary["warnings"]:
        for warning in summary["warnings"]:
            lines.append(f"- {warning}")
    else:
        lines.append("- None")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--inputs",
        type=Path,
        nargs="+",
        required=True,
        help="One or more JSONL item files to validate and summarize.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        required=True,
        help="Directory where coverage_summary.json and coverage_report.md will be written.",
    )
    args = parser.parse_args()

    items = load_items(args.inputs)
    summary = summarize(items)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    json_path = args.output_dir / "coverage_summary.json"
    markdown_path = args.output_dir / "coverage_report.md"

    with json_path.open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2)
        handle.write("\n")

    with markdown_path.open("w", encoding="utf-8") as handle:
        handle.write(to_markdown(summary))

    print(f"Wrote {json_path}")
    print(f"Wrote {markdown_path}")


if __name__ == "__main__":
    main()
