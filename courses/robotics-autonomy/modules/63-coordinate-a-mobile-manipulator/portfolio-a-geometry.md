# A-GEOMETRY integration evidence

Integrate these existing lessons: P01, P02, P12, P13, P25, P26, P27, P63.

Required evidence: Frame round trips, group closure, adjoint duality, constraint residuals, and convention checks.

## Derive and predict

Use P01: Predict straight motion, a left arc and pure spin from wheel speeds. The mean rim speed sets translation while the difference divided by track width sets yaw; world displacement must rotate with heading. Connect this result to at least one other listed lesson, identifying the exact quantity, units and assumption transferred across their interface.

## Compare connected mechanisms

Use P12: Recover a sensor transform and check a held-out point. Rigid calibration must preserve distances and orientation; fit rotation and translation jointly and evaluate points outside the fit set. Connect this result to at least one other listed lesson, identifying the exact quantity, units and assumption transferred across their interface.

## Diagnose and recover

Use P26: Compare rigid pose composition with elementwise matrix interpolation. Proper rotations preserve orthogonality and determinant one; translation and rotation composition generally do not commute. Connect this result to at least one other listed lesson, identifying the exact quantity, units and assumption transferred across their interface.

## Integrate and defend the boundary

Use P63: Compare base travel with arm dexterity for one target. Moving the base changes relative target coordinates and arm conditioning; a weighted objective trades travel against singularity avoidance. Connect this result to at least one other listed lesson, identifying the exact quantity, units and assumption transferred across their interface.

## Required integration artifact

Build a frame ledger for a camera point transferred through the robot base to a tool frame. Specify transform direction and distinguish points, free vectors, twists and wrenches. Reconstruct the inverse chain and verify the round-trip error. Transfer the same physical twist between frames and show that wrench–twist power is invariant under the corresponding dual transform. Carry the position and frame convention into the visual-servo lesson; explain why a correct control law with an inverted extrinsic can move in the wrong direction. Include a near-zero rotation and a noncommuting rotation pair. A consistent endpoint alone cannot establish that every intermediate frame was correct.

## Four-criterion rubric

1. Governing reasoning: equations, units and frame/sign conventions justify a numerical prediction; naming an algorithm alone earns no evidence.
2. Controlled comparison: two isolated sweeps and at least one limiting case distinguish mechanisms and make a falsifiable claim.
3. Diagnose and recover: identify the first failing assumption from actual outputs, restore it and demonstrate deterministic recovery.
4. Integration and scope: show the value passed between stages, an independently checked result, and a limitation that prevents a broader claim.

Retain inputs, selected outputs and your explanation as a cumulative artifact. No learner completion, automatic score, physical qualification or production acceptance is recorded.
