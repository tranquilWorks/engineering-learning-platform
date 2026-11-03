## Evidence portfolio A-STOCHASTIC

This authored assessment joins P16, P52, P53, P61. It records no learner score. Use the linked labs below rather than inventing a single executable model that combines them.

### 1. Model and prediction

Predict what happens when assumed measurement noise disagrees with the retained noisy sensor stream. Before running, calculate the governing relation and state the assumptions. Then compare your prediction with the actual plotted state, geometry or covariance.

### 2. Transfer and tradeoff

Compare NIS before a gated update and NEES after it using the retained truth trajectory. Record one change at a time, with units. Explain what knowledge transfers from the first lab and what model assumptions change; equal-looking curves are not evidence that the models are interchangeable.

### 3. Diagnose and recover

Trace prior covariance, state-error injection and covariance reset in the actual one-axis filter. Enable its named fault, collect the evidence that discriminates the cause, recover at identical inputs and reset. Reconcile the actual requirement, state or history with the claimed recovery.

### 4. Defend the boundary

This one-axis formulation does not implement a complete inertial ESKF. Name which additional experiment or external course would be needed to extend this claim. Separate authored reasoning from a measured learner result.

### Four-criterion rubric

- **Model:** derive the chosen relation with conventions, units and an independently worked baseline value.
- **Evidence:** retain parameter values, predictions, actual plots/metrics and two separate control sweeps; explain any disagreement.
- **Diagnosis:** show a causal fault and exact-input recovery, including infeasible, singular or censored outcomes where applicable.
- **Integration and scope:** explain how the named competencies connect and where their models differ; retain all physical and learner-validation exclusions.

A complete portfolio meets all four criteria. Revise incomplete evidence; no aggregate learner pass is inferred from the presence of these instructions.

### Labs and individual reasoning targets

- [P16: Fuse Noisy Sensors with a Kalman Filter](/courses/controls-gnc/modules/16-fuse-noisy-sensors-with-a-kalman-filter): Kalman gain balances propagated covariance against assumed measurement covariance. Smaller reported P can mean overconfidence rather than smaller actual error, so inspect innovations and truth error separately.
- [P52: Build Stochastic Process Models and Interpret Covariance](/courses/controls-gnc/modules/52-build-stochastic-process-models-and-interpret-covariance): Positive process noise adds qT to initial variance. The mean can remain unchanged while uncertainty grows; subtracting noise can produce an invalid covariance even if a clipped plot stays finite.
- [P53: Monitor Innovations, NIS, NEES, and Measurement Gates](/courses/controls-gnc/modules/53-monitor-innovations-nis-nees-and-measurement-gates): NIS divides squared innovation by S; NEES divides posterior truth error by P. Bypassing the gate changes the posterior path at the same injection; independent-trial consistency cannot be inferred from deterministic time samples.
- [P61: Inject and Reset a One-Axis Navigation Error State](/courses/controls-gnc/modules/61-fuse-gnss-and-ins-with-an-error-state-kalman-filter): An error estimate must be injected into the nominal state as well as propagated in covariance. A shrinking covariance with an uncorrected nominal error is overconfidence, not successful navigation.
