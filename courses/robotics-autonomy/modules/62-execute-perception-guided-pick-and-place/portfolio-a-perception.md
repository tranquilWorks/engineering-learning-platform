# Cumulative portfolio A-PERCEPTION

Integrate these existing lessons: P09, P10, P11, P12, P41, P42, P43, P44, P45, P46, P47, P48, P62.

Required evidence: Projection, reprojection, distortion, repeatability, inlier, depth, pose, occupancy, and registration residuals.

## Derive and predict

Use P09: Estimate encoder resolution and the speed ripple caused by quantization. Position increments are discrete counts; differentiation divides quantization error by sample time and can amplify it. Connect this result to at least one other listed lesson, identifying the exact quantity, units and assumption transferred across their interface.

## Compare connected mechanisms

Use P41: Predict pixel motion from depth and camera pose. Perspective division follows the camera frame; points behind or too near the image plane require explicit handling. Connect this result to at least one other listed lesson, identifying the exact quantity, units and assumption transferred across their interface.

## Diagnose and recover

Use P45: Predict depth uncertainty as disparity approaches zero. Triangulation couples baseline, focal scale and disparity; far-range depth becomes sensitive even when pixel residuals stay small. Connect this result to at least one other listed lesson, identifying the exact quantity, units and assumption transferred across their interface.

## Integrate and defend the boundary

Use P62: Trace observation, approach, grasp verification, transfer and release. Every task transition must follow measured geometric or contact evidence; endpoint reachability alone cannot prove placement. Connect this result to at least one other listed lesson, identifying the exact quantity, units and assumption transferred across their interface.

## Four-criterion rubric

1. Governing reasoning: equations, units and frame/sign conventions justify a numerical prediction; naming an algorithm alone earns no evidence.
2. Controlled comparison: two isolated sweeps and at least one limiting case distinguish mechanisms and make a falsifiable claim.
3. Diagnose and recover: identify the first failing assumption from actual outputs, restore it and demonstrate deterministic recovery.
4. Integration and scope: show the value passed between stages, an independently checked result, and a limitation that prevents a broader claim.

Retain inputs, selected outputs and your explanation as a cumulative artifact. No learner completion, automatic score, physical qualification or production acceptance is recorded.
