## P53 course checkpoint

**Predict and calculate.** Compare NIS before a gated update and NEES after it using the retained truth trajectory.

Use `S_k=P_k^-+R,\quad \mathrm{NIS}_k=\nu_k^2/S_k; K_k=P_k^-/S_k,\quad \hat x_k^+=\hat x_k^-+K_k\nu_k; \mathrm{NEES}_k=(\hat x_k^+-x_k)^2/P_k^+` with the conventions in the lesson. Work one baseline value by hand before running. The live controls are **NIS gate**, **Outlier magnitude**.

**Collect evidence.** Save the default result, then perform the lesson's two one-variable sweeps separately. Record exact parameters, units, the `response` and `mechanism` plots, and the quantity that discriminates your prediction. Explain what stayed invariant as well as what changed.

**Fault and recovery.** Enable **Enable the intentionally broken case** at the same inputs. Explain which governing term is changed or omitted, show its effect on the actual trajectory, matrix or criterion, then disable it and use **Reset parameters**. Confirm recovery reproduces the baseline rather than merely a more favorable number.

### Expected reasoning

NIS divides squared innovation by S; NEES divides posterior truth error by P. Bypassing the gate changes the posterior path at the same injection; independent-trial consistency cannot be inferred from deterministic time samples.

### Model boundary

NEES needs truth and deterministic samples do not validate chi-square coverage.

### Reasoning rubric

1. State the model, units, sign convention and independently worked value.
2. Explain both sweeps using this lesson's governing relation and recorded evidence.
3. Diagnose the actual fault mechanism and exact-input recovery.
4. Defend the stated boundary and link this result to the cumulative portfolio **A-STOCHASTIC**.

This is authored self-assessment guidance. No learner completion, score or effectiveness result has been recorded.
