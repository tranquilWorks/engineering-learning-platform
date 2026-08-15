import time
from pathlib import Path

import pytest
from fixture_course import module_manifest, write_course

from elp_api.catalog import CatalogError, CourseCatalog
from elp_api.runtime import ExperimentRuntime, RuntimeContractError, RuntimeTimeout


@pytest.fixture
def runtime() -> ExperimentRuntime:
    root = Path(__file__).resolve().parents[3]
    return ExperimentRuntime(CourseCatalog([root / "courses"]))


def test_echo_delay_baseline(runtime: ExperimentRuntime) -> None:
    result = runtime.run("demo-radar", "30-measure-range-from-echo-delay", {})
    metrics = {metric.id: metric for metric in result.metrics}
    assert metrics["true_range"].value == pytest.approx(902.001, rel=2e-3)
    assert metrics["delay_samples"].value == pytest.approx(120.35, rel=1e-6)
    assert metrics["range_bin"].value == pytest.approx(7.4948, rel=2e-3)
    assert {
        "fast_time",
        "correlation",
        "fractional_error",
        "sample_rate_ruler",
    } <= set(result.plots)


def test_broken_geometry_is_exactly_factor_two(runtime: ExperimentRuntime) -> None:
    result = runtime.run(
        "demo-radar",
        "30-measure-range-from-echo-delay",
        {"broken_formula": True},
    )
    metrics = {metric.id: metric for metric in result.metrics}
    assert metrics["reported_range"].value == pytest.approx(
        2 * metrics["refined_range"].value,
        rel=1e-12,
    )


def test_plotting_showcase_returns_advanced_views(runtime: ExperimentRuntime) -> None:
    result = runtime.run("platform-showcase", "01-plotting-and-data-workbench", {})
    assert {
        "time_domain",
        "spectrum",
        "iq_plane",
        "spectrogram",
        "response_surface",
        "polar_pattern",
    } <= set(result.plots)
    assert "spectral_peaks" in result.tables
    assert result.tables["spectral_peaks"].rows


def test_runtime_rejects_unknown_and_out_of_range_parameters(runtime: ExperimentRuntime) -> None:
    with pytest.raises(RuntimeContractError, match="unknown parameters"):
        runtime.run("demo-radar", "30-measure-range-from-echo-delay", {"not_a_control": 1})
    with pytest.raises(RuntimeContractError, match="outside"):
        runtime.run("demo-radar", "30-measure-range-from-echo-delay", {"sample_rate_mhz": 500})
    with pytest.raises(RuntimeContractError, match="boolean"):
        runtime.run("demo-radar", "30-measure-range-from-echo-delay", {"second_target": "yes"})


def _runtime_for(tmp_path: Path, experiment: str, module: dict | None = None) -> ExperimentRuntime:
    write_course(
        tmp_path,
        modules=[
            module
            or module_manifest(
                status="implemented",
                runtime={"kind": "python", "entrypoint": "experiment.py:run"},
                blocks=[],
            )
        ],
        experiment=experiment,
    )
    return ExperimentRuntime(CourseCatalog([tmp_path]))


def test_timeout_returns_bounded_error_and_catalog_recovers(tmp_path: Path) -> None:
    module = module_manifest(
        status="implemented",
        runtime={
            "kind": "python",
            "entrypoint": "experiment.py:run",
            "timeout_seconds": 0.01,
        },
        controls=[{"id": "slow", "type": "toggle", "label": "Slow", "default": False}],
        blocks=[],
    )
    runtime = _runtime_for(
        tmp_path,
        "import time\ndef run(parameters):\n"
        "    if parameters['slow']:\n        time.sleep(0.08)\n"
        "    return {}\n",
        module,
    )
    started = time.monotonic()
    with pytest.raises(RuntimeTimeout, match="exceeded 0.01 seconds"):
        runtime.run("sample-course", "sample-module", {"slow": True})
    assert time.monotonic() - started < 0.06
    assert runtime.catalog.summaries()[0].id == "sample-course"
    time.sleep(0.09)
    assert runtime.catalog.summaries()[0].modules[0].id == "sample-module"


@pytest.mark.parametrize(
    ("returned", "message"),
    [
        ("{'unknown': True}", "extra_forbidden"),
        (
            "{'plots': {'main': {'data': [{'type': 'scatter'}], 'layout': {}, 'unknown': True}}}",
            "extra_forbidden",
        ),
        (
            "{'metrics': ["
            "{'id': 'same', 'label': 'One', 'value': 1}, "
            "{'id': 'same', 'label': 'Two', 'value': 2}]}",
            "metric ids must be unique",
        ),
        (
            "{'tables': {'cases': {'columns': ['a', 'b'], 'rows': [{'a': 1}]}}}",
            "columns must exactly match",
        ),
        ("{'diagnostics': {'bad': float('nan')}}", "non-finite"),
        ("{'diagnostics': {'bad': {1, 2}}}", "unordered sets"),
        ("{'diagnostics': {1: 'bad-key'}}", "string keys"),
    ],
    ids=[
        "envelope-extra",
        "plot-shell-extra",
        "duplicate-metric",
        "incomplete-table-row",
        "non-finite",
        "unordered-set",
        "non-string-key",
    ],
)
def test_malformed_result_boundaries_fail_closed(
    tmp_path: Path, returned: str, message: str
) -> None:
    module = module_manifest(
        status="implemented",
        runtime={"kind": "python", "entrypoint": "experiment.py:run"},
        controls=[{"id": "bad", "type": "toggle", "label": "Bad", "default": False}],
        blocks=[],
    )
    runtime = _runtime_for(
        tmp_path,
        f"def run(parameters):\n"
        f"    if parameters['bad']:\n        return {returned}\n"
        f"    return {{}}\n",
        module,
    )
    with pytest.raises(RuntimeContractError, match=message):
        runtime.run("sample-course", "sample-module", {"bad": True})


def test_invalid_default_result_is_not_promoted_into_catalog(tmp_path: Path) -> None:
    write_course(
        tmp_path,
        modules=[
            module_manifest(
                status="implemented",
                runtime={"kind": "python", "entrypoint": "experiment.py:run"},
                blocks=[],
            )
        ],
        experiment="def run(parameters):\n    return {'unknown': True}\n",
    )
    with pytest.raises(CatalogError, match="default runtime validation failed"):
        CourseCatalog([tmp_path])


def test_result_references_are_revalidated_for_each_parameter_state(
    tmp_path: Path,
) -> None:
    module = module_manifest(
        status="implemented",
        runtime={"kind": "python", "entrypoint": "experiment.py:run"},
        controls=[{"id": "show", "type": "toggle", "label": "Show plot", "default": True}],
        blocks=[{"type": "plot", "plot": "main"}],
    )
    experiment = """def run(parameters):
    plots = {}
    if parameters["show"]:
        plots["main"] = {
            "data": [{"type": "scatter"}],
            "layout": {"title": "Main"},
        }
    return {"plots": plots}
"""
    runtime = _runtime_for(tmp_path, experiment, module)
    assert "main" in runtime.run("sample-course", "sample-module", {}).plots
    with pytest.raises(RuntimeContractError, match="missing plot"):
        runtime.run("sample-course", "sample-module", {"show": False})
