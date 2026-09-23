"""Independent fixtures for Python-first Robotics/Autonomy expansion lessons.

This package imports no production experiment, consumes no production result, and perturbs no
production value. Fixtures are retained from independently evaluated analytic relations keyed by
the exact reviewed scenario inputs.
"""
from __future__ import annotations

import json
from typing import Any

import numpy as np

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

def _p49(p: dict[str, Any]) -> list[float]:
    ratio = float(p["rate_ratio"])
    excitation = 0.0 if p["broken_mode"] else float(p["excitation_level"])
    duration = 6.0
    omega = 2.0 * np.pi * 0.35
    rows: list[np.ndarray] = []
    for time_s in np.linspace(0.0, duration, round(duration * ratio) + 1):
        command = excitation * (
            np.sin(omega * time_s) + 0.35 * np.cos(0.5 * omega * time_s)
        )
        rows.append(np.array([0.0, 0.0, command / 0.04, 1.0 / 0.04]))
    for time_s in np.arange(0.0, duration + 0.5, 1.0):
        integrated = excitation * (
            time_s / omega
            - np.sin(omega * time_s) / omega**2
            + 1.4 * (1.0 - np.cos(0.5 * omega * time_s)) / omega**2
        )
        rows.append(np.array([1.0, time_s, integrated, 0.5 * time_s**2]) / 0.08)
    matrix = np.vstack(rows)
    information = matrix.T @ matrix
    singular = np.linalg.svd(information, compute_uv=False)
    rank = int(np.sum(singular > singular[0] * 1.0e-9))
    if rank < 4:
        return [float(rank), 1.0e12, 1.0e6]
    return [
        float(rank),
        float(singular[0] / singular[-1]),
        float(np.trace(np.linalg.inv(information))),
    ]

def _p50(p: dict[str, Any]) -> list[float]:
    gate = float(p["gate_sigma"])
    outlier = float(p["outlier_sigma"])
    if p["broken_mode"]:
        gate, outlier = 0.6, 11.0
    norms = np.array([np.hypot(0.60, -0.40), np.hypot(outlier, 0.35 * outlier)])
    accepted = np.ones(2, dtype=bool) if p["broken_mode"] else norms <= gate
    if p["broken_mode"]:
        costs = 0.5 * norms**2
    else:
        costs = np.where(norms <= 1.5, 0.5 * norms**2, 1.5 * (norms - 0.75))
    return [float(accepted[0]), float(not accepted[1]), float(np.sum(costs[accepted]))]

