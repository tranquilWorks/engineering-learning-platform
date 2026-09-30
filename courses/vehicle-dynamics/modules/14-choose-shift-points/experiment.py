from __future__ import annotations

import math
from typing import Any


def _linspace(lo, hi, count):
    return [lo + (hi - lo) * i / (count - 1) for i in range(count)]


def _trace(name, x, y, xq, xu, yq, yu, mode="lines", color=None):
    trace = {
        "type": "scatter",
        "mode": mode,
        "name": name,
        "x": x,
        "y": y,
        "meta": {"x_quantity": xq, "x_unit": xu, "y_quantity": yq, "y_unit": yu},
    }
    if color:
        trace["line"] = {"color": color}
    return trace


def _wrap_label(text, width=24):
    lines = []
    current = ""
    for word in text.split():
        if current and len(current) + len(word) + 1 > width:
            lines.append(current)
            current = word
        else:
            current = (current + " " + word).strip()
    return "<br>".join(lines + [current])


def _plot(title, traces, xq, xu, yq, yu, equal=False):
    for trace in traces:
        trace["name"] = _wrap_label(trace["name"], 28)
    bottom = 105 + len(traces) * 30
    layout = {
        "title": {"text": _wrap_label(title), "font": {"size": 13}},
        "xaxis": {
            "title": {"text": _wrap_label(f"{xq} ({xu})"), "font": {"size": 11}},
            "automargin": True,
        },
        "yaxis": {
            "title": {"text": _wrap_label(f"{yq} ({yu})"), "font": {"size": 11}},
            "automargin": True,
        },
        "uirevision": "vehicle-quality",
        "margin": {"l": 78, "r": 24, "t": 62, "b": bottom},
        "legend": {
            "orientation": "v",
            "y": -0.38,
            "x": 0,
            "yanchor": "top",
            "font": {"size": 10},
        },
        "height": 310 + bottom,
    }
    if equal:
        layout["yaxis"].update(scaleanchor="x", scaleratio=1)
    return {
        "data": traces,
        "layout": layout,
        "config": {"responsive": True, "displaylogo": False},
    }


def _model(a, b, broken):
    return _state(a, b, broken)["signature"]


def _finish(values, **extra):
    state = dict(zip(FIELDS, values, strict=True))
    state.update(extra)
    state["signature"] = values
    return state


def _sweep(a, b, primary):
    bounds = PRIMARY_RANGE if primary else SECONDARY_RANGE
    chosen = a if primary else b
    xs = sorted(set(_linspace(*bounds, 61) + [chosen]))
    states = [_state(x, b, False) if primary else _state(a, x, False) for x in xs]
    if NUMBER == 14:
        pairs = [(x, s) for x, s in zip(xs, states) if s["decision_available"]]
        xs, states = [p[0] for p in pairs], [p[1] for p in pairs]
    fields, quantity, unit = P_SWEEP if primary else S_SWEEP
    return {
        "x": xs,
        "series": [[s[field] for s in states] for label, field in fields],
        "names": [label for label, field in fields],
        "x_quantity": P_LABEL if primary else S_LABEL,
        "x_unit": P_UNIT if primary else S_UNIT,
        "y_quantity": quantity,
        "y_unit": unit,
    }


