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

def _p36(p):
    slow=float(p['dominant_pole_per_s']); fast=slow*float(p['pole_ratio'])
    position=slow*fast
    return [0.,abs(1-1/position) if p['broken_mode'] else 0.,position,slow+fast]

def _p37(p: dict[str, Any]) -> list[float]:
    return list(_NATIVE_FIXTURES[37][_key(p)])

def _p38(p):
    # Analytic double-integrator CARE: p12=bw^2, p22=sqrt(3)*bw.
    bw=float(p['regulator_bandwidth_per_s']); ow=bw*float(p['observer_speed_ratio'])
    observer=(3+np.sqrt(17))*ow/2 if p['broken_mode'] else -ow
    return [-np.sqrt(3)*bw/2,observer,0.,0.]

def _p39(p: dict[str, Any]) -> list[float]:
    return list(_NATIVE_FIXTURES[39][_key(p)])

def _p40(p: dict[str, Any]) -> list[float]:
    return list(_NATIVE_FIXTURES[40][_key(p)])

def _p41(p: dict[str, Any]) -> list[float]:
    return list(_NATIVE_FIXTURES[41][_key(p)])

def _p42(p):
    # Independent piecewise-affine sampled state transition, with saturation regions.
    limit=float(p['actuator_limit']); manual=min(.7,limit)
    kaw=0. if p['broken_mode'] else float(p['antiwindup_gain_per_s'])
    s=np.zeros(2); history=[]; integral=[]; command=[]
    for tick in range(1201):
        r=2. if tick<700 else .2
        if tick==300: s[1]=0. if p['broken_mode'] else manual-2*(r-s[0])
        request=manual if tick<300 else 2*r+np.array([-2.,1.])@s
        applied=min(limit,max(-limit,request))
        history.append(s[0]); integral.append(s[1]); command.append(applied)
        if tick<300: s=np.diag([.99,1.])@s+np.array([.01*manual,0.])
        elif abs(request)<=limit:
            s=np.array([[.97,.01],[-.012,1.]])@s+np.array([.02*r,.012*r])
        else:
            s=np.array([[.99,0.],[.01*(-1.2+2*kaw),1-.01*kaw]])@s+np.array([.01*applied,.01*((1.2-2*kaw)*r+kaw*applied)])
    last_bad=max([i for i in range(700,1201) if abs(history[i]-.2)>.04],default=699)
    observed=last_bad<1200; duration=(last_bad+1)*.01-7 if observed else 5.
    return [abs(command[300]-command[299]),duration,max(abs(np.array(integral))),float(observed)]

