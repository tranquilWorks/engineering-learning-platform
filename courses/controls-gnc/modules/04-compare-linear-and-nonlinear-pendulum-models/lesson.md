# Compare Linear and Nonlinear Pendulum Models

**Guiding question:** What inputs, observable effects, and failure modes matter when you compare Linear and Nonlinear Pendulum Models?

Expose when the small-angle pendulum approximation stops representing the nonlinear plant. This native lab preserves the source experiment while making the levers, diagnostics, and recovery available directly in the learning platform.

## Predict before running

Large release angles should lengthen the nonlinear period relative to the linear prediction. Write down the mechanism you expect—not only the trace direction—before moving a control.

## Model and equations

- $$\ddot{\theta}+2\zeta\sqrt{g/L}\dot{\theta}+(g/L)\sin\theta=0$$ — The nonlinear restoring torque follows sine of angle.
- $$\sin\theta\approx\theta$$ — The linear model is trustworthy only for small angles.

The GUI evaluates these equations deterministically. Read the metric cards and both plots together: a pleasing response can still conceal poor authority, weak conditioning, stale data, or invalid assumptions.

## Two one-variable sweeps

1. Sweep `initial_angle_deg` through [5.0, 30.0, 100.0]. Hold every other control fixed and explain the causal chain from equation to trace to metric.
2. Sweep `length_m` through [0.5, 1.0, 2.0]. Compare the changed mechanism plot with your first prediction.

Do not tune both levers at once until you can identify which term each lever changes.

## Intentionally broken case

The broken case forces a 120 degree release while interpreting the small-angle trace as truth. Predict the signature before enabling **broken mode**.

## Recovery

Disable the broken case or reduce the release angle until the approximation error is acceptable. A recovery is complete only when you can name the failed assumption and point to the metric or trace that confirms it.

## Common mistakes

- Treating a simulation trace as proof about hardware or production behavior.
- Changing multiple controls at once and losing causal attribution.
- Reading only the final value while ignoring transient effort, conditioning, delay, or saturation.
- Hiding a failed assumption by retuning instead of reproducing and explaining it.

## Teach-back

In two minutes: state the governing equation, explain what each live lever changes, identify the broken assumption, and justify the recovery with one visible metric and one plot feature.

---

## Source lesson (retained and polished into this GUI)

# Lesson: Compare Linear and Nonlinear Pendulum Models

## Guiding question

What inputs, observable effects, and failure modes matter when you compare Linear and Nonlinear Pendulum Models?

## Compounds on P03

P03 related a linear second-order equation to a pole pair and visible oscillation.
For a pendulum near its hanging equilibrium, the linearized equation has natural
frequency `wn = sqrt(g/L)` and poles determined by `wn` and damping ratio `zeta`.
P04 keeps that linear prediction beside the physical nonlinear restoring law so the
approximation boundary becomes observable.

## Mental model

For angle `theta` in radians,

```text
nonlinear restoring acceleration = -(g/L)*sin(theta)
linear restoring acceleration    = -(g/L)*theta.
```

The approximation is local, not magical. Around zero, `sin(theta) = theta -
theta^3/6 + ...`, so the omitted term is tiny. At a large angle, the linear term has
too much magnitude. It pulls the prediction toward zero too quickly, shortening the
predicted cycle relative to the nonlinear pendulum.

The inputs are release angle, release angular rate, length, damping ratio, and the
calculation grid. The primary observables are both angle histories, restoring-law
curves, first-zero times, phase error, period scale, and specific mechanical energy.

## Observe before manipulating

Run only the baseline sections of `experiment.m`. Make one prediction: after a
20-degree release, will the nonlinear curve lead or lag the linear curve? Observe
the angle history first, then use the restoring-law plot to explain the direction of
the accumulating phase error.

## Move one lever at a time

