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
