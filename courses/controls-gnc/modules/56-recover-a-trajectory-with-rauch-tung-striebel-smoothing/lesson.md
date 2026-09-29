# Recover a Trajectory with RTS Smoothing



## Model and equations

`x[k+1]=x[k]+w[k]; y[k]=x[k]+v[k]; Q=q m²; R=r m²`

`K=Pminus/(Pminus+r); Pplus=(1-K)²Pminus+K²r`

`C[k]=Pf[k]/Pminus[k+1]; ms[k]=mf[k]+C[k](ms[k+1]-mminus[k+1])`

`Ps[k]=Pf[k]+C[k]²(Ps[k+1]-Pminus[k+1])`

The state is scalar position in metres, sampled every 0.25 seconds. There are 41 retained measurements. The initial prior mean is zero and its variance is 1 m². Process variance is per sample, not per second. The deterministic truth increments use sqrt(q)[0.7 sin(0.6k)+0.2 cos(1.1k)], and measurement noise uses sqrt(r)[0.7 cos(1.4k)+0.2 sin(0.2k)]. These sequences exercise the estimator without pretending to be random draws establishing statistical coverage. At q=0.08 and r=0.4, the first gain is 1/1.4=0.714286 and the first posterior variance is 0.285714 m². The next prediction adds q, giving 0.365714 m². The backward gain therefore begins with a ratio of retained covariances, not a chosen percentage reduction. Every corrected mean uses future information through the adjacent smoothed estimate.

## Predict before running

Predict which sample cannot benefit from the backward pass, and whether smaller model covariance guarantees smaller error in every realization.

## Baseline workflow

Reset controls and leave the named fault disabled. Use Process variance = 0.08 m^2; Measurement variance = 0.4 m^2. Write a prediction before executing. Read the response curve first, then explain it using the mechanism curve.

Executed estimates plots Position (m) against Time (s). Its series are Synthetic truth, Forward filter, Reported smoother. Filter/smoother covariance plots Position variance (m²) against Time (s). Its series are Filtered covariance, Reported smoothed covariance.

The computed default record is Mean filtered variance: 0.148688 m^2; Mean reported smoothed variance: 0.0911881 m^2; Mean variance reduction: 0.0574995 m^2; Reported trajectory RMSE: 0.176841 m. These values are a reproducible worked example, not acceptance thresholds for every slider setting. Retain units and parameter values when comparing another run. A displayed residual near machine precision should be interpreted with the stated model and numerical tolerance.

## Two one-variable sweeps

1. Increase process variance from 0.08 to 0.5 m² while holding measurement variance at 0.4 m². Compare the entire forward and backward variance curves; large process uncertainty weakens the coupling between adjacent states.

2. Increase measurement variance from 0.4 to 2 m² with process variance fixed. Explain why the model trusts each individual measurement less. Compare the estimated trajectory as well as the average covariance.

Return to defaults between sweeps. Keep the other control fixed, record the changed quantity and identify an expected invariant. A control need not change every output; explain the model path through which it acts.

## Intentionally broken case

Broken mode skips the backward recursion and reports the forward filter as the smoother. Both controls still generate the data and filter covariance.

Run the same selected controls with the fault enabled. Compare the curve shape as well as the numerical summary. The fault is a specific executed operation; a red warning or a changed mode flag would not by itself demonstrate its consequence.

## Recovery

Disable the fault and reset the two variances. Confirm the last means and variances remain equal while earlier covariance usually falls.

Repeat one previously saved nominal setting and check that its values and curves return. Recovery should restore the mechanism, not merely dismiss the warning.

## Limiting cases and invariants

At the final sample no future measurement exists, so filter and smoother coincide. Positive q and r maintain positive covariance. A smoother uses a completed record and is not causal real-time estimation. Model covariance and realized RMSE answer different questions.

## Independent evidence

An independently conditioned joint Gaussian trajectory uses C[i,j]=1+q min(i,j). Its posterior covariance is C-C(C+rI)^-1 C; prefix conditioning supplies the filtered variances. It does not import the production recursion.

Five retained cases cover baseline, two single-control sweeps, the named fault and recovery. Expected values are generated independently; actual values come from the executable lesson. Absolute and relative tolerances remain 1e-8. Agreement checks the declared synthetic model, not empirical validity. MATLAB has not been executed and no MATLAB equivalence is claimed. Browser and container evidence are recorded separately from numerical evidence.

## Engineering review checklist

Check the declared coordinates, units and ordering before evaluating the result. Reconstruct at least one displayed value from retained state or geometric data. Identify which output changes in each sweep and which should remain invariant. Diagnose the named faulty operation, then demonstrate its recovery. Finally state the strongest claim supported by these observations and one claim that requires additional evidence.

## Common mistakes

Do not infer correctness from a changing headline alone. In this lesson, the critical limit is: At the final sample no future measurement exists, so filter and smoother coincide. Positive q and r maintain positive covariance. A smoother uses a completed record and is not causal real-time estimation. Model covariance and realized RMSE answer different questions.

Do not compare two runs after changing both controls and attribute the difference to one cause. Do not treat a near-zero floating-point residual as symbolic identity, or a finite sample sweep as a proof for all configurations. Keep the operation that creates the evidence separate from the interpretation assigned to it.

## Teach-back

Why must the final smoother covariance equal the filter covariance, and why is a fixed 35 percent improvement incorrect?

Answer rationale: The backward recursion is initialized by the final filtered pair. Earlier reductions depend on the retained covariance ratios and future observations; no universal percentage follows. A lower posterior covariance describes the model distribution, not guaranteed improvement for every observed truth trace.

Use the embedded Course checkpoint to collect a default record, a sweep, a faulty record and a recovered record. Explain the evidence to a colleague using the governing relation and units, then name the untested boundary. This is a self-assessment; no learner score is stored.
