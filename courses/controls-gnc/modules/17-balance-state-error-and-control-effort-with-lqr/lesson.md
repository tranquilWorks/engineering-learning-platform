# Balance State Error and Control Effort with LQR

**Guiding question:** What inputs, observable effects, and failure modes matter when you balance State Error and Control Effort with LQR?

Trade position regulation against command effort with a discrete LQR design. This native lab preserves the source experiment while making the levers, diagnostics, and recovery available directly in the learning platform.

## Predict before running

More position weight should regulate faster with a larger peak command. Write down the mechanism you expect—not only the trace direction—before moving a control.

## Model and equations

- $$J=\sum(x^TQx+u^TRu)$$ — The cost declares the state/effort tradeoff.
- $$u_k=-Kx_k$$ — Riccati feedback minimizes the declared quadratic cost.

The GUI evaluates these equations deterministically. Read the metric cards and both plots together: a pleasing response can still conceal poor authority, weak conditioning, stale data, or invalid assumptions.

## Two one-variable sweeps

1. Sweep `position_weight` through [1.0, 4.0, 16.0]. Hold every other control fixed and explain the causal chain from equation to trace to metric.
2. Sweep `control_weight` through [0.1, 1.0, 10.0]. Compare the changed mechanism plot with your first prediction.

Do not tune both levers at once until you can identify which term each lever changes.

## Intentionally broken case

The broken case sets actuator effectiveness to zero, so a valid design model cannot move the plant. Predict the signature before enabling **broken mode**.

## Recovery

Disable the broken case and verify actuator authority before applying the gain. A recovery is complete only when you can name the failed assumption and point to the metric or trace that confirms it.

## Common mistakes

- Treating a simulation trace as proof about hardware or production behavior.
- Changing multiple controls at once and losing causal attribution.
- Reading only the final value while ignoring transient effort, conditioning, delay, or saturation.
- Hiding a failed assumption by retuning instead of reproducing and explaining it.

## Teach-back

In two minutes: state the governing equation, explain what each live lever changes, identify the broken assumption, and justify the recovery with one visible metric and one plot feature.

---

## Source lesson (retained and polished into this GUI)

# P17 lesson: Balance State Error and Control Effort with LQR

## Guiding question

What inputs, observable effects, and failure modes matter when you balance State Error and Control Effort with LQR?

## Compounds on

P16 — Fuse Noisy Sensors with a Kalman Filter. P16 made full-state feedback feasible by producing a
position/rate estimate and covariance. P17 uses the exact state in its deterministic model to isolate
the control-design tradeoff. In practice LQR acts on P16's estimate, not inaccessible truth. P13's
controllability lesson also returns: an actuator must influence every state the design must regulate.

## Mental model

Imagine assigning prices before driving the cart back to the origin. `Q` charges for state error and
`R` charges for the command. A high position price makes lingering displacement costly. A high input
price makes a hard acceleration costly. LQR finds one feedback gain that minimizes their declared
sum for the nominal linear plant; it does not minimize each term separately.

The Riccati matrix `P` is a map from the current state to future cost. At convergence, one additional
Bellman step does not change it:

```text
P = Q + A'*P*A - A'*P*B*(R + B'*P*B)^(-1)*B'*P*A
```

The model computes that scalar division and matrix recurrence directly. The closed-loop poles of
`A-B*K` must lie inside the unit circle for nominal sampled regulation.

## What the two levers mean

- **Position-error weight `q_p`** changes only the position entry of `Q`. Raising it increases the
  position feedback gain, reduces position integral squared error, and increases the squared-command
  effort integral.
  At exactly zero, a stationary position offset costs nothing; position gain is zero and the offset
  persists. That is an interpretable limiting case, not a numerical crash.
- **Control-effort weight `r`** changes only scalar `R`. Raising it makes input more expensive, lowers
  feedback gains and peak acceleration, reduces the effort integral, and generally lengthens settling.

Every sweep resets actuator effectiveness, initial state, duration, interval, and the non-swept
weight. The comparisons therefore isolate the declared lever.

## Deliberately broken assumption

The controller is designed with the nominal input column `B`, which represents full acceleration
authority. The broken case sets actual actuator effectiveness to zero after design. Commanded
acceleration remains nonzero, applied acceleration is exactly zero, and the position error cannot
change. LQR optimality is conditional on the model and cannot restore a disconnected actuator or
lost controllability. A fresh effectiveness-one call exactly recovers the baseline.

## Misconceptions to correct directly