def _p51(p: dict[str, Any]) -> list[float]:
    count = round(float(p["pose_count"]))
    loop_noise = float(p["loop_noise_m"])
    broken = bool(p["broken_mode"])
    phase = np.linspace(0.0, 2.0 * np.pi, count)
    truth = np.column_stack((4.0 * np.cos(phase), 2.5 * np.sin(phase)))
    edge_phase = np.linspace(0.0, 2.0 * np.pi, count - 1, endpoint=False)
    odometry = np.diff(truth, axis=0) + 0.012 * np.column_stack(
        (np.sin(edge_phase), -0.6 * np.cos(edge_phase))
    )
    estimate = np.vstack((truth[0], truth[0] + np.cumsum(odometry, axis=0)))
    estimate += 0.08 * np.column_stack((np.sin(1.7 * phase), np.cos(1.3 * phase)))
    if broken:
        estimate += np.array([0.40, -0.30])
    loop_measurement = truth[0] - truth[-1] + loop_noise * np.array([1.0, -0.5])
    landmarks = np.array([[-1.5, 0.8], [1.2, -0.9]])

    def system() -> tuple[np.ndarray, np.ndarray]:
        residuals: list[float] = []
        rows: list[np.ndarray] = []

        def vector_factor(value: np.ndarray, blocks: dict[int, np.ndarray], sigma: float) -> None:
            jacobian = np.zeros((len(value), 2 * count))
            for pose, block in blocks.items():
                jacobian[:, 2 * pose:2 * pose + 2] = block
            residuals.extend((value / sigma).tolist())
            rows.extend(jacobian / sigma)

        if not broken:
            vector_factor(estimate[0] - truth[0], {0: np.eye(2)}, 0.02)
        for index, measurement in enumerate(odometry):
            vector_factor(
                estimate[index + 1] - estimate[index] - measurement,
                {index: -np.eye(2), index + 1: np.eye(2)},
                0.05,
            )
        vector_factor(
            estimate[-1] - estimate[0] - loop_measurement,
            {0: -np.eye(2), count - 1: np.eye(2)},
            max(loop_noise, 0.02),
        )
        if not broken:
            for pose in range(0, count, max(1, count // 10)):
                for landmark_index, landmark in enumerate(landmarks):
                    offset = estimate[pose] - landmark
                    distance = max(float(np.linalg.norm(offset)), 1.0e-9)
                    measured = float(np.linalg.norm(truth[pose] - landmark)) + 0.015 * np.sin(
                        0.7 * pose + landmark_index
                    )
                    row = np.zeros(2 * count)
                    row[2 * pose:2 * pose + 2] = offset / distance / 0.04
                    rows.append(row)
                    residuals.append((distance - measured) / 0.04)
        return np.asarray(residuals), np.vstack(rows)

    condition = 0.0
    for _ in range(1 if broken else 7):
        residual, jacobian = system()
        normal_singular = np.linalg.svd(jacobian.T @ jacobian, compute_uv=False)
        condition = (
            1.0e12
            if normal_singular[-1] <= normal_singular[0] * 1.0e-12
            else float(normal_singular[0] / normal_singular[-1])
        )
        increment = np.linalg.lstsq(jacobian, -residual, rcond=1.0e-10)[0]
        estimate += increment.reshape((-1, 2))
        if float(np.linalg.norm(increment)) < 1.0e-9:
            break
    return [
        float(np.sqrt(np.mean(np.sum((estimate - truth) ** 2, axis=1)))),
        float(np.linalg.norm(estimate[0] - truth[0])),
        condition,
    ]

def _p52(p: dict[str, Any]) -> list[float]:
    score = float(p["descriptor_score"])
    residual = float(p["geometric_residual_m"])
    broken = bool(p["broken_mode"])
    if broken:
        score, residual = 0.95, 1.8
    normalized = residual / 0.30
    inserted = score >= 0.70 and (residual <= 0.30 or broken)
    influence = 1.0 if broken else min(1.0, 1.0 / max(abs(normalized), 1.0))
    weight = score * influence if inserted else 0.0
    cost = (
        0.5 * normalized**2
        if broken
        else (0.5 * abs(normalized) ** 2 if abs(normalized) <= 1.0 else abs(normalized) - 0.5)
    )
    return [weight, cost, weight * residual * (2.0 if broken else 0.20)]

def _p53(p: dict[str, Any]) -> list[float]:
    acceleration_sigma = float(p["process_noise"])
    position_sigma = float(p["measurement_noise"])
    broken = bool(p["broken_mode"])
    count = 81
    dt = 0.1
    time_s = np.arange(count, dtype=float) * dt
    truth = np.zeros((count, 2))
    truth[0] = [0.0, 0.8]
    for index in range(count - 1):
        acceleration = 0.05 * np.sin(0.55 * time_s[index])
        truth[index + 1] = [
            truth[index, 0] + dt * truth[index, 1] + 0.5 * dt**2 * acceleration,
            truth[index, 1] + dt * acceleration,
        ]
    measurements = truth[:, 0] + position_sigma * (
        0.72 * np.sin(1.91 * np.arange(count)) + 0.28 * np.cos(0.73 * np.arange(count))
    )
    transition = np.array([[1.0, dt], [0.0, 1.0]])
    gain_vector = np.array([0.5 * dt**2, dt])
    process_covariance = acceleration_sigma**2 * np.outer(gain_vector, gain_vector) + 1.0e-10 * np.eye(2)
    measurement_variance = max(position_sigma, 1.0e-4) ** 2
    filtered = np.zeros((count, 2))
    filtered_covariance = np.zeros((count, 2, 2))
    predicted = np.zeros((count, 2))
    predicted_covariance = np.zeros((count, 2, 2))
    filtered[0] = [measurements[0], 0.5]
    filtered_covariance[0] = np.diag([measurement_variance, 0.5])
    heldout = np.arange(count) % 5 == 0
    for index in range(1, count):
        predicted[index] = transition @ filtered[index - 1]
        predicted_covariance[index] = transition @ filtered_covariance[index - 1] @ transition.T + process_covariance
        if heldout[index]:
            filtered[index] = predicted[index]
            filtered_covariance[index] = predicted_covariance[index]
        else:
            innovation = measurements[index] - predicted[index, 0]
            innovation_variance = predicted_covariance[index, 0, 0] + measurement_variance
            gain = predicted_covariance[index, :, 0] / innovation_variance
            filtered[index] = predicted[index] + gain * innovation
            filtered_covariance[index] = (np.eye(2) - np.outer(gain, [1.0, 0.0])) @ predicted_covariance[index]
    estimate = filtered.copy()
    covariance = filtered_covariance.copy()
    if broken:
        covariance *= 0.12
    else:
        for index in range(count - 2, -1, -1):
            smoothing_gain = filtered_covariance[index] @ transition.T @ np.linalg.inv(predicted_covariance[index + 1])
            estimate[index] += smoothing_gain @ (estimate[index + 1] - predicted[index + 1])
            covariance[index] += smoothing_gain @ (covariance[index + 1] - predicted_covariance[index + 1]) @ smoothing_gain.T
    error = estimate[:, 0] - truth[:, 0]
    normalized_error = error**2 / np.maximum(covariance[:, 0, 0], 1.0e-12)
    return [
        float(np.sqrt(np.mean(error**2))),
        float(np.mean(normalized_error <= 3.841458820694124)),
        float(np.sqrt(np.mean((estimate[heldout, 0] - measurements[heldout]) ** 2))),
    ]

_NATIVE_FIXTURES.update({49: {'{"broken_mode":false,"excitation_level":0.6,"rate_ratio":10.0}': [4.0, 467.44921906856433, 0.003734438153009505], '{"broken_mode":false,"excitation_level":0.6,"rate_ratio":40.0}': [4.0, 785.9063711313481, 0.0033415647978850085], '{"broken_mode":false,"excitation_level":2.0,"rate_ratio":10.0}': [4.0, 548.018463472212, 0.003615206250568606], '{"broken_mode":true,"excitation_level":0.6,"rate_ratio":10.0}': [3.0, 1000000000000.0, 1000000.0]}, 50: {'{"broken_mode":false,"gate_sigma":3.0,"outlier_sigma":5.0}': [1.0, 1.0, 0.26000000000000006], '{"broken_mode":false,"gate_sigma":8.0,"outlier_sigma":5.0}': [1.0, 0.0, 7.081107537656409], '{"broken_mode":false,"gate_sigma":3.0,"outlier_sigma":12.0}': [1.0, 1.0, 0.26000000000000006], '{"broken_mode":true,"gate_sigma":3.0,"outlier_sigma":5.0}': [1.0, 0.0, 68.17125]}, 51: {'{"broken_mode":false,"loop_noise_m":0.08,"pose_count":30.0}': [0.012172684762798827, 0.002303392270687024, 85.82395855625573], '{"broken_mode":false,"loop_noise_m":0.5,"pose_count":30.0}': [0.009589522618660204, 0.0023757197396582458, 160.20210140185935], '{"broken_mode":false,"loop_noise_m":0.08,"pose_count":100.0}': [0.01886875988544594, 0.001850431361698094, 611.2830315135892], '{"broken_mode":true,"loop_noise_m":0.08,"pose_count":30.0}': [0.5491952667579718, 0.46016263875887276, 1000000000000.0]}, 52: {'{"broken_mode":false,"descriptor_score":0.78,"geometric_residual_m":0.12}': [0.78, 0.08000000000000002, 0.01872], '{"broken_mode":false,"descriptor_score":1.0,"geometric_residual_m":0.12}': [1.0, 0.08000000000000002, 0.024], '{"broken_mode":false,"descriptor_score":0.78,"geometric_residual_m":2.0}': [0.0, 6.166666666666667, 0.0], '{"broken_mode":true,"descriptor_score":0.78,"geometric_residual_m":0.12}': [0.95, 18.0, 3.42]}, 53: {'{"broken_mode":false,"measurement_noise":0.15,"process_noise":0.06}': [0.034830218840569104, 0.9629629629629629, 0.09936613216746079], '{"broken_mode":false,"measurement_noise":0.15,"process_noise":0.5}': [0.007120494350136375, 1.0, 0.09037480200978411], '{"broken_mode":false,"measurement_noise":1.0,"process_noise":0.06}': [0.07283725335437781, 1.0, 0.6161368231469574], '{"broken_mode":true,"measurement_noise":0.15,"process_noise":0.06}': [0.056480195906314846, 0.43209876543209874, 0.10642418417035024]}})

def _p54(p: dict[str, Any]) -> list[float]:
    start, goal = (2, 4), (21, 4)
    occupied = {(11, y) for y in range(16) if y not in {4, 12}}
    weight = float(p["heuristic_weight"])

    def neighbors(node: tuple[int, int]) -> list[tuple[int, int]]:
        if node in occupied:
            return []
        x, y = node
        return [candidate for candidate in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1))
                if 0 <= candidate[0] < 24 and 0 <= candidate[1] < 16 and candidate not in occupied]

    g: dict[tuple[int, int], float] = {}
    rhs: dict[tuple[int, int], float] = {start: 0.0}
    versions: dict[tuple[int, int], int] = {}
    queue: list[tuple[float, float, int, tuple[int, int]]] = []

    def value(table: dict[tuple[int, int], float], node: tuple[int, int]) -> float:
        return table.get(node, float("inf"))

    def key(node: tuple[int, int]) -> tuple[float, float]:
        best = min(value(g, node), value(rhs, node))
        return best + weight * (abs(node[0] - goal[0]) + abs(node[1] - goal[1])), best

    def push(node: tuple[int, int]) -> None:
        version = versions.get(node, 0) + 1
        versions[node] = version
        first, second = key(node)
        queue.append((first, second, version, node))

    def update(node: tuple[int, int]) -> None:
        if node != start:
            rhs[node] = min((value(g, predecessor) + 1.0 for predecessor in neighbors(node)),
                            default=float("inf"))
        versions[node] = versions.get(node, 0) + 1
        if value(g, node) != value(rhs, node):
            push(node)

    def compute() -> int:
        expansions = 0
        while True:
            valid = [entry for entry in queue
                     if entry[2] == versions.get(entry[3]) and entry[:2] == key(entry[3])]
            top = min(valid) if valid else None
            if top is None or (top[:2] >= key(goal) and value(rhs, goal) == value(g, goal)):
                return expansions
            queue.remove(top)
            node = top[3]
            if value(g, node) > value(rhs, node):
                g[node] = value(rhs, node)
                for successor in neighbors(node):
                    update(successor)
            else:
                g[node] = float("inf")
                update(node)
                for successor in neighbors(node):
                    update(successor)
            expansions += 1

    def extract() -> list[tuple[int, int]]:
        path = [goal]
        while path[-1] != start:
            path.append(min(neighbors(path[-1]), key=lambda node: (value(g, node) + 1.0, node)))
        return list(reversed(path))

    push(start)
    compute()
    original = extract()
    occupied.add((11, 4))
    update((11, 4))
    for adjacent in ((10, 4), (12, 4), (11, 3), (11, 5)):
        update(adjacent)
    repair = 0 if p["broken_mode"] else compute()
    path = original if p["broken_mode"] else extract()

    frontier = [(0.0, 0.0, start)]
    best = {start: 0.0}
    settled: set[tuple[int, int]] = set()
    while frontier:
        entry = min(frontier)
        frontier.remove(entry)
        _, cost, node = entry
        if node in settled:
            continue
        settled.add(node)
        if node == goal:
            break
        for neighbor in neighbors(node):
            candidate = cost + 1.0
            if candidate < best.get(neighbor, float("inf")):
                best[neighbor] = candidate
                frontier.append((candidate, candidate, neighbor))
    return [
        (len(path) - 1) * float(p["grid_resolution_m"]),
        float(sum(node in occupied for node in path)),
        repair / max(len(settled), 1),
    ]


