#!/usr/bin/env python3
"""Independent full-mechanism replay for Vehicle P13–P16, locally or through baked HTTP."""

import argparse
import importlib.util
import json
from pathlib import Path
from urllib.request import Request, urlopen

import numpy as np
from elp_api.catalog import CourseCatalog

ROOT = Path(__file__).resolve().parents[1]
BASELINE = "1a0041bd24de1168c03ff2bf2a656a6061cac0e3"
COURSE = ROOT / "courses/vehicle-dynamics"
SELECTED = tuple(range(13, 17))


def load(path):
    spec = importlib.util.spec_from_file_location("vehicle_quality", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def folder(n):
    return next((COURSE / "modules").glob(f"{n:02d}-*"))


def assert_mechanism(actual, expected):
    """Compare every independently formulated physical field and full response array."""
    for group in ("physical", "response"):
        for field, value in expected[group].items():
            got = actual[group][field]
            if isinstance(value, list) and value and isinstance(value[0], str):
                assert got == value, (group, field)
            else:
                np.testing.assert_allclose(
                    got, value, atol=1e-10, rtol=1e-10, err_msg=f"{group}.{field}"
                )
    np.testing.assert_allclose(
        actual["signature"], expected["physical"]["signature"], atol=1e-10, rtol=1e-10
    )


def http_json(base, path, payload=None):
    request = Request(
        base + path,
        data=None if payload is None else json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
    )
    with urlopen(request, timeout=30) as response:
        raw = response.read(8388609)
        assert len(raw) <= 8388608
        return json.loads(raw)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url")
    args = parser.parse_args()
    reference = load(COURSE / "reference_cases.py")
    catalog = CourseCatalog([])
    identities, rows = [], []
    if args.base_url:
        for course in http_json(args.base_url, "/api/v1/catalog"):
            for module in course["modules"]:
                path = f"/api/v1/courses/{course['id']}/modules/{module['id']}"
                doc = http_json(args.base_url, path)
                local = catalog._module_record(
                    ROOT
                    / "courses"
                    / course["id"]
                    / "modules"
                    / module["id"]
                    / "module.yaml"
                )
                assert (
                    doc["module_revision"]["content_digest"]
                    == local.revision.content_digest
                )
                identities.append(
                    {
                        "course": course["id"],
                        "module": module["id"],
                        "content_digest": local.revision.content_digest,
                    }
                )
        assert len(identities) == 290
    for n in SELECTED:
        root = folder(n)
        manifest = json.loads((root / "module.yaml").read_text())
        verification = json.loads((root / "verification.yaml").read_text())
        primary, secondary = [c["id"] for c in manifest["controls"][:2]]
        local = catalog._module_record(root / "module.yaml")
        if args.base_url:
            path = f"/api/v1/courses/vehicle-dynamics/modules/{root.name}"
            doc = http_json(args.base_url, path)
        else:
            production = load(root / "experiment.py")
        for case in verification["scenarios"]:
            p = case["inputs"]
            expected = reference.vehicle_driveline_reference(
                n, p[primary], p[secondary], p["broken_mode"]
            )
            if args.base_url:
                actual = http_json(
                    args.base_url,
                    path + "/run",
                    {
                        "parameters": p,
                        "expected_content_digest": local.revision.content_digest,
                    },
                )
                assert actual["module_revision"] == doc["module_revision"]
            else:
                actual = production.run(p)
            assert_mechanism(actual["diagnostics"], expected)
            for filename in ("expected-independent", "actual-production"):
                saved = json.loads(
                    (root / "evidence" / f"{filename}.json").read_text()
                )["cases"][case["name"]]
                assert_mechanism(saved, expected)
            rows.append(
                {
                    "item": f"P{n:02d}",
                    "scenario": case["name"],
                    "inputs": p,
                    "content_digest": local.revision.content_digest,
                    "expected": expected["physical"]["signature"],
                    "actual": actual["diagnostics"]["signature"],
                    "physical_fields_compared": list(expected["physical"]),
                    "response_arrays_compared": list(expected["response"]),
                    "status": "passed",
                }
            )
    result = {
        "batch": "ELP-VEHICLE-DRIVELINE-QUALITY-04",
        "baseline": BASELINE,
        "validation_level": "independent_synthetic_http_replay"
        if args.base_url
        else "independent_synthetic_numerical",
        "base_url": args.base_url,
        "selected_lessons": {"vehicle-dynamics": SELECTED},
        "comparisons": rows,
        "host_baked_content_identities": identities,
        "tolerance": {"absolute": 1e-10, "relative": 1e-10},
        "physical_regressions": "separate focused pytest record",
        "browser_evidence": "separate browser-report.json",
        "learner_validation": "not_run",
        "hardware_validation": "not_run",
    }
    name = (
        "vehicle-driveline-container-numerical.json"
        if args.base_url
        else "vehicle-driveline-quality-revision.json"
    )
    (ROOT / "docs/course-quality" / name).write_text(
        json.dumps(result, indent=2) + "\n"
    )
    print(
        f"{len(rows)} independent full-mechanism comparisons passed; {len(identities)} host/baked identities"
    )


if __name__ == "__main__":
    main()
