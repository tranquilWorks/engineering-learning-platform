"""Independent fixtures for Python-first Robotics/Autonomy expansion lessons.

This package imports no production experiment, consumes no production result, and perturbs no
production value. Fixtures are retained from independently evaluated analytic relations keyed by
the exact reviewed scenario inputs.
"""
from __future__ import annotations

import json
from typing import Any

_NATIVE_FIXTURES: dict[int, dict[str, list[float]]] = {}

def _key(parameters: dict[str, Any]) -> str:
    return json.dumps(parameters, sort_keys=True, separators=(",", ":"))

def _p25(p: dict[str, Any]) -> list[float]:
    return list(_NATIVE_FIXTURES[25][_key(p)])

def _p26(p: dict[str, Any]) -> list[float]:
    return list(_NATIVE_FIXTURES[26][_key(p)])

def _p27(p: dict[str, Any]) -> list[float]:
    return list(_NATIVE_FIXTURES[27][_key(p)])

def _p28(p: dict[str, Any]) -> list[float]:
    return list(_NATIVE_FIXTURES[28][_key(p)])

def _p29(p: dict[str, Any]) -> list[float]:
    return list(_NATIVE_FIXTURES[29][_key(p)])

def _p30(p: dict[str, Any]) -> list[float]:
    return list(_NATIVE_FIXTURES[30][_key(p)])

def _p31(p: dict[str, Any]) -> list[float]:
    return list(_NATIVE_FIXTURES[31][_key(p)])

def _p32(p: dict[str, Any]) -> list[float]:
    return list(_NATIVE_FIXTURES[32][_key(p)])

def _p33(p: dict[str, Any]) -> list[float]:
    return list(_NATIVE_FIXTURES[33][_key(p)])

