from __future__ import annotations

import importlib.util
import json
import math
from pathlib import Path
from typing import Any

import pytest

from elp_api.catalog import CourseCatalog

ROOT = Path(__file__).resolve().parents[3]
COURSE = ROOT / "courses/vehicle-dynamics"
IDS = [
    "01-turn-steering-and-speed-into-a-vehicle-path",
    "02-relate-acceleration-to-tire-force",
    "03-see-longitudinal-weight-transfer",
    "04-use-the-friction-circle",
    "05-build-slip-ratio-intuition",
    "06-build-slip-angle-intuition",
    "07-use-the-bicycle-model",
    "08-separate-understeer-from-oversteer",
    "09-choose-spring-rate-and-ride-frequency",
    "10-see-damping-change-transient-motion",
    "11-distribute-roll-stiffness",
    "12-explore-camber-and-toe-geometry",
    "13-map-engine-torque-through-gearing",
    "14-choose-shift-points",
    "15-model-braking-distance-and-heat",
    "16-balance-drag-and-downforce",
    "17-decode-and-plot-can-signals",
    "18-fuse-gps-and-imu-motion",
    "19-estimate-vehicle-state",
    "20-identify-parameters-from-a-real-drive",
    "21-optimize-a-racing-line",
    "22-build-a-lap-time-simulator",
    "23-compare-setup-changes-quantitatively",
    "24-construct-a-gr86-digital-twin",
]


def _load(path: Path, name: str) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


REFERENCE = _load(COURSE / "reference_cases.py", "vehicle_reference")


def test_exact_membership_provenance_evidence_and_digests() -> None:
    roots = sorted(path.parent for path in (COURSE / "modules").glob("*/module.yaml"))[: len(IDS)]
    assert [path.name for path in roots] == IDS
    coverage, _ = CourseCatalog._read_yaml(COURSE / "coverage.yaml")
    catalog = CourseCatalog([ROOT / "courses"]).course("vehicle-dynamics")
    digests = {item.manifest.number: item.revision.content_digest for item in catalog.modules}
    for number, root in enumerate(roots, 1):
        manifest, _ = CourseCatalog._read_yaml(root / "module.yaml")
        verification, _ = CourseCatalog._read_yaml(root / "verification.yaml")
        expected = json.loads((root / "expected.json").read_text())
        actual = json.loads((root / "actual.json").read_text())
        assert manifest["number"] == number and manifest["status"] == "implemented"
        provenance = "implemented-source comparison" if number <= 2 else "Python-first native"
        assert verification["provenance"] == provenance
        assert not verification["reference"]["imports_production"]
        assert not verification["reference"]["consumes_production_output"]
        assert list(expected) == ["baseline", "sweep_1", "sweep_2", "broken", "recovery"]
        assert expected["baseline"] == expected["recovery"]
        for scenario in expected:
            assert actual[scenario] == pytest.approx(expected[scenario], abs=1e-10, rel=1e-10)
        if number >= 9:
            assert expected["broken"] != expected["recovery"]
        assert coverage["items"][number - 1]["target_content_digest"] == digests[number]


@pytest.mark.parametrize(("number", "module_id"), list(enumerate(IDS, 1)))
def test_scenarios_reference_determinism_limits_and_outputs(number: int, module_id: str) -> None:
    root = COURSE / "modules" / module_id
    manifest, _ = CourseCatalog._read_yaml(root / "module.yaml")
    experiment = _load(root / "experiment.py", f"vehicle_{number}")
    primary, secondary = manifest["controls"][:2]
    cases = [
        (primary["default"], secondary["default"], False),
        (primary["minimum"], secondary["default"], False),
        (primary["default"], secondary["maximum"], False),
        (primary["default"], secondary["default"], True),
    ]
    for p_value, s_value, broken in cases:
        inputs = {primary["id"]: p_value, secondary["id"]: s_value, "broken_mode": broken}
        first = experiment.run(inputs)
        assert first == experiment.run(inputs)
        signature = first["diagnostics"]["signature"]
        assert signature == pytest.approx(
            REFERENCE.evaluate(f"P{number:02d}", p_value, s_value, broken), abs=1e-10, rel=1e-10
        )
        assert all(math.isfinite(value) for value in signature)
        assert set(first["plots"]) == {
            "response",
            "primary_sweep",
            "secondary_sweep",
            "broken_recovery",
        }
    with pytest.raises(ValueError, match="outside declared finite range"):
        experiment.run(
            {
                primary["id"]: primary["maximum"] + abs(primary["step"]),
                secondary["id"]: secondary["default"],
                "broken_mode": False,
            }
        )


def test_lessons_and_catalog_boundary() -> None:
    for root in sorted((COURSE / "modules").glob("*"))[: len(IDS)]:
        lesson = (root / "lesson.md").read_text().lower()
        for phrase in (
            "physical model",
            "predict and sweep",
            "named broken behavior",
            "exact recovery",
            "limits and limiting cases",
            "common mistakes",
            "formative checks",
            "teach-back checklist",
            "not measured-vehicle",
        ):
            assert phrase in lesson
    summaries = CourseCatalog([ROOT / "courses"]).summaries()
    assert len(summaries) == 6
    assert sum(len(course.modules) for course in summaries) == 256
    assert sum(module.interactive for course in summaries for module in course.modules) == 256


