from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


def _split_paths(value: str) -> tuple[Path, ...]:
    paths: list[Path] = []
    for item in value.split(os.pathsep):
        item = item.strip()
        if item:
            paths.append(Path(item).expanduser().resolve())
    return tuple(paths)


@dataclass(frozen=True)
class Settings:
    course_paths: tuple[Path, ...]
    web_dist: Path | None
    dev_cors: tuple[str, ...]
    max_result_bytes: int
    runtime_timeout_seconds: float

    @classmethod
    def from_env(cls) -> "Settings":
        course_value = os.getenv("ELP_COURSE_PATHS", "./courses")
        web_value = os.getenv("ELP_WEB_DIST")
        cors_value = os.getenv("ELP_DEV_CORS", "http://localhost:5173")
        return cls(
            course_paths=_split_paths(course_value),
            web_dist=Path(web_value).expanduser().resolve() if web_value else None,
            dev_cors=tuple(item.strip() for item in cors_value.split(",") if item.strip()),
            max_result_bytes=int(os.getenv("ELP_MAX_RESULT_BYTES", str(8 * 1024 * 1024))),
            runtime_timeout_seconds=float(os.getenv("ELP_RUNTIME_TIMEOUT_SECONDS", "5")),
        )
