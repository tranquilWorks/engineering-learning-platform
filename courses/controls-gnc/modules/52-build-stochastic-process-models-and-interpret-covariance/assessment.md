## P52 course checkpoint

**Predict and calculate.** Distinguish zero-mean state prediction from covariance growth under a random walk.

Use `\dot P=q,\quad P(0)=1; P(T)=1+qT,\quad \sigma(T)=\sqrt{P(T)}` with the conventions in the lesson. Work one baseline value by hand before running. The live controls are **Process noise density**, **Propagation interval**.

**Collect evidence.** Save the default result, then perform the lesson's two one-variable sweeps separately. Record exact parameters, units, the `response` and `mechanism` plots, and the quantity that discriminates your prediction. Explain what stayed invariant as well as what changed.

**Fault and recovery.** Enable **Enable the intentionally broken case** at the same inputs. Explain which governing term is changed or omitted, show its effect on the actual trajectory, matrix or criterion, then disable it and use **Reset parameters**. Confirm recovery reproduces the baseline rather than merely a more favorable number.

### Expected reasoning

Positive process noise adds qT to initial variance. The mean can remain unchanged while uncertainty grows; subtracting noise can produce an invalid covariance even if a clipped plot stays finite.

### Model boundary

The experiment is scalar covariance propagation, not a general vector stochastic process.

### Reasoning rubric

1. State the model, units, sign convention and independently worked value.
2. Explain both sweeps using this lesson's governing relation and recorded evidence.
3. Diagnose the actual fault mechanism and exact-input recovery.
4. Defend the stated boundary and link this result to the cumulative portfolio **A-STOCHASTIC**.

This is authored self-assessment guidance. No learner completion, score or effectiveness result has been recorded.