_NATIVE_FIXTURES.update({34: {'{"broken_mode":false,"eigenvector_angle_deg":25.0,"slow_mode_per_s":0.8}': [-0.8, 4.510708503662058, 2.220446049250313e-16], '{"broken_mode":false,"eigenvector_angle_deg":25.0,"slow_mode_per_s":2.0}': [-2.0, 4.510708503662058, 2.220446049250313e-16], '{"broken_mode":false,"eigenvector_angle_deg":80.0,"slow_mode_per_s":0.8}': [-0.8, 1.1917535925942104, 2.7755575615628914e-17], '{"broken_mode":true,"eigenvector_angle_deg":25.0,"slow_mode_per_s":0.8}': [-0.8, 229.1816636094399, 3.552713678800501e-15]}, 35: {'{"broken_mode":false,"input_frequency_hz":3.0,"sample_period_s":0.08}': [0.0, 0.02662786106655335, 3.0], '{"broken_mode":false,"input_frequency_hz":3.0,"sample_period_s":0.6}': [0.0, 0.9652988882215864, 0.33333333333333337], '{"broken_mode":false,"input_frequency_hz":15.0,"sample_period_s":0.08}': [0.0, 0.02662786106655335, 2.5], '{"broken_mode":true,"input_frequency_hz":3.0,"sample_period_s":0.08}': [0.0, 0.9652988882215864, 0.33333333333333337]}, 37: {'{"broken_mode":false,"command_limit_m_s2":2.0,"integral_gain_per_s":1.2}': [0.0009220805323911785, 2.0, 0.0007142857142857143], '{"broken_mode":false,"command_limit_m_s2":2.0,"integral_gain_per_s":4.0}': [7.333902374284662e-10, 2.0, 0.09], '{"broken_mode":false,"command_limit_m_s2":5.0,"integral_gain_per_s":1.2}': [0.000922127130557171, 2.012, 0.0], '{"broken_mode":true,"command_limit_m_s2":2.0,"integral_gain_per_s":1.2}': [0.5333333333333341, 2.0, 0.0007142857142857143]}, 39: {'{"broken_mode":false,"horizon_s":4.0,"terminal_weight":6.0}': [1.129505201276164, 6.0, 6.0], '{"broken_mode":false,"horizon_s":10.0,"terminal_weight":6.0}': [1.0737534365343266, 6.0, 6.0], '{"broken_mode":false,"horizon_s":4.0,"terminal_weight":20.0}': [1.1296281388121907, 20.0, 20.0], '{"broken_mode":true,"horizon_s":4.0,"terminal_weight":6.0}': [6.0, 50.0, 50.0]}, 40: {'{"broken_mode":false,"converter_bits":10.0,"jitter_fraction":0.03}': [0.0005675236256323636, 0.015927186908898206, 32.93035540597862], '{"broken_mode":false,"converter_bits":16.0,"jitter_fraction":0.03}': [8.722068835139099e-06, 0.015927186908898206, 32.94719325993279], '{"broken_mode":false,"converter_bits":10.0,"jitter_fraction":0.45}': [0.0005763313973259444, 0.23722362548203732, 9.483256750076183], '{"broken_mode":true,"converter_bits":10.0,"jitter_fraction":0.03}': [0.09009496961473262, 0.23722362548203732, 9.096849748474687]}, 41: {'{"broken_mode":false,"execution_delay_ms":12.0,"rate_ratio":5.0}': [0.07664950886042267, 3.0239999999999996, 0.052000000000000005], '{"broken_mode":false,"execution_delay_ms":12.0,"rate_ratio":20.0}': [0.3422639015216974, 3.0239999999999996, 0.202], '{"broken_mode":false,"execution_delay_ms":80.0,"rate_ratio":5.0}': [0.07664950886042267, 20.159999999999997, 0.12], '{"broken_mode":true,"execution_delay_ms":12.0,"rate_ratio":5.0}': [0.3422639015216974, 20.159999999999997, 0.47000000000000003]}})

def _p43(p):
    from scipy.integrate import solve_ivp
    # Implicit Radau independently integrates the two physical states (no work state).
    damping=float(p['damping_per_s'])*(-1 if p['broken_mode'] else 1)
    initial=float(p['initial_energy'])
    solution=solve_ivp(lambda t,z:[z[1],z[0]*(1-z[0]**2)-damping*z[1]],(0,6),[0,np.sqrt(2*initial)],method='Radau',rtol=2e-12,atol=2e-13)
    if not solution.success: raise ValueError(solution.message)
    x,v=solution.y[:,-1]; final=v*v/2-x*x/2+x**4/4
    abscissa=(-damping+np.sqrt(complex(damping*damping-8))).real/2
    return [(final-initial)/6,min(abs(x-1),abs(x+1)),abscissa]

def _p44(p: dict[str, Any]) -> list[float]:
    return list(_NATIVE_FIXTURES[44][_key(p)])

def _p45(p):
    a=float(p['barrier_gain_per_s']); v=float(p['nominal_closing_speed']); step=.01
    if p['broken_mode']: return [-v,.4-3*v,0.]
    # Closed-form linear approach until the first exponential/geometric stage.
    n=max(0,int(np.ceil((.4-v/a)/(step*v))))
    n=min(300,n); h_switch=.4-n*step*v
    final=h_switch*(1-a*step)**(300-n)
    first=max(-v,-.4*a); last=max(-v,-a*final)
    return [first,final,last+v]