def _run(number: int, **overrides: float | bool) -> list[float]:
    root = COURSE / "modules" / IDS[number - 1]
    manifest, _ = CourseCatalog._read_yaml(root / "module.yaml")
    experiment = _load(root / "experiment.py", f"vehicle_topic_{number}")
    inputs = {control["id"]: control["default"] for control in manifest["controls"]}
    inputs.update(overrides)
    return experiment.run(inputs)["diagnostics"]["signature"]


def test_p09_p16_topic_relations_boundaries_and_failures() -> None:
    p09 = _run(9)
    assert p09[0] == pytest.approx(p09[3] * p09[4] ** 2)
    assert p09[0] * p09[2] == pytest.approx(300.0 * 9.81)

    p10 = _run(10)
    p10_broken = _run(10, broken_mode=True)
    assert p10[1] > 0.0 and p10[5] > 0.0 and p10[-1] == 0.0
    assert p10_broken[1] < 0.0 and p10_broken[5] < 0.0 and p10_broken[-1] == 1.0

    p11 = _run(11)
    assert p11[4] == pytest.approx(0.0, abs=1e-10)
    assert p11[1] * 1.53 + p11[2] * 1.53 == pytest.approx(1320.0 * 7.0 * 0.50)
    assert p11[1] + p11[2] == pytest.approx(1320.0 * 7.0 * 0.50 / 1.53)

    p12_zero = _run(12, camber_deg=0.0, toe_deg=0.0)
    assert p12_zero[2:5] == pytest.approx([0.0, 0.0, 0.0])
    assert _run(12)[2] > 0.0

    p13 = _run(13, engine_torque_n_m=320.0, gear_ratio=4.2)
    p13_broken = _run(13, broken_mode=True)
    assert p13[2] == pytest.approx(p13[3]) and p13[2] < p13[1]
    assert p13_broken[-1] == 1.0 and p13_broken != _run(13)

    p14 = _run(14)
    assert 2500.0 <= p14[0] <= 7400.0 and p14[4] < p14[0]
    assert _run(14, broken_mode=True)[-1] == 1.0

    p15 = _run(15, requested_brake_force_n=18000.0)
    p15_broken = _run(15, broken_mode=True)
    assert p15[0] < 18000.0
    assert p15[0] * p15[2] == pytest.approx(p15[4])
    assert p15[6] + p15[7] == pytest.approx(1320.0 * 9.81)
    assert p15_broken[5] > _run(15)[5] and p15_broken[-1] == 1.0

    p16 = _run(16)
    p16_slow = _run(16, speed_m_s=20.0)
    assert p16[0] == pytest.approx(4.0 * p16_slow[0])
    assert p16[4] == pytest.approx(p16[1] * 40.0)
    assert p16[3] - 1320.0 * 9.81 == pytest.approx(p16[2])
    assert _run(16, broken_mode=True)[-1] == 1.0


def test_p17_p24_topic_relations_boundaries_and_failures() -> None:
    p17 = _run(17)
    assert p17[:3] == pytest.approx([36.0, 10.0, 0.0])
    assert _run(17, frame_age_ms=250.0)[-1] == 1.0
    assert _run(17, broken_mode=True)[2] != 0.0

    p18 = _run(18)
    p18_broken = _run(18, broken_mode=True)
    assert p18[5] == 0.0 and p18_broken[5] == 1.0
    assert p18_broken[2] > p18[2] and p18_broken[-1] == 1.0

    p19 = _run(19)
    assert p19[3] * p19[4] == pytest.approx(1.0)
    assert p19[6] == pytest.approx(20.0 * 10.0)
    assert _run(19, broken_mode=True)[2] > 4000.0

    p20_exact = _run(20, force_noise_n=0.0)
    assert p20_exact[:2] == pytest.approx([180.0, 0.64], abs=1e-10)
    assert p20_exact[2:4] == pytest.approx([0.0, 0.0], abs=1e-10)
    assert _run(20, broken_mode=True)[4:6] == [0.0, 0.0]

    p21 = _run(21)
    assert p21[6] >= 0.0 and p21[7] == 41.0
    assert _run(21, broken_mode=True)[6] < 0.0

    p22 = _run(22)
    p22_broken = _run(22, broken_mode=True)
    assert p22[3] == pytest.approx(0.0) and p22[-1] == 0.0
    assert p22_broken[3] > 0.0 and p22_broken[-1] == 1.0

    p23 = _run(23)
    assert sum(p23[3:6]) == pytest.approx(p23[2])
    assert p23[7] > 0.0 and p23[8] == 1.0
    assert _run(23, broken_mode=True)[6] > p23[6]

    p24 = _run(24)
    p24_broken = _run(24, broken_mode=True)
    assert p24[6] == 3.0 and p24[-1] == 0.0
    assert p24_broken[1] > p24[1] and p24_broken[2] > p24[2]
    assert p24_broken[-1] == 1.0
