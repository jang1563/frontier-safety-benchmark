#!/usr/bin/env python3
"""Generate a release manifest from one or more run manifests and release artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8192), b""):
            digest.update(chunk)
    return digest.hexdigest()


def resolve_project_path(path: Path) -> Path:
    if path.is_absolute():
        return path
    return (ROOT.parent / path).resolve()


def rel_to_project_root(path: Path) -> str:
    return str(resolve_project_path(path).relative_to(ROOT.parent))


def artifact_entry(path: Path, artifact_type: str) -> dict:
    return {
        "path": rel_to_project_root(path),
        "sha256": sha256_file(path),
        "size_bytes": path.stat().st_size,
        "artifact_type": artifact_type,
    }


def append_unique_artifact(artifacts: list[dict], artifact: dict, source_label: str) -> None:
    for existing in artifacts:
        if existing["path"] != artifact["path"]:
            continue
        if existing["artifact_type"] != artifact["artifact_type"]:
            raise ValueError(
                "Conflicting artifact types for "
                f"{artifact['path']}: {existing['artifact_type']} vs {artifact['artifact_type']} "
                f"(while processing {source_label})"
            )
        return
    artifacts.append(artifact)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--run-manifest",
        type=Path,
        action="append",
        required=True,
        help="Path to a run manifest JSON file. Repeat to include multiple runs in one release manifest.",
    )
    parser.add_argument("--release-version", required=True, help="Release version string, for example v0.2.0.")
    parser.add_argument(
        "--benchmark-version",
        required=True,
        help="Benchmark version string, for example 0.2.0-draft.",
    )
    parser.add_argument(
        "--extra-docs",
        type=Path,
        nargs="*",
        default=[],
        help="Optional extra documentation files to include in the manifest.",
    )
    parser.add_argument(
        "--extra-output-files",
        type=Path,
        nargs="*",
        default=[],
        help="Optional packaged output artifacts to include in the manifest.",
    )
    parser.add_argument("--output", type=Path, required=True, help="Path where the release manifest JSON will be written.")
    args = parser.parse_args()

    output_path = resolve_project_path(args.output)
    run_manifest_paths = [resolve_project_path(path) for path in args.run_manifest]

    input_artifacts = []
    output_artifacts = []
    metadata_artifacts = []
    generated_from_run_manifests: list[str] = []

    for run_manifest_path in run_manifest_paths:
        run_manifest = read_json(run_manifest_path)
        generated_from_run_manifests.append(rel_to_project_root(run_manifest_path))

        for rel_path in run_manifest["input_files"]:
            path = resolve_project_path(Path(rel_path))
            if not path.exists():
                raise FileNotFoundError(f"Missing input artifact listed in run manifest: {path}")
            append_unique_artifact(
                input_artifacts,
                artifact_entry(path, "input"),
                run_manifest_path.name,
            )
        for rel_path in run_manifest["output_files"]:
            path = resolve_project_path(Path(rel_path))
            if not path.exists():
                raise FileNotFoundError(f"Missing output artifact listed in run manifest: {path}")
            append_unique_artifact(
                output_artifacts,
                artifact_entry(path, "output"),
                run_manifest_path.name,
            )

        append_unique_artifact(
            metadata_artifacts,
            artifact_entry(run_manifest_path, "metadata"),
            run_manifest_path.name,
        )

    doc_artifacts = []
    for doc_path in args.extra_docs:
        resolved_doc_path = resolve_project_path(doc_path)
        if not resolved_doc_path.exists():
            raise FileNotFoundError(f"Missing extra doc artifact: {resolved_doc_path}")
        append_unique_artifact(
            doc_artifacts,
            artifact_entry(resolved_doc_path, "documentation"),
            "extra docs",
        )

    packaged_output_artifacts = []
    for output_file in args.extra_output_files:
        resolved_output_path = resolve_project_path(output_file)
        if not resolved_output_path.exists():
            raise FileNotFoundError(f"Missing extra output artifact: {resolved_output_path}")
        append_unique_artifact(
            packaged_output_artifacts,
            artifact_entry(resolved_output_path, "output"),
            "extra output files",
        )

    manifest = {
        "manifest_version": "release-manifest-v1",
        "release_version": args.release_version,
        "benchmark_version": args.benchmark_version,
        "generated_from_run_manifests": generated_from_run_manifests,
        "artifacts": input_artifacts + output_artifacts + packaged_output_artifacts + doc_artifacts + metadata_artifacts,
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as handle:
        json.dump(manifest, handle, indent=2)
        handle.write("\n")

    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
