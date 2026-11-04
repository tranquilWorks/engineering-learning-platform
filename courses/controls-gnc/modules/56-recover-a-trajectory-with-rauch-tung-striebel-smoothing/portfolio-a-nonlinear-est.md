## Evidence portfolio A-NONLINEAR-EST

This authored assessment joins P54, P55, P56. It records no learner score. Use the linked labs below rather than inventing a single executable model that combines them.

### 1. Model and prediction

Calculate the actual EKF state update and nonlinear residual from the selected prior. Before running, calculate the governing relation and state the assumptions. Then compare your prediction with the actual plotted state, geometry or covariance.

### 2. Transfer and tradeoff

Explain the difference between sigma-point mean weights and covariance correction for a squared Gaussian transform. Record one change at a time, with units. Explain what knowledge transfers from the first lab and what model assumptions change; equal-looking curves are not evidence that the models are interchangeable.

### 3. Diagnose and recover

Explain why later measurements can reduce an earlier state's uncertainty in an RTS smoother. Enable its named fault, collect the evidence that discriminates the cause, recover at identical inputs and reset. Reconcile the actual requirement, state or history with the claimed recovery.

### 4. Defend the boundary

The retained scalar random-walk example is not a general navigation smoother. Name which additional experiment or external course would be needed to extend this claim. Separate authored reasoning from a measured learner result.

### Four-criterion rubric

- **Model:** derive the chosen relation with conventions, units and an independently worked baseline value.
- **Evidence:** retain parameter values, predictions, actual plots/metrics and two separate control sweeps; explain any disagreement.
- **Diagnosis:** show a causal fault and exact-input recovery, including infeasible, singular or censored outcomes where applicable.
- **Integration and scope:** explain how the named competencies connect and where their models differ; retain all physical and learner-validation exclusions.

A complete portfolio meets all four criteria. Revise incomplete evidence; no aggregate learner pass is inferred from the presence of these instructions.

### Labs and individual reasoning targets

- [P54: Estimate Nonlinear State with an Extended Kalman Filter](/courses/controls-gnc/modules/54-estimate-nonlinear-state-with-an-extended-kalman-filter): Linearize the measurement at the prior, compute innovation and gain, and update both state and covariance. A zero Jacobian loses first-order information; prior variance is not the nonlinear Taylor residual.
- [P55: Transform Gaussian Uncertainty with Sigma Points](/courses/controls-gnc/modules/55-transform-uncertainty-with-an-unscented-kalman-filter): The squared zero-mean Gaussian has mean sigma squared and variance twice sigma fourth. A missing covariance correction can preserve the mean while corrupting variance; the two weight sums have different roles.
- [P56: Recover a Trajectory with RTS Smoothing](/courses/controls-gnc/modules/56-recover-a-trajectory-with-rauch-tung-striebel-smoothing): A smoother conditions on future data through a backward gain while a filter conditions only on data available at the time. Compare full conditional covariance, not an arbitrary fixed percentage improvement.
