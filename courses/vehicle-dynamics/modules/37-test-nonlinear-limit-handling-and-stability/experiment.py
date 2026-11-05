from __future__ import annotations

from typing import Any

import numpy as np
from scipy.optimize import least_squares

ITEM_NUMBER = 37
DEFAULTS = {"steer_deg": 6.0, "friction_mu": 1.15}
RANGES = {"steer_deg": (1.0, 10.0), "friction_mu": (0.7, 1.5)}
BROKEN_TEXT = "Broken mode extends axle cornering stiffness linearly beyond the declared friction capacity, producing utilization above one."
RECOVERY_TEXT = "Restore bounded nonlinear axle forces, then recompute utilization, yaw moment, and the local restoring-moment slope."


def _parameters(supplied: dict[str, Any]) -> dict[str, float]:
    result: dict[str, float] = {}
    for key, default in DEFAULTS.items():
        value = float(supplied.get(key, default))
        minimum, maximum = RANGES[key]
        if not np.isfinite(value) or value < minimum or value > maximum:
            raise ValueError(f"{key} outside declared finite range [{minimum}, {maximum}]")
        result[key] = value
    return result


def _trace(
    name: str,
    x: Any,
    y: Any,
    x_quantity: str,
    x_unit: str,
    y_quantity: str,
    y_unit: str,
    *,
    mode: str = "lines",
) -> dict[str, Any]:
    return {
        "type": "scattergl",
        "mode": mode,
        "name": name,
        "x": np.asarray(x, dtype=float),
        "y": np.asarray(y, dtype=float),
        "meta": {
            "x_quantity": x_quantity,
            "x_unit": x_unit,
            "y_quantity": y_quantity,
            "y_unit": y_unit,
        },
    }


def _plot(
    title: str,
    x_title: str,
    y_title: str,
    traces: list[dict[str, Any]],
) -> dict[str, Any]:
    result = {
        "data": traces,
        "layout": {
            "title": {"text": title, "x": 0.02},
            "xaxis": {"title": {"text": x_title}},
            "yaxis": {"title": {"text": y_title}},
            "legend": {"orientation": "h"},
            "margin": {"l": 72, "r": 36, "t": 62, "b": 62},
            "hovermode": "closest",
            "uirevision": "keep-view",
        },
        "config": {"responsive": True, "displaylogo": False},
    }
    # Course-owned layout: keep engineering labels readable in narrow plot panels.
    from textwrap import fill
    layout = result["layout"]
    layout["title"] = {"text": fill(title, width=30).replace("\n", "<br>"), "x": 0.02, "font": {"size": 14}}
    layout["legend"] = {"orientation": "h"}
    layout.setdefault("margin", {"l": 72, "r": 36, "t": 62, "b": 110})
    for axis in ("xaxis", "yaxis"):
        layout[axis]["automargin"] = True
        if isinstance(layout[axis].get("title"), dict):
            layout[axis]["title"]["standoff"] = 12
    return result


def _result(model: dict[str, Any], broken: bool) -> dict[str, Any]:
    return {
        "metrics": [
            {
                "id": key,
                "label": label,
                "value": float(value),
                "unit": unit,
                "emphasis": "primary" if index == 0 else "normal",
            }
            for index, (key, label, value, unit) in enumerate(model["metrics"])
        ],
        "plots": model["plots"],
        "explanations": {
            "observation": model["observation"],
            "broken": BROKEN_TEXT,
            "recovery": RECOVERY_TEXT,
        },
        "diagnostics": {
            "item_number": ITEM_NUMBER,
            "broken_active": bool(broken),
            "signature": [float(value) for value in model["signature"]],
        },
    }


def _forces(beta: float, steer: float, friction: float, broken: bool) -> tuple[float, float]:
    speed, a, b = 28.0, 1.20, 1.50
    mass, gravity = 1450.0, 9.81
    yaw_rate = speed * np.tan(steer) / (a + b)
    alpha_front = steer - beta - a * yaw_rate / speed
    alpha_rear = -beta + b * yaw_rate / speed
    front_linear, rear_linear = 70000.0 * alpha_front, 75000.0 * alpha_rear
    front_capacity = friction * mass * gravity * b / (a + b)
    rear_capacity = friction * mass * gravity * a / (a + b)
    if broken:
        return front_linear, rear_linear
    return (
        front_capacity * np.tanh(front_linear / front_capacity),
        rear_capacity * np.tanh(rear_linear / rear_capacity),
    )


