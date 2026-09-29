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
