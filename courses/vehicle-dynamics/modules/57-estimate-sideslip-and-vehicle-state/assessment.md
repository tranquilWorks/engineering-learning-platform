# P57 course checkpoint

## Predict and derive

Derive fixed-gain covariance propagation and distinguish a conditional uncertainty calculation from empirical error.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `x_predict[k+1]=x_hat[k]+Delta_t(A x_hat[k]+B delta[k])`
- `innovation[k+1]=z[k+1]-x_predict[k+1]`
- `x_hat[k+1]=x_predict[k+1]+K innovation[k+1]`
- `Pminus=F P F^T+Q; Pplus=(I-L)Pminus(I-L)^T+L R L^T in declared normalized coordinates`

## Controlled comparison

- `observer_gain`: 0.35 → 0.65. Hold the other controls at baseline; predict and explain the change before executing.
- `measurement_noise`: 0.08 → 0.15. Hold the other controls at baseline; predict and explain the change before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

In normalized coordinates [beta/(1 rad),r/(1 rad/s),bias/(1 rad)], prediction is Pminus=F*P*F transpose+Q. For fixed gain L and direct measurements, posterior is (I-L)*Pminus*(I-L) transpose+L*R*L transpose. Both plant propagation and measurement noise are necessary; shrinking P only by I-L is not a covariance update. Increasing noise must increase the conditional posterior even if the chosen gain is unchanged. Compare state histories and actual truth error separately.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

L is a user-selected fixed gain, not an optimal Kalman gain. The correlated deterministic fixture does not satisfy the independent-noise assumptions of the conditional covariance, and the sign fault adds unmodeled bias.

Competency links: VD-STATE-RECONSTRUCTION. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
