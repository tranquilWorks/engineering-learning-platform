# A-CAP-MOBILE integration evidence

Integrate these existing lessons: P16, P19, P24, P47, P48, P50, P51, P52, P53, P59, P60, P66, P67, P68.

Required evidence: Reused perception, mapping, localization, replanning, local avoidance, monitoring, replay, and recovery artifacts.

## Derive and predict

Use P16: Identify the unknown landmark and the global translation gauge. Odometry constrains differences; landmark observations couple pose and map variables; one absolute anchor removes the common translation ambiguity. Connect this result to at least one other listed lesson, identifying the exact quantity, units and assumption transferred across their interface.

## Compare connected mechanisms

Use P48: Separate nearest-neighbor association from rigid-transform fitting. ICP alternates correspondences and pose updates; residual reduction depends on initialization and overlap. Connect this result to at least one other listed lesson, identifying the exact quantity, units and assumption transferred across their interface.

## Diagnose and recover

Use P59: Reconstruct position and velocity from every bounded acceleration action. A kinodynamic state includes velocity; reaching the target at nonzero speed is a different goal from terminal rest. Connect this result to at least one other listed lesson, identifying the exact quantity, units and assumption transferred across their interface.

## Integrate and defend the boundary

Use P68: Connect a sensor observation to map, state estimate, route and executed motion. Map and estimator outputs must feed planning and control; assess freshness, swept clearance, goal progress and recovery separately. Connect this result to at least one other listed lesson, identifying the exact quantity, units and assumption transferred across their interface.

## Required integration artifact

Submit a stage ledger linking observation → occupancy odds → route → estimated state/covariance → acceleration command → actual trajectory → freshness hold/resume. Record the numerical quantity and units passed at each arrow. At baseline, identify the occupancy threshold crossing, actual detour, hold interval, resumed motion, final error and continuous clearance. Increase dropout alone and explain covariance growth and braking. Change obstacle speed alone and determine whether it intersects the arrival interval or is inactive in that regime. In broken mode show that arrival can coexist with collision. Compare the original ideal-segment component study with the tracked extension; neither runs P51 full SLAM or models a finite vehicle footprint. Acceptance requires the bounded stage claims, not merely a green goal flag.

## Four-criterion rubric

1. Governing reasoning: equations, units and frame/sign conventions justify a numerical prediction; naming an algorithm alone earns no evidence.
2. Controlled comparison: two isolated sweeps and at least one limiting case distinguish mechanisms and make a falsifiable claim.
3. Diagnose and recover: identify the first failing assumption from actual outputs, restore it and demonstrate deterministic recovery.
4. Integration and scope: show the value passed between stages, an independently checked result, and a limitation that prevents a broader claim.

Retain inputs, selected outputs and your explanation as a cumulative artifact. No learner completion, automatic score, physical qualification or production acceptance is recorded.
