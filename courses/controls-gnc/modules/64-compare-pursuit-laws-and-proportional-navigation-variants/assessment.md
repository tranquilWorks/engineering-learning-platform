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


---

## P64 course checkpoint

**Predict and calculate.** Explain the different moving-beacon guidance paths using the actual relative geometry.

Use `Rdot=r·vrel/||r||; lambda_dot=cross(r,vrel)/||r||²; a_PN=N max(-Rdot,0) lambda_dot; heading_dot=a/3; a_pursuit=v_p k_heading wrap(lambda-heading); v_p=3 m/s; k_heading=1.5/s; a_augmented=a_PN+(N/2) v_beacon omega_beacon cos(heading_beacon-heading); v_beacon=1 m/s` with the conventions in the lesson. Work one baseline value by hand before running. The live controls are **PN navigation constant**, **Beacon turn rate**.

**Collect evidence.** Save the default result, then perform the lesson's two one-variable sweeps separately. Record exact parameters, units, the `response` and `mechanism` plots, and the quantity that discriminates your prediction. Explain what stayed invariant as well as what changed.

**Fault and recovery.** Enable **Enable the intentionally broken case** at the same inputs. Explain which governing term is changed or omitted, show its effect on the actual trajectory, matrix or criterion, then disable it and use **Reset parameters**. Confirm recovery reproduces the baseline rather than merely a more favorable number.

### Expected reasoning

Closing speed, line-of-sight rate and turning geometry govern the trajectory. Compare bounded civilian synthetic paths under the same initial conditions rather than treating a smaller endpoint distance as universal superiority.

### Model boundary

These synthetic beacon comparisons do not validate an operational pursuit system.

### Reasoning rubric

1. State the model, units, sign convention and independently worked value.
2. Explain both sweeps using this lesson's governing relation and recorded evidence.
3. Diagnose the actual fault mechanism and exact-input recovery.
4. Defend the stated boundary and link this result to the cumulative portfolio **A-GUIDANCE**.

This is authored self-assessment guidance. No learner completion, score or effectiveness result has been recorded.