def _p46(p):
    rho=float(p['operating_point']); step=float(p['grid_spacing'])
    nodes=np.r_[np.arange(0.,1.-1e-12,step),1.]
    def secant(x):
        if p['broken_mode']: return 2.
        i=min(len(nodes)-2,max(0,int(np.searchsorted(nodes,x,side='right')-1)))
        left,right=nodes[i:i+2]; fraction=(x-left)/(right-left)
        return (1-fraction)*2/(1+left*left/2)+fraction*2/(1+right*right/2)
    locations=np.unique(np.r_[np.linspace(0,1,201),nodes,(nodes[1:]+nodes[:-1])/2])
    bandwidth=(1+rho*rho/2)*secant(rho)
    return [bandwidth,abs(bandwidth-2),max(abs(secant(x)-2/(1+x*x/2)) for x in locations)]

def _p47(p):
    delta=2-float(p['model_mismatch']) if p['broken_mode'] else float(p['model_mismatch'])
    k=float(p['tracking_gain_per_s']); end=4.
    if delta>k:
        # Equivalent reciprocal-state solution: x=1 / [delta/k+(1-delta/k)*exp(k*t)].
        crossing=np.log((.1-delta/k)/(1-delta/k))/k
        end=min(end,crossing)
    terminal=1/(delta/k+(1-delta/k)*np.exp(k*end))
    return [delta,delta-k,abs(terminal)]

def _p48(p):
    radius=float(p['uncertainty_radius']); gain=float(p['feedback_gain'])*(-1 if p['broken_mode'] else 1)
    largest=0.
    for delta in np.linspace(-radius,radius,81):
        for frequency in np.geomspace(.05,100.,160):
            plant=1/(1+delta+1j*frequency)
            largest=max(largest,abs(1/(1+gain*plant)))
    return [1-radius+gain,largest,2*radius]

def _p49(p):
    # Scalar Bellman solution: saturated first move, otherwise unconstrained Riccati gain.
    # For this integrator/zero target, later optimal moves decrease in magnitude, so a
    # free first move implies all later bounds are inactive; convexity gives the clipped branch.
    horizon=int(p['prediction_horizon']); limit=float(p['input_limit']); value=0.; gains=[]
    for _ in range(horizon):
        gain=(1+value)/(1.1+value); gains.append(gain); value=.1*(1+value)/(1.1+value)
    state=1.5; moves=[]
    for gain in reversed(gains):
        move=-gain*state
        if not p['broken_mode']: move=max(-limit,min(limit,move))
        moves.append(move); state+=move
    return [moves[0],max(0.,abs(moves[0])-limit),abs(state)]

def _p50(p):
    # Convolution builds observations; a two-column Gram solve fits coefficients.
    amplitude=float(p['excitation_amplitude']); spread=float(p['frequency_spread_hz'])
    train_t=.02*np.arange(300); valid_t=.02*np.arange(300,500)
    u=amplitude*(np.sin(2*np.pi*.3*train_t)+.5*np.sin(2*np.pi*(.3+spread)*train_t+.4))
    uv=amplitude*(np.sin(2*np.pi*.7*valid_t+1)+.5*np.sin(2*np.pi*(.7+spread)*valid_t+.8))
    if p['broken_mode']: u[:]=0
    y=np.r_[0.,np.convolve(.18*u+.002*np.cos(1.7*np.arange(300)),.82**np.arange(300))[:300]]
    v=np.r_[0.,np.convolve(.18*uv+.002*np.cos(1.7*np.arange(300,500)),.82**np.arange(200))[:200]]
    xx=y[:-1]@y[:-1]; xu=y[:-1]@u; uu=u@u
    g=np.array([[xx,xu],[xu,uu]]); target=np.array([y[:-1]@y[1:],u@y[1:]])
    if uu==0: theta=np.array([target[0]/xx,0.])
    else: theta=np.array([uu*target[0]-xu*target[1],xx*target[1]-xu*target[0]])/(xx*uu-xu*xu)
    prediction=np.r_[0.,np.convolve(theta[1]*uv,theta[0]**np.arange(200))[:200]]
    smallest=np.sqrt(max(0.,min(np.linalg.eigvalsh(g))))
    return [smallest,np.sqrt(sum((theta-[.82,.18])**2)),np.sqrt(np.mean((prediction[1:]-v[1:])**2))]

