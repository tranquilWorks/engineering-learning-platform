## P55 evidence task

At alpha=1, why does removing the central covariance correction leave the mean correct but reduce variance to zero?

Before running: Does a negative central mean weight necessarily invalidate the transform? Try alpha below one and compare the computed moments with the Gaussian formulas.

Collect three records: the default plots and metrics; one change from the stated sweeps with the other control fixed; and the fault followed by restored defaults. Record parameter values and units beside each observation.

Actual sigma-point transform displays the nonlinear curve and the three transformed points. Weighted variance contributions shows what each point adds to the covariance calculation. The metrics expose computed moments, their errors, minimum mean weight and covariance-weight sum.

### Reasoning rubric

- Model: use `x~N(0,sigma^2); y=x^2; E[y]=sigma^2; Var[y]=2*sigma^4` to explain the observed quantity rather than repeating a metric label.
- Evidence: Mean weights sum to one; covariance weights generally do not. Show where your plot or numerical record tests this statement.
- Diagnosis: Broken mode omits the Gaussian covariance correction and reuses mean weights for covariance. Mean remains correct, but variance becomes (alpha²−1)*sigma⁴: zero at alpha=1 and negative for alpha<1. Identify the measured consequence in your record.
- Recovery and scope: Restore the beta=2 covariance correction and reset both controls. Check both computed moments against analytic Gaussian values; do not reject a transform solely because its central mean weight is negative. State this limit: Exactness here concerns a zero-mean Gaussian squared map, not every nonlinear function or a full recursive UKF.

### Check your explanation

The two off-center transformed values equal the mean, so their variance contributions vanish. The center maps to zero, differs from mean by sigma² and contributes 2*sigma⁴ only through the covariance correction. Its mean weight is zero.

A complete answer includes the calculation or recurrence, an observed comparison with units, fault/recovery evidence and the stated limitation. Revisit the lesson if the explanation depends only on a changing headline number. This is a self-assessment; no learner score is stored.
