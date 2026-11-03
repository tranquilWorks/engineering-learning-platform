## P14 course checkpoint

**Predict and calculate.** Explain why a longer observation window cannot restore a fundamentally missing measured direction.

Use `\mathcal O=[C;CA]; y(t)=g(x_0+v_0t)` with the conventions in the lesson. Work one baseline value by hand before running. The live controls are **Sensor gain**, **Observation window**.

**Collect evidence.** Save the default result, then perform the lesson's two one-variable sweeps separately. Record exact parameters, units, the `response` and `mechanism` plots, and the quantity that discriminates your prediction. Explain what stayed invariant as well as what changed.

**Fault and recovery.** Enable **Enable the source broken case** at the same inputs. Explain which governing term is changed or omitted, show its effect on the actual trajectory, matrix or criterion, then disable it and use **Reset parameters**. Confirm recovery reproduces the baseline rather than merely a more favorable number.

### Expected reasoning

Observability involves C, CA and the state dynamics. Longer data may improve an existing weak direction, but identical or absent sensitivities retain a null space.

### Model boundary

A nominal rank test is not noise-qualified estimation accuracy.

### Reasoning rubric

1. State the model, units, sign convention and independently worked value.
2. Explain both sweeps using this lesson's governing relation and recorded evidence.
3. Diagnose the actual fault mechanism and exact-input recovery.
4. Defend the stated boundary and link this result to the cumulative portfolio **A-MODELING**.

This is authored self-assessment guidance. No learner completion, score or effectiveness result has been recorded.
