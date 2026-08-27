# Expose Delay and Sampling Limits

**Guiding question:** What inputs, observable effects, and failure modes matter when you expose Delay and Sampling Limits?

Reveal held commands, computation latency, and sampled-data pole movement. This native lab preserves the source experiment while making the levers, diagnostics, and recovery available directly in the learning platform.

## Predict before running

Sampling and delay together should increase oscillation even when the continuous design is fast. Write down the mechanism you expect—not only the trace direction—before moving a control.

## Model and equations

- $$u_k=K_p(1-y_k)$$ — The command is computed only at sample instants.
- $$u(t)=u_{k-1}\;\text{then}\;u_k$$ — Computation delay retains the previous command within each interval.

The GUI evaluates these equations deterministically. Read the metric cards and both plots together: a pleasing response can still conceal poor authority, weak conditioning, stale data, or invalid assumptions.

## Two one-variable sweeps

1. Sweep `sample_period_s` through [0.02, 0.1, 0.2]. Hold every other control fixed and explain the causal chain from equation to trace to metric.
2. Sweep `delay_fraction` through [0.0, 0.5, 0.9]. Compare the changed mechanism plot with your first prediction.

Do not tune both levers at once until you can identify which term each lever changes.

## Intentionally broken case

The broken case uses a 0.2 s period with 90 percent computation delay. Predict the signature before enabling **broken mode**.

## Recovery

Disable the broken case and schedule computation early in the sample interval. A recovery is complete only when you can name the failed assumption and point to the metric or trace that confirms it.

## Common mistakes

- Treating a simulation trace as proof about hardware or production behavior.
- Changing multiple controls at once and losing causal attribution.
- Reading only the final value while ignoring transient effort, conditioning, delay, or saturation.
- Hiding a failed assumption by retuning instead of reproducing and explaining it.

## Teach-back

In two minutes: state the governing equation, explain what each live lever changes, identify the broken assumption, and justify the recovery with one visible metric and one plot feature.

---

## Source lesson (retained and polished into this GUI)

# P10 lesson: Expose Delay and Sampling Limits

## Guiding question

What inputs, observable effects, and failure modes matter when you expose Delay and Sampling Limits?

## Compounds on

P05 established proportional feedback and its nonzero steady-state error. P07 tied
visible motion to stability reserve. P09 separated sample instants from continuous
plant motion and exposed a held digital command. P10 preserves those ideas and adds
the time required to turn a sampled measurement into an applied command.

## Mental model

The plant is `y' = -y + u`. At each sample the controller computes
`u[k] = 8*(1-y[k])`. Computation takes `Td` seconds, so the actuator cannot apply that
new command immediately. It retains `u[k-1]` during `Td`, then applies `u[k]` for the
remaining `Ts-Td`. The plant never waits for the processor.

The exact interval equation has three contributions:

`y[k+1] = exp(-Ts)*y[k] + wOld*u[k-1] + wNew*u[k]`.

`wOld = exp(-(Ts-Td))*(1-exp(-Td))` measures the stale-command portion, and
`wNew = 1-exp(-(Ts-Td))` measures the new-command portion. Their sum with
`exp(-Ts)` is one. At `Td=0`, `wOld=0`; the new command owns the entire interval.
At `Td=Ts`, `wNew=0`; the whole interval uses the previous command.

The sample-period sweep sets `Td=0` and moves only `Ts`, making the held-update limit
visible. The delay sweep fixes `Ts=0.1 s` and moves only `Td`, making stale-command
time visible. Pole magnitude reports whether deviations shrink (`<1`), persist at
the boundary (`=1`), or grow (`>1`).

The deliberately broken case uses `Ts=0.2 s` and `Td=0.18 s`. Its sample rate still
exceeds twice the continuous closed-loop bandwidth in hertz, but its pole magnitude
exceeds one. That is not a contradiction: Nyquist is a signal-reconstruction bound,
not a complete feedback-stability guarantee. Delay consumes phase and lets old
commands act after the measured error has changed. Reducing only `Td` to `0.02 s`
moves the poles inside the unit circle again.

