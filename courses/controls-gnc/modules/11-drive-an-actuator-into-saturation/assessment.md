## P11 course checkpoint

**Predict and calculate.** Determine when a requested command is feasible and trace the plant driven by its applied value.

Use `u=\operatorname{clip}(K_p(r-y),-u_{max},u_{max}); \dot y=-y+u` with the conventions in the lesson. Work one baseline value by hand before running. The live controls are **Reference**, **Actuator limit**.

**Collect evidence.** Save the default result, then perform the lesson's two one-variable sweeps separately. Record exact parameters, units, the `response` and `mechanism` plots, and the quantity that discriminates your prediction. Explain what stayed invariant as well as what changed.

**Fault and recovery.** Enable **Enable the source broken case** at the same inputs. Explain which governing term is changed or omitted, show its effect on the actual trajectory, matrix or criterion, then disable it and use **Reset parameters**. Confirm recovery reproduces the baseline rather than merely a more favorable number.

### Expected reasoning

The actuator limit bounds applied command rather than requested command. Tracking can fail despite nominally stable poles if sufficient control authority is unavailable.

### Model boundary

Static clipping omits actuator rate, heating and mechanical dynamics.

### Reasoning rubric

1. State the model, units, sign convention and independently worked value.
2. Explain both sweeps using this lesson's governing relation and recorded evidence.
3. Diagnose the actual fault mechanism and exact-input recovery.
4. Defend the stated boundary and link this result to the cumulative portfolio **A-DIGITAL**.

This is authored self-assessment guidance. No learner completion, score or effectiveness result has been recorded.