def _model(p: dict[str, float], broken: bool) -> dict[str, Any]:
    steer = np.deg2rad(p["steer_deg"])
    friction = p["friction_mu"]
    mass, gravity, a, b = 1450.0, 9.81, 1.20, 1.50
    front_capacity = friction * mass * gravity * b / (a + b)
    rear_capacity = friction * mass * gravity * a / (a + b)
    beta = np.deg2rad(10.0)
    front, rear = _forces(beta, steer, friction, broken)
    front_util, rear_util = abs(front) / front_capacity, abs(rear) / rear_capacity
    yaw_moment = a * front - b * rear
    epsilon = 1.0e-5
    plus = _forces(beta + epsilon, steer, friction, broken)
    minus = _forces(beta - epsilon, steer, friction, broken)
    slope = (a * (plus[0] - minus[0]) - b * (plus[1] - minus[1])) / (2.0 * epsilon)
    stability_margin = -slope
    capacity_excess = max(0.0, front_util - 1.0, rear_util - 1.0)
    signature = [front_util, rear_util, abs(yaw_moment), stability_margin, capacity_excess]
    beta_sweep = np.deg2rad(np.linspace(-6.0, 6.0, 121))
    moments = []
    utilizations = []
    for value in beta_sweep:
        sample_front, sample_rear = _forces(value, steer, friction, broken)
        moments.append(a * sample_front - b * sample_rear)
        utilizations.append(max(abs(sample_front) / front_capacity, abs(sample_rear) / rear_capacity))
    return {
        "signature": signature,
        "metrics": [
            ("front_utilization", "Front utilization", front_util, "1"),
            ("rear_utilization", "Rear utilization", rear_util, "1"),
            ("yaw_moment", "Yaw-moment imbalance", abs(yaw_moment), "N*m"),
            ("stability_margin", "Restoring-moment slope", stability_margin, "N*m/rad"),
        ],
        "plots": {
            "response": _plot(
                "Nonlinear yaw moment",
                "Body sideslip (deg)",
                "Yaw moment (N*m)",
                [
                    _trace("Yaw moment", np.rad2deg(beta_sweep), moments, "Body sideslip", "deg", "Yaw moment", "N*m"),
                ],
            ),
            "mechanism": _plot(
                "Axle capacity utilization",
                "Body sideslip (deg)",
                "Maximum axle utilization (1)",
                [
                    _trace("Maximum utilization", np.rad2deg(beta_sweep), utilizations, "Body sideslip", "deg", "Maximum axle utilization", "1"),
                    _trace("Capacity boundary", np.rad2deg(beta_sweep), np.ones(beta_sweep.size), "Body sideslip", "deg", "Maximum axle utilization", "1"),
                ],
            ),
        },
        "observation": "A local restoring slope does not excuse a force demand above capacity; stability and saturation must be inspected together.",
    }


def _dynamic_rhs(state, steer, friction, broken=False):
    """Constant-speed, small-body-angle bicycle with nonlinear axle forces."""
    beta, yaw = state
    alpha = np.array([steer-beta-1.2*yaw/28.0, -beta+1.5*yaw/28.0])
    stiffness = np.array([70000.0, 75000.0])
    capacities = friction*1450.0*9.81*np.array([1.5, 1.2])/2.7
    linear = stiffness*alpha
    forces = linear if broken else capacities*np.tanh(linear/capacities)
    rates = np.array([(forces.sum()/(1450.0*28.0))-yaw,
                      (1.2*forces[0]-1.5*forces[1])/2400.0])
    slopes = stiffness if broken else stiffness*(1.0-np.tanh(linear/capacities)**2)
    force_jacobian = slopes[:, None]*np.array([[-1.0, -1.2/28.0], [-1.0, 1.5/28.0]])
    jacobian = np.array([[1/(1450*28), 1/(1450*28)], [1.2/2400, -1.5/2400]]) @ force_jacobian
    jacobian[0, 1] -= 1.0
    return rates, jacobian, forces/capacities


