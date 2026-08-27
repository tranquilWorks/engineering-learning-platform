# Tune a PID by Observing Each Term

**Guiding question:** What inputs, observable effects, and failure modes matter when you tune a PID by Observing Each Term?

Observe proportional, integral, and derivative actions separately on a loaded carriage. This native lab preserves the source experiment while making the levers, diagnostics, and recovery available directly in the learning platform.

## Predict before running

Integral action should remove load error; derivative action should suppress overshoot. Write down the mechanism you expect—not only the trace direction—before moving a control.

## Model and equations

- $$u=K_pe+K_i\int e\,dt-K_d\dot{x}$$ — Each term reacts to a different feature of error.
- $$m\ddot{x}=u+F_{load}-b\dot{x}$$ — The controller must accelerate the mass and reject load.

The GUI evaluates these equations deterministically. Read the metric cards and both plots together: a pleasing response can still conceal poor authority, weak conditioning, stale data, or invalid assumptions.

## Two one-variable sweeps

1. Sweep `integral_gain` through [0.0, 1.0, 3.0]. Hold every other control fixed and explain the causal chain from equation to trace to metric.
2. Sweep `derivative_gain` through [0.0, 3.0, 7.0]. Compare the changed mechanism plot with your first prediction.

Do not tune both levers at once until you can identify which term each lever changes.

## Intentionally broken case

The broken case applies derivative action with the wrong sign, injecting velocity instead of damping it. Predict the signature before enabling **broken mode**.

## Recovery

Disable the broken case to restore derivative damping. A recovery is complete only when you can name the failed assumption and point to the metric or trace that confirms it.

## Common mistakes

- Treating a simulation trace as proof about hardware or production behavior.
- Changing multiple controls at once and losing causal attribution.
- Reading only the final value while ignoring transient effort, conditioning, delay, or saturation.
- Hiding a failed assumption by retuning instead of reproducing and explaining it.

## Teach-back

In two minutes: state the governing equation, explain what each live lever changes, identify the broken assumption, and justify the recovery with one visible metric and one plot feature.

---

## Source lesson (retained and polished into this GUI)

# P06 lesson: Tune a PID by Observing Each Term

## Guiding question

What inputs, observable effects, and failure modes matter when you tune a PID by Observing Each Term?

## Compounds on

P05 — Close a Loop with Proportional Control made `P = Kp*e` and finite
proportional offset visible. P06 keeps the measured-error loop, adds an error
memory and velocity damping, and uses a constant load so each term has a distinct
observable job.

## Mental model

The carriage obeys `m*x'' = u + Fload - b*x'` with `m = 1 kg`, `b = 0.5
N*s/m`, `r = 1 m`, and `Fload = -1 N`. The controller force is
`u = Kp*e + Ki*q - Kd*v`, where `e = r-x` and `q' = e`.

- Proportional action sees present error. It acts immediately, but on its own it
  must keep `0.25 m` of error so `Kp*e = 1 N` can balance the load.
- Integral action sees accumulated error. It can hold `+1 N` with nearly zero
  present error, but aggressive memory produces overshoot.
- Derivative action sees measured velocity. It vanishes at rest and trades force
  for damping during the transient.

The derivative is taken on measurement, not on the commanded step. For a constant
reference, `e' = -v`, so `D = -Kd*v`; this avoids presenting an ideal reference
step as an impulsive derivative force.

When `Ki = 0`, the carriage position can settle while the displayed error
accumulator keeps growing because it is disconnected from force. The module calls
that output loop stable but does not call the full integrated state asymptotically
stable.

## Tutor sequence

Ask one prediction: which term remains nonzero after error and velocity approach
zero? Show only the baseline position, then reveal the four force traces. Move
`Ki` once and explain offset versus stored-error overshoot. Reset, move `Kd` once,
and explain overshoot versus derivative effort. Finally reverse the derivative
sign and ask the learner to name the violated damping assumption from the growing
oscillation before showing recovery.

## Direct misconception corrections

- “Derivative removes steady error.” No. At rest `v = 0`, so D is zero; I supplies
  the steady load force.
- “Integral makes every response faster.” No. More integral action removes offset,
  but excess stored correction can overshoot and take longer to unwind.
- “Any oscillation means gains are merely high.” No. The broken case has a polarity
  error: `+Kd*v` reinforces motion. Restore the sign before tuning magnitudes.
- “The plot proves hardware behavior.” No. It is a deterministic software model;
  MATLAB runtime, UI, numerical fidelity, bench, HIL, and field behavior require
  separate evidence.

## Teach-back

In two sentences, name the input seen by P, I, and D; explain one visible `Ki` or
`Kd` tradeoff; then identify the wrong-sign derivative symptom and recovery.

## Source walkthrough

# Walkthrough: Tune a PID by Observing Each Term

Run one experiment section per step so every changed view has one cause.

1. Read the guiding question: What inputs, observable effects, and failure modes matter when you tune a PID by Observing Each Term?
2. Recall P05's finite proportional offset, then predict which term will hold the
   carriage against `-1 N` after error and velocity approach zero.
3. Run only the baseline position section. Observe a bounded move from `0 m` toward
   the `1 m` reference and read final error, overshoot, settling time, and force.
4. Run the PID-term section. At `t = 0`, identify `P = 4 N`, `I = 0 N`, and `D =
   0 N`; near equilibrium, identify the integral term approaching `+1 N`.
5. Run sweep 1. Only `Ki` changes. Compare the `0.25 m` P+D offset at `Ki = 0`
   with offset removal and the larger overshoot at `Ki = 2 N/(m*s)`.
6. Reset `Ki = 1 N/(m*s)`, then run sweep 2. Only `Kd` changes. Compare position
   overshoot with peak derivative force while every other input stays fixed.
7. Open `interactive.m`. Move integral gain once, press **Reset baseline**, then
   move derivative gain once. State the changed observable and invariant each time.
8. Run the wrong-sign broken case. Name the violated derivative-damping assumption
   from the growing oscillation, then restore the opposing sign and observe recovery.
9. Run `run_checks.m`, then answer `checks.md` one question at a time.
10. Teach back in two sentences: say what P, I, and D observe, name a tuning
    tradeoff, and explain the wrong-sign symptom plus recovery.

## Source checks

# P06 checks: Tune a PID by Observing Each Term

Run `run_checks.m` before answering these questions. The executable checks cover
controller and plant identities, deterministic repeatability, both isolated
sweeps, limiting cases, malformed inputs, the derivative-sign failure and
recovery, time resolution, and the 20,001-sample resource bound.

Answer one interpretation question at a time:

1. At the baseline's first sample, why is the proportional force `4 N` while the
   integral and derivative forces are both zero?
2. With `Ki = 0`, why does the `-1 N` load leave `0.25 m` of error when `Kp = 4
   N/m`, even though the derivative term damps the transient?
3. When only `Ki` increases, which view proves offset removal, and which metric
   reveals that excessive integral action can overshoot?
4. When only `Kd` increases, why does overshoot fall while the peak magnitude of
   the derivative force rises?
5. In the broken case, what named assumption is violated when `D = +Kd*v`, and
   why is restoring `D = -Kd*v` the recovery step before retuning?

Teach-back: in two sentences, answer “What inputs, observable effects, and failure
modes matter when you tune a PID by Observing Each Term?” Name what P, I, and D
respond to, one visible tuning tradeoff, the wrong-sign symptom, and its recovery.
