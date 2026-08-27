# Reject a Disturbance with Feedback

**Guiding question:** What inputs, observable effects, and failure modes matter when you reject a Disturbance with Feedback?

Separate true disturbance rejection from the cost of measurement bias. This native lab preserves the source experiment while making the levers, diagnostics, and recovery available directly in the learning platform.

## Predict before running

More gain should reject a slow plant disturbance but amplify control response to bias. Write down the mechanism you expect—not only the trace direction—before moving a control.

## Model and equations

- $$\dot y=-y-K(y+b)+d$$ — Feedback rejects plant disturbance but reacts to sensor bias as if it were real output.
- $$|S_d(j\omega)|=1/\sqrt{(1+K)^2+\omega^2}$$ — Rejection is strongest below loop bandwidth.

The GUI evaluates these equations deterministically. Read the metric cards and both plots together: a pleasing response can still conceal poor authority, weak conditioning, stale data, or invalid assumptions.

## Two one-variable sweeps

1. Sweep `feedback_gain` through [1.0, 4.0, 9.0]. Hold every other control fixed and explain the causal chain from equation to trace to metric.
2. Sweep `disturbance_frequency_rad_s` through [0.0, 2.0, 8.0]. Compare the changed mechanism plot with your first prediction.

Do not tune both levers at once until you can identify which term each lever changes.

## Intentionally broken case

The broken case injects a 0.5-unit sensor bias with no physical disturbance. Predict the signature before enabling **broken mode**.

## Recovery

Disable the broken case and validate/calibrate the sensor bias. A recovery is complete only when you can name the failed assumption and point to the metric or trace that confirms it.

## Common mistakes

- Treating a simulation trace as proof about hardware or production behavior.
- Changing multiple controls at once and losing causal attribution.
- Reading only the final value while ignoring transient effort, conditioning, delay, or saturation.
- Hiding a failed assumption by retuning instead of reproducing and explaining it.

## Teach-back

In two minutes: state the governing equation, explain what each live lever changes, identify the broken assumption, and justify the recovery with one visible metric and one plot feature.

---

## Source lesson (retained and polished into this GUI)

# P08 lesson: Reject a Disturbance with Feedback

## Guiding question

What inputs, observable effects, and failure modes matter when you reject a Disturbance with Feedback?

## Compounds on

P06 made proportional offset, integral memory, and controller effort visible.
P07 connected loop gain to stability reserve. P08 keeps a stable transparent
loop and asks what unwanted input enters, what signal feedback observes, and what
tradeoff is visible when gain changes.

## Mental model

The normalized plant is `tau*y' = -y + u + d`, with `tau = 1 s`, zero reference,
and `u = -K*y_m`. Output `y`, plant-input disturbance `d`, measurement bias, and
control effort `u` share normalized `output` units. Gain is dimensionless.

For an honest sensor, `y_m = y`. A constant load then settles at
`y_ss = d/(1+K)` while the controller holds `u_ss = -K*d/(1+K)`. More gain reduces
the residual and shortens the loop time constant to `tau/(1+K)`, but controller
effort approaches the full load. Proportional feedback does not make a constant
residual exactly zero; P06's integral term is the mechanism for that job.

For a sinusoidal load, the exact disturbance-to-output magnitude is
`1/sqrt((1+K)^2 + (tau*omega)^2)`. The plant itself filters fast inputs. The
relative with-feedback/no-feedback ratio approaches `1/(1+K)` at low frequency
but approaches one at high frequency. A small fast output does not mean feedback
did all the work.

The broken case uses `y_m = y + b`. With no physical load, equilibrium becomes
`y = -K*b/(1+K)` and `y_m = b/(1+K)`. High gain can make the measured error look
small by moving the true plant almost one bias unit in the opposite direction.
That is a disturbance-location failure, not inadequate gain.

## Tutor sequence

