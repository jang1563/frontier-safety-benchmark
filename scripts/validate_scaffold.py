#!/usr/bin/env python3
"""Validate the basic integrity of the public CBRN-AI 2.0 scaffold."""

from __future__ import annotations

import json
import re
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ITEMS_PATH = ROOT / "data_public" / "sample_items.jsonl"
RESPONSES_PATH = ROOT / "data_public" / "reviewed_sample_responses.jsonl"
PUBLIC_DEV_ITEMS_PATH = ROOT / "data_public" / "public_dev_items.jsonl"
PUBLIC_EVAL_ITEMS_PATH = ROOT / "data_public" / "public_eval_items.jsonl"
PUBLIC_DEV_RESPONSES_PATH = ROOT / "data_public" / "reviewed_public_dev_responses_v0_2_demo.jsonl"
PUBLIC_DEV_RESPONSES_SLICE_B_PATH = ROOT / "data_public" / "reviewed_public_dev_responses_v0_2_slice_b.jsonl"
PUBLIC_EVAL_RESPONSES_PATH = ROOT / "data_public" / "reviewed_public_eval_responses_v0_2_demo.jsonl"
PUBLIC_EVAL_RESPONSES_SLICE_B_PATH = ROOT / "data_public" / "reviewed_public_eval_responses_v0_2_slice_b.jsonl"
RUN_MANIFEST_PATH = ROOT / "data_public" / "run_manifest_demo.json"
PUBLIC_DEV_AUDIT_RUN_MANIFEST_PATH = ROOT / "data_public" / "run_manifest_public_dev_audit_demo.json"
PUBLIC_DEV_AUDIT_SLICE_B_RUN_MANIFEST_PATH = ROOT / "data_public" / "run_manifest_public_dev_audit_slice_b.json"
PUBLIC_EVAL_AUDIT_RUN_MANIFEST_PATH = ROOT / "data_public" / "run_manifest_public_eval_audit_demo.json"
PUBLIC_EVAL_AUDIT_SLICE_B_RUN_MANIFEST_PATH = ROOT / "data_public" / "run_manifest_public_eval_audit_slice_b.json"
RELEASE_MANIFEST_PATH = ROOT / "results" / "v0_2_demo" / "release_manifest.json"
VALID_CONDITIONS = {"pre_mitigation", "post_mitigation"}
PUBLIC_ITEM_SCHEMA_PATH = ROOT / "schemas" / "public_item.schema.json"
REVIEWED_RESPONSE_SCHEMA_PATH = ROOT / "schemas" / "reviewed_response.schema.json"
RUN_MANIFEST_SCHEMA_PATH = ROOT / "schemas" / "run_manifest.schema.json"
RELEASE_MANIFEST_SCHEMA_PATH = ROOT / "schemas" / "release_manifest.schema.json"


def read_jsonl(path: Path) -> list[dict]:
    records = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}: invalid JSON on line {line_number}") from exc
    return records


def read_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8192), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_against_schema(value: object, schema: dict, context: str) -> None:
    expected_type = schema.get("type")
    if expected_type == "object":
        if not isinstance(value, dict):
            raise ValueError(f"{context}: expected object")
        required = schema.get("required", [])
        missing = sorted(key for key in required if key not in value)
        if missing:
            raise ValueError(f"{context}: missing required keys: {', '.join(missing)}")
        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            extras = sorted(key for key in value if key not in properties)
            if extras:
                raise ValueError(f"{context}: unexpected keys: {', '.join(extras)}")
        for key, property_schema in properties.items():
            if key in value:
                validate_against_schema(value[key], property_schema, f"{context}.{key}")
        return

    if expected_type == "array":
        if not isinstance(value, list):
            raise ValueError(f"{context}: expected array")
        min_items = schema.get("minItems")
        if min_items is not None and len(value) < min_items:
            raise ValueError(f"{context}: expected at least {min_items} items")
        item_schema = schema.get("items")
        if item_schema is not None:
            for index, item in enumerate(value):
                validate_against_schema(item, item_schema, f"{context}[{index}]")
        return

    if expected_type == "string":
        if not isinstance(value, str):
            raise ValueError(f"{context}: expected string")
        min_length = schema.get("minLength")
        if min_length is not None and len(value) < min_length:
            raise ValueError(f"{context}: expected minLength {min_length}")
        pattern = schema.get("pattern")
        if pattern is not None and re.fullmatch(pattern, value) is None:
            raise ValueError(f"{context}: does not match pattern {pattern}")
    elif expected_type == "integer":
        if type(value) is not int:
            raise ValueError(f"{context}: expected integer")
        minimum = schema.get("minimum")
        maximum = schema.get("maximum")
        if minimum is not None and value < minimum:
            raise ValueError(f"{context}: expected value >= {minimum}")
        if maximum is not None and value > maximum:
            raise ValueError(f"{context}: expected value <= {maximum}")

    enum_values = schema.get("enum")
    if enum_values is not None and value not in enum_values:
        raise ValueError(f"{context}: expected one of {enum_values}, got {value!r}")


