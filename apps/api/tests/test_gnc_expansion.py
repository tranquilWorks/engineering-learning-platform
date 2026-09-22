from __future__ import annotations

import ast
import importlib.util
import json
import math
import re
from pathlib import Path
from typing import Any

import numpy as np

from elp_api.catalog import CourseCatalog
from elp_api.runtime import ExperimentRuntime

ROOT = Path(__file__).resolve().parents[3]
COURSE_ROOT = ROOT / "courses" / "controls-gnc"
SCENARIOS = ("baseline", "sweep_1", "sweep_2", "broken", "recovery")
GENERIC_LABELS = {"Independent variable", "Response", "Diagnostic", "output", "units"}


def _yaml(path: Path) -> dict[str, Any]:
    value, _ = CourseCatalog._read_yaml(path)
    return value


def _load(path: Path, name: str) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


REFERENCE = _load(COURSE_ROOT / "expansion_reference_cases.py", "gnc_expansion_reference")
EXPANSION = _yaml(COURSE_ROOT / "expansion-map.yaml")
NATIVE = EXPANSION["implemented_native_modules"]


def _schema_errors(document: dict[str, Any], schema: dict[str, Any]) -> list[str]:
    helper = _load(ROOT / "apps/api/tests/test_dsp_conversion_framework.py", "gnc_schema_helper")
    return helper._schema_errors(document, schema, schema)


def test_gnc_competency_map_is_closed_and_count_is_derived() -> None:
    mapping = _yaml(COURSE_ROOT / "competency-map.yaml")
    schema = json.loads((COURSE_ROOT / "competency-map.schema.json").read_text())
    assert _schema_errors(mapping, schema) == []
    assert mapping["count_derivation"]["source"] == "len(modules)"
    assert mapping["count_derivation"]["planned_module_count"] == len(mapping["modules"]) == 68
    assert [len(batch["module_ids"]) for batch in mapping["batch_plan"]] == [9, 9, 9, 5, 6, 3, 3]
    order = {module["id"]: index for index, module in enumerate(mapping["modules"])}
    for module in mapping["modules"]:
        assert all(order[dependency] < order[module["id"]] for dependency in module["depends_on"])


def test_gnc_native_designs_are_schema_valid_and_semantically_distinct() -> None:
    schema = json.loads((COURSE_ROOT / "native-design.schema.json").read_text())
    expected_ids = [f"P{number:02d}" for number in range(25, 25 + len(NATIVE))]
    assert [item["id"] for item in NATIVE] == expected_ids
    fingerprints: set[tuple[str, ...]] = set()
    for item in NATIVE:
        root = COURSE_ROOT / item["folder"]
        design = _yaml(root / "design.yaml")
        assert _schema_errors(design, schema) == []
        fingerprints.add(tuple(design["governing_equations"]))
        assert design["scenarios"]["baseline"] == design["scenarios"]["recovery"]
        assert design["scenarios"]["broken"]["broken_mode"] is True
        assert design["provenance"] == {
            "kind": "python-first-native",
            "source_equivalence_claimed": False,
            "competency_map": "../../competency-map.yaml",
            "matlab_runtime": "not_run",
        }
        lesson = (root / "lesson.md").read_text()
        for section in (
            "Model and equations",
            "Baseline workflow",
            "Two one-variable sweeps",
            "Intentionally broken case",
            "Recovery",
            "Limiting cases and invariants",
            "Independent evidence",
            "Common mistakes",
            "Teach-back",
        ):
            assert f"## {section}" in lesson
    assert len(fingerprints) == len(NATIVE)


def test_gnc_native_reference_has_no_production_execution_path() -> None:
    path = COURSE_ROOT / "expansion_reference_cases.py"
    tree = ast.parse(path.read_text())
    allowed_imports = {"json", "typing", "numpy", "__future__"}
    forbidden_calls = {"eval", "exec", "compile", "__import__", "run", "import_module"}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            assert all(alias.name.split(".")[0] in allowed_imports for alias in node.names)
        if isinstance(node, ast.ImportFrom):
            assert (node.module or "").split(".")[0] in allowed_imports
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            assert node.func.id not in forbidden_calls
    doc = ast.get_docstring(tree, clean=True) or ""
    assert "imports no production experiment" in doc
    assert "consumes no production result" in doc
    assert "perturbs no production value" in " ".join(doc.split())


