# Drive an Actuator into Saturation

**Guiding question:** What inputs, observable effects, and failure modes matter when you drive an Actuator into Saturation?

Show the gap between requested and physically available actuator effort. This native lab preserves the source experiment while making the levers, diagnostics, and recovery available directly in the learning platform.

## Predict before running

A limit below the needed equilibrium command should create persistent tracking error. Write down the mechanism you expect—not only the trace direction—before moving a control.

## Model and equations

- $$u=\operatorname{clip}(K_p(r-y),-u_{max},u_{max})$$ — Saturation changes the loop from linear to piecewise linear.
- $$\dot y=-y+u$$ — The plant cannot exceed the authority delivered by the clipped input.

The GUI evaluates these equations deterministically. Read the metric cards and both plots together: a pleasing response can still conceal poor authority, weak conditioning, stale data, or invalid assumptions.

## Two one-variable sweeps

1. Sweep `reference` through [0.5, 1.5, 3.0]. Hold every other control fixed and explain the causal chain from equation to trace to metric.
2. Sweep `actuator_limit` through [0.5, 2.0, 5.0]. Compare the changed mechanism plot with your first prediction.

Do not tune both levers at once until you can identify which term each lever changes.

## Intentionally broken case

The broken case restricts a 1.5-unit request to 0.6 actuator units. Predict the signature before enabling **broken mode**.

## Recovery

Disable the broken case or reduce the command to fit available authority. A recovery is complete only when you can name the failed assumption and point to the metric or trace that confirms it.

## Common mistakes

- Treating a simulation trace as proof about hardware or production behavior.
- Changing multiple controls at once and losing causal attribution.
- Reading only the final value while ignoring transient effort, conditioning, delay, or saturation.
- Hiding a failed assumption by retuning instead of reproducing and explaining it.

## Teach-back

In two minutes: state the governing equation, explain what each live lever changes, identify the broken assumption, and justify the recovery with one visible metric and one plot feature.

---

## Source lesson (retained and polished into this GUI)

# P11 lesson: Drive an Actuator into Saturation

## Guiding question

What inputs, observable effects, and failure modes matter when you drive an Actuator into Saturation?

## Compounds on

P05 established proportional feedback. P10, the direct prerequisite, separated a
newly computed command from the command actually applied to the plant. P11 holds
timing fixed and asks what changes when actuator amplitude—not timing—is constrained.

## Tutor path

Ask one prediction: when `uRequested` exceeds `uLimit`, which trace shows the limit
first? Then reveal the baseline output view before the command view.

The controller requests, with `Kp=4 actuator/output`,

`uRequested = 4*(r-y)`.

The actuator applies

`uApplied = min(max(uRequested,-uLimit),uLimit)`.

For `tau=1 s` and plant gain `g=1 output/actuator`, each held interval moves as

`yNext = exp(-dt/tau)*y + (1-exp(-dt/tau))*g*uApplied`.

That equation explains the observation: the output stays continuous, but it rises
more slowly because the missing command never reached the plant. The gap
`uRequested-uApplied` is the most direct saturation symptom.

Move reference amplitude while holding actuator limit fixed. After the learner names
the longer clipped interval, reset reference and move only the limit. Connect shorter
clipping and lower tracking error to increased physical authority, not a change in
controller gain.

For the broken case, `r=1.5 output` and `uLimit=0.6 actuator`. Constant maximum
actuation can approach only `y=0.6 output`, so the target is infeasible and clipping
persists. Recover by changing only `uLimit` to `2 actuator`.

## Misconceptions to correct directly

- Saturation is not merely a flat-looking plot; it is a mismatch between requested
  and applied physical effort.
- A faster sample rate cannot create missing actuator authority.
- Proportional error during saturation is not integrator windup. P11 has no integral
  state; P12 will show what changes when an integrator accumulates this error.
- A target can be physically infeasible even though the code continues to produce
  finite numbers.
- The reference, controller gain, and actuator limit are different quantities with
  different units and roles.

## Completion

Run `run_checks.m`, ask the interpretation questions in `checks.md` one at a time,
and request the two-sentence teach-back. Static repository checks do not establish
MATLAB runtime, UI behavior, numerical fidelity, bench, HIL, field, or production
validation.

## Source walkthrough

# P11 walkthrough: Drive an Actuator into Saturation

1. Read the guiding question and predict where clipping appears first.
2. Run the `r=1 output`, `uLimit=2 actuator` baseline output section. The limited
   response initially trails the unlimited proportional response, then approaches the
   same P-only equilibrium.
3. Reveal the command view. The controller initially requests `4 actuator`, the plant
   receives `2 actuator`, and the clipping gap is `2 actuator`.
4. Observe that clipping releases near `0.29 s`; requested and applied commands then meet.
5. Sweep only reference through `[0.25 0.5 1 1.5 2] output` at a fixed `2 actuator`
   limit. Larger demand widens the missing-command gap and increases clipped time.
6. Reset reference to `1 output`. Sweep only limit through
   `[0.4 0.6 0.8 1.2 2] actuator`. Low authority keeps the command clipped; higher
   authority releases sooner and reduces accumulated absolute tracking error.
7. Run the broken `r=1.5`, `uLimit=0.6` case. The actuator remains at its limit and
   the output approaches `0.6`, not the requested `1.5`.
8. Increase only the limit to `2 actuator`. The command releases from saturation and
   the trajectory recovers toward the unchanged P-only equilibrium.
9. Explain the mechanism: the clamp bounds applied effort, and plant gain
   `g=1 output/actuator` converts that bounded effort into visible motion.
10. Run `run_checks.m` and give the teach-back from `checks.md`.

Do not describe static checks as MATLAB execution. No rendered plot, UI callback,
MATLAB numerical-fidelity, bench, HIL, field, or production result is retained here.

## Source checks

# P11 checks: Drive an Actuator into Saturation

Run `run_checks.m`, then answer one interpretation question at a time.

1. Which two traces must be compared to prove saturation rather than infer it from output shape?
2. What physical quantity does `uRequested-uApplied` represent?
3. Why does the plant output remain continuous when the command is clipped?
4. In the reference sweep, what remains fixed and why does clipped time grow?
5. In the actuator-limit sweep, what remains fixed and why can low limits remain active?
6. What should happen when the actuator limit is high enough that the clamp never activates?
7. Why is the `r=1.5`, `uLimit=0.6` target infeasible for
   `tau*y'=-y+g*uApplied` with `g=1 output/actuator`?
8. Which retained invariant proves the actuator never exceeds its declared limit?
9. Why is increasing only the limit a real recovery while smoothing the plot is not?
10. Why is the integral absolute error metric in P11 not evidence of integrator windup?
11. Which numerical checks are independent of presentation plots?

## Teach-back

In two sentences, answer the guiding question by distinguishing reference demand from
actuator limit, naming one visible effect of clipping, and explaining persistent
saturation plus the one-limit recovery.

Do not mark personal completion until the executable checks pass and the learner gives
that teach-back. Static repository checks are not MATLAB-runtime, UI,
numerical-fidelity, bench, HIL, field, or production evidence.
