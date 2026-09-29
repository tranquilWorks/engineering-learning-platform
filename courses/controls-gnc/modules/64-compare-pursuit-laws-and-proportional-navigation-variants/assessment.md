## P64 evidence task

Why can two laws have the same one-metre minimum yet different guidance performance?

Before running: Predict how reversing the measured line-of-sight rate changes the initial PN command and the integrated path.

Collect the default result, one single-control sweep, the named fault and recovery. Record controls and units beside the evidence.

Moving-beacon separation plots Separation (m) against Time (s). Its series are pursuit, pn, augmented. Executed lateral commands plots Acceleration (m/s²) against Time (s). Its series are pursuit, pn, augmented.

### Reasoning rubric

- Model: use `Rdot=r·vrel/||r||; lambda_dot=cross(r,vrel)/||r||²` to reconstruct a quantity from the executed mechanism.
- Evidence: Increase navigation constant from 1 to 6 while holding beacon turn fixed. Compare command demand, actual capture duration and separation history. Do not infer universal performance from one sampled minimum.
- Diagnosis: Broken mode reverses the LOS-rate sign in PN and augmented PN while preserving both controls and the pursuit comparison.
- Recovery and scope: Restore the rate sign and defaults. Confirm the initial command reverses back and inspect the resulting trajectory duration and separation curve. State this limit: Capture is a one-metre event, not zero-distance contact. Closest approach is sampled. No actuator saturation, collision planning, sensor noise or universal capture guarantee is included. A comparison ending early has a shorter observation window.

### Check your explanation

Both may reach the declared capture event, which terminates their integrations at the same radius. Capture time, command demand and trajectory history still differ; the threshold is not a fabricated miss metric.

A complete answer includes the calculation or geometric construction, an observed comparison with units, fault/recovery evidence and the stated limitation. This is a self-assessment; no learner score is stored.
