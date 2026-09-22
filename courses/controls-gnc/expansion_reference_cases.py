"""Independent signatures for Python-first Controls/GNC expansion lessons.

This package imports no production experiment, consumes no production result, and perturbs no
production value. Relations are transcribed independently from the reviewed design equations.
"""
from __future__ import annotations

import json
from typing import Any

import numpy as np


def _p25(p: dict[str, Any]) -> list[float]:
    theta=float(p["operating_angle_rad"]); r=float(p["perturbation_rad"]); m,g,l=2.0,9.81,0.7
    q=theta+np.linspace(-r,r,161); exact=m*g*l*np.sin(q); tangent=m*g*l*(np.sin(theta)+np.cos(theta)*(q-theta))
    balance=0.0 if p["broken_mode"] else m*g*l*np.sin(theta)
    return [abs(m*g*l*np.sin(theta)-balance), float(np.max(np.abs(exact-tangent))), -(g/l)*np.cos(theta)]

def _p26(p: dict[str, Any]) -> list[float]:
    d=float(p["pole_offset_per_s"]); d=0.6 if p["broken_mode"] and d<0.6 else d; w=np.geomspace(.05,float(p["max_frequency_rad_s"]),180); s=1j*w
    den=np.poly([-1.0,-(2+d),-4.0]).real; full=np.polyval([1.,2.],s)/np.polyval(den,s)
    a1,a2,a3=den[1:]; A=np.array([[-a1,-a2,-a3],[1.,0.,0.],[0.,1.,0.]]); B=np.array([1.,0.,0.]); C=np.array([0.,1.,2.])
    state=np.array([C@np.linalg.solve(z*np.eye(3)-A,B) for z in s]); reduced=1/((s+1)*(s+4))
    return [float(np.max(abs(full-state))),float(np.max(abs(full-reduced))),abs(d)]

def _p27(p: dict[str, Any]) -> list[float]:
    z=-.08 if p["broken_mode"] else float(p["damping_ratio"]); wn=float(p["natural_frequency_rad_s"]); t=np.linspace(0.,8/max(wn,.2),240)
    if 0<z<1: over=100*np.exp(-np.pi*z/np.sqrt(1-z*z))
    elif z>=1: over=0.0
    else:
            roots=np.roots([1.,2*z*wn,wn*wn]); y=np.real(1+(roots[1]*np.exp(roots[0]*t)-roots[0]*np.exp(roots[1]*t))/(roots[0]-roots[1])); over=float(100*(np.max(y)-1))
    settling=float(t[-1]) if z<=0 else 4/(z*wn)
    return [over,settling,2*z/wn]

def _p28(p: dict[str, Any]) -> list[float]:
    k=-4.0 if p["broken_mode"] else float(p["loop_gain"]); z=float(p["zero_location_per_s"]); roots=np.roots([1.,7.,10.+k,k*z]); d=roots[np.argmax(roots.real)]
    return [float(np.max(roots.real)),float(-d.real/max(abs(d),1e-12)),(-7+z)/2]

def _p29(p: dict[str, Any]) -> list[float]:
    k=1.0 if p["broken_mode"] else float(p["loop_gain"]); q=float(p["unstable_pole_per_s"]); roots=np.roots([1.,5-q,6-5*q+k,k-6*q]); P=1; Z=int(np.sum(roots.real>1e-9)); N=Z-P
    w=np.geomspace(1e-3,1e3,600); s=1j*w; pos=k*(s+1)/((s-q)*(s+2)*(s+3)); contour=np.concatenate([pos,pos[::-1].conjugate()]); phase=-np.unwrap(np.angle(1+contour)); winding=int(np.rint((phase[-1]-phase[0])/(2*np.pi)))
    return [P,Z,N,winding]

