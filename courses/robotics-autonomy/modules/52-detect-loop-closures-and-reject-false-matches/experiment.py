from __future__ import annotations

import numpy as np


def trace(name, x, y, x_quantity, x_unit, y_quantity, y_unit):
    x, y = np.asarray(x, float), np.asarray(y, float)
    return {
        "type": "scatter",
        "mode": "lines+markers" if x.size and np.ptp(x) == 0 else "lines",
        "name": name,
        "x": x,
        "y": y,
        "meta": {
            "x_quantity": x_quantity,
            "x_unit": x_unit,
            "y_quantity": y_quantity,
            "y_unit": y_unit,
        },
    }


def plot(title, x, y, traces):
    return {
        "data": traces,
        "layout": {
            "title": {"text": title, "x": 0.02},
            "xaxis": {"title": {"text": x, "standoff": 16}},
            "yaxis": {"title": {"text": y, "standoff": 16}},
            "legend": {
                "orientation": "h",
                "y": -0.3,
                "entrywidth": 0.5,
                "entrywidthmode": "fraction",
            },
            "margin": {"l": 72, "r": 25, "t": 65, "b": 115},
            "uirevision": "keep-view",
        },
        "config": {"responsive": True, "displaylogo": False},
    }


def finish(number, broken, diagnostics, metrics, plots, observation, fault, recovery):
    diagnostics.update(
        item_number=number,
        broken_active=broken,
        software_only=True,
        signature=[float(m[2]) for m in metrics],
    )
    return {
        "metrics": [
            {
                "id": key,
                "label": label,
                "value": float(value),
                "unit": unit,
                "emphasis": "primary" if i == 0 else "normal",
            }
            for i, (key, label, value, unit) in enumerate(metrics)
        ],
        "plots": plots,
        "diagnostics": diagnostics,
        "explanations": {
            "observation": observation,
            "broken": fault,
            "recovery": recovery,
        },
    }


def points(name, x, y, xq, xu, yq, yu):
    item = trace(name, x, y, xq, xu, yq, yu)
    item["mode"] = "markers"
    return item


def heatmap(name, x, y, z, xq, xu, yq, yu):
    return {
        "type": "heatmap",
        "name": name,
        "x": np.asarray(x),
        "y": np.asarray(y),
        "z": np.asarray(z),
        "colorscale": "Greys",
        "showscale": False,
        "meta": {
            "x_quantity": xq,
            "x_unit": xu,
            "y_quantity": yq,
            "y_unit": yu,
            "z_quantity": "Value",
            "z_unit": "1",
        },
    }


def huber(x, delta):
    return 0.5 * x * x if x <= delta else delta * (x - 0.5 * delta)


def problem(score, residual):
    truth = np.array(
        [
            [0.0, 0.0],
            [0.5, 0.0],
            [1.0, 0.0],
            [1.0, 0.5],
            [1.0, 1.0],
            [0.5, 1.0],
            [0.0, 1.0],
            [0.0, 0.5],
            [0.0, 0.0],
        ]
    )
    odom = np.diff(truth, axis=0) + [0.02, 0.005]
    baseline = np.vstack([[0.0, 0.0], np.cumsum(odom, axis=0)])
    closure = baseline[-1] - [residual, 0.0]
    A = np.eye(8) - np.eye(8, k=-1)
    C = np.zeros((1, 8))
    C[0, -1] = 1
    return truth, odom, baseline, closure, A, C


