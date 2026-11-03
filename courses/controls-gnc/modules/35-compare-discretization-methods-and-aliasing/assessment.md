## P35 course checkpoint

**Predict and calculate.** Compare exact ZOH, Euler pole mapping and alias-equivalent sampled tones at the same sample interval.

Use `z_ZOH=exp(a*T_s); z_Tustin=(1+a*T_s/2)/(1-a*T_s/2); f_alias=wrap(f,[-f_s/2,f_s/2])` with the conventions in the lesson. Work one baseline value by hand before running. The live controls are **Sample period**, **Input frequency**.

**Collect evidence.** Save the default result, then perform the lesson's two one-variable sweeps separately. Record exact parameters, units, the `response` and `mechanism` plots, and the quantity that discriminates your prediction. Explain what stayed invariant as well as what changed.

**Fault and recovery.** Enable **Enable the intentionally broken case** at the same inputs. Explain which governing term is changed or omitted, show its effect on the actual trajectory, matrix or criterion, then disable it and use **Reset parameters**. Confirm recovery reproduces the baseline rather than merely a more favorable number.

### Expected reasoning

The exact scalar pole is exp(aT), whereas Euler uses 1+aT. A stable continuous pole can map to an unstable Euler pole; sampled sinusoidal frequency is ambiguous modulo sampling frequency.

### Model boundary

The retained lab compares a scalar pole and tone, not a full sampled-data loop.

### Reasoning rubric

1. State the model, units, sign convention and independently worked value.
2. Explain both sweeps using this lesson's governing relation and recorded evidence.
3. Diagnose the actual fault mechanism and exact-input recovery.
4. Defend the stated boundary and link this result to the cumulative portfolio **A-DIGITAL**.

This is authored self-assessment guidance. No learner completion, score or effectiveness result has been recorded.
