# P31 course checkpoint

## Predict and derive

Check inertia symmetry, positive energy and the Coriolis skew identity.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `M(q) qddot+C(q,qdot) qdot+g(q)=tau`
- `kinetic_energy=0.5 qdot^T M(q) qdot`
- `S=Mdot-2C; S+S^T=0`

## Controlled comparison

- `payload_kg`: 1.0 → 5.0. Hold the other controls at baseline and explain the mechanism before executing.
- `elbow_angle_deg`: 55.0 → 160.0. Hold the other controls at baseline and explain the mechanism before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

Kinetic energy defines inertia; configuration derivatives produce coupling terms, while gravity is the potential gradient.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

A positive inertia matrix alone does not validate every dynamic term.

Competency links: ROBOT-DYNAMICS. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