def test_gnc_native_five_scenario_evidence_and_runtime() -> None:
    catalog = CourseCatalog([ROOT / "courses"])
    runtime = ExperimentRuntime(catalog)
    for item in NATIVE:
        number = int(item["id"][1:])
        root = COURSE_ROOT / item["folder"]
        design = _yaml(root / "design.yaml")
        module_id = _yaml(root / "module.yaml")["id"]
        expected = json.loads((root / "evidence/expected-independent.json").read_text())
        actual = json.loads((root / "evidence/actual-production.json").read_text())
        assert expected["origin"] == REFERENCE.origin(number)
        assert actual["origin"]["independent"] is False
        assert expected["signature_fields"] == actual["signature_fields"] == design["signature"]
        assert tuple(expected["cases"]) == tuple(actual["cases"]) == SCENARIOS
        for scenario in SCENARIOS:
            parameters = design["scenarios"][scenario]
            reference = REFERENCE.reference_signature(number, parameters)
            production = runtime.run("controls-gnc", module_id, parameters).diagnostics["signature"]
            assert reference == expected["cases"][scenario]["signature"]
            assert production == pytest_approx(
                actual["cases"][scenario]["signature"], design["tolerance"]
            )
            assert len(reference) == len(production) == len(design["signature"])
            assert np.all(np.isfinite(reference)) and np.all(np.isfinite(production))
            assert production == pytest_approx(reference, design["tolerance"])
        assert expected["cases"]["baseline"] == expected["cases"]["recovery"]
        assert actual["cases"]["baseline"] == actual["cases"]["recovery"]
        assert actual["cases"]["broken"]["signature"] != actual["cases"]["recovery"]["signature"]


def pytest_approx(expected: list[float], tolerance: dict[str, float]) -> Any:
    import pytest

    return pytest.approx(expected, abs=tolerance["absolute"], rel=tolerance["relative"])


def test_gnc_native_plots_use_quantity_specific_axes_and_units() -> None:
    catalog = CourseCatalog([ROOT / "courses"])
    runtime = ExperimentRuntime(catalog)
    for item in NATIVE:
        root = COURSE_ROOT / item["folder"]
        module_id = _yaml(root / "module.yaml")["id"]
        result = runtime.run("controls-gnc", module_id, {}).model_dump(mode="json")
        assert set(result["plots"]) == {"response", "mechanism"}
        for plot in result["plots"].values():
            for axis in ("xaxis", "yaxis"):
                title = plot["layout"][axis]["title"]["text"]
                assert title not in GENERIC_LABELS
                assert re.search(r"\([^()]+\)$", title), title
            for trace in plot["data"]:
                assert set(trace["meta"]) == {"x_quantity", "x_unit", "y_quantity", "y_unit"}
                assert all(str(value).strip() for value in trace["meta"].values())


def test_gnc_modeling_and_classical_teaching_invariants() -> None:
    catalog = CourseCatalog([ROOT / "courses"])
    runtime = ExperimentRuntime(catalog)

    def signature(number: int, supplied: dict[str, Any]) -> list[float]:
        item = NATIVE[number - 25]
        module_id = _yaml(COURSE_ROOT / item["folder"] / "module.yaml")["id"]
        return runtime.run("controls-gnc", module_id, supplied).diagnostics["signature"]

    assert signature(25, {"broken_mode": False})[0] == 0
    assert signature(25, {"broken_mode": True})[0] > 0
    assert signature(26, {"broken_mode": False})[0] < 1e-12
    assert signature(26, {"pole_offset_per_s": 0.0})[1] < 1e-12
    assert signature(27, {"damping_ratio": 0.3})[0] > signature(27, {"damping_ratio": 0.8})[0]
    assert signature(28, {"broken_mode": True})[0] > 0
    nyquist = signature(29, {"broken_mode": False})
    assert nyquist[2] == nyquist[1] - nyquist[0] == nyquist[3]
    sensitivity = signature(30, {"broken_mode": False})
    assert sensitivity[3] < 1e-12
    assert signature(31, {"broken_mode": False})[0] > 0
    assert signature(31, {"broken_mode": True})[0] <= 1e-8
    assert signature(32, {"broken_mode": False})[0] < signature(32, {"broken_mode": True})[0]
    assert signature(33, {"decoupler_regularization": 0.0, "broken_mode": False})[2] < 1e-12
    assert math.isfinite(signature(33, {"cross_coupling": 1.0})[1])


def test_gnc_state_and_digital_teaching_invariants() -> None:
    catalog = CourseCatalog([ROOT / "courses"])
    runtime = ExperimentRuntime(catalog)

    def signature(number: int, supplied: dict[str, Any]) -> list[float]:
        item = NATIVE[number - 25]
        module_id = _yaml(COURSE_ROOT / item["folder"] / "module.yaml")["id"]
        return runtime.run("controls-gnc", module_id, supplied).diagnostics["signature"]

    assert signature(34, {"broken_mode": True})[1] > signature(34, {"broken_mode": False})[1]
    assert signature(35, {"broken_mode": True})[1] > signature(35, {"broken_mode": False})[1]
    assert signature(36, {"broken_mode": False})[0] < 1e-12
    assert signature(36, {"broken_mode": True})[1] > 0.5
    assert signature(37, {"broken_mode": True})[0] > signature(37, {"broken_mode": False})[0]
    assert signature(38, {"broken_mode": False})[1] < 0 < signature(38, {"broken_mode": True})[1]
    assert signature(39, {"terminal_weight": 6.0})[1] == 6.0
    assert signature(39, {"broken_mode": True})[1] != 6.0
    assert signature(40, {"broken_mode": True})[2] < signature(40, {"broken_mode": False})[2]
    assert signature(41, {"broken_mode": True})[2] > signature(41, {"broken_mode": False})[2]
    assert signature(42, {"broken_mode": False})[0] == 0
    assert signature(42, {"broken_mode": True})[0] > 0
