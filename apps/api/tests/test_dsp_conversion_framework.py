from __future__ import annotations

import copy
import csv
import hashlib
import io
import json
import math
import os
import re
import stat
import subprocess
from collections import Counter
from pathlib import Path, PurePosixPath
from typing import Any

import pytest

from elp_api.catalog import CatalogError, CourseCatalog
from elp_api.models import CourseManifest
from elp_api.runtime import ExperimentRuntime

ROOT = Path(__file__).resolve().parents[3]
COURSE_ROOT = ROOT / "courses" / "dsp-radar"
SOURCE_MAP_PATH = COURSE_ROOT / "source-map.yaml"
CONVERSION_MANIFEST_PATH = COURSE_ROOT / "conversion-manifest.yaml"
COVERAGE_PATH = COURSE_ROOT / "coverage.yaml"
CONVERSION_SCHEMA_PATH = COURSE_ROOT / "conversion.schema.json"
AUTHORING_PATH = COURSE_ROOT / "AUTHORING.md"

EXPECTED_SOURCE_REPOSITORY = "kpbianco/dsp-radar_learning"
EXPECTED_SOURCE_COMMIT = "5d73667a486df4a7b6c581e4c9406e810ed4f0f6"
EXPECTED_SOURCE_TREE = "7a3a0f9adce607e10097724c13745eace212f4e1"
EXPECTED_CURRICULUM_SHA256 = "0b92e76efc1f72930fab730145326315219ab3813b8cbf17d32a33f507a4974f"
EXPECTED_FILE_SET_SHA256 = "c2511015b195a48bd847bd1f1cdeed92384a10eddf0b23e755590af4fb66ddca"
EXPECTED_SOURCE_MAP_SHA256 = "dc46c37e2f1e8701127a504200c7a4fd9f84a9da5d7f2064474195eec7cb0e05"
EXPECTED_CONVERSION_MANIFEST_SHA256 = (
    "a6b7699ddb8b3a5b9e099fd382a555c3e7ea8345bb88fcdee4f054c1e636e193"
)
EXPECTED_COURSE_SHA256 = "9950220969a64e5c7faed96ae1f8a2395339c7dbd292a9471c89001a2a5d0228"
EXPECTED_CONVERSION_SCHEMA_SHA256 = (
    "8d728f2158c95944ff7ee3ba599bfdddb91e937099d94c8b601c2a43bd1ea73f"
)
EXPECTED_AUTHORING_SHA256 = "77b1d9497c085aad3fd2f3ff1f45113344420408f05893e4c23d2c68a7d64721"
EXPECTED_GITMODULES_SHA256 = "acbd5f8bfe9675bc25216b8494570dff4ceecd7f5553a60b4618db99f3ea442f"
EXPECTED_PHASE_COUNTS = {1: 10, 2: 10, 3: 8, 4: 14, 5: 10, 6: 8, 7: 8, 8: 6, 9: 10}
REQUIRED_SOURCE_FILES = ("README.md", "lesson.md", "walkthrough.md", "checks.md", "experiment.m")
HEX_64 = re.compile(r"^[0-9a-f]{64}$")
STABLE_COVERAGE_KEYS = (
    "id",
    "number",
    "source_folder",
    "target_module_id",
    "target_folder",
    "batch_id",
)
SUPPORTED_SCHEMA_KEYWORDS = {
    "$defs",
    "$id",
    "$ref",
    "$schema",
    "additionalProperties",
    "const",
    "description",
    "enum",
    "exclusiveMinimum",
    "items",
    "maximum",
    "maxItems",
    "minimum",
    "minItems",
    "minLength",
    "oneOf",
    "pattern",
    "properties",
    "required",
    "title",
    "type",
    "uniqueItems",
}
IMAGE_SUFFIXES = {".gif", ".jpeg", ".jpg", ".png", ".svg", ".webp"}

EXPECTED_GITLINKS = {
    "courses/controls-gnc-learning": "ffd6623ee2cf8ccd8599fffd935ef07370750fa3",
    "courses/distributed-realtime-learning": "97f455503e6d2ae65a87b31968bae4c32d2f7bc3",
    "courses/dsp-radar-learning": EXPECTED_SOURCE_COMMIT,
    "courses/embedded-rt-hil-learning": "0ab836efcace36158687a467f64225bd5cff8177",
    "courses/flight-dynamics-learning": "131cc662845614d362133f685e0c159091001f76",
    "courses/fpga-data-path-learning": "bf3d168ae4ab48ce4264d95f1b77a97a8d028f14",
    "courses/hwil-systems-learning": "94f12813572d0e4a0d3f30b4d143151a0066e074",
    "courses/numerical-optimization-learning": "4014f89fcfcdc18e037b4216cd42048f9adc400a",
    "courses/reliability-fdir-learning": "e604208c90c5424e6bd9dbcc22837b0fb2228c32",
    "courses/rf-lab-learning": "5b1650d5ddc42757e14b27b112de1528ce0f7460",
    "courses/robotics-autonomy-learning": "f8807640258f1a6c1c77f1dcc9e61734551c585b",
    "courses/stats-estimation-learning": "c5bc5ab6b723bfd9afd9039379628ceac3cff411",
    "courses/vehicle-dynamics-learning": "916c3e6a9cbbc9e1c4ede821e894132b13c3b9c8",
}


class DuplicateJsonKey(ValueError):
    pass


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load_yaml(path: Path) -> dict[str, Any]:
    value, _ = CourseCatalog._read_yaml(path)
    return value


def _unique_json_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            raise DuplicateJsonKey(f"duplicate JSON key {key!r}")
        value[key] = item
    return value


def _reject_json_constant(value: str) -> None:
    raise ValueError(f"non-finite JSON constant {value}")


def _load_json(path: Path) -> dict[str, Any]:
    value = json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=_unique_json_object,
        parse_constant=_reject_json_constant,
    )
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected a JSON object")
    return value


def _exact_keys(value: Any, expected: set[str], path: str, errors: list[str]) -> None:
    if not isinstance(value, dict):
        errors.append(f"{path}: expected mapping")
        return
    actual = set(value)
    if actual != expected:
        errors.append(
            f"{path}: fields differ; missing={sorted(expected - actual)} "
            f"unknown={sorted(actual - expected)}"
        )


def _exact_v1(value: Any) -> bool:
    return type(value) is int and value == 1


def _normalized_relative(value: Any) -> bool:
    if not isinstance(value, str) or not value or "\\" in value:
        return False
    path = PurePosixPath(value)
    return (
        not path.is_absolute()
        and path.as_posix() == value
        and all(part not in {"", ".", ".."} for part in path.parts)
    )


def _canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _same_json_value(first: Any, second: Any) -> bool:
    return _canonical(first) == _canonical(second)


def _matches_json_type(value: Any, expected: str) -> bool:
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "boolean":
        return type(value) is bool
    if expected == "integer":
        return type(value) is int
    if expected == "number":
        return type(value) in {int, float} and math.isfinite(value)
    if expected == "null":
        return value is None
    raise AssertionError(f"unsupported JSON Schema type {expected!r}")


def _resolve_local_ref(root_schema: dict[str, Any], reference: str) -> dict[str, Any]:
    if not reference.startswith("#/"):
        raise AssertionError(f"only local JSON Schema references are supported: {reference}")
    value: Any = root_schema
    for raw_part in reference[2:].split("/"):
        part = raw_part.replace("~1", "/").replace("~0", "~")
        value = value[part]
    if not isinstance(value, dict):
        raise AssertionError(f"JSON Schema reference does not resolve to an object: {reference}")
    return value


def _schema_errors(
    value: Any,
    schema: dict[str, Any],
    root_schema: dict[str, Any],
    path: str = "$",
) -> list[str]:
    errors: list[str] = []
    if "$ref" in schema:
        target = _resolve_local_ref(root_schema, schema["$ref"])
        errors.extend(_schema_errors(value, target, root_schema, path))
        siblings = {key: item for key, item in schema.items() if key != "$ref"}
        if siblings:
            errors.extend(_schema_errors(value, siblings, root_schema, path))
        return errors

    if "oneOf" in schema:
        branches = [_schema_errors(value, branch, root_schema, path) for branch in schema["oneOf"]]
        passed = sum(not branch_errors for branch_errors in branches)
        if passed != 1:
            errors.append(f"{path}: expected exactly one oneOf branch, found {passed}")
        schema = {key: item for key, item in schema.items() if key != "oneOf"}

    if "const" in schema and not _same_json_value(value, schema["const"]):
        errors.append(f"{path}: expected const {schema['const']!r}")
    if "enum" in schema and not any(_same_json_value(value, item) for item in schema["enum"]):
        errors.append(f"{path}: value is not in enum")

    expected_type = schema.get("type")
    if expected_type is not None:
        candidates = expected_type if isinstance(expected_type, list) else [expected_type]
        if not any(_matches_json_type(value, item) for item in candidates):
            errors.append(f"{path}: expected JSON type {expected_type!r}")
            return errors

    if isinstance(value, dict):
        required = set(schema.get("required", []))
        missing = required - set(value)
        if missing:
            errors.append(f"{path}: missing required fields {sorted(missing)}")
        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            unknown = set(value) - set(properties)
            if unknown:
                errors.append(f"{path}: unknown fields {sorted(unknown)}")
        for key, item in value.items():
            if key in properties:
                errors.extend(_schema_errors(item, properties[key], root_schema, f"{path}.{key}"))

    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            errors.append(f"{path}: fewer than minItems")
        if "maxItems" in schema and len(value) > schema["maxItems"]:
            errors.append(f"{path}: more than maxItems")
        if schema.get("uniqueItems") and len({_canonical(item) for item in value}) != len(value):
            errors.append(f"{path}: array items are not unique")
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for index, item in enumerate(value):
                errors.extend(_schema_errors(item, item_schema, root_schema, f"{path}[{index}]"))

    if isinstance(value, str):
        if len(value) < schema.get("minLength", 0):
            errors.append(f"{path}: string is shorter than minLength")
        if "pattern" in schema and re.search(schema["pattern"], value) is None:
            errors.append(f"{path}: string does not match pattern")

    if type(value) in {int, float} and not isinstance(value, bool):
        if not math.isfinite(value):
            errors.append(f"{path}: number is non-finite")
        if "minimum" in schema and value < schema["minimum"]:
            errors.append(f"{path}: number is below minimum")
        if "maximum" in schema and value > schema["maximum"]:
            errors.append(f"{path}: number is above maximum")
        if "exclusiveMinimum" in schema and value <= schema["exclusiveMinimum"]:
            errors.append(f"{path}: number is not above exclusiveMinimum")
    return errors


