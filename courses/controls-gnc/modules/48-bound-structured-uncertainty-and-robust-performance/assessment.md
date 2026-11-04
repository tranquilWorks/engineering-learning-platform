## P48 evidence task

Why does reversing feedback invalidate a robustness claim even when the sensitivity chart contains only finite values?

Before running: Can a finite, smooth frequency-response curve prove the closed-loop family is stable? Check the pole calculation separately.

Collect three records: the default plots and metrics; one change from the stated sweeps with the other control fixed; and the fault followed by restored defaults. Record parameter values and units beside each observation.

Declared uncertainty family plots decay rate over exactly the selected perturbation interval. True sensitivity magnitude plots the maximum over 81 uncertainty samples at each of 160 frequencies from 0.05 to 100 rad/s. Its peak is a sampled finite-band quantity.

### Reasoning rubric

- Model: use `P(s)=1/(s+a); a=1+delta; delta in [-radius,+radius] 1/s` to explain the observed quantity rather than repeating a metric label.
- Evidence: Zero uncertainty radius collapses the family to one model. Show where your plot or numerical record tests this statement.
- Diagnosis: Broken mode reverses the feedback sign, replacing a+K by a−K. At default settings the entire family is unstable even though finite-frequency magnitude values can still be computed. Identify the measured consequence in your record.
- Recovery and scope: Restore negative feedback and reset both controls. Verify the minimum decay margin is positive before interpreting sensitivity as a stable closed-loop disturbance response. State this limit: An unstable transfer expression is not a bounded-input bounded-output performance certificate; the sampled finite-band peak is not an H-infinity norm.

### Check your explanation

The denominator has a right-half-plane pole whenever a−K<0. Sampling on the imaginary axis can produce finite values despite that pole; internal stability is a separate requirement.

A complete answer includes the calculation or recurrence, an observed comparison with units, fault/recovery evidence and the stated limitation. Revisit the lesson if the explanation depends only on a changing headline number. This is a self-assessment; no learner score is stored.


---

## P48 course checkpoint

**Predict and calculate.** Compare worst sampled sensitivity over the declared uncertainty interval with the nominal response.

Use `P(s)=1/(s+a); a=1+delta; delta in [-radius,+radius] 1/s; S(s)=1/(1+K*P(s))=(s+a)/(s+a+K); closed-loop pole=-(a+K)` with the conventions in the lesson. Work one baseline value by hand before running. The live controls are **Pole uncertainty radius**, **Feedback gain**.

**Collect evidence.** Save the default result, then perform the lesson's two one-variable sweeps separately. Record exact parameters, units, the `response` and `mechanism` plots, and the quantity that discriminates your prediction. Explain what stayed invariant as well as what changed.

**Fault and recovery.** Enable **Enable the intentionally broken case** at the same inputs. Explain which governing term is changed or omitted, show its effect on the actual trajectory, matrix or criterion, then disable it and use **Reset parameters**. Confirm recovery reproduces the baseline rather than merely a more favorable number.

### Expected reasoning

Robust performance names an uncertainty set and a performance quantity. Dimensionless normalized margins must not mix incompatible units; a sample grid is evidence for that grid, not an exact all-frequency theorem.

### Model boundary

Finite grids do not establish structured singular-value certification.

### Reasoning rubric

1. State the model, units, sign convention and independently worked value.
2. Explain both sweeps using this lesson's governing relation and recorded evidence.
3. Diagnose the actual fault mechanism and exact-input recovery.
4. Defend the stated boundary and link this result to the cumulative portfolio **A-ROBUST**.

This is authored self-assessment guidance. No learner completion, score or effectiveness result has been recorded.