def _p51(p):
    forgetting=float(p['forgetting_factor']); level=float(p['excitation_level'])
    if p['broken_mode']: return [1.,10*forgetting**200,0.]
    ticks=np.arange(200); regressor=level*(np.sin(.31*ticks)+.4*np.cos(.13*ticks))
    response=regressor+.01*np.sin(.73*ticks); weights=forgetting**(199-ticks)
    information=forgetting**200/10+sum(weights*regressor**2)
    estimate=sum(weights*regressor*response)/information
    return [abs(estimate-1),1/information,sum(regressor**2)/10]

_NATIVE_FIXTURES.update({44: {'{"broken_mode":false,"cubic_coefficient":0.8,"sublevel_radius":0.7}': [0.6080000000000001, -0.29791999999999996, 1.118033988749895], '{"broken_mode":false,"cubic_coefficient":0.8,"sublevel_radius":1.4}': [-0.5679999999999998, 1.1132799999999998, 1.118033988749895], '{"broken_mode":false,"cubic_coefficient":1.5,"sublevel_radius":0.7}': [0.2650000000000001, -0.12985000000000002, 0.8164965809277261], '{"broken_mode":true,"cubic_coefficient":0.8,"sublevel_radius":0.7}': [-0.4580000000000002, 0.8347050000000009, 1.118033988749895]}})

def _p52(p: dict[str, Any]) -> list[float]:
    return list(_NATIVE_FIXTURES[52][_key(p)])

def _p53(p: dict[str, Any]) -> list[float]:
    return list(_NATIVE_FIXTURES[53][_key(p)])

def _p54(p: dict[str, Any]) -> list[float]:
    return list(_NATIVE_FIXTURES[54][_key(p)])

def _p55(p):
    sigma=float(p['state_standard_deviation']); alpha=float(p['sigma_spread'])
    # Gaussian fourth moment E[x^4]=3*sigma^4, so Var[x^2]=2*sigma^4.
    # Omitting the covariance correction leaves (alpha^2-1)*sigma^4.
    error=abs(alpha*alpha-3)*sigma**4 if p['broken_mode'] else 0.
    return [0.,error,min(1-1/alpha**2,1/(2*alpha**2))]

def _p56(p: dict[str, Any]) -> list[float]:
    return list(_NATIVE_FIXTURES[56][_key(p)])

_NATIVE_FIXTURES.update({52: {'{"broken_mode":false,"process_noise_density":0.2,"propagation_interval_s":0.5}': [1.1, 1.1, 1.0488088481701516], '{"broken_mode":false,"process_noise_density":1.0,"propagation_interval_s":0.5}': [1.5, 1.5, 1.224744871391589], '{"broken_mode":false,"process_noise_density":0.2,"propagation_interval_s":3.0}': [1.6, 1.6, 1.2649110640673518], '{"broken_mode":true,"process_noise_density":0.2,"propagation_interval_s":0.5}': [-0.6000000000000001, -0.6000000000000001, 0.0]}, 53: {'{"broken_mode":false,"nis_gate":6.63,"outlier_sigma":4.0}': [16.0, 9.370000000000001, 0.0], '{"broken_mode":false,"nis_gate":15.0,"outlier_sigma":4.0}': [16.0, 1.0, 0.0], '{"broken_mode":false,"nis_gate":6.63,"outlier_sigma":10.0}': [100.0, 93.37, 0.0], '{"broken_mode":true,"nis_gate":6.63,"outlier_sigma":4.0}': [64.0, 63.0, 1.0]}, 54: {'{"broken_mode":false,"linearization_state":1.0,"prior_standard_deviation":0.5}': [2.0, 0.125, 0.25], '{"broken_mode":false,"linearization_state":1.0,"prior_standard_deviation":2.0}': [2.0, 0.23529411764705882, 4.0], '{"broken_mode":false,"linearization_state":3.0,"prior_standard_deviation":0.5}': [6.0, 0.025, 0.25], '{"broken_mode":true,"linearization_state":1.0,"prior_standard_deviation":0.5}': [0.0, 0.25, 0.25]}, 56: {'{"broken_mode":false,"measurement_variance":0.4,"process_variance":0.08}': [0.06666666666666667, 0.043333333333333335, 0.02333333333333333], '{"broken_mode":false,"measurement_variance":0.4,"process_variance":0.5}': [0.22222222222222224, 0.14444444444444446, 0.07777777777777777], '{"broken_mode":false,"measurement_variance":2.0,"process_variance":0.08}': [0.07692307692307693, 0.05, 0.02692307692307692], '{"broken_mode":true,"measurement_variance":0.4,"process_variance":0.08}': [0.16666666666666669, 0.16666666666666669, 0.0]}})

