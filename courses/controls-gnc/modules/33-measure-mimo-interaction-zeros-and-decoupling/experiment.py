from __future__ import annotations

from typing import Any

import numpy as np

ITEM_NUMBER = 33
BROKEN_TEXT = 'Broken mode omits the decoupler and treats diagonal loop closures as independent despite measured cross-coupling.'
RECOVERY_TEXT = 'Compute RGA and transmission zeros first, then use a conditioned decoupler and report its off-diagonal residual rather than claiming perfect separation.'


def _trace(name: str, x: Any, y: Any, x_quantity: str, x_unit: str,
           y_quantity: str, y_unit: str, *, mode: str = "lines") -> dict[str, Any]:
    return {
        "type": "scattergl", "mode": mode, "name": name,
        "x": np.asarray(x, dtype=float), "y": np.asarray(y, dtype=float),
        "meta": {"x_quantity": x_quantity, "x_unit": x_unit,
                 "y_quantity": y_quantity, "y_unit": y_unit},
    }


def _plot(title: str, x_title: str, y_title: str,
          traces: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "data": traces,
        "layout": {
            "title": {"text": title, "x": 0.02},
            "xaxis": {"title": {"text": x_title}},
            "yaxis": {"title": {"text": y_title}},
            "legend": {"orientation": "h"},
            "margin": {"l": 72, "r": 36, "t": 62, "b": 62},
            "hovermode": "closest", "uirevision": "keep-view",
        },
        "config": {"responsive": True, "displaylogo": False},
    }


def _result(model: dict[str, Any], broken: bool) -> dict[str, Any]:
    return {
        "metrics": [
            {"id": key, "label": label, "value": float(value), "unit": unit,
              "emphasis": "primary" if index == 0 else "normal"}
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

def _model(p: dict[str, Any], broken: bool) -> dict[str, Any]:
    coupling = float(p["cross_coupling"])
    epsilon = float(p["decoupler_regularization"])
    G0 = np.array([[1.0, coupling/2.0], [coupling/6.0, 0.8]])
    rga = G0*np.linalg.inv(G0).T
    D = np.eye(2) if broken else np.linalg.inv(G0+epsilon*np.eye(2))
    decoupled = G0@D
    residual = float(np.linalg.norm(decoupled-np.diag(np.diag(decoupled)), ord="fro"))
    # det G numerator for G11=1/(s+1), G12=c/(s+2), G21=.5c/(s+3), G22=1.2/(s+1.5)
    zero_poly = 1.2*np.poly([-2.0, -3.0])-0.5*coupling**2*np.poly([-1.0, -1.5])
    zeros = np.roots(zero_poly)
    rightmost_zero = float(np.max(zeros.real))
    w = np.geomspace(0.02, 80.0, 240)
    sigmas, offdiag = [], []
    for omega in w:
        s = 1j*omega
        G = np.array([[1/(s+1), coupling/(s+2)], [0.5*coupling/(s+3), 1.2/(s+1.5)]])
        sigmas.append(np.linalg.svd(G, compute_uv=False))
        offdiag.append(np.linalg.norm((G@D)-np.diag(np.diag(G@D))))
    sigmas = np.asarray(sigmas)
    rga_offdiag = float(abs(rga[0, 1])+abs(rga[1, 0]))
    return {
        "signature": [rga_offdiag, rightmost_zero, residual],
        "metrics": [("rga_offdiag", "RGA off-diagonal sum", rga_offdiag, "1"),
                    ("transmission_zero", "Rightmost transmission zero", rightmost_zero, "1/s"),
                    ("decoupling_residual", "Static off-diagonal residual", residual, "1")],
        "plots": {
            "response": _plot("MIMO plant singular values", "Angular frequency (rad/s)", "Singular value magnitude (1)", [
                _trace("Maximum singular value", w, sigmas[:, 0], "Angular frequency", "rad/s", "Singular value magnitude", "1"),
                _trace("Minimum singular value", w, sigmas[:, 1], "Angular frequency", "rad/s", "Singular value magnitude", "1")]),
            "mechanism": _plot("Frequency-dependent decoupling residual", "Angular frequency (rad/s)", "Off-diagonal Frobenius norm (1)", [
                _trace("Applied decoupler", w, offdiag, "Angular frequency", "rad/s", "Off-diagonal Frobenius norm", "1"),
                _trace("Zero residual target", w, np.zeros_like(w), "Angular frequency", "rad/s", "Off-diagonal Frobenius norm", "1")]),
        },
        "observation": "Pairing, invertibility, and dynamic interaction are different tests; RGA, zeros, and residual conditioning must be read together."
    }


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    broken = bool(parameters["broken_mode"])
    return _result(_model(parameters, broken), broken)
