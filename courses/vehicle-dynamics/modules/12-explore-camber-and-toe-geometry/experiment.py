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


def _branch_traces(response, prefix=""):
    traces = []
    for stable, label in [(True, "Stable branch"), (False, "Formal unstable branch")]:
        indices = [i for i, flag in enumerate(response["stable"]) if flag == stable]
        if not indices:
            continue
        trace = _trace(
            prefix + label,
            [response["x"][i] for i in indices],
            [response["series"][0][i] for i in indices],
            response["x_quantity"],
            response["x_unit"],
            response["y_quantity"],
            response["y_unit"],
        )
        trace["meta"]["steady_branch_stable"] = stable
        if not stable:
            trace["line"] = {"dash": "dash", "color": "#a63d40"}
        traces.append(trace)
    return traces


def _model(a, b, broken):
    return _state(a, b, broken)["signature"]


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    a = float(parameters[PRIMARY])
    b = float(parameters[SECONDARY])
    broken = bool(parameters["broken_mode"])
    for name, value, bounds in [
        (PRIMARY, a, PRIMARY_RANGE),
        (SECONDARY, b, SECONDARY_RANGE),
    ]:
        if not math.isfinite(value) or not bounds[0] <= value <= bounds[1]:
            raise ValueError(f"{name} outside declared finite range")
    state = _state(a, b, broken)
    s = state["signature"]
    nominal = _state(a, b, False)
    fault = _state(a, b, True)
    if not all(math.isfinite(v) for v in s):
        raise ValueError("non-finite model result")
    response = _response(a, b, broken)
    xq = response["x_quantity"]
    xu = response["x_unit"]
    yq = response["y_quantity"]
    yu = response["y_unit"]
    traces = [
        _trace(name, response["x"], ys, xq, xu, yq, yu)
        for name, ys in zip(response["names"], response["series"])
    ]
    if NUMBER == 4:
        traces += [
            _trace(
                "Applied vector",
                response["vector_x"],
                response["vector_y"],
                xq,
                xu,
                yq,
                yu,
                "lines+markers",
            ),
            _trace(
                "Requested force",
                response["requested_x"],
                response["requested_y"],
                xq,
                xu,
                yq,
                yu,
                "markers",
            ),
        ]
    if NUMBER == 8:
        traces = _branch_traces(response)
    px = _linspace(*PRIMARY_RANGE, 61)
    sx = _linspace(*SECONDARY_RANGE, 61)
    py = [_state(v, b, False)["signature"][P_INDEX] for v in px]
    sy = [_state(a, v, False)["signature"][S_INDEX] for v in sx]
    # At the same selected inputs, compare actual curves from the executed fault and nominal model.
    good = _response(a, b, False)
    bad = _response(a, b, True)
    comparison = [
        _trace("Nominal: " + name, good["x"], ys, xq, xu, yq, yu)
        for name, ys in zip(good["names"], good["series"])
    ]
    comparison += [
        _trace("Fault: " + name, bad["x"], ys, xq, xu, yq, yu)
        for name, ys in zip(bad["names"], bad["series"])
    ]
    if NUMBER == 4:
        comparison = [
            _trace("Friction boundary", good["x"], good["series"][0], xq, xu, yq, yu),
            _trace(
                "Projected request",
                good["vector_x"],
                good["vector_y"],
                xq,
                xu,
                yq,
                yu,
                "lines+markers",
            ),
            _trace(
                "Unprojected request",
                bad["vector_x"],
                bad["vector_y"],
                xq,
                xu,
                yq,
                yu,
                "lines+markers",
            ),
        ]
    if NUMBER == 8:
        comparison = _branch_traces(good, "Nominal: ") + _branch_traces(bad, "Fault: ")
    metrics = [
        {"id": "input_primary", "label": P_LABEL, "value": a, "unit": P_UNIT},
        {"id": "input_secondary", "label": S_LABEL, "value": b, "unit": S_UNIT},
    ]
    for i, (label, unit, index) in enumerate(METRICS):
        value = s[index]
        if (NUMBER == 8 and index == 2 and not state["critical_speed_available"]) or (
            NUMBER == 10 and index == 4 and not state["time_scale_available"]
        ):
            value = "Unavailable"
        metrics.append(
            {"id": f"physical_{i}", "label": label, "value": value, "unit": unit}
        )
    metrics.append(
        {
            "id": "valid",
            "label": "Declared checks satisfied",
            "value": not bool(s[-1]),
            "unit": "boolean",
        }
    )
    if NUMBER == 7:
        metrics += [
            {
                "id": "force_residual",
                "label": "Force-balance residual",
                "value": state["force_balance_residual_n"],
                "unit": "N",
            },
            {
                "id": "moment_residual",
                "label": "Yaw-moment residual",
                "value": state["yaw_balance_residual_nm"],
                "unit": "N·m",
            },
        ]
    changed = (
        max(
            abs(x - y)
            for x, y in zip(nominal["signature"][:-1], fault["signature"][:-1])
        )
        > 1e-12
    )
    interpretation = f"Camber thrust is {s[2]:.6g} N; toe scrub power is {s[4]:.6g} W. Power is not a temperature prediction."
    return {
        "metrics": metrics,
        "plots": {
            "response": _plot(
                "Selected physical response",
                traces,
                xq,
                xu,
                yq,
                yu,
                response.get("equal_axes", False),
            ),
            "primary_sweep": _plot(
                "Vary " + P_LABEL,
                [
                    _trace(
                        "Nominal sweep",
                        px,
                        py,
                        P_LABEL,
                        P_UNIT,
                        P_QUANTITY,
                        P_RESPONSE_UNIT,
                    )
                ],
                P_LABEL,
                P_UNIT,
                P_QUANTITY,
                P_RESPONSE_UNIT,
            ),
            "secondary_sweep": _plot(
                "Vary " + S_LABEL,
                [
                    _trace(
                        "Nominal sweep",
                        sx,
                        sy,
                        S_LABEL,
                        S_UNIT,
                        S_QUANTITY,
                        S_RESPONSE_UNIT,
                    )
                ],
                S_LABEL,
                S_UNIT,
                S_QUANTITY,
                S_RESPONSE_UNIT,
            ),
            "broken_recovery": _plot(
                "Same-input fault comparison",
                comparison,
                xq,
                xu,
                yq,
                yu,
                response.get("equal_axes", False),
            ),
        },
        "explanations": {
            "observation": f"{P_LABEL}={a:g} {P_UNIT}; {S_LABEL}={b:g} {S_UNIT}. "
            + interpretation
            + " "
            + LIMIT,
            "broken": FAULT
            + ". "
            + (
                "The selected inputs expose a numerical difference."
                if changed
                else "This input is a benign limit: the two results coincide."
            ),
            "recovery": "Disable the fault at the same inputs to restore the declared model. Reset parameters separately to reproduce the worked baseline.",
        },
        "diagnostics": {
            "item_id": f"P{NUMBER:02d}",
            "signature": s,
            "broken_active": broken,
            "physical": state,
            "response": response,
            "primary_sweep": {"x": px, "y": py},
            "secondary_sweep": {"x": sx, "y": sy},
        },
    }


