## P08 course checkpoint

**Predict and calculate.** Compare feedback disturbance rejection at zero frequency and at a higher disturbance frequency.

Use `\dot y=-y-K(y+b)+d; |S_d(j\omega)|=1/\sqrt{(1+K)^2+\omega^2}` with the conventions in the lesson. Work one baseline value by hand before running. The live controls are **Feedback gain**, **Disturbance frequency**.

**Collect evidence.** Save the default result, then perform the lesson's two one-variable sweeps separately. Record exact parameters, units, the `response` and `mechanism` plots, and the quantity that discriminates your prediction. Explain what stayed invariant as well as what changed.

**Fault and recovery.** Enable **Enable the source broken case** at the same inputs. Explain which governing term is changed or omitted, show its effect on the actual trajectory, matrix or criterion, then disable it and use **Reset parameters**. Confirm recovery reproduces the baseline rather than merely a more favorable number.

### Expected reasoning

The closed-loop sensitivity attenuates some disturbances but its attenuation varies with frequency. Identify the disturbance injection point before equating an output change to the loop gain.

### Model boundary

The modeled injection and sensor paths determine which sensitivity function applies.

### Reasoning rubric

1. State the model, units, sign convention and independently worked value.
2. Explain both sweeps using this lesson's governing relation and recorded evidence.
3. Diagnose the actual fault mechanism and exact-input recovery.
4. Defend the stated boundary and link this result to the cumulative portfolio **A-CLASSICAL**.

This is authored self-assessment guidance. No learner completion, score or effectiveness result has been recorded.
