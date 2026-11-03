# Analyze Navigation Observability and Alignment Calibration

**Guiding question:** Which maneuvers make heading and sensor bias separately observable?

This Python-first lab executes the bounded mechanism described below. Historical source/conversion records are retained separately.

## Model and equations

$$Y_i=[\cos\psi_i,1],\quad I=Y^TY/\sigma^2$$

$$\mathrm{Cov}(\hat\theta,\hat b)=I^{-1}\quad\text{only if rank}(Y)=2$$

$$\mathrm{rcond}(I)=s_{\min}(Y)^2/s_{\max}(Y)^2$$

## Worked example

At zero span, every row is [1,1]. The two columns are identical, rank is one, and no finite covariance for heading and bias separately exists. Reducing sigma changes scale but cannot change that rank. At 60 degrees, use the actual 41 rows; neither sin(span)^2/sigma^2 nor a regularized condition shortcut is the determinant of this information matrix.

## Baseline workflow

Write your prediction before running. Reset, inspect both plots and the internal state/geometry in the numerical evidence, then calculate the worked example independently. Separate reported metrics from the actual history or matrix that produces them.

## Two one-variable sweeps

1. From reset defaults, change only `maneuver_span_deg` to `180.0`. Predict from the displayed relation; record both plots and dimensioned metrics, then restore the baseline.

2. From reset defaults, change only `measurement_noise` to `0.3`. Predict from the displayed relation; record both plots and dimensioned metrics, then restore the baseline.

## Intentionally broken case

Remove heading diversity while retaining measurement noise, so the actual calibration regressor loses rank. Compare the same selected inputs. A changed sign or gate must act on the stated equation, not swap in unrelated scenario values.

## Recovery

Restore a nonzero span and examine rank, singular values and covariance availability before trusting calibration. Verify recovery matches the original baseline rather than a newly tuned scenario.

## Limiting cases and invariants

A symmetric span samples both its interior and endpoints; opposite endpoint headings alone need not give distinct cosines. The zero-span case is unidentifiable. Its uncertainty is unavailable, not zero; the finite signature placeholder is accompanied by a rank and availability flag. This normalized two-parameter example is not full inertial alignment.

## Independent evidence

`expansion_reference_cases.py` independently evaluates this lesson's signature and full mechanism. References use a polynomial derivative, integrated covariance equation, information-form posterior, SVD geometry, closed-form bias integrals or an implicit nonlinear LOS solution as applicable. They import no production experiment and consume no production result. Five retained cases include baseline, two one-variable sweeps, fault and recovery. Unchanged absolute/relative tolerances remain 1e-8. Additional off-grid, degenerate and mechanism-array checks are required by the aggregate review.

## Common mistakes

- Treating a finite placeholder or clipped square root as valid uncertainty.
- Claiming global or full-system behavior from the bounded model.
- Comparing a fault at different inputs and attributing the difference solely to the fault.
- Reading only a pass flag rather than its governing calculation and physical units.

## Teach-back

Reproduce the worked calculation, explain each sweep causally, show the measured fault and recovery, and state the model boundary in your own words. The Course checkpoint adds the cumulative evidence link. No learner result is recorded by authoring this material.
