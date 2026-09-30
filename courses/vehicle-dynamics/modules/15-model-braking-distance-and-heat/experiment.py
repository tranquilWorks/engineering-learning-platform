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
            names=["Nominal heat partition", "Fault: heat double-counted"],
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


NUMBER = 15
PRIMARY = "initial_speed_m_s"
SECONDARY = "requested_brake_force_n"
PRIMARY_RANGE = (5.0, 55.0)
SECONDARY_RANGE = (1000.0, 18000.0)
FIELDS = [
    "applied_brake_force_n",
    "deceleration_m_s2",
    "stopping_distance_m",
    "stop_time_s",
    "kinetic_energy_j",
    "rotor_delta_t_c",
    "front_load_n",
    "rear_load_n",
    "invalid",
]

P_LABEL, S_LABEL, P_UNIT, S_UNIT = "Initial speed", "Requested brake force", "m/s", "N"
P_SWEEP = S_SWEEP = (
    [("Nominal stopping distance", "stopping_distance_m")],
    "Stopping distance",
    "m",
)
COMPARISON_INDICES = [0]
METRICS = [
    ("Applied brake force", "applied_brake_force_n", "N"),
    ("Deceleration magnitude", "deceleration_m_s2", "m/s²"),
    ("Stopping distance", "stopping_distance_m", "m"),
    ("Stop time", "stop_time_s", "s"),
    ("Initial kinetic energy", "kinetic_energy_j", "J"),
    ("Rotor heat", "rotor_heat_j", "J"),
    ("Other heat", "other_heat_j", "J"),
    ("Rotor temperature rise", "rotor_delta_t_c", "°C"),
    ("Heat-budget residual / initial energy", "heat_residual_fraction", "1"),
]
FAULT = "The fault sends 100% of stopping work to the rotors while retaining the other 15% heat allocation. It double counts heat; applied braking force and stopping trajectory are unchanged."
LIMIT = "This constant-force stop omits cooling, brake bias, fade, ABS transients, drag and road grade. Temperature is a bulk rise, not an absolute rotor temperature."


def _state(a, b, broken):
    mass, weight = 1320.0, 1320.0 * 9.81
    cap = 1.05 * weight
    force = min(b, cap)
    decel = force / mass
    distance = a * a / (2 * decel)
    stop = a / decel
    energy = 0.5 * mass * a * a
    work = force * distance
    rotor = (1.0 if broken else 0.85) * work
    other = 0.15 * work
    transfer = force * 0.5 / 2.57
    front = 0.53 * weight + transfer
    rear = weight - front
    heat_residual = (rotor + other - energy) / energy
    values = [
        force,
        decel,
        distance,
        stop,
        energy,
        rotor / (28 * 460),
        front,
        rear,
        float(abs(heat_residual) > 1e-10 or rear < 0),
    ]
    return _finish(
        values,
        traction_limit_n=cap,
        stopping_work_j=work,
        rotor_heat_j=rotor,
        other_heat_j=other,
        heat_residual_fraction=heat_residual,
        work_residual_fraction=(work - energy) / energy,
        load_transfer_n=transfer,
        normal_load_residual_n=front + rear - weight,
        pitch_moment_residual_nm=(front - 0.53 * weight) * 2.57 - force * 0.5,
    )


def _response(a, b, broken):
    state = _state(a, b, broken)
    force = state["applied_brake_force_n"]
    decel = state["deceleration_m_s2"]
    ts = _linspace(0.0, state["stop_time_s"], 61)
    velocity = [max(0.0, a - decel * t) for t in ts]
    distance = [a * t - 0.5 * decel * t * t for t in ts]
    work = [force * x for x in distance]
    fraction = 1.0 if broken else 0.85
    return {
        "x": ts,
        "series": [velocity],
        "distance_m": distance,
        "remaining_kinetic_energy_j": [0.5 * 1320 * v * v for v in velocity],
        "stopping_work_j": work,
        "braking_power_w": [force * v for v in velocity],
        "rotor_heat_j": [fraction * w for w in work],
        "other_heat_j": [0.15 * w for w in work],
        "rotor_temperature_rise_c": [fraction * w / (28 * 460) for w in work],
        "names": ["Vehicle speed during stop"],
        "x_quantity": "Time from braking",
        "x_unit": "s",
        "y_quantity": "Vehicle speed",
        "y_unit": "m/s",
    }


def _interpret(s):
    excess = s["heat_residual_fraction"] * s["kinetic_energy_j"]
    return (
        f"The stop takes {s['stop_time_s']:.6g} s over {s['stopping_distance_m']:.6g} m with {s['applied_brake_force_n']:.6g} N applied. "
        f"Rotor heat is {s['rotor_heat_j']:.6g} J and other heat {s['other_heat_j']:.6g} J; their excess over initial energy is {excess:.6g} J. "
        f"The rotor rise is {s['rotor_delta_t_c']:.6g} °C. The fault changes heat allocation, not the speed trajectory."
    )