def _schema_object_nodes(value: Any, path: str = "$schema") -> list[tuple[str, dict[str, Any]]]:
    values: list[tuple[str, dict[str, Any]]] = []
    if isinstance(value, dict):
        if value.get("type") == "object":
            values.append((path, value))
        for key, child in value.items():
            values.extend(_schema_object_nodes(child, f"{path}.{key}"))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            values.extend(_schema_object_nodes(child, f"{path}[{index}]"))
    return values


def _unsupported_schema_keywords(schema: dict[str, Any], path: str = "$schema") -> list[str]:
    errors = [
        f"{path}: unsupported JSON Schema keyword {key!r}"
        for key in schema
        if key not in SUPPORTED_SCHEMA_KEYWORDS
    ]
    for container in ("$defs", "properties"):
        children = schema.get(container, {})
        if isinstance(children, dict):
            for key, child in children.items():
                if isinstance(child, dict):
                    errors.extend(_unsupported_schema_keywords(child, f"{path}.{container}.{key}"))
    item_schema = schema.get("items")
    if isinstance(item_schema, dict):
        errors.extend(_unsupported_schema_keywords(item_schema, f"{path}.items"))
    for index, child in enumerate(schema.get("oneOf", [])):
        if isinstance(child, dict):
            errors.extend(_unsupported_schema_keywords(child, f"{path}.oneOf[{index}]"))
    additional = schema.get("additionalProperties")
    if isinstance(additional, dict):
        errors.extend(_unsupported_schema_keywords(additional, f"{path}.additionalProperties"))
    return errors


def _framework_errors(
    source_map: dict[str, Any],
    conversion_manifest: dict[str, Any],
    coverage: dict[str, Any],
) -> list[str]:
    errors: list[str] = []
    _exact_keys(source_map, {"schema_version", "source", "items"}, "source-map", errors)
    _exact_keys(
        conversion_manifest,
        {"schema_version", "course_id", "source_map_file", "source_map_sha256", "items"},
        "conversion-manifest",
        errors,
    )
    _exact_keys(
        coverage,
        {
            "schema_version",
            "course_id",
            "source_map_file",
            "source_map_sha256",
            "conversion_manifest_file",
            "conversion_manifest_sha256",
            "summary",
            "items",
        },
        "coverage",
        errors,
    )
    versions = (source_map, conversion_manifest, coverage)
    if not all(_exact_v1(item.get("schema_version")) for item in versions):
        errors.append("all framework schema_version values must be the exact integer 1")
    if any(item.get("course_id") != "dsp-radar" for item in (conversion_manifest, coverage)):
        errors.append("framework course_id must be dsp-radar")
    if conversion_manifest.get("source_map_file") != "source-map.yaml":
        errors.append("conversion manifest source_map_file drift")
    if coverage.get("source_map_file") != "source-map.yaml":
        errors.append("coverage source_map_file drift")
    if coverage.get("conversion_manifest_file") != "conversion-manifest.yaml":
        errors.append("coverage conversion_manifest_file drift")
    if conversion_manifest.get("source_map_sha256") != EXPECTED_SOURCE_MAP_SHA256:
        errors.append("conversion manifest source-map binding drift")
    if coverage.get("source_map_sha256") != EXPECTED_SOURCE_MAP_SHA256:
        errors.append("coverage source-map binding drift")
    if coverage.get("conversion_manifest_sha256") != EXPECTED_CONVERSION_MANIFEST_SHA256:
        errors.append("coverage conversion-manifest binding drift")

    source = source_map.get("source")
    _exact_keys(
        source,
        {
            "repository",
            "commit",
            "tree",
            "curriculum",
            "required_files",
            "aggregate_file_set_sha256",
        },
        "source-map.source",
        errors,
    )
    if isinstance(source, dict):
        expected_source = {
            "repository": EXPECTED_SOURCE_REPOSITORY,
            "commit": EXPECTED_SOURCE_COMMIT,
            "tree": EXPECTED_SOURCE_TREE,
            "required_files": list(REQUIRED_SOURCE_FILES),
            "aggregate_file_set_sha256": EXPECTED_FILE_SET_SHA256,
        }
        for key, expected in expected_source.items():
            if source.get(key) != expected:
                errors.append(f"source-map.source.{key} drift")
        curriculum = source.get("curriculum")
        _exact_keys(curriculum, {"path", "sha256"}, "source-map.source.curriculum", errors)
        if not isinstance(curriculum, dict) or curriculum != {
            "path": "curriculum/modules.json",
            "sha256": EXPECTED_CURRICULUM_SHA256,
        }:
            errors.append("source curriculum identity drift")

    source_items = source_map.get("items")
    conversion_items = conversion_manifest.get("items")
    coverage_items = coverage.get("items")
    item_sets = (source_items, conversion_items, coverage_items)
    if not all(isinstance(value, list) for value in item_sets):
        errors.append("framework items must be lists")
        return errors
    assert isinstance(source_items, list)
    assert isinstance(conversion_items, list)
    assert isinstance(coverage_items, list)
    if not (len(source_items) == len(conversion_items) == len(coverage_items) == 84):
        errors.append("framework must contain exactly 84 entries in every ledger")
        return errors

    all_files: list[dict[str, Any]] = []
    for index, (source_item, conversion_item, coverage_item) in enumerate(
        zip(source_items, conversion_items, coverage_items, strict=True), start=1
    ):
        item_id = f"P{index:02d}"
        source_path = f"source-map.items[{index - 1}]"
        conversion_path = f"conversion-manifest.items[{index - 1}]"
        coverage_path = f"coverage.items[{index - 1}]"
        _exact_keys(
            source_item,
            {
                "id",
                "number",
                "source_folder",
                "title",
                "guiding_question",
                "phase",
                "phase_title",
                "files",
            },
            source_path,
            errors,
        )
        _exact_keys(
            conversion_item,
            {
                "id",
                "number",
                "source_folder",
                "target_module_id",
                "target_folder",
                "title",
                "guiding_question",
                "phase",
                "phase_title",
                "batch_id",
            },
            conversion_path,
            errors,
        )
        _exact_keys(
            coverage_item,
            {
                "id",
                "number",
                "source_folder",
                "target_module_id",
                "target_folder",
                "batch_id",
                "status",
                "conversion_record",
                "target_content_digest",
                "blocker",
            },
            coverage_path,
            errors,
        )
        item_triplet = (source_item, conversion_item, coverage_item)
        if not all(isinstance(item, dict) for item in item_triplet):
            continue
        expected_identity = {"id": item_id, "number": index}
        for item, path in (
            (source_item, source_path),
            (conversion_item, conversion_path),
            (coverage_item, coverage_path),
        ):
            if any(item.get(key) != value for key, value in expected_identity.items()):
                errors.append(f"{path}: identity/order drift")
        source_folder = source_item.get("source_folder")
        if not _normalized_relative(source_folder) or not str(source_folder).startswith(
            f"modules/{index:02d}-"
        ):
            errors.append(f"{source_path}: invalid source folder")
        target_module_id = str(source_folder).removeprefix("modules/")
        expected_stable = {
            "id": item_id,
            "number": index,
            "source_folder": source_folder,
            "target_module_id": target_module_id,
            "target_folder": source_folder,
            "batch_id": f"ELP-DSP-P{index:02d}",
        }
        for key, expected in expected_stable.items():
            if conversion_item.get(key) != expected:
                errors.append(f"{conversion_path}.{key}: mapping drift")
            if coverage_item.get(key) != expected:
                errors.append(f"{coverage_path}.{key}: mapping drift")
        for key in ("title", "guiding_question", "phase", "phase_title"):
            if conversion_item.get(key) != source_item.get(key):
                errors.append(f"{conversion_path}.{key}: source-map drift")
        files = source_item.get("files")
        if not isinstance(files, list) or len(files) != 5:
            errors.append(f"{source_path}.files: expected five source files")
            continue
        expected_paths = [f"{source_folder}/{name}" for name in REQUIRED_SOURCE_FILES]
        actual_paths: list[Any] = []
        for file_index, file_identity in enumerate(files):
            _exact_keys(
                file_identity,
                {"path", "sha256"},
                f"{source_path}.files[{file_index}]",
                errors,
            )
            if isinstance(file_identity, dict):
                actual_paths.append(file_identity.get("path"))
                if not HEX_64.fullmatch(str(file_identity.get("sha256", ""))):
                    errors.append(f"{source_path}.files[{file_index}]: invalid SHA-256")
                all_files.append(file_identity)
        if actual_paths != expected_paths:
            errors.append(f"{source_path}.files: path, order, or required file-set drift")

    ids = [item.get("id") for item in source_items if isinstance(item, dict)]
    folders = [item.get("source_folder") for item in source_items if isinstance(item, dict)]
    if len(set(ids)) != 84 or len(set(folders)) != 84:
        errors.append("source-map identities and folders must be unique")
    file_paths = [item.get("path") for item in all_files]
    if len(all_files) != 420 or len(set(file_paths)) != 420:
        errors.append("source-map must contain exactly 420 unique file paths")
    phase_counts = Counter(item.get("phase") for item in source_items if isinstance(item, dict))
    if dict(phase_counts) != EXPECTED_PHASE_COUNTS:
        errors.append("source-map phase distribution drift")
    records = "".join(
        f"{item['sha256']}  {item['path']}\n"
        for item in sorted(all_files, key=lambda candidate: candidate["path"])
    ).encode()
    if hashlib.sha256(records).hexdigest() != EXPECTED_FILE_SET_SHA256:
        errors.append("source-map aggregate file-set digest drift")
    errors.extend(_coverage_errors(coverage, conversion_manifest))
    return errors


