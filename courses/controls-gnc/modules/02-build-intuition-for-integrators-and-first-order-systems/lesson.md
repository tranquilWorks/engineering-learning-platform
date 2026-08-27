# Build Intuition for Integrators and First-Order Systems

**Guiding question:** What inputs, observable effects, and failure modes matter when you build Intuition for Integrators and First-Order Systems?

Compare accumulation with exponential memory under the same step input. This native lab preserves the source experiment while making the levers, diagnostics, and recovery available directly in the learning platform.

## Predict before running

The integrator ramp slope follows input amplitude; the first-order final value does not depend on tau. Write down the mechanism you expect—not only the trace direction—before moving a control.

## Model and equations

- $$\dot{x}_I=u$$ — An integrator accumulates area and has no finite step equilibrium.
- $$\tau\dot{y}+y=Ku$$ — A first-order state approaches Ku with time constant tau.

The GUI evaluates these equations deterministically. Read the metric cards and both plots together: a pleasing response can still conceal poor authority, weak conditioning, stale data, or invalid assumptions.

## Two one-variable sweeps

1. Sweep `input_amplitude` through [0.5, 1.0, 1.5]. Hold every other control fixed and explain the causal chain from equation to trace to metric.
2. Sweep `time_constant_s` through [0.5, 2.0, 4.0]. Compare the changed mechanism plot with your first prediction.

Do not tune both levers at once until you can identify which term each lever changes.

## Intentionally broken case

The broken case uses forward Euler with dt/tau greater than two, creating a discrete pole outside the unit circle. Predict the signature before enabling **broken mode**.

## Recovery

Disable the broken case to use the exact first-order transition. A recovery is complete only when you can name the failed assumption and point to the metric or trace that confirms it.

## Common mistakes

- Treating a simulation trace as proof about hardware or production behavior.
- Changing multiple controls at once and losing causal attribution.
- Reading only the final value while ignoring transient effort, conditioning, delay, or saturation.
- Hiding a failed assumption by retuning instead of reproducing and explaining it.

## Teach-back

In two minutes: state the governing equation, explain what each live lever changes, identify the broken assumption, and justify the recovery with one visible metric and one plot feature.

---

## Source lesson (retained and polished into this GUI)

# Lesson: Build Intuition for Integrators and First-Order Systems

## Guiding question

What inputs, observable effects, and failure modes matter when you build Intuition for Integrators and First-Order Systems?

## Compounds on P01

P01 showed a physical state changing because energy was stored and dissipated. Here
we strip that system down to two elemental behaviors. An integrator is pure storage;
a first-order system stores one state while continuously closing its gap to an
equilibrium. These blocks will reappear inside plants, actuators, sensors, observers,
and controllers later in the track.

## Mental model

For a normalized input `u`, an ideal integrator obeys

```text
dx_I/dt = u.
```

The output is accumulated area. A constant positive input therefore produces a
constant positive slope, not a finite settling value.

A first-order system obeys

```text
tau * dy/dt + y = K * u,
```

or `dy/dt = (K*u - y)/tau`. The rate is proportional to the remaining gap. Under a
step of amplitude `A`, the response is `K*A*(1-exp(-t/tau))`; after one `tau` it has
closed about 63.2% of the gap, and after four `tau` it is close to settled.

## Observe before manipulating

Run the baseline section of `experiment.m`. Ask only this prediction first: which
output can settle while the positive input remains applied? In the output view,
observe the ramp beside the bounded exponential. Then inspect the rate view: the
integrator rate stays constant while the first-order rate decays toward zero.

## Move one lever at a time

First change only input amplitude. The integrator slope and first-order equilibrium
scale with amplitude. Reset the amplitude, then change only `tau`. The first-order
curve stretches or compresses in time, but its equilibrium `K*A` does not change.
Use `interactive.m` to repeat those isolated moves.

## Deliberately broken assumption

The continuous first-order system is stable for positive `tau`, but an explicit-Euler
calculation is only stable here when `0 < dt/tau < 2`. The broken case uses
`dt/tau = 3`; its sampled error alternates and grows even though the exact response
settles. The violated assumption is that the numerical interval resolves the system
dynamics. The symptom is invented oscillatory divergence, not physical instability.

## Common misconceptions

- An integrator is not merely a very slow first-order system: the integrator has no
  finite DC equilibrium under a nonzero constant input.
- `tau` changes response speed, not the first-order equilibrium.
- Reaching 63.2% after one time constant does not mean 63.2% is the final value.
- A plausible numerical plot is not automatically a faithful model of the governing
  equation.

## Completion standard

Pass `run_checks.m`, answer the interpretation questions in `checks.md`, and give a
two-sentence teach-back that connects the visible behavior to both equations without
using MATLAB syntax as the explanation.

## Source walkthrough

# Walkthrough: Build Intuition for Integrators and First-Order Systems

Run one experiment section per step so each visual transition has one cause.

1. Read the guiding question: What inputs, observable effects, and failure modes matter when you build Intuition for Integrators and First-Order Systems?
2. Recall P01: damping made stored motion decay. Predict which P02 output can settle while a positive input remains applied.
3. Run only the baseline sections of `experiment.m`. On the output plot, the integrator is a straight ramp while the first-order response bends toward `K*A`.
4. Inspect the rate view. The integrator rate stays at `A`; the first-order rate begins at `K*A/tau` and shrinks with the equilibrium gap.
5. Run sweep 1. Only amplitude changes, so each integrator slope scales in direct proportion. Read the mechanism note before proceeding.
6. Reset to amplitude `A = 1`, then run sweep 2. Only `tau` changes; slower curves retain the same equilibrium. Each curve reaches 63.2% at its own `tau`.
7. Open `interactive.m`. Move amplitude once, press **Reset baseline**, then move `tau` once. State what changed and what remained invariant after each move.
8. Run the broken case. The exact curve still settles while explicit Euler alternates and grows. Name the violated interval-to-dynamics assumption, not merely “numerical error.”
9. Run `run_checks.m`, then answer `checks.md` one question at a time.
10. Teach back in two sentences: mechanism first, visible consequence second.

## Source checks

# Checks: Build Intuition for Integrators and First-Order Systems

## Executable numerical checks

Run:

```matlab
run_checks
```

The assertions cover deterministic repeatability, analytic invariants, amplitude and
time-constant independence, zero-input and one-time-constant limits, the broken-Euler
symptom, malformed inputs, a strictly increasing endpoint-inclusive time grid, actual
Euler interval diagnostics, and the sample-count resource bound.

## Interpretation questions

1. Why does a constant positive input make the integrator ramp instead of settle?
2. When `tau` increases with `A` and `K` fixed, what changes in the first-order plot and what remains invariant?
3. At one time constant, what fraction of the first-order change is complete, and why is that not its final value?
4. In the broken case, which assumption is violated? Explain why the alternating growth is numerical rather than physical.
5. Connect this module to P01: which P01 effects resembled storage and which resembled a state losing its gap or energy?

## Teach-back

In two sentences, answer: “What inputs, observable effects, and failure modes matter
when you build Intuition for Integrators and First-Order Systems?” Lead with the two
mechanisms, then name their visible consequences and the coarse-step failure mode.