def run(p):
    score = float(p["descriptor_score"])
    residual = float(p["geometric_residual_m"])
    broken = bool(p["broken_mode"])
    truth, odom, baseline, measurement, A, C = problem(score, residual)
    innovation = baseline[-1] - measurement
    inserted = score >= 0.7 and (np.linalg.norm(innovation) <= 0.3 or broken)
    nodes = baseline.copy()
    weight = 0.0
    history = []
    so = 0.03
    sc = 0.08
    delta = 0.05
    status = "rejected"
    if inserted:
        status = "maximum_iterations"
        for _ in range(100):
            old = nodes.copy()
            r = np.linalg.norm(nodes[-1] - measurement)
            weight = 1.0 if broken or r <= delta else delta / r
            gain = np.sqrt(score * weight) / sc
            H = np.vstack([A / so, gain * C])
            rhs = np.vstack([odom / so, gain * measurement])
            nodes[1:] = np.linalg.lstsq(H, rhs, rcond=None)[0]
            history.append(nodes.copy())
            if broken or np.max(abs(nodes - old)) < 1e-12:
                status = "solved" if broken else "irls_stationary"
                break
        r = np.linalg.norm(nodes[-1] - measurement)
        weight = 1.0 if broken or r <= delta else delta / r
    odom_residual = A @ nodes[1:] - odom
    closure_residual = nodes[-1] - measurement
    cost = 0.5 * np.sum((odom_residual / so) ** 2)
    if inserted:
        cost += score * (
            0.5 * np.sum((closure_residual / sc) ** 2)
            if broken
            else huber(np.linalg.norm(closure_residual) / sc, delta / sc)
        )
    displacement = np.linalg.norm(nodes - baseline, axis=1)
    gradient = A.T @ odom_residual / so**2
    if inserted:
        gradient += C.T @ (score * weight * closure_residual[None, :] / sc**2)
    metrics = [
        ("closure_influence", "Final closure influence", score * weight, "1"),
        ("graph_objective", "Optimized factor objective", cost, "1"),
        ("maximum_map_shift", "Maximum node displacement", displacement.max(), "m"),
    ]
    plots = {
        "response": plot(
            "Anchored position graph",
            "World x (m)",
            "World y (m)",
            [
                trace(
                    "Baseline",
                    baseline[:, 0],
                    baseline[:, 1],
                    "World x",
                    "m",
                    "World y",
                    "m",
                ),
                trace(
                    "Updated", nodes[:, 0], nodes[:, 1], "World x", "m", "World y", "m"
                ),
            ],
        ),
        "mechanism": plot(
            "Loop-induced displacement",
            "Node index (1)",
            "Displacement (m)",
            [
                trace(
                    "Shift",
                    np.arange(9),
                    displacement,
                    "Node index",
                    "1",
                    "Displacement",
                    "m",
                )
            ],
        ),
    }
    plots["response"]["layout"]["yaxis"].update(scaleanchor="x", scaleratio=1)
    plots["mechanism"]["layout"]["yaxis"].update(
        range=[0, max(0.01, 1.1 * float(displacement.max()))], tickformat=".3f"
    )
    status_label = {
        "rejected": "candidate rejected",
        "solved": "quadratic graph solved",
        "irls_stationary": "IRLS changes met the tolerance",
        "maximum_iterations": "IRLS reached its iteration limit",
    }[status]
    return finish(
        52,
        broken,
        {
            "sample_count": 9,
            "true_nodes": truth,
            "odometry": odom,
            "baseline_nodes": baseline,
            "optimized_nodes": nodes,
            "closure_measurement": measurement,
            "innovation": innovation,
            "factor_inserted": inserted,
            "robust_weight": float(weight),
            "odometry_residuals": odom_residual,
            "closure_residual": closure_residual,
            "node_displacements": displacement,
            "gradient": gradient,
            "irls_history": history,
            "solver_status": status,
            "odometry_sigma": so,
            "closure_sigma": sc,
            "huber_delta_m": delta,
        },
        metrics,
        plots,
        "An actual anchored translation graph is solved with the accepted loop factor. Candidate status: "
        + status_label
        + ". Appearance is externally supplied, and robust influence is not a probability of place identity.",
        "The fault preserves appearance gating but bypasses geometric rejection and uses quadratic closure influence. Selected score and innovation remain unchanged.",
        "Restore the 0.30 m geometric gate and Huber factor. Rejected candidates leave the baseline unchanged; limited deformation alone cannot prove a loop is correct.",
    )
