# P33 course checkpoint

## Predict and derive

Distinguish residual containment from a conditional prediction interval and prove that validation rows were not fitted.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `theta_hat=argmin sum_train(y-theta*x)^2`
- `r_i=y_i-theta_hat*x_i`
- `z_i=r_i/sigma`
- `coverage=mean(|z_i|<=1.96)`

## Controlled comparison

- `observation_sigma_n`: 80 → 220. Hold the other controls at baseline; predict and explain the change before executing.
- `validation_fraction`: 0.35 → 0.6. Hold the other controls at baseline; predict and explain the change before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

In the one-parameter model y=theta*x+noise, theta_hat=sum(x*y)/sum(x²) on the training prefix only. With declared independent noise sigma, Var(theta_hat)=sigma²/sum(x_train²), and prediction variance at a held-out x is sigma²+x²*Var(theta_hat). The second term widens the predictive band beyond a residual-only 1.96*sigma threshold. Doubling sigma doubles interval widths. Record both containment fractions and the split; fitting validation rows and shrinking sigma changes two distinct assumptions.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

The fixture noise is deterministic and correlated. Gaussian conditional formulas do not establish empirical 95 percent coverage, nor include model-form error.

Competency links: VD-TIRE-LONG, VD-TIRE-LAT, VD-IDENTIFICATION-UNCERTAINTY. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
