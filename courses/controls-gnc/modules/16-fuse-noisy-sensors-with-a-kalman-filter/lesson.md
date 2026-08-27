# Fuse Noisy Sensors with a Kalman Filter

**Guiding question:** What inputs, observable effects, and failure modes matter when you fuse Noisy Sensors with a Kalman Filter?

Fuse noisy position samples with a deterministic constant-velocity Kalman filter. This native lab preserves the source experiment while making the levers, diagnostics, and recovery available directly in the learning platform.

## Predict before running

Assuming noisier measurements should smooth the estimate but slow its response to real motion changes. Write down the mechanism you expect—not only the trace direction—before moving a control.

## Model and equations

- $$K_k=P^-C^T(CP^-C^T+R)^{-1}$$ — Kalman gain balances predicted and measured uncertainty.
- $$P^+=(I-KC)P^-$$ — The covariance update records information gained from the sensor.

The GUI evaluates these equations deterministically. Read the metric cards and both plots together: a pleasing response can still conceal poor authority, weak conditioning, stale data, or invalid assumptions.

## Two one-variable sweeps

1. Sweep `assumed_sensor_noise_m` through [0.15, 0.35, 0.8]. Hold every other control fixed and explain the causal chain from equation to trace to metric.
2. Sweep `assumed_process_noise_m_s2` through [0.02, 0.08, 0.3]. Compare the changed mechanism plot with your first prediction.

Do not tune both levers at once until you can identify which term each lever changes.

## Intentionally broken case

The broken case injects one unvalidated 4 m position outlier. Predict the signature before enabling **broken mode**.

## Recovery

Disable the broken case; in production, gate innovations before applying the update. A recovery is complete only when you can name the failed assumption and point to the metric or trace that confirms it.

## Common mistakes

- Treating a simulation trace as proof about hardware or production behavior.
- Changing multiple controls at once and losing causal attribution.
- Reading only the final value while ignoring transient effort, conditioning, delay, or saturation.
- Hiding a failed assumption by retuning instead of reproducing and explaining it.

## Teach-back

In two minutes: state the governing equation, explain what each live lever changes, identify the broken assumption, and justify the recovery with one visible metric and one plot feature.

---

## Source lesson (retained and polished into this GUI)

# P16 lesson: Fuse Noisy Sensors with a Kalman Filter

## Guiding question

What inputs, observable effects, and failure modes matter when you fuse Noisy Sensors with a Kalman Filter?

## Compounds on

P15 — Build a State Observer. P15 introduced model prediction, known input, innovation, correction,
and the danger of trusting a biased measurement. P16 keeps that observer loop and replaces its fixed
gain with covariance-weighted fusion of two noisy position sensors. P15's observability remains
necessary: position changes over time are what reveal rate.

## Mental model

Carry two things through time: the best state estimate and an uncertainty ellipse represented by
`P`. The motion model advances both. Uncertain acceleration adds `Q`, enlarging the predicted
uncertainty. Two position sensors report values and noise variances in `R`. Their innovation
covariance is `S=C*Pminus*C'+R`, and the correction gain is `K=Pminus*C'/S`.

A smaller sensor variance gives that sensor more leverage, but only relative to the other sensor and
the model. A larger process variance says that unmodeled acceleration may have changed the state, so
the filter reports more rate uncertainty and uses later measurements more strongly. Covariance is a
declared model of uncertainty; it is not proof that a sensor obeys the declaration.

Normalized innovation squared (NIS) compares a two-sensor innovation with `S`:

```text
NIS = innovation' * S^(-1) * innovation
```

Because both measurements are positions, each innovation has metres, `S` has square metres, and NIS
is dimensionless. Position and rate covariance metrics stay separate because their units differ.

## What the two levers mean

- **Assumed sensor A noise standard deviation** changes only one diagonal entry of `R`. Raising it
  lowers sensor A's position gain, shifts relative trust toward sensor B and prediction, and makes a
  fixed raw innovation less surprising.
- **Assumed process acceleration standard deviation** changes only `Q`. Raising it increases
  predicted uncertainty, the rate correction gain from position, and reported rate uncertainty.

Every sweep resets seed, actual pseudo-noise, command, outlier, other covariance assumption,
duration, and sample interval. The seeded physical trajectory is therefore identical across each
controlled comparison.

## Deliberately broken assumption

The broken case adds one `+4 m` sample to sensor A at `12 s`. `R` still describes ordinary zero-mean
noise with `0.35 m` standard deviation, so the outlier is much larger than the innovation covariance
predicts. NIS spikes and the gain still moves the estimate: an ordinary Kalman update does not
automatically reject an outlier. A fresh zero-outlier call exactly recovers the baseline because the
model has no global random or persisted state.

## Misconceptions to correct directly

