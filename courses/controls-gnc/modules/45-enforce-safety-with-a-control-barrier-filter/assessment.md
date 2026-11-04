## P45 evidence task

Derive h[k+1]>=(1−alpha*dt)h[k] and explain why this browser range satisfies it. What physical effects are excluded?

Before running: Should the safe trajectory cross h=0 if every command is reevaluated? State the sample-period condition your answer requires.

Collect three records: the default plots and metrics; one change from the stated sweeps with the other control fixed; and the fault followed by restored defaults. Record parameter values and units beside each observation.

Safety margin over time includes the zero boundary. State-dependent barrier filter shows applied and nominal velocities and u+alpha*h. A nonnegative residual certifies the sampled step under the declared integrator assumptions.

### Reasoning rubric

- Model: use `h=x-x_min; dh/dt=u; u_nom=-v_close` to explain the observed quantity rather than repeating a metric label.
- Evidence: For alpha*dt<=1, nonnegative current clearance implies nonnegative next clearance. Show where your plot or numerical record tests this statement.
- Diagnosis: Broken mode bypasses the filter and continuously applies the selected nominal closing speed. At the default speed, clearance crosses zero within three seconds; slower closing can stay positive throughout this finite window. No control setting is secretly replaced. Identify the measured consequence in your record.
- Recovery and scope: Disable broken mode and reset controls. Inspect the entire clearance history, not just its first sample, and verify a nonnegative minimum barrier residual. State this limit: If nominal velocity already satisfies the barrier, intervention is zero; this does not remove the need to reevaluate it later.

### Check your explanation

Substitute u>=−alpha*h into the Euler integrator. Here alpha*dt<=0.08, so the multiplier stays nonnegative. Delay, disturbances and actuator lag are excluded; the demonstration does not certify a real robot.

A complete answer includes the calculation or recurrence, an observed comparison with units, fault/recovery evidence and the stated limitation. Revisit the lesson if the explanation depends only on a changing headline number. This is a self-assessment; no learner score is stored.


---

## P45 course checkpoint

**Predict and calculate.** Compare a barrier condition evaluated along the actual state trajectory with the nominal command.

Use `h=x-x_min; dh/dt=u; u_nom=-v_close; u[k]=max(u_nom,-alpha*h[k]); h[k+1]=h[k]+dt*u[k]; dt=0.01 s; h[k+1]>=(1-alpha*dt)*h[k]` with the conventions in the lesson. Work one baseline value by hand before running. The live controls are **Barrier gain**, **Nominal closing speed**.

**Collect evidence.** Save the default result, then perform the lesson's two one-variable sweeps separately. Record exact parameters, units, the `response` and `mechanism` plots, and the quantity that discriminates your prediction. Explain what stayed invariant as well as what changed.

**Fault and recovery.** Enable **Enable the intentionally broken case** at the same inputs. Explain which governing term is changed or omitted, show its effect on the actual trajectory, matrix or criterion, then disable it and use **Reset parameters**. Confirm recovery reproduces the baseline rather than merely a more favorable number.

### Expected reasoning

A safety filter must recompute its constraint at each evolving state. Check feasibility and realized barrier margin rather than assuming a projected command guarantees all future motion.

### Model boundary

The finite sampled barrier model does not certify arbitrary continuous or delayed plants.

### Reasoning rubric

1. State the model, units, sign convention and independently worked value.
2. Explain both sweeps using this lesson's governing relation and recorded evidence.
3. Diagnose the actual fault mechanism and exact-input recovery.
4. Defend the stated boundary and link this result to the cumulative portfolio **A-CONSTRAINTS**.

This is authored self-assessment guidance. No learner completion, score or effectiveness result has been recorded.
