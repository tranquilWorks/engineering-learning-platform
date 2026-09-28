# Identify, control, estimate, and stress one plant

The claim is deliberately small: a known synthetic calibration record identifies a normalized first-order plant; that model then drives a feedback controller and a scalar estimator across three uncertain plants. Passing a plot by eye cannot replace passing each stage.

## Model and equations

With normalized state $x$ and command $u$, $\dot x=-a x+b u$, where $a$ and $b$ have units $\mathrm{s^{-1}}$. Holding a command for $\Delta t=0.02\,\mathrm{s}$ gives

\[x_{k+1}=A x_k+B u_k,\qquad A=e^{-a\Delta t},\quad B=\frac b a(1-A).\]

Four hundred known-state calibration samples fit $[\hat A,\hat B]$ by least squares on columns $[x_k,u_k]$. Sines at two discrete frequencies excite both columns. This is not identification from noisy, unknown physical states.

Place the nominal discrete pole at $p=e^{-2\Delta t}$: $K=(\hat A-p)/\hat B$, $N=(1-\hat A+\hat B K)/\hat B$, and $u=\operatorname{clip}(N-K\hat x,-3,3)$. The scalar Kalman recursion propagates $P^-=\hat A^2P+Q$, uses $L=P^-/(P^-+R)$ and updates $P=(1-L)P^-$. Healthy tuning uses $R=\sigma^2$ and $Q=10^{-5}+(0.1\delta)^2$ in squared normalized-state units per sample. This declared process allowance is a tuning model for mismatch, not a measured disturbance covariance.

The three actual plants use $a=1+s$, $b=1-s/2$ for $s\in\{-\delta,0,\delta\}$. Measurement noise is deterministic: $\sigma[\sin(0.73k)+\cos(1.17k)]$. Mean NEES is the measured average of $(x-\hat x)^2/P$; it is not a probabilistic coverage test for this sinusoidal sequence.

## Baseline workflow

Predict which stress plant tracks worst. At $a=b=1$, $A=0.980199$, $B=0.019801$, $K\approx0.980199$ and $N\approx1.980199$. A zero initial estimate therefore commands about 1.98 before saturation. Run uncertainty 0.2 and noise 0.1. Inspect the executed state traces, then the requirement table: calibration rank 2, worst settled RMS below 0.35, command at most 3, and mean NEES at most 6. These are explicit teaching thresholds, not a universal control specification.

Only samples 300–599 enter settled tracking and consistency metrics. The baseline worst tracking RMS is about 0.176 and maximum mean NEES about 0.746. The requirement table explains why a visually plausible response may still be invalid.

## Two one-variable sweeps

1. Keep noise 0.1; raise uncertainty from 0.2 to 0.8. Predict a tracking failure from weaker gain and slower dynamics. The worst RMS grows to about 0.786 even though identification and command limits still pass.
2. Restore uncertainty 0.2; raise noise from 0.1 to 0.5. Explain why filter tuning changes both estimation and closed-loop behavior. Compare actual tracking RMS and mean NEES rather than asserting every error must increase monotonically.

## Intentionally broken case

The broken calibration holds $x=u=1$, making both regressors identical. Rank drops to one. An explicit stale fallback supplies runnable coefficients, while the estimator underreports covariance. The controls retain your uncertainty and noise values. A low tracking error cannot rescue the failed identification and consistency requirements.

## Recovery

Disable broken mode with the same controls. Persistent excitation, the fitted model and declared covariance tuning return. Repeating the baseline must reproduce its signature exactly.

## Limiting cases and invariants

At zero uncertainty all three true plants coincide. With zero internal measurement-noise input, state estimates approach the measured state; the numerical variance floor keeps the equations finite. At equilibrium excitation, two coefficients cannot be separately identified. Every applied command remains within ±3 in both modes.

## Independent evidence

The reference solves the two-column normal equations explicitly and uses an information-form scalar update. It imports no production experiment and generates the expected baseline, two sweeps, fault and recovery vectors. Additional checks reconstruct the state recurrence and rank from the retained histories.

## Common mistakes

Do not use estimator covariance as observed error, confuse a successful fallback with successful identification, or call three sampled plants a robust-stability proof.

## Teach-back

- Why is the constant calibration rank one? Both columns are the same, so many coefficient pairs explain the observations.
- Why can a noise sweep alter tracking? Feedback uses the estimate, so estimation error enters the command.
- Does NEES below 6 certify uncertainty coverage? No; the deterministic noise and three stress points do not establish a sampling distribution.

## Cumulative assessment

Before claiming this model valid, derive $A,B,K,N$ with units; identify a failed requirement in the 0.8 uncertainty run from an actual quantity; and recover the broken calibration without changing the stress controls. Full credit requires all three explanations and the repeated recovery values, not just a pass count.