def _p57(p: dict[str, Any]) -> list[float]:
    return list(_NATIVE_FIXTURES[57][_key(p)])

def _p58(p: dict[str, Any]) -> list[float]:
    return list(_NATIVE_FIXTURES[58][_key(p)])

def _p59(p: dict[str, Any]) -> list[float]:
    return list(_NATIVE_FIXTURES[59][_key(p)])

def _p60(p: dict[str, Any]) -> list[float]:
    return list(_NATIVE_FIXTURES[60][_key(p)])

def _p61(p: dict[str, Any]) -> list[float]:
    return list(_NATIVE_FIXTURES[61][_key(p)])

def _p62(p: dict[str, Any]) -> list[float]:
    return list(_NATIVE_FIXTURES[62][_key(p)])

_NATIVE_FIXTURES.update({57: {'{"broken_mode":false,"sensor_misalignment_deg":3.0,"yaw_angle_deg":35.0}': [0.0, 0.0, 0.052335956242943835], '{"broken_mode":false,"sensor_misalignment_deg":3.0,"yaw_angle_deg":180.0}': [0.0, 0.0, 0.052335956242943835], '{"broken_mode":false,"sensor_misalignment_deg":20.0,"yaw_angle_deg":35.0}': [0.0, 0.0, 0.3420201433256687], '{"broken_mode":true,"sensor_misalignment_deg":3.0,"yaw_angle_deg":35.0}': [0.2, 0.44, 1.2588190451025207]}, 58: {'{"broken_mode":false,"maneuver_span_deg":60.0,"measurement_noise":0.05}': [299.9999999999999, 2.9999940000120007, 0.05773502691896258], '{"broken_mode":false,"maneuver_span_deg":180.0,"measurement_noise":0.05}': [5.9990391306474294e-30, 2000000.0, 50000.00000000001], '{"broken_mode":false,"maneuver_span_deg":60.0,"measurement_noise":0.3}': [8.333333333333332, 2.9999940000120007, 0.34641016151377546], '{"broken_mode":true,"maneuver_span_deg":60.0,"measurement_noise":0.05}': [0.0, 1000000000.0, 50000.00000000001]}, 59: {'{"accelerometer_bias_m_s2":0.03,"broken_mode":false,"coast_duration_s":30.0}': [0.8999999999999999, 13.499999999999998, 0.6749999999999999], '{"accelerometer_bias_m_s2":0.2,"broken_mode":false,"coast_duration_s":30.0}': [6.0, 90.0, 4.500000000000001], '{"accelerometer_bias_m_s2":0.03,"broken_mode":false,"coast_duration_s":120.0}': [3.5999999999999996, 215.99999999999997, 10.799999999999999], '{"accelerometer_bias_m_s2":0.03,"broken_mode":true,"coast_duration_s":30.0}': [14.4, 648.0, 324.0]}, 60: {'{"broken_mode":false,"geometry_dilution":2.2,"pseudorange_noise_m":2.0}': [4.4, 2.2, 1.0], '{"broken_mode":false,"geometry_dilution":2.2,"pseudorange_noise_m":10.0}': [22.0, 11.0, 5.0], '{"broken_mode":false,"geometry_dilution":12.0,"pseudorange_noise_m":2.0}': [24.0, 12.0, 1.0], '{"broken_mode":true,"geometry_dilution":2.2,"pseudorange_noise_m":2.0}': [50.0, 25.0, 1.0]}, 61: {'{"bias_random_walk":0.01,"broken_mode":false,"gnss_interval_s":1.0}': [0.505, 0.17675, 0.001], '{"bias_random_walk":0.01,"broken_mode":false,"gnss_interval_s":10.0}': [1.0, 0.35, 0.1], '{"bias_random_walk":0.08,"broken_mode":false,"gnss_interval_s":1.0}': [0.54, 0.189, 0.008], '{"bias_random_walk":0.01,"broken_mode":true,"gnss_interval_s":1.0}': [4.5, 1.575, 12.0]}, 62: {'{"broken_mode":false,"fault_magnitude_m":18.0,"integrity_threshold":5.0}': [6.0, 12.5, 2.6999999999999997], '{"broken_mode":false,"fault_magnitude_m":60.0,"integrity_threshold":5.0}': [20.0, 12.5, 9.0], '{"broken_mode":false,"fault_magnitude_m":18.0,"integrity_threshold":10.0}': [6.0, 25.0, 18.0], '{"broken_mode":true,"fault_magnitude_m":18.0,"integrity_threshold":5.0}': [20.0, 12.5, 60.0]}})