First sweep release angle while length stays at `1 m`. The five-degree curves nearly
overlap; the 90-degree curves separate because `sin(theta)` no longer follows
`theta`. Reset to 20 degrees, then sweep only length. Since
`T_small = 2*pi*sqrt(L/g)`, longer pendulums move more slowly. Length changes the
clock for both models; release angle changes the approximation error.

## Deliberately broken assumption and recovery

The broken case trusts the small-angle substitution at 120 degrees. There,
`theta = 2.094 rad` but `sin(theta) = 0.866`, so the linear model begins with more
than twice the restoring magnitude and runs ahead. Recover by reducing the release
to five degrees, or use the nonlinear model when large-angle timing matters.

## Common misconceptions

- “Linear” does not mean the line traced by the pendulum bob; it means the state
  appears only to the first power in the governing equation.
- Degrees are convenient for controls and labels, but `sin(theta) approximately
  theta` requires radians.
- A deterministic numerical curve is not automatically a faithful physical model;
  the approximation and the calculation step are separate assumptions.
- Length changes the natural time scale in both models. It does not make a large
  angle small.
- Model disagreement is not numerical instability here. The broken case is a valid
  calculation with an invalid small-angle interpretation.

## Completion standard

Pass `run_checks.m`, answer the interpretation questions in `checks.md`, and give a
two-sentence teach-back: mechanism first, visible consequence second. MATLAB syntax
is not an explanation.

## Source walkthrough

# Walkthrough: Compare Linear and Nonlinear Pendulum Models

Run one experiment section per step so every changed view has one cause.

1. Read the guiding question: What inputs, observable effects, and failure modes matter when you compare Linear and Nonlinear Pendulum Models?
2. Recall P03's linear second-order motion and pole pair. Predict whether the nonlinear pendulum will lead or lag after a 20-degree release.
3. Run only the baseline motion section. Observe the initially close curves and the slowly accumulating timing difference.
4. Run the restoring-law section. Connect the weaker magnitude of `sin(theta)` away from zero to the nonlinear curve's later zero crossing.
5. Run sweep 1. Only release angle changes; compare five, 30, and 90 degrees while length, damping, and initial rate stay fixed. Read the mechanism note before proceeding.
6. Reset release angle to 20 degrees, then run sweep 2. Only length changes; connect the stretched cycles to `T_small = 2*pi*sqrt(L/g)`.
7. Open `interactive.m`. Move release angle once, press **Reset baseline**, then move length once. State the changed observable and invariant after each move.
8. Run the 120-degree broken case. Name the violated small-angle assumption from the early linear crossing, then observe recovery at five degrees.
9. Run `run_checks.m`, then answer `checks.md` one question at a time.
10. Teach back in two sentences: state the restoring-law mechanism first, then name when the approximation works, how failure appears, and how to recover.

## Source checks

# P04 checks: Compare Linear and Nonlinear Pendulum Models

Run `run_checks.m` first. It checks deterministic repeatability, shared initial
conditions, governing accelerations, linear poles and period, energy direction,
release-angle and length levers, small-angle and zero-state limits, sign symmetry,
the broken/recovered pair, malformed inputs, endpoint behavior, calculation
resolution, and resource bounds.

Then answer one interpretation question at a time:

1. Which single restoring term differs between the models, and why must `theta` be in radians when making the small-angle comparison?
2. At a 20-degree release, why does the nonlinear curve gradually lag even though both models begin from exactly the same state?
3. When only release angle increases, which error grows and which physical parameters remain unchanged?
4. When only length increases, why do both predictions slow down, and why does that not repair a large-angle approximation?
5. In the 120-degree broken case, which assumption is violated, what visible symptom reveals it, and what two recovery choices are available?

## Teach-back

In two sentences, answer: “What inputs, observable effects, and failure modes matter
when you compare Linear and Nonlinear Pendulum Models?” Sentence one must connect
the two restoring laws to release angle and length. Sentence two must identify the
large-angle symptom and a valid recovery.

Passing static repository tests does not claim that these MATLAB checks, figures, or
controls executed. Record a separate MATLAB-runtime result if they are run.
