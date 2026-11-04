# Monitor Innovations, NIS, NEES, and Measurement Gates

**Guiding question:** How do consistency statistics distinguish expected residuals from outliers and filter overconfidence?

This Python-first lab executes the bounded mechanism described below. Historical source/conversion records are retained separately.

## Model and equations

$$S_k=P_k^-+R,\quad \mathrm{NIS}_k=\nu_k^2/S_k$$

$$K_k=P_k^-/S_k,\quad \hat x_k^+=\hat x_k^-+K_k\nu_k$$

$$\mathrm{NEES}_k=(\hat x_k^+-x_k)^2/P_k^+$$

## Worked example

The injected innovation is 4 sqrt(S) at defaults, so its NIS is 16 and its exceedance over 6.63 is 9.37. Nominal gating retains the prior at that step; bypassing it changes the posterior state and covariance. Compare the full paths and posterior NEES rather than treating an accept flag alone as a filter.

## Baseline workflow

Write your prediction before running. Reset, inspect both plots and the internal state/geometry in the numerical evidence, then calculate the worked example independently. Separate reported metrics from the actual history or matrix that produces them.

## Two one-variable sweeps

1. From reset defaults, change only `nis_gate` to `15.0`. Predict from the displayed relation; record both plots and dimensioned metrics, then restore the baseline.

2. From reset defaults, change only `outlier_sigma` to `10.0`. Predict from the displayed relation; record both plots and dimensioned metrics, then restore the baseline.

## Intentionally broken case

Bypass the innovation gate while retaining the identical injected innovation at update 20. Compare the same selected inputs. A changed sign or gate must act on the stated equation, not swap in unrelated scenario values.

## Recovery

Restore gating, reset, and verify the original measurement is rejected when its NIS exceeds the selected threshold. Verify recovery matches the original baseline rather than a newly tuned scenario.

## Limiting cases and invariants

The truth, process and measurement streams are deterministic illustrations; the samples are neither independent trials nor a chi-square coverage validation. NIS is observable without truth, whereas NEES requires truth. This scalar filter does not establish general consistency or navigation integrity.

## Independent evidence

`expansion_reference_cases.py` independently evaluates this lesson's signature and full mechanism. References use a polynomial derivative, integrated covariance equation, information-form posterior, SVD geometry, closed-form bias integrals or an implicit nonlinear LOS solution as applicable. They import no production experiment and consume no production result. Five retained cases include baseline, two one-variable sweeps, fault and recovery. Unchanged absolute/relative tolerances remain 1e-8. Additional off-grid, degenerate and mechanism-array checks are required by the aggregate review.

## Common mistakes

- Treating a finite placeholder or clipped square root as valid uncertainty.
- Claiming global or full-system behavior from the bounded model.
- Comparing a fault at different inputs and attributing the difference solely to the fault.
- Reading only a pass flag rather than its governing calculation and physical units.

## Teach-back

Reproduce the worked calculation, explain each sweep causally, show the measured fault and recovery, and state the model boundary in your own words. The Course checkpoint adds the cumulative evidence link. No learner result is recorded by authoring this material.
