#!/usr/bin/env python3
"""Generate portable JSON Schemas from the executable Pydantic contracts."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "apps" / "api" / "src"))

from elp_api.models import CourseManifest, ModuleManifest  # noqa: E402

TARGETS = {
    ROOT / "packages" / "lesson-schema" / "course.schema.json": CourseManifest,
    ROOT / "packages" / "lesson-schema" / "module.schema.json": ModuleManifest,
}


def rendered(model: type) -> str:
    value = model.model_json_schema(mode="validation")
    value["$schema"] = "https://json-schema.org/draft/2020-12/schema"
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    drift: list[str] = []
    for path, model in TARGETS.items():
        expected = rendered(model)
        if args.check:
            if not path.is_file() or path.read_text(encoding="utf-8") != expected:
                drift.append(str(path.relative_to(ROOT)))
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(expected, encoding="utf-8")
    if drift:
        print("schema drift: " + ", ".join(drift), file=sys.stderr)
        return 1
    if not args.check:
        print("generated " + ", ".join(str(path.relative_to(ROOT)) for path in TARGETS))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
