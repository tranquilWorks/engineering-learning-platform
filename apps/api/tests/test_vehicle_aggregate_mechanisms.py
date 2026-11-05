"""Independent physical identities and full histories for the Vehicle repairs."""
import importlib.util
from pathlib import Path

import numpy as np
import pytest
from scipy.integrate import solve_ivp
from scipy.linalg import eigh

COURSE = Path(__file__).resolve().parents[3] / 'courses/vehicle-dynamics'


def load(number):
    path = next((COURSE/'modules').glob(f'{number:02d}-*'))/'experiment.py'
    spec = importlib.util.spec_from_file_location(f'vehicle_{number}', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize('steer,mu,broken', [(1,.7,False),(6,1.15,False),(10,.7,False),(3.37,.93,False),(10,1.5,False),(6,1.15,True),(10,.7,True)])
def test_nonlinear_bicycle_full_history_and_jacobian(steer, mu, broken):
    module=load(37)
    p={'steer_deg':steer,'friction_mu':mu}
    study=module._dynamic_study(p,broken)
    # Independent lateral-velocity coordinates, axle moment balance and DOP853.
    def rhs(t,state):
        lateral,yaw=state
        slips=[np.deg2rad(steer)-(lateral+1.2*yaw)/28, -(lateral-1.5*yaw)/28]
        limits=mu*9.81*np.array([1450*1.5/2.7,1450*1.2/2.7])
        requested=np.array([70000,75000])*slips
        forces=requested if broken else limits*np.tanh(requested/limits)
        return [(sum(forces)-1450*28*yaw)/1450, np.dot([1.2,-1.5],forces)/2400]
    independent=solve_ivp(rhs,[0,study['time'][-1]],[0,0],t_eval=study['time'],method='DOP853',rtol=1e-11,atol=1e-12)
    states=independent.y.T/np.array([28,1])
    np.testing.assert_allclose(study['states'],states,atol=2e-8,rtol=2e-7)
    refined=module._dynamic_study(p,broken,dt=.0025)
    common=min(len(study['states']),len(refined['states'][::2]))
    np.testing.assert_allclose(study['states'][:common],refined['states'][::2][:common],atol=2e-8,rtol=2e-7)
    point=np.array([-.07,.21]);epsilon=1e-6
    _,jac,_=module._dynamic_rhs(point,np.deg2rad(steer),mu,broken)
    numeric=np.column_stack([(module._dynamic_rhs(point+epsilon*axis,np.deg2rad(steer),mu,broken)[0]-module._dynamic_rhs(point-epsilon*axis,np.deg2rad(steer),mu,broken)[0])/(2*epsilon) for axis in np.eye(2)])
    np.testing.assert_allclose(jac,numeric,rtol=2e-8,atol=2e-8)
    if study['trim_valid']:
        np.testing.assert_allclose(rhs(0,study['trim']*np.array([28,1])),0,atol=3e-7)
        assert study['decay_margin']==pytest.approx(-max(np.linalg.eigvals(module._dynamic_rhs(study['trim'],np.deg2rad(steer),mu,broken)[1]).real))
    else:
        assert study['decay_margin']==0
    if not broken:
        assert max(study['utilization'])<=1
    assert np.max(abs(study['states'][:,0]))<=.35


@pytest.mark.parametrize('accel,fraction',[(.2,.3),(1,.58),(1.5,.75),(.73,.413)])
def test_transfer_force_moment_and_contact_boundary(accel,fraction):
    module=load(38)
    model=module._model({'lateral_accel_g':accel,'front_roll_stiffness_fraction':fraction},False)
    front,rear,_,closure,loss=model['signature']
    assert front*1.55+rear*1.53==pytest.approx(1450*accel*9.81*.52)
    weight=1450*9.81*1.5/2.7
    normals=np.linalg.solve([[1,1],[-1.55/2,1.55/2]],[weight,front*1.55])
    if min(normals)>=0:
        expected=1.25*3500*(2*(weight/7000)**.86-sum((normals/3500)**.86))
        assert loss==pytest.approx(expected)
    assert closure<1e-9
    assert module._capacity_loss(weight,0)==pytest.approx(0,abs=1e-10)
    assert module._capacity_loss(weight,weight)==pytest.approx(module._capacity_loss(weight,weight/2))
    assert np.all(np.diff([module._capacity_loss(weight,t) for t in np.linspace(0,weight/2,50)])>=0)


@pytest.mark.parametrize('front,rear,broken',[(42000,38000,False),(65000,25000,False),(31731,51237,False),(42000,38000,True)])
def test_modal_energy_and_generalized_eigenproblem(front,rear,broken):
    module=load(39)
    m=np.diag([1450,2600,650])
    geometry=np.array([[1,1.2,.775],[1,1.2,-.775],[1,-1.5,.765],[1,-1.5,-.765]])
    k=geometry.T @ np.diag([1.04*front,.96*front,.97*rear,1.03*rear]) @ geometry
    values,vectors=eigh(np.diag(np.diag(k)) if broken else k,m)
    result=module._model({'front_spring_rate_n_m':front,'rear_spring_rate_n_m':rear},broken)
    np.testing.assert_allclose(result['signature'][:3],np.sqrt(values)/(2*np.pi),atol=1e-12)
    expected=np.diag(m)[:,None]*vectors**2
    actual=np.array([t['y'] for t in result['plots']['mechanism']['data']])
    np.testing.assert_allclose(actual,expected,atol=1e-12)
    np.testing.assert_allclose(actual.sum(axis=0),1,atol=1e-12)
    assert result['signature'][-1] > .01 if broken else result['signature'][-1]<1e-12


@pytest.mark.parametrize('gain,noise',[(.35,.08),(.13,.033),(.7,.2)])
def test_observer_covariance_complete_history_independent_sum(gain,noise):
    module=load(57)
    actual=module._covariance_history(gain,noise)
    f=np.eye(3)+.02*np.array([[-1.1,-.35,.2],[.8,-1.6,.1],[0,0,-.25]])
    l=np.diag([gain,.75*gain,.45*gain]);c=np.eye(3)-l
    closed=c@f
    added=c@np.diag([2e-5,4e-5,1e-5])@c.T+noise**2*l@l.T
    # Sum independent noise contributions from each previous epoch.
    powers=[np.linalg.matrix_power(closed,i) for i in range(301)]
    accumulated=np.zeros((3,3))
    expected=[]
    for i,power in enumerate(powers):
        expected.append(power@(.25*np.eye(3))@power.T+accumulated)
        accumulated+=power@added@power.T
    np.testing.assert_allclose(actual,expected,atol=1e-14,rtol=1e-11)
    assert np.linalg.eigvalsh(actual).min()>0
    larger=module._covariance_history(gain,noise*2)
    assert np.trace(larger[-1])>np.trace(actual[-1])


@pytest.mark.parametrize('excitation,sigma',[(.2,150),(.7,80),(.437,36.7)])
def test_parameter_covariance_matches_qr_and_excitation_scaling(excitation,sigma):
    module=load(59)
    signature,_,_,standard=module._analyze(excitation,sigma,False)
    i=np.arange(60)
    x=excitation*np.column_stack([.030*np.sin(.25*i)+.008*np.cos(.53*i),.028*np.sin(.25*i+.16)+.004*np.cos(.91*i)])
    _,r=np.linalg.qr(x,mode='reduced');inverse=np.linalg.solve(r,np.eye(2))
    np.testing.assert_allclose(standard,np.sqrt(np.diag(sigma**2*inverse@inverse.T)),rtol=1e-12)
    twice=module._analyze(excitation*2,sigma,False)
    np.testing.assert_allclose(twice[-1],standard/2,rtol=1e-12)
    assert signature[5] in (0,.5,1)


@pytest.mark.parametrize('sigma,fraction',[(80,.35),(25,.2),(137,.47)])
def test_prediction_band_includes_parameter_uncertainty(sigma,fraction):
    module=load(33)
    result=module._model({'observation_sigma_n':sigma,'validation_fraction':fraction},False)
    traces={t['name']:t for t in result['plots']['mechanism']['data']}
    upper=traces['Conditional predictive upper']['y']
    assert np.all(upper>1.96)
    # The added parameter term must increase with held-out regressor magnitude.
    x=np.array(result['plots']['response']['data'][0]['x'])
    ratio=(upper/1.96)**2-1
    np.testing.assert_allclose(ratio/x**2,np.full_like(x,ratio[0]/x[0]**2),rtol=1e-11)


def test_shift_interruption_pays_road_resistance():
    module=load(47)
    _,time,speed,gears=module._simulate(4.1,.25,False)
    differences=np.diff(speed)
    assert np.any(differences<0)
    indices=np.flatnonzero(differences<0)
    expected=-(180+.38*speed[indices]**2)/1450*np.diff(time)[indices]
    np.testing.assert_allclose(differences[indices],expected,atol=1e-12,rtol=1e-10)
    assert gears[0]>=1


@pytest.mark.parametrize('number,key',[(26,'response'),(34,'response'),(35,'response'),(37,'state_history'),(52,'mechanism'),(53,'response')])
def test_repaired_axes_have_one_unit_per_axis(number,key):
    module=load(number)
    result=module.run({})
    plot=result['plots'][key]
    units={}
    for trace in plot['data']:
        units.setdefault(trace.get('yaxis','y'),set()).add(trace['meta']['y_unit'])
    assert all(len(v)==1 for v in units.values())
    assert 'yaxis2' in plot['layout']