def validate_items(items: list[dict]) -> dict[str, dict]:
    item_schema = read_json(PUBLIC_ITEM_SCHEMA_PATH)
    seen = {}
    for record in items:
        validate_against_schema(record, item_schema, f"item {record.get('item_id', '<unknown>')}")
        item_id = record["item_id"]
        if item_id in seen:
            raise ValueError(f"duplicate item_id found: {item_id}")
        seen[item_id] = record
    return seen


def validate_responses(responses: list[dict], items: dict[str, dict]) -> None:
    response_schema = read_json(REVIEWED_RESPONSE_SCHEMA_PATH)
    seen_triplets: set[tuple[str, str, str]] = set()
    coverage: dict[str, dict[str, set[str]]] = {}
    for record in responses:
        validate_against_schema(
            record,
            response_schema,
            f"response {record.get('item_id', '<unknown>')}/{record.get('condition', '<unknown>')}",
        )
        item_id = record["item_id"]
        if item_id not in items:
            raise ValueError(f"response references unknown item_id: {item_id}")
        condition = record["condition"]
        model_name = record["model_name"]
        triplet = (item_id, condition, model_name)
        if triplet in seen_triplets:
            raise ValueError(
                f"duplicate review row found for item_id={item_id}, condition={condition}, model_name={model_name}"
            )
        seen_triplets.add(triplet)
        coverage.setdefault(model_name, {}).setdefault(item_id, set()).add(condition)

    expected_items = set(items.keys())
    for model_name, item_map in sorted(coverage.items()):
        missing_items = sorted(expected_items - set(item_map.keys()))
        if missing_items:
            raise ValueError(
                f"model {model_name}: missing reviewed items: {', '.join(missing_items)}"
            )
        for item_id in sorted(expected_items):
            conditions = item_map[item_id]
            if conditions != VALID_CONDITIONS:
                missing = ", ".join(sorted(VALID_CONDITIONS - conditions))
                raise ValueError(
                    f"model {model_name}, item {item_id}: missing reviewed conditions: {missing}"
                )


def validate_manifest_paths(manifest: dict, keys: list[str], base_context: str) -> None:
    for key in keys:
        for rel_path in manifest.get(key, []):
            path = ROOT.parent / rel_path
            if not path.exists():
                raise ValueError(f"{base_context}: referenced file does not exist: {rel_path}")


def validate_run_manifest(path: Path) -> None:
    if not path.exists():
        return False
    schema = read_json(RUN_MANIFEST_SCHEMA_PATH)
    manifest = read_json(path)
    validate_against_schema(manifest, schema, f"run manifest {path.name}")
    script_path = ROOT.parent / manifest["script_path"]
    if not script_path.exists():
        raise ValueError(f"run manifest {path.name}: script_path does not exist: {manifest['script_path']}")
    validate_manifest_paths(manifest, ["input_files", "output_files"], f"run manifest {path.name}")
    return True


