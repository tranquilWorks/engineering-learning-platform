# Cumulative portfolio A-DYNAMICS

Integrate these existing lessons: P30, P31, P32, P33, P35, P36, P40.

Required evidence: Energy, symmetry, skew-property, statics, inverse-dynamics residual, identification, and underactuation checks.

## Derive and predict

Use P30: Derive joint torques from a specified end-effector wrench. Virtual work equates task and joint power, giving a Jacobian-transpose mapping with explicit force and moment units. Connect this result to at least one other listed lesson, identifying the exact quantity, units and assumption transferred across their interface.

## Compare connected mechanisms

Use P32: Separate parameter fitting from held-out torque prediction. Excitation determines regressor rank; fit residual and parameter error must be checked separately on new motion. Connect this result to at least one other listed lesson, identifying the exact quantity, units and assumption transferred across their interface.

## Diagnose and recover

Use P35: Explain the effect of payload mismatch on computed-torque compensation. Model cancellation uses inertia, coupling and gravity; feedback corrects residual error only within available effort. Connect this result to at least one other listed lesson, identifying the exact quantity, units and assumption transferred across their interface.

## Integrate and defend the boundary

Use P40: Explain the energy-shaping and balance-control switching condition. The unactuated link receives energy through coupled dynamics; switching depends on angle and rate, not merely elapsed time. Connect this result to at least one other listed lesson, identifying the exact quantity, units and assumption transferred across their interface.

## Four-criterion rubric

1. Governing reasoning: equations, units and frame/sign conventions justify a numerical prediction; naming an algorithm alone earns no evidence.
2. Controlled comparison: two isolated sweeps and at least one limiting case distinguish mechanisms and make a falsifiable claim.
3. Diagnose and recover: identify the first failing assumption from actual outputs, restore it and demonstrate deterministic recovery.
4. Integration and scope: show the value passed between stages, an independently checked result, and a limitation that prevents a broader claim.

Retain inputs, selected outputs and your explanation as a cumulative artifact. No learner completion, automatic score, physical qualification or production acceptance is recorded.
