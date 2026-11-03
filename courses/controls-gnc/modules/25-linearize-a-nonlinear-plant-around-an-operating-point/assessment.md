## P25 course checkpoint

**Predict and calculate.** Compare operating-point residual and tangent-model error when changing angle and perturbation independently.

Use `tau_g=m*g*l*sin(theta); delta_x_dot=A*delta_x+B*delta_tau; A21=-(g/l)*cos(theta_0)` with the conventions in the lesson. Work one baseline value by hand before running. The live controls are **Operating angle**, **Perturbation radius**.

**Collect evidence.** Save the default result, then perform the lesson's two one-variable sweeps separately. Record exact parameters, units, the `response` and `mechanism` plots, and the quantity that discriminates your prediction. Explain what stayed invariant as well as what changed.

**Fault and recovery.** Enable **Enable the intentionally broken case** at the same inputs. Explain which governing term is changed or omitted, show its effect on the actual trajectory, matrix or criterion, then disable it and use **Reset parameters**. Confirm recovery reproduces the baseline rather than merely a more favorable number.

### Expected reasoning

An equilibrium must first balance gravity torque. The Jacobian describes a local perturbation after that balance; a small Taylor error cannot excuse linearizing around an unbalanced state.

### Model boundary

The approximation is local and excludes large-angle dynamic equivalence.

### Reasoning rubric

1. State the model, units, sign convention and independently worked value.
2. Explain both sweeps using this lesson's governing relation and recorded evidence.
3. Diagnose the actual fault mechanism and exact-input recovery.
4. Defend the stated boundary and link this result to the cumulative portfolio **A-MODELING**.

This is authored self-assessment guidance. No learner completion, score or effectiveness result has been recorded.
