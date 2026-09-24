from __future__ import annotations

import json
from collections import Counter
from itertools import pairwise
from pathlib import Path
from typing import Any

import numpy as np

ITEM_NUMBER = 60
DEFAULTS = {"inspection_limit": 309.0, "reorder_window": 2.0}
RANGES = {"inspection_limit": (100.0, 309.0), "reorder_window": (0.0, 4.0)}
BROKEN_TEXT = "Broken mode trusts arrival order, packet length, and uniqueness, so corrupted transport is misreported as a complete replay."
RECOVERY_TEXT = "Validate payload length against nominal DLC, remove duplicates, declare malformed records missing, and reorder only inversions covered by the bounded recovery window."
FIXTURE_ROOT = Path(__file__).resolve().parents[2] / "fixtures"


def _parameters(supplied: dict[str, Any]) -> dict[str, float]:
    result: dict[str, float] = {}
    for key, default in DEFAULTS.items():
        value = float(supplied.get(key, default))
        minimum, maximum = RANGES[key]
        if not np.isfinite(value) or value < minimum or value > maximum:
            raise ValueError(f"{key} outside declared finite range [{minimum}, {maximum}]")
        result[key] = value
    return result


def _trace(name: str, x: Any, y: Any, xq: str, xu: str, yq: str, yu: str) -> dict[str, Any]:
    return {"type": "scattergl", "mode": "lines+markers", "name": name, "x": np.asarray(x, dtype=float), "y": np.asarray(y, dtype=float), "meta": {"x_quantity": xq, "x_unit": xu, "y_quantity": yq, "y_unit": yu}}


def _plot(title: str, xt: str, yt: str, traces: list[dict[str, Any]]) -> dict[str, Any]:
    return {"data": traces, "layout": {"title": {"text": title, "x": 0.02}, "xaxis": {"title": {"text": xt}}, "yaxis": {"title": {"text": yt}}, "legend": {"orientation": "h"}, "margin": {"l": 72, "r": 36, "t": 62, "b": 62}, "hovermode": "closest", "uirevision": "keep-view"}, "config": {"responsive": True, "displaylogo": False}}


def _result(model: dict[str, Any], broken: bool) -> dict[str, Any]:
    return {"metrics": [{"id": key, "label": label, "value": float(value), "unit": unit, "emphasis": "primary" if index == 0 else "normal"} for index, (key, label, value, unit) in enumerate(model["metrics"])], "plots": model["plots"], "explanations": {"observation": model["observation"], "broken": BROKEN_TEXT, "recovery": RECOVERY_TEXT}, "diagnostics": {"item_number": ITEM_NUMBER, "broken_active": bool(broken), "signature": [float(value) for value in model["signature"]]}}


def _fixture(limit: int) -> tuple[list[dict[str, Any]], list[dict[str, Any]], bool]:
    nominal = [json.loads(line) for line in (FIXTURE_ROOT / "racechrono-ble-replay-v1.jsonl").read_text(encoding="utf-8").splitlines()[:limit]]
    plan = json.loads((FIXTURE_ROOT / "racechrono-ble-fault-plan-v1.json").read_text(encoding="utf-8"))
    manifest = json.loads((FIXTURE_ROOT / "manifest.json").read_text(encoding="utf-8"))
    provenance_ok = manifest["fixture_set_id"] == plan["fixture_set_id"] == "gr86-protocol-replay-v1" and manifest["provenance_class"] == "synthetic_protocol_fixture" and manifest["measured_vehicle_data"] is False
    corrupted = [dict(item) for item in nominal]
    for operation in plan["operations"]:
        if operation["kind"] == "drop":
            corrupted = [item for item in corrupted if item["sequence"] != operation["sequence"]]
        elif operation["kind"] == "duplicate" and operation["sequence"] < limit:
            location = next(index for index, item in enumerate(corrupted) if item["sequence"] == operation["sequence"])
            corrupted.insert(location + 1, dict(corrupted[location]))
        elif operation["kind"] == "swap_adjacent" and max(operation["sequences"]) < limit:
            first = next(index for index, item in enumerate(corrupted) if item["sequence"] == operation["sequences"][0])
            second = next(index for index, item in enumerate(corrupted) if item["sequence"] == operation["sequences"][1])
            corrupted[first], corrupted[second] = corrupted[second], corrupted[first]
        elif operation["kind"] == "truncate_payload" and operation["sequence"] < limit:
            item = next(value for value in corrupted if value["sequence"] == operation["sequence"])
            item["payload_hex"] = item["payload_hex"][: -2 * operation["remove_tail_bytes"]]
    return nominal, corrupted, provenance_ok


