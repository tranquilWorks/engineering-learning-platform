> The component study below is retained. The new **Integrated navigation** section and additional plots extend it to the complete sequence.

# Propagate One-Axis Inertial Bias Errors

**Guiding question:** How do prescribed accelerometer bias and its correction accumulate into velocity and position error?

This Python-first lab executes the bounded mechanism described below. Historical source/conversion records are retained separately.

## Model and equations

$$\dot{\delta v}=b_a,\quad \dot{\delta p}=\delta v$$

$$\delta v(T)=b_aT,\quad \delta p(T)=b_aT^2/2$$

$$b_{\rm residual}=0.05b_a\quad\text{for the declared nominal correction}$$

## Worked example

With b=0.03 m/s^2 and T=30 s, velocity error is 0.9 m/s and position error is 13.5 m. A declared residual of 0.0015 m/s^2 leaves 0.675 m; omitting correction leaves 13.5 m. Doubling T doubles velocity and quadruples position error, and the plotted endpoint must match the selected T.

## Baseline workflow

Write your prediction before running. Reset, inspect both plots and the internal state/geometry in the numerical evidence, then calculate the worked example independently. Separate reported metrics from the actual history or matrix that produces them.

## Two one-variable sweeps

1. From reset defaults, change only `accelerometer_bias_m_s2` to `0.2`. Predict from the displayed relation; record both plots and dimensioned metrics, then restore the baseline.

2. From reset defaults, change only `coast_duration_s` to `120.0`. Predict from the displayed relation; record both plots and dimensioned metrics, then restore the baseline.

## Intentionally broken case

Omit the declared 95-percent bias correction while keeping the same sensor bias and coast duration. Compare the same selected inputs. A changed sign or gate must act on the stated equation, not swap in unrelated scenario values.

## Recovery

Restore correction and compare both paths over the same selected coast interval. Verify recovery matches the original baseline rather than a newly tuned scenario.

## Limiting cases and invariants

The numerical paths integrate a one-axis bias model at fixed known attitude and zero true acceleration. There is no attitude/quaternion update, Earth rotation, gravity subtraction or full strapdown mechanization. Bias correction is prescribed, not estimated. Those missing mechanisms remain explicit Flight Dynamics/navigation handoffs.

## Independent evidence

`expansion_reference_cases.py` independently evaluates this lesson's signature and full mechanism. References use a polynomial derivative, integrated covariance equation, information-form posterior, SVD geometry, closed-form bias integrals or an implicit nonlinear LOS solution as applicable. They import no production experiment and consume no production result. Five retained cases include baseline, two one-variable sweeps, fault and recovery. Unchanged absolute/relative tolerances remain 1e-8. Additional off-grid, degenerate and mechanism-array checks are required by the aggregate review.

## Common mistakes

- Treating a finite placeholder or clipped square root as valid uncertainty.
- Claiming global or full-system behavior from the bounded model.
- Comparing a fault at different inputs and attributing the difference solely to the fault.
- Reading only a pass flag rather than its governing calculation and physical units.

## Teach-back

Reproduce the worked calculation, explain each sweep causally, show the measured fault and recovery, and state the model boundary in your own words. The Course checkpoint adds the cumulative evidence link. No learner result is recorded by authoring this material.
