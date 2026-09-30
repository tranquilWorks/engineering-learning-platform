from __future__ import annotations

import numpy as np
from scipy.spatial.transform import Rotation


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


def skew(v):
    x, y, z = v
    return np.array([[0.0, -z, y], [z, 0.0, -x], [-y, x, 0.0]])


def setup(n, noise):
    i = np.arange(40)
    a = i * 2.399963229728653
    z = 1 - 2 * (i + 0.5) / 40
    r = np.sqrt(1 - z * z)
    points = np.column_stack(
        [0.55 * r * np.cos(a), 0.45 * r * np.sin(a), 0.35 * z]
    )  # Select across the whole shape even at four observations.
    points = points[np.linspace(0, 39, n).round().astype(int)]
    R = Rotation.from_rotvec([0.18, -0.1, 0.25]).as_matrix()
    t = np.array([0.15, -0.1, 3.2])
    camera = points @ R.T + t
    pixels = 800 * camera[:, :2] / camera[:, 2, None] + [320, 240]
    j = np.arange(n)
    pixels += noise * np.column_stack([np.sin(1.7 * j + 0.3), np.cos(2.3 * j - 0.2)])
    return points, pixels, R, t


def fit(points, obs, focal):
    R = np.eye(3)
    t = np.array([0.0, 0.0, 3.0])
    history = []
    converged = False

    def evaluate(R, t):
        rotated = points @ R.T
        camera = rotated + t
        pred = focal * camera[:, :2] / camera[:, 2, None] + [320, 240]
        res = (pred - obs).ravel()
        J = []
        for X, p in zip(camera, rotated, strict=True):
            x, y, z = X
            projection = focal * np.array(
                [[1 / z, 0, -x / z**2], [0, 1 / z, -y / z**2]]
            )
            J.extend(projection @ np.column_stack([-skew(p), np.eye(3)]))
        return res, np.array(J), camera

    for iteration in range(80):
        res, J, _camera = evaluate(R, t)
        cost = 0.5 * res @ res
        delta = np.linalg.lstsq(J, -res, rcond=None)[0]
        history.append(
            [
                cost,
                float(np.linalg.norm(J.T @ res, np.inf)),
                float(np.linalg.norm(delta)),
            ]
        )
        if np.linalg.norm(delta) < 1e-13:
            converged = True
            break
        accepted = False
        for power in range(25):
            alpha = 2.0**-power
            candidateR = Rotation.from_rotvec(alpha * delta[:3]).as_matrix() @ R
            candidatet = t + alpha * delta[3:]
            new, _, cam = evaluate(candidateR, candidatet)
            if min(cam[:, 2]) > 0.2 and (
                0.5 * new @ new <= cost + 1e-13 or np.linalg.norm(delta) < 1e-7
            ):
                R, t = candidateR, candidatet
                accepted = True
                break
        if not accepted:
            break
    res, J, _camera = evaluate(R, t)
    return R, t, res, J, np.array(history), converged


def run(p):
    count = int(p["visible_landmarks"])
    noise = float(p["landmark_noise_px"])
    broken = bool(p["broken_mode"])
    focal = 650.0 if broken else 800.0
    landmarks, observed, truth_R, truth_t = setup(count, noise)
    R, t, residual, J, history, converged = fit(landmarks, observed, focal)
    camera = landmarks @ R.T + t
    predicted = focal * camera[:, :2] / camera[:, 2, None] + [320, 240]
    relative = R @ truth_R.T
    sine = (
        np.linalg.norm(
            [
                relative[2, 1] - relative[1, 2],
                relative[0, 2] - relative[2, 0],
                relative[1, 0] - relative[0, 1],
            ]
        )
        / 2
    )
    angle = np.rad2deg(np.arctan2(sine, (np.trace(relative) - 1) / 2))
    status = (
        "small_increment"
        if converged
        else "maximum_iterations"
        if len(history) == 80
        else "stalled_search"
    )
    metrics = [
        ("translation_error", "Translation error", np.linalg.norm(t - truth_t), "m"),
        ("rotation_error", "Rotation error", angle, "deg"),
        (
            "reprojection_rms",
            "Landmark reprojection RMS",
            np.sqrt(np.mean(np.sum(residual.reshape(-1, 2) ** 2, axis=1))),
            "px",
        ),
    ]
    plots = {
        "response": plot(
            "Observed and fitted pixels",
            "Image x (px)",
            "Image y (px)",
            [
                points(
                    "Observed",
                    observed[:, 0],
                    observed[:, 1],
                    "Image x",
                    "px",
                    "Image y",
                    "px",
                ),
                points(
                    "Fitted",
                    predicted[:, 0],
                    predicted[:, 1],
                    "Image x",
                    "px",
                    "Image y",
                    "px",
                ),
            ],
        ),
        "mechanism": plot(
            "Pose-fit objective",
            "Iteration (count)",
            "Half SSE (px²)",
            [
                trace(
                    "Objective",
                    np.arange(len(history)),
                    history[:, 0],
                    "Iteration",
                    "count",
                    "Half squared pixel error",
                    "px^2",
                )
            ],
        ),
    }
    plots["response"]["layout"]["yaxis"].update(scaleanchor="x", scaleratio=1)
    status_label = {
        "small_increment": "converged by the increment test",
        "stalled_search": "line search stalled",
        "maximum_iterations": "the 80-iteration limit was reached",
    }[status]
    return finish(
        46,
        broken,
        {
            "sample_count": count,
            "landmarks": landmarks,
            "observed_pixels": observed,
            "true_rotation": truth_R,
            "true_translation": truth_t,
            "rotation": R,
            "translation": t,
            "camera_points": camera,
            "predicted_pixels": predicted,
            "residuals": residual.reshape(-1, 2),
            "jacobian": J,
            "jacobian_rank": int(np.linalg.matrix_rank(J)),
            "jacobian_condition": float(np.linalg.cond(J)),
            "history": history,
            "solver_status": status,
            "small_increment": converged,
            "used_focal_length": focal,
            "minimum_camera_depth": float(camera[:, 2].min()),
        },
        metrics,
        plots,
        "A full six-DOF local pose fit starts at identity rotation and [0,0,3] m. Status: "
        + status_label
        + "; actual pixel Jacobian rank "
        + str(np.linalg.matrix_rank(J))
        + " of six.",
        "The estimator uses 650 px focal length for observations generated with 800 px. Pose can absorb part of that error while remaining metrically biased.",
        "Restore 800 px calibration and compare rotation, translation and pixel residual separately. More points do not guarantee global uniqueness or cure a wrong camera model.",
    )
