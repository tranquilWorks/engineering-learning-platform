## P63 course checkpoint

**Predict and calculate.** Predict the initial LOS heading and compare nonlinear cross-track evolution with its local approximation.

Use `\chi_c=-\arctan(y/L); \dot x=V\cos\chi_c,\quad \dot y=V\sin\chi_c; \dot y\simeq -(V/L)y\quad\text{only for }|y|\ll L` with the conventions in the lesson. Work one baseline value by hand before running. The live controls are **LOS lookahead**, **Vehicle speed**.

**Collect evidence.** Save the default result, then perform the lesson's two one-variable sweeps separately. Record exact parameters, units, the `response` and `mechanism` plots, and the quantity that discriminates your prediction. Explain what stayed invariant as well as what changed.

**Fault and recovery.** Enable **Enable the intentionally broken case** at the same inputs. Explain which governing term is changed or omitted, show its effect on the actual trajectory, matrix or criterion, then disable it and use **Reset parameters**. Confirm recovery reproduces the baseline rather than merely a more favorable number.

### Expected reasoning

The actual heading is minus atan(y/L); lateral speed is V times its sine. Exponential decay is valid only for small y/L, and reversing the sign causes growing error with a changing peak heading.

### Model boundary

The lab follows a straight path with instantaneous heading tracking, not a full waypoint controller.

### Reasoning rubric

1. State the model, units, sign convention and independently worked value.
2. Explain both sweeps using this lesson's governing relation and recorded evidence.
3. Diagnose the actual fault mechanism and exact-input recovery.
4. Defend the stated boundary and link this result to the cumulative portfolio **A-GUIDANCE**.

This is authored self-assessment guidance. No learner completion, score or effectiveness result has been recorded.
