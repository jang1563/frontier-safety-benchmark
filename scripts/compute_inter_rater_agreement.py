#!/usr/bin/env python3
"""Compute inter-rater agreement metrics from dual-reviewer benchmark data.

Reads two reviewed-response JSONL files (from two independent reviewers
for the same items, model, and conditions) and reports:

- Per-metric mean absolute divergence
- Per-metric Cohen's kappa (binarized at threshold 4)
- Error-tag exact-match agreement rate
- Adjudication trigger list

Usage:
    python3 compute_inter_rater_agreement.py \
        --reviewer-a data_public/reviewed_responses_reviewer_a.jsonl \
        --reviewer-b data_public/reviewed_responses_reviewer_b.jsonl \
        --output-dir results/v0_2_demo/inter_rater
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from datetime import date
from pathlib import Path


METRICS = [
    "calibration_score",
    "safe_boundary_score",
    "refusal_consistency_score",
    "mitigation_robustness_score",
    "evidence_grounding_score",
]

SCORE_DIVERGENCE_THRESHOLD = 2
ERROR_TAG_CONFLICT_THRESHOLD = 2
RANDOM_SAMPLE_FRACTION = 0.10
KAPPA_BINARIZE_THRESHOLD = 4


def read_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def review_key(row: dict) -> tuple[str, str, str]:
    return (row["item_id"], row["model_name"], row["condition"])


def index_reviews(rows: list[dict]) -> dict[tuple[str, str, str], dict]:
    indexed = {}
    for row in rows:
        indexed[review_key(row)] = row
    return indexed


def cohens_kappa(a_labels: list[int], b_labels: list[int]) -> float:
    """Cohen's kappa for binary labels (0/1)."""
    n = len(a_labels)
    if n == 0:
        return 0.0
    agree = sum(1 for a, b in zip(a_labels, b_labels) if a == b)
    p_o = agree / n
    a1 = sum(a_labels) / n
    b1 = sum(b_labels) / n
    p_e = a1 * b1 + (1 - a1) * (1 - b1)
    if p_e == 1.0:
        return 1.0
    return (p_o - p_e) / (1 - p_e)


def compute_agreement(
    reviews_a: dict[tuple[str, str, str], dict],
    reviews_b: dict[tuple[str, str, str], dict],
) -> dict:
    common_keys = sorted(set(reviews_a.keys()) & set(reviews_b.keys()))
    n = len(common_keys)

    if n == 0:
        return {"error": "No overlapping (item_id, model_name, condition) pairs found."}

    # Per-metric divergence and kappa
    metric_divergences: dict[str, list[float]] = defaultdict(list)
    metric_binary_a: dict[str, list[int]] = defaultdict(list)
    metric_binary_b: dict[str, list[int]] = defaultdict(list)

    error_tag_matches = 0
    adjudication_triggers: list[dict] = []

    for key in common_keys:
        ra = reviews_a[key]
        rb = reviews_b[key]
        scores_a = ra.get("review", {})
        scores_b = rb.get("review", {})
        tags_a = sorted(ra.get("review", {}).get("error_tags", []))
        tags_b = sorted(rb.get("review", {}).get("error_tags", []))

        triggered = False
        trigger_reasons = []
        disputed_metrics = []

        for metric in METRICS:
            sa = scores_a.get(metric)
            sb = scores_b.get(metric)
            if sa is not None and sb is not None:
                div = abs(sa - sb)
                metric_divergences[metric].append(div)
                metric_binary_a[metric].append(1 if sa >= KAPPA_BINARIZE_THRESHOLD else 0)
                metric_binary_b[metric].append(1 if sb >= KAPPA_BINARIZE_THRESHOLD else 0)
                if div >= SCORE_DIVERGENCE_THRESHOLD:
                    triggered = True
                    trigger_reasons.append("score_divergence")
                    disputed_metrics.append({
                        "metric_name": metric,
                        "reviewer_a_score": sa,
                        "reviewer_b_score": sb,
                        "divergence": div,
                    })

        if tags_a == tags_b:
            error_tag_matches += 1
        elif (len(tags_a) == 0 and len(tags_b) >= ERROR_TAG_CONFLICT_THRESHOLD) or \
             (len(tags_b) == 0 and len(tags_a) >= ERROR_TAG_CONFLICT_THRESHOLD):
            triggered = True
            trigger_reasons.append("error_tag_conflict")

        if triggered:
            adjudication_triggers.append({
                "item_id": key[0],
                "model_name": key[1],
                "condition": key[2],
                "trigger_reasons": list(set(trigger_reasons)),
                "disputed_metrics": disputed_metrics,
            })

    # Compute summaries
    metric_mad = {}
    metric_kappa = {}
    for metric in METRICS:
        divs = metric_divergences.get(metric, [])
        metric_mad[metric] = round(sum(divs) / len(divs), 3) if divs else None
        a_bin = metric_binary_a.get(metric, [])
        b_bin = metric_binary_b.get(metric, [])
        metric_kappa[metric] = round(cohens_kappa(a_bin, b_bin), 3) if a_bin else None

    return {
        "generated_on": date.today().isoformat(),
        "total_paired_reviews": n,
        "metric_mean_absolute_divergence": metric_mad,
        "metric_cohens_kappa_binarized": metric_kappa,
        "error_tag_exact_match_rate": round(error_tag_matches / n, 3) if n else 0,
        "adjudication_trigger_count": len(adjudication_triggers),
        "adjudication_trigger_rate": round(len(adjudication_triggers) / n, 3) if n else 0,
        "adjudication_triggers": adjudication_triggers,
    }


