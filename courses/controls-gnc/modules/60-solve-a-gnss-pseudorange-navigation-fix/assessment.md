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