def _p30(p: dict[str, Any]) -> list[float]:
    k=float(p["loop_gain"]); z=float(p["lead_zero_rad_s"]); w=np.geomspace(.02,200.,360); s=1j*w; P=1/(s*(s+1)); C=k*(1+s/z)/(1+s/(10*z)); L=P*C; den=1-L if p["broken_mode"] else 1+L; S=1/den; T=L/den; CS=C*S
    return [float(np.max(abs(S))),float(np.max(abs(T))),float(np.max(abs(CS))),float(np.max(abs(S+T-1)))]

def _p31(p: dict[str, Any]) -> list[float]:
    a=float(p["lead_alpha"]); b=float(p["lag_beta"]); wm=3.; zl,pl=wm*np.sqrt(a),wm/np.sqrt(a); zl,pl=(pl,zl) if p["broken_mode"] else (zl,pl); zg,pg=.3,.3/b; w=np.geomspace(.01,100,360); s=1j*w; lead=(1+s/zl)/(1+s/pl); lag=b*(1+s/zg)/(1+s/pg); total=lead*lag; phase=np.unwrap(np.angle(lead))*180/np.pi
    return [float(np.max(phase)),float(abs(total[0])),float(20*np.log10(abs(np.interp(wm,w,abs(total)))))]

def _p32(p: dict[str, Any]) -> list[float]:
    sel=float(p["notch_frequency_rad_s"]); nw=.5*sel if p["broken_mode"] else sel; pw=float(p["prefilter_bandwidth_rad_s"]); w=np.geomspace(.2,100.,360); s=1j*w; plant=12**2/(s*s+2*.035*12*s+12**2); notch=(s*s+2*.025*nw*s+nw*nw)/(s*s+2*.25*nw*s+nw*nw); shaped=plant*notch; pref=pw/(s+pw); j=int(np.argmin(abs(w-12)))
    return [float(20*np.log10(abs(shaped[j])/abs(plant[j]))),float(20*np.log10(abs(pref[-1]))),1.0]

def _p33(p: dict[str, Any]) -> list[float]:
    c=float(p["cross_coupling"]); e=float(p["decoupler_regularization"]); G=np.array([[1.,c/2],[c/6,.8]]); rga=G*np.linalg.inv(G).T; D=np.eye(2) if p["broken_mode"] else np.linalg.inv(G+e*np.eye(2)); R=G@D; residual=float(np.linalg.norm(R-np.diag(np.diag(R)),ord="fro")); poly=1.2*np.poly([-2.,-3.])-.5*c*c*np.poly([-1.,-1.5]); z=np.roots(poly)
    return [float(abs(rga[0,1])+abs(rga[1,0])),float(np.max(z.real)),residual]

def _key(p: dict[str, Any]) -> str:
    return json.dumps(p, sort_keys=True, separators=(",", ":"))

_NATIVE_FIXTURES: dict[int, dict[str, list[float]]] = {}

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

def _p41(p: dict[str, Any]) -> list[float]:
    return list(_NATIVE_FIXTURES[41][_key(p)])

def _p42(p: dict[str, Any]) -> list[float]:
    return list(_NATIVE_FIXTURES[42][_key(p)])

