## P07 course checkpoint

**Predict and calculate.** Reconcile a time-response oscillation with the loop margin and actuator-lag change.

Use `L(s)=K/[s(s+1)(\tau_a s+1)]; PM=180^\circ+\angle L(j\omega_c)` with the conventions in the lesson. Work one baseline value by hand before running. The live controls are **Loop gain**, **Actuator lag**.

**Collect evidence.** Save the default result, then perform the lesson's two one-variable sweeps separately. Record exact parameters, units, the `response` and `mechanism` plots, and the quantity that discriminates your prediction. Explain what stayed invariant as well as what changed.

**Fault and recovery.** Enable **Enable the source broken case** at the same inputs. Explain which governing term is changed or omitted, show its effect on the actual trajectory, matrix or criterion, then disable it and use **Reset parameters**. Confirm recovery reproduces the baseline rather than merely a more favorable number.

### Expected reasoning

Added lag changes phase near crossover and can reduce stability margin even if low-frequency gain improves tracking. A positive gain margin alone does not summarize every crossover or delay effect.

### Model boundary

Finite frequency sampling is not exhaustive robust stability certification.

### Reasoning rubric

1. State the model, units, sign convention and independently worked value.
2. Explain both sweeps using this lesson's governing relation and recorded evidence.
3. Diagnose the actual fault mechanism and exact-input recovery.
4. Defend the stated boundary and link this result to the cumulative portfolio **A-CLASSICAL**.

This is authored self-assessment guidance. No learner completion, score or effectiveness result has been recorded.
