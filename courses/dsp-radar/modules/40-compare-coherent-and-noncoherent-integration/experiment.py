from __future__ import annotations

from typing import Any

import numpy as np

SEED = 4001
ITEM_NUMBER = 40
PHASE = 4
MAX_POINTS = 512


def _layout(title: str, x_label: str, y_label: str) -> dict[str, Any]:
    return {
        "title": {"text": title, "x": 0.02, "xanchor": "left"},
        "margin": {"l": 68, "r": 22, "t": 58, "b": 58},
        "xaxis": {"title": x_label, "showgrid": True},
        "yaxis": {"title": y_label, "showgrid": True},
        "legend": {"orientation": "h", "y": 1.14},
        "hovermode": "closest",
        "uirevision": "keep-view",
    }


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    primary = float(parameters["primary_scale"])
    secondary = float(parameters["secondary_scale"])
    noise_db = float(parameters["noise_db"])
    broken_mode = bool(parameters["broken_mode"])
    count = 192 + 16 * (ITEM_NUMBER % 4)
    if count > MAX_POINTS:
        raise ValueError("experiment exceeds the retained point ceiling")
    rng = np.random.default_rng(SEED)
    x = np.linspace(0.0, 1.0, count, endpoint=False)
    variant = 1.0 + (ITEM_NUMBER % 7) / 5.0
    noise_scale = 10.0 ** (noise_db / 20.0)

    if PHASE == 1:
        truth = np.cos(2.0 * np.pi * variant * primary * x + 0.4 * secondary)
        measured = truth + noise_scale * rng.standard_normal(count)
        response_axis = np.fft.rfftfreq(count, d=1.0 / count)
        response = np.abs(np.fft.rfft(measured)) / count
        broken_response = np.roll(measured, count // 7) if broken_mode else measured
    elif PHASE == 2:
        tone = np.exp(1j * (2.0 * np.pi * (8.0 + variant * primary) * x + secondary))
        measured = tone + noise_scale * (rng.standard_normal(count) + 1j * rng.standard_normal(count))
        response_axis = np.fft.fftshift(np.fft.fftfreq(count, d=1.0 / count))
        response = np.abs(np.fft.fftshift(np.fft.fft(measured))) / count
        broken_response = np.abs(measured.real) if broken_mode else np.abs(measured)
        truth = tone.real
    elif PHASE == 3:
        symbols = np.sign(np.sin(2.0 * np.pi * (4.0 + variant) * x))
        carrier = np.cos(2.0 * np.pi * (18.0 + 2.0 * primary) * x + secondary)
        truth = symbols * carrier
        measured = truth + noise_scale * rng.standard_normal(count)
        response_axis = np.fft.rfftfreq(count, d=1.0 / count)
        response = np.abs(np.fft.rfft(measured)) / count
        broken_response = np.roll(measured, int(2 + 10 * secondary)) if broken_mode else measured
    elif PHASE == 4:
        bins = np.arange(count, dtype=float)
        center = count * (0.25 + 0.25 * (primary - 0.5))
        width = 2.0 + 4.0 * secondary
        truth = np.exp(-0.5 * ((bins - center) / width) ** 2)
        measured = truth + noise_scale * rng.standard_normal(count)
        response_axis = bins
        response = np.abs(np.fft.fftshift(np.fft.fft(measured))) / np.sqrt(count)
        broken_response = np.roll(measured, count // 3) if broken_mode else measured
        x = bins
    elif PHASE == 5:
        cells = np.arange(count, dtype=float)
        background = 0.2 + (0.45 * secondary) * (cells >= count // 2)
        power = background + np.abs(noise_scale * rng.standard_normal(count))
        target_bin = int(count * (0.3 + 0.25 * (primary - 0.5)))
        power[target_bin] += 1.4
        truth = power
        measured = power
        response_axis = cells
        response = np.full(count, np.quantile(power, 0.82 + 0.1 * secondary))
        if broken_mode:
            response = np.full(count, np.mean(power) * (1.2 + primary))
        broken_response = response
        x = cells
    elif PHASE == 6:
        steps = np.arange(count, dtype=float)
        truth = 0.04 * steps + 0.0002 * variant * secondary * steps**2
        measured = truth + noise_scale * 8.0 * rng.standard_normal(count)
        gain = np.clip(0.12 + 0.5 * primary, 0.05, 0.95)
        response = np.empty(count)
        response[0] = measured[0]
        for index in range(1, count):
            response[index] = response[index - 1] + gain * (measured[index] - response[index - 1])
        response_axis = steps
        broken_response = np.roll(response, 12) if broken_mode else response
        x = steps
    elif PHASE == 7:
        angles = np.linspace(-90.0, 90.0, count)
        u = np.sin(np.deg2rad(angles)) - np.sin(np.deg2rad(45.0 * (primary - 1.0)))
        spacing = 0.45 + 0.45 * secondary
        elements = 6 + ITEM_NUMBER % 7
        denominator = np.sin(np.pi * spacing * u)
        numerator = np.sin(elements * np.pi * spacing * u)
        response = np.where(np.abs(denominator) < 1e-10, 1.0, np.abs(numerator / (elements * denominator)))
        truth = response
        measured = np.maximum(response + noise_scale * rng.standard_normal(count), 0.0)
        response_axis = angles
        broken_response = np.roll(response, 9) if broken_mode else response
        x = angles
    elif PHASE == 8:
        bins = np.arange(count, dtype=float)
        beat_bin = count * (0.15 + 0.35 * (primary - 0.5))
        truth = np.cos(2.0 * np.pi * beat_bin * bins / count + secondary)
        measured = truth + noise_scale * rng.standard_normal(count)
        response_axis = np.fft.rfftfreq(count, d=1.0 / count)
        response = np.abs(np.fft.rfft(measured)) / count
        broken_response = np.roll(measured, int(8 + 16 * secondary)) if broken_mode else measured
        x = bins
    else:
        coordinate = np.linspace(-1.0, 1.0, count)
        width = 0.05 + 0.16 / primary
        truth = np.exp(-0.5 * ((coordinate + 0.25) / width) ** 2) + 0.65 * np.exp(-0.5 * ((coordinate - 0.3) / (1.4 * width)) ** 2)
        measured = truth + noise_scale * rng.standard_normal(count)
        kernel = np.ones(3 + 2 * int(secondary * 5))
        kernel /= kernel.sum()
        response = np.convolve(measured, kernel, mode="same")
        response_axis = coordinate
        broken_response = np.roll(response, 18) + 0.25 * np.roll(response, -13) if broken_mode else response
        x = coordinate

    displayed = broken_response if broken_mode else measured
    separation = float(np.max(response) - np.median(response))
    rmse = float(np.sqrt(np.mean((np.asarray(displayed).real - np.asarray(truth).real) ** 2)))
    signature = [float(count), primary, secondary, noise_db, float(np.mean(np.asarray(displayed).real)), float(np.std(np.asarray(displayed).real)), separation, rmse]
    sweep_primary = [0.6, 1.0, 1.4]
    sweep_secondary = [0.0, 0.5, 1.0]
    sweep_response = [variant * value for value in sweep_primary]
    stress_response = [separation / (1.0 + value) for value in sweep_secondary]
    title = 'Compare Coherent and Noncoherent Integration'

    return {
        "metrics": [
            {"id": "primary", "label": 'Pulse Count', "value": primary, "unit": "× baseline", "emphasis": "primary"},
            {"id": "response_separation", "label": "Response separation", "value": separation, "unit": "normalized"},
            {"id": "model_error", "label": "Model/display error", "value": rmse, "unit": "normalized"},
            {"id": "points", "label": "Bounded points", "value": count, "unit": "points"},
        ],
        "plots": {
            "model_view": {"data": [
                {"type": "scatter", "mode": "lines", "name": "physical/model truth", "x": x, "y": np.asarray(truth).real},
                {"type": "scatter", "mode": "lines", "name": "measured/processed", "x": x, "y": np.asarray(displayed).real},
            ], "layout": _layout(title + " — model view", 'range bin', 'normalized response'), "config": {"responsive": True, "displaylogo": False}},
            "response_view": {"data": [
                {"type": "scatter", "mode": "lines", "name": "response", "x": response_axis, "y": np.asarray(response).real},
            ], "layout": _layout(title + " — response view", 'range bin', 'normalized response'), "config": {"responsive": True, "displaylogo": False}},
            "parameter_sweeps": {"data": [
                {"type": "scatter", "mode": "lines+markers", "name": "primary scale", "x": sweep_primary, "y": sweep_response},
                {"type": "scatter", "mode": "lines+markers", "name": "secondary stress", "x": sweep_secondary, "y": stress_response},
            ], "layout": _layout("Two one-variable sweeps", "control value", "response statistic"), "config": {"responsive": True, "displaylogo": False}},
            "broken_case": {"data": [
                {"type": "scatter", "mode": "lines", "name": "recovered", "x": x, "y": np.asarray(measured).real},
                {"type": "scatter", "mode": "lines", "name": "broken" if broken_mode else "enable broken mode", "x": x, "y": np.asarray(broken_response).real},
            ], "layout": _layout("Intentional assumption failure", 'range bin', 'normalized response'), "config": {"responsive": True, "displaylogo": False}},
        },
        "explanations": {
            "observation": f"The {title} model uses a bounded deterministic pulse-radar processing experiment. Primary scale={primary:.2f} and secondary stress={secondary:.2f} remain independently controllable.",
            "broken": "Broken mode deliberately violates the lesson's central interpretation assumption so the displayed response becomes ambiguous, biased, contaminated, or defocused.",
            "recovery": "Disable broken mode, restore both scales to 1.0 and 0.25, then connect the recovered shape to the pinned source equations before changing one control at a time.",
        },
        "diagnostics": {"seed": SEED, "item_number": ITEM_NUMBER, "point_count": count, "signature": signature, "broken_active": broken_mode},
    }
