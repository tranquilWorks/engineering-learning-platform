# Close a Loop with Proportional Control

**Guiding question:** What inputs, observable effects, and failure modes matter when you close a Loop with Proportional Control?

Make proportional feedback speed/error tradeoffs and the sign of feedback visible. This native lab preserves the source experiment while making the levers, diagnostics, and recovery available directly in the learning platform.

## Predict before running

Gain should speed the response and reduce—but not eliminate—the step error. Write down the mechanism you expect—not only the trace direction—before moving a control.

## Model and equations

- $$\tau\dot y=-y+G K_p(r-y)$$ — Negative feedback increases the closed-loop rate.
- $$y_{ss}=GK_p r/(1+GK_p)$$ — Proportional control retains a finite step error.

The GUI evaluates these equations deterministically. Read the metric cards and both plots together: a pleasing response can still conceal poor authority, weak conditioning, stale data, or invalid assumptions.

## Two one-variable sweeps

1. Sweep `proportional_gain` through [0.5, 2.0, 6.0]. Hold every other control fixed and explain the causal chain from equation to trace to metric.
2. Sweep `plant_time_constant_s` through [0.5, 1.0, 3.0]. Compare the changed mechanism plot with your first prediction.

Do not tune both levers at once until you can identify which term each lever changes.

## Intentionally broken case

The broken toggle reverses the measurement sign, producing positive feedback. Predict the signature before enabling **broken mode**.

## Recovery

Disable the broken case to restore subtraction at the summing junction. A recovery is complete only when you can name the failed assumption and point to the metric or trace that confirms it.

## Common mistakes

- Treating a simulation trace as proof about hardware or production behavior.
- Changing multiple controls at once and losing causal attribution.
- Reading only the final value while ignoring transient effort, conditioning, delay, or saturation.
- Hiding a failed assumption by retuning instead of reproducing and explaining it.

## Teach-back

In two minutes: state the governing equation, explain what each live lever changes, identify the broken assumption, and justify the recovery with one visible metric and one plot feature.

---

## Source lesson (retained and polished into this GUI)

# Lesson: Close a Loop with Proportional Control

## Guiding question

What inputs, observable effects, and failure modes matter when you close a Loop with Proportional Control?

## Compounds on P04

P04 showed that a calculation is useful only while its governing model and assumptions
match the question. P05 uses a transparent first-order plant rather than the pendulum
so one new mechanism can be isolated: the measured output changes the next command.
The pole-to-motion connection from earlier modules remains visible in the closed-loop
time scale.

## Mental model

Let `r` be a position reference in metres, `y` the measured position, `u` the
command, `G` the plant's static gain in metres per command unit, and `tau` its time
constant in seconds:

```text
plant:       tau*y' = -y + G*u
error:       e = r - y
controller:  u = Kp*e
closed loop: tau*y' = G*Kp*r - (1 + G*Kp)*y.
```

For negative feedback, the closed-loop pole is
`p = -(1 + G*Kp)/tau`. Increasing `Kp` moves that pole farther left and shortens
the time constant. At steady state, however,
`y_ss = G*Kp*r/(1 + G*Kp)` and `e_ss = r/(1 + G*Kp)`. The controller needs that
remaining error because `u_ss = Kp*e_ss` is what holds the plant away from zero.

## Observe before manipulating

Run only the baseline sections of `experiment.m`. Make one prediction: will the
output reach the `1 m` reference exactly with `Kp = 2`? Observe position first,
then inspect tracking error and command. Connect the residual error to the nonzero
command rather than calling it a numerical defect.

## Move one lever at a time

First sweep `Kp` while `tau = 1 s`. Larger gain makes the response faster and
reduces residual error, but it also increases the initial command. Reset `Kp = 2`,
then sweep only `tau`. A slower plant stretches the transient while leaving the
negative-feedback steady-state ratio unchanged.

## Deliberately broken assumption and recovery

Negative feedback assumes the measured output is subtracted. Reverse that sign and
the loop obeys `tau*y' = G*Kp*r + (G*Kp - 1)*y`. With `G*Kp > 1`, the pole is
positive: a positive output increases the command, which increases the output again.
The recognizable symptom is exponential growth away from the reference. Recover by
restoring the subtracting sign before changing gain. Saturation is intentionally not
added here; actuator constraints belong to a later module.

## Common misconceptions

- Closing a loop does not guarantee zero error. Proportional control alone needs
  steady error to produce a steady command for this plant.
- Larger `Kp` is not free: the initial and peak command grow even in this ideal model.
- Plant time constant changes transient speed, not the negative-feedback steady-state
  ratio for fixed `G` and `Kp`.
- Positive feedback is not simply “too much gain.” Its sign reverses correction into
  reinforcement; with `G*Kp > 1`, the closed-loop pole crosses into growth.
- A deterministic simulated curve is not hardware evidence, and this ideal model
  contains no sensor noise, delay, or actuator limit.

## Completion standard

Pass `run_checks.m`, answer the interpretation questions in `checks.md`, and give a
two-sentence teach-back: mechanism first, visible tradeoff and sign failure second.
MATLAB syntax is not an explanation.

## Source walkthrough

# Walkthrough: Close a Loop with Proportional Control

Run one experiment section per step so every changed view has one cause.

1. Read the guiding question: What inputs, observable effects, and failure modes matter when you close a Loop with Proportional Control?
2. Recall P04's model-assumption boundary, then predict whether `Kp = 2` makes the output reach a `1 m` reference exactly.
3. Run only the baseline output section. Observe the quick rise and the gap that remains below the reference.
4. Run the error-and-effort section. Connect `u = Kp*e` to the fact that nonzero holding command requires nonzero error.
5. Run sweep 1. Only proportional gain changes; compare response time, final error, and initial command while plant time constant stays at `1 s`.
6. Reset `Kp = 2`, then run sweep 2. Only plant time constant changes; observe stretched transients and an unchanged steady-state ratio.
7. Open `interactive.m`. Move proportional gain once, press **Reset baseline**, then move plant time constant once. State the changed observable and invariant after each move.
8. Run the reversed-sign broken case. Name the violated subtracting-feedback assumption from the growing response, then restore negative feedback and observe recovery.
9. Run `run_checks.m`, then answer `checks.md` one question at a time.
10. Teach back in two sentences: state how measured error creates command, then name the gain tradeoff, reversed-sign symptom, and recovery.

## Source checks

# P05 checks: Close a Loop with Proportional Control

Run `run_checks.m` first. It checks deterministic repeatability, the governing
equation, exact interval propagation, the closed-loop pole and time constant,
steady-state balance, both independent levers, zero-gain and zero-state limits,
sign symmetry, the reversed-sign broken/recovered pair, malformed inputs, endpoint
behavior, response bounds, and the maximum calculation grid.

Then answer one interpretation question at a time:

1. Which measured quantity is subtracted from the reference, and how does that subtraction change the next command?
2. Why does larger `Kp` reduce steady error and response time while increasing initial command?
3. Why can proportional control hold a nonzero output only while a nonzero error remains in this plant?
4. When only `tau` increases, which observable changes and which steady-state ratio remains fixed?
5. In the reversed-sign case, which assumption is violated, what visible symptom reveals the positive pole, and what recovery must happen first?

## Teach-back

In two sentences, answer: “What inputs, observable effects, and failure modes matter
when you close a Loop with Proportional Control?” Sentence one must connect
reference, measured output, error, gain, and command. Sentence two must identify the
speed/error/effort tradeoff, the reversed-sign symptom, and recovery.

Passing static repository tests does not claim that these MATLAB checks, figures, or
controls executed. Record a separate MATLAB-runtime result if they are run.