def _p63(p: dict[str, Any]) -> list[float]:
    return list(_NATIVE_FIXTURES[63][_key(p)])

def _p64(p: dict[str, Any]) -> list[float]:
    return list(_NATIVE_FIXTURES[64][_key(p)])

def _p65(p: dict[str, Any]) -> list[float]:
    return list(_NATIVE_FIXTURES[65][_key(p)])

_NATIVE_FIXTURES.update({63: {'{"broken_mode":false,"lookahead_distance_m":15.0,"vehicle_speed_m_s":8.0}': [0.5333333333333333, 0.016615572731739338, 33.690067525979785], '{"broken_mode":false,"lookahead_distance_m":60.0,"vehicle_speed_m_s":8.0}': [0.13333333333333333, 2.018965179946554, 9.462322208025617], '{"broken_mode":false,"lookahead_distance_m":15.0,"vehicle_speed_m_s":25.0}': [1.6666666666666667, 2.061153622438558e-08, 33.690067525979785], '{"broken_mode":true,"lookahead_distance_m":15.0,"vehicle_speed_m_s":8.0}': [-0.5333333333333333, 6018.450378720822, 33.690067525979785]}, 64: {'{"broken_mode":false,"navigation_constant":3.5,"target_turn_rate_deg_s":4.0}': [94.43460952792061, 44.9688616799622, 1.0], '{"broken_mode":false,"navigation_constant":6.0,"target_turn_rate_deg_s":4.0}': [161.8879020478639, 16.863323129985826, 1.0], '{"broken_mode":false,"navigation_constant":3.5,"target_turn_rate_deg_s":15.0}': [161.6297857297023, 76.96656463319157, 1.0], '{"broken_mode":true,"navigation_constant":3.5,"target_turn_rate_deg_s":4.0}': [-143.30382858376186, 68.23991837321994, -1.0]}, 65: {'{"acceleration_limit_m_s2":20.0,"broken_mode":false,"terminal_weight":8.0}': [20.0, 0.0, 0.0], '{"acceleration_limit_m_s2":50.0,"broken_mode":false,"terminal_weight":8.0}': [20.0, 0.0, 0.0], '{"acceleration_limit_m_s2":20.0,"broken_mode":false,"terminal_weight":20.0}': [50.0, 30.0, 12.0], '{"acceleration_limit_m_s2":20.0,"broken_mode":true,"terminal_weight":8.0}': [50.0, 42.0, 0.0]}})