def _halton(index: int, base: int) -> float:
    value, denominator = 0.0, 1.0
    while index:
        index, remainder = divmod(index, base)
        denominator *= base
        value += remainder / denominator
    return value


def _circle_segment_distance(a: np.ndarray, b: np.ndarray, center: np.ndarray) -> float:
    delta = b - a
    fraction = np.clip(np.dot(center - a, delta) / max(np.dot(delta, delta), 1.0e-12), 0.0, 1.0)
    return float(np.linalg.norm(a + fraction * delta - center))


def _p55(p: dict[str, Any]) -> list[float]:
    obstacles = ((4.1, 3.1, 1.05), (6.4, 2.35, 0.95))
    nodes = [np.array([0.5, 0.5]), np.array([9.5, 5.5])]
    index = 1
    while len(nodes) < round(float(p["sample_count"])) + 2:
        point = np.array([10.0 * _halton(index, 2), 6.0 * _halton(index, 3)])
        index += 1
        if all(np.linalg.norm(point - np.array([cx, cy])) > radius + 0.25
               for cx, cy, radius in obstacles):
            nodes.append(point)
    adjacency: list[list[tuple[int, float]]] = [[] for _ in nodes]
    radius = float(p["connection_radius_m"])

    def clear(a: np.ndarray, b: np.ndarray) -> bool:
        return all(_circle_segment_distance(a, b, np.array([cx, cy])) > obstacle_radius + 0.25
                   for cx, cy, obstacle_radius in obstacles)

    for left in range(len(nodes)):
        for right in range(left + 1, len(nodes)):
            distance = float(np.linalg.norm(nodes[left] - nodes[right]))
            if distance <= radius and (p["broken_mode"] or clear(nodes[left], nodes[right])):
                adjacency[left].append((right, distance))
                adjacency[right].append((left, distance))
    queue = [(0.0, 0)]
    best = {0: 0.0}
    parent: dict[int, int] = {}
    settled: set[int] = set()
    while queue:
        entry = min(queue)
        queue.remove(entry)
        cost, node = entry
        if node in settled:
            continue
        settled.add(node)
        if node == 1:
            break
        for neighbor, length in adjacency[node]:
            candidate = cost + length
            if candidate < best.get(neighbor, float("inf")):
                best[neighbor] = candidate
                parent[neighbor] = node
                queue.append((candidate, neighbor))
    path = [1]
    while path[-1] != 0:
        path.append(parent[path[-1]])
    path.reverse()
    collisions = sum(not clear(nodes[path[i]], nodes[path[i + 1]]) for i in range(len(path) - 1))
    return [best[1], float(collisions), len(settled) / len(nodes)]


