"""Fresh independent replay and concrete assessment bindings; no learner scoring."""

import hashlib
import importlib.util
import json
import math
from pathlib import Path

import numpy as np
import yaml
from elp_api.catalog import CourseCatalog
from elp_api.runtime import ExperimentRuntime

ROOT = Path(__file__).resolve().parents[1]
COURSE = ROOT / "courses/dsp-radar"
PROBES = {
    "DSP-A01": (3, ["signed_alias", "apparent_frequency"], ["folding", "phase_check"]),
    "DSP-A02": (
        11,
        ["bin_spacing", "peak_bin", "reported_frequency"],
        ["bin_map", "neighboring_bins"],
    ),
    "DSP-A03": (28, [], ["roc", "selection", "variance_sweep"]),
    "DSP-A04": (
        40,
        [
            "coherent_output_snr",
            "active_signal_power_fraction",
            "recovered_signal_power_fraction",
        ],
        [],
    ),
    "DSP-A05": (
        52,
        [
            "active_alpha",
            "active_alarm_count",
            "active_measured_pfa",
            "active_theoretical_pfa",
            "wilson_lower",
            "wilson_upper",
            "correlated_pfa",
            "textured_pfa",
        ],
        [],
    ),
    "DSP-A06": (
        60,
        ["position_rmse", "fixed_cv_rmse", "probability_sum_error"],
        ["probability"],
    ),
    "DSP-A07": (
        68,
        [
            "active_scnr",
            "fixed_scnr",
            "separate_scnr",
            "target_response",
            "interference_output",
            "distortionless_error",
        ],
        ["components"],
    ),
    "DSP-A08": (
        74,
        [
            "bulk_doppler",
            "limb_low",
            "limb_high",
            "window_duration",
            "native_frequency_scale",
        ],
        ["spectrogram"],
    ),
    "DSP-A09": (
        83,
        [
            "active_scnr",
            "clean_scnr",
            "distortionless_error",
            "target_output_change",
            "interference_output_change",
        ],
        ["active", "clean"],
    ),
    "DSP-A10": (
        84,
        [
            "receiver_reconstruction_error",
            "compression_peak_ratio",
            "detected_cells",
            "clustered_reports",
            "matched_truth_reports",
            "false_reports",
            "empirical_false_cell_rate",
            "baseline_track_rmse",
            "baseline_sequence_pd",
            "scan_four_coast_count",
        ],
        [
            "waveform",
            "receiver",
            "matched",
            "range_doppler",
            "detections",
            "reports",
            "track",
            "coast",
        ],
    ),
}


def replay():
    registry = json.loads((COURSE / "assessment-map.json").read_text())
    spec = importlib.util.spec_from_file_location(
        "aggregate_independent_reference", COURSE / "remediation_reference_cases.py"
    )
    reference = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(reference)
    catalog = CourseCatalog([ROOT / "courses"])
    runtime = ExperimentRuntime(catalog)
    comparisons, bindings, baselines = [], [], {}
    for checkpoint in registry["lessons"]:
        n, module_id = checkpoint["number"], checkpoint["module_id"]
        folder = COURSE / "modules" / module_id
        raw = (folder / "conversion.yaml").read_text()
        conversion = (
            json.loads(raw) if raw.lstrip().startswith("{") else yaml.safe_load(raw)
        )
        for index, case in enumerate(conversion["python_source_equivalence"]["cases"]):
            scenario = case["name"]
            if n == 1:
                params = {"alias_mode": index == 1}
                fs = 8.0 if index == 1 else 200.0
                # Independently evaluated elementary phasor identities.
                expected = [fs, fs / 5, 5.0, math.sqrt(3) / 2, 0.5, 0.0, 0.0]
            else:
                params = reference.SCENARIOS[f"P{n:02}"][scenario]
                expected = reference.expected_signature(f"P{n:02}", scenario)
            actual = runtime.run("dsp-radar", module_id, params)
            observed = np.asarray(actual.diagnostics["signature"], dtype=float)
            expected = np.asarray(expected, dtype=float)
            assert (
                observed.shape == expected.shape
                and np.all(np.isfinite(observed))
                and np.all(np.isfinite(expected))
            )
            absolute = float(np.max(abs(observed - expected)))
            relative = float(
                np.max(
                    abs(observed - expected)
                    / np.maximum(np.maximum(abs(observed), abs(expected)), 1)
                )
            )
            tolerance = case["tolerance"]
            assert (
                absolute <= tolerance["absolute"] and relative <= tolerance["relative"]
            ), (n, scenario, absolute, relative, tolerance)
            retained = json.loads((COURSE / case["expected"]["path"]).read_text())
            retained_signature = retained["signature"] if n == 1 else retained
            np.testing.assert_allclose(
                expected,
                retained_signature,
                atol=tolerance["absolute"],
                rtol=tolerance["relative"],
            )
            assert (
                hashlib.sha256(
                    (COURSE / case["expected"]["path"]).read_bytes()
                ).hexdigest()
                == case["expected"]["sha256"]
            )
            comparisons.append(
                {
                    "number": n,
                    "module": module_id,
                    "scenario": scenario,
                    "maximum_absolute_error": absolute,
                    "maximum_relative_error": relative,
                    "tolerance": tolerance,
                    "status": "passed",
                }
            )
            if index == 0:
                baselines[n] = actual
                assert set(checkpoint["plot_keys"]) <= set(actual.plots)
                _, record = catalog.module_record("dsp-radar", module_id)
                bindings.append(
                    {
                        "number": n,
                        "module": module_id,
                        "content_digest": record.revision.content_digest,
                        "checkpoint": checkpoint["id"],
                        "assessment_sha256": hashlib.sha256(
                            (folder / "assessment.md").read_bytes()
                        ).hexdigest(),
                        "plot_keys": checkpoint["plot_keys"],
                        "status": "passed",
                    }
                )
            print(f"P{n:02} {scenario} independent comparison passed", flush=True)
    probes = []
    for domain, (n, metric_ids, plot_keys) in PROBES.items():
        actual = baselines[n]
        metrics = {m.id: m for m in actual.metrics}
        assert set(metric_ids) <= set(metrics), (domain, set(metric_ids) - set(metrics))
        assert set(plot_keys) <= set(actual.plots)
        probes.append(
            {
                "assessment": domain,
                "number": n,
                "metrics": [
                    {"id": k, "value": metrics[k].value, "unit": metrics[k].unit}
                    for k in metric_ids
                ],
                "plot_keys": plot_keys,
                "status": "passed",
            }
        )
    assert len(comparisons) == 417 and len(bindings) == 84 and len(probes) == 10
    result = {
        "batch": "ELP-DSP-AGGREGATE-QUALITY-01",
        "baseline": registry["baseline"],
        "validation_level": "independent_synthetic_numerical_and_authored_assessment_binding",
        "comparisons": comparisons,
        "checkpoint_bindings": bindings,
        "cumulative_probes": probes,
        "formative_checkpoints": 84,
        "cumulative_assessments": 10,
        "learner_validation": "not_run",
        "manual_screen_reader": "not_run",
        "matlab_hardware_production": "not_run",
        "other_curricula_remaining_findings": 60,
        "browser_container": "pending",
    }
    (ROOT / "docs/course-quality/dsp-aggregate-review.json").write_text(
        json.dumps(result, indent=2) + "\n"
    )
    print(
        "417 independent comparisons, 84 checkpoint bindings and 10 cumulative probes passed"
    )


if __name__ == "__main__":
    replay()
