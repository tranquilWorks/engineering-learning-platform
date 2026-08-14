#!/usr/bin/env python3
"""Validate course identity, lesson references, runtime outputs, and determinism."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "apps" / "api" / "src"))

from elp_api.catalog import CourseCatalog
from elp_api.runtime import ExperimentRuntime


def stable_digest(value: Any) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()
    return hashlib.sha256(encoded).hexdigest()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--execute", action="store_true", help="execute each Python module with defaults")
    parser.add_argument("--deterministic", action="store_true", help="execute each Python module twice and compare")
    parser.add_argument("--json", action="store_true", dest="as_json")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    roots = tuple(Path(item).resolve() for item in os.getenv("ELP_COURSE_PATHS", str(ROOT / "courses")).split(os.pathsep) if item)
    catalog = CourseCatalog(roots)
    runtime = ExperimentRuntime(catalog)
    errors: list[str] = []
    course_count = 0
    module_count = 0
    interactive_count = 0

    for course in catalog.summaries():
        course_count += 1
        seen_numbers: set[int] = set()
        seen_ids: set[str] = set()
        for summary in course.modules:
            module_count += 1
            if summary.id in seen_ids:
                errors.append(f"{course.id}: duplicate module id {summary.id}")
            seen_ids.add(summary.id)
            if summary.number is not None:
                if summary.number in seen_numbers:
                    errors.append(f"{course.id}: duplicate module number {summary.number}")
                seen_numbers.add(summary.number)
            document = catalog.document(course.id, summary.id)
            manifest = document.module
            control_ids = [control.id for control in manifest.controls]
            if len(control_ids) != len(set(control_ids)):
                errors.append(f"{course.id}/{summary.id}: duplicate control ids")
            for block in manifest.blocks:
                if block.type == "widget":
                    if block.widget != "parameter-map":
                        errors.append(f"{course.id}/{summary.id}: unknown widget {block.widget!r}")
                    else:
                        numeric = {
                            control.id
                            for control in manifest.controls
                            if control.type in {"slider", "number"}
                        }
                        for axis in ("x_control", "y_control"):
                            target = block.props.get(axis)
                            if target not in numeric:
                                errors.append(
                                    f"{course.id}/{summary.id}: parameter-map {axis} must reference a numeric control"
                                )

            if manifest.runtime.kind == "python":
                interactive_count += 1
                if args.execute or args.deterministic:
                    first = runtime.run(course.id, summary.id, {}).model_dump(mode="json")
                    for block in manifest.blocks:
                        if block.plot and block.plot not in first["plots"]:
                            errors.append(f"{course.id}/{summary.id}: block references missing plot {block.plot}")
                        for plot in block.plots:
                            if plot not in first["plots"]:
                                errors.append(f"{course.id}/{summary.id}: block references missing plot {plot}")
                        if block.table and block.table not in first["tables"]:
                            errors.append(f"{course.id}/{summary.id}: block references missing table {block.table}")
                    if args.deterministic:
                        second = runtime.run(course.id, summary.id, {}).model_dump(mode="json")
                        if stable_digest(first) != stable_digest(second):
                            errors.append(f"{course.id}/{summary.id}: default execution is not deterministic")

    if not course_count:
        errors.append("no courses discovered")
    report = {
        "schema_version": 1,
        "course_roots": [str(path) for path in roots],
        "courses": course_count,
        "modules": module_count,
        "interactive_modules": interactive_count,
        "executed": bool(args.execute or args.deterministic),
        "determinism_checked": bool(args.deterministic),
        "errors": errors,
        "status": "pass" if not errors else "fail",
    }
    if args.as_json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(f"courses={course_count} modules={module_count} interactive={interactive_count}")
        for error in errors:
            print(f"ERROR: {error}")
        print(report["status"].upper())
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
