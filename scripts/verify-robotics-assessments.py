"""Independently originate and replay all 69 Robotics assessments at their entry point."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import urllib.request
from pathlib import Path

import numpy as np
import yaml
from elp_api.catalog import CourseCatalog
from elp_api.runtime import ExperimentRuntime

ROOT = Path(__file__).resolve().parents[1]
COURSE = ROOT / "courses/robotics-autonomy"


def load(path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def compare(actual, expected, tolerance):
    a, b = np.asarray(actual, float), np.asarray(expected, float)
    assert (
        a.shape == b.shape and a.size and np.isfinite(a).all() and np.isfinite(b).all()
    )
    error = float(np.max(abs(a - b)))
    scaled = float(np.max(abs(a - b) / np.maximum(1, np.maximum(abs(a), abs(b)))))
    assert error <= max(
        tolerance["absolute"], tolerance["relative"] * max(1, float(np.max(abs(b))))
    )
    assert scaled <= tolerance["relative"]
    return error, scaled


def replay(base_url=None, refresh=False):
    source = load(COURSE / "reference_cases.py")
    native = load(COURSE / "expansion_reference_cases.py")
    registry = json.loads((COURSE / "assessment-map.json").read_text())
    catalog = CourseCatalog([COURSE])
    runtime = ExperimentRuntime(catalog)
    comparisons = []
    bindings = []
    for lesson in registry["lessons"]:
        n = lesson["number"]
        folder = COURSE / "modules" / lesson["module_id"]
        manifest = yaml.safe_load((folder / "module.yaml").read_text())
        if n <= 24:
            record = yaml.safe_load((folder / "verification.yaml").read_text())
            baseline = {c["id"]: c["default"] for c in manifest["controls"]}
            scenarios = {"baseline": baseline}
            for i, sweep in enumerate(record["learning"]["sweeps"][:2], 1):
                values = [v for v in sweep["values"] if v != baseline[sweep["control"]]]
                scenarios[f"sweep_{i}"] = {**baseline, sweep["control"]: values[-1]}
            scenarios.update(
                broken={**baseline, "broken_mode": True}, recovery=baseline
            )
            tolerance = record["python_verification"]["cases"][0]["tolerance"]
            reference = lambda p, n=n: source.expected_signature(
                f"P{n:02d}", p["broken_mode"], p
            )
            origin = record["python_verification"]["reference_method"]
        else:
            design = yaml.safe_load((folder / "design.yaml").read_text())
            scenarios = design["scenarios"]
            tolerance = design["tolerance"]
            reference = lambda p, n=n: native.reference_signature(n, p)
            origin = native.origin(n)
        _, record = catalog.module_record("robotics-autonomy", lesson["module_id"])
        retained_path = folder / "evidence/aggregate-independent.json"
        retained = {
            "schema_version": 1,
            "item_id": f"P{n:02d}",
            "origin": origin,
            "tolerance": tolerance,
            "cases": {},
        }
        for name, parameters in scenarios.items():
            expected = reference(parameters)
            retained["cases"][name] = {"parameters": parameters, "signature": expected}
            if base_url:
                request = urllib.request.Request(
                    base_url.rstrip("/")
                    + f"/api/v1/courses/robotics-autonomy/modules/{lesson['module_id']}/run",
                    data=json.dumps(
                        {
                            "parameters": parameters,
                            "expected_content_digest": record.revision.content_digest,
                        }
                    ).encode(),
                    headers={"Content-Type": "application/json"},
                )
                with urllib.request.urlopen(request, timeout=30) as response:
                    actual = json.load(response)
            else:
                actual = runtime.run(
                    "robotics-autonomy", lesson["module_id"], parameters
                ).model_dump(mode="json")
            error, scaled = compare(
                actual["diagnostics"]["signature"], expected, tolerance
            )
            comparisons.append(
                {
                    "number": n,
                    "scenario": name,
                    "status": "passed",
                    "maximum_absolute_error": error,
                    "maximum_scaled_relative_error": scaled,
                    "tolerance": tolerance,
                }
            )
            if refresh and n in (59, 67):
                # These native mechanisms changed in this batch. Historical source
                # conversion artifacts remain untouched.
                for filename, signature in [
                    ("expected-independent.json", expected),
                    ("actual-production.json", actual["diagnostics"]["signature"]),
                ]:
                    p = folder / "evidence" / filename
                    data = json.loads(p.read_text())
                    data["cases"][name]["signature"] = signature
                    p.write_text(json.dumps(data, indent=2) + "\n")
        if refresh:
            retained_path.write_text(json.dumps(retained, indent=2) + "\n")
        else:
            assert json.loads(retained_path.read_text()) == retained
        assert len(scenarios) == 5
        assert (folder / "assessment.md").is_file()
        assert set(lesson["plot_keys"]) == {
            p
            for b in manifest["blocks"]
            if b["type"] == "plot_grid"
            for p in b["plots"]
        }
        bindings.append(
            {
                "number": n,
                "module_id": lesson["module_id"],
                "content_digest": record.revision.content_digest,
                "independent_sha256": hashlib.sha256(
                    retained_path.read_bytes()
                ).hexdigest(),
            }
        )
        print(f"P{n:02d}: five independently calculated comparisons passed", flush=True)
    return {
        "schema_version": 1,
        "course_id": "robotics-autonomy",
        "status": "passed",
        "entrypoint": "http" if base_url else "runtime",
        "comparisons": comparisons,
        "bindings": bindings,
        "formative_count": len(registry["lessons"]),
        "portfolio_count": len(registry["portfolios"]),
        "learner_validation": "not_run",
        "container_validation": "owner_deferred",
        "claim_boundary": "Synthetic numerical and authored assessment bindings only; full aggregate acceptance is separate.",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url")
    parser.add_argument("--refresh-retained", action="store_true")
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "docs/course-quality/robotics-aggregate-replay.json",
    )
    args = parser.parse_args()
    report = replay(args.base_url, args.refresh_retained)
    args.output.write_text(json.dumps(report, indent=2) + "\n")
    print("345 comparisons and 69 current identity bindings passed")
