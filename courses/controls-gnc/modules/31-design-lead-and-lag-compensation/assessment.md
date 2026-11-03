## P31 course checkpoint

**Predict and calculate.** Explain why a lead stage adds phase while a lag stage changes low-frequency gain differently.

Use `C_lead=(1+s/z_l)/(1+s/p_l), p_l>z_l; phi_max=sin^-1((1-alpha)/(1+alpha)); C_lag=(1+s/z_g)/(1+s/p_g), p_g<z_g` with the conventions in the lesson. Work one baseline value by hand before running. The live controls are **Lead alpha**, **Lag beta**.

**Collect evidence.** Save the default result, then perform the lesson's two one-variable sweeps separately. Record exact parameters, units, the `response` and `mechanism` plots, and the quantity that discriminates your prediction. Explain what stayed invariant as well as what changed.

**Fault and recovery.** Enable **Enable the intentionally broken case** at the same inputs. Explain which governing term is changed or omitted, show its effect on the actual trajectory, matrix or criterion, then disable it and use **Reset parameters**. Confirm recovery reproduces the baseline rather than merely a more favorable number.

### Expected reasoning

Lead and lag are identified by their pole-zero ordering, not a component name. Swapping the lead pole and zero reverses the phase effect; compare the same frequencies and scaling.

### Model boundary

An isolated compensator plot does not certify the full closed loop.

### Reasoning rubric

1. State the model, units, sign convention and independently worked value.
2. Explain both sweeps using this lesson's governing relation and recorded evidence.
3. Diagnose the actual fault mechanism and exact-input recovery.
4. Defend the stated boundary and link this result to the cumulative portfolio **A-LOOP**.

This is authored self-assessment guidance. No learner completion, score or effectiveness result has been recorded.
