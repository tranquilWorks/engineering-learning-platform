"""Replay independent Controls evidence through the real runtime or HTTP API.

Retains scientific tolerances and hashes. This never records learner success.
"""

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
COURSE = ROOT / "courses/controls-gnc"


def load(path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def compare(actual, expected, tolerance):
    left, right = np.asarray(actual, dtype=float), np.asarray(expected, dtype=float)
    assert left.shape == right.shape and left.size
    assert np.isfinite(left).all() and np.isfinite(right).all()
    error = abs(left - right)
    absolute = float(np.max(error))
    relative = float(np.max(error / np.maximum(1, np.maximum(abs(left), abs(right)))))
    scale = float(max(np.max(abs(left)), np.max(abs(right)), 1))
    allowed = max(tolerance["absolute"], tolerance["relative"] * scale)
    assert absolute <= allowed, (absolute, allowed, tolerance)
    assert relative <= tolerance["relative"], (relative, tolerance)
    return absolute, relative


def http(base, path, payload=None):
    request = urllib.request.Request(
        base.rstrip("/") + path,
        data=json.dumps(payload).encode() if payload is not None else None,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def replay(base_url=None):
    source = load(COURSE / "reference_cases.py")
    native = load(COURSE / "expansion_reference_cases.py")
    registry = json.loads((COURSE / "assessment-map.json").read_text())
    catalog = CourseCatalog([ROOT / "courses"])
    runtime = ExperimentRuntime(catalog)
    comparisons, bindings, mechanisms = [], [], []
    for checkpoint in registry["lessons"]:
        number, module_id = checkpoint["number"], checkpoint["module_id"]
        folder = COURSE / "modules" / module_id
        retained_path = folder / "evidence/expected-independent.json"
        retained = json.loads(retained_path.read_text())
        scenarios = retained["cases"]
        design = (
            yaml.safe_load((folder / "design.yaml").read_text())
            if number > 24
            else None
        )
        tolerance = design["tolerance"] if design else source.tolerance(number)
        reference = native if design else source
        _, record = catalog.module_record("controls-gnc", module_id)
        path = f"/api/v1/courses/controls-gnc/modules/{module_id}"
        if base_url:
            document = http(base_url, path)
            assert (
                document["module_revision"]["content_digest"]
                == record.revision.content_digest
            )
        for scenario in ("baseline", "sweep_1", "sweep_2", "broken", "recovery"):
            parameters = scenarios[scenario]["parameters"]
            expected = reference.reference_signature(number, parameters)
            compare(expected, scenarios[scenario]["signature"], tolerance)
            if base_url:
                result = http(
                    base_url,
                    path + "/run",
                    {
                        "parameters": parameters,
                        "expected_content_digest": record.revision.content_digest,
                    },
                )
            else:
                result = runtime.run("controls-gnc", module_id, parameters).model_dump(
                    mode="json"
                )
            absolute, relative = compare(
                result["diagnostics"]["signature"], expected, tolerance
            )
            comparisons.append(
                {
                    "number": number,
                    "scenario": scenario,
                    "status": "passed",
                    "maximum_absolute_error": absolute,
                    "maximum_scaled_relative_error": relative,
                    "tolerance": tolerance,
                    "origin": reference.origin(number),
                    "expected_artifact_sha256": hashlib.sha256(
                        retained_path.read_bytes()
                    ).hexdigest(),
                }
            )
            if number in (44, 52, 53, 54, 58, 59, 63):
                full = native.aggregate_mechanism(number, parameters)
                keys = []
                for key, values in full.items():
                    if key == "signature" or values is None:
                        continue
                    actual = result["diagnostics"][key]
                    compare(
                        [actual] if np.isscalar(actual) else actual,
                        [values] if np.isscalar(values) else values,
                        tolerance,
                    )
                    keys.append(key)
                mechanisms.append(
                    {
                        "number": number,
                        "scenario": scenario,
                        "keys": keys,
                        "status": "passed",
                    }
                )
        bindings.append(
            {
                "number": number,
                "module_id": module_id,
                "content_digest": record.revision.content_digest,
                "assessment_sha256": hashlib.sha256(
                    (folder / "assessment.md").read_bytes()
                ).hexdigest(),
                "referenced": "assessment.md" in dict(record.input_hashes),
            }
        )
        assert bindings[-1]["referenced"]
        print(
            f"P{number:02}: five independent comparisons and checkpoint binding passed",
            flush=True,
        )
    assert len(comparisons) == 340 and len(bindings) == 68 and len(mechanisms) == 35
    return {
        "batch": "ELP-GNC-AGGREGATE-QUALITY-01",
        "baseline": registry["baseline"],
        "validation_level": "host_http_independent_replay"
        if base_url
        else "host_runtime_independent_replay",
        "base_url": base_url,
        "comparisons": comparisons,
        "bindings": bindings,
        "full_mechanism_comparisons": mechanisms,
        "formative_count": 68,
        "cumulative_count": 22,
        "learner_validation": "not_run",
        "manual_accessibility": "not_run",
        "matlab": "not_run",
        "hardware": "not_run",
        "production": "not_run",
        "container_validation": "separate_required_gate",
        "claim_boundary": "Retained synthetic models/cases only; authored assessment is not a learner outcome.",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url")
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "docs/course-quality/gnc-aggregate-review.json",
    )
    arguments = parser.parse_args()
    report = replay(arguments.base_url)
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(report, indent=2) + "\n")
    print(
        "340 fresh independent comparisons, 35 full mechanisms and 68 identity bindings passed"
    )
