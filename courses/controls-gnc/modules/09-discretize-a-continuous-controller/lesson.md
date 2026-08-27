# Discretize a Continuous Controller

**Guiding question:** What inputs, observable effects, and failure modes matter when you discretize a Continuous Controller?

Compare a sampled PI implementation with its continuous design target. This native lab preserves the source experiment while making the levers, diagnostics, and recovery available directly in the learning platform.

## Predict before running

A coarser sample period should move the digital response away from the continuous target. Write down the mechanism you expect—not only the trace direction—before moving a control.

## Model and equations

- $$y_{k+1}=e^{-T_s}y_k+(1-e^{-T_s})u_k$$ — The plant uses the exact zero-order-hold transition.
- $$q_{k+1}=q_k+T_s e_k$$ — The integral rule introduces its own discrete dynamics.

The GUI evaluates these equations deterministically. Read the metric cards and both plots together: a pleasing response can still conceal poor authority, weak conditioning, stale data, or invalid assumptions.

## Two one-variable sweeps

1. Sweep `sample_period_s` through [0.02, 0.1, 0.3]. Hold every other control fixed and explain the causal chain from equation to trace to metric.
2. Sweep `integral_gain` through [1.0, 4.0, 7.0]. Compare the changed mechanism plot with your first prediction.

Do not tune both levers at once until you can identify which term each lever changes.

## Intentionally broken case

The broken case combines coarse sampling with the less forgiving forward-error integral update. Predict the signature before enabling **broken mode**.

## Recovery

Disable the broken case and reduce the controller sample period. A recovery is complete only when you can name the failed assumption and point to the metric or trace that confirms it.

## Common mistakes

- Treating a simulation trace as proof about hardware or production behavior.
- Changing multiple controls at once and losing causal attribution.
- Reading only the final value while ignoring transient effort, conditioning, delay, or saturation.
- Hiding a failed assumption by retuning instead of reproducing and explaining it.

## Teach-back

In two minutes: state the governing equation, explain what each live lever changes, identify the broken assumption, and justify the recovery with one visible metric and one plot feature.

---

## Source lesson (retained and polished into this GUI)

# P09 lesson: Discretize a Continuous Controller

## Guiding question

What inputs, observable effects, and failure modes matter when you discretize a Continuous Controller?

## Compounds on

P06 exposed PI memory and separate controller terms. P07 connected loop dynamics
to stability reserve. P08 showed continuous feedback rejecting unwanted inputs.
P09 keeps a stable continuous PI target but makes measurement, computation, and
command timing explicit.

## Mental model

The normalized plant is `y' = -y + u`. A continuous PI controller would read
`e = 1-y` at every instant and apply `u = 2*e + 4*integral(e dt)`. Its closed-loop
characteristic equation is `s^2 + 3*s + 4 = 0`, so the continuous target is stable.

A digital controller reads `e[k]` every `Ts` seconds. Between samples, a zero-order
hold preserves `u[k]`, and the plant moves exactly according to
`y[k+1] = a*y[k] + (1-a)*u[k]`, where `a = exp(-Ts)`. The implementation writes
that operation directly instead of hiding it behind a conversion toolbox.

Forward Euler updates integral memory after using it, so `u[k]` contains error
through sample `k-1`. Backward Euler updates memory with `e[k]` before forming
`u[k]`. At small `Ts`, both approximate the same continuous controller. At finite
`Ts`, their timing and pole locations differ.

The sample-period sweep isolates how fewer updates create a larger tracking gap,
more visible hold action, and less trustworthy continuous approximation. The rule
sweep holds `Ts` and both gains fixed, so any delta comes from which sampled error
enters integral memory.

The broken case uses forward Euler at `Ts = 0.8 s`. Its explicitly calculated
closed-loop spectral radius exceeds one. Oscillations grow even though the original
continuous PI design is stable. The violated assumption is that the sample period
is small enough for the chosen discrete realization. Reducing `Ts` to `0.05 s`
restores pole magnitude below one and convergence.