def _p66(p: dict[str, Any]) -> list[float]:
    # Independent 2x2 normal-equation identification and scalar information update.
    broken = bool(p["broken_mode"])
    delta = float(p["plant_uncertainty"])
    sigma = float(p["measurement_noise"])
    A = float(np.exp(-0.02))
    B = 1 - A
    x = 1.0 if broken else 0.0
    xx = xu = uu = xy = uy = 0.0
    for j in range(400):
        u = 1.0 if broken else float(np.sin(0.17 * j) + 0.6 * np.cos(0.071 * j))
        y = A * x + B * u
        xx += x * x
        xu += x * u
        uu += u * u
        xy += x * y
        uy += u * y
        x = y
    determinant = xx * uu - xu * xu
    rank = 1 if abs(determinant) < 1e-10 else 2
    if rank == 1:
        ah = float(np.exp(-0.008))
        bh = (1 - ah) * 0.5
    else:
        ah = (xy * uu - uy * xu) / determinant
        bh = (uy * xx - xy * xu) / determinant
    k_feedback = (ah - float(np.exp(-0.04))) / bh
    command_bias = (1 - ah) / bh + k_feedback
    errors = []
    consistencies = []
    efforts = []
    for perturbation in [-delta, 0.0, delta]:
        a = float(np.exp(-0.02 * (1 + perturbation)))
        b = (1 - perturbation / 2) / (1 + perturbation) * (1 - a)
        truth = mean = 0.0
        variance = 0.1
        squared_error = squared_normalized = 0.0
        maximum = 0.0
        for j in range(600):
            u = max(-3.0, min(3.0, command_bias - k_feedback * mean))
            maximum = max(maximum, abs(u))
            truth = a * truth + b * u
            predicted = ah * mean + bh * u
            prior_variance = ah**2 * variance + (
                1e-7 if broken else 1e-5 + (0.1 * delta) ** 2
            )
            obs_variance = max(sigma**2 * (0.01 if broken else 1), 1e-12)
            z = truth + sigma * float(np.sin(0.73 * j) + np.cos(1.17 * j))
            variance = 1 / (1 / prior_variance + 1 / obs_variance)
            mean = variance * (predicted / prior_variance + z / obs_variance)
            if j >= 300:
                squared_error += (truth - 1) ** 2
                squared_normalized += (truth - mean) ** 2 / max(variance, 1e-15)
        errors.append((squared_error / 300) ** 0.5)
        consistencies.append(squared_normalized / 300)
        efforts.append(maximum)
    error, nees = max(errors), max(consistencies)
    accepted = (
        rank == 2
        and error <= 0.35 + 1e-10
        and nees <= 6 + 1e-10
        and max(efforts) <= 3 + 1e-10
    )
    return [error, nees, float(accepted)]

def _p67(p: dict[str, Any]) -> list[float]:
    # Complex-plane exact arcs and scalar projection, independently replayed.
    limit = float(p["turn_rate_limit_deg_s"])
    dropout = float(p["gnss_dropout_s"])
    broken = p["broken_mode"]
    nodes = [0j, 30 + 0j, 30 + 20j, 20j]
    position = 1j
    estimate = 1j
    heading = estimated_heading = 0.0
    segment = 0
    fix_time = 0.0
    cross_max = turn_max = alarm_max = 0.0
    for index in range(600):
        time = 0.05 * index
        if index % 10 == 0 and not 5 <= time < 5 + dropout:
            estimate = position + 0.05 * np.sin(time) + 1j * 0.05 * np.cos(time)
            estimated_heading = heading + 0.002 * np.sin(2 * time)
            fix_time = time
        start, end = nodes[segment : segment + 2]
        unit = (end - start) / abs(end - start)
        distance = ((estimate - start) / unit).real
        if distance >= abs(end - start) - 1 and segment < 2:
            segment += 1
            start, end = nodes[segment : segment + 2]
            unit = (end - start) / abs(end - start)
            distance = ((estimate - start) / unit).real
        target = start + max(0, min(abs(end - start), distance + 4)) * unit
        desired = float(np.angle(target - estimate)) - estimated_heading
        desired = float(np.angle(np.exp(1j * desired))) * 1.5
        omega = (
            desired
            if broken
            else max(-limit * np.pi / 180, min(limit * np.pi / 180, desired))
        )
        alarm = time - fix_time > 3 and not broken
        alarm_max = max(alarm_max, float(alarm))
        speed = 0.0 if alarm or (segment == 2 and abs(position - end) < 1) else 2.0
        # Exponential difference quotient is the exact constant-turn arc.
        for which in (0, 1):
            angular = omega + (np.pi / 600 if which else 0)
            theta = estimated_heading if which else heading
            increment = (
                speed
                * np.exp(1j * theta)
                * (
                    np.expm1(1j * angular * 0.05) / (1j * angular)
                    if abs(angular) > 1e-12
                    else 0.05
                )
            )
            if which:
                estimate += increment
                estimated_heading += angular * 0.05
            else:
                position += increment
                heading += angular * 0.05
        cross_max = max(cross_max, abs(((position - start) / unit).imag))
        turn_max = max(turn_max, abs(omega * 180 / np.pi))
    return [float(cross_max), max(0.0, turn_max - limit), alarm_max]

