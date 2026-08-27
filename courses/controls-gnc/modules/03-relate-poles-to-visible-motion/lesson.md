# Relate Poles to Visible Motion

**Guiding question:** What inputs, observable effects, and failure modes matter when you relate Poles to Visible Motion?

Translate complex pole location into decay, oscillation, and instability. This native lab preserves the source experiment while making the levers, diagnostics, and recovery available directly in the learning platform.

## Predict before running

Moving sigma right slows decay and eventually turns the envelope into growth. Write down the mechanism you expect—not only the trace direction—before moving a control.

## Model and equations

- $$x(t)=e^{\sigma t}\cos(\omega t)$$ — The real part sets the envelope and the imaginary part sets oscillation rate.
- $$T=2\pi/|\omega|$$ — Imaginary pole magnitude maps directly to period.

The GUI evaluates these equations deterministically. Read the metric cards and both plots together: a pleasing response can still conceal poor authority, weak conditioning, stale data, or invalid assumptions.

## Two one-variable sweeps

1. Sweep `pole_real_per_s` through [-1.0, -0.5, 0.2]. Hold every other control fixed and explain the causal chain from equation to trace to metric.
2. Sweep `pole_imag_rad_s` through [0.5, 2.0, 5.0]. Compare the changed mechanism plot with your first prediction.

Do not tune both levers at once until you can identify which term each lever changes.

## Intentionally broken case

The broken case reflects a stable pole into the right half-plane, turning decay into exponential growth. Predict the signature before enabling **broken mode**.

## Recovery

Disable the broken case and keep the real part negative. A recovery is complete only when you can name the failed assumption and point to the metric or trace that confirms it.

## Common mistakes

- Treating a simulation trace as proof about hardware or production behavior.
- Changing multiple controls at once and losing causal attribution.
- Reading only the final value while ignoring transient effort, conditioning, delay, or saturation.
- Hiding a failed assumption by retuning instead of reproducing and explaining it.

## Teach-back

In two minutes: state the governing equation, explain what each live lever changes, identify the broken assumption, and justify the recovery with one visible metric and one plot feature.

---

## Source lesson (retained and polished into this GUI)

# Lesson: Relate Poles to Visible Motion

## Guiding question

What inputs, observable effects, and failure modes matter when you relate Poles to Visible Motion?

## Compounds on P02

P02 showed a first-order response settling with the exponential factor
`exp(-t/tau)`. Its pole is `-1/tau`: moving that real pole left makes the
exponential vanish faster. P03 extends the same idea to a conjugate pair. The real
coordinate still controls an exponential, while an imaginary coordinate makes the
state alternate direction.

## Mental model

For poles `p = sigma +/- j*omega`, free displacement follows

```text
x'' - 2*sigma*x' + (sigma^2 + omega^2)*x = 0
x(t) = exp(sigma*t) * (x0*cos(omega*t) + B*sin(omega*t))
B = (v0 - sigma*x0)/omega.
```

The inputs are the two pole coordinates, initial displacement `x0` in metres,
initial velocity `v0` in metres per second, and the observation grid. The primary
observables are displacement, its exponential envelope, the pole-plane location,
cycle period, and unit-mass mechanical energy.

- `sigma < 0` means left-half-plane poles and a shrinking envelope.
- `sigma = 0` means imaginary-axis poles and sustained motion.
- `sigma > 0` means right-half-plane poles and a growing envelope.
- `omega > 0` gives period `T = 2*pi/omega`; larger `omega` packs cycles closer.
- `omega = 0` is a repeated real pole, handled by its exact nonoscillatory limit.

Initial conditions decide phase and visible amplitude, but they do not move the
poles. Likewise, a pole pair predicts the mode's shape in time; it does not specify
how strongly an external input excites that mode.

## Observe before manipulating

Run only the baseline sections of `experiment.m`. Make one prediction first: will
the released displacement reverse direction, and will its envelope grow or shrink?
Observe the motion view, then locate the same `sigma` and `omega` on the pole plane.

## Move one lever at a time