## Tutor sequence

Ask one prediction before the baseline: which signal first reveals sampling—the
plant output or controller command? Show the output comparison, then reveal the
held command. Move sample period once and connect the change to update spacing.
Reset, change only the Euler rule, and connect the delta to current versus previous
error. Finally show the coarse-sample pole magnitude before revealing its growing
time trace, then recover by reducing `Ts`.

## Direct misconception corrections

- “Discretizing only changes syntax.” No. It changes when error enters memory and
  where the closed-loop poles lie.
- “The physical plant becomes discrete.” No. The controller samples and holds;
  the plant continues moving between samples.
- “A smooth line through samples proves a good approximation.” No. Inspect held
  effort, tracking gap, samples per natural period, and pole magnitude.
- “A stable continuous controller stays stable at any sample period.” No. The
  discrete realization can lose asymptotic convergence at pole magnitude one and
  grow when pole magnitude exceeds one.
- “The plot proves runtime or hardware behavior.” No. It is a retained software
  model; MATLAB runtime, UI, numerical fidelity, bench, HIL, and field validation
  require separate evidence.

## Teach-back

In two sentences, explain what is sampled and what is held, describe how `Ts` or
Euler rule changes one observable, and name the broken assumption, symptom, and
recovery.

## Source walkthrough

# P09 walkthrough: Discretize a Continuous Controller

Run one experiment section per step so every changed view has one cause.

1. Read the guiding question: What inputs, observable effects, and failure modes matter when you discretize a Continuous Controller?
2. Recall P06's integral memory and P08's continuous feedback loop. Predict whether
   sampling first appears as stair steps in plant output or control effort.
3. Run only the baseline output section. Compare the digital output with the stable
   continuous PI target for `Ts = 0.05 s` and backward Euler.
4. Reveal the held-effort section. Observe that command changes only at samples
   while the plant moves continuously between them. Read the baseline metrics.
5. Run sweep 1. Only sample period changes; keep backward Euler and both gains fixed.
   Watch the tracking gap and samples per natural period change.
6. Reset `Ts = 0.05 s`, then run sweep 2. Only the integration rule changes. Explain
   why current-error and previous-error memory updates produce different commands.
7. Open `interactive.m`. Move sample period once, press **Reset baseline**, then
   change the rule once. Name the metric that changed and what stayed fixed.
8. Run the broken `Ts = 0.8 s` forward-Euler case. First inspect pole magnitude,
   then reveal the growing oscillation and name the resolved-sampling assumption.
9. Recover by reducing `Ts` to `0.05 s`. Run `run_checks.m`, then answer
   `checks.md` one question at a time.
10. Teach back in two sentences: say what is sampled and held, explain one lever's
    effect, and identify the failure symptom plus recovery.

## Source checks

# P09 checks: Discretize a Continuous Controller

Run `run_checks.m`, then answer one interpretation question at a time.

1. In `y[k+1] = a*y[k] + (1-a)*u[k]`, what does `a = exp(-Ts)` mean physically?
2. Which signal is sampled, which command is held, and why is plant output not a staircase?
3. In the sample-period sweep, what remains fixed and why does the continuous-target gap grow?
4. In the rule sweep, which error sample enters forward versus backward Euler memory?
5. What limiting behavior should both rules approach as `Ts` tends toward zero?
6. Why can a stable continuous PI target produce an unstable discrete realization?
7. In the broken case, which pole metric exposes failure before the plot is trusted?
8. Why is reducing sample period a valid recovery while drawing a smooth interpolation is not?
9. Which retained checks are independent of the presentation plots?

## Teach-back

In two sentences, answer the guiding question by naming the timing inputs, one
observable discretization effect, and the coarse-sampling failure plus recovery.

Do not mark personal completion until the executable checks pass and the learner
gives that teach-back. Static repository checks are not MATLAB-runtime, UI,
numerical-fidelity, bench, HIL, field, or production evidence.
