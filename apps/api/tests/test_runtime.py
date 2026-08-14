from pathlib import Path

import pytest

from elp_api.catalog import CourseCatalog
from elp_api.runtime import ExperimentRuntime


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
    from elp_api.runtime import RuntimeContractError

    with pytest.raises(RuntimeContractError, match="unknown parameters"):
        runtime.run("demo-radar", "30-measure-range-from-echo-delay", {"not_a_control": 1})
    with pytest.raises(RuntimeContractError, match="outside"):
        runtime.run("demo-radar", "30-measure-range-from-echo-delay", {"sample_rate_mhz": 500})
    with pytest.raises(RuntimeContractError, match="boolean"):
        runtime.run("demo-radar", "30-measure-range-from-echo-delay", {"second_target": "yes"})
