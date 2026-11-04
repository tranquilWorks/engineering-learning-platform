# P15 course checkpoint

## Predict and derive

Explain particle weights, effective sample size and resampling diversity.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `w_i proportional to p(z|x_i)`
- `N_eff=1/sum(w_i^2)`

## Controlled comparison

- Vary only `particle_count` through [100, 400, 1000]; predict Higher count reduces sampling granularity without repairing model bias.
- Vary only `sensor_noise_m` through [0.1, 0.4, 1.5]; predict Narrow likelihoods concentrate weights and reduce ESS.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

Bayes weights favor compatible poses, normalization preserves probability mass, and resampling trades weight degeneracy for duplicate hypotheses.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

A concentrated particle set can converge to a wrong mode.

Competency links: STATE-ESTIMATION. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
