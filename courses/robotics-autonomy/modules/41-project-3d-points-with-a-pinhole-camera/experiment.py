from __future__ import annotations

import numpy as np


def trace(name, x, y, x_quantity, x_unit, y_quantity, y_unit):
    x, y = np.asarray(x, float), np.asarray(y, float)
    return {
        "type": "scatter",
        "mode": "lines+markers" if np.ptp(x) == 0 else "lines",
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


def run(p):
    focal = float(p["focal_length_px"])
    depth = float(p["point_depth_m"])
    broken = bool(p["broken_mode"])
    angle = 0.3
    R = np.array(
        [
            [np.cos(angle), 0, np.sin(angle)],
            [0, 1, 0],
            [-np.sin(angle), 0, np.cos(angle)],
        ]
    )
    camera = np.array([0.2, -0.1, 1.0])
    x = np.linspace(-0.4, 0.4, 121)
    world = np.column_stack(
        [x, np.full_like(x, 0.2), depth + np.linspace(-3.2, 0, 121)]
    )
    true = (world - camera) @ R
    used = world if broken else true
    valid = used[:, 2] > 0.05
    true_valid = true[:, 2] > 0.05
    pixels = focal * used[valid, :2] / used[valid, 2, None]
    physical_invalid = int(np.count_nonzero(~true_valid & valid))
    sensitivity = focal * np.linalg.norm(used[valid, :2], axis=1) / used[valid, 2] ** 2
    rays = np.column_stack([pixels / focal, np.ones(len(pixels))])
    reconstructed = rays * used[valid, 2, None]
    error = np.linalg.norm(reconstructed - true[valid], axis=1)
    # A second, always-visible depth sweep makes near-plane rejection observable even if all selected points are rejected.
    depths = np.linspace(0.1, 12, 121)
    center = np.column_stack([np.full(121, 0.4), np.full(121, 0.2), depths])
    ct = (center - camera) @ R
    uv = center if broken else ct
    mask = uv[:, 2] > 0.05
    u = focal * uv[mask, 0] / uv[mask, 2]
    metric = [
        (
            "image_radius",
            "Maximum accepted image radius",
            max(np.linalg.norm(pixels, axis=1), default=0.0),
            "px",
        ),
        (
            "depth_sensitivity",
            "Maximum accepted depth sensitivity",
            max(sensitivity, default=0.0),
            "px/m",
        ),
        (
            "behind_camera_count",
            "Invalid camera rays incorrectly accepted",
            physical_invalid,
            "count",
        ),
    ]
    plots = {
        "response": plot(
            "Projection over depth",
            "World depth (m)",
            "Image x (px)",
            [
                trace(
                    "Projection",
                    depths[mask],
                    u,
                    "World depth",
                    "m",
                    "Horizontal image coordinate",
                    "px",
                )
            ],
        ),
        "mechanism": plot(
            "Camera-frame depths",
            "World x (m)",
            "Camera depth (m)",
            [
                trace("Depth", x, true[:, 2], "World x", "m", "Camera depth", "m"),
                trace(
                    "Near plane",
                    x,
                    np.full(121, 0.05),
                    "World x",
                    "m",
                    "Camera depth",
                    "m",
                ),
            ],
        ),
    }
    return finish(
        41,
        broken,
        {
            "sample_count": 121,
            "world_points": world,
            "camera_rotation": R,
            "camera_origin": camera,
            "camera_points": true,
            "used_points": used,
            "accepted": valid,
            "projection_available": bool(np.any(valid)),
            "physically_valid": true_valid,
            "pixels": pixels,
            "depth_sensitivity": sensitivity,
            "reconstructed_points": reconstructed,
            "reconstruction_error": error,
            "rejected_count": int(sum(~valid)),
            "invalid_accepted_count": physical_invalid,
            "depth_sweep": depths,
            "depth_sweep_accepted": mask,
        },
        metric,
        plots,
        f"{int(sum(valid))} of 121 selected points are accepted; {physical_invalid} accepted rays violate the physical camera near plane. A zero pixel metric with no accepted rays means unavailable projection, not perfect accuracy.",
        "The fault omits camera pose, tests world Z as though it were camera Z, and projects those incorrectly framed points.",
        "Restore camera-frame transformation and depth rejection. At large positive depth the fault may accept no invalid rays yet still have a nonzero reconstruction error.",
    )
