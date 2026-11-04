## P34 course checkpoint

**Predict and calculate.** Hold both decay rates fixed and change the angle between the eigenvectors.

Use `x(t)=V exp(Lambda t) V^-1 x(0); Phi(t)=exp(A t); kappa(V)=sigma_max(V)/sigma_min(V)` with the conventions in the lesson. Work one baseline value by hand before running. The live controls are **Slow modal decay**, **Eigenvector separation angle**.

**Collect evidence.** Save the default result, then perform the lesson's two one-variable sweeps separately. Record exact parameters, units, the `response` and `mechanism` plots, and the quantity that discriminates your prediction. Explain what stayed invariant as well as what changed.

**Fault and recovery.** Enable **Enable the intentionally broken case** at the same inputs. Explain which governing term is changed or omitted, show its effect on the actual trajectory, matrix or criterion, then disable it and use **Reset parameters**. Confirm recovery reproduces the baseline rather than merely a more favorable number.

### Expected reasoning

Eigenvalues remain stable while nearly parallel eigenvectors amplify coordinate sensitivity and transient cancellation. A tiny reconstruction error is not proof that the modal basis is well conditioned.

### Model boundary

Roundoff reconstruction residual is not a physical state error bound.

### Reasoning rubric

1. State the model, units, sign convention and independently worked value.
2. Explain both sweeps using this lesson's governing relation and recorded evidence.
3. Diagnose the actual fault mechanism and exact-input recovery.
4. Defend the stated boundary and link this result to the cumulative portfolio **A-STATE**.

This is authored self-assessment guidance. No learner completion, score or effectiveness result has been recorded.
