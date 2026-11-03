## P67 course checkpoint

**Predict and calculate.** Reconcile actual survey position, estimated position, turn limits and stale-navigation hold events.

Use `position increment=v dt sinc(omega dt/2) [cos(psi+omega dt/2),sin(psi+omega dt/2)] m; omega=clip(1.5 wrap(heading_target-heading_estimate),-limit,limit) rad/s; GNSS age=t-last_fix; speed=0 when age>3 s; inertial gyro bias=0.3 deg/s` with the conventions in the lesson. Work one baseline value by hand before running. The live controls are **GNSS dropout**, **Turn-rate limit**.

**Collect evidence.** Save the default result, then perform the lesson's two one-variable sweeps separately. Record exact parameters, units, the `response` and `mechanism` plots, and the quantity that discriminates your prediction. Explain what stayed invariant as well as what changed.

**Fault and recovery.** Enable **Enable the intentionally broken case** at the same inputs. Explain which governing term is changed or omitted, show its effect on the actual trajectory, matrix or criterion, then disable it and use **Reset parameters**. Confirm recovery reproduces the baseline rather than merely a more favorable number.

### Expected reasoning

The planar survey applies LOS guidance and a bounded turn command to a simplified navigation estimate. GNSS age can trigger a hold even if cross-track error is small; inspect each requirement and the executed path.

### Model boundary

The capstone uses simplified planar position aiding, not raw pseudoranges or full GNSS/INS mechanization.

### Reasoning rubric

1. State the model, units, sign convention and independently worked value.
2. Explain both sweeps using this lesson's governing relation and recorded evidence.
3. Diagnose the actual fault mechanism and exact-input recovery.
4. Defend the stated boundary and link this result to the cumulative portfolio **A-CAP-ID**.

This is authored self-assessment guidance. No learner completion, score or effectiveness result has been recorded.


## Extended integration evidence

Read the **Integrated navigation** section and complete its prediction, two sweeps, numerical reconstruction, fault and recovery tasks. Keep the original component evidence above, then explain how the integrated sequence changes the scope. Record actual histories and units; a screenshot without the recurrence or frame reasoning is insufficient. No learner completion is recorded automatically.
