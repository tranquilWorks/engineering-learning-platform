## P60 evidence task

Why is geometry concentration an input while PDOP is an output, and why does clock omission affect position?

Before running: Predict whether removing the receiver clock unknown merely changes clock error or also biases position.

Collect the default result, one single-control sweep, the named fault and recovery. Record controls and units beside the evidence.

Position iteration plots Position (m) against Iteration (1). Its series are x, y, z. Fitted range residuals plots Residual (m) against Satellite index (1). Its series are Post-fit residual.

### Reasoning rubric

- Model: use `rho_i=||s_i-x||+b+epsilon_i; b=c delta_t in metres` to reconstruct a quantity from the executed mechanism.
- Evidence: Increase noise amplitude from 2 to 10 m at fixed concentration. Compare position, clock and post-fit residual separately; deterministic errors need not equal amplitude times PDOP.
- Diagnosis: Broken mode omits the clock column and forces the fit to explain clock-biased measurements with three position coordinates.
- Recovery and scope: Restore the fourth unknown, reset both controls and verify the post-fit residual and position/clock errors recover. State this limit: Formal dilution assumes equal independent range variances and full column rank. Small residual alone does not prove accurate position. No atmosphere, ephemeris errors, Earth rotation, live receiver or operational accuracy claim is included.

### Check your explanation

Concentration constructs lines of sight. Their design matrix determines PDOP. The omitted common range offset projects onto position columns, biasing the fitted position; it cannot generally be represented by a harmless display-only clock error.

A complete answer includes the calculation or geometric construction, an observed comparison with units, fault/recovery evidence and the stated limitation. This is a self-assessment; no learner score is stored.


---

## P60 course checkpoint

**Predict and calculate.** Separate position and clock error in a nonlinear synthetic pseudorange solution.

Use `rho_i=||s_i-x||+b+epsilon_i; b=c delta_t in metres; H_i=[(x-s_i)^T/||x-s_i||,1]; delta=argmin ||H delta-r||²; PDOP=sqrt(trace((H^T H)^-1[0:3,0:3]))` with the conventions in the lesson. Work one baseline value by hand before running. The live controls are **Pseudorange noise**, **Geometry concentration**.

**Collect evidence.** Save the default result, then perform the lesson's two one-variable sweeps separately. Record exact parameters, units, the `response` and `mechanism` plots, and the quantity that discriminates your prediction. Explain what stayed invariant as well as what changed.

**Fault and recovery.** Enable **Enable the intentionally broken case** at the same inputs. Explain which governing term is changed or omitted, show its effect on the actual trajectory, matrix or criterion, then disable it and use **Reset parameters**. Confirm recovery reproduces the baseline rather than merely a more favorable number.

### Expected reasoning

Each range measurement contains geometry and a common clock term. Omitting that term forces the solver to absorb timing error into position; residual size alone does not identify the error source.

### Model boundary

Synthetic geometry and deterministic noise are not real GNSS qualification.

### Reasoning rubric

1. State the model, units, sign convention and independently worked value.
2. Explain both sweeps using this lesson's governing relation and recorded evidence.
3. Diagnose the actual fault mechanism and exact-input recovery.
4. Defend the stated boundary and link this result to the cumulative portfolio **A-NAVIGATION**.

This is authored self-assessment guidance. No learner completion, score or effectiveness result has been recorded.
