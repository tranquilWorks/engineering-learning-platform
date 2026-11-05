# P46 course checkpoint

## Predict and derive

Compare open and biased differential force allocation under separate wheel capacities and one total demand.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `F_open=2 min(F_demand/2,mu_L F_z,mu_R F_z)`
- `F_R<=TBR F_L`
- `F_L+F_R<=F_demand and F_k<=mu_k F_z`

## Controlled comparison

- `left_friction_mu`: 0.35 → 0.6. Hold the other controls at baseline; predict and explain the change before executing.
- `torque_bias_ratio`: 4 → 2. Hold the other controls at baseline; predict and explain the change before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

With 3200 N per wheel and left mu=0.35, the left capacity is 1120 N. The open differential supplies at most 2240 N total. A bias ratio of four requests 4480 N on the right, but right capacity is only 1.15*3200=3680 N; the capped total is therefore 4800 N. Unlimited multiplication would exceed the high-grip contact. Check both wheel constraints and total demand rather than assuming the bias ratio is always achieved.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

This quasi-static allocation has no preload, speed-sensitive locking, axle compliance or wheel-speed dynamics.

Competency links: VD-POWERTRAIN. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
