from __future__ import annotations

import numpy as np
from scipy.ndimage import convolve1d, map_coordinates, maximum_filter


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


def scene(angle):
    row, col = np.indices((96, 96), dtype=float)
    x, y = col - 47.5, row - 47.5
    c, s = np.cos(angle), np.sin(angle)
    base_x = c * x + s * y
    base_y = -s * x + c * y
    image = np.zeros((96, 96))
    centers = [(x, y) for y in (-24.0, 0.0, 24.0) for x in (-24.0, 0.0, 24.0)]
    for i, (cx, cy) in enumerate(centers):
        phi = 0.47 * i + 0.2
        dx, dy = base_x - cx, base_y - cy
        u = np.cos(phi) * dx + np.sin(phi) * dy
        v = -np.sin(phi) * dx + np.cos(phi) * dy
        patch = (
            0.25
            * (1 + np.tanh(u / 0.8))
            * (1 + np.tanh(v / 0.8))
            * np.exp(-(u * u + v * v) / 50)
        )
        texture = (
            1
            + 0.12 * np.cos((0.5 + 0.04 * i) * u)
            + 0.08 * np.sin((0.7 + 0.03 * i) * v)
        )
        image += (0.45 + 0.055 * i) * patch * texture
    return image


def detect(image, threshold):
    dx = convolve1d(image, [-0.5, 0, 0.5], axis=1, mode="nearest")
    dy = convolve1d(image, [-0.5, 0, 0.5], axis=0, mode="nearest")
    kernel = np.array([1.0, 4, 6, 4, 1]) / 16

    def smooth(x):
        return convolve1d(
            convolve1d(x, kernel, axis=0, mode="nearest"),
            kernel,
            axis=1,
            mode="nearest",
        )

    xx, xy, yy = smooth(dx * dx), smooth(dx * dy), smooth(dy * dy)
    score = xx * yy - xy * xy - 0.04 * (xx + yy) ** 2
    score[:8] = 0
    score[-8:] = 0
    score[:, :8] = 0
    score[:, -8:] = 0
    candidates = np.argwhere(
        (score >= threshold * score.max())
        & (score == maximum_filter(score, size=7, mode="nearest"))
        & (score > 0)
    )
    ordered = sorted(
        candidates.tolist(), key=lambda q: (-score[q[0], q[1]], q[0], q[1])
    )
    selected = []
    for r, c in ordered:
        if all((r - rr) ** 2 + (c - cc) ** 2 > 36 for rr, cc in selected):
            selected.append([r, c])
    return np.array(selected, int).reshape(-1, 2), score


def describe(image, points, normalize):
    dy, dx = np.mgrid[-6:7, -6:7]
    mask = dx * dx + dy * dy <= 36
    gy, gx = np.mgrid[-4:5, -4:5]
    out = []
    angles = []
    for row, col in points:
        patch = image[row - 6 : row + 7, col - 6 : col + 7]
        theta = (
            np.arctan2(np.sum(patch * dy * mask), np.sum(patch * dx * mask))
            if normalize
            else 0.0
        )
        angles.append(theta)
        c, s = np.cos(theta), np.sin(theta)
        xx = col + c * gx - s * gy
        yy = row + s * gx + c * gy
        values = map_coordinates(
            image, [yy.ravel(), xx.ravel()], order=1, mode="nearest"
        )
        values -= values.mean()
        norm = np.linalg.norm(values)
        out.append(values / max(norm, 1e-15))
    return np.array(out), np.array(angles)


def run(p):
    threshold = float(p["detector_threshold"])
    angle = np.deg2rad(float(p["image_rotation_deg"]))
    broken = bool(p["broken_mode"])
    a, b = scene(0), scene(angle)
    pa, ra = detect(a, threshold)
    pb, rb = detect(b, threshold)
    ca, sa = np.cos(angle), np.sin(angle)
    pred = (pa[:, ::-1] - 47.5) @ np.array([[ca, sa], [-sa, ca]]) + 47.5
    pairs = []
    used = set()
    for i, point in enumerate(pred):
        if not len(pb):
            break
        distance = np.linalg.norm(pb[:, ::-1] - point, axis=1)
        j = int(np.argmin(distance))
        if distance[j] <= 2.5 and j not in used:
            pairs.append((i, j))
            used.add(j)
    da, aa = describe(a, pa, not broken)
    db, ab = describe(b, pb, not broken)
    distances = np.array([np.linalg.norm(da[i] - db[j]) for i, j in pairs])
    indices = np.arange(len(distances))
    metrics = [
        (
            "geometric_repeatability",
            "Geometric repeatability",
            len(pairs) / max(1, len(pa)),
            "1",
        ),
        (
            "descriptor_distance",
            "Mean paired descriptor distance",
            distances.mean() if len(distances) else 0.0,
            "1",
        ),
        ("detected_features", "Rotated-image detections", len(pb), "count"),
    ]
    shown = heatmap(
        "Image", np.arange(96), np.arange(96), b, "Column", "px", "Row", "px"
    )
    plot_image = plot(
        "Detected corners",
        "Column (px)",
        "Row (px)",
        [shown, points("Corners", pb[:, 1], pb[:, 0], "Column", "px", "Row", "px")],
    )
    plot_image["layout"]["yaxis"]["autorange"] = "reversed"
    plots = {
        "response": plot_image,
        "mechanism": plot(
            "Paired patch distance",
            "Pair index (1)",
            "Distance (1)",
            [trace("Distance", indices, distances, "Pair index", "1", "Distance", "1")],
        ),
    }
    plots["response"]["layout"]["yaxis"].update(scaleanchor="x", scaleratio=1)
    plots["response"]["data"][0].update(
        colorscale=[[0, "#000000"], [1, "#ffffff"]], reversescale=False
    )
    plots["response"]["data"][0]["meta"]["z_quantity"] = "Image intensity"
    plots["response"]["data"][1]["marker"] = {"color": "#ea580c", "size": 6}
    plots["mechanism"]["layout"]["yaxis"].update(range=[0, 2], tickformat=".2f")
    if not len(distances):
        plots["mechanism"]["layout"]["annotations"] = [
            {
                "text": "No paired patches",
                "xref": "paper",
                "yref": "paper",
                "x": 0.5,
                "y": 0.5,
                "showarrow": False,
            }
        ]
    return finish(
        43,
        broken,
        {
            "sample_count": max(len(pa), len(pb)),
            "image_shape": [96, 96],
            "base_image": a,
            "rotated_image": b,
            "base_response": ra,
            "rotated_response": rb,
            "base_features": pa,
            "rotated_features": pb,
            "base_orientations": aa,
            "rotated_orientations": ab,
            "base_descriptors": da,
            "rotated_descriptors": db,
            "geometric_pairs": np.asarray(pairs, int).reshape(-1, 2),
            "descriptor_distances": distances,
            "matching_available": bool(len(pairs)),
            "descriptor_orientation_enabled": not broken,
        },
        metrics,
        plots,
        "Actual sampled images drive Harris corners and normalized intensity patches. Geometric evaluation pairs "
        + str(len(pairs))
        + " detections; descriptor distance is "
        + ("available." if len(pairs) else "unavailable (zero sentinel)."),
        "Only patch orientation normalization is disabled. Detector positions and geometric repeatability therefore remain unchanged between modes.",
        "Restore oriented sampling and compare the same geometric pairs. Zero rotation can hide the fault; this fixed-scale patch model is not SIFT.",
    )
