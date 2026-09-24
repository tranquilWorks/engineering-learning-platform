from __future__ import annotations

import ast
import importlib.util
import json
import math
import re
from pathlib import Path
from typing import Any

import numpy as np
import pytest

from elp_api.catalog import CourseCatalog
from elp_api.runtime import ExperimentRuntime

ROOT = Path(__file__).resolve().parents[3]
COURSE_ROOT = ROOT / "courses" / "vehicle-dynamics"
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


REFERENCE = _load(
    COURSE_ROOT / "expansion_reference_cases.py",
    "vehicle_dynamics_expansion_reference",
)
EXPANSION = _yaml(COURSE_ROOT / "expansion-map.yaml")
NATIVE = EXPANSION["implemented_native_modules"]


def _schema_errors(document: dict[str, Any], schema: dict[str, Any]) -> list[str]:
    helper = _load(
        ROOT / "apps/api/tests/test_dsp_conversion_framework.py",
        "vehicle_expansion_schema_helper",
    )
    return helper._schema_errors(document, schema, schema)


def _signature(
    runtime: ExperimentRuntime,
    number: int,
    overrides: dict[str, float | bool],
) -> list[float]:
    item = NATIVE[number - 25]
    root = COURSE_ROOT / item["folder"]
    manifest = _yaml(root / "module.yaml")
    return runtime.run("vehicle-dynamics", manifest["id"], overrides).diagnostics["signature"]


def test_vehicle_expansion_matches_reviewed_map_and_declares_pending_depth() -> None:
    mapping = _yaml(COURSE_ROOT / "competency-map.yaml")
    schema = json.loads((COURSE_ROOT / "competency-map.schema.json").read_text())
    assert _schema_errors(mapping, schema) == []
    assert mapping["count_derivation"]["source"] == "len(modules)"
    assert mapping["count_derivation"]["planned_module_count"] == len(mapping["modules"]) == 67
    assert [len(batch["module_ids"]) for batch in mapping["batch_plan"]] == [
        8,
        8,
        8,
        9,
        10,
        9,
        8,
        7,
    ]
    assert EXPANSION["source_bound_modules"] == 24
    assert EXPANSION["planned_modules"] == 67
    assert [item["id"] for item in NATIVE] == [
        f"P{number:02d}" for number in range(25, 44)
    ]
    assert EXPANSION["pending_native_modules"] == [
        f"P{number:02d}" for number in range(44, 68)
    ]
    map_by_id = {item["id"]: item for item in mapping["modules"]}
    assert [map_by_id[item["id"]]["title"] for item in NATIVE] == [
        "Measure Motion in Body, Path, and Wheel Frames",
        "Quantify Tire Load Sensitivity",
        "Fit Longitudinal Force versus Slip Ratio",
        "Fit Lateral Force versus Slip Angle and Camber",
        "Combine Longitudinal and Lateral Slip",
        "Model Tire Relaxation and Transient Force",
        "Track Tire Temperature, Pressure, and Grip",
        "Accumulate Tire Work and Thermal Energy",
        "Validate a Tire Model with Uncertainty",
        "Derive the Dynamic Bicycle State Model",
        "Analyze Yaw and Sideslip Frequency Response",
        "Measure Understeer Gradient and Characteristic Speed",
        "Test Nonlinear Limit Handling and Stability",
        "Partition Lateral Load Transfer",
        "Couple Heave, Pitch, and Roll Modes",
        "Predict Road-Input Ride Transmissibility",
        "Shape Digressive Damper Force-Velocity Response",
        "Trace Suspension Kinematics and Compliance",
        "Evaluate Anti-Dive and Anti-Squat Geometry",
    ]


def test_vehicle_native_designs_are_schema_valid_and_semantically_distinct() -> None:
    schema = json.loads((COURSE_ROOT / "native-design.schema.json").read_text())
    fingerprints: set[tuple[str, ...]] = set()
    for item in NATIVE:
        root = COURSE_ROOT / item["folder"]
        design = _yaml(root / "design.yaml")
        manifest = _yaml(root / "module.yaml")
        assert _schema_errors(design, schema) == []
        assert design["item_id"] == item["id"]
        assert manifest["number"] == int(item["id"][1:])
        assert manifest["title"] == next(
            module["title"]
            for module in _yaml(COURSE_ROOT / "competency-map.yaml")["modules"]
            if module["id"] == item["id"]
        )
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
            "Formative checks",
            "Teach-back",
        ):
            assert f"## {section}" in lesson
        assert "not a source conversion" in lesson
        assert "measured-vehicle result" in lesson
    assert len(fingerprints) == len(NATIVE)


