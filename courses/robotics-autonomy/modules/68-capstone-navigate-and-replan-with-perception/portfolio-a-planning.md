# A-PLANNING integration evidence

Integrate these existing lessons: P07, P17, P18, P19, P33, P54, P55, P56, P57, P58, P59, P60, P68.

Required evidence: Completeness boundary, collision clearance, cost improvement, dynamic feasibility, prediction, and fallback checks.

## Derive and predict

Use P07: Compute endpoint velocity and acceleration for the displayed trajectory. Differentiate the interpolation polynomial and check endpoints, extrema and physical units; sample spacing alone does not guarantee smooth motion. Connect this result to at least one other listed lesson, identifying the exact quantity, units and assumption transferred across their interface.

## Compare connected mechanisms

Use P33: Find the trajectory duration required by both speed and acceleration limits. Time scaling changes first derivatives inversely with duration and second derivatives inversely with duration squared. Connect this result to at least one other listed lesson, identifying the exact quantity, units and assumption transferred across their interface.

## Diagnose and recover

Use P57: Check swept clearance after removing intermediate waypoints. A shortcut can cross an inflated obstacle even when its endpoints are free; re-evaluate the full segment after smoothing. Connect this result to at least one other listed lesson, identifying the exact quantity, units and assumption transferred across their interface.

## Integrate and defend the boundary

Use P68: Connect a sensor observation to map, state estimate, route and executed motion. Map and estimator outputs must feed planning and control; assess freshness, swept clearance, goal progress and recovery separately. Connect this result to at least one other listed lesson, identifying the exact quantity, units and assumption transferred across their interface.

## Required integration artifact

Compare graph, sampling and kinodynamic representations using the same distinction between geometric feasibility and executable motion. Retain a path cost, continuous segment clearance and terminal velocity rather than only a success flag. Demonstrate the finite-lattice no-plan case at acceleration 3 m/s² and speed 1 m/s, explaining why the first positive lattice edge is excluded without proving continuous-space impossibility. Connect P68 waypoints to its bounded-acceleration tracker and compare the planned route with actual position. Use an obstacle crossing to separate prediction from a frozen obstacle assumption. State the discretization, horizon and footprint boundaries of every clearance claim.

## Four-criterion rubric

1. Governing reasoning: equations, units and frame/sign conventions justify a numerical prediction; naming an algorithm alone earns no evidence.
2. Controlled comparison: two isolated sweeps and at least one limiting case distinguish mechanisms and make a falsifiable claim.
3. Diagnose and recover: identify the first failing assumption from actual outputs, restore it and demonstrate deterministic recovery.
4. Integration and scope: show the value passed between stages, an independently checked result, and a limitation that prevents a broader claim.

Retain inputs, selected outputs and your explanation as a cumulative artifact. No learner completion, automatic score, physical qualification or production acceptance is recorded.
