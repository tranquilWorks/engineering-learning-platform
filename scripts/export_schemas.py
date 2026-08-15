#!/usr/bin/env python3
"""Generate every JSON Schema and TypeScript derivative from Pydantic models."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

from pydantic import TypeAdapter
from pydantic.json_schema import models_json_schema

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "apps" / "api" / "src"))

from elp_api.models import (
    ControlSpec,
    CourseManifest,
    CourseSummary,
    LessonBlock,
    ModuleDocument,
    ModuleManifest,
    RunRequest,
    RunResult,
    RuntimeSpec,
)

JSON_MODELS = {
    ROOT / "packages" / "lesson-schema" / "course.schema.json": CourseManifest,
    ROOT / "packages" / "lesson-schema" / "module.schema.json": ModuleManifest,
}
API_MODELS = (CourseSummary, ModuleDocument, RunRequest, RunResult)
TYPESCRIPT_TARGETS: dict[str, Any] = {
    "ControlSpec": TypeAdapter(ControlSpec),
    "CourseSummary": CourseSummary,
    "LessonBlock": TypeAdapter(LessonBlock),
    "ModuleDocument": ModuleDocument,
    "RunRequest": RunRequest,
    "RunResult": RunResult,
    "RuntimeSpec": TypeAdapter(RuntimeSpec),
}
API_SCHEMA_PATH = ROOT / "packages" / "lesson-schema" / "api.schema.json"
TYPESCRIPT_PATH = ROOT / "apps" / "web" / "src" / "types.ts"


def _json(value: Any) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def rendered_model(model: type) -> str:
    value = model.model_json_schema(mode="validation")
    value["$schema"] = "https://json-schema.org/draft/2020-12/schema"
    return _json(value)


def rendered_api_schema() -> str:
    _, value = models_json_schema(
        [(model, "serialization") for model in API_MODELS],
        title="Engineering Learning Platform API contract",
    )
    value["$schema"] = "https://json-schema.org/draft/2020-12/schema"
    return _json(value)


def _schema_for(target: Any) -> dict[str, Any]:
    if isinstance(target, TypeAdapter):
        return target.json_schema(mode="serialization")
    return target.model_json_schema(mode="serialization")


def _literal(value: Any) -> str:
    if value is None:
        return "null"
    if value is True:
        return "true"
    if value is False:
        return "false"
    return json.dumps(value, ensure_ascii=False)


def _property_name(value: str) -> str:
    return (
        value if re.fullmatch(r"[A-Za-z_$][A-Za-z0-9_$]*", value) else json.dumps(value)
    )


def _type_expression(schema: dict[str, Any]) -> str:
    if not schema:
        return "unknown"
    if "$ref" in schema:
        return schema["$ref"].rsplit("/", 1)[-1]
    if "const" in schema:
        return _literal(schema["const"])
    if "enum" in schema:
        return " | ".join(_literal(value) for value in schema["enum"])
    for keyword in ("oneOf", "anyOf"):
        if keyword in schema:
            values = list(
                dict.fromkeys(_type_expression(item) for item in schema[keyword])
            )
            return " | ".join(values)
    schema_type = schema.get("type")
    if isinstance(schema_type, list):
        return " | ".join(_type_expression({"type": item}) for item in schema_type)
    if schema_type == "string":
        return "string"
    if schema_type in {"integer", "number"}:
        return "number"
    if schema_type == "boolean":
        return "boolean"
    if schema_type == "null":
        return "null"
    if schema_type == "array":
        return f"Array<{_type_expression(schema.get('items', {}))}>"
    if schema_type == "object" or any(
        key in schema
        for key in ("properties", "additionalProperties", "patternProperties")
    ):
        properties = schema.get("properties", {})
        if properties:
            required = set(schema.get("required", []))
            fields = [
                f"{_property_name(name)}{' ' if name in required else '?'}: "
                f"{_type_expression(value)};"
                for name, value in properties.items()
            ]
            return "{ " + " ".join(fields) + " }"
        patterns = schema.get("patternProperties", {})
        if patterns:
            values = {_type_expression(value) for value in patterns.values()}
            return f"Record<string, {' | '.join(sorted(values))}>"
        additional = schema.get("additionalProperties")
        if additional is True:
            return "Record<string, unknown>"
        if isinstance(additional, dict):
            return f"Record<string, {_type_expression(additional)}>"
        return "Record<string, never>"
    raise ValueError(f"unsupported JSON Schema node for TypeScript: {schema!r}")


def _render_named(name: str, schema: dict[str, Any]) -> str:
    if schema.get("type") == "object" and schema.get("properties"):
        required = set(schema.get("required", []))
        lines = [f"export interface {name} {{"]
        for field_name, field_schema in schema["properties"].items():
            optional = "" if field_name in required else "?"
            lines.append(
                f"  {_property_name(field_name)}{optional}: {_type_expression(field_schema)};"
            )
        lines.append("}")
        return "\n".join(lines)
    return f"export type {name} = {_type_expression(schema)};"


def rendered_typescript() -> str:
    named: dict[str, dict[str, Any]] = {}
    roots: dict[str, dict[str, Any]] = {}
    for name, target in TYPESCRIPT_TARGETS.items():
        schema = _schema_for(target)
        for definition_name, definition in schema.pop("$defs", {}).items():
            existing = named.get(definition_name)
            if existing is not None and existing != definition:
                raise ValueError(f"conflicting schema definition {definition_name}")
            named[definition_name] = definition
        roots[name] = schema
    named.update(roots)
    sections = [
        "// Generated by scripts/export_schemas.py from elp_api.models; do not edit.",
        "// These types describe serialized API values and have no independent compatibility policy.",
        "",
    ]
    for name in sorted(named):
        sections.append(_render_named(name, named[name]))
        sections.append("")
    return "\n".join(sections)


def rendered_targets() -> dict[Path, str]:
    targets = {path: rendered_model(model) for path, model in JSON_MODELS.items()}
    targets[API_SCHEMA_PATH] = rendered_api_schema()
    targets[TYPESCRIPT_PATH] = rendered_typescript()
    return targets


def drifted_paths(targets: dict[Path, str]) -> list[Path]:
    return [
        path
        for path, expected in targets.items()
        if not path.is_file() or path.read_text(encoding="utf-8") != expected
    ]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    targets = rendered_targets()
    drift = drifted_paths(targets) if args.check else []
    if not args.check:
        for path, expected in targets.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(expected, encoding="utf-8")
    if drift:
        print(
            "generated contract drift: "
            + ", ".join(str(path.relative_to(ROOT)) for path in drift),
            file=sys.stderr,
        )
        return 1
    if not args.check:
        print("generated " + ", ".join(str(path.relative_to(ROOT)) for path in targets))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
