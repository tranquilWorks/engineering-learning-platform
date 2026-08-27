# Test Observability

**Guiding question:** What inputs, observable effects, and failure modes matter when you test Observability?

Use measurement history and observability conditioning to expose hidden state. This native lab preserves the source experiment while making the levers, diagnostics, and recovery available directly in the learning platform.

## Predict before running

A longer position record should improve velocity inference; a rate-only sensor hides initial position. Write down the mechanism you expect—not only the trace direction—before moving a control.

## Model and equations

- $$\mathcal O=[C;CA]$$ — Full column rank lets outputs distinguish every state direction.
- $$y(t)=g(x_0+v_0t)$$ — Position history reveals constant rate through slope.

The GUI evaluates these equations deterministically. Read the metric cards and both plots together: a pleasing response can still conceal poor authority, weak conditioning, stale data, or invalid assumptions.

## Two one-variable sweeps

1. Sweep `sensor_gain` through [0.25, 1.0, 2.0]. Hold every other control fixed and explain the causal chain from equation to trace to metric.
2. Sweep `observation_window_s` through [0.25, 2.0, 5.0]. Compare the changed mechanism plot with your first prediction.

Do not tune both levers at once until you can identify which term each lever changes.

## Intentionally broken case

The broken case measures rate only, so initial position never appears in the output. Predict the signature before enabling **broken mode**.

## Recovery

Disable the broken case to measure position and restore full observability. A recovery is complete only when you can name the failed assumption and point to the metric or trace that confirms it.

## Common mistakes

- Treating a simulation trace as proof about hardware or production behavior.
- Changing multiple controls at once and losing causal attribution.
- Reading only the final value while ignoring transient effort, conditioning, delay, or saturation.
- Hiding a failed assumption by retuning instead of reproducing and explaining it.

## Teach-back

In two minutes: state the governing equation, explain what each live lever changes, identify the broken assumption, and justify the recovery with one visible metric and one plot feature.

---

## Source lesson (retained and polished into this GUI)

# P14 lesson: Test Observability

## Guiding question

What inputs, observable effects, and failure modes matter when you test Observability?

## Compounds on

P13 — Test Controllability. P13 followed command effects from an input into state directions. P14
uses the dual viewpoint: follow initial-state effects through the dynamics and out to a measurement.
The same state-space discipline applies, but reachability and visibility answer different questions.

## Mental model

Imagine a coasting cart with position and rate coordinates. Rate decays with drag, while position
accumulates rate. A position sensor directly reveals position; successive position samples reveal
the initial rate because different rates bend the position history differently. The rows of
`[C; C*A]` ask:

- what state combination does the sensor see immediately?
- what additional state combination reaches the sensor after the dynamics act?

Independent columns mean both normalized initial-state directions are observable. The finite-window
matrix in the experiment repeats the same idea at every sample and reconstructs the noise-free
initial state using explicit two-by-two arithmetic.

## What the two levers mean

- **Position-sensor sensitivity** scales every output effect. A weak but nonzero sensor can retain
  rank while shrinking candidate separation and increasing worst-case inverse noise gain.
- **Observation-window duration** controls how much position history is available. More time lets
  the initial rate accumulate into position and strengthens its weakest visible direction.

Neither lever changes damping, initial states, sample interval, sensor selection, state scales, or
the other lever during its sweep.

## Deliberately broken assumption

The broken case replaces position measurement with rate-only measurement. The sensor remains active,
but a constant initial-position offset never changes rate. Two trajectories one metre apart therefore
produce identical output histories. Observability rank falls from two to one and the model reports
the initial state as non-unique rather than inventing a zero position. Restoring position measurement
recovers output separation, full rank, and exact noise-free reconstruction.

## Misconceptions to correct directly

- Full rank does not mean good conditioning, adequate sensitivity, or immunity to noise and bias.
- A small singular value is coordinate dependent; this lesson declares fixed state scales before
  comparing it.
- Observability concerns whether outputs reveal state. Whether an input can move state was the
  controllability question in P13.
- `rank(obsv(A,C))` is not the lesson. The governing rows, output histories, ambiguous states, and
  failed measurement assumption must remain visible.

Ask one observation question at a time, then request the teach-back only after executable checks.

## Source walkthrough

# P14 walkthrough: Test Observability

## Read and predict

Read the guiding question and the state/measurement equations in `README.md`. Make one prediction:
can a position sensor reveal initial rate even though rate is not measured directly?

## Baseline

Run the baseline sections of `experiment.m`.

1. The true state starts at `0.8 m` and `0.6 m/s`; the comparison state has the same rate but a
   position offset of `1 m`.
2. Both rates decay identically, and the two positions remain one metre apart.
3. Position measurement separates the candidates at every sample.
4. The initial-rate observation column begins at zero and grows as rate accumulates into position.
5. The traditional observability rows and finite-window Gramian both have rank two, and the
   noise-free initial-state reconstruction error is numerical roundoff.

Mechanism: every observation row is one sample's view of the initial state. Dynamics carry initial
rate into later position, so the stacked rows span two state directions.

## Lever 1 — position-sensor sensitivity

Keep position measurement selected, window at `2 s`, interval at `0.05 s`, and both candidate states
fixed.

- Smaller sensitivity shrinks every observation row and the candidate-output separation.
- Rank stays two for the nonzero sweep values.
- The weakest singular value grows with sensitivity, while worst-case inverse noise gain falls.

Read the explanation only after comparing separation and inverse gain.

## Lever 2 — observation-window duration

Reset sensitivity to `1 sensor unit/m` and sweep `0.1–4 s`.

- A short history contains little accumulated evidence about initial rate.
- A longer history adds rows and strengthens the weakest observation direction.
- Damping, initial states, sample interval, and sensor stay fixed; only the window changes.

## Broken case and recovery

Select rate-only measurement while retaining the same gain and candidate states.

1. The sensor produces a healthy decaying rate signal.
2. The two different initial positions produce exactly the same output history.
3. Rank is one and the full initial state is non-unique.
4. Restore position measurement; output separation returns, rank returns to two, and the initial
   state is reconstructed.

## Check and teach back

Run `run_module_checks("P14")`. Answer the interpretation questions in `checks.md`, then give the
two-sentence teach-back. Learner completion remains separate from batch implementation.

## Source checks

# P14 checks: Test Observability

Run `run_module_checks("P14")` before answering the interpretation prompts.

## Observe

1. Which initial state is visible in the first position sample, and which becomes visible only after
   the dynamics create later samples?
2. Why does halving sensor sensitivity increase inverse noise gain even though observability rank
   remains two?
3. Why does a longer observation window reveal initial rate more strongly without changing the
   sensor or dynamics?
4. In the broken case, why can the rate sensor produce a healthy signal while initial position
   remains ambiguous?

## Numerical completion contract

The executable checks independently verify:

- exact free-response state transition and traditional observability rows;
- every finite-window observation row and deterministic state recurrence;
- noise-free initial-state reconstruction from explicit two-by-two arithmetic;
- isolated sensor-sensitivity and observation-window sweeps;
- zero-sensor, rate-only, short-window, and zero-initial-rate limiting cases;
- malformed input, grid alignment, and resource bounds;
- isolation and recovery when position measurement is restored.

## Teach back

In two sentences, answer: “What inputs, observable effects, and failure modes matter when you test
Observability?” Name the measurement path, one visible output effect, and why full rank alone does
not guarantee a reliable estimate from an imperfect sensor.