def _p56(p: dict[str, Any]) -> list[float]:
    obstacles = ((4.2, 2.7, 1.15), (6.5, 3.5, 1.0))
    start, goal = np.array([0.5, 0.5]), np.array([9.5, 5.5])

    def clear(a: np.ndarray, b: np.ndarray) -> bool:
        return all(_circle_segment_distance(a, b, np.array([cx, cy])) > radius + 0.2
                   for cx, cy, radius in obstacles)

    nodes = [start.copy()]
    parent = [0]
    costs = [0.0]
    rewires = 0
    radius = float(p["rewire_radius_m"])
    for sample_index in range(1, round(float(p["sample_count"])) + 1):
        sample = goal if sample_index % 12 == 0 else np.array([
            10.0 * _halton(sample_index, 2), 6.0 * _halton(sample_index, 3)
        ])
        nearest = int(np.argmin([np.linalg.norm(node - sample) for node in nodes]))
        direction = sample - nodes[nearest]
        distance = float(np.linalg.norm(direction))
        new = sample.copy() if distance <= 0.68 else nodes[nearest] + 0.68 * direction / distance
        if not (0.0 <= new[0] <= 10.0 and 0.0 <= new[1] <= 6.0) or not clear(nodes[nearest], new):
            continue
        near = [idx for idx, node in enumerate(nodes) if np.linalg.norm(node - new) <= radius]
        chosen = nearest
        chosen_cost = costs[nearest] + float(np.linalg.norm(nodes[nearest] - new))
        if not p["broken_mode"]:
            for candidate in near:
                alternative = costs[candidate] + float(np.linalg.norm(nodes[candidate] - new))
                if alternative < chosen_cost and clear(nodes[candidate], new):
                    chosen, chosen_cost = candidate, alternative
        nodes.append(new)
        parent.append(chosen)
        costs.append(chosen_cost)
        added = len(nodes) - 1
        if not p["broken_mode"]:
            for candidate in near:
                alternative = chosen_cost + float(np.linalg.norm(nodes[candidate] - new))
                if candidate != chosen and alternative + 1.0e-12 < costs[candidate] and clear(new, nodes[candidate]):
                    descendants = [candidate]
                    for descendant in descendants:
                        descendants.extend(idx for idx, ancestor in enumerate(parent)
                                           if ancestor == descendant and idx != descendant)
                    delta = alternative - costs[candidate]
                    parent[candidate] = added
                    for descendant in descendants:
                        costs[descendant] += delta
                    rewires += 1
    choices = [costs[index] + float(np.linalg.norm(node - goal))
               for index, node in enumerate(nodes)
               if np.linalg.norm(node - goal) <= 2.2 and clear(node, goal)]
    best_cost = min(choices)
    lower = float(np.linalg.norm(goal - start))
    return [best_cost, float(rewires), best_cost / lower - 1.0]