def _blocker_errors(value: Any, path: str) -> list[str]:
    errors: list[str] = []
    _exact_keys(value, {"reason", "evidence"}, path, errors)
    if not isinstance(value, dict):
        return errors
    if not isinstance(value.get("reason"), str) or not value["reason"].strip():
        errors.append(f"{path}.reason: required")
    evidence = value.get("evidence")
    if not isinstance(evidence, list) or not evidence:
        errors.append(f"{path}.evidence: at least one retained evidence path is required")
    elif any(not _normalized_relative(item) for item in evidence):
        errors.append(f"{path}.evidence: paths must be normalized and relative")
    return errors


def _retained_file(
    relative: Any, roots: tuple[Path, ...], path: str, errors: list[str]
) -> Path | None:
    if not _normalized_relative(relative):
        errors.append(f"{path}: path must be normalized and relative")
        return None
    matches: list[Path] = []
    for root in dict.fromkeys(candidate.resolve() for candidate in roots):
        candidate = root / relative
        resolved = candidate.resolve()
        if root not in resolved.parents:
            continue
        if candidate.is_file() and not candidate.is_symlink():
            matches.append(candidate)
    if len(matches) != 1:
        errors.append(f"{path}: retained file must exist exactly once, found={len(matches)}")
        return None
    return matches[0]


def _numeric_leaf_errors(value: Any, path: str) -> tuple[list[str], int]:
    if type(value) in {int, float}:
        return ([] if math.isfinite(value) else [f"{path}: non-finite numeric value"], 1)
    if isinstance(value, list):
        errors: list[str] = []
        count = 0
        for index, item in enumerate(value):
            child_errors, child_count = _numeric_leaf_errors(item, f"{path}[{index}]")
            errors.extend(child_errors)
            count += child_count
        return errors, count
    if isinstance(value, dict):
        errors = []
        count = 0
        for key, item in value.items():
            child_errors, child_count = _numeric_leaf_errors(item, f"{path}.{key}")
            errors.extend(child_errors)
            count += child_count
        return errors, count
    return [f"{path}: expected numeric scalar/vector content"], 0


def _numeric_file_errors(candidate: Path, path: str) -> list[str]:
    if candidate.suffix.lower() in IMAGE_SUFFIXES:
        return [f"{path}: image evidence cannot be a numeric result"]
    try:
        text = candidate.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return [f"{path}: numeric evidence must be retained UTF-8 JSON or delimited text"]
    try:
        value = json.loads(text, parse_constant=_reject_json_constant)
    except (json.JSONDecodeError, ValueError):
        delimiter = "\t" if candidate.suffix.lower() == ".tsv" else ","
        rows = [row for row in csv.reader(io.StringIO(text), delimiter=delimiter) if row]
        if not rows:
            return [f"{path}: numeric evidence is empty"]
        numeric_rows = rows
        try:
            [float(cell) for cell in rows[0] if cell.strip()]
        except ValueError:
            numeric_rows = rows[1:]
        cells = [cell.strip() for row in numeric_rows for cell in row if cell.strip()]
        if not cells:
            return [f"{path}: numeric evidence has no values"]
        try:
            numbers = [float(cell) for cell in cells]
        except ValueError:
            return [f"{path}: numeric evidence contains non-numeric values"]
        if not all(math.isfinite(item) for item in numbers):
            return [f"{path}: numeric evidence contains non-finite values"]
        return []
    errors, count = _numeric_leaf_errors(value, path)
    if count == 0:
        errors.append(f"{path}: numeric evidence has no values")
    return errors


def _file_identity_errors(
    identity: dict[str, Any],
    roots: tuple[Path, ...],
    path: str,
    *,
    numeric: bool = False,
) -> tuple[list[str], Path | None]:
    errors: list[str] = []
    candidate = _retained_file(identity.get("path"), roots, f"{path}.path", errors)
    if candidate is not None:
        if _sha256(candidate) != identity.get("sha256"):
            errors.append(f"{path}.sha256: retained file identity mismatch")
        if numeric:
            errors.extend(_numeric_file_errors(candidate, path))
    return errors, candidate


