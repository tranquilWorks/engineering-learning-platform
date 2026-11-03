## P51 evidence task

At lambda=1, why does the broken covariance no longer shrink, and why is the estimate still wrong?

Before running: What should happen to covariance when excitation vanishes and lambda<1? Decide before enabling the broken case.

Collect three records: the default plots and metrics; one change from the stated sweeps with the other control fixed; and the fault followed by restored defaults. Record parameter values and units beside each observation.

Recursive parameter estimate displays each computed update and known truth. Covariance and missing excitation compares reported P with the correct zero-excitation evolution. Information rate is the actual sum of squared regressors divided by ten seconds.

### Reasoning rubric

- Model: use `g[k]=P[k-1]*phi[k]/(lambda+phi[k]^2*P[k-1])` to explain the observed quantity rather than repeating a metric label.
- Evidence: At lambda=1, recursive estimates match regularized batch least squares with prior information 1/P0. Show where your plot or numerical record tests this statement.
- Diagnosis: Broken mode sets the actual regressor to zero and uses the incorrect covariance update lambda*P. The parameter stays at zero while the reported covariance shrinks for lambda<1. The selected forgetting factor remains active. Identify the measured consequence in your record.
- Recovery and scope: Restore excitation and the correct covariance recurrence, then reset the controls. Check estimate motion is accompanied by nonzero regressors and actual information accumulation. State this limit: The deterministic disturbance is explicitly 0.01*sin(0.73*k); observed error is not a statistical convergence guarantee.

### Check your explanation

Multiplication by one leaves P fixed, so this particular false-confidence symptom disappears. The zero regressor still gives zero gain and no information, leaving theta=0 instead of the true value one.

A complete answer includes the calculation or recurrence, an observed comparison with units, fault/recovery evidence and the stated limitation. Revisit the lesson if the explanation depends only on a changing headline number. This is a self-assessment; no learner score is stored.


---

## P51 course checkpoint

**Predict and calculate.** Relate recursive least squares estimates and covariance to an independently weighted batch fit.

Use `g[k]=P[k-1]*phi[k]/(lambda+phi[k]^2*P[k-1]); theta[k]=theta[k-1]+g[k]*(y[k]-phi[k]*theta[k-1]); P[k]=(P[k-1]-g[k]*phi[k]*P[k-1])/lambda` with the conventions in the lesson. Work one baseline value by hand before running. The live controls are **Forgetting factor**, **Excitation level**.

**Collect evidence.** Save the default result, then perform the lesson's two one-variable sweeps separately. Record exact parameters, units, the `response` and `mechanism` plots, and the quantity that discriminates your prediction. Explain what stayed invariant as well as what changed.

**Fault and recovery.** Enable **Enable the intentionally broken case** at the same inputs. Explain which governing term is changed or omitted, show its effect on the actual trajectory, matrix or criterion, then disable it and use **Reset parameters**. Confirm recovery reproduces the baseline rather than merely a more favorable number.

### Expected reasoning

Each RLS update uses a gain and covariance recursion. Forgetting changes the data weights; small covariance without sufficient excitation is not trustworthy certainty about the true parameters.

### Model boundary

The retained model and excitation family limit the adaptation claim.

### Reasoning rubric

1. State the model, units, sign convention and independently worked value.
2. Explain both sweeps using this lesson's governing relation and recorded evidence.
3. Diagnose the actual fault mechanism and exact-input recovery.
4. Defend the stated boundary and link this result to the cumulative portfolio **A-IDENTIFICATION**.

This is authored self-assessment guidance. No learner completion, score or effectiveness result has been recorded.