First sweep only `sigma`. More-negative values shrink the envelope faster while
`omega = 2 rad/s` preserves the `pi`-second cycle spacing. Reset `sigma`, then sweep
only `omega`. The period changes in inverse proportion, while the common real part
preserves `exp(-0.5*t)` as the envelope ratio. The natural frequency changes when
either coordinate moves, so call the controls pole coordinates rather than treating
the real-part control as an isolated physical damper.

## Deliberately broken assumption and recovery

The broken case violates the assumption that the mode dissipates energy and its
poles remain in the left half-plane. Moving `sigma` from `-0.25` to `+0.25 1/s`
crosses the stability boundary. The cycle spacing stays fixed because `omega` did
not move, but the envelope and unit-mass energy grow outward. Restoring the negative
real coordinate recovers decay without changing the imaginary coordinates.

## Common misconceptions

- Pole plots are not abstract decorations: horizontal position maps to envelope
  growth or decay, and vertical distance maps to cycle spacing.
- A negative real part does not mean the displacement is always negative; it means
  the exponential envelope decays.
- A larger imaginary part means faster oscillation, not faster envelope decay.
- Initial displacement and velocity change the visible phase and scale, not the pole
  locations.
- A sampled curve that looks bounded for a short window is not proof of stability;
  the pole real part and longer-horizon envelope reveal growth.

## Completion standard

Pass `run_checks.m`, answer the interpretation questions in `checks.md`, and give a
two-sentence teach-back: mechanism first, visible consequence second. MATLAB syntax
is not an explanation.

## Source walkthrough

# Walkthrough: Relate Poles to Visible Motion

Run one experiment section per step so every changed view has one cause.

1. Read the guiding question: What inputs, observable effects, and failure modes matter when you relate Poles to Visible Motion?
2. Recall P02's first-order pole at `-1/tau`. Predict whether the P03 baseline will reverse direction and whether its envelope will grow or shrink.
3. Run only the baseline motion section. Observe repeated zero crossings inside the shrinking displacement envelope.
4. Run the pole-plane section. Connect horizontal coordinate `sigma = -0.5 1/s` to decay and vertical coordinates `+/-2 rad/s` to the `pi`-second period.
5. Run sweep 1. Only `sigma` changes, so the envelope constants become 1, 2, and 5 seconds while cycle spacing stays fixed. Read the mechanism note before proceeding.
6. Reset `sigma = -0.5 1/s`, then run sweep 2. Only `omega` changes, so periods become `2*pi`, `pi`, and `pi/2` seconds while the exponential ratio stays fixed.
7. Open `interactive.m`. Move the real coordinate once, press **Reset baseline**, then move the imaginary coordinate once. State the changed observable and invariant after each move.
8. Run the broken case. Identify the violated left-half-plane/dissipation assumption from the growing envelope and energy, then explain why restoring negative `sigma` recovers decay.
9. Run `run_checks.m`, then answer `checks.md` one question at a time.
10. Teach back in two sentences: map pole coordinates to mechanisms first, then name their visible consequences and the right-half-plane failure.

## Source checks

# P03 checks: Relate Poles to Visible Motion

Run `run_checks.m` first. It checks deterministic repeatability, initial conditions,
the characteristic equation, analytic envelope bounds, energy direction, lever
independence, repeated and marginal limits, the broken/recovered pair, malformed
inputs, endpoint behavior, and calculation resource bounds.

Then answer one interpretation question at a time:

1. With `sigma = -0.5 1/s` and `omega = 2 rad/s`, which visible feature comes from each coordinate, and what are the envelope time constant and oscillation period?
2. When only `sigma` becomes more negative, why does the motion disappear sooner even though its zero-crossing spacing remains similar?
3. When only `omega` increases, why do more cycles fit in the same window without changing the common exponential ratio?
4. What happens at the two limits `sigma = 0` and `omega = 0`, and how does the double-zero case reconnect to P02's integrator?
5. In the broken case, which assumption is violated, what symptoms reveal it, and what single coordinate change recovers decay?

## Teach-back

In two sentences, answer: “What inputs, observable effects, and failure modes matter
when you relate Poles to Visible Motion?” Sentence one must map real and imaginary
coordinates to mechanisms. Sentence two must connect initial conditions to visible
motion and explain the right-half-plane failure plus its recovery.

Passing static repository tests does not claim that these MATLAB checks, figures, or
controls executed. Record a separate MATLAB-runtime result if they are run.
