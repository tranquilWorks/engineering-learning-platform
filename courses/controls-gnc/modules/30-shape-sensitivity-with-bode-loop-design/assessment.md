## P30 course checkpoint

**Predict and calculate.** Measure sensitivity, complementary sensitivity and effort together while shaping the loop.

Use `S=1/(1+L); T=L/(1+L); PS=P*S and CS=C*S` with the conventions in the lesson. Work one baseline value by hand before running. The live controls are **Loop gain**, **Lead zero**.

**Collect evidence.** Save the default result, then perform the lesson's two one-variable sweeps separately. Record exact parameters, units, the `response` and `mechanism` plots, and the quantity that discriminates your prediction. Explain what stayed invariant as well as what changed.

**Fault and recovery.** Enable **Enable the intentionally broken case** at the same inputs. Explain which governing term is changed or omitted, show its effect on the actual trajectory, matrix or criterion, then disable it and use **Reset parameters**. Confirm recovery reproduces the baseline rather than merely a more favorable number.

### Expected reasoning

For negative feedback S+T=1. Improving disturbance rejection in one frequency region can increase noise or effort elsewhere; an incorrect feedback denominator breaks the identity.

### Model boundary

Peak values are over the declared sampled frequency band.

### Reasoning rubric

1. State the model, units, sign convention and independently worked value.
2. Explain both sweeps using this lesson's governing relation and recorded evidence.
3. Diagnose the actual fault mechanism and exact-input recovery.
4. Defend the stated boundary and link this result to the cumulative portfolio **A-LOOP**.

This is authored self-assessment guidance. No learner completion, score or effectiveness result has been recorded.
