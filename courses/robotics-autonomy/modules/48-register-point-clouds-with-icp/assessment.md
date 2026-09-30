## P48 evidence task

Why can an ICP run converge with a small residual and still have a wrong transform?

Before running: Predict whether a falling nearest-neighbour residual establishes correct registration when initialization is poor or correspondences include clutter.

Collect a default record, one single-control sweep, the named fault and recovery. Record the parameter values, plotted quantities and units so another learner can reproduce the comparison.

Registered point clouds plots World y (m) against World x (m). Its series are Target, Moved. ICP objective plots Mean cost (m²) against Update (count). Its series are Objective.

### Reasoning rubric

- Model: reconstruct a displayed value using `nearest_i=argmin_j ||R*source_i+t-target_j||` and the actual state or geometry.
- Evidence: Increase initial translation offset with outlier fraction fixed. Compare convergence status, objective descent and truth-based transform error; look for a finite wrong local fit or the maximum iteration budget.
- Diagnosis: The estimator disables the 0.5 m correspondence gate and includes every source point in each nearest-neighbour rigid fit.
- Recovery and scope: Restore the gate, restart from the same initial transform and compare the final rigid transform, accepted correspondence set and executed iteration history. State this boundary: The problem is planar SE(2), uses a fixed local initializer family and can reach a wrong local alignment or its iteration budget. Zero clutter can hide the rejection fault. A decreasing nearest-neighbour objective or tiny final increment does not establish the correct physical correspondence or a global optimum.

### Check your explanation

Nearest-neighbour assignments and rigid fitting optimize a local objective. A wrong correspondence pattern can be self-consistent and produce tiny updates; independent geometry, initialization limits and truth-based evaluation are separate checks.

A complete explanation contains a calculation, an observed comparison with units, the executed fault and a reproduced recovery. Name a setting that can hide the fault and a claim requiring evidence outside this model. This is a self-assessment; no learner score is stored.
