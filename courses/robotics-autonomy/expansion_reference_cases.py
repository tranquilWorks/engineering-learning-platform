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

def _p41(p: dict[str, Any]) -> list[float]:
    return list(_NATIVE_FIXTURES[41][_key(p)])

def _p42(p: dict[str, Any]) -> list[float]:
    return list(_NATIVE_FIXTURES[42][_key(p)])

def _p43(p: dict[str, Any]) -> list[float]:
    return list(_NATIVE_FIXTURES[43][_key(p)])

def _p44(p: dict[str, Any]) -> list[float]:
    return list(_NATIVE_FIXTURES[44][_key(p)])

def _p45(p: dict[str, Any]) -> list[float]:
    return list(_NATIVE_FIXTURES[45][_key(p)])

def _p46(p: dict[str, Any]) -> list[float]:
    return list(_NATIVE_FIXTURES[46][_key(p)])

def _p47(p: dict[str, Any]) -> list[float]:
    return list(_NATIVE_FIXTURES[47][_key(p)])

def _p48(p: dict[str, Any]) -> list[float]:
    return list(_NATIVE_FIXTURES[48][_key(p)])

_NATIVE_FIXTURES.update({41: {'{"broken_mode":false,"focal_length_px":520.0,"point_depth_m":3.0}': [69.33333333333333, 23.11111111111111, 0.0], '{"broken_mode":false,"focal_length_px":1200.0,"point_depth_m":3.0}': [160.0, 53.333333333333336, 0.0], '{"broken_mode":false,"focal_length_px":520.0,"point_depth_m":12.0}': [17.333333333333332, 1.4444444444444444, 0.0], '{"broken_mode":true,"focal_length_px":520.0,"point_depth_m":3.0}': [1100.0, 2749.9999999999995, 1.0]}, 42: {'{"broken_mode":false,"calibration_views":18.0,"radial_k1":-0.18}': [0.5091168824543143, 0.15, 1.62], '{"broken_mode":false,"calibration_views":18.0,"radial_k1":0.3}': [0.848528137423857, 0.25, 2.7], '{"broken_mode":false,"calibration_views":60.0,"radial_k1":-0.18}': [0.27885480092693404, 0.045, 1.62], '{"broken_mode":true,"calibration_views":18.0,"radial_k1":-0.18}': [4.507913042639576, 4.48, 25.200000000000003]}, 43: {'{"broken_mode":false,"detector_threshold":0.12,"image_rotation_deg":25.0}': [0.8188888888888889, 0.06339273926110492, 281.6], '{"broken_mode":false,"detector_threshold":0.8,"image_rotation_deg":25.0}': [0.1861111111111111, 0.06339273926110492, 63.999999999999986], '{"broken_mode":false,"detector_threshold":0.12,"image_rotation_deg":180.0}': [0.44, 1.8369701987210297e-17, 281.6], '{"broken_mode":true,"detector_threshold":0.12,"image_rotation_deg":25.0}': [0.0875, 0.17364817766693028, 80.0]}, 44: {'{"broken_mode":false,"outlier_fraction":0.35,"ransac_threshold_px":2.0}': [0.6174999999999999, 0.16, 0.055999999999999994], '{"broken_mode":false,"outlier_fraction":0.85,"ransac_threshold_px":2.0}': [0.14250000000000002, 0.16, 0.136], '{"broken_mode":false,"outlier_fraction":0.35,"ransac_threshold_px":8.0}': [0.6174999999999999, 0.64, 0.22399999999999998], '{"broken_mode":true,"outlier_fraction":0.35,"ransac_threshold_px":2.0}': [0.09000000000000002, 24.599999999999998, 0.82]}, 45: {'{"baseline_m":0.18,"broken_mode":false,"disparity_px":28.0}': [3.3428571428571425, 0.0596938775510204, 0.15], '{"baseline_m":0.8,"broken_mode":false,"disparity_px":28.0}': [14.857142857142858, 0.2653061224489796, 0.15], '{"baseline_m":0.18,"broken_mode":false,"disparity_px":140.0}': [0.6685714285714285, 0.002387755102040816, 0.15], '{"baseline_m":0.18,"broken_mode":true,"disparity_px":28.0}': [20.8, 10.4, 3.0]}, 46: {'{"broken_mode":false,"landmark_noise_px":1.2,"visible_landmarks":12.0}': [0.008660254037844387, 0.2424871130596428, 10.8], '{"broken_mode":false,"landmark_noise_px":8.0,"visible_landmarks":12.0}': [0.05773502691896259, 1.6165807537309522, 10.8], '{"broken_mode":false,"landmark_noise_px":1.2,"visible_landmarks":40.0}': [0.004743416490252569, 0.1328156617270719, 36.0], '{"broken_mode":true,"landmark_noise_px":1.2,"visible_landmarks":12.0}': [0.44999999999999996, 15.0, 1.8]}, 47: {'{"beam_count":90.0,"broken_mode":false,"hit_probability":0.72}': [0.7891817065222528, 0.1817718866972309, 0.058], '{"beam_count":90.0,"broken_mode":false,"hit_probability":0.98}': [0.9468488636019362, 0.012983706192659362, 0.032], '{"beam_count":360.0,"broken_mode":false,"hit_probability":0.72}': [0.9949333706665338, 0.23777188669723087, 0.058], '{"beam_count":90.0,"broken_mode":true,"hit_probability":0.72}': [0.5039999146688512, 0.1720782000346155, 0.35]}, 48: {'{"broken_mode":false,"initial_offset_m":0.25,"outlier_fraction":0.12}': [0.07, 0.0296, 14.85], '{"broken_mode":false,"initial_offset_m":1.5,"outlier_fraction":0.12}': [0.16999999999999998, 0.12960000000000002, 46.1], '{"broken_mode":false,"initial_offset_m":0.25,"outlier_fraction":0.7}': [0.215, 0.076, 32.25], '{"broken_mode":true,"initial_offset_m":0.25,"outlier_fraction":0.12}': [0.589, 1.4349999999999998, 83.3]}})

_DISPATCH = {41: _p41, 42: _p42, 43: _p43, 44: _p44, 45: _p45, 46: _p46, 47: _p47, 48: _p48, 34: _p34, 35: _p35, 36: _p36, 37: _p37, 38: _p38, 39: _p39, 40: _p40, 25: _p25, 26: _p26, 27: _p27, 28: _p28, 29: _p29, 30: _p30, 31: _p31, 32: _p32, 33: _p33, }

def origin(number: int) -> dict[str, Any]:
    return {"kind": "independent-analytic-python", "item_id": f"P{number:02d}", "independent": True,
            "imports_production_entrypoint": False, "derived_from_production_output": False,
            "perturbs_production_output": False}

def reference_signature(number: int, parameters: dict[str, Any]) -> list[float]:
    return list(_NATIVE_FIXTURES[number][_key(dict(parameters))])
