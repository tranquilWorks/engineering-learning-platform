# Coupled GNSS/INS error-state estimation

The original one-axis filter isolates injection. The additional 3D experiment
uses the P59 mechanization with a 15-coordinate error state
$\delta x=(\delta p,\delta v,\delta\theta,\delta b_a,\delta b_g)$.
The nominal state carries a quaternion, while covariance uses a three-component
small right attitude error. Gravity is known; it is not a sixteenth estimated state.

## Prediction and coupling

The nonzero continuous Jacobian blocks are

$$
F_{pv}=I,\quad F_{v\theta}=-R[f]_{\times},\quad F_{vb_a}=-R,
$$
$$
F_{\theta\theta}=-[\omega]_{\times},\quad F_{\theta b_g}=-I.
$$

The implementation uses $\Phi=I+F\Delta t+\tfrac12F^2\Delta t^2$ and
$P^-=\Phi P^+\Phi^T+Q_d$. This bounded second-order discretization has a separate
finite-perturbation/step-refinement check. Sensor noise densities are 0.02 m/s²/√Hz
and 0.001 rad/s/√Hz; the bias-random-walk control supplies accelerometer-bias
process uncertainty. Gyro-bias walk is 0.0001 rad/s/√s. Truth biases are constant:
the random-walk control changes the assumed model, not a secretly randomized truth.

## GNSS measurement pipeline

Six synthetic satellite locations generate pseudoranges with a 75 m receiver
clock offset and deterministic 0.03 m sinusoidal perturbations. Iterative least
squares solves three Cartesian receiver coordinates and the clock offset. The
result supplies position observations to the INS filter; this is **loosely coupled
GNSS/INS**, not raw-pseudorange tightly coupled estimation. A conservative declared
position observation covariance is 0.25 I m², not a claimed receiver covariance.

With $H=[I\;0\;0\;0\;0]$,

$$
S=HP^-H^T+R_z,\quad K=P^-H^TS^{-1},\quad \delta\hat x=K(z-\hat p).
$$

Position-only observations correct velocity, attitude and biases through the
cross-covariances created by the dynamics. Their observability depends on motion
and geometry; one run cannot prove every bias is observable.

## Injection and reset

Add position, velocity and bias corrections; apply
$q^+=q^-\otimes\mathrm{Exp}(\delta\hat\theta)$ and normalize.
Use the Joseph measurement covariance, then reset its coordinates:

$$
G_{\theta\theta}=I-\tfrac12[\delta\hat\theta]_{\times},\qquad P^+=G P_{Joseph}G^T.
$$

The mean error state resets to zero. This first-order reset is local; large
attitude uncertainty or large corrections require a more appropriate estimator.
The fault updates formal covariance while withholding all nominal corrections.
A small displayed covariance beside growing error is then intentionally inconsistent.

## Assessment

Sweep GNSS interval from 0.2 to 10 seconds at fixed bias walk, then sweep walk.
Record terminal position error, unaided error, last correction in all five state
groups, and minimum covariance eigenvalue. Explain how position observations
reach gyro bias through attitude and velocity cross-covariance. Recompute one
update by information conditioning and compare quaternion orientation, allowing
q and -q to represent the same rotation. Toggle fault, verify lost injection,
and reset. Do not describe the formal sigma norm as a calibrated 95% region.

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
