# Estimate Nonlinear State with an Extended Kalman Filter

**Guiding question:** When is a first-order measurement linearization informative enough for an EKF update?

This Python-first lab executes the bounded mechanism described below. Historical source/conversion records are retained separately.

## Model and equations

$$h(x)=x^2,\quad H=2\hat x^-,\quad \nu=z-h(\hat x^-)$$

$$K=P^-H/(H^2P^-+R),\quad \hat x^+=\hat x^-+K\nu$$

$$P^+=(1-KH)^2P^-+K^2R$$

## Worked example

At xhat=1 and sigma=0.5, P=0.25, H=2, S=2, K=0.25 and innovation=1.25. Thus xplus=1.3125 and Pplus=0.125. The true nonlinear-minus-linearized residual is (0.3125)^2=0.09765625; the old prior variance 0.25 is not that residual.

## Baseline workflow

Write your prediction before running. Reset, inspect both plots and the internal state/geometry in the numerical evidence, then calculate the worked example independently. Separate reported metrics from the actual history or matrix that produces them.

## Two one-variable sweeps

1. From reset defaults, change only `prior_standard_deviation` to `2.0`. Predict from the displayed relation; record both plots and dimensioned metrics, then restore the baseline.

2. From reset defaults, change only `linearization_state` to `3.0`. Predict from the displayed relation; record both plots and dimensioned metrics, then restore the baseline.

## Intentionally broken case

Freeze the measurement Jacobian at zero while preserving prior state, prior uncertainty and the measurement. Compare the same selected inputs. A changed sign or gate must act on the stated equation, not swap in unrelated scenario values.

## Recovery

Restore H=2*xhat, then compare the same prior and measurement; discuss a nonlinear alternative at a truly zero prior. Verify recovery matches the original baseline rather than a newly tuned scenario.

## Limiting cases and invariants

This is one scalar measurement update with fixed z=2.25 and R=1 in normalized units, not a complete time-recursive EKF. A squared observation has a global sign ambiguity. A zero Jacobian at the true linearization point is a real first-order information loss, not a software fault.

## Independent evidence

`expansion_reference_cases.py` independently evaluates this lesson's signature and full mechanism. References use a polynomial derivative, integrated covariance equation, information-form posterior, SVD geometry, closed-form bias integrals or an implicit nonlinear LOS solution as applicable. They import no production experiment and consume no production result. Five retained cases include baseline, two one-variable sweeps, fault and recovery. Unchanged absolute/relative tolerances remain 1e-8. Additional off-grid, degenerate and mechanism-array checks are required by the aggregate review.

## Common mistakes

- Treating a finite placeholder or clipped square root as valid uncertainty.
- Claiming global or full-system behavior from the bounded model.
- Comparing a fault at different inputs and attributing the difference solely to the fault.
- Reading only a pass flag rather than its governing calculation and physical units.

## Teach-back

Reproduce the worked calculation, explain each sweep causally, show the measured fault and recovery, and state the model boundary in your own words. The Course checkpoint adds the cumulative evidence link. No learner result is recorded by authoring this material.
