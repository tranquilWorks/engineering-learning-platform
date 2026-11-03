## P39 course checkpoint

**Predict and calculate.** Explain why a terminal Riccati boundary must be propagated backward in time.

Use `-P_dot=2A(t)P-P^2/R+Q; P(t_f)=S_f; K(t)=R^-1 B^T P(t)` with the conventions in the lesson. Work one baseline value by hand before running. The live controls are **Control horizon**, **Terminal state weight**.

**Collect evidence.** Save the default result, then perform the lesson's two one-variable sweeps separately. Record exact parameters, units, the `response` and `mechanism` plots, and the quantity that discriminates your prediction. Explain what stayed invariant as well as what changed.

**Fault and recovery.** Enable **Enable the intentionally broken case** at the same inputs. Explain which governing term is changed or omitted, show its effect on the actual trajectory, matrix or criterion, then disable it and use **Reset parameters**. Confirm recovery reproduces the baseline rather than merely a more favorable number.

### Expected reasoning

The finite-horizon value at the end is prescribed. Starting that value at the beginning solves a different boundary problem; compare the terminal metric and time-varying gain schedule.

### Model boundary

The lab uses a declared finite-difference Riccati scheme, not an exact continuous optimizer or full state-cost rollout.

### Reasoning rubric

1. State the model, units, sign convention and independently worked value.
2. Explain both sweeps using this lesson's governing relation and recorded evidence.
3. Diagnose the actual fault mechanism and exact-input recovery.
4. Defend the stated boundary and link this result to the cumulative portfolio **A-OPTIMAL**.

This is authored self-assessment guidance. No learner completion, score or effectiveness result has been recorded.
