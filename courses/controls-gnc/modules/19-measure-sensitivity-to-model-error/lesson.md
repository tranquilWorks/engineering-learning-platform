# Measure Sensitivity to Model Error

**Guiding question:** What inputs, observable effects, and failure modes matter when you measure Sensitivity to Model Error?

Measure how actuator gain and drag mismatch change closed-loop speed tracking. This native lab preserves the source experiment while making the levers, diagnostics, and recovery available directly in the learning platform.

## Predict before running

Lower actuator gain and higher drag should both increase tracking error, but through different mechanisms. Write down the mechanism you expect—not only the trace direction—before moving a control.

## Model and equations

- $$\dot v=-b_av+g_au$$ — The actual plant carries uncertain drag and control effectiveness.
- $$S_p=(y_a-y_n)/y_n$$ — Sensitivity compares actual response with nominal prediction.

The GUI evaluates these equations deterministically. Read the metric cards and both plots together: a pleasing response can still conceal poor authority, weak conditioning, stale data, or invalid assumptions.

## Two one-variable sweeps

1. Sweep `actuator_gain_ratio` through [0.5, 1.0, 1.5]. Hold every other control fixed and explain the causal chain from equation to trace to metric.
2. Sweep `drag_ratio` through [0.5, 1.0, 2.0]. Compare the changed mechanism plot with your first prediction.

Do not tune both levers at once until you can identify which term each lever changes.

## Intentionally broken case

The broken case reverses actuator sign, outside the modeled positive-gain uncertainty family. Predict the signature before enabling **broken mode**.

## Recovery

Disable the broken case and validate control polarity before tuning robustness. A recovery is complete only when you can name the failed assumption and point to the metric or trace that confirms it.

## Common mistakes

- Treating a simulation trace as proof about hardware or production behavior.
- Changing multiple controls at once and losing causal attribution.
- Reading only the final value while ignoring transient effort, conditioning, delay, or saturation.
- Hiding a failed assumption by retuning instead of reproducing and explaining it.

## Teach-back

In two minutes: state the governing equation, explain what each live lever changes, identify the broken assumption, and justify the recovery with one visible metric and one plot feature.

---

## Source lesson (retained and polished into this GUI)

# P19 lesson: Measure Sensitivity to Model Error

## Guiding question

What inputs, observable effects, and failure modes matter when you measure Sensitivity to Model Error?

## Compounds on P18

P18 separated a known feedforward command from feedback correction. That lesson assumed the model
used by the reference and controller matched the plant. P19 keeps the same two command roles and
changes one physical coefficient at a time, so feedback's ability to reduce model error is measured
rather than assumed.

## Mental model

Imagine cruise control with a map that says how much throttle balances drag. The map is the nominal
model. A weak actuator or extra drag means the predicted speed and measured speed separate; feedback
responds to that gap, but a nonzero correction does not rewrite the map.

For the first-order speed plant and fixed controller,

```text
u[k]   = (a0/b0)*r[k] + K*(r[k]-v[k])
v[k+1] = exp(-a*dt)*v[k] + (b/a)*(1-exp(-a*dt))*u[k]
v_ss   = b*(a0/b0+K)*r / (a+b*K)
```

The speed and command are sampled every `dt=0.02 s`, and each command is held until the next sample.
The state update is the exact held-input solution of `dv/dt=-a*v+b*u`; the reported pole is for this
sampled-data feedback loop.

`a` is drag in `1/s`, `b` is dimensionless actuator effectiveness, speed is `m/s`, and command is
`m/s^2`. Differentiating the visible steady-state quotient gives output change per fractional model
change. At the matched baseline, the signs are opposite: more actuator gain raises steady speed,
while more drag lowers it.

## What the two levers reveal

- **Actuator gain ratio:** a weak actuator produces less speed per command. The actual controller asks
  for more correction, but the fixed proportional loop retains a steady prediction gap.
- **Drag ratio:** extra loss lowers speed for the same command. Because drag appears in the equilibrium
  denominator, its local sensitivity is negative.

At a ratio of one, predicted and actual histories are identical. The prediction gap is exactly zero,
yet the local sensitivities are not: zero present error does not mean zero vulnerability to the next
small parameter error.

## Deliberately broken assumption

Ordinary model uncertainty preserves the command direction. Reversed actuator polarity does not.
Positive tracking error then produces a command that drives actual speed farther from reference, the
discrete closed-loop pole magnitude exceeds one, and steady-response sensitivity is not meaningful
for the diverging trajectory. Restoring
the sign in a fresh call recovers the exact baseline because the model has no hidden state.

## Misconceptions to correct directly

- Sensitivity is not merely a large error; it is output change normalized by an input change.
- A zero baseline prediction gap does not prove the model is insensitive.
- Feedback attenuates these bounded errors but does not identify which physical parameter is wrong.
- Actuator error and drag error can have different signs even when their absolute sizes match.
- Reversed polarity is a violated structure, not a larger point on the positive-gain sweep.
- This lesson measures one fixed controller; choosing a robust design belongs to P20.
- Independent reference simulation is not MATLAB-runtime, UI, bench, HIL, or field evidence.

Ask one observation question at a time. Request the teach-back only after executable checks pass.

## Source walkthrough

# P19 walkthrough: Measure Sensitivity to Model Error

## Learner sequence

1. Read the guiding question and the speed-plant equation before running code.
2. Predict only whether a `20%` weaker actuator puts measured steady speed above or below prediction.
3. Visualize the baseline reference, nominal prediction, and actual speed. Confirm that matched
   parameters give an exactly zero prediction-gap history.
4. View nominal and actual command histories. At the matched limit they coincide; model error makes
   feedback request a different correction.
5. Sweep only actuator gain ratio. Observe the direction of steady-speed change, then read the local
   sensitivity as output speed per unit fractional gain error.
6. Explain the changed view from actuator effectiveness in both numerator and denominator of the
   equilibrium quotient, not from MATLAB syntax.
7. Reset actuator gain to one and sweep only drag ratio. Observe the opposite sensitivity sign while
   reference, controller, sign, duration, and time grid remain fixed.
8. Explain why extra drag lowers speed from the same quotient and why the prediction-gap RMSE is zero
   only at the matched ratio.
9. Reverse actuator polarity. Identify the pole magnitude above one and growing correction as a
   structural failure, then restore correct polarity and recover the exact baseline.
10. Run `run_module_checks("P19")`, answer one interpretation prompt at a time, and give the required
    two-sentence teach-back.

No MATLAB-runtime, rendered-UI, or physical evidence is claimed by this source walkthrough.

## Source checks

# P19 checks: Measure Sensitivity to Model Error

Run `run_module_checks("P19")`, then answer one prompt at a time:

1. Why can the matched baseline have zero prediction gap but nonzero local sensitivities?
2. Why does a weaker actuator produce a negative steady prediction error while actuator-gain
   sensitivity is positive?
3. Why does extra drag have the opposite sensitivity sign from extra actuator effectiveness?
4. Which view distinguishes an ordinary positive actuator-gain error from reversed actuator polarity?
5. Why does feedback attenuate these parameter errors without proving which coefficient is wrong?

## Teach-back

In exactly two sentences, name the two uncertain inputs and the observable used to measure their
sensitivities. Then use the matched limit and reversed-sign pole to distinguish bounded model error
from a broken structural assumption.

The source and independent oracle provide static and simulated evidence only. No MATLAB-runtime,
rendered-UI, numerical-fidelity, bench, HIL, field, or production validation is claimed.
