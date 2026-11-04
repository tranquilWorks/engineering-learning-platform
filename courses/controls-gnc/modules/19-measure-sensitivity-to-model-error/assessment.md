## P19 course checkpoint

**Predict and calculate.** Predict the effect of actual actuator gain and drag mismatch without redesigning the nominal controller.

Use `\dot v=-b_av+g_au; S_p=(y_a-y_n)/y_n` with the conventions in the lesson. Work one baseline value by hand before running. The live controls are **Actual / nominal actuator gain**, **Actual / nominal drag**.

**Collect evidence.** Save the default result, then perform the lesson's two one-variable sweeps separately. Record exact parameters, units, the `response` and `mechanism` plots, and the quantity that discriminates your prediction. Explain what stayed invariant as well as what changed.

**Fault and recovery.** Enable **Enable the source broken case** at the same inputs. Explain which governing term is changed or omitted, show its effect on the actual trajectory, matrix or criterion, then disable it and use **Reset parameters**. Confirm recovery reproduces the baseline rather than merely a more favorable number.

### Expected reasoning

Model error changes the physical loop while the nominal design remains fixed. Compare gain and drag sweeps independently; a robust claim must name the tested uncertainty family and performance measure.

### Model boundary

A sampled two-parameter family is not all possible plant uncertainty.

### Reasoning rubric

1. State the model, units, sign convention and independently worked value.
2. Explain both sweeps using this lesson's governing relation and recorded evidence.
3. Diagnose the actual fault mechanism and exact-input recovery.
4. Defend the stated boundary and link this result to the cumulative portfolio **A-LOOP**.

This is authored self-assessment guidance. No learner completion, score or effectiveness result has been recorded.
