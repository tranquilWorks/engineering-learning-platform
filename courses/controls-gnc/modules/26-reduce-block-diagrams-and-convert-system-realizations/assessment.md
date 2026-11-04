## P26 course checkpoint

**Predict and calculate.** Distinguish equivalent state/transfer realizations from an invalid near pole-zero cancellation.

Use `G(s)=(s+2)/((s+1)(s+2+delta)(s+4)); G(s)=C(sI-A)^-1B; G_red(s)=1/((s+1)(s+4)) only when delta=0` with the conventions in the lesson. Work one baseline value by hand before running. The live controls are **Near-cancelled pole offset**, **Maximum probe frequency**.

**Collect evidence.** Save the default result, then perform the lesson's two one-variable sweeps separately. Record exact parameters, units, the `response` and `mechanism` plots, and the quantity that discriminates your prediction. Explain what stayed invariant as well as what changed.

**Fault and recovery.** Enable **Enable the intentionally broken case** at the same inputs. Explain which governing term is changed or omitted, show its effect on the actual trajectory, matrix or criterion, then disable it and use **Reset parameters**. Confirm recovery reproduces the baseline rather than merely a more favorable number.

### Expected reasoning

A coordinate realization preserves the full transfer relation. Dropping a nearly cancelled mode changes the model unless exact cancellation and the relevant input/output assumptions hold.

### Model boundary

Input/output cancellation does not establish every internal state is harmless.

### Reasoning rubric

1. State the model, units, sign convention and independently worked value.
2. Explain both sweeps using this lesson's governing relation and recorded evidence.
3. Diagnose the actual fault mechanism and exact-input recovery.
4. Defend the stated boundary and link this result to the cumulative portfolio **A-MODELING**.

This is authored self-assessment guidance. No learner completion, score or effectiveness result has been recorded.
