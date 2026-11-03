# From the unscented transform to a recursive UKF

The original square-map plots isolate the transform. The added 80-sample
sequence uses the same nonlinear dynamics, observations and deterministic
forcing as the recursive EKF in P54, with initial estimate 1. The state sigma
and alpha controls now also affect this complete recursive sequence.

## Sigma points through prediction

For scalar mean m and variance P, the points are $m,m\pm\alpha\sqrt P$.
Mean weights are $1-1/\alpha^2,1/(2\alpha^2),1/(2\alpha^2)$.
Covariance weights add $1-\alpha^2+\beta$ to the central weight, with $\beta=2$.
Propagate each point through
$f_k(x)=0.94x+0.08\sin x+0.05\cos(0.2k)$, then reconstruct predicted mean
and covariance and add $Q=0.0004$.

**Generate fresh sigma points from the resulting prior covariance.** Reusing
points from before adding Q would omit process-noise uncertainty from the
measurement transform. Pass the fresh points through $h(x)=0.4x+0.1x^2$.
Reconstruct measurement mean, innovation covariance S (including R=0.01), and
state/measurement cross covariance C.

$$
K=C/S,\quad m^+=m^-+K(z-\bar z),\quad
P^+=P^- -2KC+K^2S.
$$

With the optimal scalar gain this is $P^- - C^2/S$. The new posterior produces
the next step's sigma points: both process prediction and measurement correction
are executed, not just one transform. A scalar Gaussian approximation remains
unimodal and cannot represent arbitrary multimodal posteriors.

## An independent moment check

For the quadratic measurement and beta=2, the scalar transform yields

$$
\bar z=0.4m+0.1(m^2+P),\quad C=(0.4+0.2m)P,
$$
$$
S=(0.4+0.2m)^2P+0.02P^2+R.
$$

These analytic symmetric-moment expressions independently verify the actual
sigma-point measurement calculation. The square-map component still demonstrates
why a negative central mean weight need not invalidate the transform.

## Fault, recovery and assessment

The component fault omits its covariance-weight correction. In the recursive
sequence the same toggle deliberately withholds every measurement correction:
mean/covariance prediction continues, but K is zero. These are two explicitly
different failures in two linked experiments; a negative component variance is
never fed into a recursive square root.

Sweep alpha from 0.2 to 2 at fixed state sigma, then sweep sigma. Record transformed
moments, recursive RMSE, first gain and final covariance. Compare with P54 using
initial state 1 and the same sigma. Explain why nonlinear transition moments can
change with alpha even though the quadratic measurement identities above do not.
Reset and demonstrate identical recovery. Identify the process-noise re-sampling
step and distinguish formal NIS/NEES from empirical statistical coverage.

## Evidence boundary

These are bounded synthetic software experiments, not measured navigation or
statistical coverage certification. All state, measurement and covariance histories
are returned by the actual lesson runtime. The independent reference lives in
`recursive_navigation_references.py`; it does not import the lesson implementation.
Historical component plots and their numerical signatures remain intact so the
new integrated behavior can be compared with those limiting cases.

## Further reading

[Julier and Uhlmann, Unscented Filtering and Nonlinear Estimation (2004)](https://doi.org/10.1109/JPROC.2003.823141).

The numerical evidence table shows selected epochs (including the first two and final sample); complete histories are retained by the runtime and independent verifier. Values in each column use the units in its label.
