# See Stability Margin in Time and Frequency

**Guiding question:** What inputs, observable effects, and failure modes matter when you see Stability Margin in Time and Frequency?

Connect gain/phase margins to ringing and instability in the same transparent loop. This native lab preserves the source experiment while making the levers, diagnostics, and recovery available directly in the learning platform.

## Predict before running

Higher gain moves crossover upward where actuator lag removes phase margin. Write down the mechanism you expect—not only the trace direction—before moving a control.

## Model and equations

- $$L(s)=K/[s(s+1)(\tau_a s+1)]$$ — The actuator pole adds lag before crossover.
- $$PM=180^\circ+\angle L(j\omega_c)$$ — Phase margin measures distance from positive-feedback alignment.

The GUI evaluates these equations deterministically. Read the metric cards and both plots together: a pleasing response can still conceal poor authority, weak conditioning, stale data, or invalid assumptions.

## Two one-variable sweeps

1. Sweep `loop_gain` through [0.5, 1.0, 4.0]. Hold every other control fixed and explain the causal chain from equation to trace to metric.
2. Sweep `actuator_lag_s` through [0.0, 0.2, 0.5]. Compare the changed mechanism plot with your first prediction.

Do not tune both levers at once until you can identify which term each lever changes.

## Intentionally broken case

The broken case keeps K=4 while exposing a 0.5 s actuator lag omitted by the optimistic design. Predict the signature before enabling **broken mode**.

## Recovery

Disable the broken case or lower loop gain until both margins are positive. A recovery is complete only when you can name the failed assumption and point to the metric or trace that confirms it.

## Common mistakes

- Treating a simulation trace as proof about hardware or production behavior.
- Changing multiple controls at once and losing causal attribution.
- Reading only the final value while ignoring transient effort, conditioning, delay, or saturation.
- Hiding a failed assumption by retuning instead of reproducing and explaining it.

## Teach-back

In two minutes: state the governing equation, explain what each live lever changes, identify the broken assumption, and justify the recovery with one visible metric and one plot feature.

---

## Source lesson (retained and polished into this GUI)

# P07 lesson: See Stability Margin in Time and Frequency

## Guiding question

What inputs, observable effects, and failure modes matter when you see Stability Margin in Time and Frequency?

## Compounds on

P06 — Tune a PID by Observing Each Term showed that a controller can look well
tuned for one model. P07 steps outside the closed-loop trace and measures how much
gain and phase change that design can tolerate.

## Mental model

The plant has one integrating state and one damped state. Normalized output `y`
has unit `output`; `v` has `output/s`; the plant damping rate is `b = 1/s`; and
controller gain `K` has `1/s^2`. The command `c = K(r-y)`, in `output/s^2`,
passes through an actuator with time constant `tau` before becoming plant
acceleration `a`:

- `y' = v`;
- `v' = a-b*v`;
- `tau*a' = c-a` when `tau > 0`.

Opening the loop gives `L(s) = K/[s(s+b)(tau*s+1)]`. At frequency `omega`, its
magnitude and phase are evaluated factor by factor:

- `|L(j*omega)| = K/[omega*sqrt(b^2+omega^2)*sqrt(1+(tau*omega)^2)]`;
- `angle L = -90 deg - atan(omega/b) - atan(tau*omega)`.

Gain crossover `omega_gc` is where magnitude equals one. Phase margin is the
distance from the phase there to `-180 deg`. For positive actuator lag, phase
crossover is independently `sqrt(b/tau)`, critical gain is
`b*(1+b*tau)/tau` in `1/s^2`, and gain margin is the dimensionless ratio
`Kcritical/K`.

That reserve is not a cosmetic frequency-domain number. Increasing `K` moves
crossover upward, where both dynamic factors contribute more lag. Increasing
`tau` makes the actuator fall behind at a lower frequency. Either change reduces
margin, so the time response rings more. Crossing zero phase margin makes a mode
grow instead of decay.

## Tutor sequence

