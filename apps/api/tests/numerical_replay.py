"""Test-only fixture portability; independent scientific gates remain mandatory."""

from collections.abc import Mapping, Sequence
from numbers import Real

import numpy as np
import pytest


def _tolerances(tolerance: Mapping[str, float]) -> tuple[float, float]:
    values = (tolerance["absolute"], tolerance["relative"])
    assert all(
        isinstance(value, Real)
        and not isinstance(value, bool)
        and np.isfinite(value)
        and value >= 0
        for value in values
    ), "invalid scientific tolerance"
    return values


def _signature(values: Sequence[float]) -> np.ndarray:
    array = np.asarray(values)
    assert array.ndim == 1 and array.size, "signature must be a nonempty vector"
    assert array.dtype.kind in "iuf", "signature must contain real numbers"
    assert all(
        isinstance(value, Real) and not isinstance(value, (bool, np.bool_)) for value in values
    ), "signature must contain real numbers"
    array = array.astype(float)
    assert np.all(np.isfinite(array)), "signature must be finite"
    return array


def _pair(reference: Sequence[float], actual: Sequence[float]) -> tuple[np.ndarray, np.ndarray]:
    left, right = _signature(reference), _signature(actual)
    assert left.shape == right.shape, "signature shape mismatch"
    return left, right


def assert_replay(
    live: Sequence[float], saved: Sequence[float], tolerance: Mapping[str, float]
) -> None:
    """Cap each difference by roundoff AND 1% of its scientific budget."""
    absolute, relative = _tolerances(tolerance)
    saved_values, live_values = _pair(saved, live)
    budget = np.minimum(
        1e-9 * np.maximum(1.0, np.abs(saved_values)),
        0.01 * np.maximum(absolute, relative * np.abs(saved_values)),
    )
    difference = np.abs(live_values - saved_values)
    assert np.all(difference <= budget), f"fixture replay drift: {difference=} exceeds {budget=}"


def comparison_metrics(
    reference: Sequence[float], actual: Sequence[float], tolerance: Mapping[str, float]
) -> dict[str, float]:
    """Preserve the original GNC comparison definitions exactly."""
    absolute, relative = _tolerances(tolerance)
    expected, produced = _pair(reference, actual)
    difference = np.abs(expected - produced)
    scale = float(max(np.max(np.abs(expected)), np.max(np.abs(produced)), 1.0))
    return {
        "comparison_scale": scale,
        "allowed_absolute_error": max(absolute, relative * scale),
        "max_absolute_error": float(np.max(difference)),
        "max_relative_error": float(
            np.max(
                difference
                / np.maximum.reduce([np.abs(expected), np.abs(produced), np.ones_like(difference)])
            )
        ),
    }


def assert_recorded_metrics(
    saved_reference: Sequence[float], saved_actual: Sequence[float], case: Mapping
) -> None:
    metrics = comparison_metrics(saved_reference, saved_actual, case["tolerance"])
    for key, value in metrics.items():
        assert value == pytest.approx(case[key], abs=1e-15, rel=1e-15), key


def assert_scientific_comparison(
    reference: Sequence[float], actual: Sequence[float], tolerance: Mapping[str, float]
) -> None:
    metrics = comparison_metrics(reference, actual, tolerance)
    assert metrics["max_absolute_error"] <= metrics["allowed_absolute_error"]
    assert metrics["max_relative_error"] <= tolerance["relative"]
