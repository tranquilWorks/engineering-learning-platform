from __future__ import annotations

import numpy as np
from scipy.spatial import cKDTree


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


def data(fraction):
    i = np.arange(120)
    a = i * 2 * np.pi / 120
    r = 1 + 0.15 * np.cos(3 * a) + 0.08 * np.sin(5 * a)
    clean = np.column_stack(
        [
            1.4 * r * np.cos(a) + 0.15 * np.cos(2 * a),
            0.8 * r * np.sin(a) + 0.1 * np.sin(3 * a),
        ]
    )
    theta = 0.18
    R = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
    t = np.array([0.25, -0.12])
    target = (
        clean @ R.T + t + 0.002 * np.column_stack([np.sin(1.37 * i), np.cos(1.73 * i)])
    )
    source = clean.copy()
    mask = np.zeros(120, bool)
    mask[(np.arange(int(np.floor(120 * fraction))) * 37) % 120] = True
    phi = 2.399963229728653 * i[mask]
    source[mask] = np.column_stack([4.5 * np.cos(phi) + 0.2, 4 * np.sin(phi) - 0.3])
    return source, target, clean, R, t, mask


def run(p):
    offset = float(p["initial_offset_m"])
    fraction = float(p["outlier_fraction"])
    broken = bool(p["broken_mode"])
    source, target, clean, truth_R, truth_t, outliers = data(fraction)
    R = np.eye(2)
    t = np.array([offset, 0.0])
    tree = cKDTree(target)
    history = []
    transforms = []
    masks = []
    status = "maximum_iterations"
    gate = 0.5
    for _ in range(30):
        moved = source @ R.T + t
        distance, index = tree.query(moved)
        mask = np.ones(len(source), bool) if broken else distance <= gate
        if sum(mask) < 3:
            status = "insufficient_matches"
            break
        A = moved[mask]
        B = target[index[mask]]
        ma, mb = A.mean(axis=0), B.mean(axis=0)
        A = A - ma
        B = B - mb
        U, _sv, V = np.linalg.svd(A.T @ B)
        correction = np.diag([1.0, np.linalg.det(V.T @ U.T)])
        dR = V.T @ correction @ U.T
        angle = np.arctan2(dR[1, 0], dR[0, 0])
        dt = mb - dR @ ma
        R, t = dR @ R, dR @ t + dt
        fresh, _ = tree.query(source @ R.T + t)
        objective = np.mean(
            fresh * fresh if broken else np.minimum(fresh * fresh, gate * gate)
        )
        history.append([objective, float(np.linalg.norm(dt)), float(abs(angle))])
        transforms.append(np.column_stack([R, t]))
        masks.append(mask)
        if np.linalg.norm(dt) < 1e-9 and abs(angle) < 1e-9:
            status = "converged"
            break
    moved = source @ R.T + t
    distance, index = tree.query(moved)
    accepted = np.ones(len(source), bool) if broken else distance <= gate
    rmse = np.sqrt(np.mean(distance[accepted] ** 2)) if accepted.any() else 0.0
    error = np.sqrt(
        np.mean(np.sum((clean @ R.T + t - (clean @ truth_R.T + truth_t)) ** 2, axis=1))
    )
    history = np.asarray(history).reshape(-1, 3)
    metrics = [
        ("correspondence_rms", "Accepted correspondence RMS", rmse, "m"),
        ("transform_point_error", "Clean-shape transform RMS error", error, "m"),
        ("executed_iterations", "Executed rigid updates", len(history), "count"),
    ]
    plots = {
        "response": plot(
            "Registered point clouds",
            "World x (m)",
            "World y (m)",
            [
                points(
                    "Target", target[:, 0], target[:, 1], "World x", "m", "World y", "m"
                ),
                points(
                    "Moved", moved[:, 0], moved[:, 1], "World x", "m", "World y", "m"
                ),
            ],
        ),
        "mechanism": plot(
            "ICP objective",
            "Update (count)",
            "Mean cost (m²)",
            [
                trace(
                    "Objective",
                    np.arange(1, len(history) + 1),
                    history[:, 0],
                    "Update",
                    "count",
                    "Mean cost",
                    "m^2",
                )
            ],
        ),
    }
    plots["response"]["layout"]["yaxis"].update(scaleanchor="x", scaleratio=1)
    status_label = {
        "converged": "converged by the update thresholds",
        "maximum_iterations": "the 30-update limit was reached",
        "insufficient_matches": "fewer than three matches were accepted",
    }[status]
    return finish(
        48,
        broken,
        {
            "sample_count": 120,
            "source_points": source,
            "target_points": target,
            "clean_source": clean,
            "true_rotation": truth_R,
            "true_translation": truth_t,
            "source_outliers": outliers,
            "rotation": R,
            "translation": t,
            "moved_points": moved,
            "nearest_indices": index,
            "distances": distance,
            "accepted": accepted,
            "history": history,
            "transform_history": transforms,
            "accepted_history": masks,
            "solver_status": status,
            "residual_available": bool(accepted.any()),
            "cost_definition": "full_squared_distance"
            if broken
            else "squared_distance_truncated_at_0.25_m2",
        },
        metrics,
        plots,
        "Planar ICP recomputes actual nearest neighbours and rigid updates. Status: "
        + status_label
        + ". A decreasing local objective is separate from true transform accuracy.",
        "The fault accepts every correspondence, including source clutter. Normal mode uses a 0.5 m gate and a truncated diagnostic objective.",
        "Restore the gate and restart from the same offset. Inspect transform error and termination status; local minima and maximum-budget results are retained.",
    )
