## Evidence portfolio A-NAVIGATION

This authored assessment joins P58, P59, P60, P61, P67. It records no learner score. Use the linked labs below rather than inventing a single executable model that combines them.

### 1. Model and prediction

Build the actual two-column calibration regressor and decide whether separate bias uncertainty is available. Before running, calculate the governing relation and state the assumptions. Then compare your prediction with the actual plotted state, geometry or covariance.

### 2. Transfer and tradeoff

Separate position and clock error in a nonlinear synthetic pseudorange solution. Record one change at a time, with units. Explain what knowledge transfers from the first lab and what model assumptions change; equal-looking curves are not evidence that the models are interchangeable.

### 3. Diagnose and recover

Reconcile actual survey position, estimated position, turn limits and stale-navigation hold events. Enable its named fault, collect the evidence that discriminates the cause, recover at identical inputs and reset. Reconcile the actual requirement, state or history with the claimed recovery.

### 4. Defend the boundary

The capstone uses simplified planar position aiding, not raw pseudoranges or full GNSS/INS mechanization. Name which additional experiment or external course would be needed to extend this claim. Separate authored reasoning from a measured learner result.

### Four-criterion rubric

- **Model:** derive the chosen relation with conventions, units and an independently worked baseline value.
- **Evidence:** retain parameter values, predictions, actual plots/metrics and two separate control sweeps; explain any disagreement.
- **Diagnosis:** show a causal fault and exact-input recovery, including infeasible, singular or censored outcomes where applicable.
- **Integration and scope:** explain how the named competencies connect and where their models differ; retain all physical and learner-validation exclusions.

A complete portfolio meets all four criteria. Revise incomplete evidence; no aggregate learner pass is inferred from the presence of these instructions.

### Labs and individual reasoning targets

- [P58: Analyze Navigation Observability and Alignment Calibration](/courses/controls-gnc/modules/58-analyze-navigation-observability-and-alignment-calibration): Information is Y-transpose R-inverse Y. Identical columns have rank one regardless of noise scale; with diverse headings use singular values and the inverse information covariance to quantify sensitivity.
- [P59: Propagate One-Axis Inertial Bias Errors](/courses/controls-gnc/modules/59-propagate-strapdown-inertial-navigation-and-imu-error): Velocity error is bias times time and position error is half bias times time squared. A five-percent residual bias produces five-percent position error; omitting correction leaves the full drift.
- [P60: Solve Position and Clock from Synthetic Pseudoranges](/courses/controls-gnc/modules/60-solve-a-gnss-pseudorange-navigation-fix): Each range measurement contains geometry and a common clock term. Omitting that term forces the solver to absorb timing error into position; residual size alone does not identify the error source.
- [P61: Inject and Reset a One-Axis Navigation Error State](/courses/controls-gnc/modules/61-fuse-gnss-and-ins-with-an-error-state-kalman-filter): An error estimate must be injected into the nominal state as well as propagated in covariance. A shrinking covariance with an uncorrected nominal error is overconfidence, not successful navigation.
- [P67: Capstone: Navigate, Guide, and Constrain an Autonomous Survey](/courses/controls-gnc/modules/67-capstone-navigate-guide-and-constrain-an-autonomous-survey): The planar survey applies LOS guidance and a bounded turn command to a simplified navigation estimate. GNSS age can trigger a hold even if cross-track error is small; inspect each requirement and the executed path.


## Integrated-sequence extension

Complete the integrated assessment in this lesson as well as the component tasks above. For each stage, retain the actual state, innovation, covariance or command history, identify its upstream input and downstream effect, and explain a failed case. Compare nominal, both control sweeps, fault and exact recovery. Use the four-criterion rubric above; do not substitute correct labels for an executed recurrence or frame transformation.
