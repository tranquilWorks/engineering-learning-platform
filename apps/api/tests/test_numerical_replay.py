import numpy as np
import pytest
from numerical_replay import (
    assert_recorded_metrics,
    assert_replay,
    assert_scientific_comparison,
    comparison_metrics,
)

TOLERANCE = {"absolute": 1e-6, "relative": 1e-6}


def test_roundoff_replay_preserves_each_component() -> None:
    assert_replay([1 + 1e-10, 1e8 + 0.01, 1e-12], [1, 1e8, 0], TOLERANCE)
    assert_replay([1, 0], [1, 0], {"absolute": 0, "relative": 0})


@pytest.mark.parametrize(
    "live,saved,tolerance",
    [
        ([1 + 1e-7], [1], TOLERANCE),  # scientifically close, but not fixture replay
        ([1e8, 1e-5], [1e8, 0], TOLERANCE),  # no vector-global hiding
        ([1e-13], [0], {"absolute": 1e-12, "relative": 0}),  # 1% ceiling
        ([1e-12], [0], {"absolute": 0, "relative": 1e-6}),  # zero component budget
        ([1e-12], [0], {"absolute": 0, "relative": 0}),
        ([2, 1], [1, 2], TOLERANCE),  # order matters
        ([1], [1, 2], TOLERANCE),
        ([[1, 2]], [1, 2], TOLERANCE),
        ([], [], TOLERANCE),
        ([1], [[1]], TOLERANCE),
        ([float("nan")], [1], TOLERANCE),
        ([1], [float("nan")], TOLERANCE),
        ([float("inf")], [1], TOLERANCE),
        ([1], [float("-inf")], TOLERANCE),
        (["1"], [1], TOLERANCE),
        ([True], [1], TOLERANCE),
        ([True, 2.0], [1, 2], TOLERANCE),
        ([1j], [1], TOLERANCE),
        (1, [1], TOLERANCE),
    ],
)
def test_invalid_or_changed_replay_is_rejected(live, saved, tolerance) -> None:
    with pytest.raises(AssertionError):
        assert_replay(live, saved, tolerance)


@pytest.mark.parametrize("field", ["absolute", "relative"])
@pytest.mark.parametrize("value", [-1, float("nan"), float("inf"), "1e-6", True, None])
def test_invalid_tolerance_is_rejected(field, value) -> None:
    with pytest.raises(AssertionError, match="invalid scientific tolerance"):
        assert_replay([1], [1], {**TOLERANCE, field: value})


@pytest.mark.parametrize(
    "key",
    [
        "comparison_scale",
        "allowed_absolute_error",
        "max_absolute_error",
        "max_relative_error",
    ],
)
def test_saved_metadata_corruption_is_detected(key) -> None:
    # Simple exactly representable values give an independently known record.
    tolerance = {"absolute": 0.25, "relative": 0.25}
    case = {
        "tolerance": tolerance,
        "comparison_scale": 2.0,
        "allowed_absolute_error": 0.5,
        "max_absolute_error": 0.25,
        "max_relative_error": 0.125,
    }
    assert_recorded_metrics([2, 0], [1.75, 0], case)
    with pytest.raises(AssertionError, match=key):
        assert_recorded_metrics([2, 0], [1.75, 0], {**case, key: case[key] + 1e-8})


def test_live_error_need_not_equal_historical_error() -> None:
    case = {"tolerance": TOLERANCE, **comparison_metrics([1], [1], TOLERANCE)}
    assert_recorded_metrics([1], [1], case)
    assert_replay([1 + 1e-10], [1], TOLERANCE)
    assert_scientific_comparison([1], [1 + 1e-10], TOLERANCE)


def test_replay_does_not_rescue_failed_scientific_comparison() -> None:
    saved = [1e-6]
    live = [1e-6 + 1e-12]
    assert_scientific_comparison([0], saved, TOLERANCE)
    assert_replay(live, saved, TOLERANCE)
    with pytest.raises(AssertionError):
        assert_scientific_comparison([0], live, TOLERANCE)


def test_original_relative_gate_still_rejects_small_component_error() -> None:
    with pytest.raises(AssertionError):
        assert_scientific_comparison([1e8, 0], [1e8, 1e-5], TOLERANCE)


def test_numpy_real_signature_is_supported() -> None:
    assert_replay(np.array([1.0, 2.0]), np.array([1, 2]), TOLERANCE)