- A Kalman gain is not a magic constant; it follows the current predicted covariance and `R`.
- A smaller `R` does not make the physical sensor quieter. It tells the filter to trust that sensor.
- A larger `Q` does not add noise to the already seeded truth in a sweep. It changes what the filter
  assumes about model error.
- Two sensors do not guarantee correctness when their uncertainty or mean is modeled incorrectly.
- NIS is a consistency diagnostic, not automatic outlier rejection and not proof of Gaussian data.
- Seeded pseudo-noise and independent reference simulation are not MATLAB-runtime or sensor evidence.

Ask one observation question at a time, then request the teach-back only after executable checks.

## Source walkthrough

# P16 walkthrough: Fuse Noisy Sensors with a Kalman Filter

## Read and predict

Read the guiding question and covariance equations in `README.md`. Make one prediction: with both
sensors measuring position, which one should receive more position gain when sensor A reports
`0.35 m` noise and sensor B reports `0.8 m`?

## Baseline

Run the baseline sections of `experiment.m`.

1. Both raw sensor traces scatter around the same true position.
2. The fused position is smoother than either raw sequence because prediction and both measurements
   share the correction.
3. Rate is reconstructed from position history and the P15 motion model; no rate sensor is hidden.
4. Posterior rate standard deviation and NIS make the filter's uncertainty claim visible.
5. The fixed seed makes truth, measurements, estimates, gains, and metrics repeat exactly.

Mechanism: P15 supplied prediction and innovation feedback. P16 propagates `P`, adds `Q`, combines
prediction and sensor variance in `S`, and calculates a new covariance-weighted gain.

## Lever 1 — reported sensor A noise

Keep assumed process acceleration noise at `0.08 m/s^2`, sensor B at `0.8 m`, outlier at zero, seed
at `1601`, duration at `20 s`, and interval at `0.05 s`. Sweep sensor A from `0.1–0.9 m`.

- Sensor A's steady position gain falls as its reported noise grows.
- Sensor B's relative contribution grows because its own noise declaration is unchanged.
- Under-reporting the actual `0.35 m` noise makes mean NIS too large for the claimed covariance.

Read the `R → S → K` mechanism only after comparing the gain and NIS view.

## Lever 2 — assumed process acceleration noise

Reset sensor A to `0.35 m`, then sweep process noise from `0.01–0.5 m/s^2`.

- Larger `Q` makes the prediction admit more unmodeled acceleration.
- Rate gain from position innovation increases.
- Reported posterior rate standard deviation increases.
- Truth and both raw sensor sequences remain identical because the seed and actual process noise do
  not change.

## Broken case and recovery

Inject one `+4 m` outlier into sensor A at `12 s`.

1. The true state, ordinary pseudo-noise, commands, gains, and covariance remain unchanged.
2. Sensor A's innovation leaves the range predicted by `S`.
3. NIS spikes and the fused estimate receives an unsupported correction that may help or hurt by chance.
4. Restore zero outlier; a fresh call returns the exact baseline.

## Check and teach back

Run `run_module_checks("P16")`. Answer the interpretation questions in `checks.md`, then give the
two-sentence teach-back. Learner completion remains separate from batch implementation.

## Source checks

# P16 checks: Fuse Noisy Sensors with a Kalman Filter

Run `run_module_checks("P16")` before answering the interpretation prompts.

## Observe

1. Why does raising sensor A's reported noise lower its gain even though the raw seeded sensor data
   do not change?
2. Why does raising process uncertainty increase rate correction from position innovations?
3. What units belong to `Q`, `R`, the two innovations, the gain entries, and NIS?
4. Why can two individually noisy position sensors reconstruct rate when neither measures rate?
5. In the broken case, why does NIS spike, and why does that diagnostic not reject the outlier by itself?

## Numerical completion contract

The executable checks independently verify:

- the exact P15 zero-order-hold plant matrices and covariance definitions;
- the local seeded noise sequence, deterministic repeat, truth, predict, gain, update, Joseph
  covariance, and NIS recurrences at every sample;
- covariance symmetry, positive diagonals and determinant, separated position/rate units, and bounded
  baseline metrics;
- isolated sensor-noise and process-noise sweeps with their monotone gain/covariance consequences;
- a single-sample outlier symptom, unchanged truth and gain, exact fresh-call recovery, alternate-seed
  isolation, and the largest accepted finite grid;
- nonscalar, nonreal, nonfinite, nonpositive, noninteger, under-range, over-range, misaligned, and
  resource-exhausting inputs before trajectory allocation.

## Teach back

In two sentences, answer: “What inputs, observable effects, and failure modes matter when you fuse
Noisy Sensors with a Kalman Filter?” Name prediction, two measurements, `Q`, and `R`; describe one
visible trust tradeoff; and explain the outlier/NIS failure without relying on MATLAB syntax.
