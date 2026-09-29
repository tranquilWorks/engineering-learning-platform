# Solve Position and Clock from Synthetic Pseudoranges



## Model and equations

`rho_i=||s_i-x||+b+epsilon_i; b=c delta_t in metres`

`H_i=[(x-s_i)^T/||x-s_i||,1]; delta=argmin ||H delta-r||²`

`PDOP=sqrt(trace((H^T H)^-1[0:3,0:3]))`

Eight synthetic satellites lie at radius 20 million metres. Their declared azimuths are [0,47,99,146,201,249,294,337] degrees divided by geometry concentration; elevations are 0.6+(base elevation-0.6)/sqrt(concentration) radians, with base elevations [18,55,32,73,24,61,40,16] degrees. Concentration is a geometry control, not an assigned dilution value. The receiver truth is [25,-12,20] m with a 30 m clock-range bias. The noise amplitude multiplies [0.4,-0.7,0.2,0.8,-0.5,0.1,-0.3,0.6]. A 30 m clock-range bias corresponds to about 100 nanoseconds. The solve starts at zero and repeatedly fits the actual range residual. Removing the known satellite radius from observations improves numerical conditioning; a rationalized distance difference avoids subtracting two nearly equal large distances. The fitted geometry determines the displayed dilution, while realized position error comes from the actual estimated coordinates.

## Predict before running

Predict whether removing the receiver clock unknown merely changes clock error or also biases position.

## Baseline workflow

Reset controls and leave the named fault disabled. Use Pseudorange noise = 2.0 m; Geometry concentration = 2.2 1. Write a prediction before executing. Read the response curve first, then explain it using the mechanism curve.

Position iteration plots Position (m) against Iteration (1). Its series are x, y, z. Fitted range residuals plots Residual (m) against Satellite index (1). Its series are Post-fit residual.

The computed default record is Position error: 1.77255 m; Clock-range error: 0.975552 m; Post-fit RMS: 0.925614 m; Computed position dilution: 2.71448 1. These values are a reproducible worked example, not acceptance thresholds for every slider setting. Retain units and parameter values when comparing another run. A displayed residual near machine precision should be interpreted with the stated model and numerical tolerance.

## Two one-variable sweeps

1. Increase noise amplitude from 2 to 10 m at fixed concentration. Compare position, clock and post-fit residual separately; deterministic errors need not equal amplitude times PDOP.

2. Increase concentration from 2.2 to 12 with noise fixed. Inspect the computed dilution and convergence trace. Closely grouped directions make some state combinations harder to distinguish.

Return to defaults between sweeps. Keep the other control fixed, record the changed quantity and identify an expected invariant. A control need not change every output; explain the model path through which it acts.

## Intentionally broken case

Broken mode omits the clock column and forces the fit to explain clock-biased measurements with three position coordinates.

Run the same selected controls with the fault enabled. Compare the curve shape as well as the numerical summary. The fault is a specific executed operation; a red warning or a changed mode flag would not by itself demonstrate its consequence.

## Recovery

Restore the fourth unknown, reset both controls and verify the post-fit residual and position/clock errors recover.

Repeat one previously saved nominal setting and check that its values and curves return. Recovery should restore the mechanism, not merely dismiss the warning.

## Limiting cases and invariants

Formal dilution assumes equal independent range variances and full column rank. Small residual alone does not prove accurate position. No atmosphere, ephemeris errors, Earth rotation, live receiver or operational accuracy claim is included.

## Independent evidence

The reference uses complex-step derivatives and a separate nonlinear least-squares solver on dimensionless rationalized range offsets. The production solver uses an analytic Jacobian and Gauss-Newton increments.

Five retained cases cover baseline, two single-control sweeps, the named fault and recovery. Expected values are generated independently; actual values come from the executable lesson. Absolute and relative tolerances remain 1e-8. Agreement checks the declared synthetic model, not empirical validity. MATLAB has not been executed and no MATLAB equivalence is claimed. Browser and container evidence are recorded separately from numerical evidence.

## Engineering review checklist

Check the declared coordinates, units and ordering before evaluating the result. Reconstruct at least one displayed value from retained state or geometric data. Identify which output changes in each sweep and which should remain invariant. Diagnose the named faulty operation, then demonstrate its recovery. Finally state the strongest claim supported by these observations and one claim that requires additional evidence.

## Common mistakes

Do not infer correctness from a changing headline alone. In this lesson, the critical limit is: Formal dilution assumes equal independent range variances and full column rank. Small residual alone does not prove accurate position. No atmosphere, ephemeris errors, Earth rotation, live receiver or operational accuracy claim is included.

Do not compare two runs after changing both controls and attribute the difference to one cause. Do not treat a near-zero floating-point residual as symbolic identity, or a finite sample sweep as a proof for all configurations. Keep the operation that creates the evidence separate from the interpretation assigned to it.

## Teach-back

Why is geometry concentration an input while PDOP is an output, and why does clock omission affect position?

Answer rationale: Concentration constructs lines of sight. Their design matrix determines PDOP. The omitted common range offset projects onto position columns, biasing the fitted position; it cannot generally be represented by a harmless display-only clock error.

Use the embedded Course checkpoint to collect a default record, a sweep, a faulty record and a recovered record. Explain the evidence to a colleague using the governing relation and units, then name the untested boundary. This is a self-assessment; no learner score is stored.

Related primary reference: [GNSS measurement modelling and estimation](https://gssc.esa.int/navipedia/index.php/GNSS_Measurements_Modelling).