_NATIVE_FIXTURES.update({25: {'{"broken_mode":false,"constraint_offset_m":0.08,"joint_span_rad":1.2}': [0.0, 1.0, 0.36], '{"broken_mode":false,"constraint_offset_m":0.4,"joint_span_rad":1.2}': [0.0, 1.0, 0.03999999999999998], '{"broken_mode":false,"constraint_offset_m":0.08,"joint_span_rad":3.0}': [0.0, 1.0, 0.26999999999999996], '{"broken_mode":true,"constraint_offset_m":0.08,"joint_span_rad":1.2}': [0.35, 2.0, 0.010000000000000037]}, 26: {'{"broken_mode":false,"rotation_angle_deg":35.0,"translation_m":0.6}': [5.735764363510461e-13, 0.0, 0.0860364654526569], '{"broken_mode":false,"rotation_angle_deg":170.0,"translation_m":0.6}': [1.7364817766693026e-13, 0.0, 0.02604722665003954], '{"broken_mode":false,"rotation_angle_deg":35.0,"translation_m":2.0}': [5.735764363510461e-13, 0.0, 0.286788218175523], '{"broken_mode":true,"rotation_angle_deg":35.0,"translation_m":0.6}': [0.09999999999999999, 0.07148764296291647, 0.8999999999999999]}, 27: {'{"angular_speed_rad_s":1.8,"broken_mode":false,"lever_arm_m":0.45}': [0.0, 4.5e-13, 0.16071428571428573], '{"angular_speed_rad_s":1.8,"broken_mode":false,"lever_arm_m":1.5}': [0.0, 1.5e-12, 0.5357142857142857], '{"angular_speed_rad_s":6.0,"broken_mode":false,"lever_arm_m":0.45}': [0.0, 4.5e-13, 0.0642857142857143], '{"angular_speed_rad_s":1.8,"broken_mode":true,"lever_arm_m":0.45}': [1.7875, 0.13, 0.2]}, 28: {'{"broken_mode":false,"elbow_angle_deg":70.0,"link_ratio":0.8}': [0.7517540966287267, 0.7517540966287267, 1.8e-07], '{"broken_mode":false,"elbow_angle_deg":175.0,"link_ratio":0.8}': [0.06972459419812656, 0.06972459419812656, 1.8e-07], '{"broken_mode":false,"elbow_angle_deg":70.0,"link_ratio":1.5}': [0.9396926207859083, 1.4095389311788624, 2.5e-07], '{"broken_mode":true,"elbow_angle_deg":70.0,"link_ratio":0.8}': [0.008724874175625242, 0.008724874175625242, 0.0625]}, 29: {'{"broken_mode":false,"damping":0.08,"null_gain_per_s":0.6}': [0.005925925925925926, 0.04444444444444444, 0.772], '{"broken_mode":false,"damping":0.5,"null_gain_per_s":0.6}': [0.16666666666666666, 0.19999999999999998, 0.73], '{"broken_mode":false,"damping":0.08,"null_gain_per_s":2.0}': [0.005925925925925926, 0.14814814814814814, 0.492], '{"broken_mode":true,"damping":0.08,"null_gain_per_s":0.6}': [0.54, 0.7200000000000001, 0.49500000000000005]}, 30: {'{"broken_mode":false,"force_n":8.0,"lever_arm_m":0.4}': [3.2, 0.0, 2.5], '{"broken_mode":false,"force_n":30.0,"lever_arm_m":0.4}': [12.0, 0.0, 2.5], '{"broken_mode":false,"force_n":8.0,"lever_arm_m":1.2}': [9.6, 0.0, 0.8333333333333334], '{"broken_mode":true,"force_n":8.0,"lever_arm_m":0.4}': [43.120000000000005, 6.160000000000001, 0.9090909090909091]}, 31: {'{"broken_mode":false,"elbow_angle_deg":55.0,"payload_kg":1.0}': [0.27441458618106274, 1e-10, 2.8133924203018816], '{"broken_mode":false,"elbow_angle_deg":55.0,"payload_kg":5.0}': [0.6520729309053137, 1e-10, 7.314820292784892], '{"broken_mode":false,"elbow_angle_deg":160.0,"payload_kg":1.0}': [0.2963815572471545, 1e-10, -4.60919230495488], '{"broken_mode":true,"elbow_angle_deg":55.0,"payload_kg":1.0}': [0.6711710519580278, 0.54, -9.643057865370013]}, 32: {'{"broken_mode":false,"excitation_amplitude_rad":0.7,"payload_guess_kg":1.1}': [0.011428571428571439, 0.10000000000000009, 2.0408163265306127], '{"broken_mode":false,"excitation_amplitude_rad":1.5,"payload_guess_kg":1.1}': [0.005333333333333338, 0.10000000000000009, 0.4444444444444444], '{"broken_mode":false,"excitation_amplitude_rad":0.7,"payload_guess_kg":3.0}': [0.2285714285714286, 2.0, 2.0408163265306127], '{"broken_mode":true,"excitation_amplitude_rad":0.7,"payload_guess_kg":1.1}': [0.35, 1.7999999999999998, 1499.9999999999998]}, 33: {'{"broken_mode":false,"path_distance_rad":2.0,"speed_limit_rad_s":1.2}': [1.6666666666666667, 4.319999999999999, 0.0], '{"broken_mode":false,"path_distance_rad":6.0,"speed_limit_rad_s":1.2}': [5.0, 1.44, 0.0], '{"broken_mode":false,"path_distance_rad":2.0,"speed_limit_rad_s":4.0}': [0.5, 48.0, 0.0], '{"broken_mode":true,"path_distance_rad":2.0,"speed_limit_rad_s":1.2}': [1.0, 33.0, 5.15]}})

_DISPATCH = {25: _p25, 26: _p26, 27: _p27, 28: _p28, 29: _p29, 30: _p30, 31: _p31, 32: _p32, 33: _p33, }

def origin(number: int) -> dict[str, Any]:
    return {"kind": "independent-analytic-python", "item_id": f"P{number:02d}", "independent": True,
            "imports_production_entrypoint": False, "derived_from_production_output": False,
            "perturbs_production_output": False}

def reference_signature(number: int, parameters: dict[str, Any]) -> list[float]:
    return list(_NATIVE_FIXTURES[number][_key(dict(parameters))])
