# Detect and Exclude a Synthetic Range Fault



## Model and equations

`r=y-h(xhat); leverage_i=H_i(H^T H)^-1 H_i^T`

`z_i=r_i/(sigma sqrt(1-leverage_i)); alarm=max|z_i|>threshold`

`Remove selected row, then solve the retained nonlinear measurement problem again`

The geometry and receiver truth follow the eight-satellite synthetic navigation model at concentration one. A small deterministic noise pattern has amplitude 0.1 m. The fault adds the selected number of metres to satellite index 2. The residual test assumes sigma=1 m and divides by the residual variance reduction caused by fitting the state. The suspect is the row with largest absolute standardized residual. An alarm removes that row only in normal mode; a fresh nonlinear solve uses the seven retained observations. Before and after curves use the actual retained indices. For example, a raw residual of 6 m with leverage 0.36 has standardized magnitude 6/sqrt(0.64)=7.5, exceeding a threshold of five. This illustrates why a residual is not divided by sigma alone. The formal horizontal sigma comes from the retained design matrix; it is a local model covariance, not a certified horizontal protection level.

## Predict before running

Predict whether a zero injected fault should always trigger exclusion and whether deleting one residual value is a valid refit.

## Baseline workflow

Reset controls and leave the named fault disabled. Use Fault magnitude = 16.0 m; Residual alarm threshold = 5.0 sigma. Write a prediction before executing. Read the response curve first, then explain it using the mechanism curve.

Actual fit residuals plots Residual (m) against Satellite index (1). Its series are Before exclusion, Retained and refitted. Residual test plots Standardized magnitude (1) against Satellite index (1). Its series are Magnitude, Threshold.

The computed default record is Largest standardized residual: 9.51586 1; Retained-solution position error: 0.0357419 m; Retained post-fit RMS: 0.0504225 m; Formal horizontal sigma: 1.34126 m. These values are a reproducible worked example, not acceptance thresholds for every slider setting. Retain units and parameter values when comparing another run. A displayed residual near machine precision should be interpreted with the stated model and numerical tolerance.

## Two one-variable sweeps

1. Increase fault magnitude from zero to 60 m with threshold fixed. Locate the alarm transition and inspect which row is excluded; zero fault should not force a deletion.

2. Increase threshold from two to ten with fault magnitude fixed. At the default 16 m fault, the statistic is about 9.5: thresholds below it exclude the suspect, while a threshold of ten retains it. Inspect both retained row count and actual state error.

Return to defaults between sweeps. Keep the other control fixed, record the changed quantity and identify an expected invariant. A control need not change every output; explain the model path through which it acts.

## Intentionally broken case

Broken mode leaves the alarm computation visible but suppresses exclusion, retaining all eight rows for the final fit.

Run the same selected controls with the fault enabled. Compare the curve shape as well as the numerical summary. The fault is a specific executed operation; a red warning or a changed mode flag would not by itself demonstrate its consequence.

## Recovery

Disable the fault mode, restore defaults and confirm that the selected row disappears from the refitted residual series and state error decreases.

Repeat one previously saved nominal setting and check that its values and curves return. Recovery should restore the mechanism, not merely dismiss the warning.

## Limiting cases and invariants

A residual test is geometry dependent and does not cover arbitrary multiple correlated faults. Exclusion can change formal uncertainty. A lower retained residual does not by itself establish integrity or real-world safety.

## Independent evidence

The reference computes leverage through an orthonormal SVD basis and uses a separate complex-step nonlinear solver before and after selecting a row.

Five retained cases cover baseline, two single-control sweeps, the named fault and recovery. Expected values are generated independently; actual values come from the executable lesson. Absolute and relative tolerances remain 1e-8. Agreement checks the declared synthetic model, not empirical validity. MATLAB has not been executed and no MATLAB equivalence is claimed. Browser and container evidence are recorded separately from numerical evidence.

## Engineering review checklist

Check the declared coordinates, units and ordering before evaluating the result. Reconstruct at least one displayed value from retained state or geometric data. Identify which output changes in each sweep and which should remain invariant. Diagnose the named faulty operation, then demonstrate its recovery. Finally state the strongest claim supported by these observations and one claim that requires additional evidence.

## Common mistakes

Do not infer correctness from a changing headline alone. In this lesson, the critical limit is: A residual test is geometry dependent and does not cover arbitrary multiple correlated faults. Exclusion can change formal uncertainty. A lower retained residual does not by itself establish integrity or real-world safety.

Do not compare two runs after changing both controls and attribute the difference to one cause. Do not treat a near-zero floating-point residual as symbolic identity, or a finite sample sweep as a proof for all configurations. Keep the operation that creates the evidence separate from the interpretation assigned to it.

## Teach-back

What evidence distinguishes a real exclusion/refit from multiplying the displayed residual by a fixed factor?

Answer rationale: The retained row identities and count change, the state estimate changes, and residuals recomputed from retained measurements satisfy the new fit. A fixed factor cannot demonstrate those operations.

Use the embedded Course checkpoint to collect a default record, a sweep, a faulty record and a recovered record. Explain the evidence to a colleague using the governing relation and units, then name the untested boundary. This is a self-assessment; no learner score is stored.

Related primary reference: [GNSS measurement modelling and estimation](https://gssc.esa.int/navipedia/index.php/GNSS_Measurements_Modelling).