NUMBER = 12
PRIMARY = "camber_deg"
SECONDARY = "toe_deg"
PRIMARY_RANGE = (-5.0, 2.0)
SECONDARY_RANGE = (-0.5, 0.5)
P_LABEL = "Camber"
S_LABEL = "Toe"
P_UNIT = "deg"
S_UNIT = "deg"
METRICS = [
    ("Camber thrust", "N", 2),
    ("Toe scrub force", "N", 3),
    ("Toe scrub power", "W", 4),
]
P_INDEX = 2
S_INDEX = 4
P_QUANTITY = "Camber thrust"
P_RESPONSE_UNIT = "N"
S_QUANTITY = "Toe scrub power"
S_RESPONSE_UNIT = "W"
FAULT = "Treat degree inputs as radians"
LIMIT = "This is an empirical force/power estimate, not suspension-geometry or tire-temperature simulation."


def _state(a, b, broken):
    camber = a if broken else math.radians(a)
    toe = b if broken else math.radians(b)
    thrust = -60000 * camber
    scrub = 3600 * abs(math.tan(toe))
    power = 20 * scrub
    residual = camber - math.radians(a)
    toe_residual = toe - math.radians(b)
    s = [
        camber,
        toe,
        thrust,
        scrub,
        power,
        toe,
        float(max(abs(residual), abs(toe_residual)) > 1e-12),
    ]
    return dict(
        signature=s,
        camber_conversion_residual_rad=residual,
        toe_conversion_residual_rad=toe_residual,
        power_identity_residual_w=power - 20 * scrub,
    )


def _response(a, b, broken):
    xs = _linspace(-5, 2, 61)
    return dict(
        x=xs,
        series=[[_state(v, b, broken)["signature"][2] for v in xs]],
        names=["Linear empirical camber thrust"],
        x_quantity="Declared camber",
        x_unit="deg",
        y_quantity="Left camber thrust",
        y_unit="N",
    )