def _as_plot(title, response):
    xq, xu, yq, yu = [
        response[k] for k in ("x_quantity", "x_unit", "y_quantity", "y_unit")
    ]
    traces = [
        _trace(name, response["x"], ys, xq, xu, yq, yu)
        for name, ys in zip(response["names"], response["series"], strict=True)
    ]
    return _plot(title, traces, xq, xu, yq, yu)


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    a, b = float(parameters[PRIMARY]), float(parameters[SECONDARY])
    broken = bool(parameters["broken_mode"])
    for name, value, bounds in [
        (PRIMARY, a, PRIMARY_RANGE),
        (SECONDARY, b, SECONDARY_RANGE),
    ]:
        if not math.isfinite(value) or not bounds[0] <= value <= bounds[1]:
            raise ValueError(f"{name} outside declared finite range")
    state = _state(a, b, broken)
    if not all(math.isfinite(v) for v in state["signature"]):
        raise ValueError("non-finite physical signature")
    response = _response(a, b, broken)
    ps, ss = _sweep(a, b, True), _sweep(a, b, False)
    good, bad = _response(a, b, False), _response(a, b, True)
    comparison = {
        k: good[k] for k in ("x", "x_quantity", "x_unit", "y_quantity", "y_unit")
    }
    if NUMBER == 15:
        comparison.update(
            y_quantity="Rotor temperature rise",
            y_unit="°C",
            names=["Nominal heat partition", "Fault: rotor heat counted twice"],
            series=[good["rotor_temperature_rise_c"], bad["rotor_temperature_rise_c"]],
        )
    else:
        comparison["names"] = [
            prefix + r["names"][i]
            for prefix, r in [("Nominal: ", good), ("Fault: ", bad)]
            for i in COMPARISON_INDICES
        ]
        comparison["series"] = [
            r["series"][i] for r in [good, bad] for i in COMPARISON_INDICES
        ]
    metrics = [
        {"id": "input_primary", "label": P_LABEL, "value": a, "unit": P_UNIT},
        {"id": "input_secondary", "label": S_LABEL, "value": b, "unit": S_UNIT},
    ]
    for i, (label, field, unit) in enumerate(METRICS):
        value = state[field]
        if NUMBER == 14 and field in FIELDS[:-1] and not state["decision_available"]:
            value = "Unavailable"
        metrics.append(
            {"id": f"physical_{i}", "label": label, "value": value, "unit": unit}
        )
    if NUMBER == 14:
        label = (
            "Unavailable"
            if not state["decision_available"]
            else "Force crossover"
            if state["crossover"]
            else "Redline limited"
        )
        metrics.append(
            {
                "id": "decision_kind",
                "label": "Shift decision",
                "value": label,
                "unit": "status",
            }
        )
    metrics.append(
        {
            "id": "valid",
            "label": "Declared model checks satisfied",
            "value": not bool(state["invalid"]),
            "unit": "boolean",
        }
    )
    return {
        "metrics": metrics,
        "plots": {
            "response": _as_plot("Selected physical response", response),
            "primary_sweep": _as_plot("Vary " + P_LABEL, ps),
            "secondary_sweep": _as_plot("Vary " + S_LABEL, ss),
            "broken_recovery": _as_plot("Same-input fault comparison", comparison),
        },
        "explanations": {
            "observation": f"{P_LABEL}={a:g} {P_UNIT}; {S_LABEL}={b:g} {S_UNIT}. "
            + _interpret(state)
            + " "
            + LIMIT,
            "broken": FAULT
            + " The comparison uses the same selected inputs; the sweep panels retain the nominal model.",
            "recovery": "Disable the fault without moving either input to restore the declared model. Use Reset parameters separately to reproduce the worked baseline.",
        },
        "diagnostics": {
            "item_id": f"P{NUMBER:02d}",
            "signature": state["signature"],
            "fields": FIELDS,
            "broken_active": broken,
            "physical": state,
            "response": response,
            "primary_sweep": ps,
            "secondary_sweep": ss,
        },
    }


NUMBER = 14
PRIMARY = "current_gear_ratio"
SECONDARY = "next_gear_ratio"
PRIMARY_RANGE = (1.4, 3.7)
SECONDARY_RANGE = (0.8, 2.4)
FIELDS = [
    "shift_rpm",
    "shift_speed_m_s",
    "current_force_n",
    "next_force_n",
    "post_shift_rpm",
    "force_gap_n",
    "invalid",
]

