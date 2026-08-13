from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import yaml

from .models import (
    CourseManifest,
    CourseSummary,
    ModuleDocument,
    ModuleManifest,
    ModuleSummary,
)


class CatalogError(RuntimeError):
    pass


@dataclass(frozen=True)
class ModuleRecord:
    manifest: ModuleManifest
    path: Path


@dataclass(frozen=True)
class CourseRecord:
    manifest: CourseManifest
    path: Path
    modules: tuple[ModuleRecord, ...]

    def summary(self) -> CourseSummary:
        return CourseSummary(
            id=self.manifest.id,
            title=self.manifest.title,
            description=self.manifest.description,
            order=self.manifest.order,
            tags=self.manifest.tags,
            modules=[
                ModuleSummary(
                    id=item.manifest.id,
                    number=item.manifest.number,
                    title=item.manifest.title,
                    summary=item.manifest.summary,
                    status=item.manifest.status,
                    interactive=item.manifest.runtime.kind != "static" or bool(item.manifest.controls),
                )
                for item in self.modules
            ],
        )


class CourseCatalog:
    def __init__(self, roots: Iterable[Path]) -> None:
        self.roots = tuple(Path(path).resolve() for path in roots)
        self._courses: dict[str, CourseRecord] = {}
        self.reload()

    @staticmethod
    def _read_yaml(path: Path) -> dict:
        try:
            value = yaml.safe_load(path.read_text(encoding="utf-8"))
        except (OSError, yaml.YAMLError) as exc:
            raise CatalogError(f"cannot read {path}: {exc}") from exc
        if not isinstance(value, dict):
            raise CatalogError(f"{path} must contain a YAML mapping")
        return value

    def reload(self) -> None:
        discovered: dict[str, CourseRecord] = {}
        for root in self.roots:
            if not root.exists():
                continue
            candidates = [root / "course.yaml"] if (root / "course.yaml").is_file() else sorted(root.glob("*/course.yaml"))
            for manifest_path in candidates:
                course_dir = manifest_path.parent
                if course_dir.name.startswith("_"):
                    continue
                manifest = CourseManifest.model_validate(self._read_yaml(manifest_path))
                if manifest.id.startswith("_"):
                    continue
                modules_dir = course_dir / manifest.modules_path
                modules: list[ModuleRecord] = []
                if modules_dir.is_dir():
                    for module_path in sorted(modules_dir.glob("*/module.yaml")):
                        module = ModuleManifest.model_validate(self._read_yaml(module_path))
                        modules.append(ModuleRecord(module, module_path.parent))
                modules.sort(key=lambda item: (item.manifest.number is None, item.manifest.number or 0, item.manifest.id))
                if manifest.id in discovered:
                    raise CatalogError(f"duplicate course id {manifest.id!r}")
                discovered[manifest.id] = CourseRecord(manifest, course_dir, tuple(modules))
        self._courses = discovered

    def summaries(self) -> list[CourseSummary]:
        values = [course.summary() for course in self._courses.values()]
        values.sort(key=lambda item: (item.order, item.title.lower()))
        return values

    def course(self, course_id: str) -> CourseRecord:
        try:
            return self._courses[course_id]
        except KeyError as exc:
            raise KeyError(f"unknown course {course_id!r}") from exc

    def module_record(self, course_id: str, module_id: str) -> tuple[CourseRecord, ModuleRecord]:
        course = self.course(course_id)
        for module in course.modules:
            if module.manifest.id == module_id:
                return course, module
        raise KeyError(f"unknown module {course_id}/{module_id}")


    @staticmethod
    def _safe_asset(root: Path, relative: str) -> Path:
        candidate = (root / relative).resolve()
        resolved_root = root.resolve()
        if resolved_root not in candidate.parents or not candidate.is_file():
            raise KeyError(f"unknown asset {relative!r}")
        if any(part.startswith(".") for part in Path(relative).parts):
            raise KeyError(f"unknown asset {relative!r}")
        return candidate

    def course_asset(self, course_id: str, relative: str) -> Path:
        course = self.course(course_id)
        return self._safe_asset(course.path / "assets", relative)

    def module_asset(self, course_id: str, module_id: str, relative: str) -> Path:
        _, module = self.module_record(course_id, module_id)
        return self._safe_asset(module.path / "assets", relative)

    def document(self, course_id: str, module_id: str) -> ModuleDocument:
        course, module = self.module_record(course_id, module_id)
        sources: dict[str, str] = {}
        for block in module.manifest.blocks:
            if block.type == "markdown" and block.source and block.source not in sources:
                source = (module.path / block.source).resolve()
                if module.path.resolve() not in source.parents:
                    raise CatalogError(f"module source escapes directory: {block.source}")
                sources[block.source] = source.read_text(encoding="utf-8")
        defaults = {control.id: control.default for control in module.manifest.controls}
        return ModuleDocument(
            course=course.summary(),
            module=module.manifest,
            markdown_sources=sources,
            default_parameters=defaults,
        )
