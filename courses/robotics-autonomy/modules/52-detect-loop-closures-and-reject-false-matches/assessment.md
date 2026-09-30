## P52 evidence task

Why are geometric rejection and a robust loss complementary rather than interchangeable?

Before running: Predict whether a high appearance score is enough to justify moving a map, and distinguish rejecting a loop from reducing the influence of an accepted loop.

Collect a default record, one single-control sweep, the named fault and recovery. Record the parameter values, plotted quantities and units so another learner can reproduce the comparison.

Anchored position graph plots World y (m) against World x (m). Its series are Baseline, Updated. Loop-induced displacement plots Displacement (m) against Node index (1). Its series are Shift.

### Reasoning rubric

- Model: reconstruct a displayed value using `objective=0.5*sum(||position_j-position_i-odometry_ij||²/sigma_odom²)+score*Huber(||closure_residual||/sigma_closure)` and the actual state or geometry.
- Evidence: Increase appearance score while holding innovation fixed, including values on both sides of 0.70. Separate the discrete insertion decision from the continuous influence of an accepted factor.
- Diagnosis: The system keeps the appearance gate but skips geometric rejection and replaces robust closure influence with a quadratic loss. Both selected controls and all odometry factors remain intact.
- Recovery and scope: Restore geometric gating and Huber influence, solve again from the same odometry graph and confirm the anchor, residuals and node displacements. State this boundary: This is an anchored two-dimensional translation graph with an externally supplied appearance score, not full rotational SLAM or image-based loop recognition. Rejected factors and zero innovation leave the baseline unchanged. A robust loss limits damage but does not prove that an accepted factor identifies the correct physical place.

### Check your explanation

A gate decides whether a factor enters the graph at all; a robust loss controls how an inserted factor influences the fitted states. Neither alone proves place identity, and a high appearance score cannot replace geometric consistency.

A complete explanation contains a calculation, an observed comparison with units, the executed fault and a reproduced recovery. Name a setting that can hide the fault and a claim requiring evidence outside this model. This is a self-assessment; no learner score is stored.