def validate_release_manifest(path: Path) -> None:
    if not path.exists():
        return False
    schema = read_json(RELEASE_MANIFEST_SCHEMA_PATH)
    manifest = read_json(path)
    validate_against_schema(manifest, schema, f"release manifest {path.name}")
    for rel_path in manifest["generated_from_run_manifests"]:
        run_manifest_path = ROOT.parent / rel_path
        if not run_manifest_path.exists():
            raise ValueError(
                f"release manifest {path.name}: generated_from_run_manifests path does not exist: "
                f"{rel_path}"
            )
        validate_run_manifest(run_manifest_path)
    seen_paths: set[str] = set()
    for artifact in manifest["artifacts"]:
        if artifact["path"] in seen_paths:
            raise ValueError(
                f"release manifest {path.name}: duplicate artifact path: {artifact['path']}"
            )
        seen_paths.add(artifact["path"])
        artifact_path = ROOT.parent / artifact["path"]
        if not artifact_path.exists():
            raise ValueError(
                f"release manifest {path.name}: referenced artifact does not exist: {artifact['path']}"
            )
        if artifact_path.stat().st_size != artifact["size_bytes"]:
            raise ValueError(
                f"release manifest {path.name}: size mismatch for {artifact['path']}"
            )
        if sha256_file(artifact_path) != artifact["sha256"]:
            raise ValueError(
                f"release manifest {path.name}: sha256 mismatch for {artifact['path']}"
            )
    return True


def main() -> None:
    items = read_jsonl(ITEMS_PATH)
    responses = read_jsonl(RESPONSES_PATH)
    item_index = validate_items(items)
    validate_responses(responses, item_index)

    optional_v0_2_summaries: list[tuple[str, str, int, int]] = []
    optional_items_cache: dict[Path, tuple[list[dict], dict[str, dict]]] = {}
    optional_audits = [
        ("public_dev", "demo", PUBLIC_DEV_ITEMS_PATH, PUBLIC_DEV_RESPONSES_PATH),
        ("public_dev", "slice_b", PUBLIC_DEV_ITEMS_PATH, PUBLIC_DEV_RESPONSES_SLICE_B_PATH),
        ("public_eval", "slice_a", PUBLIC_EVAL_ITEMS_PATH, PUBLIC_EVAL_RESPONSES_PATH),
        ("public_eval", "slice_b", PUBLIC_EVAL_ITEMS_PATH, PUBLIC_EVAL_RESPONSES_SLICE_B_PATH),
    ]
    for scope, label, items_path, response_path in optional_audits:
        if items_path.exists() and response_path.exists():
            if items_path not in optional_items_cache:
                scope_items = read_jsonl(items_path)
                optional_items_cache[items_path] = (scope_items, validate_items(scope_items))
            scope_items, scope_index = optional_items_cache[items_path]
            scope_responses = read_jsonl(response_path)
            validate_responses(scope_responses, scope_index)
            optional_v0_2_summaries.append(
                (scope, label, len(scope_items), len(scope_responses))
            )

    run_manifest_validated = False
    for manifest_path in [
        RUN_MANIFEST_PATH,
        PUBLIC_DEV_AUDIT_RUN_MANIFEST_PATH,
        PUBLIC_DEV_AUDIT_SLICE_B_RUN_MANIFEST_PATH,
        PUBLIC_EVAL_AUDIT_RUN_MANIFEST_PATH,
        PUBLIC_EVAL_AUDIT_SLICE_B_RUN_MANIFEST_PATH,
    ]:
        run_manifest_validated = validate_run_manifest(manifest_path) or run_manifest_validated
    release_manifest_validated = validate_release_manifest(RELEASE_MANIFEST_PATH)
    print("Scaffold validation passed.")
    print(f"Validated {len(items)} public items and {len(responses)} reviewed responses.")
    for scope, label, item_count, response_count in optional_v0_2_summaries:
        print(
            f"Validated optional v0.2 {scope} demo {label}: "
            f"{item_count} items and {response_count} reviewed responses."
        )
    print(f"Run manifest validated: {'yes' if run_manifest_validated else 'no'}")
    print(f"Release manifest validated: {'yes' if release_manifest_validated else 'no'}")


if __name__ == "__main__":
    main()
