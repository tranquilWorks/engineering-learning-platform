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


def views(indices):
    bx, by = np.meshgrid(np.linspace(-0.45, 0.45, 4), np.linspace(-0.3, 0.3, 3))
    board = np.column_stack([bx.ravel(), by.ravel(), np.zeros(12)])
    points = []
    for j in indices:
        x, y, z = 0.2 * np.cos(0.8 * j), 0.25 * np.sin(1.3 * j), 0.17 * j
        Rx = np.array(
            [[1.0, 0.0, 0.0], [0.0, np.cos(x), -np.sin(x)], [0.0, np.sin(x), np.cos(x)]]
        )
        Ry = np.array(
            [[np.cos(y), 0.0, np.sin(y)], [0.0, 1.0, 0.0], [-np.sin(y), 0.0, np.cos(y)]]
        )
        Rz = np.array(
            [[np.cos(z), -np.sin(z), 0.0], [np.sin(z), np.cos(z), 0.0], [0.0, 0.0, 1.0]]
        )
        points.append(
            board @ (Rz @ Ry @ Rx).T
            + [0.5 * np.sin(2.1 * j), 0.3 * np.cos(1.7 * j), 2 + 0.2 * np.sin(0.6 * j)]
        )
    return np.vstack(points)


def design(camera, distortion=True):
    xy = camera[:, :2] / camera[:, 2, None]
    r2 = np.sum(xy * xy, axis=1)
    n = len(xy)
    A = np.zeros((2 * n, 4 if distortion else 3))
    A[::2, 0] = xy[:, 0]
    A[1::2, 0] = xy[:, 1]
    if distortion:
        A[::2, 1] = xy[:, 0] * r2
        A[1::2, 1] = xy[:, 1] * r2
    A[::2, -2] = 1
    A[1::2, -1] = 1
    return A, xy


def run(p):
    k = float(p["radial_k1"])
    count = int(p["calibration_views"])
    broken = bool(p["broken_mode"])
    camera = views(np.arange(count))
    A, xy = design(camera, not broken)
    truth = np.array([800.0, 800 * k, 320.0, 240.0])
    full, _ = design(camera)
    obs = (full @ truth).reshape(-1, 2)
    j = np.repeat(np.arange(count), 12)
    i = np.tile(np.arange(12), count)
    obs += np.column_stack(
        [0.15 * np.sin(1.9 * i + 0.83 * j), 0.12 * np.cos(1.3 * i + 0.41 * j)]
    )
    coefficients = np.linalg.lstsq(A, obs.ravel(), rcond=None)[0]
    fitted = (
        coefficients
        if not broken
        else np.array([coefficients[0], 0.0, *coefficients[1:]])
    )
    heldout = views(np.array([0.37, 2.81, 8.43, 13.29]))
    H, hxy = design(heldout)
    predicted = (H @ fitted).reshape(-1, 2)
    expected = (H @ truth).reshape(-1, 2)
    residual = predicted - expected
    norms = np.linalg.norm(residual, axis=1)
    radius = np.linalg.norm(hxy, axis=1)
    edge = radius >= np.quantile(radius, 0.75)
    radial = np.linspace(0, max(np.linalg.norm(xy, axis=1).max(), radius.max()), 101)
    true_factor = 1 + k * radial**2
    fit_factor = 1 + fitted[1] / fitted[0] * radial**2
    metrics = [
        (
            "heldout_reprojection_rms",
            "Held-out reprojection RMS",
            np.sqrt(np.mean(norms**2)),
            "px",
        ),
        (
            "focal_bias_percent",
            "Focal-length bias",
            100 * abs(fitted[0] - 800) / 800,
            "%",
        ),
        (
            "outer_reprojection_rms",
            "Outer-region reprojection RMS",
            np.sqrt(np.mean(norms[edge] ** 2)),
            "px",
        ),
    ]
    plots = {
        "response": plot(
            "Held-out residuals",
            "Point index (1)",
            "Residual (px)",
            [
                trace(
                    "Residual",
                    np.arange(48),
                    norms,
                    "Point index",
                    "1",
                    "Residual",
                    "px",
                )
            ],
        ),
        "mechanism": plot(
            "Fitted radial model",
            "Radius (1)",
            "Radial factor (1)",
            [
                trace("True", radial, true_factor, "Radius", "1", "Radial factor", "1"),
                trace(
                    "Fitted", radial, fit_factor, "Radius", "1", "Radial factor", "1"
                ),
            ],
        ),
    }
    return finish(
        42,
        broken,
        {
            "sample_count": 48,
            "training_point_count": len(camera),
            "training_camera_points": camera,
            "observed_pixels": obs,
            "design_matrix": A,
            "rank": int(np.linalg.matrix_rank(A)),
            "condition": float(np.linalg.cond(A)),
            "coefficients": fitted,
            "estimated_k1": float(fitted[1] / fitted[0]),
            "heldout_camera_points": heldout,
            "heldout_true_pixels": expected,
            "heldout_predicted_pixels": predicted,
            "heldout_residuals": residual,
            "outer_mask": edge,
            "radius": radial,
            "true_radial_factor": true_factor,
            "fitted_radial_factor": fit_factor,
        },
        metrics,
        plots,
        "Known board poses make this a four-coefficient intrinsic fit. Forty-eight independent held-out points measure actual reprojection error; training rank is "
        + str(np.linalg.matrix_rank(A))
        + ".",
        "The fault omits the radial column while preserving observed lens distortion and the selected view count.",
        "Restore the full fit and inspect held-out and outer-region residuals. Zero true distortion can hide the missing-column fault.",
    )
