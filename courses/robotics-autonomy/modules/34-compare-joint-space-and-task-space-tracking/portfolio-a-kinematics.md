# A-KINEMATICS integration evidence

Integrate these existing lessons: P03, P04, P28, P29, P34.

Required evidence: Forward/inverse residuals, branch choices, Jacobian finite differences, singular values, and null-space invariants.

## Derive and predict

Use P03: Predict the endpoint with the elbow straight and then folded. Ordered rotations produce a sum of link vectors; equal links can cancel at a folded elbow although joint angles remain finite. Connect this result to at least one other listed lesson, identifying the exact quantity, units and assumption transferred across their interface.

## Compare connected mechanisms

Use P04: Explain why an unreachable target must be rejected before clipping the cosine. The annular workspace has both inner and outer boundaries; elbow branches can share an endpoint while differing in joint configuration. Connect this result to at least one other listed lesson, identifying the exact quantity, units and assumption transferred across their interface.

## Diagnose and recover

Use P29: Separate desired task velocity from secondary null-space motion. The projector should suppress the secondary task-space contribution; damping alters the primary inverse and its residual. Connect this result to at least one other listed lesson, identifying the exact quantity, units and assumption transferred across their interface.

## Integrate and defend the boundary

Use P34: Compare joint-space tracking with task-space error under the same plant. Joint errors map through geometry; task commands need a consistent Jacobian and can demand large rates near singularity. Connect this result to at least one other listed lesson, identifying the exact quantity, units and assumption transferred across their interface.

## Required integration artifact

Use one reachable arm target to compare inverse-kinematics branches, then verify both branches through forward kinematics. Transfer one branch into its Jacobian and compare a small joint perturbation with the predicted Cartesian displacement. Sweep toward a singular configuration and connect the smallest singular value to commanded joint speed. Add a null-space motion and measure the residual task-space motion at finite step size. Report which results are first-order approximations and which are exact geometry. For the coupled mobile/arm example, list the frame and unit of every velocity passed between subsystems.

## Four-criterion rubric

1. Governing reasoning: equations, units and frame/sign conventions justify a numerical prediction; naming an algorithm alone earns no evidence.
2. Controlled comparison: two isolated sweeps and at least one limiting case distinguish mechanisms and make a falsifiable claim.
3. Diagnose and recover: identify the first failing assumption from actual outputs, restore it and demonstrate deterministic recovery.
4. Integration and scope: show the value passed between stages, an independently checked result, and a limitation that prevents a broader claim.

Retain inputs, selected outputs and your explanation as a cumulative artifact. No learner completion, automatic score, physical qualification or production acceptance is recorded.