def test_vehicle_native_reference_has_no_production_execution_path() -> None:
    path = COURSE_ROOT / "expansion_reference_cases.py"
    tree = ast.parse(path.read_text())
    allowed_imports = {"typing", "numpy", "__future__"}
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


def test_vehicle_native_five_scenario_evidence_and_runtime() -> None:
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
            production = runtime.run(
                "vehicle-dynamics",
                module_id,
                parameters,
            ).diagnostics["signature"]
            assert reference == expected["cases"][scenario]["signature"]
            assert production == pytest.approx(
                actual["cases"][scenario]["signature"],
                abs=design["tolerance"]["absolute"],
                rel=design["tolerance"]["relative"],
            )
            assert production == pytest.approx(
                reference,
                abs=design["tolerance"]["absolute"],
                rel=design["tolerance"]["relative"],
            )
            assert len(reference) == len(production) == len(design["signature"])
            assert np.all(np.isfinite(reference))
            assert np.all(np.isfinite(production))
        assert expected["cases"]["baseline"] == expected["cases"]["recovery"]
        assert actual["cases"]["baseline"] == actual["cases"]["recovery"]
        assert actual["cases"]["broken"]["signature"] != actual["cases"]["recovery"]["signature"]


def test_vehicle_native_plots_use_quantity_specific_axes_and_units() -> None:
    runtime = ExperimentRuntime(CourseCatalog([ROOT / "courses"]))
    for item in NATIVE:
        root = COURSE_ROOT / item["folder"]
        module_id = _yaml(root / "module.yaml")["id"]
        result = runtime.run("vehicle-dynamics", module_id, {}).model_dump(mode="json")
        assert set(result["plots"]) == {"response", "mechanism"}
        for plot in result["plots"].values():
            for axis in ("xaxis", "yaxis"):
                title = plot["layout"][axis]["title"]["text"]
                assert title not in GENERIC_LABELS
                assert re.search(r"\([^()]+\)$", title), title
            for trace in plot["data"]:
                assert set(trace["meta"]) == {
                    "x_quantity",
                    "x_unit",
                    "y_quantity",
                    "y_unit",
                }
                assert all(str(value).strip() for value in trace["meta"].values())


def test_vehicle_tire_teaching_invariants_and_named_failures() -> None:
    runtime = ExperimentRuntime(CourseCatalog([ROOT / "courses"]))

    frames = _signature(runtime, 25, {"broken_mode": False})
    frames_broken = _signature(runtime, 25, {"broken_mode": True})
    assert frames[3] < 1e-12 and frames[4] < 1e-12
    assert frames_broken[3] < 1e-12 and frames_broken[4] > 0.5

    load = _signature(runtime, 26, {"broken_mode": False})
    load_broken = _signature(runtime, 26, {"broken_mode": True})
    assert load[2] > 0.0 and load[3] < 1e-12
    assert abs(load_broken[2]) < 1e-12 and load_broken[3] > 0.0

    longitudinal = _signature(runtime, 27, {"broken_mode": False})
    longitudinal_broken = _signature(runtime, 27, {"broken_mode": True})
    assert longitudinal[2] < 1e-10 and longitudinal[4] < 1e-12
    assert longitudinal_broken[2] > 1000.0 and longitudinal_broken[4] > 0.9

    lateral = _signature(runtime, 28, {"broken_mode": False})
    lateral_broken = _signature(runtime, 28, {"broken_mode": True})
    assert lateral[2] < 1e-8 and lateral[4] < 1e-10
    assert lateral_broken[2] > 500.0 and lateral_broken[4] > 0.9

    combined = _signature(runtime, 29, {"broken_mode": False})
    combined_broken = _signature(runtime, 29, {"broken_mode": True})
    assert combined[2] <= 1.0 + 1e-12 and combined[4] == 0.0
    assert combined_broken[2] > 1.0 and combined_broken[4] > 0.0

    relaxation = _signature(runtime, 30, {"broken_mode": False})
    relaxation_broken = _signature(runtime, 30, {"broken_mode": True})
    assert relaxation[0] == pytest.approx(3000.0 * (1.0 - math.exp(-1.0)))
    assert relaxation[1] == pytest.approx(0.45)
    assert relaxation[4] < 1e-12
    assert relaxation_broken[0] < relaxation[0] and relaxation_broken[4] > 1.0

    thermal = _signature(runtime, 31, {"broken_mode": False})
    thermal_broken = _signature(runtime, 31, {"broken_mode": True})
    assert thermal[3] == 0.0 and thermal[4] < 1e-7
    assert thermal_broken[3] > 100.0

    energy = _signature(runtime, 32, {"broken_mode": False})
    energy_broken = _signature(runtime, 32, {"broken_mode": True})
    assert energy[4] < 1e-7
    assert energy_broken[4] > 1000.0

    validation = _signature(runtime, 33, {"broken_mode": False})
    validation_broken = _signature(runtime, 33, {"broken_mode": True})
    assert 0.0 <= validation[3] <= 1.0
    assert validation_broken[3] < validation[3]
    assert validation_broken[4] > validation[4]


