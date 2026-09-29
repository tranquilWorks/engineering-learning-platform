# Inject and Reset a One-Axis Navigation Error State



## Model and equations

`delta=[position error, velocity error, accelerometer bias error]`

`F=[[1,dt,-dt²/2],[0,1,-dt],[0,0,1]]; Pminus=F P F^T+Q`

`K=Pminus H^T/(H Pminus H^T+R); nominal+=K innovation; delta_reset=0`

`Pplus=(I-KH)Pminus(I-KH)^T+K R K^T`

This additive one-axis model uses position in metres, velocity in metres per second and accelerometer bias in metres per second squared. Truth moves at 2 m/s for 20 seconds, with zero true acceleration. The measured acceleration is 0.04 m/s² because of a constant bias. The estimator starts at [0,2,0] with covariance diag(1,0.25,0.0025). GNSS positions are 2t+0.3 sin(0.7t) metres, with assumed measurement variance 1 m². The time grid includes both 0.1-second propagation points and every requested GNSS update time. Bias random-walk intensity q has units m/s²/sqrt(s); its integrated process covariance includes position/bias and velocity/bias cross terms. Without any correction, the 0.04 m/s² bias creates 0.5 times 0.04 times 20²=8 m of position drift. Each innovation produces a three-component correction. Additive coordinates have identity reset Jacobian after injection; this is not the attitude reset used in a three-dimensional inertial filter.

## Predict before running

Predict what happens if covariance is updated but the nominal navigation state never receives the correction.

## Baseline workflow

Reset controls and leave the named fault disabled. Use GNSS update interval = 1.0 s; Bias random walk = 0.01 m/s^2/sqrt(s). Write a prediction before executing. Read the response curve first, then explain it using the mechanism curve.

Injected navigation state plots Position (m) against Time (s). Its series are Estimated position, Truth. Error and formal sigma plots Position error (m) against Time (s). Its series are Actual error, Formal sigma.

The computed default record is Last update prior position sigma: 0.76907 m; Last update posterior position sigma: 0.609631 m; Terminal position error: 0.148086 m; Terminal bias error: 0.00458205 m/s^2. These values are a reproducible worked example, not acceptance thresholds for every slider setting. Retain units and parameter values when comparing another run. A displayed residual near machine precision should be interpreted with the stated model and numerical tolerance.

## Two one-variable sweeps

1. Increase GNSS interval from 1 to 10 seconds while holding bias intensity fixed. Observe longer propagation gaps and distinguish pre-update from post-update uncertainty.

2. Increase bias random walk from 0.01 to 0.08 at fixed update interval. Compare formal sigma and actual error; assumed uncertainty changes the gains but does not alter the declared constant true bias.

Return to defaults between sweeps. Keep the other control fixed, record the changed quantity and identify an expected invariant. A control need not change every output; explain the model path through which it acts.

## Intentionally broken case

Broken mode computes updates and shrinks covariance but discards the state correction instead of injecting it.

Run the same selected controls with the fault enabled. Compare the curve shape as well as the numerical summary. The fault is a specific executed operation; a red warning or a changed mode flag would not by itself demonstrate its consequence.

## Recovery

Restore injection and reset both controls. Check actual position error and bias estimate, not only the covariance drop.

Repeat one previously saved nominal setting and check that its values and curves return. Recovery should restore the mechanism, not merely dismiss the warning.

## Limiting cases and invariants

The terminal sigma can fall while actual error remains large in the fault. Additive reset leaves covariance coordinates unchanged. This lesson does not implement attitude, Earth frames, lever arms or a complete strapdown INS.

## Independent evidence

The independent full-state filter uses the same physical model but evaluates process covariance by three-point Gaussian quadrature and uses the Schur covariance update instead of the production Joseph recurrence.

Five retained cases cover baseline, two single-control sweeps, the named fault and recovery. Expected values are generated independently; actual values come from the executable lesson. Absolute and relative tolerances remain 1e-8. Agreement checks the declared synthetic model, not empirical validity. MATLAB has not been executed and no MATLAB equivalence is claimed. Browser and container evidence are recorded separately from numerical evidence.

## Engineering review checklist

Check the declared coordinates, units and ordering before evaluating the result. Reconstruct at least one displayed value from retained state or geometric data. Identify which output changes in each sweep and which should remain invariant. Diagnose the named faulty operation, then demonstrate its recovery. Finally state the strongest claim supported by these observations and one claim that requires additional evidence.

## Common mistakes

Do not infer correctness from a changing headline alone. In this lesson, the critical limit is: The terminal sigma can fall while actual error remains large in the fault. Additive reset leaves covariance coordinates unchanged. This lesson does not implement attitude, Earth frames, lever arms or a complete strapdown INS.

Do not compare two runs after changing both controls and attribute the difference to one cause. Do not treat a near-zero floating-point residual as symbolic identity, or a finite sample sweep as a proof for all configurations. Keep the operation that creates the evidence separate from the interpretation assigned to it.

## Teach-back

Why can both normal and broken cases show a smaller post-update sigma while only one corrects position?

Answer rationale: The covariance recurrence is independent of the realized innovation for this linear model. State injection uses that innovation; dropping it makes the reported uncertainty inconsistent with the executed estimator.

Use the embedded Course checkpoint to collect a default record, a sweep, a faulty record and a recovered record. Explain the evidence to a colleague using the governing relation and units, then name the untested boundary. This is a self-assessment; no learner score is stored.
