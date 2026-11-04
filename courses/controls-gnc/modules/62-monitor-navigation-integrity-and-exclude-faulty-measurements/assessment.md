## P62 evidence task

What evidence distinguishes a real exclusion/refit from multiplying the displayed residual by a fixed factor?

Before running: Predict whether a zero injected fault should always trigger exclusion and whether deleting one residual value is a valid refit.

Collect the default result, one single-control sweep, the named fault and recovery. Record controls and units beside the evidence.

Actual fit residuals plots Residual (m) against Satellite index (1). Its series are Before exclusion, Retained and refitted. Residual test plots Standardized magnitude (1) against Satellite index (1). Its series are Magnitude, Threshold.

### Reasoning rubric

- Model: use `r=y-h(xhat); leverage_i=H_i(H^T H)^-1 H_i^T` to reconstruct a quantity from the executed mechanism.
- Evidence: Increase fault magnitude from zero to 60 m with threshold fixed. Locate the alarm transition and inspect which row is excluded; zero fault should not force a deletion.
- Diagnosis: Broken mode leaves the alarm computation visible but suppresses exclusion, retaining all eight rows for the final fit.
- Recovery and scope: Disable the fault mode, restore defaults and confirm that the selected row disappears from the refitted residual series and state error decreases. State this limit: A residual test is geometry dependent and does not cover arbitrary multiple correlated faults. Exclusion can change formal uncertainty. A lower retained residual does not by itself establish integrity or real-world safety.

### Check your explanation

The retained row identities and count change, the state estimate changes, and residuals recomputed from retained measurements satisfy the new fit. A fixed factor cannot demonstrate those operations.

A complete answer includes the calculation or geometric construction, an observed comparison with units, fault/recovery evidence and the stated limitation. This is a self-assessment; no learner score is stored.


---

## P62 course checkpoint

**Predict and calculate.** Compare actual residual-based detection and exclusion with the refitted solution and alarm threshold.

Use `r=y-h(xhat); leverage_i=H_i(H^T H)^-1 H_i^T; z_i=r_i/(sigma sqrt(1-leverage_i)); alarm=max|z_i|>threshold; Remove selected row, then solve the retained nonlinear measurement problem again` with the conventions in the lesson. Work one baseline value by hand before running. The live controls are **Fault magnitude**, **Residual alarm threshold**.

**Collect evidence.** Save the default result, then perform the lesson's two one-variable sweeps separately. Record exact parameters, units, the `response` and `mechanism` plots, and the quantity that discriminates your prediction. Explain what stayed invariant as well as what changed.

**Fault and recovery.** Enable **Enable the intentionally broken case** at the same inputs. Explain which governing term is changed or omitted, show its effect on the actual trajectory, matrix or criterion, then disable it and use **Reset parameters**. Confirm recovery reproduces the baseline rather than merely a more favorable number.

### Expected reasoning

Redundancy permits inconsistency detection under stated geometry. Excluding a suspect row changes the fitted position and residual structure; distinguish a synthetic threshold from a certified protection level.

### Model boundary

No aviation integrity or protection-level certification is supported.

### Reasoning rubric

1. State the model, units, sign convention and independently worked value.
2. Explain both sweeps using this lesson's governing relation and recorded evidence.
3. Diagnose the actual fault mechanism and exact-input recovery.
4. Defend the stated boundary and link this result to the cumulative portfolio **A-INTEGRITY**.

This is authored self-assessment guidance. No learner completion, score or effectiveness result has been recorded.
