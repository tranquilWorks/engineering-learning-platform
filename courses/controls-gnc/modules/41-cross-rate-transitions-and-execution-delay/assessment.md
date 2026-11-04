## P41 course checkpoint

**Predict and calculate.** Explain the difference between slow-rate hold error, execution delay and timestamp-derived age.

Use `u_fast[k]=u_slow[floor(k/M)]; delay phase=-omega*tau; age=t_read-t_sample` with the conventions in the lesson. Work one baseline value by hand before running. The live controls are **Fast-to-slow rate ratio**, **Execution delay**.

**Collect evidence.** Save the default result, then perform the lesson's two one-variable sweeps separately. Record exact parameters, units, the `response` and `mechanism` plots, and the quantity that discriminates your prediction. Explain what stayed invariant as well as what changed.

**Fault and recovery.** Enable **Enable the intentionally broken case** at the same inputs. Explain which governing term is changed or omitted, show its effect on the actual trajectory, matrix or criterion, then disable it and use **Reset parameters**. Confirm recovery reproduces the baseline rather than merely a more favorable number.

### Expected reasoning

A held sample accumulates age within its rate period; transport/execution delay adds another contribution. A nominal phase-lag number alone does not prove data freshness for every tick.

### Model boundary

Fixed software index timing is not measured operating-system scheduling.

### Reasoning rubric

1. State the model, units, sign convention and independently worked value.
2. Explain both sweeps using this lesson's governing relation and recorded evidence.
3. Diagnose the actual fault mechanism and exact-input recovery.
4. Defend the stated boundary and link this result to the cumulative portfolio **A-DIGITAL**.

This is authored self-assessment guidance. No learner completion, score or effectiveness result has been recorded.
