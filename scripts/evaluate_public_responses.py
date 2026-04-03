#!/usr/bin/env python3
"""Aggregate reviewed public benchmark responses into simple audit reports."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean


METRIC_FIELDS = [
    "calibration_score",
    "safe_boundary_score",
    "refusal_consistency_score",
    "mitigation_robustness_score",
    "evidence_grounding_score",
]
CONDITION_ORDER = {
    "pre_mitigation": 0,
    "post_mitigation": 1,
}


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


def summarize(items: list[dict], responses: list[dict]) -> dict:
    item_index = {item["item_id"]: item for item in items}
    by_model: dict[str, list[dict]] = defaultdict(list)
    for row in responses:
        item_id = row["item_id"]
        if item_id not in item_index:
            raise ValueError(f"Response references unknown item_id: {item_id}")
        by_model[row["model_name"]].append(row)

    model_summaries: dict[str, dict] = {}
    for model_name, model_rows in sorted(by_model.items()):
        summaries: dict[str, dict] = {}
        item_deltas = []
        seen_keys: set[tuple[str, str]] = set()
        by_condition: dict[str, list[dict]] = defaultdict(list)
        for row in model_rows:
            key = (row["item_id"], row["condition"])
            if key in seen_keys:
                raise ValueError(
                    f"Duplicate response row found for model_name={model_name}, "
                    f"item_id={row['item_id']}, condition={row['condition']}"
                )
            seen_keys.add(key)
            by_condition[row["condition"]].append(row)

        for condition, rows in sorted(by_condition.items(), key=lambda item: CONDITION_ORDER.get(item[0], 999)):
            metric_summary = {}
            error_counter: Counter[str] = Counter()
            for metric in METRIC_FIELDS:
                metric_summary[metric] = round(mean(row["review"][metric] for row in rows), 3)
            for row in rows:
                error_counter.update(row["review"].get("error_tags", []))
            summaries[condition] = {
                "count": len(rows),
                "metrics": metric_summary,
                "error_tags": dict(error_counter.most_common()),
            }

        grouped_by_item: dict[str, dict[str, dict]] = defaultdict(dict)
        for row in model_rows:
            grouped_by_item[row["item_id"]][row["condition"]] = row

        for item_id, condition_map in grouped_by_item.items():
            if "pre_mitigation" not in condition_map or "post_mitigation" not in condition_map:
                raise ValueError(
                    f"Model {model_name} is missing one or more conditions for item {item_id}"
                )
            delta_record = {"item_id": item_id, "title": item_index[item_id]["title"], "deltas": {}}
            for metric in METRIC_FIELDS:
                pre_value = condition_map["pre_mitigation"]["review"][metric]
                post_value = condition_map["post_mitigation"]["review"][metric]
                delta_record["deltas"][metric] = round(post_value - pre_value, 3)
            item_deltas.append(delta_record)

        overall_delta = {}
        if "pre_mitigation" in summaries and "post_mitigation" in summaries:
            for metric in METRIC_FIELDS:
                overall_delta[metric] = round(
                    summaries["post_mitigation"]["metrics"][metric]
                    - summaries["pre_mitigation"]["metrics"][metric],
                    3,
                )

        model_summaries[model_name] = {
            "conditions": summaries,
            "overall_delta": overall_delta,
            "item_deltas": sorted(item_deltas, key=lambda row: row["item_id"]),
        }

    return {"models": model_summaries}


def to_markdown(summary: dict) -> str:
    lines = [
        "# Public Response Audit",
        "",
    ]
    for model_name, model_summary in summary["models"].items():
        lines.extend([f"## Model: {model_name}", ""])
        for condition, payload in sorted(
            model_summary["conditions"].items(),
            key=lambda item: CONDITION_ORDER.get(item[0], 999),
        ):
            lines.extend(
                [
                    f"### {condition.replace('_', ' ').title()}",
                    "",
                    f"- Reviewed responses: {payload['count']}",
                ]
            )
            for metric, value in payload["metrics"].items():
                lines.append(f"- {metric}: {value}")
            if payload["error_tags"]:
                lines.append(
                    "- Error tags: " + ", ".join(f"{k}={v}" for k, v in payload["error_tags"].items())
                )
            lines.append("")

        if model_summary["overall_delta"]:
            lines.extend(["### Overall Delta (Post - Pre)", ""])
            for metric, value in model_summary["overall_delta"].items():
                lines.append(f"- {metric}: {value}")
            lines.append("")

        if model_summary["item_deltas"]:
            lines.extend(["### Per-Item Delta", ""])
            for record in model_summary["item_deltas"]:
                deltas = ", ".join(f"{metric}={value}" for metric, value in record["deltas"].items())
                lines.append(f"- {record['item_id']} ({record['title']}): {deltas}")
            lines.append("")

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--items", type=Path, required=True, help="Path to sample item JSONL file.")
    parser.add_argument(
        "--responses",
        type=Path,
        required=True,
        help="Path to reviewed response JSONL file.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        required=True,
        help="Directory where summary.json and summary.md will be written.",
    )
    args = parser.parse_args()

    items = read_jsonl(args.items)
    responses = read_jsonl(args.responses)
    summary = summarize(items, responses)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    json_path = args.output_dir / "summary.json"
    markdown_path = args.output_dir / "summary.md"

    with json_path.open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2)
        handle.write("\n")

    with markdown_path.open("w", encoding="utf-8") as handle:
        handle.write(to_markdown(summary))

    print(f"Wrote {json_path}")
    print(f"Wrote {markdown_path}")


if __name__ == "__main__":
    main()