## Tutor sequence

Ask one prediction before the baseline: which trace exposes latency first? Show the
output comparison, then reveal computed versus applied commands. Move `Ts` once with
zero delay and connect the changed target gap to hold duration. Reset to `Ts=0.1 s`,
move only `Td`, and connect overshoot to stale-command weight. Finally reveal the
broken pole magnitude and Nyquist ratio before the growing output, then recover by
reducing delay without changing sample period.

## Direct misconception corrections

- “The plant pauses while the controller computes.” No. It keeps evolving under
  the previous actuator command.
- “Sample period and computation delay are the same thing.” No. `Ts` spaces
  measurements; `Td` decides how long the prior command persists after each sample.
- “Sampling above Nyquist guarantees stable feedback.” No. Nyquist addresses signal
  reconstruction; feedback also depends on dynamics, gain, hold, and latency.
- “A delayed plot can be repaired by interpolation.” No. Smoothing does not change
  the stale command physically applied during `Td`.
- “The plot proves runtime or hardware behavior.” No. This is retained model content;
  MATLAB runtime, UI, numerical fidelity, bench, HIL, and field validation require
  separate evidence.

## Teach-back

In two sentences, distinguish `Ts` from `Td`, name one observable caused by each,
and explain why the broken case can fail despite its Nyquist ratio plus how it recovers.

## Source walkthrough

# P10 walkthrough: Expose Delay and Sampling Limits

Run one experiment section per step so every changed view has one cause.

1. Read the guiding question: What inputs, observable effects, and failure modes matter when you expose Delay and Sampling Limits?
2. Recall P05's proportional feedback and P09's sampled command. Predict whether
   computation delay first appears in applied command or plant output.
3. Run only the baseline output section for `Ts=0.05 s`, `Td=0.01 s`. Compare the
   timed loop with the immediate continuous proportional target.
4. Reveal computed versus applied commands. During `Td`, identify the previous
   command that remains active while the plant continues moving.
5. Run sweep 1. Keep `Td=0`, gain, plant, and reference fixed. Increase only `Ts`
   and observe continuous-target gap, overshoot, and pole magnitude.
6. Reset `Ts=0.1 s`, then run sweep 2. Increase only `Td` and connect the rising
   stale-command weight and delay phase to oscillation and overshoot.
7. Open `interactive.m`. Move sample period once, press **Reset baseline**, then
   move delay fraction once. Name what changed and what stayed fixed.
8. Inspect the broken `Ts=0.2 s`, `Td=0.18 s` pole magnitude and Nyquist ratio before
   revealing the growing time trace. State why Nyquist alone is insufficient.
9. Recover by reducing only `Td` to `0.02 s`. Run `run_checks.m`, then answer
   `checks.md` one question at a time.
10. Teach back in two sentences: distinguish sample spacing from compute latency,
    connect each lever to an observable, and name the failed assumption plus recovery.

## Source checks

# P10 checks: Expose Delay and Sampling Limits

Run `run_checks.m`, then answer one interpretation question at a time.

1. In the exact interval equation, what physical motion do `wOld` and `wNew` represent?
2. Why does the plant keep moving during computation delay?
3. In the sample-period sweep, what remains fixed and why does target gap increase?
4. In the delay sweep, what remains fixed and why does stale-command weight increase?
5. What should happen to the model as `Ts` and `Td` both approach zero?
6. What do the `Td=0` and `Td=Ts` limiting cases mean physically?
7. Why can Nyquist ratio above one coexist with an unstable feedback loop?
8. Which pole metric exposes the broken case before the time plot is trusted?
9. Why is reducing `Td` a real recovery while smoothing or interpolating samples is not?
10. Which retained numerical checks are independent of presentation plots?

## Teach-back

In two sentences, answer the guiding question by distinguishing `Ts` and `Td`, naming
one visible timing effect, and explaining the combined-limit failure plus recovery.

Do not mark personal completion until the executable checks pass and the learner
gives that teach-back. Static repository checks are not MATLAB-runtime, UI,
numerical-fidelity, bench, HIL, field, or production evidence.
