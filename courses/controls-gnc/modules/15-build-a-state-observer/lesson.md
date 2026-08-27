# Build a State Observer

**Guiding question:** What inputs, observable effects, and failure modes matter when you build a State Observer?

Watch a Luenberger observer reconstruct position and rate from position measurements. This native lab preserves the source experiment while making the levers, diagnostics, and recovery available directly in the learning platform.

## Predict before running

Faster poles should reduce settling time but increase sensitivity to measurement contamination. Write down the mechanism you expect—not only the trace direction—before moving a control.

## Model and equations

- $$\dot{\hat x}=A\hat x+Bu+L(y-C\hat x)$$ — The innovation corrects both estimated states.
- $$\dot e=(A-LC)e$$ — Observer poles set nominal error convergence.

The GUI evaluates these equations deterministically. Read the metric cards and both plots together: a pleasing response can still conceal poor authority, weak conditioning, stale data, or invalid assumptions.

## Two one-variable sweeps

1. Sweep `observer_speed_per_s` through [1.0, 2.0, 5.0]. Hold every other control fixed and explain the causal chain from equation to trace to metric.
2. Sweep `sensor_bias_m` through [-0.1, 0.0, 0.1]. Compare the changed mechanism plot with your first prediction.

Do not tune both levers at once until you can identify which term each lever changes.

## Intentionally broken case

The broken case introduces a persistent 0.15 m measurement bias. Predict the signature before enabling **broken mode**.

## Recovery

Disable the broken case and correct the sensor bias before trusting the state estimate. A recovery is complete only when you can name the failed assumption and point to the metric or trace that confirms it.

## Common mistakes

- Treating a simulation trace as proof about hardware or production behavior.
- Changing multiple controls at once and losing causal attribution.
- Reading only the final value while ignoring transient effort, conditioning, delay, or saturation.
- Hiding a failed assumption by retuning instead of reproducing and explaining it.

## Teach-back

In two minutes: state the governing equation, explain what each live lever changes, identify the broken assumption, and justify the recovery with one visible metric and one plot feature.

---

## Source lesson (retained and polished into this GUI)

# P15 lesson: Build a State Observer

## Guiding question

What inputs, observable effects, and failure modes matter when you build a State Observer?

## Compounds on

P14 — Test Observability. P14 showed that position measurement history distinguishes position and
rate for this cart. Full observability is the permission to build an observer, not the observer
itself. P15 adds prediction, innovation, correction gain, and a running initial estimate. P16 will
handle stochastic sensor fusion; this lesson uses only deterministic interference.

## Mental model

Think of two copies of the cart. The physical copy receives a known acceleration command. The
observer copy receives the same command and predicts position and rate. Only physical position is
measured. At each sample, `innovation = measured position - predicted position` tells the observer
how its prediction disagrees with the sensor, and `L*innovation` corrects both state estimates.

For the matched noise-free case, the known input cancels from the estimation error:

```text
error[k+1] = (Ad - L*C) error[k]
```

The lesson requests a repeated error pole `q = exp(-speed*dt)`. Smaller `q` means faster sampled
decay, but the required gain is stronger. Metres and metres per second are normalized by declared
scales of `1 m` and `1 m/s` before their errors are combined into one norm.

## What the two levers mean

- **Observer pole speed** changes the desired decay of initial-estimate error. In the fixed eight-second
  sweep, faster poles leave less final error and require a larger correction gain.
- **Measurement-interference amplitude** changes only a repeatable `2.5 Hz` position disturbance.
  The observer cannot know whether innovation came from true state error or sensor interference, so
  both position and rate estimates acquire ripple.

Each sweep resets the other lever, sensor bias, command, duration, sample interval, true initial
state, and estimated initial state.

## Deliberately broken assumption

The broken case adds a constant `+0.15 m` calibration bias to the position sensor. The measurement
path remains observable and the observer error poles remain stable. Nevertheless, the observer
eventually estimates position about `0.15 m` too high while innovation approaches zero. This is the
recognizable false-confidence symptom: a quiet residual can mean agreement with a biased sensor,
not agreement with truth. Restoring zero bias in a fresh call recovers the deterministic baseline.

## Misconceptions to correct directly

