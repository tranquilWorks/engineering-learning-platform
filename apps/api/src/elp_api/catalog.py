from __future__ import annotations

import hashlib
import re
import threading
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Any, TypeVar

import yaml
from pydantic import BaseModel, ValidationError

from . import __version__
from .models import (
    ContentRevision,
    CourseManifest,
    CourseSummary,
    ModuleDocument,
    ModuleManifest,
    ModuleSummary,
    PlatformRevision,
)


class CatalogError(RuntimeError):
    pass


class _UniqueKeyLoader(yaml.SafeLoader):
    pass


def _construct_unique_mapping(
    loader: _UniqueKeyLoader, node: yaml.MappingNode, deep: bool = False
) -> dict[Any, Any]:
    result: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        try:
            duplicate = key in result
        except TypeError as exc:
            raise yaml.constructor.ConstructorError(
                "while constructing a mapping",
                node.start_mark,
                "found unhashable key",
                key_node.start_mark,
            ) from exc
        if duplicate:
            raise yaml.constructor.ConstructorError(
                "while constructing a mapping",
                node.start_mark,
                f"found duplicate key {key!r}",
                key_node.start_mark,
            )
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


_UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    _construct_unique_mapping,
)


def _sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _framed_digest(files: Iterable[tuple[str, bytes]]) -> str:
    digest = hashlib.sha256(b"engineering-learning-platform-content-v1\0")
    for name, value in sorted(files):
        encoded_name = name.encode("utf-8")
        digest.update(len(encoded_name).to_bytes(8, "big"))
        digest.update(encoded_name)
        digest.update(len(value).to_bytes(8, "big"))
        digest.update(value)
    return digest.hexdigest()


def _read_ref(git_dir: Path, common_dir: Path, ref: str) -> str | None:
    for root in (git_dir, common_dir):
        candidate = root / ref
        if candidate.is_file():
            value = candidate.read_text(encoding="ascii").strip()
            if re.fullmatch(r"[0-9a-f]{40}(?:[0-9a-f]{24})?", value):
                return value
    for root in (git_dir, common_dir):
        packed = root / "packed-refs"
        if not packed.is_file():
            continue
        for line in packed.read_text(encoding="ascii").splitlines():
            if not line or line.startswith(("#", "^")):
                continue
            value, separator, name = line.partition(" ")
            if separator and name == ref and re.fullmatch(r"[0-9a-f]{40}(?:[0-9a-f]{24})?", value):
                return value
    return None


def git_commit_for(path: Path) -> str | None:
    """Resolve a containing Git HEAD without invoking a command or writing the source."""
    start = path.resolve()
    for root in (start, *start.parents):
        marker = root / ".git"
        if marker.is_dir():
            git_dir = marker
        elif marker.is_file():
            first = marker.read_text(encoding="utf-8").strip()
            prefix = "gitdir: "
            if not first.startswith(prefix):
                return None
            raw = Path(first[len(prefix) :])
            git_dir = raw if raw.is_absolute() else (root / raw).resolve()
        else:
            continue
        common_dir = git_dir
        common_marker = git_dir / "commondir"
        if common_marker.is_file():
            raw = Path(common_marker.read_text(encoding="utf-8").strip())
            common_dir = raw if raw.is_absolute() else (git_dir / raw).resolve()
        head_path = git_dir / "HEAD"
        if not head_path.is_file():
            return None
        head = head_path.read_text(encoding="ascii").strip()
        if re.fullmatch(r"[0-9a-f]{40}(?:[0-9a-f]{24})?", head):
            return head
        prefix = "ref: "
        return (
            _read_ref(git_dir, common_dir, head[len(prefix) :]) if head.startswith(prefix) else None
        )
    return None


def platform_revision(runtime_kind: str) -> PlatformRevision:
    repository = Path(__file__).resolve().parents[4]
    package = Path(__file__).resolve().parent
    runtime_files = [(path.name, path.read_bytes()) for path in sorted(package.glob("*.py"))]
    return PlatformRevision(
        platform_version=__version__,
        platform_git_commit=git_commit_for(repository),
        runtime_content_digest=_framed_digest(runtime_files),
        runtime_kind=("python-in-process" if runtime_kind == "python" else "static"),
    )


@dataclass(frozen=True)
class ModuleRecord:
    manifest: ModuleManifest
    path: Path
    revision: ContentRevision
    markdown_sources: tuple[tuple[str, str], ...]
    input_hashes: tuple[tuple[str, str], ...]

    def assert_unchanged(self) -> None:
        for relative, expected in self.input_hashes:
            candidate = self.path / relative
            try:
                actual = _sha256_file(candidate)
            except OSError as exc:
                raise CatalogError(
                    f"{candidate}: accepted module input is unavailable; reload required"
                ) from exc
            if actual != expected:
                raise CatalogError(f"{candidate}: accepted module input changed; reload required")


