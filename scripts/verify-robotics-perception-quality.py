#!/usr/bin/env python3
"""Record independent replay and physical regressions for the scoped Robotics perception revision."""

import argparse
import importlib.util
import json
import subprocess
import sys
import time
from pathlib import Path
from urllib.error import URLError
from urllib.request import Request, urlopen

import numpy as np
import yaml
from elp_api.catalog import CourseCatalog

ROOT = Path(__file__).resolve().parents[1]
SELECTED = {"robotics-autonomy": (42, 43, 44, 45, 46, 47, 48, 52)}


def load(path):
    spec = importlib.util.spec_from_file_location("verified_model", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def http_json(base, path, payload=None):
    data = None if payload is None else json.dumps(payload).encode()
    request = Request(
        base + path, data=data, headers={"Content-Type": "application/json"}
    )
    with urlopen(request, timeout=30) as response:
        raw = response.read(8388609)
        assert len(raw) <= 8388608
        return json.loads(raw)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--base-url", help="Replay the baked HTTP runtime instead of local production"
    )
    args = parser.parse_args()
    if args.base_url:
        # A just-started preview first validates its baked catalog. Retry readiness
        # only; individual experiment failures below remain immediate failures.
        for attempt in range(60):
            try:
                http_json(args.base_url, "/api/v1/catalog")
                break
            except (URLError, ConnectionResetError):
                if attempt == 59:
                    raise
                time.sleep(1)
    identity_catalog = CourseCatalog([])
    rows = []
    identities = []
    if args.base_url:
        for course_doc in http_json(args.base_url, "/api/v1/catalog"):
            for module_doc in course_doc["modules"]:
                course_id, module_id = course_doc["id"], module_doc["id"]
                doc = http_json(
                    args.base_url, f"/api/v1/courses/{course_id}/modules/{module_id}"
                )
                canonical = (
                    ROOT / "courses" / course_id / "modules" / module_id / "module.yaml"
                )
                local = identity_catalog._module_record(canonical)
                assert (
                    doc["module_revision"]["content_digest"]
                    == local.revision.content_digest
                )
                identities.append(
                    {
                        "course": course_id,
                        "module": module_id,
                        "content_digest": local.revision.content_digest,
                    }
                )
        assert len(identities) == 290
    for course, number in [(c, n) for c, numbers in SELECTED.items() for n in numbers]:
        COURSE = ROOT / "courses" / course
        reference = load(COURSE / "expansion_reference_cases.py")
        folder = next((COURSE / "modules").glob(f"{number}-*"))
        design = yaml.safe_load((folder / "design.yaml").read_text())
        if args.base_url:
            path = f"/api/v1/courses/{course}/modules/{folder.name}"
            doc = http_json(args.base_url, path)
            local_record = identity_catalog._module_record(folder / "module.yaml")
            assert (
                doc["module_revision"]["content_digest"]
                == local_record.revision.content_digest
            )
        else:
            experiment = load(folder / "experiment.py")
        for scenario, parameters in design["scenarios"].items():
            expected = reference.reference_signature(number, parameters)
            if args.base_url:
                result = http_json(
                    args.base_url,
                    path + "/run",
                    {
                        "parameters": parameters,
                        "expected_content_digest": doc["module_revision"][
                            "content_digest"
                        ],
                    },
                )
                assert result["module_revision"] == doc["module_revision"]
                actual = result["diagnostics"]["signature"]
            else:
                actual = experiment.run(parameters)["diagnostics"]["signature"]
            np.testing.assert_allclose(actual, expected, atol=1e-8, rtol=1e-8)
            rows.append(
                {
                    "course": course,
                    "item": f"P{number}",
                    "scenario": scenario,
                    "content_digest": doc["module_revision"]["content_digest"]
                    if args.base_url
                    else None,
                    "expected": expected,
                    "actual": actual,
                    "max_absolute_difference": float(
                        max(abs(np.array(actual) - expected))
                    ),
                    "status": "passed",
                }
            )
    if not args.base_url:
        subprocess.run(
            [
                sys.executable,
                "-m",
                "pytest",
                "-q",
                "apps/api/tests/test_robotics_perception_quality.py",
            ],
            cwd=ROOT,
            check=True,
        )
    result = {
        "batch": "ELP-ROBOTICS-PERCEPTION-QUALITY-08",
        "baseline": "f04472f16fc1da00e817d385eaef0a63f3c71b48",
        "validation_level": "independent_synthetic_http_replay"
        if args.base_url
        else "independent_synthetic_numerical",
        "base_url": args.base_url,
        "selected_lessons": SELECTED,
        "comparisons": rows,
        "host_baked_content_identities": identities,
        "physical_regressions": "separate local test record"
        if args.base_url
        else "passed",
        "tolerance": {"absolute": 1e-8, "relative": 1e-8},
        "learner_validation": "not_run",
        "hardware_validation": "not_run",
        "browser_evidence": "browser-report.json (separate run)",
    }
    filename = (
        "robotics-perception-container-numerical.json"
        if args.base_url
        else "robotics-perception-quality-revision.json"
    )
    (ROOT / "docs/course-quality" / filename).write_text(
        json.dumps(result, indent=2) + "\n"
    )
    print(f"{len(rows)} independent comparisons passed ({result['validation_level']})")


if __name__ == "__main__":
    main()