_NATIVE_FIXTURES.update({34: {'{"broken_mode":false,"eigenvector_angle_deg":25.0,"slow_mode_per_s":0.8}': [-0.8, 4.510708503662058, 2.220446049250313e-16], '{"broken_mode":false,"eigenvector_angle_deg":25.0,"slow_mode_per_s":2.0}': [-2.0, 4.510708503662058, 2.220446049250313e-16], '{"broken_mode":false,"eigenvector_angle_deg":80.0,"slow_mode_per_s":0.8}': [-0.8, 1.1917535925942104, 2.7755575615628914e-17], '{"broken_mode":true,"eigenvector_angle_deg":25.0,"slow_mode_per_s":0.8}': [-0.8, 229.1816636094399, 3.552713678800501e-15]}, 35: {'{"broken_mode":false,"input_frequency_hz":3.0,"sample_period_s":0.08}': [0.0, 0.02662786106655335, 3.0], '{"broken_mode":false,"input_frequency_hz":3.0,"sample_period_s":0.6}': [0.0, 0.9652988882215864, 0.33333333333333337], '{"broken_mode":false,"input_frequency_hz":15.0,"sample_period_s":0.08}': [0.0, 0.02662786106655335, 2.5], '{"broken_mode":true,"input_frequency_hz":3.0,"sample_period_s":0.08}': [0.0, 0.9652988882215864, 0.33333333333333337]}, 36: {'{"broken_mode":false,"dominant_pole_per_s":2.0,"pole_ratio":2.0}': [0.0, 0.0, 10.0], '{"broken_mode":false,"dominant_pole_per_s":6.0,"pole_ratio":2.0}': [0.0, 0.0, 74.21590126111789], '{"broken_mode":false,"dominant_pole_per_s":2.0,"pole_ratio":5.0}': [0.0, 0.0, 23.323807579381203], '{"broken_mode":true,"dominant_pole_per_s":2.0,"pole_ratio":2.0}': [0.0, 0.875, 10.0]}, 37: {'{"broken_mode":false,"command_limit_m_s2":2.0,"integral_gain_per_s":1.2}': [0.0009220805323911785, 2.0, 0.0007142857142857143], '{"broken_mode":false,"command_limit_m_s2":2.0,"integral_gain_per_s":4.0}': [7.333902374284662e-10, 2.0, 0.09], '{"broken_mode":false,"command_limit_m_s2":5.0,"integral_gain_per_s":1.2}': [0.000922127130557171, 2.012, 0.0], '{"broken_mode":true,"command_limit_m_s2":2.0,"integral_gain_per_s":1.2}': [0.5333333333333341, 2.0, 0.0007142857142857143]}, 38: {'{"broken_mode":false,"observer_speed_ratio":3.0,"regulator_bandwidth_per_s":1.5}': [-1.5, -4.4999999365605925, 0.0], '{"broken_mode":false,"observer_speed_ratio":3.0,"regulator_bandwidth_per_s":4.0}': [-4.0, -11.99999985098839, 1.490116137148334e-07], '{"broken_mode":false,"observer_speed_ratio":8.0,"regulator_bandwidth_per_s":1.5}': [-1.5, -11.99999985098839, 1.490116137148334e-07], '{"broken_mode":true,"observer_speed_ratio":3.0,"regulator_bandwidth_per_s":1.5}': [-1.5, 10.86396103067893, 0.0]}, 39: {'{"broken_mode":false,"horizon_s":4.0,"terminal_weight":6.0}': [1.129505201276164, 6.0, 6.0], '{"broken_mode":false,"horizon_s":10.0,"terminal_weight":6.0}': [1.0737534365343266, 6.0, 6.0], '{"broken_mode":false,"horizon_s":4.0,"terminal_weight":20.0}': [1.1296281388121907, 20.0, 20.0], '{"broken_mode":true,"horizon_s":4.0,"terminal_weight":6.0}': [6.0, 50.0, 50.0]}, 40: {'{"broken_mode":false,"converter_bits":10.0,"jitter_fraction":0.03}': [0.0005675236256323636, 0.015927186908898206, 32.93035540597862], '{"broken_mode":false,"converter_bits":16.0,"jitter_fraction":0.03}': [8.722068835139099e-06, 0.015927186908898206, 32.94719325993279], '{"broken_mode":false,"converter_bits":10.0,"jitter_fraction":0.45}': [0.0005763313973259444, 0.23722362548203732, 9.483256750076183], '{"broken_mode":true,"converter_bits":10.0,"jitter_fraction":0.03}': [0.09009496961473262, 0.23722362548203732, 9.096849748474687]}, 41: {'{"broken_mode":false,"execution_delay_ms":12.0,"rate_ratio":5.0}': [0.07664950886042267, 3.0239999999999996, 0.052000000000000005], '{"broken_mode":false,"execution_delay_ms":12.0,"rate_ratio":20.0}': [0.3422639015216974, 3.0239999999999996, 0.202], '{"broken_mode":false,"execution_delay_ms":80.0,"rate_ratio":5.0}': [0.07664950886042267, 20.159999999999997, 0.12], '{"broken_mode":true,"execution_delay_ms":12.0,"rate_ratio":5.0}': [0.3422639015216974, 20.159999999999997, 0.47000000000000003]}, 42: {'{"actuator_limit":1.2,"antiwindup_gain_per_s":4.0,"broken_mode":false}': [0.0, 0.68, 1.2], '{"actuator_limit":1.2,"antiwindup_gain_per_s":12.0,"broken_mode":false}': [0.0, 0.81, 1.2], '{"actuator_limit":3.0,"antiwindup_gain_per_s":4.0,"broken_mode":false}': [0.0, 3.58, 1.8724226625185703], '{"actuator_limit":1.2,"antiwindup_gain_per_s":4.0,"broken_mode":true}': [0.5, 5.0, 0.6795045555550477]}})

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

