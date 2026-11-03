# From a measurement update to a recursive EKF

The first plots isolate one quadratic measurement update. The additional plots
close the feedback loop: the posterior at sample k becomes the next prior.
All states are normalized dimensionless quantities; the clock is a sample index.

## Model and prediction

For 80 samples use

$$
f_k(x)=0.94x+0.08\sin x+0.05\cos(0.2k),\qquad h(x)=0.4x+0.1x^2.
$$

The declared filter model has additive $Q=0.0004$, $R=0.01$. Synthetic truth
starts at 0.8 and adds $0.015\sin(0.7k)$ to f; observations add
$0.08\cos(0.9k)$ to h. These deterministic disturbances are repeatable and are
not Gaussian draws. Prior standard deviation and initial linearization state
come from the two existing controls.

$$
\hat x_k^-=f_k(\hat x_{k-1}^+),\quad F_k=0.94+0.08\cos\hat x_{k-1}^+,
\quad P_k^-=F_k^2P_{k-1}^++Q.
$$

## Conditioning and feedback

$$
H_k=0.4+0.2\hat x_k^-,\quad r_k=z_k-h(\hat x_k^-),\quad
S_k=H_k^2P_k^-+R,\quad K_k=P_k^-H_k/S_k.
$$

$$
\hat x_k^+=\hat x_k^-+K_kr_k,\quad
P_k^+=(1-K_kH_k)^2P_k^-+K_k^2R.
$$

The Joseph expression preserves the covariance interpretation. It does not
correct a wrong process model. For the default initial state 1 and sigma 0.5,
the first predicted state is approximately 1.05632 and predicted variance
0.24208. Recompute the first gain and posterior from the displayed equation,
then verify that sample two starts from that posterior, not from the original
initial condition.

## Fault, recovery and assessment

Predict the consequences of setting H=0 at every sample. Toggle the fault:
K becomes zero, the filter predicts but never uses measurements. Reset recovers
exactly the same nominal sequence. Sweep initial state at fixed sigma, then
sigma at fixed initial state; record first gain, final error and RMS error.
Explain why a small sigma can slow correction of an initially wrong state.

The error plot includes ±2 formal standard deviations. NIS is $r^2/S$; NEES
is $(\hat x-x_{truth})^2/P$. A trace within those bands is not a calibrated
95% coverage result for this deterministic stream. The original squared-only
measurement has sign ambiguity; the recursive experiment uses a different,
locally informative measurement map, explicitly given above.

A satisfactory answer shows the prediction-to-posterior recurrence, quantifies
both sweeps, diagnoses the zero-gain fault, and states the Gaussian/local-model
limitations. Compare P55 on its matching initial state of 1.

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