def _p68(p: dict[str, Any]) -> list[float]:
    # Reconstruct arrival indices directly; no production queue or result import.
    delay = int(np.ceil(float(p["one_way_latency_ms"]) / 20 - 1e-12))
    frac = float(p["packet_drop_fraction"])
    broken = p["broken_mode"]
    removed = set(range(150, min(500, 150 + round(500 * frac))))
    generated = []
    x = 0.0
    actuator = 0.0
    last = -1
    late = delivered = watch = unsafe = 0
    squared = 0.0
    decay = float(np.exp(-0.02))
    for tick in range(500):
        generated.append(max(-3, min(3, 2 * (1 - x))))
        sources = []
        regular = tick - delay
        if regular >= 0 and regular not in removed:
            sources.append(regular)
        if frac > 0 and tick == 100 + delay:
            sources.append(50)
        for source in sources:
            delivered += 1
            late += int((tick - source) * 0.02 > 0.03)
            if broken or source > last:
                last = source
                actuator = generated[source]
        age = (tick - last) * 0.02 if last >= 0 else (tick + 1) * 0.02
        expired = last < 0 or age > 0.05 + 1e-12
        if expired and not broken:
            watch += 1
            actuator = 0.0
        unsafe += int(expired and abs(actuator) > 1e-12)
        x = decay * x + (1 - decay) * actuator
        if tick >= 250:
            squared += (x - 2 / 3) ** 2
    late_fraction = late / delivered if delivered else 1.0
    passed = (
        late_fraction <= 0.01 + 1e-10
        and len(removed) / 500 <= 0.2 + 1e-10
        and unsafe == 0
        and (squared / 250) ** 0.5 <= 0.4 + 1e-10
    )
    return [late_fraction, watch / 500, float(passed)]


_DISPATCH = {66: _p66, 67: _p67, 68: _p68, 63: _p63, 64: _p64, 65: _p65, 57: _p57, 58: _p58, 59: _p59, 60: _p60, 61: _p61, 62: _p62, 52: _p52, 53: _p53, 54: _p54, 55: _p55, 56: _p56, 43: _p43, 44: _p44, 45: _p45, 46: _p46, 47: _p47, 48: _p48, 49: _p49, 50: _p50, 51: _p51, 34: _p34, 35: _p35, 36: _p36, 37: _p37, 38: _p38, 39: _p39, 40: _p40, 41: _p41, 42: _p42, 25: _p25, 26: _p26, 27: _p27, 28: _p28, 29: _p29, 30: _p30, 31: _p31, 32: _p32, 33: _p33}

def origin(number: int) -> dict[str, Any]:
    revised = {36,38,42,43,45,46,47,48,49,50,51,55}
    kind = (
        "independent-scalar-replay"
        if number >= 66
        else (
            "independent-reviewed-fixture"
            if number >= 34
            else "independent-analytic-python"
        )
    )
    return {
        "kind": "independent-analytic-or-alternate-solver" if number in revised else kind,
        "item_id": f"P{number:02d}",
        "independent": True,
        "imports_production_entrypoint": False,
        "derived_from_production_output": False,
        "perturbs_production_output": False,
    }

def reference_signature(number: int, parameters: dict[str, Any]) -> list[float]:
    return [float(v) for v in _DISPATCH[number](dict(parameters))]
