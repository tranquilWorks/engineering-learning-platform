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


def data(fraction):
    i = np.arange(80)
    source = np.column_stack([20 + 15 * (i % 10), 30 + 12 * (i // 10)])
    truth = np.array([5.0, -3.0])
    delta = truth + 0.2 * np.column_stack(
        [np.sin(1.73 * i + 0.2), np.cos(2.21 * i - 0.3)]
    )
    mask = np.zeros(80, bool)
    mask[(np.arange(int(np.floor(80 * fraction))) * 37) % 80] = True
    angle = 2.399963229728653 * i[mask]
    radius = 18 + 6 * np.sin(1.13 * i[mask]) ** 2
    delta[mask] = (
        truth
        + [35, 15]
        + radius[:, None] * np.column_stack([np.cos(angle), np.sin(angle)])
    )
    return source, source + delta, mask, truth


def run(p):
    fraction = float(p["outlier_fraction"])
    threshold = float(p["ransac_threshold_px"])
    broken = bool(p["broken_mode"])
    source, target, outliers, truth = data(fraction)
    delta = target - source
    history = []
    candidates = []
    if broken:
        translation = delta.mean(axis=0)
        status = "all_data_least_squares"
    else:
        for i, t in enumerate(delta):
            residual = np.linalg.norm(delta - t, axis=1)
            mask = residual <= threshold
            candidates.append((-int(mask.sum()), float(np.sum(residual[mask] ** 2)), i))
        choice = min(candidates)[2]
        translation = delta[choice].copy()
        prior = None
        status = "maximum_refits"
        for _ in range(20):
            mask = np.linalg.norm(delta - translation, axis=1) <= threshold
            history.append(mask.copy())
            if prior is not None and np.array_equal(mask, prior):
                status = "stable_consensus"
                break
            if not mask.any():
                status = "no_consensus"
                break
            translation = delta[mask].mean(axis=0)
            prior = mask
    residual = np.linalg.norm(delta - translation, axis=1)
    accepted = residual <= threshold
    metrics = [
        ("accepted_fraction", "Accepted correspondence fraction", accepted.mean(), "1"),
        (
            "translation_error",
            "Translation error",
            np.linalg.norm(translation - truth),
            "px",
        ),
        (
            "false_acceptance",
            "True-outlier acceptance rate",
            np.sum(accepted & outliers) / max(1, outliers.sum()),
            "1",
        ),
    ]
    plots = {
        "response": plot(
            "Match residuals",
            "Match index (1)",
            "Residual (px)",
            [
                trace(
                    "Residual",
                    np.arange(80),
                    residual,
                    "Match index",
                    "1",
                    "Residual",
                    "px",
                ),
                trace(
                    "Limit",
                    np.arange(80),
                    np.full(80, threshold),
                    "Match index",
                    "1",
                    "Residual",
                    "px",
                ),
            ],
        ),
        "mechanism": plot(
            "Observed displacements",
            "Horizontal (px)",
            "Vertical (px)",
            [
                points(
                    "Matches",
                    delta[:, 0],
                    delta[:, 1],
                    "Horizontal displacement",
                    "px",
                    "Vertical displacement",
                    "px",
                ),
                points(
                    "Fitted",
                    [translation[0]],
                    [translation[1]],
                    "Horizontal displacement",
                    "px",
                    "Vertical displacement",
                    "px",
                ),
            ],
        ),
    }
    plots["mechanism"]["layout"]["yaxis"].update(scaleanchor="x", scaleratio=1)
    status_label = {
        "all_data_least_squares": "an all-data least-squares fit",
        "stable_consensus": "a stable refitted consensus",
        "maximum_refits": "the refit iteration limit",
        "no_consensus": "no supported fit",
    }[status]
    return finish(
        44,
        broken,
        {
            "sample_count": 80,
            "source_pixels": source,
            "target_pixels": target,
            "displacements": delta,
            "true_outliers": outliers,
            "true_translation": truth,
            "translation": translation,
            "residuals": residual,
            "accepted": accepted,
            "candidate_scores": candidates,
            "refit_masks": history,
            "solver_status": status,
            "consensus_available": bool(accepted.any()),
        },
        metrics,
        plots,
        "Eighty actual displacements are fitted in a translation-only model. Exhaustive single-match hypotheses and refits produce "
        + status_label
        + "; this is not random RANSAC confidence.",
        "The fault fits all observed displacements by least squares. The selected threshold still evaluates the resulting residuals.",
        "Restore consensus and inspect support, true translation error and false acceptance together. Coherent wrong matches can defeat consensus.",
    )