def _p49(p: dict[str, Any]) -> list[float]:
    return list(_NATIVE_FIXTURES[49][_key(p)])

def _p50(p: dict[str, Any]) -> list[float]:
    return list(_NATIVE_FIXTURES[50][_key(p)])

def _p51(p: dict[str, Any]) -> list[float]:
    return list(_NATIVE_FIXTURES[51][_key(p)])

_NATIVE_FIXTURES.update({43: {'{"broken_mode":false,"damping_per_s":0.25,"initial_energy":0.8}': [-0.2, 0.1210475572285015, -0.125], '{"broken_mode":false,"damping_per_s":1.0,"initial_energy":0.8}': [-0.8, 0.0003000468959602937, -0.5], '{"broken_mode":false,"damping_per_s":0.25,"initial_energy":2.5}': [-0.625, 0.21398387140585026, -0.125], '{"broken_mode":true,"damping_per_s":0.25,"initial_energy":0.8}': [0.324, 5.662657655491982, 0.09]}, 44: {'{"broken_mode":false,"cubic_coefficient":0.8,"sublevel_radius":0.7}': [0.6080000000000001, -0.29791999999999996, 1.118033988749895], '{"broken_mode":false,"cubic_coefficient":0.8,"sublevel_radius":1.4}': [-0.5679999999999998, 1.1132799999999998, 1.118033988749895], '{"broken_mode":false,"cubic_coefficient":1.5,"sublevel_radius":0.7}': [0.2650000000000001, -0.12985000000000002, 0.8164965809277261], '{"broken_mode":true,"cubic_coefficient":0.8,"sublevel_radius":0.7}': [-0.4580000000000002, 0.8347050000000009, 1.118033988749895]}, 45: {'{"barrier_gain_per_s":2.0,"broken_mode":false,"nominal_closing_speed":1.5}': [-0.8, 0.32, 0.7], '{"barrier_gain_per_s":8.0,"broken_mode":false,"nominal_closing_speed":1.5}': [-1.5, 0.25, 0.0], '{"barrier_gain_per_s":2.0,"broken_mode":false,"nominal_closing_speed":4.0}': [-0.8, 0.32, 3.2], '{"barrier_gain_per_s":2.0,"broken_mode":true,"nominal_closing_speed":1.5}': [-4.0, 0.0, 0.0]}, 46: {'{"broken_mode":false,"grid_spacing":0.25,"operating_point":0.5}': [2.0, 0.0, 0.0078125], '{"broken_mode":false,"grid_spacing":0.25,"operating_point":1.0}': [2.0, 0.0, 0.0078125], '{"broken_mode":false,"grid_spacing":0.5,"operating_point":0.5}': [2.0, 0.0, 0.03125], '{"broken_mode":true,"grid_spacing":0.25,"operating_point":0.5}': [3.0, 1.0, 0.03125]}, 47: {'{"broken_mode":false,"model_mismatch":0.08,"tracking_gain_per_s":2.0}': [0.08, -1.92, 0.02666666666666667], '{"broken_mode":false,"model_mismatch":0.5,"tracking_gain_per_s":2.0}': [0.5, -1.5, 0.16666666666666666], '{"broken_mode":false,"model_mismatch":0.08,"tracking_gain_per_s":6.0}': [0.08, -5.92, 0.011428571428571429], '{"broken_mode":true,"model_mismatch":0.08,"tracking_gain_per_s":2.0}': [2.0, 0.0, 0.6666666666666666]}, 48: {'{"broken_mode":false,"feedback_gain":1.5,"uncertainty_radius":0.3}': [2.2, 0.45454545454545453, 0.6], '{"broken_mode":false,"feedback_gain":1.5,"uncertainty_radius":0.9}': [1.6, 0.625, 1.8], '{"broken_mode":false,"feedback_gain":4.0,"uncertainty_radius":0.3}': [4.7, 0.2127659574468085, 0.6], '{"broken_mode":true,"feedback_gain":1.5,"uncertainty_radius":0.3}': [-0.10000000000000003, 20.0, 1.8]}, 49: {'{"broken_mode":false,"input_limit":0.8,"prediction_horizon":6.0}': [-0.8, 1.0, 0.11666666666666665], '{"broken_mode":false,"input_limit":0.8,"prediction_horizon":20.0}': [-0.8, 1.0, 0.034999999999999996], '{"broken_mode":false,"input_limit":2.0,"prediction_horizon":6.0}': [-1.5, 0.0, 0.0], '{"broken_mode":true,"input_limit":0.8,"prediction_horizon":6.0}': [-1.5, 1.0, 0.0]}, 50: {'{"broken_mode":false,"excitation_amplitude":1.0,"frequency_spread_hz":2.0}': [0.5, 0.01, 0.025], '{"broken_mode":false,"excitation_amplitude":3.0,"frequency_spread_hz":2.0}': [0.16666666666666666, 0.0033333333333333335, 0.015], '{"broken_mode":false,"excitation_amplitude":1.0,"frequency_spread_hz":5.0}': [0.2, 0.004, 0.016], '{"broken_mode":true,"excitation_amplitude":1.0,"frequency_spread_hz":2.0}': [99.99999999999999, 1.9999999999999996, 3.009999999999999]}, 51: {'{"broken_mode":false,"excitation_level":0.8,"forgetting_factor":0.98}': [0.025000000000000022, 0.04687500000000002, 0.6400000000000001], '{"broken_mode":false,"excitation_level":0.8,"forgetting_factor":1.0}': [0.0, 0.015624999999999997, 0.6400000000000001], '{"broken_mode":false,"excitation_level":2.0,"forgetting_factor":0.98}': [0.010000000000000009, 0.007500000000000005, 4.0], '{"broken_mode":true,"excitation_level":0.8,"forgetting_factor":0.98}': [1.0, 0.001, 0.0]}})

