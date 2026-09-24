from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np

ITEM_NUMBER = 53
DEFAULTS = {"record_limit": 60.0, "engine_scale_rpm_count": 0.25}
RANGES = {"record_limit": (12.0, 120.0), "engine_scale_rpm_count": (0.20, 0.30)}
BROKEN_TEXT = "Broken mode decodes documented big-endian CAN signal bytes as little-endian values, creating large engineering-unit residuals even though transport parity still passes."
RECOVERY_TEXT = "Preserve four-byte little-endian BLE CAN identifiers, compare the remaining bytes exactly with CAN payloads, and decode each declared signal with its documented byte order and scale."
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


def _trace(name: str, x: Any, y: Any, x_quantity: str, x_unit: str, y_quantity: str, y_unit: str) -> dict[str, Any]:
    return {"type": "scattergl", "mode": "lines+markers", "name": name, "x": np.asarray(x, dtype=float), "y": np.asarray(y, dtype=float), "meta": {"x_quantity": x_quantity, "x_unit": x_unit, "y_quantity": y_quantity, "y_unit": y_unit}}


def _plot(title: str, x_title: str, y_title: str, traces: list[dict[str, Any]]) -> dict[str, Any]:
    return {"data": traces, "layout": {"title": {"text": title, "x": 0.02}, "xaxis": {"title": {"text": x_title}}, "yaxis": {"title": {"text": y_title}}, "legend": {"orientation": "h"}, "margin": {"l": 72, "r": 36, "t": 62, "b": 62}, "hovermode": "closest", "uirevision": "keep-view"}, "config": {"responsive": True, "displaylogo": False}}


def _result(model: dict[str, Any], broken: bool) -> dict[str, Any]:
    return {"metrics": [{"id": key, "label": label, "value": float(value), "unit": unit, "emphasis": "primary" if index == 0 else "normal"} for index, (key, label, value, unit) in enumerate(model["metrics"])], "plots": model["plots"], "explanations": {"observation": model["observation"], "broken": BROKEN_TEXT, "recovery": RECOVERY_TEXT}, "diagnostics": {"item_number": ITEM_NUMBER, "broken_active": bool(broken), "signature": [float(value) for value in model["signature"]]}}


def _records(limit: int) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    can_path = FIXTURE_ROOT / "gr86-can-replay-v1.jsonl"
    ble_path = FIXTURE_ROOT / "racechrono-ble-replay-v1.jsonl"
    can = [json.loads(line) for line in can_path.read_text(encoding="utf-8").splitlines()[:limit]]
    ble = [json.loads(line) for line in ble_path.read_text(encoding="utf-8").splitlines()[:limit]]
    return can, ble


def _model(p: dict[str, float], broken: bool) -> dict[str, Any]:
    limit = round(p["record_limit"])
    scale = p["engine_scale_rpm_count"]
    can_records, ble_records = _records(limit)
    manifest = json.loads((FIXTURE_ROOT / "manifest.json").read_text(encoding="utf-8"))
    provenance_ok = manifest["fixture_set_id"] == "gr86-protocol-replay-v1" and manifest["provenance_class"] == "synthetic_protocol_fixture" and manifest["measured_vehicle_data"] is False
    parity_failures = 0
    engine_sequence, engine_decoded, engine_expected = [], [], []
    wheel_sequence, wheel_decoded, wheel_expected = [], [], []
    byte_order = "little" if broken else "big"
    for can, ble in zip(can_records, ble_records, strict=True):
        payload = bytes.fromhex(ble["payload_hex"])
        data = bytes.fromhex(can["data_hex"])
        parity_failures += int(
            can["sequence"] != ble["sequence"]
            or can["source_time_us"] != ble["source_time_us"]
            or int.from_bytes(payload[:4], "little") != int(can["can_id"], 16)
            or payload[4:] != data
        )
        if can["can_id"] == "0x118":
            value = int.from_bytes(data[:2], byte_order) * scale
            engine_sequence.append(can["sequence"])
            engine_decoded.append(value)
            engine_expected.append(can["decoded"]["engine_speed"]["value"])
        if can["can_id"] == "0x139":
            values = [int.from_bytes(data[index : index + 2], byte_order) / 128.0 for index in range(0, 8, 2)]
            expected = [can["decoded"][key]["value"] for key in ("wheel_speed_fl", "wheel_speed_fr", "wheel_speed_rl", "wheel_speed_rr")]
            wheel_sequence.append(can["sequence"])
            wheel_decoded.append(float(np.mean(values)))
            wheel_expected.append(float(np.mean(expected)))
    residuals = np.concatenate((np.asarray(engine_decoded) - engine_expected, np.asarray(wheel_decoded) - wheel_expected))
    decode_rmse = float(np.sqrt(np.mean(residuals**2)))
    signature = [float(limit), float(engine_decoded[-1]), float(np.mean(wheel_decoded)), float(parity_failures), float(provenance_ok), decode_rmse]
    return {
        "signature": signature,
        "metrics": [("records", "Replayed records", limit, "record"), ("engine_speed", "Last decoded engine speed", signature[1], "rpm"), ("wheel_speed", "Mean decoded wheel speed", signature[2], "km/h"), ("parity_failures", "CAN/BLE parity failures", parity_failures, "record"), ("provenance", "Synthetic fixture provenance verified", signature[4], "1"), ("decode_rmse", "Engineering-value decode RMSE", decode_rmse, "engineering unit")],
        "plots": {
            "response": _plot("Decoded telemetry", "Record sequence (1)", "Engineering value (mixed)", [_trace("Engine speed", engine_sequence, engine_decoded, "Record sequence", "1", "Engine speed", "rpm"), _trace("Mean wheel speed", wheel_sequence, wheel_decoded, "Record sequence", "1", "Wheel speed", "km/h")]),
            "mechanism": _plot("Decode reference comparison", "Decoded sample (1)", "Engineering value (mixed)", [_trace("Decoded engine", np.arange(len(engine_decoded)), engine_decoded, "Decoded sample", "1", "Engine speed", "rpm"), _trace("Expected engine", np.arange(len(engine_expected)), engine_expected, "Decoded sample", "1", "Engine speed", "rpm")]),
        },
        "observation": "Transport framing and engineering-value decoding are separate invariants: identical payload bytes do not prove that byte order and scale were interpreted correctly.",
    }


def run(parameters: dict[str, Any]) -> dict[str, Any]:
    values = _parameters(parameters)
    broken = bool(parameters.get("broken_mode", False))
    return _result(_model(values, broken), broken)
