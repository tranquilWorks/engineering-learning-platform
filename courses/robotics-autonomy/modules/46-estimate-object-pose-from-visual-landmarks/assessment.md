## P46 evidence task

Why can a low pixel residual coexist with a biased translation estimate?

Before running: Predict whether more visible landmarks can repair a focal-calibration error, and distinguish residual fit from actual pose accuracy.

Collect a default record, one single-control sweep, the named fault and recovery. Record the parameter values, plotted quantities and units so another learner can reproduce the comparison.

Observed and fitted pixels plots Image y (px) against Image x (px). Its series are Observed, Fitted. Pose-fit objective plots Half SSE (px²) against Iteration (count). Its series are Objective.

### Reasoning rubric

- Model: reconstruct a displayed value using `pixel_i=project(R*landmark_i+t); R in SO(3), t in metres` and the actual state or geometry.
- Evidence: Increase pixel-noise amplitude at a fixed landmark count. Compare actual translation, rotation and reprojection errors, and inspect the solver status instead of assuming every local fit has converged.
- Diagnosis: The estimator uses focal length 650 px for observations generated with 800 px. The actual selected points, pixel noise, initializer and positive-depth condition remain unchanged.
- Recovery and scope: Restore focal length 800 px, rerun from the declared initializer and compare the fitted transform, pixel residuals and local rank under the same observations. State this boundary: This solves a local six-degree-of-freedom pose from a near initializer and a synthetic noncoplanar object; it makes no global PnP uniqueness or arbitrary-initialization claim. The noise sequence is deterministic, visible points are selected by a fixed rule, and solver budget or stalling status remains meaningful even when two independent estimates agree closely.

### Check your explanation

Pose can compensate partly for incorrect focal calibration, and noisy data are fitted within the assumed model. Residual consistency is different from agreement with independent metric truth; inspect calibration, geometry and the full transform.

A complete explanation contains a calculation, an observed comparison with units, the executed fault and a reproduced recovery. Name a setting that can hide the fault and a claim requiring evidence outside this model. This is a self-assessment; no learner score is stored.