Ask one prediction: as gain rises against a constant plant-input load, which gets
smaller—true output, controller effort, or both? Show the baseline output first,
then reveal effort. Move gain once and explain the equilibrium balance. Reset and
move disturbance frequency once; separate absolute plant filtering from feedback's
additional rejection. Finally inject sensor bias, ask which signal looks healthy,
and recover by validating and correcting the sensor.

## Direct misconception corrections

- “Feedback removes any disturbance.” No. Rejection depends on where the input
  enters and what the controller measures.
- “A small high-frequency response proves strong feedback.” No. The uncontrolled
  first-order plant already filters fast inputs; compare the relative ratio.
- “More proportional gain removes a constant load completely.” No. Finite gain
  leaves `d/(1+K)` so it can command the holding effort.
- “A near-zero sensor reading proves true output is near zero.” No. Bias can make
  the loop move the plant while hiding that motion in the measurement.
- “The plot proves hardware behavior.” No. It is a deterministic software model;
  MATLAB runtime, UI, numerical fidelity, bench, HIL, and field behavior require
  separate evidence.

## Teach-back

In two sentences, name the plant-input disturbance and measured signal, explain
one gain or frequency tradeoff, then identify the sensor-bias symptom and recovery.

## Source walkthrough

# Walkthrough: Reject a Disturbance with Feedback

Run one experiment section per step so every changed view has one cause.

1. Read the guiding question: What inputs, observable effects, and failure modes matter when you reject a Disturbance with Feedback?
2. Recall P06's proportional offset and P07's loop reserve. Predict what larger
   feedback gain does to output deviation and control effort under a constant load.
3. Run only the baseline time section. Observe the unit disturbance, `0.2 output`
   residual, and `-0.8 output` controller effort for `K = 4`.
4. Reveal the frequency view. Compare absolute `|Y/D|` with and without feedback,
   then inspect the relative ratio so plant filtering is not credited to feedback.
5. Run sweep 1. Only feedback gain changes. Verify that residual output and loop
   time constant fall while steady controller effort approaches the load amplitude.
6. Reset `K = 4`, then run sweep 2. Only disturbance frequency changes. Observe
   smaller absolute fast-load output but a relative feedback benefit closer to one.
7. Open `interactive.m`. Move gain once, press **Reset baseline**, then move
   frequency once. Name the changed metric and the input that stayed fixed.
8. Run the broken sensor-bias case. Compare true output with measured output and
   name the violated honest-sensor assumption before viewing recovery.
9. Recover by validating and removing bias, not by increasing gain. Run
   `run_checks.m`, then answer `checks.md` one question at a time.
10. Teach back in two sentences: say where the load and bias enter, explain one
    rejection tradeoff, and identify the bias symptom plus recovery.

## Source checks

# P08 checks: Reject a Disturbance with Feedback

Run `run_checks.m` first. It checks determinism, governing equations, the exact
step and sinusoidal time histories, frequency limits, both isolated sweeps, the
sensor-bias failure and recovery, malformed inputs, numerical convergence, event
handling, and resource bounds. Then answer one interpretation question at a time.

1. A unit constant plant-input load produces `0.2 output` with `K = 4`. What
   equilibrium balance makes the remaining `-0.8 output` controller effort visible?
2. Why does increasing proportional gain reduce, but not eliminate, constant-load
   deviation? Which P06 mechanism could remove the residual?
3. A fast disturbance produces a smaller output but a with-feedback/no-feedback
   ratio closer to one. Which attenuation belongs to plant dynamics, and which
   belongs to feedback?
4. In the broken case, why can measured output approach zero while true output
   approaches minus the sensor bias as gain rises?
5. Why is sensor validation and correction the recovery, rather than another gain
   increase? How does P07 constrain any legitimate increase in loop action?

## Teach-back

In two sentences, name where a plant-input load and sensor bias enter, explain one
gain or frequency tradeoff, and identify the biased-sensor symptom and recovery.

Do not mark P08 complete until the executable checks pass and the learner gives
that teach-back. Static repository checks are not MATLAB-runtime, UI, numerical-
fidelity, bench, HIL, field, or production evidence.