def _diagnose(limit: int, window: int, broken: bool) -> tuple[list[float], list[dict[str, Any]], list[int]]:
    nominal, corrupted, provenance_ok = _fixture(limit)
    if broken:
        residual = float(2 + 1 + 1 + 1 + abs(len(corrupted) - (limit - 2)) + 1)
        return [0.0, 0.0, 0.0, 0.0, float(len(corrupted)), 0.0, residual], corrupted, [item["sequence"] for item in corrupted]
    expected_lengths = {item["sequence"]: len(bytes.fromhex(item["payload_hex"])) for item in nominal}
    counts = Counter(item["sequence"] for item in corrupted)
    duplicates = {sequence for sequence, count in counts.items() if count > 1}
    inversions = [(left["sequence"], right["sequence"]) for left, right in pairwise(corrupted) if left["sequence"] > right["sequence"]]
    malformed = {item["sequence"] for item in corrupted if len(bytes.fromhex(item["payload_hex"])) != expected_lengths[item["sequence"]]}
    valid = {item["sequence"]: item for item in corrupted if item["sequence"] not in malformed}
    missing = set(range(limit)) - set(valid)
    recovered = sorted(valid)
    if inversions and window < max(left - right for left, right in inversions):
        recovered.remove(inversions[0][0])
    signature = [float(len(missing)), float(len(duplicates)), float(len(inversions)), float(len(malformed)), float(len(recovered)), float(provenance_ok), 0.0]
    return signature, corrupted, recovered


def _model(p: dict[str, float], broken: bool) -> dict[str, Any]:
    limit, window = round(p["inspection_limit"]), round(p["reorder_window"])
    signature, corrupted, recovered = _diagnose(limit, window, broken)
    arrival = np.arange(len(corrupted), dtype=float)
    sequence = np.array([item["sequence"] for item in corrupted], dtype=float)
    return {
        "signature": signature,
        "metrics": [("missing", "Missing sequences", signature[0], "record"), ("duplicates", "Duplicate sequences", signature[1], "record"), ("out_of_order", "Out-of-order pairs", signature[2], "pair"), ("malformed", "Malformed payloads", signature[3], "record"), ("recovered", "Recovered valid records", signature[4], "record"), ("provenance", "Fixture provenance verified", signature[5], "1"), ("diagnostic_residual", "Diagnostic ledger residual", signature[6], "record")],
        "plots": {"response": _plot("Corrupt replay arrival order", "Arrival index (1)", "Declared sequence (1)", [_trace("Corrupted replay", arrival, sequence, "Arrival index", "1", "Declared sequence", "1")]), "mechanism": _plot("Recovered sequence order", "Recovered index (1)", "Recovered sequence (1)", [_trace("Recovered replay", np.arange(len(recovered)), recovered, "Recovered index", "1", "Recovered sequence", "1")])},
        "observation": "Recovery is auditable only when missing, duplicate, inverted, and malformed records are separate diagnostics tied to a provenance-bearing nominal fixture.",
    }


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    values = _parameters(parameters)
    broken = bool(parameters.get("broken_mode", False))
    return _result(_model(values, broken), broken)
