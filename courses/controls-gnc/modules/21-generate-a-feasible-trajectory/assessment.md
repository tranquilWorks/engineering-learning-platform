## P21 course checkpoint

**Predict and calculate.** Check whether changing distance or move duration violates the generated trajectory's limits.

Use `x=x_f(10s^3-15s^4+6s^5); s=t/T` with the conventions in the lesson. Work one baseline value by hand before running. The live controls are **Target position**, **Move duration**.

**Collect evidence.** Save the default result, then perform the lesson's two one-variable sweeps separately. Record exact parameters, units, the `response` and `mechanism` plots, and the quantity that discriminates your prediction. Explain what stayed invariant as well as what changed.

**Fault and recovery.** Enable **Enable the source broken case** at the same inputs. Explain which governing term is changed or omitted, show its effect on the actual trajectory, matrix or criterion, then disable it and use **Reset parameters**. Confirm recovery reproduces the baseline rather than merely a more favorable number.

### Expected reasoning

Time scaling changes velocity and acceleration at different powers of duration. A geometrically smooth reference may still demand infeasible actuator authority; check each derivative with its units.

### Model boundary

Reference feasibility is not guaranteed closed-loop tracking.

### Reasoning rubric

1. State the model, units, sign convention and independently worked value.
2. Explain both sweeps using this lesson's governing relation and recorded evidence.
3. Diagnose the actual fault mechanism and exact-input recovery.
4. Defend the stated boundary and link this result to the cumulative portfolio **A-CONSTRAINTS**.

This is authored self-assessment guidance. No learner completion, score or effectiveness result has been recorded.
