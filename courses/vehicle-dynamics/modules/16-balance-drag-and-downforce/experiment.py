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


NUMBER = 16
PRIMARY = "speed_m_s"
SECONDARY = "wing_angle_deg"
PRIMARY_RANGE = (10.0, 70.0)
SECONDARY_RANGE = (0.0, 18.0)
FIELDS = [
    "dynamic_pressure_pa",
    "drag_n",
    "downforce_n",
    "tire_capacity_n",
    "drag_power_w",
    "front_aero_share",
    "invalid",
]

P_LABEL, S_LABEL, P_UNIT, S_UNIT = "Vehicle speed", "Wing angle", "m/s", "deg"
P_SWEEP = ([("Nominal drag power", "drag_power_w")], "Drag power demand", "W")
S_SWEEP = ([("Drag", "drag_n"), ("Downforce", "downforce_n")], "Aerodynamic force", "N")
COMPARISON_INDICES = [0, 3]
METRICS = [
    ("Dynamic pressure", "dynamic_pressure_pa", "Pa"),
    ("Drag resistance", "drag_n", "N"),
    ("Total downforce", "downforce_n", "N"),
    ("Drag power demand", "drag_power_w", "W"),
    ("Front aero contribution", "front_aero_n", "N"),
    ("Rear aero contribution", "rear_aero_n", "N"),
    ("Rear total normal load", "rear_normal_n", "N"),
    ("Constant-mu tire capacity", "tire_capacity_n", "N"),
]
FAULT = "The fault reverses drag resistance and assigns 120% of total downforce to the front axle. The remaining rear aero contribution becomes negative, violating the declared downward-allocation convention."
LIMIT = "These empirical coefficients and constant-mu capacity are not measured aero, tire-load-sensitivity or a full handling model. A negative aero contribution is distinct from a negative total wheel load."


def _state(a, b, broken):
    pressure = 0.5 * 1.225 * a * a
    weight = 1320 * 9.81
    cda = 0.65 + 0.0015 * b * b
    cla = 0.30 + 0.045 * b
    drag = pressure * cda * (-1 if broken else 1)
    down = pressure * cla
    share = 1.2 if broken else 0.48 + 0.006 * b
    front = share * down
    rear = (1 - share) * down
    front_normal = 0.53 * weight + front
    rear_normal = 0.47 * weight + rear
    power = drag * a
    capacity = weight + down
    values = [
        pressure,
        drag,
        down,
        capacity,
        power,
        share,
        float(drag < 0 or not 0 <= share <= 1),
    ]
    return _finish(
        values,
        drag_area_m2=cda,
        downforce_area_m2=cla,
        front_aero_n=front,
        rear_aero_n=rear,
        front_normal_n=front_normal,
        rear_normal_n=rear_normal,
        aero_allocation_residual_n=front + rear - down,
        normal_load_residual_n=front_normal + rear_normal - capacity,
        drag_model_residual_n=drag - pressure * cda,
    )


def _response(a, b, broken):
    xs = _linspace(10.0, 70.0, 61)
    states = [_state(v, b, broken) for v in xs]
    return {
        "x": xs,
        "series": [
            [s[k] for s in states]
            for k in ["drag_n", "downforce_n", "front_aero_n", "rear_aero_n"]
        ],
        "names": [
            "Drag resistance",
            "Total downforce",
            "Front aero contribution",
            "Rear aero contribution",
        ],
        "x_quantity": "Vehicle speed",
        "x_unit": "m/s",
        "y_quantity": "Aerodynamic force",
        "y_unit": "N",
    }


def _interpret(s):
    return (
        f"Drag is {s['drag_n']:.6g} N and demands {s['drag_power_w']:.6g} W. "
        f"Downforce {s['downforce_n']:.6g} N splits into front {s['front_aero_n']:.6g} N and rear {s['rear_aero_n']:.6g} N. "
        f"Rear total normal load remains {s['rear_normal_n']:.6g} N after static weight is included. Check resistance and allocation signs as well as the force sums."
    )