Ask one prediction: will added actuator lag increase or decrease the reserve?
Show only the baseline time response. Then reveal magnitude and phase at the
marked gain crossover. Move `K` once and connect crossover, margin, and overshoot.
Reset, move `tau` once, and identify the same mechanism without changing gain.
Finally compare the instantaneous-actuator prediction with the broken lagged
loop. Ask for the violated assumption before showing gain reduction as recovery.

## Direct misconception corrections

- “A positive gain margin means no oscillation.” No. It means the loop can
  tolerate some gain increase before instability; a stable loop can still ring.
- “Gain crossover is a closed-loop natural frequency.” No. It is the open-loop
  unity-magnitude frequency, used here to measure phase reserve.
- “Actuator lag only makes the response slower.” No. It also subtracts phase near
  crossover and can turn decaying oscillation into growth.
- “The Bode view is a separate model.” No. Its factors come from the same state
  equations used by the time calculation.
- “These plots prove hardware margins.” No. They are retained static and
  deterministic software artifacts; runtime and physical claims need separate
  evidence.

## Teach-back

In two sentences, name the two levers, connect one frequency-margin change to one
time-domain symptom, then identify the broken actuator assumption and recovery.

## Source walkthrough

# Walkthrough: See Stability Margin in Time and Frequency

Run one experiment section per step so every changed view has one cause.

1. Read the guiding question: What inputs, observable effects, and failure modes matter when you see Stability Margin in Time and Frequency?
2. Recall P06's tuned closed-loop traces. Predict whether an actuator that falls
   behind the command adds or removes phase reserve.
3. Run only the baseline time section. Observe a bounded step with decaying
   oscillation and read overshoot plus settling time.
4. Run the baseline frequency section. At `omega_gc`, read magnitude `0 dB` and
   the angular distance from phase to `-180 deg`; connect that phase margin to
   the decay seen in time.
5. Run sweep 1. Only loop gain `K` (`1/s^2`) changes. Observe crossover move upward, phase
   margin shrink, and overshoot rise while actuator lag remains `0.2 s`.
6. Reset `K = 1`, then run sweep 2. Only actuator lag `tau` changes. Observe the
   extra phase lag and time ringing while gain remains invariant.
7. Open `interactive.m`. Move gain once, press **Reset baseline**, then move lag
   once. Name a changed observable and the held input each time.
8. Run the broken case. The instantaneous-actuator model looks bounded at `K =
   4 1/s^2`, but the actual `0.5 s` lag makes gain margin less than one and phase margin
   negative. Name the omitted-lag assumption from the growing response.
9. Recover by reducing gain below `Kcritical = 3` while retaining the `0.5 s`
   lag. Confirm that margins become positive and oscillations decay.
10. Run `run_checks`, answer `checks.md` one question at a time, and give the
    two-sentence teach-back.

## Source checks

# P07 checks: See Stability Margin in Time and Frequency

Run `run_checks.m` before answering these questions. The executable checks cover
deterministic repeatability, state and frequency identities, exact margin
relations, both isolated sweeps, zero-gain and zero-lag limits, malformed inputs,
time resolution, the 20,001-sample resource bound, instability, and recovery.

Answer one interpretation question at a time:

1. At gain crossover, why is magnitude `0 dB`, and what angular distance is the
   phase margin measuring?
2. When only `K` increases, why does crossover move higher, phase margin shrink,
   and time-domain overshoot rise?
3. When only `tau` increases, which frequency term adds lag, and what time-domain
   symptom reveals the lost reserve?
4. Why can a stable response still oscillate even though gain margin exceeds one
   and phase margin is positive?
5. In the broken case, what assumption was violated when `K = 4 1/s^2` was selected
   using `tau = 0`, and why does reducing gain below `b*(1+b*tau)/tau` recover the
   actual lagged loop?

Teach-back: in two sentences, answer “What inputs, observable effects, and failure
modes matter when you see Stability Margin in Time and Frequency?” Name both
levers, one time/frequency connection, the omitted-lag symptom, and its recovery.
