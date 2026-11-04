## P29 course checkpoint

**Predict and calculate.** Count open-loop unstable poles before interpreting a Nyquist winding around minus one.

Use `L(s)=K(s+1)/((s-p)(s+2)(s+3)); N=Z-P; Delta arg(1+L)=2*pi*N` with the conventions in the lesson. Work one baseline value by hand before running. The live controls are **Loop gain**, **Open-loop unstable pole**.

**Collect evidence.** Save the default result, then perform the lesson's two one-variable sweeps separately. Record exact parameters, units, the `response` and `mechanism` plots, and the quantity that discriminates your prediction. Explain what stayed invariant as well as what changed.

**Fault and recovery.** Enable **Enable the intentionally broken case** at the same inputs. Explain which governing term is changed or omitted, show its effect on the actual trajectory, matrix or criterion, then disable it and use **Reset parameters**. Confirm recovery reproduces the baseline rather than merely a more favorable number.

### Expected reasoning

The relation between winding and closed-loop unstable poles depends on the declared contour convention. Verify polynomial pole counting as a separate check; a visually small loop is insufficient.

### Model boundary

A finite sampled contour can miss critical behavior, especially near imaginary-axis crossings.

### Reasoning rubric

1. State the model, units, sign convention and independently worked value.
2. Explain both sweeps using this lesson's governing relation and recorded evidence.
3. Diagnose the actual fault mechanism and exact-input recovery.
4. Defend the stated boundary and link this result to the cumulative portfolio **A-CLASSICAL**.

This is authored self-assessment guidance. No learner completion, score or effectiveness result has been recorded.
