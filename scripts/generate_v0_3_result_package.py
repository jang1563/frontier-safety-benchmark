#!/usr/bin/env python3
"""Generate the v0.3 result package from real model evaluation artifacts."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from datetime import date
from pathlib import Path


def read_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def read_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def write_inventory_csv(items: list[dict], output_path: Path) -> None:
    fieldnames = [
        "item_id",
        "title",
        "evaluation_split",
        "public_release_status",
        "domain_family",
        "reasoning_type",
        "risk_sensitivity_tier",
        "ambiguity_level",
        "mitigation_relevance",
        "contamination_risk_level",
    ]
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for item in sorted(items, key=lambda row: row["item_id"]):
            writer.writerow({name: item[name] for name in fieldnames})


def average_metric(mapping: dict[str, float | int]) -> float:
    if not mapping:
        return 0.0
    return round(sum(float(value) for value in mapping.values()) / len(mapping), 3)


def audit_slice_label(path: Path) -> str:
    return path.parent.name or path.stem


def audit_scope_for_label(slice_label: str) -> str:
    if "_audit" in slice_label:
        return slice_label.split("_audit", 1)[0]
    return slice_label


def audit_scopes(audit_summaries: dict[str, dict] | None) -> list[str]:
    if audit_summaries is None:
        return []
    return sorted({audit_scope_for_label(slice_label) for slice_label in audit_summaries})


def format_scope_list(scopes: list[str]) -> str:
    rendered = [f"`{scope}`" for scope in scopes]
    if not rendered:
        return "the public benchmark"
    if len(rendered) == 1:
        return rendered[0]
    if len(rendered) == 2:
        return f"{rendered[0]} and {rendered[1]}"
    return ", ".join(rendered[:-1]) + f", and {rendered[-1]}"


def model_overview_record(scope: str, slice_label: str, model_name: str, model_summary: dict) -> dict[str, str | int | float]:
    pre_payload = model_summary.get("conditions", {}).get("pre_mitigation", {})
    post_payload = model_summary.get("conditions", {}).get("post_mitigation", {})
    pre_metrics = pre_payload.get("metrics", {})
    post_metrics = post_payload.get("metrics", {})
    return {
        "scope": scope,
        "slice_label": slice_label,
        "model_name": model_name,
        "pre_review_count": pre_payload.get("count", 0),
        "post_review_count": post_payload.get("count", 0),
        "pre_metric_average": average_metric(pre_metrics),
        "post_metric_average": average_metric(post_metrics),
        "overall_delta_average": average_metric(model_summary.get("overall_delta", {})),
        "pre_error_tag_total": sum(pre_payload.get("error_tags", {}).values()),
        "post_error_tag_total": sum(post_payload.get("error_tags", {}).values()),
    }


def build_audit_slice_overview_rows(audit_summaries: dict[str, dict] | None) -> list[dict[str, str | int | float]]:
    rows: list[dict[str, str | int | float]] = []
    if audit_summaries is None:
        return rows
    for slice_label, audit_summary in sorted(audit_summaries.items()):
        scope = audit_scope_for_label(slice_label)
        for model_name, model_summary in sorted(audit_summary.get("models", {}).items()):
            rows.append(model_overview_record(scope, slice_label, model_name, model_summary))
    return rows


def write_audit_slice_overview_csv(rows: list[dict[str, str | int | float]], output_path: Path) -> None:
    fieldnames = [
        "scope",
        "slice_label",
        "model_name",
        "pre_review_count",
        "post_review_count",
        "pre_metric_average",
        "post_metric_average",
        "overall_delta_average",
        "pre_error_tag_total",
        "post_error_tag_total",
    ]
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def build_audit_longitudinal_rows(
    slice_overview_rows: list[dict[str, str | int | float]]
) -> list[dict[str, str | int | float]]:
    grouped_rows: dict[tuple[str, str], list[dict[str, str | int | float]]] = {}
    for row in slice_overview_rows:
        grouped_rows.setdefault((str(row["scope"]), str(row["model_name"])), []).append(row)

    longitudinal_rows: list[dict[str, str | int | float]] = []
    for (scope, model_name), rows in sorted(grouped_rows.items()):
        ordered_rows = sorted(rows, key=lambda row: str(row["slice_label"]))
        if len(ordered_rows) < 2:
            continue
        for previous, current in zip(ordered_rows, ordered_rows[1:]):
            longitudinal_rows.append(
                {
                    "scope": scope,
                    "model_name": model_name,
                    "from_slice": str(previous["slice_label"]),
                    "to_slice": str(current["slice_label"]),
                    "from_post_metric_average": previous["post_metric_average"],
                    "to_post_metric_average": current["post_metric_average"],
                    "post_metric_average_change": round(
                        float(current["post_metric_average"]) - float(previous["post_metric_average"]),
                        3,
                    ),
                    "from_overall_delta_average": previous["overall_delta_average"],
                    "to_overall_delta_average": current["overall_delta_average"],
                    "overall_delta_average_change": round(
                        float(current["overall_delta_average"]) - float(previous["overall_delta_average"]),
                        3,
                    ),
                    "from_post_error_tag_total": previous["post_error_tag_total"],
                    "to_post_error_tag_total": current["post_error_tag_total"],
                    "post_error_tag_total_change": int(current["post_error_tag_total"]) - int(previous["post_error_tag_total"]),
                }
            )
    return longitudinal_rows


def write_audit_longitudinal_csv(
    rows: list[dict[str, str | int | float]], output_path: Path
) -> None:
    fieldnames = [
        "scope",
        "model_name",
        "from_slice",
        "to_slice",
        "from_post_metric_average",
        "to_post_metric_average",
        "post_metric_average_change",
        "from_overall_delta_average",
        "to_overall_delta_average",
        "overall_delta_average_change",
        "from_post_error_tag_total",
        "to_post_error_tag_total",
        "post_error_tag_total_change",
    ]
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_audit_longitudinal_markdown(
    rows: list[dict[str, str | int | float]], output_path: Path
) -> None:
    lines = [
        "# Audit Longitudinal Summary",
        "",
        f"- Generated on: {date.today().isoformat()}",
        "- Positive `post_metric_average_change` means the later slice ended stronger on average.",
        "- Negative `overall_delta_average_change` can reflect a stronger pre-mitigation baseline rather than weaker final behavior.",
        "",
    ]

    if not rows:
        lines.extend(["## Comparisons", "", "- None available.", ""])
    else:
        by_scope: dict[str, list[dict[str, str | int | float]]] = {}
        for row in rows:
            by_scope.setdefault(str(row["scope"]), []).append(row)
        for scope, scope_rows in sorted(by_scope.items()):
            lines.extend([f"## Scope: {scope}", ""])
            for row in scope_rows:
                lines.append(
                    "- "
                    + str(row["model_name"])
                    + f": `{row['from_slice']} -> {row['to_slice']}` changed "
                    + f"post-mitigation average by {row['post_metric_average_change']:+.3f}, "
                    + f"overall delta average by {row['overall_delta_average_change']:+.3f}, "
                    + f"and residual post error tags {row['from_post_error_tag_total']} -> {row['to_post_error_tag_total']}."
                )
            lines.append("")

    with output_path.open("w", encoding="utf-8") as handle:
        handle.write("\n".join(lines))


def build_scorecard_rows(
    items: list[dict],
    coverage_summary: dict,
    release_manifest: dict | None,
    audit_summaries: dict[str, dict] | None,
) -> list[dict[str, str | int]]:
    rows: list[dict[str, str | int]] = []

    rows.append(
        {
            "metric_group": "overview",
            "metric_name": "total_items",
            "value": coverage_summary["total_items"],
            "notes": "Total public-safe benchmark items in the v0.3 package.",
        }
    )
    rows.append(
        {
            "metric_group": "overview",
            "metric_name": "warning_count",
            "value": len(coverage_summary.get("warnings", [])),
            "notes": "Coverage warnings reported by the taxonomy coverage checker.",
        }
    )

    for group_name, key in [
        ("split", "by_split"),
        ("release_status", "by_release_status"),
        ("domain_family", "by_domain_family"),
        ("reasoning_type", "by_reasoning_type"),
        ("mitigation_relevance", "by_mitigation_relevance"),
        ("ambiguity_level", "by_ambiguity_level"),
    ]:
        for metric_name, value in sorted(coverage_summary.get(key, {}).items()):
            rows.append(
                {
                    "metric_group": group_name,
                    "metric_name": metric_name,
                    "value": value,
                    "notes": "",
                }
            )

    risk_tier_counts = Counter(item["risk_sensitivity_tier"] for item in items)
    for metric_name, value in sorted(risk_tier_counts.items()):
        rows.append(
            {
                "metric_group": "risk_sensitivity_tier",
                "metric_name": metric_name,
                "value": value,
                "notes": "",
            }
        )

    if release_manifest is not None:
        rows.append(
            {
                "metric_group": "release_manifest",
                "metric_name": "artifact_count",
                "value": len(release_manifest["artifacts"]),
                "notes": "Artifact count recorded in the release manifest.",
            }
        )
        artifact_type_counts = Counter(
            artifact["artifact_type"] for artifact in release_manifest["artifacts"]
        )
        for metric_name, value in sorted(artifact_type_counts.items()):
            rows.append(
                {
                    "metric_group": "release_manifest_artifact_type",
                    "metric_name": metric_name,
                    "value": value,
                    "notes": "",
                }
            )

    if audit_summaries is not None:
        for slice_label, audit_summary in sorted(audit_summaries.items()):
            for model_name, model_summary in sorted(audit_summary.get("models", {}).items()):
                for condition, payload in model_summary.get("conditions", {}).items():
                    rows.append(
                        {
                            "metric_group": "audit_review_count",
                            "metric_name": f"{slice_label}.{model_name}.{condition}.count",
                            "value": payload["count"],
                            "notes": "Reviewed response count for this model and condition.",
                        }
                    )
                    for metric_name, value in sorted(payload.get("metrics", {}).items()):
                        rows.append(
                            {
                                "metric_group": "audit_metric",
                                "metric_name": f"{slice_label}.{model_name}.{condition}.{metric_name}",
                                "value": value,
                                "notes": "",
                            }
                        )
                for metric_name, value in sorted(model_summary.get("overall_delta", {}).items()):
                    rows.append(
                        {
                            "metric_group": "audit_delta",
                            "metric_name": f"{slice_label}.{model_name}.overall_delta.{metric_name}",
                            "value": value,
                            "notes": "Post-mitigation minus pre-mitigation average.",
                        }
                    )
                post_metrics = model_summary.get("conditions", {}).get("post_mitigation", {}).get("metrics", {})
                post_error_tags = model_summary.get("conditions", {}).get("post_mitigation", {}).get("error_tags", {})
                rows.append(
                    {
                        "metric_group": "audit_model_overview",
                        "metric_name": f"{slice_label}.{model_name}.post_metric_average",
                        "value": average_metric(post_metrics),
                        "notes": "Average across post-mitigation audit metrics.",
                    }
                )
                rows.append(
                    {
                        "metric_group": "audit_model_overview",
                        "metric_name": f"{slice_label}.{model_name}.overall_delta_average",
                        "value": average_metric(model_summary.get("overall_delta", {})),
                        "notes": "Average improvement across audited metrics.",
                    }
                )
                rows.append(
                    {
                        "metric_group": "audit_model_overview",
                        "metric_name": f"{slice_label}.{model_name}.post_error_tag_total",
                        "value": sum(post_error_tags.values()),
                        "notes": "Residual post-mitigation tagged issues across audited items.",
                    }
                )

    return rows


def write_scorecard_csv(rows: list[dict[str, str | int]], output_path: Path) -> None:
    fieldnames = ["metric_group", "metric_name", "value", "notes"]
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def markdown_bullet_counts(title: str, mapping: dict[str, int]) -> list[str]:
    lines = [f"## {title}", ""]
    for key, value in sorted(mapping.items()):
        lines.append(f"- {key}: {value}")
    lines.append("")
    return lines


def write_scorecard_markdown(
    coverage_summary: dict,
    release_manifest: dict | None,
    audit_summaries: dict[str, dict] | None,
    output_path: Path,
) -> None:
    warnings = coverage_summary.get("warnings", [])
    artifact_type_counts = Counter()
    release_version = "not available"
    benchmark_version = "not available"
    if release_manifest is not None:
        artifact_type_counts.update(
            artifact["artifact_type"] for artifact in release_manifest["artifacts"]
        )
        release_version = release_manifest["release_version"]
        benchmark_version = release_manifest["benchmark_version"]

    audit_slice_count = len(audit_summaries) if audit_summaries is not None else 0
    audited_scopes = audit_scopes(audit_summaries)
    audited_scope_text = format_scope_list(audited_scopes)

    lines = [
        "# v0.3 Release Scorecard",
        "",
        f"- Generated on: {date.today().isoformat()}",
        f"- Release version: {release_version}",
        f"- Benchmark version: {benchmark_version}",
        f"- Total public items: {coverage_summary['total_items']}",
        f"- Coverage warnings: {len(warnings)}",
        "",
        "## Top-line interpretation",
        "",
        "- This release evaluates real frontier and open-source models against the full 24-item public benchmark with pre/post-mitigation comparison.",
        f"- It includes {audit_slice_count} audited evaluation slice{'s' if audit_slice_count != 1 else ''} spanning {audited_scope_text}.",
        "- Results provide empirical evidence on how safety system prompts affect model behavior across domains, with cross-model comparison of mitigation effectiveness.",
        "",
    ]

    lines.extend(markdown_bullet_counts("By Split", coverage_summary["by_split"]))
    lines.extend(
        markdown_bullet_counts("By Domain Family", coverage_summary["by_domain_family"])
    )
    lines.extend(
        markdown_bullet_counts("By Reasoning Type", coverage_summary["by_reasoning_type"])
    )
    lines.extend(
        markdown_bullet_counts(
            "By Mitigation Relevance", coverage_summary["by_mitigation_relevance"]
        )
    )
    lines.extend(
        markdown_bullet_counts("By Ambiguity Level", coverage_summary["by_ambiguity_level"])
    )

    if artifact_type_counts:
        lines.extend(
            markdown_bullet_counts(
                "Release Manifest Artifact Types", dict(sorted(artifact_type_counts.items()))
            )
        )

    if audit_summaries is not None:
        lines.extend(["## Audited Public Benchmark Metrics", ""])
        for slice_label, audit_summary in sorted(audit_summaries.items()):
            lines.append(f"### Slice: {slice_label}")
            lines.append("")
            for model_name, model_summary in sorted(audit_summary.get("models", {}).items()):
                lines.append(f"#### Model: {model_name}")
                lines.append("")
                for condition, payload in model_summary.get("conditions", {}).items():
                    lines.append(f"- {condition}: {payload['count']} reviewed responses")
                    for metric_name, value in sorted(payload.get("metrics", {}).items()):
                        lines.append(f"- {condition} {metric_name}: {value}")
                    if payload.get("error_tags"):
                        lines.append(
                            "- "
                            + condition
                            + " error tags: "
                            + ", ".join(
                                f"{tag}={count}" for tag, count in payload["error_tags"].items()
                            )
                        )
                for metric_name, value in sorted(model_summary.get("overall_delta", {}).items()):
                    lines.append(f"- overall delta {metric_name}: {value}")
                lines.append("")

        lines.extend(["## Cross-Model Snapshot", ""])
        for slice_label, audit_summary in sorted(audit_summaries.items()):
            lines.append(f"### Slice: {slice_label}")
            lines.append("")
            for model_name, model_summary in sorted(audit_summary.get("models", {}).items()):
                post_metrics = model_summary.get("conditions", {}).get("post_mitigation", {}).get("metrics", {})
                post_error_tags = model_summary.get("conditions", {}).get("post_mitigation", {}).get("error_tags", {})
                lines.append(
                    "- "
                    + model_name
                    + f": post-mitigation metric average={average_metric(post_metrics)}, "
                    + f"overall delta average={average_metric(model_summary.get('overall_delta', {}))}, "
                    + f"residual post error tags={sum(post_error_tags.values())}"
                )
            lines.append("")

        if audit_slice_count > 1:
            lines.extend(["## Cross-Slice Snapshot", ""])
            by_scope_and_model: dict[tuple[str, str], list[tuple[str, dict]]] = {}
            for slice_label, audit_summary in sorted(audit_summaries.items()):
                for model_name, model_summary in sorted(audit_summary.get("models", {}).items()):
                    scope = audit_scope_for_label(slice_label)
                    by_scope_and_model.setdefault((scope, model_name), []).append((slice_label, model_summary))
            grouped_scope_entries: dict[str, list[tuple[str, list[tuple[str, dict]]]]] = {}
            for (scope, model_name), slice_entries in sorted(by_scope_and_model.items()):
                if len(slice_entries) < 2:
                    continue
                grouped_scope_entries.setdefault(scope, []).append((model_name, slice_entries))
            for scope, model_entries in sorted(grouped_scope_entries.items()):
                lines.append(f"### Scope: {scope}")
                lines.append("")
                for model_name, slice_entries in model_entries:
                    snapshot_bits = []
                    for slice_label, model_summary in slice_entries:
                        post_metrics = model_summary.get("conditions", {}).get("post_mitigation", {}).get("metrics", {})
                        post_error_tags = model_summary.get("conditions", {}).get("post_mitigation", {}).get("error_tags", {})
                        snapshot_bits.append(
                            f"{slice_label}: post avg={average_metric(post_metrics)}, "
                            f"delta avg={average_metric(model_summary.get('overall_delta', {}))}, "
                            f"post error tags={sum(post_error_tags.values())}"
                        )
                    lines.append("- " + model_name + ": " + "; ".join(snapshot_bits))
                lines.append("")
        lines.append("")

    lines.append("## Warnings")
    lines.append("")
    if warnings:
        for warning in warnings:
            lines.append(f"- {warning}")
    else:
        lines.append("- None")
    lines.append("")

    lines.append("## Summary")
    lines.append("")
    lines.append(
        "- `v0.3` evaluates real models (frontier API and open-source) against all 24 public-safe benchmark items with pre/post-mitigation comparison."
    )
    lines.append(
        f"- The release includes {audit_slice_count} audited evaluation slice{'s' if audit_slice_count != 1 else ''} spanning {audited_scope_text}, with structured scorecards, taxonomy coverage, and cross-model analysis."
    )
    lines.append(
        "- This version provides empirical grounding for the evaluation framework, moving beyond synthetic demos to production model behavior."
    )
    lines.append("")

    with output_path.open("w", encoding="utf-8") as handle:
        handle.write("\n".join(lines))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--inputs",
        type=Path,
        nargs="+",
        required=True,
        help="Public JSONL item files to include in the result package.",
    )
    parser.add_argument(
        "--coverage-summary",
        type=Path,
        required=True,
        help="Coverage summary JSON produced by check_taxonomy_coverage.py.",
    )
    parser.add_argument(
        "--release-manifest",
        type=Path,
        help="Optional release manifest JSON for artifact summary information.",
    )
    parser.add_argument(
        "--audit-summary",
        type=Path,
        action="append",
        default=[],
        help="Optional reviewed-response audit summary JSON for a public_eval audit slice. Repeat for multiple slices.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        required=True,
        help="Directory where result-package files will be written.",
    )
    args = parser.parse_args()

    items: list[dict] = []
    for path in args.inputs:
        items.extend(read_jsonl(path))

    coverage_summary = read_json(args.coverage_summary)
    release_manifest = read_json(args.release_manifest) if args.release_manifest else None
    audit_summaries = (
        {audit_slice_label(path): read_json(path) for path in args.audit_summary}
        if args.audit_summary
        else None
    )

    args.output_dir.mkdir(parents=True, exist_ok=True)
    inventory_path = args.output_dir / "benchmark_inventory.csv"
    scorecard_csv_path = args.output_dir / "release_scorecard.csv"
    scorecard_md_path = args.output_dir / "release_scorecard.md"
    slice_overview_csv_path = args.output_dir / "audit_slice_overview.csv"
    longitudinal_csv_path = args.output_dir / "audit_longitudinal_comparison.csv"
    longitudinal_md_path = args.output_dir / "audit_longitudinal_summary.md"

    write_inventory_csv(items, inventory_path)
    scorecard_rows = build_scorecard_rows(items, coverage_summary, release_manifest, audit_summaries)
    write_scorecard_csv(scorecard_rows, scorecard_csv_path)
    write_scorecard_markdown(coverage_summary, release_manifest, audit_summaries, scorecard_md_path)
    slice_overview_rows = build_audit_slice_overview_rows(audit_summaries)
    write_audit_slice_overview_csv(slice_overview_rows, slice_overview_csv_path)
    longitudinal_rows = build_audit_longitudinal_rows(slice_overview_rows)
    write_audit_longitudinal_csv(longitudinal_rows, longitudinal_csv_path)
    write_audit_longitudinal_markdown(longitudinal_rows, longitudinal_md_path)

    print(f"Wrote {inventory_path}")
    print(f"Wrote {scorecard_csv_path}")
    print(f"Wrote {scorecard_md_path}")
    print(f"Wrote {slice_overview_csv_path}")
    print(f"Wrote {longitudinal_csv_path}")
    print(f"Wrote {longitudinal_md_path}")


if __name__ == "__main__":
    main()
