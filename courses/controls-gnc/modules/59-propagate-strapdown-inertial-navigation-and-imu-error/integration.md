# Three-dimensional strapdown propagation

The one-axis bias experiment remains as an analytic limiting case. The additional
sequence propagates position, velocity and a unit quaternion in a local ENU frame.
This is full attitude/velocity/position mechanization within a stated flat-Earth
model; it omits Earth rotation, curvature, transport rates and coning/sculling
beyond the midpoint sample approximation.

## Frames, sensors and gravity

$q$ maps body vectors into local ENU. Quaternion order is scalar first; updates
multiply body-frame increments on the right. Gravity is $g^n=(0,0,-9.80665)$ m/s².
An accelerometer measures specific force, not inertial acceleration:

$$
f^b=R_{nb}^T(a^n-g^n),\qquad a^n=R_{nb}(f_m^b-b_a)+g^n.
$$

At rest a level sensor reads +9.80665 m/s² on body z. Adding downward gravity
cancels it. Rotating a one m/s² body-x force by 90 degrees yaw must produce
local north acceleration. These two checks catch gravity and frame-sign errors.

## Executed integration

$$
\Delta\theta=(\omega_m-b_g)\Delta t,\quad
q_{k+1}=q_k\otimes\mathrm{Exp}(\Delta\theta).
$$

Use the half-step quaternion for acceleration, then
$p_{k+1}=p_k+v_k\Delta t+\tfrac12a_k\Delta t^2$ and
$v_{k+1}=v_k+a_k\Delta t$. Normalize q after multiplication.
The run has 240 intervals over the selected duration. Truth includes all three
angular-rate components and all three acceleration components. The recorded
accelerometer bias controls $(b,-b/2,b/4)$; gyro bias is
$(0.0004,-0.0003,0.0006)$ rad/s.

The corrected path subtracts **a prescribed 95% of both bias vectors**. It does
not estimate them. Fault mode subtracts neither. A parallel unaided path sees the
same sensor stream. The full three-dimensional drift includes tilt-induced
gravity leakage, so it need not equal the one-axis $bT^2/2$ formula.

## Prediction and worked checks

For b=0.03 m/s² and T=30 s, the retained single-axis result is 0.9 m/s velocity
error and 13.5 m position error; its prescribed correction leaves 0.675 m.
The 3D sequence also has gyro bias, so even b=0 need not eliminate position error.
A small tilt error produces approximately $g\delta\theta$ horizontal acceleration;
constant gyro bias can therefore produce cubic-in-time position drift initially.

Sweep b at fixed T, then T at fixed b. Record 3D terminal error, unaided error,
attitude error, and quaternion norm. Toggle fault and recover. Explain why the
one-axis formula and 3D errors differ, and why a calibrated gyro matters even
when the accelerometer bias slider is zero. P61 replaces prescribed calibration
with actual coupled estimation from GNSS observations.

## Evidence boundary

These are bounded synthetic software experiments, not measured navigation or
statistical coverage certification. All state, measurement and covariance histories
are returned by the actual lesson runtime. The independent reference lives in
`recursive_navigation_references.py`; it does not import the lesson implementation.
Historical component plots and their numerical signatures remain intact so the
new integrated behavior can be compared with those limiting cases.

## Further reading

[Solà, Quaternion kinematics for the error-state Kalman filter, sections 5–6](https://arxiv.org/html/1711.02508v1).

The numerical evidence table shows selected epochs (including the first two and final sample); complete histories are retained by the runtime and independent verifier. Values in each column use the units in its label.
