## P12 course checkpoint

**Predict and calculate.** Explain why reducing the demand after saturation does not immediately erase stored integral state.

Use `\dot q=e+K_{aw}(u_{sat}-u_{raw}); u_{raw}=K_pe+K_iq` with the conventions in the lesson. Work one baseline value by hand before running. The live controls are **Anti-windup gain**, **High-demand duration**.

**Collect evidence.** Save the default result, then perform the lesson's two one-variable sweeps separately. Record exact parameters, units, the `response` and `mechanism` plots, and the quantity that discriminates your prediction. Explain what stayed invariant as well as what changed.

**Fault and recovery.** Enable **Enable the source broken case** at the same inputs. Explain which governing term is changed or omitted, show its effect on the actual trajectory, matrix or criterion, then disable it and use **Reset parameters**. Confirm recovery reproduces the baseline rather than merely a more favorable number.

### Expected reasoning

The integrator retains its history during saturation; anti-windup feeds back the request/applied discrepancy. Recovery should compare the same demand duration and limit, not a more favorable test.

### Model boundary

An anti-windup example does not guarantee every reference can be tracked.

### Reasoning rubric

1. State the model, units, sign convention and independently worked value.
2. Explain both sweeps using this lesson's governing relation and recorded evidence.
3. Diagnose the actual fault mechanism and exact-input recovery.
4. Defend the stated boundary and link this result to the cumulative portfolio **A-DIGITAL**.

This is authored self-assessment guidance. No learner completion, score or effectiveness result has been recorded.
