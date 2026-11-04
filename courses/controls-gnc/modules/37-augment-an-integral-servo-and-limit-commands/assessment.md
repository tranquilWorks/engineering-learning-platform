## P37 course checkpoint

**Predict and calculate.** Compare integral load rejection with the requested and limited command at identical authority.

Use `z_dot=r-y; u=clip(k_p(r-y)+k_i z,u_min,u_max); x_dot=-x+u+d` with the conventions in the lesson. Work one baseline value by hand before running. The live controls are **Integral gain**, **Normalized drive limit**.

**Collect evidence.** Save the default result, then perform the lesson's two one-variable sweeps separately. Record exact parameters, units, the `response` and `mechanism` plots, and the quantity that discriminates your prediction. Explain what stayed invariant as well as what changed.

**Fault and recovery.** Enable **Enable the intentionally broken case** at the same inputs. Explain which governing term is changed or omitted, show its effect on the actual trajectory, matrix or criterion, then disable it and use **Reset parameters**. Confirm recovery reproduces the baseline rather than merely a more favorable number.

### Expected reasoning

Integral action can reject a feasible constant load while command saturation prevents impossible equilibria. Track the integral state as well as position; a stable unsaturated design is not enough.

### Model boundary

The normalized first-order servo is not a complete second-order mechanical plant.

### Reasoning rubric

1. State the model, units, sign convention and independently worked value.
2. Explain both sweeps using this lesson's governing relation and recorded evidence.
3. Diagnose the actual fault mechanism and exact-input recovery.
4. Defend the stated boundary and link this result to the cumulative portfolio **A-STATE**.

This is authored self-assessment guidance. No learner completion, score or effectiveness result has been recorded.
