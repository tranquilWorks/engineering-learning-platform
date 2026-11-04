## P13 course checkpoint

**Predict and calculate.** Use a zero input gain or coupling limit to distinguish controllability rank from control effort.

Use `\mathcal C=[B\;AB]; W_c=\sum A^kBB^T(A^T)^k` with the conventions in the lesson. Work one baseline value by hand before running. The live controls are **Input gain**, **State coupling**.

**Collect evidence.** Save the default result, then perform the lesson's two one-variable sweeps separately. Record exact parameters, units, the `response` and `mechanism` plots, and the quantity that discriminates your prediction. Explain what stayed invariant as well as what changed.

**Fault and recovery.** Enable **Enable the source broken case** at the same inputs. Explain which governing term is changed or omitted, show its effect on the actual trajectory, matrix or criterion, then disable it and use **Reset parameters**. Confirm recovery reproduces the baseline rather than merely a more favorable number.

### Expected reasoning

The span of B, AB and higher powers identifies reachable directions. A barely nonzero coupling can preserve rank yet make reaching a state poorly conditioned and expensive.

### Model boundary

Binary rank alone does not quantify numerical conditioning or bounded-input reachability.

### Reasoning rubric

1. State the model, units, sign convention and independently worked value.
2. Explain both sweeps using this lesson's governing relation and recorded evidence.
3. Diagnose the actual fault mechanism and exact-input recovery.
4. Defend the stated boundary and link this result to the cumulative portfolio **A-MODELING**.

This is authored self-assessment guidance. No learner completion, score or effectiveness result has been recorded.
