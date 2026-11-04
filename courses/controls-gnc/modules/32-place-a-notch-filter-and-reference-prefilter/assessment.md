## P32 course checkpoint

**Predict and calculate.** Place the notch relative to the actual resonance and distinguish it from a reference prefilter.

Use `N(s)=(s^2+2*zeta_z*w_n*s+w_n^2)/(s^2+2*zeta_p*w_n*s+w_n^2); F(s)=w_f/(s+w_f); reference map=F*T while disturbance map keeps N inside the loop` with the conventions in the lesson. Work one baseline value by hand before running. The live controls are **Notch frequency**, **Prefilter bandwidth**.

**Collect evidence.** Save the default result, then perform the lesson's two one-variable sweeps separately. Record exact parameters, units, the `response` and `mechanism` plots, and the quantity that discriminates your prediction. Explain what stayed invariant as well as what changed.

**Fault and recovery.** Enable **Enable the intentionally broken case** at the same inputs. Explain which governing term is changed or omitted, show its effect on the actual trajectory, matrix or criterion, then disable it and use **Reset parameters**. Confirm recovery reproduces the baseline rather than merely a more favorable number.

### Expected reasoning

A notch reduces loop transmission near its chosen center, while a prefilter changes reference content. Mistuning the notch can leave the physical resonance exposed even if reference motion looks smoother.

### Model boundary

The fixed resonance model omits uncertainty and changing structural modes.

### Reasoning rubric

1. State the model, units, sign convention and independently worked value.
2. Explain both sweeps using this lesson's governing relation and recorded evidence.
3. Diagnose the actual fault mechanism and exact-input recovery.
4. Defend the stated boundary and link this result to the cumulative portfolio **A-LOOP**.

This is authored self-assessment guidance. No learner completion, score or effectiveness result has been recorded.
