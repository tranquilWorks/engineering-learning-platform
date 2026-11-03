## P61 evidence task

Why can both normal and broken cases show a smaller post-update sigma while only one corrects position?

Before running: Predict what happens if covariance is updated but the nominal navigation state never receives the correction.

Collect the default result, one single-control sweep, the named fault and recovery. Record controls and units beside the evidence.

Injected navigation state plots Position (m) against Time (s). Its series are Estimated position, Truth. Error and formal sigma plots Position error (m) against Time (s). Its series are Actual error, Formal sigma.

### Reasoning rubric

- Model: use `delta=[position error, velocity error, accelerometer bias error]` to reconstruct a quantity from the executed mechanism.
- Evidence: Increase GNSS interval from 1 to 10 seconds while holding bias intensity fixed. Observe longer propagation gaps and distinguish pre-update from post-update uncertainty.
- Diagnosis: Broken mode computes updates and shrinks covariance but discards the state correction instead of injecting it.
- Recovery and scope: Restore injection and reset both controls. Check actual position error and bias estimate, not only the covariance drop. State this limit: The terminal sigma can fall while actual error remains large in the fault. Additive reset leaves covariance coordinates unchanged. This lesson does not implement attitude, Earth frames, lever arms or a complete strapdown INS.

### Check your explanation

The covariance recurrence is independent of the realized innovation for this linear model. State injection uses that innovation; dropping it makes the reported uncertainty inconsistent with the executed estimator.

A complete answer includes the calculation or geometric construction, an observed comparison with units, fault/recovery evidence and the stated limitation. This is a self-assessment; no learner score is stored.


---

## P61 course checkpoint

**Predict and calculate.** Trace prior covariance, state-error injection and covariance reset in the actual one-axis filter.

Use `delta=[position error, velocity error, accelerometer bias error]; F=[[1,dt,-dt²/2],[0,1,-dt],[0,0,1]]; Pminus=F P F^T+Q; K=Pminus H^T/(H Pminus H^T+R); nominal+=K innovation; delta_reset=0; Pplus=(I-KH)Pminus(I-KH)^T+K R K^T` with the conventions in the lesson. Work one baseline value by hand before running. The live controls are **GNSS update interval**, **Bias random walk**.

**Collect evidence.** Save the default result, then perform the lesson's two one-variable sweeps separately. Record exact parameters, units, the `response` and `mechanism` plots, and the quantity that discriminates your prediction. Explain what stayed invariant as well as what changed.

**Fault and recovery.** Enable **Enable the intentionally broken case** at the same inputs. Explain which governing term is changed or omitted, show its effect on the actual trajectory, matrix or criterion, then disable it and use **Reset parameters**. Confirm recovery reproduces the baseline rather than merely a more favorable number.

### Expected reasoning

An error estimate must be injected into the nominal state as well as propagated in covariance. A shrinking covariance with an uncorrected nominal error is overconfidence, not successful navigation.

### Model boundary

This one-axis formulation does not implement a complete inertial ESKF.

### Reasoning rubric

1. State the model, units, sign convention and independently worked value.
2. Explain both sweeps using this lesson's governing relation and recorded evidence.
3. Diagnose the actual fault mechanism and exact-input recovery.
4. Defend the stated boundary and link this result to the cumulative portfolio **A-NAVIGATION**.

This is authored self-assessment guidance. No learner completion, score or effectiveness result has been recorded.
