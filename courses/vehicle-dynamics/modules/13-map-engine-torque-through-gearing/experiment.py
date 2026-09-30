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
                "unit": "",
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


NUMBER = 13
PRIMARY = "engine_torque_n_m"
SECONDARY = "gear_ratio"
PRIMARY_RANGE = (80.0, 320.0)
SECONDARY_RANGE = (0.8, 4.2)
FIELDS = [
    "engine_speed_rpm",
    "requested_wheel_force_n",
    "applied_wheel_force_n",
    "traction_limit_n",
    "wheel_power_w",
    "power_residual_w",
    "invalid",
]

P_LABEL, S_LABEL, P_UNIT, S_UNIT = "Requested engine torque", "Gear ratio", "N·m", "1"
P_SWEEP = (
    [
        ("Requested force", "requested_wheel_force_n"),
        ("Applied force", "applied_wheel_force_n"),
    ],
    "Wheel force",
    "N",
)
S_SWEEP = ([("Kinematic engine speed", "engine_speed_rpm")], "Engine speed", "RPM")
COMPARISON_INDICES = [1]
METRICS = [
    ("Engine speed", "engine_speed_rpm", "RPM"),
    ("Applied wheel force", "applied_wheel_force_n", "N"),
    ("Delivered engine torque", "delivered_engine_torque_nm", "N·m"),
    ("Wheel power", "wheel_power_w", "W"),
    ("Declared drivetrain loss", "drivetrain_loss_w", "W"),
    ("Curtailed power request", "curtailed_request_w", "W"),
    ("Power-budget residual", "power_residual_w", "W"),
]
FAULT = "The fault omits the declared 10% drivetrain loss in torque transmission, while keeping the traction cap. The measured power-budget residual exposes this inconsistency."
LIMIT = "This is a fixed-speed algebraic torque map with instantaneous torque curtailment, not an engine/redline-feasibility or tire-slip simulation."


def _state(a, b, broken):
    ratio, radius, speed, limit = b * 4.1, 0.315, 20.0, 1320 * 9.81
    eta = 1.0 if broken else 0.9
    omega = speed / radius * ratio
    requested = a * ratio * eta / radius
    applied = min(requested, limit)
    delivered_torque = min(a, limit * radius / (ratio * eta))
    requested_power, delivered_power = a * omega, delivered_torque * omega
    wheel = applied * speed
    loss = 0.1 * delivered_power
    residual = wheel + loss - delivered_power
    values = [
        omega * 60 / (2 * math.pi),
        requested,
        applied,
        limit,
        wheel,
        residual,
        float(abs(residual) > 1e-8),
    ]
    return _finish(
        values,
        engine_angular_speed_rad_s=omega,
        wheel_angular_speed_rad_s=speed / radius,
        delivered_engine_torque_nm=delivered_torque,
        requested_engine_power_w=requested_power,
        delivered_engine_power_w=delivered_power,
        drivetrain_loss_w=loss,
        curtailed_request_w=requested_power - delivered_power,
        transmitted_efficiency=eta,
        traction_limited=float(requested > limit),
    )


def _response(a, b, broken):
    xs = _linspace(0.8, 4.2, 61)
    states = [_state(a, g, broken) for g in xs]
    return {
        "x": xs,
        "series": [
            [s[k] for s in states]
            for k in [
                "requested_wheel_force_n",
                "applied_wheel_force_n",
                "traction_limit_n",
            ]
        ],
        "names": [
            "Modeled wheel-force request",
            "Applied wheel force",
            "Traction capacity",
        ],
        "x_quantity": "Gear ratio",
        "x_unit": "1",
        "y_quantity": "Wheel force",
        "y_unit": "N",
    }


def _interpret(s):
    return (
        f"Applied force is {s['applied_wheel_force_n']:.6g} N at {s['engine_speed_rpm']:.6g} RPM. "
        f"Delivered shaft power {s['delivered_engine_power_w']:.6g} W, wheel power {s['wheel_power_w']:.6g} W and declared loss {s['drivetrain_loss_w']:.6g} W give residual {s['power_residual_w']:.6g} W. "
        f"The curtailed request is {s['curtailed_request_w']:.6g} W; it is not drivetrain heat."
    )
