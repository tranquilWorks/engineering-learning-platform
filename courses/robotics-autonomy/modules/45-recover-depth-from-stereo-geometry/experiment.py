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


f = 520.0
a = 0.04
R = np.array([[np.cos(a), 0, np.sin(a)], [0, 1, 0], [-np.sin(a), 0, np.cos(a)]])
noise = 0.5 / np.sqrt(2)


def observations(B, d):
    point = np.array([0.08, 0.04, 1.0]) * f * B / d
    right = R.T @ (point - [B, 0, 0])
    return np.r_[f * point[:2] / point[2], f * right[:2] / right[2]], point


def production(obs, B, broken):
    left = np.r_[obs[:2] / f, 1.0]
    right = (np.eye(3) if broken else R) @ np.r_[obs[2:] / f, 1.0]
    scale = np.linalg.lstsq(np.column_stack([left, -right]), [B, 0, 0], rcond=None)[0]
    return 0.5 * (left * scale[0] + [B, 0, 0] + right * scale[1])


def production_jacobian(obs, B, broken):
    left = np.r_[obs[:2] / f, 1.0]
    orientation = np.eye(3) if broken else R
    right = orientation @ np.r_[obs[2:] / f, 1.0]
    A = np.column_stack([left, -right])
    b = np.array([B, 0, 0])
    scale = np.linalg.lstsq(A, b, rcond=None)[0]
    J = []
    for k in range(4):
        dl = np.eye(3)[:, k] / f if k < 2 else np.zeros(3)
        dr = orientation[:, k - 2] / f if k >= 2 else np.zeros(3)
        dA = np.column_stack([dl, -dr])
        ds = np.linalg.solve(A.T @ A, dA.T @ (b - A @ scale) - A.T @ dA @ scale)
        J.append(0.5 * (dl * scale[0] + left * ds[0] + dr * scale[1] + right * ds[1]))
    return np.column_stack(J)


def evaluate(B, d, broken):
    obs, truth = observations(B, d)
    point = production(obs, B, broken)
    J = production_jacobian(obs, B, broken)
    covariance = noise**2 * J @ J.T
    right = R.T @ (point - [B, 0, 0])
    pixels = np.r_[f * point[:2] / point[2], f * right[:2] / right[2]]
    residual = (pixels - obs).reshape(2, 2)
    return (
        point,
        truth,
        obs,
        pixels,
        J,
        covariance,
        float(np.sqrt(np.mean(np.sum(residual**2, axis=1)))),
    )


def run(p):
    B = float(p["baseline_m"])
    d = float(p["disparity_px"])
    broken = bool(p["broken_mode"])
    point, truth, obs, pixels, J, covariance, error = evaluate(B, d, broken)
    disparities = np.linspace(1, 140, 101)
    sweep = [evaluate(B, value, broken) for value in disparities]
    depths = np.array([r[0][2] for r in sweep])
    true_depths = f * B / disparities
    uncertainty = np.array([np.sqrt(r[5][2, 2]) for r in sweep])
    metrics = [
        ("estimated_depth", "Triangulated depth", point[2], "m"),
        (
            "depth_uncertainty",
            "Predicted depth standard deviation",
            np.sqrt(covariance[2, 2]),
            "m",
        ),
        ("reprojection_rms", "Two-view reprojection RMS", error, "px"),
    ]
    plots = {
        "response": plot(
            "Triangulated depth",
            "Disparity (px)",
            "Depth (m)",
            [
                trace("Estimate", disparities, depths, "Disparity", "px", "Depth", "m"),
                trace(
                    "True", disparities, true_depths, "Disparity", "px", "Depth", "m"
                ),
            ],
        ),
        "mechanism": plot(
            "Pixel-noise uncertainty",
            "Disparity (px)",
            "Depth sigma (m)",
            [
                trace(
                    "Sigma",
                    disparities,
                    uncertainty,
                    "Disparity",
                    "px",
                    "Depth standard deviation",
                    "m",
                ),
                points(
                    "Selected",
                    [d],
                    [np.sqrt(covariance[2, 2])],
                    "Disparity",
                    "px",
                    "Depth standard deviation",
                    "m",
                ),
            ],
        ),
    }
    return finish(
        45,
        broken,
        {
            "sample_count": 101,
            "estimated_point": point,
            "true_point": truth,
            "observed_pixels": obs.reshape(2, 2),
            "reprojected_pixels": pixels.reshape(2, 2),
            "pixel_jacobian": J,
            "point_covariance": covariance,
            "pixel_noise_std": noise,
            "right_rotation": R,
            "disparities": disparities,
            "depth_sweep": depths,
            "true_depth_sweep": true_depths,
            "uncertainty_sweep": uncertainty,
            "positive_depth": bool(point[2] > 0 and (R.T @ (point - [B, 0, 0]))[2] > 0),
        },
        metrics,
        plots,
        "Calibrated rays produce an actual 3D midpoint and two-view residual. The curves sweep disparity; the selected marker and metrics use the chosen disparity. Predicted noise uncertainty excludes calibration bias.",
        "The triangulator ignores the right camera yaw while observations and evaluation keep the true pose. A biased estimate can report smaller conditional uncertainty.",
        "Restore calibrated ray rotation and check actual reprojection. At fixed disparity, increasing baseline also moves the constructed point farther away.",
    )