- LQR is not automatically “aggressive”; behavior follows the relative state and input prices.
- An effort price discourages large input but does not enforce a hard actuator limit.
- Larger `Q` does not change the physical initial error. It changes how expensive that error is.
- Larger `R` does not weaken the actuator. It asks the design to use the actuator more sparingly.
- A small weighted cost is meaningful only with declared state/input scales and weights.
- Stable nominal poles do not prove performance when actuator authority or the plant model is wrong.
- The guarantee is for an unconstrained nominal linear model, available state, quadratic cost, and
  correct actuator authority; it is not a general robustness guarantee.
- Independent reference simulation is not MATLAB-runtime, UI, hardware, or field evidence.

Ask one observation question at a time and request the teach-back only after executable checks.

## Source walkthrough

# P17 walkthrough: Balance State Error and Control Effort with LQR

## Read and predict

Read the guiding question and cost in `README.md`. Make one prediction: with control price fixed,
does raising the position-error weight increase or decrease the first acceleration command?

## Baseline

Run the baseline sections of `experiment.m`.

1. The cart starts with `1 m` position error and zero rate error.
2. Negative acceleration first creates rate toward the origin; position and rate then decay.
3. Commanded and applied acceleration coincide because the baseline actuator has full authority.
4. The feedback gain, pole radius, settling time, position integral squared error, effort integral,
   and peak acceleration make both sides of the tradeoff visible.
5. Repeating the same call returns exactly the same matrices, trajectory, and metrics.

Mechanism: P16 supplied the state estimate. P17 uses `Q`, `R`, the nominal `A,B` model, and future
cost `P` to form `u=-K*x`.

## Lever 1 — position-error weight

Keep `r=1`, actuator effectiveness `1`, initial position `1 m`, duration `12 s`, and interval
`0.02 s`. Sweep `q_p` through `[0, 0.25, 1, 4, 16]`.

- Position gain and squared-command effort integral rise as displacement becomes more expensive.
- Position integral squared error falls.
- At `q_p=0`, position gain and commanded acceleration are exactly zero for this stationary offset;
  the error persists because the objective does not charge it.

Read the `Q → P → K` mechanism only after observing the changed view.

## Lever 2 — control-effort weight

Reset `q_p=4`, then sweep `r` through `[0.1, 0.25, 1, 4, 10]`.

- Higher `R+B'*P*B` produces smaller feedback gains and peak command.
- The effort integral falls while settling takes longer.
- The plant, state, and state prices are identical across the sweep.

## Broken case and recovery

Select `Disconnected actuator (broken)`.

1. The gain is unchanged because it was designed for the nominal `B`.
2. The controller repeatedly commands acceleration from the persistent state error.
3. Applied acceleration is zero, so position remains at `1 m` and settling is not achieved.
4. Restore full authority; a fresh call exactly matches the baseline.

## Check and teach back

Run `run_module_checks("P17")`. Answer the interpretation questions in `checks.md`, then give the
two-sentence teach-back. Learner completion remains separate from batch implementation.

## Source checks

# P17 checks: Balance State Error and Control Effort with LQR

Run `run_module_checks("P17")` before answering the interpretation prompts.

## Observe

1. Why does raising `q_p` increase initial acceleration even though the initial state does not change?
2. Why does raising `r` reduce the squared-command effort integral but lengthen settling?
3. What normalization makes the terms in `J` compatible, and what physical units remain on the plots?
4. How does the Riccati matrix connect present state to future cost?
5. Why do stable nominal poles fail to move the cart when actual actuator effectiveness is zero?

## Numerical completion contract

The executable checks independently verify:

- the exact P16 zero-order-hold damped-cart matrices, cost definitions, Riccati recurrence, Bellman
  residual, feedback optimum, closed-loop characteristic equation, and every state transition;
- exact deterministic repeat, stable nominal poles, bounded baseline error/effort metrics, and
  separated physical units;
- isolated position-weight and effort-weight sweeps with their expected monotone tradeoffs;
- the zero-position-weight limiting case, disconnected-actuator symptom, unchanged design,
  exact fresh-call recovery, sign symmetry, and the largest accepted finite grid;
- nonscalar, nonreal, nonfinite, negative, zero, under-range, over-range, misaligned, under-resolved,
  and resource-exhausting inputs before state-history allocation.

## Teach back

In two sentences, answer: “What inputs, observable effects, and failure modes matter when you balance
State Error and Control Effort with LQR?” Name the state estimate, `Q`, `R`, and the actuator model;
describe one visible error/effort tradeoff; and explain the disconnected-actuator failure without
relying on MATLAB syntax.
