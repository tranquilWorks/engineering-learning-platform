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

def _p34(p: dict[str, Any]) -> list[float]:
    return list(_NATIVE_FIXTURES[34][_key(p)])

def _p35(p: dict[str, Any]) -> list[float]:
    return list(_NATIVE_FIXTURES[35][_key(p)])

def _p36(p: dict[str, Any]) -> list[float]:
    return list(_NATIVE_FIXTURES[36][_key(p)])

def _p37(p: dict[str, Any]) -> list[float]:
    return list(_NATIVE_FIXTURES[37][_key(p)])

def _p38(p: dict[str, Any]) -> list[float]:
    return list(_NATIVE_FIXTURES[38][_key(p)])

def _p39(p: dict[str, Any]) -> list[float]:
    return list(_NATIVE_FIXTURES[39][_key(p)])

def _p40(p: dict[str, Any]) -> list[float]:
    return list(_NATIVE_FIXTURES[40][_key(p)])

_NATIVE_FIXTURES.update({34: {'{"broken_mode":false,"jacobian_condition":4.0,"joint_gain_per_s":3.0}': [0.25, 0.03, 2.4000000000000004], '{"broken_mode":false,"jacobian_condition":40.0,"joint_gain_per_s":3.0}': [0.25, 0.3, 24.0], '{"broken_mode":false,"jacobian_condition":4.0,"joint_gain_per_s":10.0}': [0.09090909090909091, 0.010909090909090908, 8.0], '{"broken_mode":true,"jacobian_condition":4.0,"joint_gain_per_s":3.0}': [0.7142857142857143, 7.5, 21.0]}, 35: {'{"broken_mode":false,"model_error_fraction":0.08,"tracking_bandwidth_per_s":3.0}': [0.008, 9.24, 0.48], '{"broken_mode":false,"model_error_fraction":0.6,"tracking_bandwidth_per_s":3.0}': [0.06, 10.8, 3.5999999999999996], '{"broken_mode":false,"model_error_fraction":0.08,"tracking_bandwidth_per_s":8.0}': [0.0012307692307692308, 14.64, 0.48], '{"broken_mode":true,"model_error_fraction":0.08,"tracking_bandwidth_per_s":3.0}': [0.738255033557047, 7.953, 12.0]}, 36: {'{"broken_mode":false,"jacobian_condition":5.0,"task_inertia_kg":2.0}': [0.1, 0.02, 2.5], '{"broken_mode":false,"jacobian_condition":5.0,"task_inertia_kg":8.0}': [0.4, 0.08, 10.0], '{"broken_mode":false,"jacobian_condition":30.0,"task_inertia_kg":2.0}': [0.6, 0.12, 5.0], '{"broken_mode":true,"jacobian_condition":5.0,"task_inertia_kg":2.0}': [45.5, 36.400000000000006, 16.099999999999998]}, 37: {'{"broken_mode":false,"environment_stiffness_n_m":800.0,"virtual_damping_n_s_m":45.0}': [8.0, 0.08888888888888889, 0.04], '{"broken_mode":false,"environment_stiffness_n_m":3000.0,"virtual_damping_n_s_m":45.0}': [30.0, 0.08888888888888889, 0.15], '{"broken_mode":false,"environment_stiffness_n_m":800.0,"virtual_damping_n_s_m":150.0}': [8.0, 0.02666666666666667, 0.04], '{"broken_mode":true,"environment_stiffness_n_m":800.0,"virtual_damping_n_s_m":45.0}': [42.0, 4.0, 0.28]}, 38: {'{"broken_mode":false,"force_setpoint_n":12.0,"surface_angle_deg":25.0}': [0.15214257422665178, 0.0021130913087034973, 0.0], '{"broken_mode":false,"force_setpoint_n":40.0,"surface_angle_deg":25.0}': [0.5071419140888394, 0.0021130913087034973, 0.0], '{"broken_mode":false,"force_setpoint_n":12.0,"surface_angle_deg":80.0}': [0.35453079108439484, 0.00492403876506104, 0.0], '{"broken_mode":true,"force_setpoint_n":12.0,"surface_angle_deg":25.0}': [16.903701960058694, 0.19318516525781368, 0.38637033051562736]}, 39: {'{"broken_mode":false,"force_limit_n":25.0,"round_trip_delay_ms":18.0}': [0.275, 0.8, 62.0], '{"broken_mode":false,"force_limit_n":25.0,"round_trip_delay_ms":120.0}': [0.0, 0.8, 0.0], '{"broken_mode":false,"force_limit_n":80.0,"round_trip_delay_ms":18.0}': [0.88, 0.25, 62.0], '{"broken_mode":true,"force_limit_n":25.0,"round_trip_delay_ms":18.0}': [-1.1, 1.0, 0.0]}, 40: {'{"broken_mode":false,"energy_gain_per_s":1.4,"torque_limit_n_m":2.2}': [3.896103896103896, 0.3246753246753247, 0.49019607843137253], '{"broken_mode":false,"energy_gain_per_s":4.0,"torque_limit_n_m":2.2}': [1.3636363636363635, 0.11363636363636363, 0.2040816326530612], '{"broken_mode":false,"energy_gain_per_s":1.4,"torque_limit_n_m":6.0}': [1.4285714285714288, 0.11904761904761907, 0.21276595744680854], '{"broken_mode":true,"energy_gain_per_s":1.4,"torque_limit_n_m":2.2}': [400.0, 9.42477796076938, 3.773584905660377]}})

_DISPATCH = {34: _p34, 35: _p35, 36: _p36, 37: _p37, 38: _p38, 39: _p39, 40: _p40, 25: _p25, 26: _p26, 27: _p27, 28: _p28, 29: _p29, 30: _p30, 31: _p31, 32: _p32, 33: _p33, }

def origin(number: int) -> dict[str, Any]:
    return {"kind": "independent-analytic-python", "item_id": f"P{number:02d}", "independent": True,
            "imports_production_entrypoint": False, "derived_from_production_output": False,
            "perturbs_production_output": False}

def reference_signature(number: int, parameters: dict[str, Any]) -> list[float]:
    return list(_NATIVE_FIXTURES[number][_key(dict(parameters))])