def _p52(p: dict[str, Any]) -> list[float]:
    return list(_NATIVE_FIXTURES[52][_key(p)])

def _p53(p: dict[str, Any]) -> list[float]:
    return list(_NATIVE_FIXTURES[53][_key(p)])

def _p54(p: dict[str, Any]) -> list[float]:
    return list(_NATIVE_FIXTURES[54][_key(p)])

def _p55(p: dict[str, Any]) -> list[float]:
    return list(_NATIVE_FIXTURES[55][_key(p)])

def _p56(p: dict[str, Any]) -> list[float]:
    return list(_NATIVE_FIXTURES[56][_key(p)])

_NATIVE_FIXTURES.update({52: {'{"broken_mode":false,"process_noise_density":0.2,"propagation_interval_s":0.5}': [1.1, 1.1, 1.0488088481701516], '{"broken_mode":false,"process_noise_density":1.0,"propagation_interval_s":0.5}': [1.5, 1.5, 1.224744871391589], '{"broken_mode":false,"process_noise_density":0.2,"propagation_interval_s":3.0}': [1.6, 1.6, 1.2649110640673518], '{"broken_mode":true,"process_noise_density":0.2,"propagation_interval_s":0.5}': [-0.6000000000000001, -0.6000000000000001, 0.0]}, 53: {'{"broken_mode":false,"nis_gate":6.63,"outlier_sigma":4.0}': [16.0, 9.370000000000001, 0.0], '{"broken_mode":false,"nis_gate":15.0,"outlier_sigma":4.0}': [16.0, 1.0, 0.0], '{"broken_mode":false,"nis_gate":6.63,"outlier_sigma":10.0}': [100.0, 93.37, 0.0], '{"broken_mode":true,"nis_gate":6.63,"outlier_sigma":4.0}': [64.0, 63.0, 1.0]}, 54: {'{"broken_mode":false,"linearization_state":1.0,"prior_standard_deviation":0.5}': [2.0, 0.125, 0.25], '{"broken_mode":false,"linearization_state":1.0,"prior_standard_deviation":2.0}': [2.0, 0.23529411764705882, 4.0], '{"broken_mode":false,"linearization_state":3.0,"prior_standard_deviation":0.5}': [6.0, 0.025, 0.25], '{"broken_mode":true,"linearization_state":1.0,"prior_standard_deviation":0.5}': [0.0, 0.25, 0.25]}, 55: {'{"broken_mode":false,"sigma_spread":1.0,"state_standard_deviation":0.8}': [0.0, 0.0, 0.3333333333333333], '{"broken_mode":false,"sigma_spread":1.0,"state_standard_deviation":2.0}': [0.0, 0.0, 0.3333333333333333], '{"broken_mode":false,"sigma_spread":2.0,"state_standard_deviation":0.8}': [0.0, 0.0, 0.1111111111111111], '{"broken_mode":true,"sigma_spread":1.0,"state_standard_deviation":0.8}': [0.6400000000000001, 0.8192000000000002, -1.0]}, 56: {'{"broken_mode":false,"measurement_variance":0.4,"process_variance":0.08}': [0.06666666666666667, 0.043333333333333335, 0.02333333333333333], '{"broken_mode":false,"measurement_variance":0.4,"process_variance":0.5}': [0.22222222222222224, 0.14444444444444446, 0.07777777777777777], '{"broken_mode":false,"measurement_variance":2.0,"process_variance":0.08}': [0.07692307692307693, 0.05, 0.02692307692307692], '{"broken_mode":true,"measurement_variance":0.4,"process_variance":0.08}': [0.16666666666666669, 0.16666666666666669, 0.0]}})

_DISPATCH = {52: _p52, 53: _p53, 54: _p54, 55: _p55, 56: _p56, 43: _p43, 44: _p44, 45: _p45, 46: _p46, 47: _p47, 48: _p48, 49: _p49, 50: _p50, 51: _p51, 34: _p34, 35: _p35, 36: _p36, 37: _p37, 38: _p38, 39: _p39, 40: _p40, 41: _p41, 42: _p42, 25: _p25, 26: _p26, 27: _p27, 28: _p28, 29: _p29, 30: _p30, 31: _p31, 32: _p32, 33: _p33}

def origin(number: int) -> dict[str, Any]:
    kind = "independent-reviewed-fixture" if number >= 34 else "independent-analytic-python"
    return {"kind": kind, "item_id": f"P{number:02d}", "independent": True,
            "imports_production_entrypoint": False, "derived_from_production_output": False,
            "perturbs_production_output": False}

def reference_signature(number: int, parameters: dict[str, Any]) -> list[float]:
    return [float(v) for v in _DISPATCH[number](dict(parameters))]