@dataclass(frozen=True)
class CourseRecord:
    manifest: CourseManifest
    path: Path
    modules: tuple[ModuleRecord, ...]
    revision: ContentRevision

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
                    interactive=item.manifest.runtime.kind != "static"
                    or bool(item.manifest.controls),
                    revision=item.revision,
                )
                for item in self.modules
            ],
            revision=self.revision,
        )


ModelT = TypeVar("ModelT", bound=BaseModel)


class CourseCatalog:
    def __init__(self, roots: Iterable[Path]) -> None:
        self.roots = tuple(Path(path).resolve() for path in roots)
        self._lock = threading.RLock()
        self._courses: dict[str, CourseRecord] = {}
        self.reload()

    @staticmethod
    def _read_yaml(path: Path) -> tuple[dict[str, Any], bytes]:
        try:
            raw = path.read_bytes()
            value = yaml.load(raw.decode("utf-8"), Loader=_UniqueKeyLoader)
        except (OSError, UnicodeError, yaml.YAMLError) as exc:
            raise CatalogError(f"{path}: cannot read YAML: {exc}") from exc
        if not isinstance(value, dict):
            raise CatalogError(f"{path}: expected a YAML mapping")
        return value, raw

    @staticmethod
    def _validate_manifest(path: Path, raw: dict[str, Any], model: type[ModelT]) -> ModelT:
        try:
            return model.model_validate(raw)
        except ValidationError as exc:
            version = raw.get("schema_version", "<missing>")
            details: list[str] = []
            for error in exc.errors(include_url=False, include_context=False):
                location = ".".join(str(item) for item in error["loc"]) or "manifest"
                message = str(error["msg"]).removeprefix("Value error, ")
                details.append(f"{location}: {message}")
            raise CatalogError(
                f"{path}: invalid {model.__name__} schema_version={version!r}: "
                + "; ".join(details)
            ) from exc

    @staticmethod
    def _contained_file(root: Path, relative: str, purpose: str) -> Path:
        raw = Path(relative)
        if raw.is_absolute() or any(part in {"", ".", ".."} for part in raw.parts):
            raise CatalogError(f"{purpose} must be a normalized relative path: {relative!r}")
        candidate = (root / raw).resolve()
        resolved_root = root.resolve()
        if resolved_root not in candidate.parents or not candidate.is_file():
            raise CatalogError(f"{purpose} escapes or is missing: {relative!r}")
        return candidate

    def _module_record(self, manifest_path: Path) -> ModuleRecord:
        raw, manifest_bytes = self._read_yaml(manifest_path)
        manifest = self._validate_manifest(manifest_path, raw, ModuleManifest)
        module_dir = manifest_path.parent.resolve()
        content_files: list[tuple[str, bytes]] = [("module.yaml", manifest_bytes)]
        markdown_sources: dict[str, str] = {}
        for block in manifest.blocks:
            if block.type != "markdown" or block.source is None:
                continue
            if block.source in markdown_sources:
                continue
            source = self._contained_file(module_dir, block.source, "markdown source")
            try:
                source_bytes = source.read_bytes()
                markdown_sources[block.source] = source_bytes.decode("utf-8")
            except (OSError, UnicodeError) as exc:
                raise CatalogError(f"{source}: cannot read markdown source: {exc}") from exc
            content_files.append((block.source, source_bytes))
        if manifest.runtime.kind == "python":
            relative, separator, function_name = manifest.runtime.entrypoint.partition(":")
            if not separator or not relative.endswith(".py") or not function_name.isidentifier():
                raise CatalogError(
                    f"{manifest_path}: runtime entrypoint must look like experiment.py:run"
                )
            entrypoint = self._contained_file(module_dir, relative, "runtime entrypoint")
            content_files.append((relative, entrypoint.read_bytes()))
        input_hashes = tuple(
            (relative, hashlib.sha256(value).hexdigest())
            for relative, value in sorted(content_files)
        )
        return ModuleRecord(
            manifest=manifest,
            path=module_dir,
            revision=ContentRevision(
                content_digest=_framed_digest(content_files),
                source_git_commit=git_commit_for(module_dir),
            ),
            markdown_sources=tuple(sorted(markdown_sources.items())),
            input_hashes=input_hashes,
        )

    def reload(self) -> None:
        discovered: dict[str, CourseRecord] = {}
        for root in self.roots:
            if not root.exists():
                continue
            single_course = (root / "course.yaml").is_file()
            candidates = (
                [root / "course.yaml"] if single_course else sorted(root.glob("*/course.yaml"))
            )
            for manifest_path in candidates:
                course_dir = manifest_path.parent.resolve()
                if not single_course and root not in course_dir.parents:
                    raise CatalogError(f"{manifest_path}: course directory escapes collection root")
                if course_dir.name.startswith("_"):
                    continue
                raw, course_bytes = self._read_yaml(manifest_path)
                manifest = self._validate_manifest(manifest_path, raw, CourseManifest)
                if manifest.id.startswith("_"):
                    continue
                modules_dir = (course_dir / manifest.modules_path).resolve()
                if course_dir not in modules_dir.parents:
                    raise CatalogError(
                        f"{manifest_path}: modules_path escapes course directory: "
                        f"{manifest.modules_path!r}"
                    )
                modules: list[ModuleRecord] = []
                if modules_dir.is_dir():
                    for module_path in sorted(modules_dir.glob("*/module.yaml")):
                        module_dir = module_path.parent.resolve()
                        if modules_dir not in module_dir.parents:
                            raise CatalogError(
                                f"{module_path}: module directory escapes modules_path"
                            )
                        modules.append(self._module_record(module_path))
                ids = [item.manifest.id for item in modules]
                duplicate_ids = sorted({item for item in ids if ids.count(item) > 1})
                if duplicate_ids:
                    raise CatalogError(f"{manifest_path}: duplicate module ids: {duplicate_ids}")
                numbers = [
                    item.manifest.number for item in modules if item.manifest.number is not None
                ]
                duplicate_numbers = sorted({item for item in numbers if numbers.count(item) > 1})
                if duplicate_numbers:
                    raise CatalogError(
                        f"{manifest_path}: duplicate module numbers: {duplicate_numbers}"
                    )
                modules.sort(
                    key=lambda item: (
                        item.manifest.number is None,
                        item.manifest.number or 0,
                        item.manifest.id,
                    )
                )
                if manifest.id in discovered:
                    raise CatalogError(f"{manifest_path}: duplicate course id {manifest.id!r}")
                course_digest_inputs = [("course.yaml", course_bytes)]
                course_digest_inputs.extend(
                    (
                        f"modules/{module.manifest.id}.content-digest",
                        module.revision.content_digest.encode("ascii"),
                    )
                    for module in modules
                )
                discovered[manifest.id] = CourseRecord(
                    manifest=manifest,
                    path=course_dir,
                    modules=tuple(modules),
                    revision=ContentRevision(
                        content_digest=_framed_digest(course_digest_inputs),
                        source_git_commit=git_commit_for(course_dir),
                    ),
                )
        with self._lock:
            previous = self._courses
            self._courses = discovered
            try:
                self._validate_output_references()
            except BaseException:
                self._courses = previous
                raise

    def _validate_output_references(self) -> None:
        from .runtime import ExperimentRuntime, RuntimeErrorBase

        runtime = ExperimentRuntime(self)
        for course in self._courses.values():
            for module in course.modules:
                references = [
                    block
                    for block in module.manifest.blocks
                    if block.type in {"plot", "plot_grid", "table"}
                    or (block.type == "callout" and block.source is not None)
                ]
                identity = f"{course.manifest.id}/{module.manifest.id}"
                if module.manifest.runtime.kind == "static":
                    if references:
                        raise CatalogError(
                            f"{identity}: static module cannot reference runtime outputs"
                        )
                    continue
                try:
                    runtime.run(course.manifest.id, module.manifest.id, {})
                except RuntimeErrorBase as exc:
                    raise CatalogError(
                        f"{identity}: default runtime validation failed: {exc}"
                    ) from exc

    def summaries(self) -> list[CourseSummary]:
        with self._lock:
            values = [course.summary() for course in self._courses.values()]
            values.sort(key=lambda item: (item.order, item.title.lower()))
            return values

    def course(self, course_id: str) -> CourseRecord:
        with self._lock:
            try:
                return self._courses[course_id]
            except KeyError as exc:
                raise KeyError(f"unknown course {course_id!r}") from exc

    def module_record(self, course_id: str, module_id: str) -> tuple[CourseRecord, ModuleRecord]:
        with self._lock:
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
        defaults = {control.id: control.default for control in module.manifest.controls}
        return ModuleDocument(
            course=course.summary(),
            module=module.manifest,
            markdown_sources=dict(module.markdown_sources),
            default_parameters=defaults,
            module_revision=module.revision,
            platform_revision=platform_revision(module.manifest.runtime.kind),
        )

    @staticmethod
    def validate_result_references(course_id: str, module: ModuleRecord, result: Any) -> None:
        identity = f"{course_id}/{module.manifest.id}"
        for block in module.manifest.blocks:
            if block.type == "plot" and block.plot not in result.plots:
                raise CatalogError(f"{identity}: block references missing plot {block.plot!r}")
            if block.type == "plot_grid":
                missing = sorted(set(block.plots) - set(result.plots))
                if missing:
                    raise CatalogError(f"{identity}: block references missing plots {missing}")
            if block.type == "table" and block.table not in result.tables:
                raise CatalogError(f"{identity}: block references missing table {block.table!r}")
            if (
                block.type == "callout"
                and block.source is not None
                and block.source not in result.explanations
            ):
                raise CatalogError(
                    f"{identity}: block references missing explanation {block.source!r}"
                )
