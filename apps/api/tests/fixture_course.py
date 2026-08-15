from __future__ import annotations

import hashlib
import os
from pathlib import Path
from typing import Any

import yaml

VALID_EXPERIMENT = """def run(parameters):
    return {
        "metrics": [{"id": "value", "label": "Value", "value": 1}],
        "plots": {
            "main": {
                "data": [{"type": "scatter", "x": [0, 1], "y": [0, 1]}],
                "layout": {"xaxis": {"title": "Input (s)"}, "yaxis": {"title": "Value (m)"}},
            }
        },
        "tables": {"cases": {"columns": ["case"], "rows": [{"case": "A"}]}},
        "explanations": {"interpretation": "Free-form explanation."},
        "diagnostics": {"plotly": {"nested": [1, {"arbitrary": True}]}},
    }
"""


def course_manifest(**overrides: Any) -> dict[str, Any]:
    value: dict[str, Any] = {
        "schema_version": 1,
        "id": "sample-course",
        "title": "Sample Course",
        "description": "Synthetic contract fixture.",
        "modules_path": "modules",
    }
    value.update(overrides)
    return value


def module_manifest(**overrides: Any) -> dict[str, Any]:
    value: dict[str, Any] = {
        "schema_version": 1,
        "id": "sample-module",
        "number": 1,
        "title": "Sample Module",
        "status": "static",
        "runtime": {"kind": "static"},
        "blocks": [{"type": "markdown", "text": "# Explicit Markdown\n\nAny body is valid."}],
    }
    value.update(overrides)
    return value


def write_course(
    root: Path,
    *,
    course: dict[str, Any] | None = None,
    modules: list[dict[str, Any]] | None = None,
    experiment: str | None = None,
    lesson: str | None = None,
) -> Path:
    course_dir = root / "sample-course"
    module_values = modules or [module_manifest()]
    (course_dir / "modules").mkdir(parents=True)
    (course_dir / "course.yaml").write_text(
        yaml.safe_dump(course or course_manifest(), sort_keys=False),
        encoding="utf-8",
    )
    for index, module in enumerate(module_values):
        module_dir = course_dir / "modules" / f"{index + 1:02d}-{module['id']}"
        module_dir.mkdir()
        (module_dir / "module.yaml").write_text(
            yaml.safe_dump(module, sort_keys=False), encoding="utf-8"
        )
        if experiment is not None:
            (module_dir / "experiment.py").write_text(experiment, encoding="utf-8")
        if lesson is not None:
            (module_dir / "lesson.md").write_text(lesson, encoding="utf-8")
    return course_dir


def tree_snapshot(root: Path) -> tuple[tuple[str, int, str], ...]:
    values: list[tuple[str, int, str]] = []
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root).as_posix()
        mode = path.stat().st_mode & 0o777
        digest = hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else "dir"
        values.append((relative, mode, digest))
    return tuple(values)


def make_read_only(root: Path) -> None:
    for path in sorted(root.rglob("*"), reverse=True):
        path.chmod(0o444 if path.is_file() else 0o555)
    root.chmod(0o555)


def make_writable(root: Path) -> None:
    root.chmod(0o755)
    for path in root.rglob("*"):
        path.chmod(0o644 if path.is_file() else 0o755)


def run_git(repository: Path, *args: str) -> str:
    import subprocess

    environment = os.environ | {
        "GIT_AUTHOR_NAME": "ELP Test",
        "GIT_AUTHOR_EMAIL": "elp-test@example.invalid",
        "GIT_COMMITTER_NAME": "ELP Test",
        "GIT_COMMITTER_EMAIL": "elp-test@example.invalid",
    }
    completed = subprocess.run(
        ["git", *args],
        cwd=repository,
        env=environment,
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()
