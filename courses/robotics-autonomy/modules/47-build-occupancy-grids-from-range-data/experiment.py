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


SIZE = 31
CELL = 0.1
LOW = -1.55
x = np.arange(SIZE) * CELL + LOW + CELL / 2
X, Y = np.meshgrid(x, x)
TRUTH = (
    (abs(X) >= 1.19)
    | (abs(Y) >= 1.19)
    | ((X >= 0.34) & (X <= 0.56) & (Y >= -0.21) & (Y <= 0.66))
    | ((X + 0.55) ** 2 + (Y + 0.4) ** 2 < 0.16**2)
)


def dda(angle):
    d = np.array([np.cos(angle), np.sin(angle)])
    cell = np.array([15, 15])
    step = np.sign(d).astype(int)
    side = np.array([0.05 / abs(a) if abs(a) > 1e-14 else np.inf for a in d])
    delta = np.array([CELL / abs(a) if abs(a) > 1e-14 else np.inf for a in d])
    out = []
    entry = 0.0
    for _ in range(100):
        col, row = cell
        if not (0 <= col < SIZE and 0 <= row < SIZE) or entry > 1.4:
            break
        hit = bool(TRUTH[row, col])
        out.append((row, col, hit, entry))
        if hit:
            break
        entry = min(side)
        if abs(side[0] - side[1]) <= 1e-12:
            cell += step
            side += delta
        elif side[0] < side[1]:
            cell[0] += step[0]
            side[0] += delta[0]
        else:
            cell[1] += step[1]
            side[1] += delta[1]
    return out


def run(p):
    strength = float(p["hit_probability"])
    count = int(p["beam_count"])
    broken = bool(p["broken_mode"])
    increment = np.log(strength / (1 - strength))
    odds = np.zeros((SIZE, SIZE))
    hit_mask = np.zeros_like(TRUTH)
    free_seen = np.zeros_like(TRUTH)
    paths = []
    angles = 0.013 + np.arange(count) * 2 * np.pi / count
    for angle in angles:
        path = dda(angle)
        paths.append(path)
        for row, col, hit, entry in path:
            if hit:
                odds[row, col] = np.clip(odds[row, col] + increment, -5, 5)
                hit_mask[row, col] = True
            else:
                free_seen[row, col] = True
                if not broken:
                    odds[row, col] = np.clip(odds[row, col] - increment, -5, 5)
    probability = 1 / (1 + np.exp(-odds))
    entropy = -np.sum(
        probability * np.log2(probability)
        + (1 - probability) * np.log2(1 - probability)
    )
    missed = np.mean(probability[~TRUTH] >= 0.45)
    metrics = [
        (
            "observed_hit_probability",
            "Mean probability at observed hits",
            probability[hit_mask].mean() if hit_mask.any() else 0.0,
            "1",
        ),
        ("map_entropy", "Sum of cell entropies", entropy, "bit"),
        ("unconfirmed_free_fraction", "Unconfirmed truth-free fraction", missed, "1"),
    ]
    row, col = np.nonzero(hit_mask)
    map_plot = plot(
        "Occupancy probability",
        "World x (m)",
        "World y (m)",
        [
            heatmap("Map", x, x, probability, "World x", "m", "World y", "m"),
            points("Hits", x[col], x[row], "World x", "m", "World y", "m"),
        ],
    )
    map_plot["data"][1]["marker"] = {"color": "#eab308", "size": 4}
    map_plot["data"][0].update(
        zmin=0, zmax=1, colorscale=[[0, "#ffffff"], [1, "#000000"]]
    )
    plots = {
        "response": map_plot,
        "mechanism": plot(
            "Central grid section",
            "World x (m)",
            "Occupancy (1)",
            [
                trace(
                    "Prob.",
                    x,
                    probability[15],
                    "World x",
                    "m",
                    "Occupancy probability",
                    "1",
                ),
                trace(
                    "Truth",
                    x,
                    TRUTH[15].astype(float),
                    "World x",
                    "m",
                    "Occupancy",
                    "1",
                ),
            ],
        ),
    }
    plots["response"]["layout"]["yaxis"].update(scaleanchor="x", scaleratio=1)
    plots["response"]["data"][0]["meta"]["z_quantity"] = "Occupancy probability"
    return finish(
        47,
        broken,
        {
            "sample_count": count,
            "grid_cell_count": SIZE * SIZE,
            "cell_size": CELL,
            "cell_centres": x,
            "truth": TRUTH,
            "angles": angles,
            "ray_paths": paths,
            "log_odds": odds,
            "probabilities": probability,
            "hit_mask": hit_mask,
            "traversed_free_mask": free_seen,
            "hit_probability_available": bool(hit_mask.any()),
            "entropy_bits": float(entropy),
        },
        metrics,
        plots,
        "Each beam traces actual grid cells. Unknown cells retain their 0.5 prior; unconfirmed free fraction includes unobserved and occluded truth-free cells.",
        "The fault adds occupied endpoints but omits traversed free-space updates. This loses free-space evidence; it does not create false-free cells.",
        "Restore free-cell updates from the same prior and beams. Repeated rays lower marginal entropy under the simplifying evidence model, without proving independent physical information.",
    )