def test_vehicle_chassis_teaching_invariants_and_named_failures() -> None:
    runtime = ExperimentRuntime(CourseCatalog([ROOT / "courses"]))

    bicycle = _signature(runtime, 34, {"broken_mode": False})
    bicycle_broken = _signature(runtime, 34, {"broken_mode": True})
    assert bicycle[2] < 0.0 and bicycle[3] < 1e-8 and bicycle[4] < 1e-8
    assert bicycle_broken[2] > 0.0 and bicycle_broken[3] > 100.0

    frequency = _signature(runtime, 35, {"broken_mode": False})
    frequency_broken = _signature(runtime, 35, {"broken_mode": True})
    assert frequency[0] > 0.0 and frequency[4] < 1e-10
    assert frequency_broken[4] > 1.0

    understeer = _signature(runtime, 36, {"broken_mode": False})
    understeer_broken = _signature(runtime, 36, {"broken_mode": True})
    assert understeer[0] > 0.0 and understeer[1] > 0.0 and understeer[4] < 1e-10
    assert understeer_broken[4] > 10.0

    limit = _signature(runtime, 37, {"broken_mode": False})
    limit_broken = _signature(runtime, 37, {"broken_mode": True})
    assert limit[0] <= 1.0 and limit[1] <= 1.0 and limit[4] == 0.0
    assert limit_broken[4] > 0.0

    transfer = _signature(runtime, 38, {"broken_mode": False})
    transfer_broken = _signature(runtime, 38, {"broken_mode": True})
    assert transfer[0] > 0.0 and transfer[1] > 0.0 and transfer[3] < 1e-8
    assert transfer_broken[3] > 100.0

    modes = _signature(runtime, 39, {"broken_mode": False})
    modes_broken = _signature(runtime, 39, {"broken_mode": True})
    assert 0.0 < modes[0] < modes[1] < modes[2] and modes[4] < 1e-10
    assert modes_broken[4] > 0.01

    ride = _signature(runtime, 40, {"broken_mode": False})
    ride_broken = _signature(runtime, 40, {"broken_mode": True})
    assert ride[0] > 0.0 and ride[2] > 0.0 and ride[4] < 1e-10
    assert ride_broken[4] > 0.5

    damper = _signature(runtime, 41, {"broken_mode": False})
    damper_broken = _signature(runtime, 41, {"broken_mode": True})
    assert damper[0] > 0.0 and damper[1] > damper[0] and damper[3] > 0.0
    assert damper[4] == 0.0 and damper_broken[4] > 1000.0

    suspension = _signature(runtime, 42, {"broken_mode": False})
    suspension_broken = _signature(runtime, 42, {"broken_mode": True})
    assert suspension[2] > 0.0 and suspension[3] > 0.0 and suspension[4] == 0.0
    assert suspension_broken[4] > 0.5

    anti = _signature(runtime, 43, {"broken_mode": False})
    anti_broken = _signature(runtime, 43, {"broken_mode": True})
    assert 0.0 < anti[0] < anti[1] < 100.0 and anti[4] < 1e-10
    assert abs(anti_broken[0]) > 100.0 and anti_broken[4] > 1000.0


def test_vehicle_native_experiments_reject_nonfinite_and_out_of_range_inputs() -> None:
    for item in NATIVE:
        root = COURSE_ROOT / item["folder"]
        manifest = _yaml(root / "module.yaml")
        experiment = _load(root / "experiment.py", f"vehicle_bounds_{item['id']}")
        first = manifest["controls"][0]
        with pytest.raises(ValueError, match="outside declared finite range"):
            experiment.run({first["id"]: first["maximum"] + abs(first["step"])})
        with pytest.raises(ValueError, match="outside declared finite range"):
            experiment.run({first["id"]: float("nan")})


def test_vehicle_expansion_catalog_shape() -> None:
    summaries = CourseCatalog([ROOT / "courses"]).summaries()
    assert len(summaries) == 6
    assert sum(len(course.modules) for course in summaries) == 266
    assert sum(module.interactive for course in summaries for module in course.modules) == 266
    vehicle = next(course for course in summaries if course.id == "vehicle-dynamics")
    assert [module.number for module in vehicle.modules] == list(range(1, 44))
