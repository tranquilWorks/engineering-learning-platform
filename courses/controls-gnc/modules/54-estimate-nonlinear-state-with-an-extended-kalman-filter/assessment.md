## P54 course checkpoint

**Predict and calculate.** Calculate the actual EKF state update and nonlinear residual from the selected prior.

Use `h(x)=x^2,\quad H=2\hat x^-,\quad \nu=z-h(\hat x^-); K=P^-H/(H^2P^-+R),\quad \hat x^+=\hat x^-+K\nu; P^+=(1-KH)^2P^-+K^2R` with the conventions in the lesson. Work one baseline value by hand before running. The live controls are **Prior standard deviation**, **Linearization state**.

**Collect evidence.** Save the default result, then perform the lesson's two one-variable sweeps separately. Record exact parameters, units, the `response` and `mechanism` plots, and the quantity that discriminates your prediction. Explain what stayed invariant as well as what changed.

**Fault and recovery.** Enable **Enable the intentionally broken case** at the same inputs. Explain which governing term is changed or omitted, show its effect on the actual trajectory, matrix or criterion, then disable it and use **Reset parameters**. Confirm recovery reproduces the baseline rather than merely a more favorable number.

### Expected reasoning

Linearize the measurement at the prior, compute innovation and gain, and update both state and covariance. A zero Jacobian loses first-order information; prior variance is not the nonlinear Taylor residual.

### Model boundary

This single scalar update does not resolve the global sign ambiguity of squared observations.

### Reasoning rubric

1. State the model, units, sign convention and independently worked value.
2. Explain both sweeps using this lesson's governing relation and recorded evidence.
3. Diagnose the actual fault mechanism and exact-input recovery.
4. Defend the stated boundary and link this result to the cumulative portfolio **A-NONLINEAR-EST**.

This is authored self-assessment guidance. No learner completion, score or effectiveness result has been recorded.


## Extended integration evidence

Read the **Recursive integration** section and complete its prediction, two sweeps, numerical reconstruction, fault and recovery tasks. Keep the original component evidence above, then explain how the integrated sequence changes the scope. Record actual histories and units; a screenshot without the recurrence or frame reasoning is insufficient. No learner completion is recorded automatically.