def _dynamic_study(p, broken, dt=0.005):
    steer, mu = np.deg2rad(p["steer_deg"]), p["friction_mu"]
    # beta in radians, yaw in radians/s; 1 s scales yaw in solver residuals.
    solution = least_squares(lambda x: _dynamic_rhs(x, steer, mu, broken)[0],
                             [0.0, 0.1], jac=lambda x: _dynamic_rhs(x, steer, mu, broken)[1],
                             bounds=([-0.35, -1.5], [0.35, 1.5]),
                             ftol=1e-12, xtol=1e-12, gtol=1e-12)
    rates, jac, _ = _dynamic_rhs(solution.x, steer, mu, broken)
    trim_residual = float(np.linalg.norm(rates))
    trim_valid = trim_residual < 1e-8 and abs(solution.x[0]) < 0.35-1e-7 and abs(solution.x[1]) < 1.5-1e-7
    poles = np.linalg.eigvals(jac)
    time, states, utilization = [0.0], [np.zeros(2)], [float(np.max(abs(_dynamic_rhs(np.zeros(2), steer, mu, broken)[2])))]
    valid = True
    for i in range(round(3.0/dt)):
        state = states[-1]
        f = lambda x: _dynamic_rhs(x, steer, mu, broken)[0]
        k1 = f(state); k2 = f(state+dt*k1/2); k3 = f(state+dt*k2/2); k4 = f(state+dt*k3)
        next_state = state+dt*(k1+2*k2+2*k3+k4)/6
        if abs(next_state[0]) > 0.35 or abs(next_state[1]) > 1.5:
            valid = False
            break
        states.append(next_state); time.append((i+1)*dt)
        utilization.append(float(np.max(abs(_dynamic_rhs(next_state, steer, mu, broken)[2]))))
    return {"time": np.array(time), "states": np.array(states), "utilization": np.array(utilization),
            "trim": solution.x, "trim_valid": trim_valid, "trim_residual": trim_residual,
            "pole_real": poles.real, "pole_imag": poles.imag, "trajectory_valid": valid,
            "decay_margin": float(-max(poles.real)) if trim_valid else 0.0}


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    values = _parameters(parameters)
    broken = bool(parameters.get("broken_mode", False))
    result = _result(_model(values, broken), broken)
    study = _dynamic_study(values, broken)
    result["diagnostics"]["dynamic_study"] = study
    for key, label, value, unit in [
        ("trim_valid", "Admissible equilibrium found", study["trim_valid"], "1"),
        ("trim_residual", "Scaled equilibrium residual", study["trim_residual"], "rad/s"),
        ("decay_margin", "Local decay margin (only if trim valid)", study["decay_margin"], "1/s"),
        ("trajectory_valid", "Full 3 s trajectory within declared domain", study["trajectory_valid"], "1"),
    ]:
        result["metrics"].append({"id": key, "label": label, "value": float(value), "unit": unit})
    result["plots"]["state_history"] = _plot("Executed nonlinear bicycle response", "Elapsed time (s)", "Body sideslip (deg)", [
        _trace("Sideslip", study["time"], np.rad2deg(study["states"][:,0]), "Elapsed time", "s", "Sideslip", "deg"),
        _trace("Yaw rate", study["time"], np.rad2deg(study["states"][:,1]), "Elapsed time", "s", "Yaw rate", "deg/s")])
    result["plots"]["state_history"]["data"][1]["yaxis"] = "y2"
    result["plots"]["state_history"]["layout"]["yaxis2"] = {"title": {"text": "Yaw rate (deg/s)"}, "overlaying": "y", "side": "right"}
    result["plots"]["state_history"]["layout"]["margin"]["r"] = 76
    result["plots"]["dynamic_utilization"] = _plot("Executed axle utilization", "Elapsed time (s)", "Maximum axle utilization (1)", [
        _trace("Actual utilization", study["time"], study["utilization"], "Elapsed time", "s", "Axle utilization", "1")])
    result["explanations"]["observation"] += " The static slope is a component diagnostic only. Full-state local stability requires an admissible equilibrium and negative real parts of BOTH Jacobian poles; the executed transient must also respect its domain and force limits."
    return result
