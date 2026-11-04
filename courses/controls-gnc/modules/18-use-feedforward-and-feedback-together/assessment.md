## P18 course checkpoint

**Predict and calculate.** Show how feedforward changes nominal tracking while feedback reacts to disturbances and mismatch.

Use `u=u_{ff}+K_pe+K_d\dot e; u_{ff}=\ddot x_d` with the conventions in the lesson. Work one baseline value by hand before running. The live controls are **Feedforward scale**, **Feedback scale**.

**Collect evidence.** Save the default result, then perform the lesson's two one-variable sweeps separately. Record exact parameters, units, the `response` and `mechanism` plots, and the quantity that discriminates your prediction. Explain what stayed invariant as well as what changed.

**Fault and recovery.** Enable **Enable the source broken case** at the same inputs. Explain which governing term is changed or omitted, show its effect on the actual trajectory, matrix or criterion, then disable it and use **Reset parameters**. Confirm recovery reproduces the baseline rather than merely a more favorable number.

### Expected reasoning

Feedforward uses the reference and model to anticipate required effort; feedback corrects measured error. A perfect nominal trace with feedforward alone does not prove rejection of model error.

### Model boundary

The feedforward model and reference smoothness bound the claim.

### Reasoning rubric

1. State the model, units, sign convention and independently worked value.
2. Explain both sweeps using this lesson's governing relation and recorded evidence.
3. Diagnose the actual fault mechanism and exact-input recovery.
4. Defend the stated boundary and link this result to the cumulative portfolio **A-STATE**.

This is authored self-assessment guidance. No learner completion, score or effectiveness result has been recorded.
