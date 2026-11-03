## P05 course checkpoint

**Predict and calculate.** Explain how proportional gain moves response speed and residual tracking error in the actual loop.

Use `\tau\dot y=-y+G K_p(r-y); y_{ss}=GK_p r/(1+GK_p)` with the conventions in the lesson. Work one baseline value by hand before running. The live controls are **Proportional gain**, **Plant time constant**.

**Collect evidence.** Save the default result, then perform the lesson's two one-variable sweeps separately. Record exact parameters, units, the `response` and `mechanism` plots, and the quantity that discriminates your prediction. Explain what stayed invariant as well as what changed.

**Fault and recovery.** Enable **Enable the source broken case** at the same inputs. Explain which governing term is changed or omitted, show its effect on the actual trajectory, matrix or criterion, then disable it and use **Reset parameters**. Confirm recovery reproduces the baseline rather than merely a more favorable number.

### Expected reasoning

Closing the loop changes the denominator as well as the reference response. A smaller steady error can coexist with larger transient effort, and incorrect feedback sign can destabilize the state.

### Model boundary

A nominal proportional loop is not an integral servo or robust performance proof.

### Reasoning rubric

1. State the model, units, sign convention and independently worked value.
2. Explain both sweeps using this lesson's governing relation and recorded evidence.
3. Diagnose the actual fault mechanism and exact-input recovery.
4. Defend the stated boundary and link this result to the cumulative portfolio **A-CLASSICAL**.

This is authored self-assessment guidance. No learner completion, score or effectiveness result has been recorded.
