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
