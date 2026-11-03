## P16 course checkpoint

**Predict and calculate.** Predict what happens when assumed measurement noise disagrees with the retained noisy sensor stream.

Use `K_k=P^-C^T(CP^-C^T+R)^{-1}; P^+=(I-KC)P^-` with the conventions in the lesson. Work one baseline value by hand before running. The live controls are **Assumed position noise**, **Assumed acceleration noise**.

**Collect evidence.** Save the default result, then perform the lesson's two one-variable sweeps separately. Record exact parameters, units, the `response` and `mechanism` plots, and the quantity that discriminates your prediction. Explain what stayed invariant as well as what changed.

**Fault and recovery.** Enable **Enable the source broken case** at the same inputs. Explain which governing term is changed or omitted, show its effect on the actual trajectory, matrix or criterion, then disable it and use **Reset parameters**. Confirm recovery reproduces the baseline rather than merely a more favorable number.

### Expected reasoning

Kalman gain balances propagated covariance against assumed measurement covariance. Smaller reported P can mean overconfidence rather than smaller actual error, so inspect innovations and truth error separately.

### Model boundary

A deterministic example does not establish probabilistic confidence coverage.

### Reasoning rubric

1. State the model, units, sign convention and independently worked value.
2. Explain both sweeps using this lesson's governing relation and recorded evidence.
3. Diagnose the actual fault mechanism and exact-input recovery.
4. Defend the stated boundary and link this result to the cumulative portfolio **A-OPTIMAL-EST**.

This is authored self-assessment guidance. No learner completion, score or effectiveness result has been recorded.
