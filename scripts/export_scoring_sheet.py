#!/usr/bin/env python3
"""Export raw model responses to a CSV scoring sheet, or import scored CSV back to JSONL.

This tool bridges the gap between raw model inference output and reviewed
response JSONL files. It supports two modes:

  export: Raw response JSONL + item metadata → CSV scoring sheet
  import: Scored CSV → reviewed response JSONL (schema-validated)

Usage:
    # Export raw responses to a scoring CSV
    python3 export_scoring_sheet.py \
      --mode export \
      --responses data_public/raw_responses_gpt4o_pre.jsonl \
                  data_public/raw_responses_gpt4o_post.jsonl \
      --items data_public/all_public_items.jsonl \
      --output scoring_sheets/gpt4o_scoring.csv

    # Import scored CSV back to reviewed JSONL
    python3 export_scoring_sheet.py \
      --mode import \
      --input scoring_sheets/gpt4o_scoring.csv \
      --output data_public/reviewed_responses_gpt4o_v0.3.jsonl
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path


METRICS = [
    "calibration_score",
    "safe_boundary_score",
    "refusal_consistency_score",
    "mitigation_robustness_score",
    "evidence_grounding_score",
]

VALID_ERROR_TAGS = {
    "overconfidence",
    "false_reassurance",
    "inconsistent_refusal",
    "unsupported_certainty",
    "policy_inconsistency",
    "incomplete_safe_alternative",
}

EXPORT_COLUMNS = [
    "item_id",
    "condition",
    "model_name",
    "title",
    "domain_family",
    "expected_behavior_tags",
    "reference_guidance_summary",
    "prompt",
    "response_text",
    "calibration_score",
    "safe_boundary_score",
    "refusal_consistency_score",
    "mitigation_robustness_score",
    "evidence_grounding_score",
    "error_tags",
    "notes",
]


def read_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSON on line {line_number} of {path}") from exc
    return rows


def export_scoring_sheet(
    response_paths: list[Path],
    items_path: Path,
    output_path: Path,
) -> None:
    """Export raw responses + item metadata to a CSV scoring sheet."""
    items = read_jsonl(items_path)
    item_index = {item["item_id"]: item for item in items}

    all_responses = []
    for path in response_paths:
        all_responses.extend(read_jsonl(path))

    # Sort by model_name, then condition (pre before post), then item_id
    condition_order = {"pre_mitigation": 0, "post_mitigation": 1}
    all_responses.sort(key=lambda r: (
        r["model_name"],
        condition_order.get(r["condition"], 99),
        r["item_id"],
    ))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=EXPORT_COLUMNS, extrasaction="ignore")
        writer.writeheader()

        for resp in all_responses:
            item = item_index.get(resp["item_id"], {})
            existing_review = resp.get("review", {})

            row = {
                "item_id": resp["item_id"],
                "condition": resp["condition"],
                "model_name": resp["model_name"],
                "title": item.get("title", ""),
                "domain_family": item.get("domain_family", ""),
                "expected_behavior_tags": "; ".join(item.get("expected_behavior_tags", [])),
                "reference_guidance_summary": item.get("reference_guidance_summary", ""),
                "prompt": item.get("prompt", ""),
                "response_text": resp.get("response_text", ""),
            }

            # Pre-fill scores if they exist (for re-export of partially scored data)
            for metric in METRICS:
                val = existing_review.get(metric)
                row[metric] = val if val is not None else ""
            row["error_tags"] = "; ".join(existing_review.get("error_tags", []))
            row["notes"] = existing_review.get("notes", "")

            writer.writerow(row)

    print(f"Exported {len(all_responses)} responses to {output_path}")
    print(f"Score each row using the annotation handbook (docs/annotation_handbook.md).")
    print(f"When done, import back with: python3 {sys.argv[0]} --mode import --input {output_path} --output <output.jsonl>")


def import_scoring_sheet(input_path: Path, output_path: Path) -> None:
    """Import a scored CSV back into reviewed response JSONL."""
    rows = []
    errors = []

    with input_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for line_num, row in enumerate(reader, start=2):  # header is line 1
            record_errors = []

            # Validate required fields
            item_id = row.get("item_id", "").strip()
            condition = row.get("condition", "").strip()
            model_name = row.get("model_name", "").strip()
            response_text = row.get("response_text", "").strip()
            notes = row.get("notes", "").strip()

            if not item_id:
                record_errors.append("missing item_id")
            if condition not in ("pre_mitigation", "post_mitigation"):
                record_errors.append(f"invalid condition: '{condition}'")
            if not model_name:
                record_errors.append("missing model_name")
            if not response_text:
                record_errors.append("missing response_text")
            if not notes:
                record_errors.append("missing notes (required)")

            # Validate scores
            scores = {}
            for metric in METRICS:
                val = row.get(metric, "").strip()
                if not val:
                    record_errors.append(f"missing {metric}")
                    scores[metric] = None
                else:
                    try:
                        score = int(val)
                        if score < 1 or score > 5:
                            record_errors.append(f"{metric}={score} out of range (1-5)")
                        scores[metric] = score
                    except ValueError:
                        record_errors.append(f"{metric}='{val}' is not an integer")
                        scores[metric] = None

            # Validate error tags
            error_tags_raw = row.get("error_tags", "").strip()
            if error_tags_raw:
                error_tags = [t.strip() for t in error_tags_raw.replace(",", ";").split(";") if t.strip()]
                for tag in error_tags:
                    if tag not in VALID_ERROR_TAGS:
                        record_errors.append(f"invalid error tag: '{tag}'")
            else:
                error_tags = []

            if record_errors:
                errors.append(f"  Line {line_num} ({item_id} / {condition}): {'; '.join(record_errors)}")
                continue

            record = {
                "item_id": item_id,
                "condition": condition,
                "model_name": model_name,
                "response_text": response_text,
                "review": {
                    "calibration_score": scores["calibration_score"],
                    "safe_boundary_score": scores["safe_boundary_score"],
                    "refusal_consistency_score": scores["refusal_consistency_score"],
                    "mitigation_robustness_score": scores["mitigation_robustness_score"],
                    "evidence_grounding_score": scores["evidence_grounding_score"],
                    "error_tags": error_tags,
                    "notes": notes,
                },
            }
            rows.append(record)

    if errors:
        print(f"Validation errors ({len(errors)} rows):", file=sys.stderr)
        for err in errors:
            print(err, file=sys.stderr)
        print(f"\nFix the errors above and re-run. No output file was written.", file=sys.stderr)
        sys.exit(1)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as handle:
        for record in rows:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")

    print(f"Imported {len(rows)} reviewed responses to {output_path}")
    print(f"Next: validate with python3 scripts/validate_scaffold.py")


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--mode",
        choices=["export", "import"],
        required=True,
        help="Operation mode: 'export' creates CSV from JSONL, 'import' creates JSONL from scored CSV.",
    )
    parser.add_argument(
        "--responses",
        type=Path,
        nargs="+",
        help="(export mode) Raw response JSONL file(s) to export.",
    )
    parser.add_argument(
        "--items",
        type=Path,
        help="(export mode) Benchmark items JSONL file for metadata enrichment.",
    )
    parser.add_argument(
        "--input",
        type=Path,
        help="(import mode) Scored CSV file to import.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="Output file path (CSV for export, JSONL for import).",
    )
    args = parser.parse_args()

    if args.mode == "export":
        if not args.responses:
            parser.error("--responses is required for export mode")
        if not args.items:
            parser.error("--items is required for export mode")
        export_scoring_sheet(args.responses, args.items, args.output)
    elif args.mode == "import":
        if not args.input:
            parser.error("--input is required for import mode")
        import_scoring_sheet(args.input, args.output)


if __name__ == "__main__":
    main()
