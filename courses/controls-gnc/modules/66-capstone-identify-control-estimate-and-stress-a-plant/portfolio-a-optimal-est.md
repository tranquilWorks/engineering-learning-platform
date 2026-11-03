## Evidence portfolio A-OPTIMAL-EST

This authored assessment joins P15, P16, P17, P38, P66. It records no learner score. Use the linked labs below rather than inventing a single executable model that combines them.

### 1. Model and prediction

Balance observer pole speed against a fixed sensor bias and explain the actual error trace. Before running, calculate the governing relation and state the assumptions. Then compare your prediction with the actual plotted state, geometry or covariance.

### 2. Transfer and tradeoff

Compare state-error and control-effort weights while recording both state history and applied control. Record one change at a time, with units. Explain what knowledge transfers from the first lab and what model assumptions change; equal-looking curves are not evidence that the models are interchangeable.

### 3. Diagnose and recover

Trace excitation, identified model, redesigned controller and estimator into the held-out stress histories. Enable its named fault, collect the evidence that discriminates the cause, recover at identical inputs and reset. Reconcile the actual requirement, state or history with the claimed recovery.

### 4. Defend the boundary

A scalar synthetic identification/control/estimation loop is not full vehicle dynamics or robust certification. Name which additional experiment or external course would be needed to extend this claim. Separate authored reasoning from a measured learner result.

### Four-criterion rubric

- **Model:** derive the chosen relation with conventions, units and an independently worked baseline value.
- **Evidence:** retain parameter values, predictions, actual plots/metrics and two separate control sweeps; explain any disagreement.
- **Diagnosis:** show a causal fault and exact-input recovery, including infeasible, singular or censored outcomes where applicable.
- **Integration and scope:** explain how the named competencies connect and where their models differ; retain all physical and learner-validation exclusions.

A complete portfolio meets all four criteria. Revise incomplete evidence; no aggregate learner pass is inferred from the presence of these instructions.

### Labs and individual reasoning targets

- [P15: Build a State Observer](/courses/controls-gnc/modules/15-build-a-state-observer): Stable observer error poles govern transient convergence when the model and measurement are valid. A persistent sensor bias is a forced error; faster poles do not make a biased measurement true.
- [P16: Fuse Noisy Sensors with a Kalman Filter](/courses/controls-gnc/modules/16-fuse-noisy-sensors-with-a-kalman-filter): Kalman gain balances propagated covariance against assumed measurement covariance. Smaller reported P can mean overconfidence rather than smaller actual error, so inspect innovations and truth error separately.
- [P17: Balance State Error and Control Effort with LQR](/courses/controls-gnc/modules/17-balance-state-error-and-control-effort-with-lqr): The LQR objective trades state cost against input cost; larger state weight generally changes gains and effort. It does not impose hard actuator constraints unless those constraints are modeled separately.
- [P38: Combine LQR and an Observer with the Separation Principle](/courses/controls-gnc/modules/38-combine-lqr-and-an-observer-with-the-separation-principle): The separation principle joins regulator and estimator modes under its assumptions. An unstable observer can spoil the actual estimated-state feedback trajectory despite stable regulator modes.
- [P66: Capstone: Identify, Control, Estimate, and Stress a Plant](/courses/controls-gnc/modules/66-capstone-identify-control-estimate-and-stress-a-plant): Identification rank must support both fitted coefficients. Stress changes the physical model while the design and estimator use the identified model; each requirement derives from recorded state, covariance or control evidence.