- Observability does not choose `L`, guarantee a useful transient, or reject sensor bias.
- A faster observer is not free: stronger correction also passes more measurement disturbance.
- The observer does not measure rate secretly; rate changes predicted position, then position
  innovation corrects the rate estimate.
- A known input belongs in both plant and observer prediction. It cancels from matched estimation
  error, but it still drives the physical and estimated trajectories.
- Deterministic sinusoidal interference is not stochastic noise validation and is not a Kalman filter.
- A small innovation is evidence of sensor-model agreement, not independent proof of state accuracy.

Ask one observation question at a time, then request the teach-back only after executable checks.

## Source walkthrough

# P15 walkthrough: Build a State Observer

## Read and predict

Read the guiding question and the prediction/correction equation in `README.md`. Make one prediction:
can position innovation correct the wrong rate estimate even though rate is never measured directly?

## Baseline

Run the baseline sections of `experiment.m`.

1. The true cart starts at `0.8 m` and `-0.3 m/s`; the observer starts at `-0.4 m` and `0.4 m/s`.
2. A known `0.4 m/s^2` acceleration begins at `0.5 s` and enters both predictions.
3. Position innovation initially is large because the estimated position is wrong.
4. The position estimate converges toward measured position, and the unmeasured rate estimate also
   converges because rate error changes later position predictions.
5. With no interference or bias, the normalized error follows the visible `Ad-L*C` recurrence.

Mechanism: P14 supplied an observable measurement path. P15 feeds its disagreement back through a
designed gain so the estimation error has stable sampled dynamics.

## Lever 1 — observer pole speed

Keep interference and bias at zero, command at `0.4 m/s^2`, duration at `8 s`, and interval at
`0.02 s`. Sweep `1–4 1/s`.

- The requested repeated pole moves farther inside the unit circle as speed increases.
- Fixed-horizon final error decreases for these controlled runs.
- The observer-gain norm increases, showing that faster correction demands more innovation feedback.

Read the mechanism only after comparing the pole, final error, and gain views.

## Lever 2 — deterministic measurement interference

Reset observer speed to `2 1/s`, then sweep interference amplitude from `0–0.05 m`.

- True state and command remain identical in every run.
- Last-second position- and rate-error ripple grow with sensor disturbance.
- Rate ripple appears even though only position is disturbed because `L` corrects both estimates.

## Broken case and recovery

Add a constant `+0.15 m` position-sensor bias.

1. The observer remains numerically stable.
2. Innovation becomes nearly zero.
3. Estimated position remains about `0.15 m` too high, so true-minus-estimated position approaches
   `-0.15 m`.
4. Restore zero bias; the original baseline returns in a fresh isolated run.

## Check and teach back

Run `run_module_checks("P15")`. Answer the interpretation questions in `checks.md`, then give the
two-sentence teach-back. Learner completion remains separate from batch implementation.

## Source checks

# P15 checks: Build a State Observer

Run `run_module_checks("P15")` before answering the interpretation prompts.

## Observe

1. How does position innovation correct rate when the observer never receives a rate measurement?
2. Why does increasing pole speed reduce fixed-horizon baseline error while increasing correction gain?
3. Why does deterministic position-sensor interference create both position- and rate-estimate ripple?
4. In the broken case, why can innovation approach zero while the position estimate remains wrong?
5. Which observer inputs must match or be trustworthy: model, known command, measurement calibration,
   initial estimate, or correction gain?

## Numerical completion contract

The executable checks independently verify:

- exact zero-order-hold plant matrices and hand-derived repeated observer-pole gain;
- error-transition trace, determinant, Jordan identity, and every sampled recurrence;
- matched known-input cancellation and the exact-initial-estimate limiting case;
- isolated pole-speed and deterministic measurement-interference sweeps;
- linear interference response, biased-sensor false confidence, fresh-call recovery, and zero-command limit;
- malformed input, grid alignment, and resource bounds before history allocation.

## Teach back

In two sentences, answer: “What inputs, observable effects, and failure modes matter when you build a
State Observer?” Name the prediction inputs and innovation, one visible speed-versus-interference
tradeoff, and why observability plus quiet innovation cannot protect against sensor bias.
