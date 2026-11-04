## P42 evidence task

Why can peak |z| exceed the command limit? What additional evidence is required before reporting a recovery time?

Before running: Can a saturated actuator hide a requested-command jump? Compare the applied switch bump with the integral and requested-command histories.

Collect three records: the default plots and metrics; one change from the stated sweeps with the other control fixed; and the fault followed by restored defaults. Record parameter values and units beside each observation.

The first plot shows output and reference. The second retains actual z, raw command and saturated command. Peak integral state is max|z| in both modes. Recovery requires the output to remain within 0.04 of 0.2 for the rest of the window; an unobserved recovery is labeled a censored five-second lower bound.

### Reasoning rubric

- Model: use `x[k+1]=x[k]+0.01*(-x[k]+u[k])` to explain the observed quantity rather than repeating a metric label.
- Evidence: At k_aw=0 the healthy switch is still bumpless, but no back-calculation acts afterward. Show where your plot or numerical record tests this statement.
- Diagnosis: Broken mode starts z at zero on switching and disables back-calculation. It still obeys actuator limits, so the integrator can accumulate error that the actuator cannot realize. Identify the measured consequence in your record.
- Recovery and scope: Disable broken mode, restore gain 4/s and limit 1.2, and verify a zero applied bump plus the actual integral history. Check the recovery-observed indicator before quoting a settling time. State this limit: A peak command is not a peak integral state, and a censored time is not an observed recovery.

### Check your explanation

Only u is clipped; z is controller memory and can be much larger. Inspect recovery-observed and ensure all later samples stay inside the stated band. A censored lower bound cannot be presented as a successful recovery.

A complete answer includes the calculation or recurrence, an observed comparison with units, fault/recovery evidence and the stated limitation. Revisit the lesson if the explanation depends only on a changing headline number. This is a self-assessment; no learner score is stored.


---

## P42 course checkpoint

**Predict and calculate.** Predict the command jump when switching from manual to automatic control and explain the recovery criterion.

Use `x[k+1]=x[k]+0.01*(-x[k]+u[k]); u_raw=2*(r-x)+z; u=clip(u_raw,-limit,limit); z[k+1]=z[k]+0.01*(1.2*(r-x)+k_aw*(u-u_raw))` with the conventions in the lesson. Work one baseline value by hand before running. The live controls are **Back-calculation gain**, **Actuator limit**.

**Collect evidence.** Save the default result, then perform the lesson's two one-variable sweeps separately. Record exact parameters, units, the `response` and `mechanism` plots, and the quantity that discriminates your prediction. Explain what stayed invariant as well as what changed.

**Fault and recovery.** Enable **Enable the intentionally broken case** at the same inputs. Explain which governing term is changed or omitted, show its effect on the actual trajectory, matrix or criterion, then disable it and use **Reset parameters**. Confirm recovery reproduces the baseline rather than merely a more favorable number.

### Expected reasoning

Bumpless transfer initializes integral state to match the existing command. Anti-windup then uses the actual saturation discrepancy; a recovery beyond the finite observation window is censored, not an observed success.

### Model boundary

A censored recovery is a lower bound on time, not an exact settling measurement.

### Reasoning rubric

1. State the model, units, sign convention and independently worked value.
2. Explain both sweeps using this lesson's governing relation and recorded evidence.
3. Diagnose the actual fault mechanism and exact-input recovery.
4. Defend the stated boundary and link this result to the cumulative portfolio **A-DIGITAL**.

This is authored self-assessment guidance. No learner completion, score or effectiveness result has been recorded.
