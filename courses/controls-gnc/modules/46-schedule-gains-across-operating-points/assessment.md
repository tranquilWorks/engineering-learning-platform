## P46 evidence task

Why can the selected bandwidth error be zero while sampled maximum gain error is positive? Which plot shows the missing information?

Before running: If the selected operating point is already a knot, will the selected bandwidth reveal the worst interpolation error?

Collect three records: the default plots and metrics; one change from the stated sweeps with the other control fixed; and the fault followed by restored defaults. Record parameter values and units beside each observation.

Gain table and interpolation displays the exact law, used schedule and sampled knots. Resulting closed-loop bandwidth shows the resulting decay rate across the full operating range. The maximum gain error is measured on the displayed grid, which includes midpoints.

### Reasoning rubric

- Model: use `g(rho)=1+rho^2/2; K_exact(rho)=2/g(rho)` to explain the observed quantity rather than repeating a metric label.
- Evidence: Healthy interpolation equals the table exactly at every knot. Show where your plot or numerical record tests this statement.
- Diagnosis: Broken mode freezes K at its rho=0 value of 2/s. The table remains visible for comparison, but the used gain no longer adapts to the plant. Identify the measured consequence in your record.
- Recovery and scope: Restore interpolation, reset spacing and compare knot values with exact gains. Inspect an off-knot value as a separate check. State this limit: The reported grid maximum is sampled evidence, not a rigorous continuous worst-case bound.

### Check your explanation

The selected point can coincide with a knot. The schedule plot exposes departures between knots, and the bandwidth plot shows their closed-loop effect across rho.

A complete answer includes the calculation or recurrence, an observed comparison with units, fault/recovery evidence and the stated limitation. Revisit the lesson if the explanation depends only on a changing headline number. This is a self-assessment; no learner score is stored.