def _p57(p: dict[str, Any]) -> list[float]:
    obstacles = ((4.0, 0.45, 1.0), (6.3, -0.35, 0.9))
    robot_radius = float(p["robot_radius_m"])
    path = [np.array(point, dtype=float) for point in (
        (0.0, 0.0), (2.2, 0.0), (3.0, 2.15), (5.2, 2.55),
        (7.3, 2.0), (8.3, 0.1), (10.0, 0.0)
    )]

    def clearance(a: np.ndarray, b: np.ndarray, footprint: float) -> float:
        return min(_circle_segment_distance(a, b, np.array([cx, cy])) - radius - footprint
                   for cx, cy, radius in obstacles)

    for attempt in range(round(float(p["smoothing_iterations"]))):
        if len(path) <= 2:
            continue
        span = len(path) - 1
        left = attempt % (len(path) - 2)
        right = min(len(path) - 1, left + 2 + (attempt // max(len(path) - 2, 1)) % max(span - left - 1, 1))
        if right <= left + 1:
            continue
        if p["broken_mode"]:
            acceptable = clearance(path[left], path[left], 0.0) >= 0.0 and clearance(path[right], path[right], 0.0) >= 0.0
        else:
            acceptable = clearance(path[left], path[right], robot_radius) >= 0.0
        if acceptable:
            path = path[:left + 1] + path[right:]
    margins = [clearance(path[index], path[index + 1], robot_radius)
               for index in range(len(path) - 1)]
    length = sum(float(np.linalg.norm(path[index + 1] - path[index]))
                 for index in range(len(path) - 1))
    return [length, min(margins), float(sum(margin < 0.0 for margin in margins))]


def _p58(p: dict[str, Any]) -> list[float]:
    center = np.array([5.0, 0.0])
    clearance = float(p["required_clearance_m"])
    safety = 1.1 + clearance
    smoothness = float(p["smoothness_weight"])
    obstacle_weight = 0.0 if p["broken_mode"] else 80.0
    fractions = np.linspace(0.0, 1.0, 31)
    height = 0.0 if p["broken_mode"] else safety + 0.65
    points = np.column_stack((10.0 * fractions, height * np.sin(np.pi * fractions)))

    def margin(a: np.ndarray, b: np.ndarray) -> float:
        return _circle_segment_distance(a, b, center) - safety

    def objective(path: np.ndarray) -> float:
        second = path[:-2] - 2.0 * path[1:-1] + path[2:]
        first = path[1:] - path[:-1]
        violations = np.maximum(safety - np.linalg.norm(path[1:-1] - center, axis=1), 0.0)
        return (smoothness * float(np.sum(second**2)) + 0.03 * float(np.sum(first**2))
                + obstacle_weight * float(np.sum(violations**2)))

    def gradient(path: np.ndarray) -> np.ndarray:
        result = np.zeros_like(path)
        for index in range(1, len(path) - 1):
            second = path[index - 1] - 2.0 * path[index] + path[index + 1]
            result[index - 1] += 2.0 * smoothness * second
            result[index] -= 4.0 * smoothness * second
            result[index + 1] += 2.0 * smoothness * second
        for index in range(1, len(path) - 1):
            result[index] += 0.06 * (2.0 * path[index] - path[index - 1] - path[index + 1])
            offset = path[index] - center
            distance = float(np.linalg.norm(offset))
            if distance < safety:
                result[index] -= 2.0 * obstacle_weight * (safety - distance) * offset / max(distance, 1.0e-9)
        result[[0, -1]] = 0.0
        return result

    def project(path: np.ndarray) -> np.ndarray:
        result = path.copy()
        for _ in range(12):
            changed = False
            for index in range(len(result) - 1):
                signed = margin(result[index], result[index + 1])
                if signed >= -1.0e-9:
                    continue
                midpoint = 0.5 * (result[index] + result[index + 1])
                direction = midpoint - center
                direction /= max(float(np.linalg.norm(direction)), 1.0e-9)
                correction = (-signed + 1.0e-6) * direction
                if index > 0:
                    result[index] += correction
                if index + 1 < len(result) - 1:
                    result[index + 1] += correction
                changed = True
            if not changed:
                break
        return result

    current = objective(points)
    for _ in range(1200):
        derivative = gradient(points)
        step = 0.01
        candidate = points.copy()
        for _ in range(12):
            candidate = points - step * derivative
            candidate[[0, -1]] = points[[0, -1]]
            if not p["broken_mode"]:
                candidate = project(candidate)
            value = objective(candidate)
            if value <= current + 1.0e-12:
                break
            step *= 0.5
        points, current = candidate, value
    margins = [margin(points[index], points[index + 1]) for index in range(len(points) - 1)]
    length = float(np.sum(np.linalg.norm(points[1:] - points[:-1], axis=1)))
    return [length, min(margins), float(sum(value < -1.0e-7 for value in margins))]


def _p59(p: dict[str, Any]) -> list[float]:
    acceleration_limit = float(p["acceleration_limit_m_s2"])
    speed_limit = float(p["speed_limit_m_s"])
    if p["broken_mode"]:
        return [8.0 / speed_limit, max(speed_limit / 0.5 - acceleration_limit, 0.0), speed_limit]
    start = (0.0, 0.0)
    queue = [(8.0 / speed_limit, 0.0, start)]
    best = {start: 0.0}
    settled: set[tuple[float, float]] = set()
    while queue:
        entry = min(queue)
        queue.remove(entry)
        _, elapsed, state = entry
        if state in settled:
            continue
        settled.add(state)
        position, speed = state
        if abs(position - 8.0) <= 0.13 and abs(speed) <= 1.0e-9:
            return [elapsed, 0.0, abs(speed)]
        if elapsed >= 20.0:
            continue
        for acceleration in (-acceleration_limit, 0.0, acceleration_limit):
            next_speed = speed + acceleration * 0.5
            if next_speed < -1.0e-9 or next_speed > speed_limit + 1.0e-9:
                continue
            next_position = position + speed * 0.5 + 0.5 * acceleration * 0.5**2
            if next_position < -0.01 or next_position > 8.13:
                continue
            next_state = (round(next_position, 6), round(next_speed, 6))
            candidate = elapsed + 0.5
            if candidate + 1.0e-12 < best.get(next_state, float("inf")):
                best[next_state] = candidate
                heuristic = max(8.0 - next_position, 0.0) / max(speed_limit, 1.0e-9)
                queue.append((candidate + heuristic, candidate, next_state))
    raise RuntimeError("independent kinodynamic search has no solution")


def _p60(p: dict[str, Any]) -> list[float]:
    horizon = 1 if p["broken_mode"] else round(float(p["prediction_horizon_steps"]))
    obstacle_speed = float(p["obstacle_speed_m_s"])
    x, y, lateral_speed, obstacle_y = 0.0, 0.0, 0.0, -2.0
    robot = [np.array([x, y])]
    separations = [float(np.hypot(x - 5.0, y - obstacle_y))]

    def cost(acceleration: float) -> float:
        predicted_y, predicted_speed = y, lateral_speed
        total = 0.0
        for step in range(1, horizon + 1):
            predicted_speed = float(np.clip(predicted_speed + acceleration * 0.2, -1.1, 1.1))
            predicted_y += predicted_speed * 0.2
            robot_x = x + 1.25 * 0.2 * step
            moving_y = obstacle_y if p["broken_mode"] else obstacle_y + obstacle_speed * 0.2 * step
            separation = float(np.hypot(robot_x - 5.0, predicted_y - moving_y))
            total += 1200.0 * max(0.9 - separation, 0.0) ** 2
            if separation < 0.9:
                total += 80.0
            total += 0.035 * predicted_y**2 + 0.01 * predicted_speed**2
        return total + 0.12 * acceleration**2 + 0.4 * predicted_y**2

    for _ in range(40):
        candidates = (-1.2, -0.6, 0.0, 0.6, 1.2)
        acceleration = min(candidates, key=lambda action: (cost(action), abs(action), action))
        lateral_speed = float(np.clip(lateral_speed + acceleration * 0.2, -1.1, 1.1))
        x += 1.25 * 0.2
        y += lateral_speed * 0.2
        obstacle_y += obstacle_speed * 0.2
        robot.append(np.array([x, y]))
        separations.append(float(np.hypot(x - 5.0, y - obstacle_y)))
    points = np.asarray(robot)
    path_length = float(np.sum(np.linalg.norm(points[1:] - points[:-1], axis=1)))
    return [min(separations), float(sum(value < 0.9 for value in separations)), path_length]


def _p61(p: dict[str, Any]) -> list[float]:
    friction = float(p["friction_coefficient"])
    radius = 0.06
    angles = (np.pi, np.deg2rad(float(p["contact_misalignment_deg"])))
    columns: list[np.ndarray] = []
    for index, angle in enumerate(angles):
        position = radius * np.array([np.cos(angle), np.sin(angle)])
        normal = -position / radius
        if p["broken_mode"] and index == 1:
            normal = -normal
        tangent = np.array([-normal[1], normal[0]])
        for sign in (-1.0, 1.0):
            force = normal + sign * friction * tangent
            moment = position[0] * force[1] - position[1] * force[0]
            columns.append(np.array([force[0], force[1], moment / radius]))
    matrix = np.column_stack(columns)
    _, singular, right = np.linalg.svd(matrix)
    rank = int(np.sum(singular > singular[0] * 1.0e-10))
    equilibrium = right[-1]
    if np.min(-equilibrium) > np.min(equilibrium):
        equilibrium = -equilibrium
    if abs(float(np.sum(equilibrium))) < 1.0e-12:
        margin = -float(np.linalg.norm(matrix @ equilibrium))
    else:
        weights = equilibrium / float(np.sum(equilibrium))
        residual = float(np.linalg.norm(matrix @ weights))
        if rank == 3 and np.min(weights) > 1.0e-9 and residual < 1.0e-8:
            margin = float(np.min(weights))
        else:
            margin = -max(residual, float(max(-np.min(weights), 0.0)))
    target = np.array([0.0, 7.5, -2.0])
    coefficients = np.zeros(matrix.shape[1])
    step = 0.8 / max(float(np.linalg.norm(matrix, 2) ** 2), 1.0e-9)
    for _ in range(240):
        load_residual = matrix @ coefficients - target
        coefficients = np.maximum(coefficients - step * matrix.T @ load_residual, 0.0)
    return [margin, float(np.linalg.norm(matrix @ coefficients - target)),
            float(np.sum(coefficients))]


def _p62(p: dict[str, Any]) -> list[float]:
    def rotation(angle: float) -> np.ndarray:
        return np.array([[np.cos(angle), -np.sin(angle)],
                         [np.sin(angle), np.cos(angle)]])

    translation = np.array([0.28, 0.12])
    true_yaw = np.deg2rad(25.0)
    object_camera = np.array([0.72, 0.18])
    true_object = translation + rotation(true_yaw) @ object_camera
    noise = 0.01 * float(p["vision_noise_cm"])
    measured = object_camera + noise * np.array([0.60, -0.35])
    if p["broken_mode"]:
        estimate = measured
    else:
        estimate = translation + rotation(
            true_yaw + np.deg2rad(float(p["camera_yaw_error_deg"]))
        ) @ measured
    first, second = 0.75, 0.55
    cosine = (float(estimate @ estimate) - first**2 - second**2) / (2.0 * first * second)
    reachable = abs(cosine) <= 1.0
    elbow = -float(np.arccos(np.clip(cosine, -1.0, 1.0)))
    shoulder = float(np.arctan2(estimate[1], estimate[0])
                     - np.arctan2(second * np.sin(elbow), first + second * np.cos(elbow)))
    endpoint = np.array([first * np.cos(shoulder) + second * np.cos(shoulder + elbow),
                         first * np.sin(shoulder) + second * np.sin(shoulder + elbow)])
    error = float(np.linalg.norm(endpoint - true_object))
    margin = first + second - float(np.linalg.norm(estimate))
    states = 9 if reachable and error <= 0.055 else 4
    return [error, margin, float(states)]


def _p63(p: dict[str, Any]) -> list[float]:
    first, second = 0.75, 0.55
    target = np.array([float(p["target_distance_m"]), 0.35])

    def solve(relative: np.ndarray) -> tuple[np.ndarray, float] | None:
        cosine = (float(relative @ relative) - first**2 - second**2) / (2.0 * first * second)
        if abs(cosine) > 1.0:
            return None
        elbow = -float(np.arccos(np.clip(cosine, -1.0, 1.0)))
        shoulder = float(np.arctan2(relative[1], relative[0])
                         - np.arctan2(second * np.sin(elbow), first + second * np.cos(elbow)))
        return np.array([shoulder, elbow]), first * second * abs(float(np.sin(elbow)))

    if p["broken_mode"]:
        base = 0.0
        solution = solve(1.30 * target / float(np.linalg.norm(target)))
        assert solution is not None
        joints, manipulability = solution
    else:
        candidates: list[tuple[float, float, np.ndarray, float]] = []
        for base_candidate in np.linspace(0.0, 1.45, 59):
            solution = solve(target - np.array([base_candidate, 0.0]))
            if solution is None:
                continue
            joints_candidate, manipulability_candidate = solution
            score = (float(p["base_motion_weight"]) * base_candidate
                     + 0.18 / max(manipulability_candidate + 0.025, 1.0e-9))
            candidates.append((score, base_candidate, joints_candidate,
                               manipulability_candidate))
        _, base, joints, manipulability = min(candidates, key=lambda item: (item[0], item[1]))
    endpoint = np.array([
        base + first * np.cos(joints[0]) + second * np.cos(np.sum(joints)),
        first * np.sin(joints[0]) + second * np.sin(np.sum(joints)),
    ])
    return [float(np.linalg.norm(endpoint - target)), manipulability, abs(base)]


def _p64(p: dict[str, Any]) -> list[float]:
    corridor = float(p["corridor_width_m"])
    actual = corridor - 0.01 * float(p["geometry_error_cm"])

    def search(blocked: set[tuple[str, str]]) -> list[tuple[str, str, float]]:
        edges = {"start": [("approach", 2.0)], "approach": [("top", 1.0), ("side", 1.6)],
                 "top": [("goal", 4.0)], "side": [("goal", 4.5)]}
        required = {("top", "goal"): 0.24, ("side", "goal"): 0.16}
        queue: list[tuple[float, str, list[tuple[str, str, float]]]] = [(0.0, "start", [])]
        best = {"start": 0.0}
        while queue:
            entry = min(queue, key=lambda item: (item[0], item[1]))
            queue.remove(entry)
            cost, state, path = entry
            if state == "goal":
                return path
            if cost > best.get(state, float("inf")) + 1.0e-12:
                continue
            for target, duration in edges.get(state, []):
                edge = (state, target)
                if edge in blocked or corridor + 1.0e-12 < required.get(edge, 0.0):
                    continue
                candidate = cost + duration
                if candidate < best.get(target, float("inf")) - 1.0e-12:
                    best[target] = candidate
                    queue.append((candidate, target, path + [(state, target, duration)]))
        raise RuntimeError("independent task graph exhausted")

    blocked: set[tuple[str, str]] = set()
    plan = search(blocked)
    replans = 0
    total = 0.0
    success = False
    while True:
        failure: tuple[str, str] | None = None
        for source, target, duration in plan:
            total += duration
            if target == "goal":
                required = 0.24 if source == "top" else 0.16
                if actual - required < -1.0e-12:
                    failure = (source, target)
                    break
                success = True
        if success or failure is None or p["broken_mode"]:
            break
        blocked.add(failure)
        replans += 1
        total += 1.0
        plan = [edge for edge in search(blocked) if edge[0] != "start"]
    return [float(success), float(replans), total]


def _p65(p: dict[str, Any]) -> list[float]:
    first = [(0, 2), (1, 2), (2, 2), (3, 2), (4, 2)]
    buffer = round(float(p["reservation_buffer_steps"]))
    delay = round(float(p["robot_b_start_delay_steps"]))

    def at(path: list[tuple[int, int]], time: int) -> tuple[int, int]:
        return path[min(max(time, 0), len(path) - 1)]

    def reserved(current: tuple[int, int], candidate: tuple[int, int], time: int) -> bool:
        if any(candidate == at(first, tau)
               for tau in range(max(0, time - buffer), time + buffer + 1)):
            return True
        return candidate == at(first, time - 1) and current == at(first, time)

    if p["broken_mode"]:
        second = [(2, 0)] * (delay + 1) + [(2, 1), (2, 2), (2, 3), (2, 4)]
    else:
        start, goal = (2, 0), (2, 4)
        queue: list[tuple[int, int, tuple[int, int], list[tuple[int, int]]]] = [
            (4, delay, start, [start] * (delay + 1))
        ]
        best = {(start, delay): delay}
        actions = ((0, 0), (0, 1), (1, 0), (-1, 0), (0, -1))
        second = []
        while queue:
            entry = min(queue, key=lambda item: (item[0], item[1], item[2]))
            queue.remove(entry)
            _, time, state, path = entry
            if state == goal:
                second = path
                break
            if time >= 18:
                continue
            for dx, dy in actions:
                candidate = (state[0] + dx, state[1] + dy)
                next_time = time + 1
                if not (0 <= candidate[0] <= 4 and 0 <= candidate[1] <= 4):
                    continue
                if reserved(state, candidate, next_time):
                    continue
                key = (candidate, next_time)
                if next_time >= best.get(key, 10**9):
                    continue
                best[key] = next_time
                heuristic = abs(candidate[0] - goal[0]) + abs(candidate[1] - goal[1])
                queue.append((next_time + heuristic, next_time, candidate, path + [candidate]))
        if not second:
            raise RuntimeError("independent reservation search found no path")
    conflicts = 0
    separations = []
    for time in range(max(len(first), len(second))):
        a, b = at(first, time), at(second, time)
        separations.append(float(np.hypot(a[0] - b[0], a[1] - b[1])))
        if a == b:
            conflicts += 1
        if time > 0 and at(first, time - 1) == b and at(second, time - 1) == a:
            conflicts += 1
    return [float(conflicts), float(max(len(first), len(second)) - 1), min(separations)]


def _p66(p: dict[str, Any]) -> list[float]:
    def transform(x: float, y: float, angle: float) -> np.ndarray:
        return np.array([[np.cos(angle), -np.sin(angle), x],
                         [np.sin(angle), np.cos(angle), y], [0.0, 0.0, 1.0]])

    def chain(joints: np.ndarray) -> np.ndarray:
        return (transform(0.20, 0.10, 0.15)
                @ transform(0.0, 0.0, joints[0]) @ transform(0.70, 0.0, 0.0)
                @ transform(0.0, 0.0, joints[1]) @ transform(0.50, 0.0, 0.0))

    true_joints = np.array([0.55, -0.85])
    scale = 2.0 * np.pi / 4096.0
    counts = true_joints / scale
    decoded = counts * scale * (1.0 + 0.01 * float(p["encoder_scale_error_percent"]))
    integrated = np.rad2deg(decoded) if p["broken_mode"] else decoded
    truth, model = chain(true_joints), chain(integrated)
    error = float(np.linalg.norm(model[:2, 2] - truth[:2, 2]))
    inverse = float(np.linalg.norm(model @ np.linalg.inv(model) - np.eye(3)))
    violations = int(abs(float(p["timestamp_skew_ms"])) > 20.0)
    if p["broken_mode"]:
        violations += 2
    return [error, inverse, float(violations)]


def _p67(p: dict[str, Any]) -> list[float]:
    dropout = 0.001 * float(p["dropout_duration_ms"])
    drift = 1.0e-6 * float(p["clock_drift_ppm"])
    times = np.arange(0.0, 2.0001, 0.02)
    truth = np.sin(1.4 * times)
    velocity = 1.4 * np.cos(1.4 * times)
    present = ~((times >= 0.80) & (times < 0.80 + dropout))
    indices = np.flatnonzero(present)
    arrival = times[indices] * (1.0 + drift) + 0.018 * np.sin(1.7 * indices)
    faults = 0
    recovery_latency = 0.0
    replay_times: list[float] = []
    replay_values: list[float] = []
    if p["broken_mode"]:
        order = indices[np.argsort(arrival)]
        estimate = 0.0
        previous_arrival = 0.0
        last_velocity = velocity[0]
        for index in order:
            event_arrival = times[index] * (1.0 + drift) + 0.018 * np.sin(1.7 * index)
            estimate += last_velocity * max(event_arrival - previous_arrival, 0.0)
            estimate = 0.92 * estimate + 0.08 * truth[index]
            last_velocity = velocity[index]
            previous_arrival = event_arrival
            replay_times.append(float(times[index]))
            replay_values.append(estimate)
        reference = np.sin(1.4 * np.asarray(replay_times))
        recovery_latency = 1000.0
    else:
        estimate = truth[0]
        last_velocity = velocity[0]
        last_measurement = 0.0
        gap_seen = False
        for index, time_s in enumerate(times):
            if index > 0:
                estimate += last_velocity * 0.02
            if present[index]:
                gap = time_s - last_measurement
                if gap > 0.060001:
                    faults += 1
                    gap_seen = True
                    estimate = truth[index]
                    recovery_latency = 20.0
                else:
                    estimate = 0.35 * estimate + 0.65 * truth[index]
                last_velocity = velocity[index]
                last_measurement = time_s
            replay_values.append(float(estimate))
        if abs(float(p["clock_drift_ppm"])) > 150.0:
            faults += 1
        if not gap_seen:
            recovery_latency = 0.0
        reference = truth
    error = float(np.sqrt(np.mean((np.asarray(replay_values) - reference) ** 2)))
    return [error, float(faults), recovery_latency]


def _p68(p: dict[str, Any]) -> list[float]:
    def grid_path(occupied: set[tuple[int, int]]) -> list[tuple[int, int]]:
        start, goal = (0, 0), (8, 0)
        queue: list[tuple[int, int, tuple[int, int], list[tuple[int, int]]]] = [(8, 0, start, [start])]
        best = {start: 0}
        for _ in range(200):
            if not queue:
                break
            entry = min(queue, key=lambda item: (item[0], item[1], item[2]))
            queue.remove(entry)
            _, cost, state, path = entry
            if state == goal:
                return path
            for dx, dy in ((1, 0), (0, 1), (0, -1), (-1, 0)):
                candidate = (state[0] + dx, state[1] + dy)
                if not (0 <= candidate[0] <= 8 and 0 <= candidate[1] <= 2):
                    continue
                if candidate in occupied:
                    continue
                next_cost = cost + 1
                if next_cost >= best.get(candidate, 10**9):
                    continue
                best[candidate] = next_cost
                heuristic = abs(candidate[0] - goal[0]) + abs(candidate[1] - goal[1])
                queue.append((next_cost + heuristic, next_cost, candidate, path + [candidate]))
        raise RuntimeError("independent capstone grid has no path")

    broken = bool(p["broken_mode"])
    discovered = (4, 0)
    path = grid_path(set() if broken else {discovered})
    collision = int(discovered in path)
    crossing = float(next(i for i, point in enumerate(path) if point == (6, 0)))
    speed = float(p["dynamic_obstacle_speed_m_s"])
    if not broken:
        while abs(-2.0 + speed * crossing) < 0.85:
            crossing += 1.0
    separation = abs(-2.0 + speed * crossing)
    dropout = float(p["range_dropout_percent"])
    margins = np.array([1.0 if collision == 0 else -1.0,
                        (separation - 0.85) / 0.85,
                        (50.0 - dropout) / 50.0,
                        1.0 if not broken else -1.0,
                        1.0 if (dropout == 0.0 or not broken) else -1.0])
    violations = int(np.sum(margins < -1.0e-12))
    return [float(violations == 0), separation, float(violations)]


def _p69(p: dict[str, Any]) -> list[float]:
    def rotation(angle: float) -> np.ndarray:
        return np.array([[np.cos(angle), -np.sin(angle)],
                         [np.sin(angle), np.cos(angle)]])

    broken = bool(p["broken_mode"])
    noise = 0.01 * float(p["vision_noise_cm"])
    friction = float(p["contact_friction_coefficient"])
    camera = np.array([0.72, 0.18])
    true_point = np.array([0.28, 0.12]) + rotation(np.deg2rad(25.0)) @ camera
    measured = camera + noise * np.array([0.5, -0.25])
    estimate = measured if broken else np.array([0.28, 0.12]) + rotation(np.deg2rad(25.0)) @ measured
    first, second = 0.75, 0.55
    cosine = (float(estimate @ estimate) - first**2 - second**2) / (2.0 * first * second)
    reachable = abs(cosine) <= 1.0
    elbow = -float(np.arccos(np.clip(cosine, -1.0, 1.0)))
    shoulder = float(np.arctan2(estimate[1], estimate[0])
                     - np.arctan2(second * np.sin(elbow), first + second * np.cos(elbow)))
    endpoint = np.array([first * np.cos(shoulder) + second * np.cos(shoulder + elbow),
                         first * np.sin(shoulder) + second * np.sin(shoulder + elbow)])
    pickup_error = float(np.linalg.norm(endpoint - true_point))
    closure = -friction if broken else friction - 0.22
    penetration, tank = 0.0, 0.18
    minimum_tank = tank
    delay = [0.0] * (7 if broken else 3)
    final_force = 0.0
    for _ in range(200):
        force = 600.0 * penetration
        if broken:
            command = float(np.clip(0.08 * (10.0 + force), -0.15, 0.15))
        else:
            command = float(np.clip(0.012 * (10.0 - force), -0.025, 0.025))
        delay.append(command)
        velocity = delay.pop(0)
        work = max(force * velocity, 0.0) * 0.01
        if not broken and work > tank and force > 1.0e-12:
            velocity = tank / (force * 0.01)
            work = tank
        tank -= work
        penetration = float(np.clip(penetration + velocity * 0.01, 0.0, 0.05))
        minimum_tank = min(minimum_tank, tank)
        final_force = 600.0 * penetration
    reach = first + second - float(np.linalg.norm(estimate))
    margins = np.array([(0.055 - pickup_error) / 0.055, reach / 0.20,
                        closure / 0.20, (3.0 - abs(final_force - 10.0)) / 3.0,
                        minimum_tank / 0.10, 1.0 if not broken else -1.0])
    violations = int(np.sum(margins < -1.0e-12)) + int(not reachable)
    return [float(violations == 0), pickup_error, minimum_tank]


_DISPATCH = {66: _p66, 67: _p67, 68: _p68, 69: _p69, 61: _p61, 62: _p62, 63: _p63, 64: _p64, 65: _p65, 58: _p58, 59: _p59, 60: _p60, 54: _p54, 55: _p55, 56: _p56, 57: _p57, 49: _p49, 50: _p50, 51: _p51, 52: _p52, 53: _p53, 41: _p41, 42: _p42, 43: _p43, 44: _p44, 45: _p45, 46: _p46, 47: _p47, 48: _p48, 34: _p34, 35: _p35, 36: _p36, 37: _p37, 38: _p38, 39: _p39, 40: _p40, 25: _p25, 26: _p26, 27: _p27, 28: _p28, 29: _p29, 30: _p30, 31: _p31, 32: _p32, 33: _p33, }

def origin(number: int) -> dict[str, Any]:
    return {"kind": "independent-analytic-python", "item_id": f"P{number:02d}", "independent": True,
            "imports_production_entrypoint": False, "derived_from_production_output": False,
            "perturbs_production_output": False}

def reference_signature(number: int, parameters: dict[str, Any]) -> list[float]:
    return list(_DISPATCH[number](dict(parameters)))