P_LABEL, S_LABEL, P_UNIT, S_UNIT = "Current gear ratio", "Next gear ratio", "1", "1"
P_SWEEP = S_SWEEP = (
    [("Available nominal decision", "shift_rpm")],
    "Decision engine speed",
    "RPM",
)
COMPARISON_INDICES = [1]
METRICS = [
    ("Decision engine speed", "shift_rpm", "RPM"),
    ("Decision road speed", "shift_speed_m_s", "m/s"),
    ("Post-shift engine speed", "post_shift_rpm", "RPM"),
    ("Current-gear force", "current_force_n", "N"),
    ("Next-gear force", "next_force_n", "N"),
    ("Decision force gap", "force_gap_n", "N"),
    ("Maximum torque-lookup force error", "maximum_lookup_force_error_n", "N"),
]
FAULT = "The fault evaluates next-gear torque at the current RPM instead of the lower post-shift RPM. Kinematic post-shift RPM is still computed correctly; a curve-wide force residual detects the wrong torque lookup."
LIMIT = "Equal or ascending ratios have no available upshift decision. Their curves are formal comparisons only. The empirical torque map omits shift time, traction and engine transients."


def _torque(rpm):
    return max(120.0, 245.0 - 0.000006 * (rpm - 5000.0) ** 2)


def _forces(a, b, rpm, broken):
    post = rpm * b / a
    current = _torque(rpm) * a * 4.1 * 0.9 / 0.315
    nxt = _torque(rpm if broken else post) * b * 4.1 * 0.9 / 0.315
    return current, nxt, post


def _state(a, b, broken):
    available = b < a
    q = b / a

    # Dividing the nominal force gap by a*(1-q) avoids cancellation near q=1.
    def gap(r):
        return -95.0 - 0.06 * (1 + q) * r + 0.000006 * (1 + q + q * q) * r * r

    crossover = available and not broken and gap(7400.0) >= 0
    rpm = 7400.0
    if crossover:
        lo, hi = 2500.0, 7400.0
        for _ in range(64):
            mid = (lo + hi) / 2
            if gap(mid) < 0:
                lo = mid
            else:
                hi = mid
        rpm = (lo + hi) / 2
    error = max(
        abs(_forces(a, b, r, broken)[1] - _forces(a, b, r, False)[1])
        for r in _linspace(2500.0, 7400.0, 121)
    )
    red_current, red_next, _ = _forces(a, b, 7400.0, broken)
    if available:
        current, nxt, post = _forces(a, b, rpm, broken)
        speed = rpm * 2 * math.pi / 60 * 0.315 / (a * 4.1)
        values = [rpm, speed, current, nxt, post, nxt - current, float(error > 1e-10)]
    else:
        # Only serialization sentinels; never rendered as physical decision values.
        values = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]
    return _finish(
        values,
        decision_available=float(available),
        crossover=float(crossover),
        redline_limited=float(available and not crossover),
        gear_speed_ratio=q,
        maximum_lookup_force_error_n=error,
        redline_current_force_n=red_current,
        redline_next_force_n=red_next,
    )


def _response(a, b, broken):
    xs = _linspace(2500.0, 7400.0, 121)
    forces = [_forces(a, b, r, broken) for r in xs]
    return {
        "x": xs,
        "series": [[f[0] for f in forces], [f[1] for f in forces]],
        "post_shift_rpm": [f[2] for f in forces],
        "next_torque_lookup_rpm": [r if broken else f[2] for r, f in zip(xs, forces)],
        "names": ["Current-gear wheel force", "Next-gear wheel force"],
        "x_quantity": "Current engine speed",
        "x_unit": "RPM",
        "y_quantity": "Wheel force",
        "y_unit": "N",
    }


def _interpret(s):
    if not s["decision_available"]:
        return "No upshift decision is available because next ratio must be strictly smaller. The main and fault-comparison panels show formal force curves; nominal sweep panels omit invalid ratios."
    kind = (
        "force crossover"
        if s["crossover"]
        else "redline-limited decision, not a force crossover"
    )
    return (
        f"This is a {kind} at {s['shift_rpm']:.9g} RPM. The next-minus-current force gap is {s['force_gap_n']:.6g} N, "
        f"and post-shift speed is {s['post_shift_rpm']:.6g} RPM. The maximum lookup error across the displayed force curve is {s['maximum_lookup_force_error_n']:.6g} N."
    )
