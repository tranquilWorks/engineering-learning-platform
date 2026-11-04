# Build Stochastic Process Models and Interpret Covariance

**Guiding question:** How do process noise and propagation interval create covariance without implying deterministic state motion?

This Python-first lab executes the bounded mechanism described below. Historical source/conversion records are retained separately.

## Model and equations

$$\dot P=q,\quad P(0)=1$$

$$P(T)=1+qT,\quad \sigma(T)=\sqrt{P(T)}$$

## Worked example

At q=0.2 /s and T=0.5 s, P=1.1 and sigma=sqrt(1.1). The same-input sign fault gives P=0.9. At q=1 /s and T=3 s it gives P=-2, which is impossible as a variance; clipping the square root cannot repair that model.

## Baseline workflow

Write your prediction before running. Reset, inspect both plots and the internal state/geometry in the numerical evidence, then calculate the worked example independently. Separate reported metrics from the actual history or matrix that produces them.

## Two one-variable sweeps

1. From reset defaults, change only `process_noise_density` to `1.0`. Predict from the displayed relation; record both plots and dimensioned metrics, then restore the baseline.

2. From reset defaults, change only `propagation_interval_s` to `3.0`. Predict from the displayed relation; record both plots and dimensioned metrics, then restore the baseline.

## Intentionally broken case

Subtract rather than add the selected process-noise variance, without changing either live parameter. Compare the same selected inputs. A changed sign or gate must act on the stated equation, not swap in unrelated scenario values.

## Recovery

Restore the positive process-noise contribution and check the original q,T pair. Verify recovery matches the original baseline rather than a newly tuned scenario.

## Limiting cases and invariants

This is a scalar normalized zero-drift random walk. It does not implement matrix state propagation or a full stochastic trajectory. A negative covariance is invalid. The displayed clipped square root is a formal plotting convention, never a valid zero uncertainty estimate.

## Independent evidence

`expansion_reference_cases.py` independently evaluates this lesson's signature and full mechanism. References use a polynomial derivative, integrated covariance equation, information-form posterior, SVD geometry, closed-form bias integrals or an implicit nonlinear LOS solution as applicable. They import no production experiment and consume no production result. Five retained cases include baseline, two one-variable sweeps, fault and recovery. Unchanged absolute/relative tolerances remain 1e-8. Additional off-grid, degenerate and mechanism-array checks are required by the aggregate review.

## Common mistakes

- Treating a finite placeholder or clipped square root as valid uncertainty.
- Claiming global or full-system behavior from the bounded model.
- Comparing a fault at different inputs and attributing the difference solely to the fault.
- Reading only a pass flag rather than its governing calculation and physical units.

## Teach-back

Reproduce the worked calculation, explain each sweep causally, show the measured fault and recovery, and state the model boundary in your own words. The Course checkpoint adds the cumulative evidence link. No learner result is recorded by authoring this material.
