# Follow a Straight Path with Nonlinear Line-of-Sight Guidance

**Guiding question:** When does local exponential LOS intuition agree with the actual nonlinear cross-track trajectory?

This Python-first lab executes the bounded mechanism described below. Historical source/conversion records are retained separately.

## Model and equations

$$\chi_c=-\arctan(y/L)$$

$$\dot x=V\cos\chi_c,\quad \dot y=V\sin\chi_c$$

$$\dot y\simeq -(V/L)y\quad\text{only for }|y|\ll L$$

## Worked example

At y=10 m, L=15 m and V=8 m/s, the initial heading is -atan(2/3)=-33.6901 degrees. Actual lateral speed is -8*10/sqrt(15^2+10^2)=-4.4376 m/s, rather than the local -5.3333 m/s approximation. The fault reverses that motion; its peak heading must be measured over the full growing-error trajectory.

## Baseline workflow

Write your prediction before running. Reset, inspect both plots and the internal state/geometry in the numerical evidence, then calculate the worked example independently. Separate reported metrics from the actual history or matrix that produces them.

## Two one-variable sweeps

1. From reset defaults, change only `lookahead_distance_m` to `60.0`. Predict from the displayed relation; record both plots and dimensioned metrics, then restore the baseline.

2. From reset defaults, change only `vehicle_speed_m_s` to `25.0`. Predict from the displayed relation; record both plots and dimensioned metrics, then restore the baseline.

## Intentionally broken case

Reverse the LOS correction sign in the executed trajectory without changing lookahead or speed. Compare the same selected inputs. A changed sign or gate must act on the stated equation, not swap in unrelated scenario values.

## Recovery

Restore the correcting heading sign, reset, and compare terminal cross-track position on the same straight path. Verify recovery matches the original baseline rather than a newly tuned scenario.

## Limiting cases and invariants

This model follows a single straight path with instantaneous heading tracking. It has no waypoint switching, obstacles or bounded turn-rate dynamics. The exponential solution is a local approximation; nonlinear kinematics generate the displayed path and peak heading. The survey capstone adds separate waypoint, freshness and turn constraints.

## Independent evidence

`expansion_reference_cases.py` independently evaluates this lesson's signature and full mechanism. References use a polynomial derivative, integrated covariance equation, information-form posterior, SVD geometry, closed-form bias integrals or an implicit nonlinear LOS solution as applicable. They import no production experiment and consume no production result. Five retained cases include baseline, two one-variable sweeps, fault and recovery. Unchanged absolute/relative tolerances remain 1e-8. Additional off-grid, degenerate and mechanism-array checks are required by the aggregate review.

## Common mistakes

- Treating a finite placeholder or clipped square root as valid uncertainty.
- Claiming global or full-system behavior from the bounded model.
- Comparing a fault at different inputs and attributing the difference solely to the fault.
- Reading only a pass flag rather than its governing calculation and physical units.

## Teach-back

Reproduce the worked calculation, explain each sweep causally, show the measured fault and recovery, and state the model boundary in your own words. The Course checkpoint adds the cumulative evidence link. No learner result is recorded by authoring this material.
