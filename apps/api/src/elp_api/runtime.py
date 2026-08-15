from __future__ import annotations

import importlib.util
import inspect
import json
import math
import sys
import threading
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import TimeoutError as FutureTimeout
from pathlib import Path
from types import ModuleType
from typing import Any

from pydantic import ValidationError

from .catalog import CatalogError, CourseCatalog, ModuleRecord, platform_revision
from .models import RunResult
from .serialization import jsonable


class RuntimeErrorBase(RuntimeError):
    pass


class RuntimeTimeout(RuntimeErrorBase):
    pass


class RuntimeContractError(RuntimeErrorBase):
    pass


class ExperimentRuntime:
    """Execute trusted course entrypoints with a bounded response wait.

    Python threads cannot forcibly terminate hostile or deadlocked code. This runtime is
    therefore only for reviewed, repository-controlled course code. A timed-out task is
    detached so the request can return, but the container/process must be recycled if the
    trusted experiment does not stop itself. Hardened subprocess/container workers are a
    separate roadmap milestone.
    """

    def __init__(self, catalog: CourseCatalog, default_timeout: float = 5.0) -> None:
        self.catalog = catalog
        self.default_timeout = default_timeout
        self._modules: dict[tuple[Path, str], ModuleType] = {}
        self._lock = threading.Lock()

    def _load_callable(
        self, record: ModuleRecord, entrypoint: str
    ) -> Callable[[dict[str, Any]], Any]:
        module_dir = record.path
        relative, separator, function_name = entrypoint.partition(":")
        if not separator or not relative.endswith(".py") or not function_name:
            raise RuntimeContractError("entrypoint must look like experiment.py:run")
        path = (module_dir / relative).resolve()
        if module_dir.resolve() not in path.parents:
            raise RuntimeContractError("entrypoint escapes module directory")
        if not path.is_file():
            raise RuntimeContractError(f"entrypoint file does not exist: {relative}")
        key = (path, record.revision.content_digest)
        with self._lock:
            module = self._modules.get(key)
            if module is None:
                name = f"elp_course_{record.revision.content_digest}"
                spec = importlib.util.spec_from_file_location(name, path)
                if spec is None or spec.loader is None:
                    raise RuntimeContractError(f"cannot import {relative}")
                module = importlib.util.module_from_spec(spec)
                previous = sys.dont_write_bytecode
                sys.dont_write_bytecode = True
                try:
                    spec.loader.exec_module(module)
                finally:
                    sys.dont_write_bytecode = previous
                self._modules = {
                    cached: value for cached, value in self._modules.items() if cached[0] != path
                }
                self._modules[key] = module
        function = getattr(module, function_name, None)
        if function is None or not callable(function):
            raise RuntimeContractError(f"entrypoint has no callable {function_name!r}")
        signature = inspect.signature(function)
        if len(signature.parameters) != 1:
            raise RuntimeContractError(
                "experiment function must accept exactly one parameter mapping"
            )
        return function

    @staticmethod
    def _validate_control_value(control: Any, value: Any) -> Any:
        if control.type in {"slider", "number"}:
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise RuntimeContractError(f"parameter {control.id!r} must be numeric")
            numeric = float(value)
            if not math.isfinite(numeric):
                raise RuntimeContractError(f"parameter {control.id!r} must be finite")
            assert control.minimum is not None and control.maximum is not None
            if numeric < control.minimum or numeric > control.maximum:
                raise RuntimeContractError(
                    f"parameter {control.id!r} is outside [{control.minimum}, {control.maximum}]"
                )
            return value
        if control.type == "toggle":
            if not isinstance(value, bool):
                raise RuntimeContractError(f"parameter {control.id!r} must be boolean")
            return value
        if control.type in {"select", "segmented"}:
            allowed = [option.value for option in control.options]
            if not any(type(value) is type(item) and value == item for item in allowed):
                raise RuntimeContractError(f"parameter {control.id!r} must be one of {allowed!r}")
            return value
        if control.type == "button":
            if value is not None and not isinstance(value, (str, int, float, bool)):
                raise RuntimeContractError(
                    f"parameter {control.id!r} must be a scalar action token"
                )
            return value
        raise RuntimeContractError(f"unsupported control type {control.type!r}")

    def _validated_parameters(self, manifest: Any, supplied: dict[str, Any]) -> dict[str, Any]:
        controls = {control.id: control for control in manifest.controls}
        unknown = set(supplied) - set(controls)
        if unknown:
            raise RuntimeContractError(f"unknown parameters: {sorted(unknown)}")
        merged: dict[str, Any] = {}
        for control in manifest.controls:
            value = supplied.get(control.id, control.default)
            merged[control.id] = self._validate_control_value(control, value)
        return merged

    def run(
        self,
        course_id: str,
        module_id: str,
        parameters: dict[str, Any],
        expected_content_digest: str | None = None,
    ) -> RunResult:
        course, record = self.catalog.module_record(course_id, module_id)
        manifest = record.manifest
        if (
            expected_content_digest is not None
            and expected_content_digest != record.revision.content_digest
        ):
            raise RuntimeContractError(
                "module content revision is stale; reload the module document"
            )
        try:
            record.assert_unchanged()
        except CatalogError as exc:
            raise RuntimeContractError(str(exc)) from exc
        merged = self._validated_parameters(manifest, parameters)
        if manifest.runtime.kind == "static":
            return RunResult(
                parameters=merged,
                course_revision=course.revision,
                module_revision=record.revision,
                platform_revision=platform_revision("static"),
            )
        assert manifest.runtime.entrypoint is not None
        function = self._load_callable(record, manifest.runtime.entrypoint)
        timeout = manifest.runtime.timeout_seconds or self.default_timeout
        executor = ThreadPoolExecutor(max_workers=1, thread_name_prefix="elp-experiment")
        future = executor.submit(function, merged)
        try:
            raw = future.result(timeout=timeout)
        except FutureTimeout as exc:
            future.cancel()
            executor.shutdown(wait=False, cancel_futures=True)
            raise RuntimeTimeout(f"experiment exceeded {timeout:.2f} seconds") from exc
        except Exception as exc:
            executor.shutdown(wait=True, cancel_futures=True)
            raise RuntimeContractError(f"experiment raised {type(exc).__name__}: {exc}") from exc
        else:
            executor.shutdown(wait=True)
        try:
            record.assert_unchanged()
            safe = jsonable(raw)
        except (CatalogError, TypeError, ValueError) as exc:
            raise RuntimeContractError(f"experiment returned invalid data: {exc}") from exc
        try:
            json.dumps(safe, separators=(",", ":"), allow_nan=False).encode("utf-8")
        except (TypeError, ValueError) as exc:
            raise RuntimeContractError(f"experiment returned invalid data: {exc}") from exc
        if not isinstance(safe, dict):
            raise RuntimeContractError("experiment must return a mapping")
        reserved = {"parameters", "course_revision", "module_revision", "platform_revision"}
        supplied_reserved = sorted(reserved & set(safe))
        if supplied_reserved:
            raise RuntimeContractError(
                f"experiment returned platform-owned fields: {supplied_reserved}"
            )
        try:
            result = RunResult.model_validate(
                safe
                | {
                    "parameters": merged,
                    "course_revision": course.revision,
                    "module_revision": record.revision,
                    "platform_revision": platform_revision("python"),
                }
            )
            self.catalog.validate_result_references(course_id, record, result)
        except (ValidationError, CatalogError) as exc:
            raise RuntimeContractError(f"invalid result envelope: {exc}") from exc
        return result
