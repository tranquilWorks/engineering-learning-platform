# P58 course checkpoint

## Predict and derive

Prove that later observations cannot change a fit computed only from the training prefix.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `F_y=X[C_front,C_rear]^T+epsilon`
- `theta_hat=argmin_theta ||X_train theta-y_train||_2`
- `RMSE_validation=sqrt(mean((X_validation theta_hat-y_validation)^2))`

## Controlled comparison

- `training_fraction`: 0.65 → 0.75. Hold the other controls at baseline; predict and explain the change before executing.
- `observation_noise_n`: 50 → 100. Hold the other controls at baseline; predict and explain the change before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

With 80 samples and training fraction 0.65, the first 52 rows estimate two stiffnesses and 28 rows remain unused until validation. Solve the two-column least-squares problem on that prefix and retain its parameter vector before examining later residuals. Perturb only held-out force observations: training coefficients and training error must remain unchanged while validation error may change. The broken mode leaks all rows into fitting and substitutes training error for validation error.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

A chronological synthetic split is stronger than in-sample fit but does not establish generalization across real tires, roads or operating regimes.

Competency links: VD-IDENTIFICATION-UNCERTAINTY. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
