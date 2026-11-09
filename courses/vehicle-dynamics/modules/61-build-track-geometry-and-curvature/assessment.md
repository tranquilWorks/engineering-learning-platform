# P61 course checkpoint

## Predict and derive

Check ellipse curvature analytically and distinguish chord-length convergence from exact arc length.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `x=a cos(theta), y=0.6a sin(theta) in m`
- `kappa=ab/(a^2 sin(theta)^2+b^2 cos(theta)^2)^(3/2) in 1/m`
- `L=sum chord lengths; integral kappa ds -> 2pi rad as sampling increases`

## Controlled comparison

- `major_radius_m`: 60 → 40. Hold the other controls at baseline; predict and explain the change before executing.
- `point_count`: 181 → 301. Hold the other controls at baseline; predict and explain the change before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

For a=60 m and b=36 m, curvature at theta=0 is a/b²=0.0462963 1/m; at pi/2 it is b/a²=0.01 1/m. Curvature integrated around a closed convex curve tends to 2*pi, while polygonal chord length approaches the smooth perimeter as sampling increases. Retain the closure gap and refinement error. A partial 1.8*pi traversal cannot claim full-lap closure merely because its points lie on the ellipse.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

This flat analytic track omits survey uncertainty, banking, elevation, width and obstacles.

Competency links: VD-PERFORMANCE-OPTIMIZATION. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
