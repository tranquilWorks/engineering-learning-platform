## P20 course checkpoint

**Predict and calculate.** Choose between nominal and robust designs using their observed uncertainty/effort tradeoff.

Use `\dot v=-a v+b u,\quad u_K=K(r-v),\;K\in\{2,4\}; J_K=\int_0^{12}[(r-v_K)^2+0.05u_K^2]dt` with the conventions in the lesson. Work one baseline value by hand before running. The live controls are **Actual / nominal actuator gain**, **Actual / nominal drag**.

**Collect evidence.** Save the default result, then perform the lesson's two one-variable sweeps separately. Record exact parameters, units, the `response` and `mechanism` plots, and the quantity that discriminates your prediction. Explain what stayed invariant as well as what changed.

**Fault and recovery.** Enable **Enable the source broken case** at the same inputs. Explain which governing term is changed or omitted, show its effect on the actual trajectory, matrix or criterion, then disable it and use **Reset parameters**. Confirm recovery reproduces the baseline rather than merely a more favorable number.

### Expected reasoning

A conservative design can sacrifice nominal speed to maintain acceptable response under a declared mismatch. Compare both at the same physical plant and include effort or tracking penalties.

### Model boundary

No untested uncertainty set or universal robust certificate is implied.

### Reasoning rubric

1. State the model, units, sign convention and independently worked value.
2. Explain both sweeps using this lesson's governing relation and recorded evidence.
3. Diagnose the actual fault mechanism and exact-input recovery.
4. Defend the stated boundary and link this result to the cumulative portfolio **A-ROBUST**.

This is authored self-assessment guidance. No learner completion, score or effectiveness result has been recorded.
