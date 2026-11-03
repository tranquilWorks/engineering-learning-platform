## P22 course checkpoint

**Predict and calculate.** Explain the signs and dimensions of the bounded proportional-navigation teaching example.

Use `a_n=N V_c\dot\lambda; \dot\lambda=(r_xv_y-r_yv_x)/\|r\|^2` with the conventions in the lesson. Work one baseline value by hand before running. The live controls are **Navigation constant**, **Acceleration limit**.

**Collect evidence.** Save the default result, then perform the lesson's two one-variable sweeps separately. Record exact parameters, units, the `response` and `mechanism` plots, and the quantity that discriminates your prediction. Explain what stayed invariant as well as what changed.

**Fault and recovery.** Enable **Enable the source broken case** at the same inputs. Explain which governing term is changed or omitted, show its effect on the actual trajectory, matrix or criterion, then disable it and use **Reset parameters**. Confirm recovery reproduces the baseline rather than merely a more favorable number.

### Expected reasoning

The modeled acceleration uses a navigation constant, closing speed and line-of-sight rate. State the closing/angle conventions before interpreting a miss distance or saturation event.

### Model boundary

This is a bounded synthetic guidance-method illustration, not operational system validation.

### Reasoning rubric

1. State the model, units, sign convention and independently worked value.
2. Explain both sweeps using this lesson's governing relation and recorded evidence.
3. Diagnose the actual fault mechanism and exact-input recovery.
4. Defend the stated boundary and link this result to the cumulative portfolio **A-GUIDANCE**.

This is authored self-assessment guidance. No learner completion, score or effectiveness result has been recorded.
