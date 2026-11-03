## P10 course checkpoint

**Predict and calculate.** Separate sample-and-hold delay from a fractional transport delay in the plotted response.

Use `u_k=K_p(1-y_k); u(t)=u_{k-1}\;\text{then}\;u_k` with the conventions in the lesson. Work one baseline value by hand before running. The live controls are **Sample period**, **Delay / sample period**.

**Collect evidence.** Save the default result, then perform the lesson's two one-variable sweeps separately. Record exact parameters, units, the `response` and `mechanism` plots, and the quantity that discriminates your prediction. Explain what stayed invariant as well as what changed.

**Fault and recovery.** Enable **Enable the source broken case** at the same inputs. Explain which governing term is changed or omitted, show its effect on the actual trajectory, matrix or criterion, then disable it and use **Reset parameters**. Confirm recovery reproduces the baseline rather than merely a more favorable number.

### Expected reasoning

Time delay adds frequency-dependent phase; a fast sample rate does not remove an independent transport delay. Interpret failure using the actual delayed path instead of nominal continuous poles.

### Model boundary

The retained delay model is an approximation with a fixed execution convention.

### Reasoning rubric

1. State the model, units, sign convention and independently worked value.
2. Explain both sweeps using this lesson's governing relation and recorded evidence.
3. Diagnose the actual fault mechanism and exact-input recovery.
4. Defend the stated boundary and link this result to the cumulative portfolio **A-DIGITAL**.

This is authored self-assessment guidance. No learner completion, score or effectiveness result has been recorded.