def write_summary_markdown(result: dict, output_path: Path) -> None:
    lines = [
        "# Inter-Rater Agreement Summary",
        "",
        f"- Generated on: {result['generated_on']}",
        f"- Total paired reviews: {result['total_paired_reviews']}",
        f"- Error-tag exact-match rate: {result['error_tag_exact_match_rate']}",
        f"- Adjudication trigger count: {result['adjudication_trigger_count']}",
        f"- Adjudication trigger rate: {result['adjudication_trigger_rate']}",
        "",
        "## Per-Metric Mean Absolute Divergence",
        "",
    ]

    for metric, val in result["metric_mean_absolute_divergence"].items():
        lines.append(f"- {metric}: {val}")
    lines.append("")

    lines.append("## Per-Metric Cohen's Kappa (binarized at 4)")
    lines.append("")
    for metric, val in result["metric_cohens_kappa_binarized"].items():
        interpretation = ""
        if val is not None:
            if val > 0.80:
                interpretation = " (strong)"
            elif val > 0.60:
                interpretation = " (moderate)"
            elif val > 0.40:
                interpretation = " (fair)"
            else:
                interpretation = " (poor)"
        lines.append(f"- {metric}: {val}{interpretation}")
    lines.append("")

    if result["adjudication_triggers"]:
        lines.append("## Adjudication Triggers")
        lines.append("")
        for trigger in result["adjudication_triggers"]:
            lines.append(
                f"- {trigger['item_id']} / {trigger['model_name']} / {trigger['condition']}: "
                f"{', '.join(trigger['trigger_reasons'])}"
            )
            for dm in trigger.get("disputed_metrics", []):
                lines.append(
                    f"  - {dm['metric_name']}: A={dm['reviewer_a_score']}, B={dm['reviewer_b_score']}, divergence={dm['divergence']}"
                )
        lines.append("")
    else:
        lines.append("## Adjudication Triggers")
        lines.append("")
        lines.append("- None")
        lines.append("")

    with output_path.open("w", encoding="utf-8") as handle:
        handle.write("\n".join(lines))


def write_summary_csv(result: dict, output_path: Path) -> None:
    rows = []
    for metric in METRICS:
        rows.append({
            "metric_name": metric,
            "mean_absolute_divergence": result["metric_mean_absolute_divergence"].get(metric),
            "cohens_kappa_binarized": result["metric_cohens_kappa_binarized"].get(metric),
        })
    fieldnames = ["metric_name", "mean_absolute_divergence", "cohens_kappa_binarized"]
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--reviewer-a",
        type=Path,
        required=True,
        help="Reviewed-response JSONL from reviewer A.",
    )
    parser.add_argument(
        "--reviewer-b",
        type=Path,
        required=True,
        help="Reviewed-response JSONL from reviewer B.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        required=True,
        help="Directory for agreement report outputs.",
    )
    args = parser.parse_args()

    rows_a = read_jsonl(args.reviewer_a)
    rows_b = read_jsonl(args.reviewer_b)

    reviews_a = index_reviews(rows_a)
    reviews_b = index_reviews(rows_b)

    result = compute_agreement(reviews_a, reviews_b)

    args.output_dir.mkdir(parents=True, exist_ok=True)

    json_path = args.output_dir / "inter_rater_agreement.json"
    md_path = args.output_dir / "inter_rater_agreement.md"
    csv_path = args.output_dir / "inter_rater_agreement.csv"

    with json_path.open("w", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2)

    write_summary_markdown(result, md_path)
    write_summary_csv(result, csv_path)

    print(f"Wrote {json_path}")
    print(f"Wrote {md_path}")
    print(f"Wrote {csv_path}")

    if "error" in result:
        print(f"Warning: {result['error']}")


if __name__ == "__main__":
    main()
