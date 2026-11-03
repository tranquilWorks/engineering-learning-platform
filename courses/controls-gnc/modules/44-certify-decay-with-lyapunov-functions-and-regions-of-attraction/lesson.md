# Certify Decay with Lyapunov Functions and Regions of Attraction

**Guiding question:** How does a Lyapunov sublevel set become a defensible local region-of-attraction certificate?

This Python-first lab executes the bounded mechanism described below. Historical source/conversion records are retained separately.

## Model and equations

$$\dot x=-a x+b x^3,\quad V=x^2/2$$

$$\dot V=-a x^2+b x^4=-x^2(a-bx^2)$$

$$r<1/\sqrt{b}\quad (a=1)$$

## Worked example

At r=0.7 and b=0.8, the decay margin is 1-0.8(0.7)^2=0.608 /s and boundary Vdot=-0.29792 /s. At the same inputs with reversed damping, Vdot=0.68208 /s. Both signs come from the executed vector field, not a hard-coded pass flag.

## Baseline workflow

Write your prediction before running. Reset, inspect both plots and the internal state/geometry in the numerical evidence, then calculate the worked example independently. Separate reported metrics from the actual history or matrix that produces them.

## Two one-variable sweeps

1. From reset defaults, change only `sublevel_radius` to `1.4`. Predict from the displayed relation; record both plots and dimensioned metrics, then restore the baseline.

2. From reset defaults, change only `cubic_coefficient` to `1.5`. Predict from the displayed relation; record both plots and dimensioned metrics, then restore the baseline.

## Intentionally broken case

Reverse the linear damping sign in the actual cubic vector field while retaining the selected radius and cubic coefficient. Compare the same selected inputs. A changed sign or gate must act on the stated equation, not swap in unrelated scenario values.

## Recovery

Restore negative linear feedback and choose a strict sublevel inside the nominal equilibrium boundary. Verify recovery matches the original baseline rather than a newly tuned scenario.

## Limiting cases and invariants

The origin has Vdot=0 and is excluded from the strict inequality. At r=1/sqrt(b), the boundary is another equilibrium; equality is not asymptotic decay. The plotted domain extends beyond the selected sublevel to make its limitation visible.

## Independent evidence

`expansion_reference_cases.py` independently evaluates this lesson's signature and full mechanism. References use a polynomial derivative, integrated covariance equation, information-form posterior, SVD geometry, closed-form bias integrals or an implicit nonlinear LOS solution as applicable. They import no production experiment and consume no production result. Five retained cases include baseline, two one-variable sweeps, fault and recovery. Unchanged absolute/relative tolerances remain 1e-8. Additional off-grid, degenerate and mechanism-array checks are required by the aggregate review.

## Common mistakes

- Treating a finite placeholder or clipped square root as valid uncertainty.
- Claiming global or full-system behavior from the bounded model.
- Comparing a fault at different inputs and attributing the difference solely to the fault.
- Reading only a pass flag rather than its governing calculation and physical units.

## Teach-back

Reproduce the worked calculation, explain each sweep causally, show the measured fault and recovery, and state the model boundary in your own words. The Course checkpoint adds the cumulative evidence link. No learner result is recorded by authoring this material.
