## P04 course checkpoint

**Predict and calculate.** Identify when a small-angle pendulum ceases to predict the nonlinear motion accurately.

Use `\ddot{\theta}+2\zeta\sqrt{g/L}\dot{\theta}+(g/L)\sin\theta=0; \sin\theta\approx\theta` with the conventions in the lesson. Work one baseline value by hand before running. The live controls are **Initial angle**, **Pendulum length**.

**Collect evidence.** Save the default result, then perform the lesson's two one-variable sweeps separately. Record exact parameters, units, the `response` and `mechanism` plots, and the quantity that discriminates your prediction. Explain what stayed invariant as well as what changed.

**Fault and recovery.** Enable **Enable the source broken case** at the same inputs. Explain which governing term is changed or omitted, show its effect on the actual trajectory, matrix or criterion, then disable it and use **Reset parameters**. Confirm recovery reproduces the baseline rather than merely a more favorable number.

### Expected reasoning

The sine law and its tangent coincide only locally. Larger initial angles change restoring torque and period; agreement near the equilibrium is insufficient at large excursions.

### Model boundary

The undriven ideal pendulum omits friction and actuator dynamics.

### Reasoning rubric

1. State the model, units, sign convention and independently worked value.
2. Explain both sweeps using this lesson's governing relation and recorded evidence.
3. Diagnose the actual fault mechanism and exact-input recovery.
4. Defend the stated boundary and link this result to the cumulative portfolio **A-MODELING**.

This is authored self-assessment guidance. No learner completion, score or effectiveness result has been recorded.