def _coverage_errors(coverage: dict[str, Any], conversion_manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    items = coverage.get("items")
    expected_items = conversion_manifest.get("items")
    summary = coverage.get("summary")
    summary_keys = {"total", "pending", "converted", "blocked", "placeholder"}
    _exact_keys(summary, summary_keys, "coverage.summary", errors)
    if not isinstance(items, list) or not isinstance(expected_items, list):
        return errors + ["coverage and conversion items must be lists"]
    if len(items) != len(expected_items):
        return errors + ["coverage/conversion item counts differ"]
    statuses: list[Any] = []
    for index, (item, expected) in enumerate(zip(items, expected_items, strict=True)):
        if not isinstance(item, dict) or not isinstance(expected, dict):
            errors.append(f"coverage.items[{index}]: expected mapping")
            continue
        for key in STABLE_COVERAGE_KEYS:
            if item.get(key) != expected.get(key):
                errors.append(f"coverage.items[{index}].{key}: immutable field drift")
        status_value = item.get("status")
        statuses.append(status_value)
        record = item.get("conversion_record")
        content_digest = item.get("target_content_digest")
        blocker = item.get("blocker")
        if status_value == "pending":
            if any(value is not None for value in (record, content_digest, blocker)):
                errors.append(f"coverage.items[{index}]: pending item carries completion state")
        elif status_value == "converted":
            expected_record = f"{item['target_folder']}/conversion.yaml"
            if record != expected_record:
                errors.append(f"coverage.items[{index}]: converted record path mismatch")
            if not HEX_64.fullmatch(str(content_digest or "")):
                errors.append(f"coverage.items[{index}]: converted target digest is invalid")
            if blocker is not None:
                errors.append(f"coverage.items[{index}]: converted item cannot carry blocker")
        elif status_value == "blocked":
            if record is not None or content_digest is not None:
                errors.append(f"coverage.items[{index}]: blocked item carries converted state")
            errors.extend(_blocker_errors(blocker, f"coverage.items[{index}].blocker"))
        else:
            errors.append(f"coverage.items[{index}]: unsupported status {status_value!r}")
    counts = Counter(statuses)
    expected_summary = {
        "total": len(items),
        "pending": counts["pending"],
        "converted": counts["converted"],
        "blocked": counts["blocked"],
        "placeholder": 0,
    }
    if summary != expected_summary:
        errors.append("coverage summary does not equal derived state counts")
    converted_count = counts["converted"]
    blocked_count = counts["blocked"]
    expected_statuses = ["converted"] * converted_count
    if blocked_count:
        if blocked_count != 1:
            errors.append("coverage may contain at most one ordered blocker")
        expected_statuses.append("blocked")
    expected_statuses.extend(["pending"] * (len(items) - len(expected_statuses)))
    if statuses != expected_statuses:
        errors.append("coverage states must form converted prefix, optional blocker, pending tail")
    return errors


def _record_semantic_errors(
    record: dict[str, Any],
    source_map: dict[str, Any],
    conversion_item: dict[str, Any],
    coverage_item: dict[str, Any],
    schema: dict[str, Any],
    course_root: Path | None = None,
    repository_root: Path | None = None,
) -> list[str]:
    errors = _schema_errors(record, schema, schema)
    if errors:
        return errors
    source_item = source_map["items"][conversion_item["number"] - 1]
    item = record["item"]
    for key in ("id", "number", "source_folder", "target_module_id", "target_folder", "batch_id"):
        if item.get(key) != conversion_item.get(key):
            errors.append(f"conversion record item.{key} mapping drift")
    if item.get("source_map_sha256") != EXPECTED_SOURCE_MAP_SHA256:
        errors.append("conversion record source-map binding drift")
    if item.get("source_inputs") != source_item.get("files"):
        errors.append("conversion record source inputs differ from immutable source map")
    if record["content"].get("guiding_question") != conversion_item.get("guiding_question"):
        errors.append("conversion record guiding question drift")
    if record["target"].get("content_digest") != coverage_item.get("target_content_digest"):
        errors.append("conversion record target digest differs from coverage")
    target_prefix = f"{conversion_item['target_folder']}/"
    target_paths = [item["path"] for item in record["target"]["files"]]
    if any(not path.startswith(target_prefix) for path in target_paths):
        errors.append("conversion record target file escapes mapped target folder")
    if len(set(target_paths)) != len(target_paths):
        errors.append("conversion record target files are duplicated")
    required_target_paths = {
        f"{conversion_item['target_folder']}/module.yaml",
        f"{conversion_item['target_folder']}/lesson.md",
        f"{conversion_item['target_folder']}/experiment.py",
    }
    if not required_target_paths <= set(target_paths):
        errors.append("conversion record omits a required target module input")
    if course_root is not None:
        for index, identity in enumerate(record["target"]["files"]):
            identity_errors, _ = _file_identity_errors(
                identity, (course_root,), f"target.files[{index}]"
            )
            errors.extend(identity_errors)

    content = record["content"]
    if content["equation_order"] != "before_toolbox_shortcuts":
        errors.append("conversion record does not put equations before shortcuts")
    dataset_names = [item["name"] for item in content["deterministic_data"]["datasets"]]
    if len(dataset_names) != len(set(dataset_names)):
        errors.append("conversion record dataset names are duplicated")
    plot_keys = [item["target_plot_key"] for item in content["plot_sequence"]]
    if len(plot_keys) != len(set(plot_keys)):
        errors.append("conversion record target plot keys are duplicated")
    for plot in content["plot_sequence"]:
        axis_roles = [axis["role"] for axis in plot["axes"]]
        if len(axis_roles) != len(set(axis_roles)):
            errors.append(f"conversion plot {plot['target_plot_key']!r} duplicates an axis role")

    equivalence = record["python_source_equivalence"]
    if equivalence["seed"] != content["deterministic_data"]["seed"]:
        errors.append("Python equivalence seed differs from deterministic lesson seed")
    input_names = [item["name"] for item in equivalence["inputs"]]
    if len(input_names) != len(set(input_names)):
        errors.append("Python equivalence input names are duplicated")
    case_names = [item["name"] for item in equivalence["cases"]]
    if len(case_names) != len(set(case_names)):
        errors.append("Python equivalence case names are duplicated")
    if not equivalence["command"].strip():
        errors.append("Python equivalence command must not be blank")
    for case in equivalence["cases"]:
        tolerance = case["tolerance"]
        if case["max_absolute_error"] > tolerance["absolute"]:
            errors.append(f"equivalence case {case['name']!r} exceeds absolute tolerance")
        if case["max_relative_error"] > tolerance["relative"]:
            errors.append(f"equivalence case {case['name']!r} exceeds relative tolerance")
        if case["expected"]["path"] == case["actual"]["path"]:
            errors.append(f"equivalence case {case['name']!r} compares one file to itself")
        for result_name in ("expected", "actual"):
            result_path = case[result_name]["path"]
            if not result_path.startswith(target_prefix):
                errors.append(
                    f"equivalence case {case['name']!r} {result_name} escapes target folder"
                )
            if PurePosixPath(result_path).suffix.lower() in IMAGE_SUFFIXES:
                errors.append(
                    f"equivalence case {case['name']!r} uses image evidence as numeric result"
                )
            if course_root is not None:
                identity_errors, _ = _file_identity_errors(
                    case[result_name],
                    (course_root,),
                    f"python_source_equivalence.{case['name']}.{result_name}",
                    numeric=True,
                )
                errors.extend(identity_errors)

    matlab = record["matlab_runtime_parity"]
    if matlab["status"] in {"passed", "failed"}:
        for key in ("runtime", "version", "command"):
            if not matlab[key].strip():
                errors.append(f"MATLAB {key} must not be blank")
        matlab_input_names = [item["name"] for item in matlab["inputs"]]
        if len(matlab_input_names) != len(set(matlab_input_names)):
            errors.append("MATLAB parity input names are duplicated")
        if matlab["seed"] != content["deterministic_data"]["seed"]:
            errors.append("MATLAB parity seed differs from deterministic lesson seed")
        evidence_roots = tuple(root for root in (course_root, repository_root) if root is not None)
        evidence_candidates: list[Path] = []
        for index, identity in enumerate(matlab["evidence"]):
            evidence_path = PurePosixPath(identity["path"])
            if evidence_path.suffix.lower() in IMAGE_SUFFIXES | {".m", ".py"}:
                errors.append("MATLAB runtime evidence cannot be screenshot/source-only")
            if evidence_roots:
                identity_errors, candidate = _file_identity_errors(
                    identity, evidence_roots, f"matlab_runtime_parity.evidence[{index}]"
                )
                errors.extend(identity_errors)
                if candidate is not None:
                    evidence_candidates.append(candidate)
        if evidence_roots and not evidence_candidates:
            errors.append("MATLAB runtime parity has no retained execution evidence")
    elif not matlab["reason"].strip():
        errors.append("MATLAB not_run reason must not be blank")

    if matlab["status"] == "passed":
        matlab_case_names = [item["name"] for item in matlab["cases"]]
        if len(matlab_case_names) != len(set(matlab_case_names)):
            errors.append("MATLAB parity case names are duplicated")
        for case in matlab["cases"]:
            tolerance = case["tolerance"]
            if case["max_absolute_error"] > tolerance["absolute"]:
                errors.append(f"MATLAB case {case['name']!r} exceeds absolute tolerance")
            if case["max_relative_error"] > tolerance["relative"]:
                errors.append(f"MATLAB case {case['name']!r} exceeds relative tolerance")
            if case["expected"]["path"] == case["actual"]["path"]:
                errors.append(f"MATLAB case {case['name']!r} compares one file to itself")
            for result_name in ("expected", "actual"):
                if PurePosixPath(case[result_name]["path"]).suffix.lower() in IMAGE_SUFFIXES:
                    errors.append(
                        f"MATLAB case {case['name']!r} uses image evidence as numeric result"
                    )
                if course_root is not None:
                    identity_errors, _ = _file_identity_errors(
                        case[result_name],
                        (course_root,),
                        f"matlab_runtime_parity.{case['name']}.{result_name}",
                        numeric=True,
                    )
                    errors.extend(identity_errors)

    evidence_roots = tuple(root for root in (course_root, repository_root) if root is not None)
    for review_name in ("browser_visual_review", "accessibility_review"):
        review = record["claims"][review_name]
        if review["status"] == "not_run":
            if not review["reason"].strip():
                errors.append(f"{review_name} not_run reason must not be blank")
            continue
        if not review["summary"].strip():
            errors.append(f"{review_name} summary must not be blank")
        if evidence_roots:
            for index, identity in enumerate(review["evidence"]):
                identity_errors, _ = _file_identity_errors(
                    identity, evidence_roots, f"claims.{review_name}.evidence[{index}]"
                )
                errors.extend(identity_errors)
    if not record["claims"]["learner_effectiveness"]["reason"].strip():
        errors.append("learner_effectiveness not_run reason must not be blank")
    return errors


def _retained_coverage_errors(
    coverage: dict[str, Any],
    source_map: dict[str, Any],
    conversion_manifest: dict[str, Any],
    schema: dict[str, Any],
    course_root: Path,
    repository_root: Path,
) -> list[str]:
    errors = _coverage_errors(coverage, conversion_manifest)
    converted = [item for item in coverage.get("items", []) if item.get("status") == "converted"]
    try:
        catalog = CourseCatalog([course_root])
    except CatalogError as exc:
        return errors + [f"converted course cannot load: {exc}"]
    actual_module_ids = {module.manifest.id for module in catalog.course("dsp-radar").modules}
    expected_module_ids = {item["target_module_id"] for item in converted}
    if actual_module_ids != expected_module_ids:
        errors.append(
            "catalog-visible module set differs from converted coverage: "
            f"missing={sorted(expected_module_ids - actual_module_ids)} "
            f"unexpected={sorted(actual_module_ids - expected_module_ids)}"
        )
    for index, item in enumerate(coverage.get("items", [])):
        if item.get("status") == "blocked":
            for evidence_index, relative in enumerate(item["blocker"]["evidence"]):
                _retained_file(
                    relative,
                    (repository_root,),
                    f"coverage.items[{index}].blocker.evidence[{evidence_index}]",
                    errors,
                )
            continue
        if item.get("status") != "converted":
            continue
        record_path = _retained_file(
            item.get("conversion_record"),
            (course_root,),
            f"coverage.items[{index}].conversion_record",
            errors,
        )
        if record_path is None:
            continue
        try:
            record = _load_yaml(record_path)
        except CatalogError as exc:
            errors.append(f"coverage.items[{index}].conversion_record: {exc}")
            continue
        errors.extend(
            _record_semantic_errors(
                record,
                source_map,
                conversion_manifest["items"][index],
                item,
                schema,
                course_root,
                repository_root,
            )
        )
        try:
            _, module = catalog.module_record("dsp-radar", item["target_module_id"])
        except KeyError:
            errors.append(f"coverage.items[{index}]: converted native module is missing")
            continue
        expected_module_path = (course_root / item["target_folder"]).resolve()
        if module.path != expected_module_path:
            errors.append(f"coverage.items[{index}]: native module path drift")
        conversion_item = conversion_manifest["items"][index]
        expected_manifest = {
            "id": item["target_module_id"],
            "number": item["number"],
            "title": conversion_item["title"],
            "guiding_question": conversion_item["guiding_question"],
            "status": "implemented",
        }
        for key, expected in expected_manifest.items():
            if getattr(module.manifest, key) != expected:
                errors.append(f"coverage.items[{index}]: native module {key} drift")
        if module.manifest.runtime.kind != "python":
            errors.append(f"coverage.items[{index}]: native module runtime is not Python")
        else:
            runtime = record["runtime"]
            for key in ("entrypoint", "trust", "timeout_seconds"):
                if getattr(module.manifest.runtime, key) != runtime[key]:
                    errors.append(f"coverage.items[{index}]: runtime {key} record drift")
        if module.revision.content_digest != item["target_content_digest"]:
            errors.append(f"coverage.items[{index}]: CourseCatalog content digest drift")
        listed = {(entry["path"], entry["sha256"]) for entry in record["target"]["files"]}
        for relative, digest in module.input_hashes:
            identity = (f"{item['target_folder']}/{relative}", digest)
            if identity not in listed:
                errors.append(
                    f"coverage.items[{index}]: target identities omit accepted input {relative}"
                )
    return errors


def _transition_errors(
    before: dict[str, Any],
    after: dict[str, Any],
    source_map: dict[str, Any],
    conversion_manifest: dict[str, Any],
    schema: dict[str, Any],
    records: dict[str, dict[str, Any]],
    course_root: Path | None = None,
    repository_root: Path | None = None,
) -> list[str]:
    errors = _coverage_errors(before, conversion_manifest)
    errors.extend(_coverage_errors(after, conversion_manifest))
    if before.get("source_map_sha256") != after.get("source_map_sha256"):
        errors.append("transition changed source-map identity")
    if before.get("conversion_manifest_sha256") != after.get("conversion_manifest_sha256"):
        errors.append("transition changed conversion-manifest identity")
    before_items = before.get("items", [])
    after_items = after.get("items", [])
    if len(before_items) != len(after_items):
        return errors + ["transition changed item count"]
    changed = [
        index
        for index, (old, new) in enumerate(zip(before_items, after_items, strict=True))
        if old != new
    ]
    if len(changed) != 1:
        return errors + [f"transition must change exactly one item, changed={changed}"]
    index = changed[0]
    old = before_items[index]
    new = after_items[index]
    for key in STABLE_COVERAGE_KEYS:
        if old.get(key) != new.get(key):
            errors.append(f"transition changed immutable field {key}")
    if old.get("status") != "pending":
        errors.append("transition source state must be pending")
    earliest_pending = next(
        (
            item_index
            for item_index, item in enumerate(before_items)
            if item.get("status") == "pending"
        ),
        None,
    )
    if earliest_pending != index:
        errors.append("transition did not change the earliest pending item")
    if any(item.get("status") == "blocked" for item in before_items):
        errors.append("blocked coverage stops the ordered conversion lane")
    if new.get("status") == "converted":
        record_path = new.get("conversion_record")
        record = records.get(record_path)
        if record is None:
            errors.append("converted transition has no retained conversion record")
        else:
            errors.extend(
                _record_semantic_errors(
                    record,
                    source_map,
                    conversion_manifest["items"][index],
                    new,
                    schema,
                    course_root,
                    repository_root,
                )
            )
    elif new.get("status") == "blocked":
        errors.extend(_blocker_errors(new.get("blocker"), f"coverage.items[{index}].blocker"))
    else:
        errors.append("transition must end in converted or blocked")
    return errors


def _valid_conversion_record(
    source_map: dict[str, Any], conversion_manifest: dict[str, Any], number: int = 1
) -> dict[str, Any]:
    source_item = source_map["items"][number - 1]
    item = conversion_manifest["items"][number - 1]
    target_folder = item["target_folder"]
    return {
        "schema_version": 1,
        "course_id": "dsp-radar",
        "item": {
            key: item[key]
            for key in (
                "id",
                "number",
                "source_folder",
                "target_module_id",
                "target_folder",
                "batch_id",
            )
        }
        | {
            "source_map_sha256": EXPECTED_SOURCE_MAP_SHA256,
            "source_inputs": copy.deepcopy(source_item["files"]),
        },
        "target": {
            "content_digest": "a" * 64,
            "files": [
                {"path": f"{target_folder}/module.yaml", "sha256": "b" * 64},
                {"path": f"{target_folder}/lesson.md", "sha256": "c" * 64},
                {"path": f"{target_folder}/experiment.py", "sha256": "d" * 64},
            ],
        },
        "content": {
            "guiding_question": item["guiding_question"],
            "physical_model": "A sampled sinusoid traces a rotating phasor.",
            "signal_flow": ["Choose amplitude", "Sample the waveform", "Inspect the phasor"],
            "equations": [{"latex": "x[n]=A\\cos(2\\pi fn/F_s+\\phi)", "meaning": "Sampled tone"}],
            "equation_order": "before_toolbox_shortcuts",
            "deterministic_data": {
                "seed": 101,
                "constants": [{"name": "sample_rate", "value": 1000, "unit": "Hz"}],
                "datasets": [
                    {
                        "name": "baseline samples",
                        "provenance": "generated",
                        "sha256": "4" * 64,
                        "unit": "V",
                    }
                ],
            },
            "plot_sequence": [
                {
                    "source_figure": "Figure 1",
                    "target_plot_key": "waveform",
                    "title": "Sampled waveform",
                    "axes": [
                        {"role": "x", "label": "Time", "unit": "s"},
                        {"role": "y", "label": "Amplitude", "unit": "V"},
                    ],
                    "interpretation": "Amplitude changes scale without changing frequency.",
                }
            ],
            "sweeps": [
                {
                    "control": "amplitude",
                    "values": [0.5, 1.0],
                    "expected_observation": "The waveform and phasor radius scale together.",
                },
                {
                    "control": "phase_deg",
                    "values": [0, 90],
                    "expected_observation": "Phase moves the initial sample and phasor angle.",
                },
            ],
            "broken_case": {
                "trigger": "Sample below Nyquist",
                "failure": "The observed frequency aliases.",
                "recovery": "Restore a sufficient sample rate.",
                "expected_observation": "The original frequency returns.",
            },
            "common_mistakes": ["Treating phase as a time-independent amplitude change."],
            "completion_checklist": ["Explain amplitude, frequency, and phase in both views."],
        },
        "runtime": {
            "kind": "python",
            "entrypoint": "experiment.py:run",
            "trust": "local-trusted",
            "timeout_seconds": 3.0,
            "max_samples": 4096,
            "max_output_bytes": 1_000_000,
        },
        "python_source_equivalence": {
            "status": "passed",
            "command": "python3 -m pytest -q tests/test_p01_conversion.py",
            "seed": 101,
            "inputs": [{"name": "amplitude", "value": 1.0, "unit": "V"}],
            "cases": [
                {
                    "name": "baseline-waveform",
                    "units": "V",
                    "tolerance": {"absolute": 1e-12, "relative": 1e-12},
                    "expected": {
                        "path": f"{target_folder}/fixtures/expected.json",
                        "sha256": "e" * 64,
                    },
                    "actual": {
                        "path": f"{target_folder}/fixtures/actual.json",
                        "sha256": "e" * 64,
                    },
                    "max_absolute_error": 0.0,
                    "max_relative_error": 0.0,
                    "passed": True,
                }
            ],
        },
        "matlab_runtime_parity": {
            "status": "not_run",
            "reason": "A licensed MATLAB runtime was not available for this software batch.",
        },
        "claims": {
            "profile": "elp-dsp-item-software-v1",
            "browser_visual_review": {"status": "not_run", "reason": "Not part of fixture."},
            "accessibility_review": {"status": "not_run", "reason": "Not part of fixture."},
            "learner_effectiveness": {"status": "not_run", "reason": "Not part of fixture."},
        },
    }


def _converted_coverage(
    coverage: dict[str, Any], conversion_manifest: dict[str, Any], number: int = 1
) -> dict[str, Any]:
    value = copy.deepcopy(coverage)
    item = value["items"][number - 1]
    item["status"] = "converted"
    item["conversion_record"] = f"{item['target_folder']}/conversion.yaml"
    item["target_content_digest"] = "a" * 64
    item["blocker"] = None
    value["summary"] = {
        "total": 84,
        "pending": 83,
        "converted": 1,
        "blocked": 0,
        "placeholder": 0,
    }
    assert item["target_module_id"] == conversion_manifest["items"][number - 1]["target_module_id"]
    return value


def _blocked_coverage(coverage: dict[str, Any], number: int = 1) -> dict[str, Any]:
    value = copy.deepcopy(coverage)
    item = value["items"][number - 1]
    item["status"] = "blocked"
    item["blocker"] = {
        "reason": "The source requires a renderer primitive outside the current contract.",
        "evidence": ["docs/evidence/ELP-DSP-P01-blocker.md"],
    }
    value["summary"] = {
        "total": 84,
        "pending": 83,
        "converted": 0,
        "blocked": 1,
        "placeholder": 0,
    }
    return value


def _retained_converted_fixture(
    tmp_path: Path,
    source_map: dict[str, Any],
    conversion_manifest: dict[str, Any],
    coverage: dict[str, Any],
) -> tuple[Path, Path, dict[str, Any], dict[str, Any]]:
    repository_root = tmp_path / "repository"
    course_root = repository_root / "courses" / "dsp-radar"
    course_root.mkdir(parents=True)
    (course_root / "course.yaml").write_bytes((COURSE_ROOT / "course.yaml").read_bytes())
    item = conversion_manifest["items"][0]
    module_root = course_root / item["target_folder"]
    fixtures = module_root / "fixtures"
    fixtures.mkdir(parents=True)
    module = {
        "schema_version": 1,
        "id": item["target_module_id"],
        "number": item["number"],
        "title": item["title"],
        "summary": "Synthetic retained conversion fixture.",
        "guiding_question": item["guiding_question"],
        "status": "implemented",
        "tags": ["dsp-radar"],
        "runtime": {
            "kind": "python",
            "entrypoint": "experiment.py:run",
            "trust": "local-trusted",
            "timeout_seconds": 3.0,
        },
        "controls": [],
        "blocks": [
            {"type": "markdown", "source": "lesson.md"},
            {
                "type": "prediction",
                "text": "What should remain deterministic?",
                "reveal": "The retained numeric vector.",
            },
        ],
    }
    (module_root / "module.yaml").write_text(json.dumps(module, indent=2) + "\n", encoding="utf-8")
    (module_root / "lesson.md").write_text("# Retained fixture\n", encoding="utf-8")
    (module_root / "experiment.py").write_text(
        "def run(parameters):\n    return {}\n", encoding="utf-8"
    )
    for name in ("expected.json", "actual.json"):
        (fixtures / name).write_text("[0.0, 1.0]\n", encoding="utf-8")

    catalog = CourseCatalog([course_root])
    _, module_record = catalog.module_record("dsp-radar", item["target_module_id"])
    converted = _converted_coverage(coverage, conversion_manifest)
    converted["items"][0]["target_content_digest"] = module_record.revision.content_digest
    record = _valid_conversion_record(source_map, conversion_manifest)
    record["target"]["content_digest"] = module_record.revision.content_digest
    record["python_source_equivalence"]["cases"][0]["tolerance"] = {
        "absolute": 0.0,
        "relative": 0.0,
    }
    record["target"]["files"] = [
        {
            "path": f"{item['target_folder']}/{relative}",
            "sha256": digest,
        }
        for relative, digest in module_record.input_hashes
    ]
    for result_name in ("expected", "actual"):
        relative = f"{item['target_folder']}/fixtures/{result_name}.json"
        record["python_source_equivalence"]["cases"][0][result_name] = {
            "path": relative,
            "sha256": _sha256(course_root / relative),
        }
    conversion_path = course_root / converted["items"][0]["conversion_record"]
    conversion_path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    return repository_root, course_root, converted, record


def _git(*args: str, cwd: Path = ROOT, check: bool = True) -> subprocess.CompletedProcess[str]:
    environment = os.environ | {"GIT_OPTIONAL_LOCKS": "0"}
    return subprocess.run(
        ["git", *args],
        cwd=cwd,
        env=environment,
        check=check,
        capture_output=True,
        text=True,
    )


def _tree_snapshot(root: Path) -> tuple[tuple[str, int, str], ...]:
    values: list[tuple[str, int, str]] = []
    paths = [root, *sorted(root.rglob("*"))]
    for path in paths:
        relative = "." if path == root else path.relative_to(root).as_posix()
        info = path.lstat()
        mode = stat.S_IMODE(info.st_mode)
        if path.is_symlink():
            identity = "symlink:" + os.readlink(path)
        elif path.is_file():
            identity = hashlib.sha256(path.read_bytes()).hexdigest()
        else:
            identity = "dir"
        values.append((relative, mode, identity))
    return tuple(values)


def test_framework_yaml_and_json_reject_duplicate_keys(tmp_path: Path) -> None:
    duplicate_yaml = tmp_path / "duplicate.yaml"
    duplicate_yaml.write_text(
        "schema_version: 1\nouter:\n  value: one\n  value: two\n", encoding="utf-8"
    )
    with pytest.raises(CatalogError, match="duplicate key"):
        _load_yaml(duplicate_yaml)
    duplicate_json = tmp_path / "duplicate.json"
    duplicate_json.write_text('{"outer":{"value":1,"value":2}}\n', encoding="utf-8")
    with pytest.raises(DuplicateJsonKey, match="duplicate JSON key"):
        _load_json(duplicate_json)


@pytest.mark.parametrize("bad_version", [None, True, 1.0, "1", 0, -1, 2])
def test_framework_manifests_require_exact_integer_version_one(bad_version: Any) -> None:
    source_map = _load_yaml(SOURCE_MAP_PATH)
    conversion_manifest = _load_yaml(CONVERSION_MANIFEST_PATH)
    coverage = _load_yaml(COVERAGE_PATH)
    for value in (source_map, conversion_manifest, coverage):
        mutated = copy.deepcopy(value)
        if bad_version is None:
            mutated.pop("schema_version")
        else:
            mutated["schema_version"] = bad_version
        inputs = [
            copy.deepcopy(source_map),
            copy.deepcopy(conversion_manifest),
            copy.deepcopy(coverage),
        ]
        inputs[(source_map, conversion_manifest, coverage).index(value)] = mutated
        assert _framework_errors(*inputs), f"accepted framework schema_version={bad_version!r}"


def test_conversion_schema_is_closed_and_accepts_complete_record() -> None:
    schema = _load_json(CONVERSION_SCHEMA_PATH)
    assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
    assert schema["properties"]["schema_version"] == {"type": "integer", "const": 1}
    assert _sha256(CONVERSION_SCHEMA_PATH) == EXPECTED_CONVERSION_SCHEMA_SHA256
    object_nodes = _schema_object_nodes(schema)
    assert object_nodes
    assert all(node.get("additionalProperties") is False for _, node in object_nodes)
    assert _unsupported_schema_keywords(schema) == []
    record = _valid_conversion_record(
        _load_yaml(SOURCE_MAP_PATH), _load_yaml(CONVERSION_MANIFEST_PATH)
    )
    assert _schema_errors(record, schema, schema) == []


@pytest.mark.parametrize(
    "mutation",
    [
        lambda value: value.update({"unknown": True}),
        lambda value: value["runtime"].update({"unknown": True}),
        lambda value: value["item"].update({"source_folder": "../escape"}),
        lambda value: value["item"].update({"source_folder": "modules/./escape"}),
        lambda value: value["python_source_equivalence"].update({"status": "skipped"}),
        lambda value: value["python_source_equivalence"].update({"cases": []}),
        lambda value: value["python_source_equivalence"]["cases"][0].update({"passed": False}),
        lambda value: value.update(
            {
                "python_source_equivalence": {
                    "status": "passed",
                    "command": "screenshot.png",
                    "cases": [{"screenshot": "result.png"}],
                }
            }
        ),
        lambda value: value.update(
            {"matlab_runtime_parity": {"status": "passed", "runtime": "MATLAB"}}
        ),
        lambda value: value["matlab_runtime_parity"].update({"evidence": "screenshot.png"}),
        lambda value: value["claims"].update(
            {"browser_visual_review": {"status": "passed", "summary": "Looks good"}}
        ),
        lambda value: value["claims"].update({"profile": "complete-professional-course"}),
        lambda value: value["claims"].update(
            {
                "learner_effectiveness": {
                    "status": "passed",
                    "summary": "Synthetic claim",
                    "evidence": [{"path": "evidence/learner.png", "sha256": "1" * 64}],
                }
            }
        ),
    ],
    ids=[
        "top-level-extra",
        "nested-extra",
        "path-escape",
        "dot-path-segment",
        "python-skip",
        "missing-equivalence-cases",
        "failed-equivalence-case",
        "screenshot-only-equivalence",
        "unsupported-matlab-pass",
        "not-run-with-pass-evidence",
        "manual-pass-without-evidence",
        "claim-profile-promotion",
        "learner-effectiveness-promotion",
    ],
)
def test_conversion_schema_rejects_incomplete_or_overclaimed_records(mutation: Any) -> None:
    source_map = _load_yaml(SOURCE_MAP_PATH)
    conversion_manifest = _load_yaml(CONVERSION_MANIFEST_PATH)
    schema = _load_json(CONVERSION_SCHEMA_PATH)
    record = _valid_conversion_record(source_map, conversion_manifest)
    mutation(record)
    assert _schema_errors(record, schema, schema)


@pytest.mark.parametrize("bad_version", [None, True, 1.0, "1", 0, -1, 2])
def test_conversion_record_requires_exact_integer_version_one(bad_version: Any) -> None:
    schema = _load_json(CONVERSION_SCHEMA_PATH)
    record = _valid_conversion_record(
        _load_yaml(SOURCE_MAP_PATH), _load_yaml(CONVERSION_MANIFEST_PATH)
    )
    if bad_version is None:
        record.pop("schema_version")
    else:
        record["schema_version"] = bad_version
    assert _schema_errors(record, schema, schema)


def test_exact_84_item_mapping_hashes_and_retained_converted_prefix() -> None:
    source_map = _load_yaml(SOURCE_MAP_PATH)
    conversion_manifest = _load_yaml(CONVERSION_MANIFEST_PATH)
    coverage = _load_yaml(COVERAGE_PATH)
    assert _sha256(SOURCE_MAP_PATH) == EXPECTED_SOURCE_MAP_SHA256
    assert _sha256(CONVERSION_MANIFEST_PATH) == EXPECTED_CONVERSION_MANIFEST_SHA256
    assert _sha256(COURSE_ROOT / "course.yaml") == EXPECTED_COURSE_SHA256
    assert _sha256(AUTHORING_PATH) == EXPECTED_AUTHORING_SHA256
    assert _framework_errors(source_map, conversion_manifest, coverage) == []
    assert (
        _retained_coverage_errors(
            coverage,
            source_map,
            conversion_manifest,
            _load_json(CONVERSION_SCHEMA_PATH),
            COURSE_ROOT,
            ROOT,
        )
        == []
    )
    converted = coverage["summary"]["converted"]
    assert coverage["summary"] == {
        "total": 84,
        "pending": 84 - converted,
        "converted": converted,
        "blocked": 0,
        "placeholder": 0,
    }
    assert [item["status"] for item in coverage["items"]] == (
        ["converted"] * converted + ["pending"] * (84 - converted)
    )
    assert [item["id"] for item in coverage["items"]] == [
        f"P{number:02d}" for number in range(1, 85)
    ]


@pytest.mark.parametrize(
    ("document", "mutation"),
    [
        ("source", lambda value: value["items"].pop()),
        ("source", lambda value: value["items"].append(copy.deepcopy(value["items"][0]))),
        ("source", lambda value: value["items"].__setitem__(slice(0, 2), value["items"][1::-1])),
        ("source", lambda value: value["items"][0].update({"source_folder": "../escape"})),
        ("source", lambda value: value["items"][0]["files"][0].update({"sha256": "0" * 64})),
        ("conversion", lambda value: value["items"][0].update({"title": "Renamed"})),
        ("conversion", lambda value: value["items"][0].update({"target_module_id": "wrong"})),
        ("coverage", lambda value: value["items"][0].update({"batch_id": "ELP-DSP-P02"})),
        ("coverage", lambda value: value.update({"unknown": True})),
    ],
    ids=[
        "omitted-item",
        "duplicated-item",
        "reordered-items",
        "source-path-escape",
        "source-hash-drift",
        "title-drift",
        "target-id-drift",
        "batch-drift",
        "unknown-field",
    ],
)
def test_framework_rejects_mapping_and_immutable_field_drift(document: str, mutation: Any) -> None:
    values = {
        "source": _load_yaml(SOURCE_MAP_PATH),
        "conversion": _load_yaml(CONVERSION_MANIFEST_PATH),
        "coverage": _load_yaml(COVERAGE_PATH),
    }
    mutation(values[document])
    assert _framework_errors(values["source"], values["conversion"], values["coverage"])


def test_legal_single_item_converted_and_blocked_transitions(tmp_path: Path) -> None:
    source_map = _load_yaml(SOURCE_MAP_PATH)
    conversion_manifest = _load_yaml(CONVERSION_MANIFEST_PATH)
    coverage = _load_yaml(COVERAGE_PATH)
    for item in coverage["items"]:
        item.update(
            {
                "status": "pending",
                "conversion_record": None,
                "target_content_digest": None,
                "blocker": None,
            }
        )
    coverage["summary"] = {
        "total": 84,
        "pending": 84,
        "converted": 0,
        "blocked": 0,
        "placeholder": 0,
    }
    schema = _load_json(CONVERSION_SCHEMA_PATH)
    repository_root, course_root, converted, record = _retained_converted_fixture(
        tmp_path, source_map, conversion_manifest, coverage
    )
    records = {converted["items"][0]["conversion_record"]: record}
    assert (
        _transition_errors(
            coverage,
            converted,
            source_map,
            conversion_manifest,
            schema,
            records,
            course_root,
            repository_root,
        )
        == []
    )
    assert (
        _retained_coverage_errors(
            converted, source_map, conversion_manifest, schema, course_root, repository_root
        )
        == []
    )
    blocked = _blocked_coverage(coverage)
    blocked_repository_root = tmp_path / "blocked-repository"
    blocked_course_root = blocked_repository_root / "courses" / "dsp-radar"
    blocked_course_root.mkdir(parents=True)
    (blocked_course_root / "course.yaml").write_bytes((COURSE_ROOT / "course.yaml").read_bytes())
    blocker_path = blocked_repository_root / blocked["items"][0]["blocker"]["evidence"][0]
    blocker_path.parent.mkdir(parents=True, exist_ok=True)
    blocker_path.write_text("Reviewed blocker evidence.\n", encoding="utf-8")
    assert _transition_errors(coverage, blocked, source_map, conversion_manifest, schema, {}) == []
    assert (
        _retained_coverage_errors(
            blocked,
            source_map,
            conversion_manifest,
            schema,
            blocked_course_root,
            blocked_repository_root,
        )
        == []
    )


def test_illegal_bulk_out_of_order_and_unattested_transitions_fail() -> None:
    source_map = _load_yaml(SOURCE_MAP_PATH)
    conversion_manifest = _load_yaml(CONVERSION_MANIFEST_PATH)
    coverage = _load_yaml(COVERAGE_PATH)
    schema = _load_json(CONVERSION_SCHEMA_PATH)
    valid_record = _valid_conversion_record(source_map, conversion_manifest)

    no_record = _converted_coverage(coverage, conversion_manifest)
    assert "no retained conversion record" in " ".join(
        _transition_errors(coverage, no_record, source_map, conversion_manifest, schema, {})
    )

    out_of_order = _converted_coverage(coverage, conversion_manifest, number=2)
    out_of_order["summary"].update({"pending": 83, "converted": 1})
    record_two = _valid_conversion_record(source_map, conversion_manifest, number=2)
    path_two = out_of_order["items"][1]["conversion_record"]
    assert _transition_errors(
        coverage,
        out_of_order,
        source_map,
        conversion_manifest,
        schema,
        {path_two: record_two},
    )

    bulk = _converted_coverage(coverage, conversion_manifest)
    second = bulk["items"][1]
    second.update(
        {
            "status": "converted",
            "conversion_record": f"{second['target_folder']}/conversion.yaml",
            "target_content_digest": "a" * 64,
        }
    )
    bulk["summary"].update({"pending": 82, "converted": 2})
    assert "exactly one item" in " ".join(
        _transition_errors(
            coverage,
            bulk,
            source_map,
            conversion_manifest,
            schema,
            {
                bulk["items"][0]["conversion_record"]: valid_record,
                second["conversion_record"]: record_two,
            },
        )
    )

    drift = _converted_coverage(coverage, conversion_manifest)
    drift["items"][0]["target_folder"] = "modules/01-renamed"
    assert _transition_errors(coverage, drift, source_map, conversion_manifest, schema, {})

    over_tolerance = _valid_conversion_record(source_map, conversion_manifest)
    over_tolerance["python_source_equivalence"]["cases"][0]["max_absolute_error"] = 1.0
    path = no_record["items"][0]["conversion_record"]
    assert "exceeds absolute tolerance" in " ".join(
        _transition_errors(
            coverage,
            no_record,
            source_map,
            conversion_manifest,
            schema,
            {path: over_tolerance},
        )
    )

    semantic_mutations = {
        "duplicated": lambda value: value["python_source_equivalence"]["cases"].append(
            copy.deepcopy(value["python_source_equivalence"]["cases"][0])
        ),
        "input names are duplicated": lambda value: value["python_source_equivalence"][
            "inputs"
        ].append(copy.deepcopy(value["python_source_equivalence"]["inputs"][0])),
        "seed differs": lambda value: value["python_source_equivalence"].update({"seed": 999}),
        "uses image evidence": lambda value: value["python_source_equivalence"]["cases"][0][
            "expected"
        ].update({"path": f"{value['item']['target_folder']}/expected.png"}),
        "compares one file to itself": lambda value: value["python_source_equivalence"]["cases"][
            0
        ].update(
            {"actual": copy.deepcopy(value["python_source_equivalence"]["cases"][0]["expected"])}
        ),
    }
    for expected_message, mutation in semantic_mutations.items():
        mutated = _valid_conversion_record(source_map, conversion_manifest)
        mutation(mutated)
        transition_errors = _transition_errors(
            coverage,
            no_record,
            source_map,
            conversion_manifest,
            schema,
            {path: mutated},
        )
        assert expected_message in " ".join(transition_errors)

    matlab_pass = _valid_conversion_record(source_map, conversion_manifest)
    matlab_case = copy.deepcopy(matlab_pass["python_source_equivalence"]["cases"][0])
    matlab_case["max_absolute_error"] = 1.0
    matlab_pass["matlab_runtime_parity"] = {
        "status": "passed",
        "runtime": "MATLAB",
        "version": "R2026a",
        "toolboxes": [],
        "command": "matlab -batch verify",
        "seed": 101,
        "inputs": copy.deepcopy(matlab_pass["python_source_equivalence"]["inputs"]),
        "cases": [matlab_case],
        "evidence": [{"path": "evidence/matlab.log", "sha256": "f" * 64}],
    }
    assert "MATLAB case 'baseline-waveform' exceeds absolute tolerance" in " ".join(
        _record_semantic_errors(
            matlab_pass, source_map, conversion_manifest["items"][0], no_record["items"][0], schema
        )
    )


def test_retained_bytes_and_review_evidence_are_required(tmp_path: Path) -> None:
    source_map = _load_yaml(SOURCE_MAP_PATH)
    conversion_manifest = _load_yaml(CONVERSION_MANIFEST_PATH)
    coverage = _load_yaml(COVERAGE_PATH)
    schema = _load_json(CONVERSION_SCHEMA_PATH)
    repository_root, course_root, converted, record = _retained_converted_fixture(
        tmp_path, source_map, conversion_manifest, coverage
    )
    expected_identity = record["python_source_equivalence"]["cases"][0]["expected"]
    (course_root / expected_identity["path"]).write_text("not numeric\n", encoding="utf-8")
    retained_errors = _retained_coverage_errors(
        converted, source_map, conversion_manifest, schema, course_root, repository_root
    )
    assert "retained file identity mismatch" in " ".join(retained_errors)
    assert "numeric evidence" in " ".join(retained_errors)

    browser = copy.deepcopy(record)
    browser["claims"]["browser_visual_review"] = {
        "status": "passed",
        "summary": "Reviewed in a browser.",
        "evidence": [{"path": "evidence/missing.png", "sha256": "0" * 64}],
    }
    assert "retained file must exist exactly once" in " ".join(
        _record_semantic_errors(
            browser,
            source_map,
            conversion_manifest["items"][0],
            converted["items"][0],
            schema,
            course_root,
            repository_root,
        )
    )

    blocked = _blocked_coverage(coverage)
    assert "retained file must exist exactly once" in " ".join(
        _retained_coverage_errors(
            blocked, source_map, conversion_manifest, schema, course_root, repository_root
        )
    )


def test_blocked_item_stops_the_ordered_lane() -> None:
    source_map = _load_yaml(SOURCE_MAP_PATH)
    conversion_manifest = _load_yaml(CONVERSION_MANIFEST_PATH)
    schema = _load_json(CONVERSION_SCHEMA_PATH)
    blocked = _blocked_coverage(_load_yaml(COVERAGE_PATH))
    after = copy.deepcopy(blocked)
    second = after["items"][1]
    second.update(
        {
            "status": "converted",
            "conversion_record": f"{second['target_folder']}/conversion.yaml",
            "target_content_digest": "a" * 64,
        }
    )
    after["summary"].update({"pending": 82, "converted": 1})
    record = _valid_conversion_record(source_map, conversion_manifest, number=2)
    assert _transition_errors(
        blocked,
        after,
        source_map,
        conversion_manifest,
        schema,
        {second["conversion_record"]: record},
    )


def test_target_modules_exactly_match_retained_converted_prefix_without_placeholders() -> None:
    coverage = _load_yaml(COVERAGE_PATH)
    modules = COURSE_ROOT / "modules"
    expected = {
        COURSE_ROOT / item["target_folder"]
        for item in coverage["items"]
        if item["status"] == "converted"
    }
    actual = {path for path in modules.iterdir() if path.is_dir()} if modules.exists() else set()
    assert actual == expected
    for module in sorted(expected):
        for name in ("module.yaml", "lesson.md", "experiment.py", "conversion.yaml"):
            path = module / name
            assert path.is_file()
            assert path.read_text(encoding="utf-8").strip()
        assert not list(module.glob("*.m"))
        learner_text = "\n".join(
            (module / name).read_text(encoding="utf-8")
            for name in ("module.yaml", "lesson.md", "experiment.py")
        )
        assert re.search(r"\b(?:TODO|TBD)\b", learner_text, re.IGNORECASE) is None


def test_native_catalog_accepts_converted_dsp_prefix_without_regressing_examples() -> None:
    course = CourseManifest.model_validate(_load_yaml(COURSE_ROOT / "course.yaml"))
    assert course.id == "dsp-radar"
    assert course.modules_path == "modules"
    catalog = CourseCatalog([ROOT / "courses"])
    summaries = {item.id: item for item in catalog.summaries()}
    assert {"platform-showcase", "demo-radar", "dsp-radar"} <= set(summaries)
    converted = _load_yaml(COVERAGE_PATH)["summary"]["converted"]
    assert len(summaries["dsp-radar"].modules) == converted
    assert len(summaries["demo-radar"].modules) == 1
    assert len(summaries["platform-showcase"].modules) == 1
    assert all(
        module.interactive
        for course_id in ("demo-radar", "platform-showcase", "dsp-radar")
        for module in summaries[course_id].modules
    )
    runtime = ExperimentRuntime(catalog)
    for course_id, module_id in (
        ("demo-radar", "30-measure-range-from-echo-delay"),
        ("platform-showcase", "01-plotting-and-data-workbench"),
    ):
        first = runtime.run(course_id, module_id, {}).model_dump(mode="json")
        second = runtime.run(course_id, module_id, {}).model_dump(mode="json")
        assert _canonical(first) == _canonical(second)


def test_framework_loading_and_serialization_are_deterministic_and_read_only() -> None:
    before = _tree_snapshot(COURSE_ROOT)
    first = (
        _load_yaml(SOURCE_MAP_PATH),
        _load_yaml(CONVERSION_MANIFEST_PATH),
        _load_yaml(COVERAGE_PATH),
        _load_json(CONVERSION_SCHEMA_PATH),
    )
    second = (
        _load_yaml(SOURCE_MAP_PATH),
        _load_yaml(CONVERSION_MANIFEST_PATH),
        _load_yaml(COVERAGE_PATH),
        _load_json(CONVERSION_SCHEMA_PATH),
    )
    assert [_canonical(value) for value in first] == [_canonical(value) for value in second]
    assert _tree_snapshot(COURSE_ROOT) == before
    for path in (
        SOURCE_MAP_PATH,
        CONVERSION_MANIFEST_PATH,
        COVERAGE_PATH,
        CONVERSION_SCHEMA_PATH,
    ):
        raw = path.read_bytes()
        assert raw.endswith(b"\n")
        assert b"\r" not in raw


def test_exact_gitlink_and_gitmodules_identity() -> None:
    assert _sha256(ROOT / ".gitmodules") == EXPECTED_GITMODULES_SHA256
    gitmodules = (ROOT / ".gitmodules").read_text(encoding="utf-8")
    assert "url = https://github.com/kpbianco/dsp-radar_learning.git" in gitmodules
    assert 'submodule "courses/dsp-radar-learning"' in gitmodules

    staged: dict[str, str] = {}
    for line in _git("ls-files", "--stage", "--", "courses").stdout.splitlines():
        metadata, path = line.split("\t", 1)
        mode, object_id, _stage = metadata.split()
        if mode == "160000":
            staged[path] = object_id
    assert staged == EXPECTED_GITLINKS
    source_root = ROOT / "courses" / "dsp-radar-learning"
    if source_root.is_dir() and (source_root / ".git").exists():
        source_head = _git("rev-parse", "HEAD", cwd=source_root).stdout.strip()
        source_tree = _git("rev-parse", "HEAD^{tree}", cwd=source_root).stdout.strip()
        assert source_head == EXPECTED_SOURCE_COMMIT
        assert source_tree == EXPECTED_SOURCE_TREE


def _assert_source_checkout(source_root: Path, source_map: dict[str, Any]) -> None:
    assert _git("status", "--porcelain=v1", "--untracked-files=all", cwd=source_root).stdout == ""
    assert _git("rev-parse", "HEAD", cwd=source_root).stdout.strip() == EXPECTED_SOURCE_COMMIT
    assert _git("rev-parse", "HEAD^{tree}", cwd=source_root).stdout.strip() == EXPECTED_SOURCE_TREE
    symbolic = _git("symbolic-ref", "-q", "HEAD", cwd=source_root, check=False)
    assert symbolic.returncode != 0, "source-attested checkout must be detached"
    curriculum_path = source_root / "curriculum" / "modules.json"
    assert _sha256(curriculum_path) == EXPECTED_CURRICULUM_SHA256
    curriculum = json.loads(curriculum_path.read_text(encoding="utf-8"))
    modules = curriculum["modules"]
    assert curriculum["schema_version"] == 1
    assert curriculum["module_count"] == 84
    assert len(modules) == 84
    assert [item["number"] for item in modules] == list(range(1, 85))
    assert [item["id"] for item in modules] == [f"P{number:02d}" for number in range(1, 85)]
    assert all(item["status"] == "implemented" for item in modules)
    assert dict(Counter(item["phase"] for item in modules)) == EXPECTED_PHASE_COUNTS

    records: list[tuple[str, str]] = []
    for source_item, curriculum_item in zip(source_map["items"], modules, strict=True):
        for key, source_key in (
            ("id", "id"),
            ("number", "number"),
            ("source_folder", "folder"),
            ("title", "title"),
            ("guiding_question", "guiding_question"),
            ("phase", "phase"),
            ("phase_title", "phase_title"),
        ):
            assert source_item[key] == curriculum_item[source_key]
        assert [Path(item["path"]).name for item in source_item["files"]] == list(
            REQUIRED_SOURCE_FILES
        )
        for file_identity in source_item["files"]:
            relative = file_identity["path"]
            assert _normalized_relative(relative)
            path = source_root / relative
            assert path.is_file() and not path.is_symlink()
            digest = _sha256(path)
            assert digest == file_identity["sha256"]
            records.append((relative, digest))
    aggregate = "".join(f"{digest}  {relative}\n" for relative, digest in sorted(records)).encode()
    assert len(records) == 420
    assert hashlib.sha256(aggregate).hexdigest() == EXPECTED_FILE_SET_SHA256
    assert not list(source_root.rglob("__pycache__"))
    assert not list(source_root.rglob("*.py[co]"))
    assert not (source_root / ".learning").exists()


def test_optional_source_attestation_is_exact_clean_and_immutable() -> None:
    configured = os.getenv("ELP_DSP_SOURCE_ROOT")
    if configured is None:
        return
    source_root = Path(configured).resolve()
    assert source_root.is_dir(), f"ELP_DSP_SOURCE_ROOT is missing: {source_root}"
    git_dir_text = _git("rev-parse", "--absolute-git-dir", cwd=source_root).stdout.strip()
    git_dir = Path(git_dir_text)
    assert git_dir.is_dir()
    common_dir_text = _git("rev-parse", "--git-common-dir", cwd=source_root).stdout.strip()
    common_dir = Path(common_dir_text)
    if not common_dir.is_absolute():
        common_dir = (source_root / common_dir).resolve()
    assert common_dir.is_dir()
    source_before = _tree_snapshot(source_root)
    git_before = _tree_snapshot(git_dir)
    common_before = _tree_snapshot(common_dir) if common_dir != git_dir else None
    tree_before = _git("ls-tree", "-rz", "--full-tree", "HEAD", cwd=source_root).stdout
    status_before = _git(
        "status", "--porcelain=v1", "--untracked-files=all", cwd=source_root
    ).stdout
    try:
        _assert_source_checkout(source_root, _load_yaml(SOURCE_MAP_PATH))
    finally:
        assert _tree_snapshot(source_root) == source_before
        assert _tree_snapshot(git_dir) == git_before
        if common_before is not None:
            assert _tree_snapshot(common_dir) == common_before
        assert _git("ls-tree", "-rz", "--full-tree", "HEAD", cwd=source_root).stdout == tree_before
        assert (
            _git("status", "--porcelain=v1", "--untracked-files=all", cwd=source_root).stdout
            == status_before
        )
