## Evidence portfolio A-OPTIMAL

This authored assessment joins P17, P18, P39, P49. It records no learner score. Use the linked labs below rather than inventing a single executable model that combines them.

### 1. Model and prediction

Compare state-error and control-effort weights while recording both state history and applied control. Before running, calculate the governing relation and state the assumptions. Then compare your prediction with the actual plotted state, geometry or covariance.

### 2. Transfer and tradeoff

Explain why a terminal Riccati boundary must be propagated backward in time. Record one change at a time, with units. Explain what knowledge transfers from the first lab and what model assumptions change; equal-looking curves are not evidence that the models are interchangeable.

### 3. Diagnose and recover

Check applied receding-horizon commands against both optimization feasibility and actual state constraints. Enable its named fault, collect the evidence that discriminates the cause, recover at identical inputs and reset. Reconcile the actual requirement, state or history with the claimed recovery.

### 4. Defend the boundary

This bounded scalar optimizer is not a general nonlinear MPC implementation. Name which additional experiment or external course would be needed to extend this claim. Separate authored reasoning from a measured learner result.

### Four-criterion rubric

- **Model:** derive the chosen relation with conventions, units and an independently worked baseline value.
- **Evidence:** retain parameter values, predictions, actual plots/metrics and two separate control sweeps; explain any disagreement.
- **Diagnosis:** show a causal fault and exact-input recovery, including infeasible, singular or censored outcomes where applicable.
- **Integration and scope:** explain how the named competencies connect and where their models differ; retain all physical and learner-validation exclusions.

A complete portfolio meets all four criteria. Revise incomplete evidence; no aggregate learner pass is inferred from the presence of these instructions.

### Labs and individual reasoning targets

- [P17: Balance State Error and Control Effort with LQR](/courses/controls-gnc/modules/17-balance-state-error-and-control-effort-with-lqr): The LQR objective trades state cost against input cost; larger state weight generally changes gains and effort. It does not impose hard actuator constraints unless those constraints are modeled separately.
- [P18: Use Feedforward and Feedback Together](/courses/controls-gnc/modules/18-use-feedforward-and-feedback-together): Feedforward uses the reference and model to anticipate required effort; feedback corrects measured error. A perfect nominal trace with feedforward alone does not prove rejection of model error.
- [P39: Solve Finite-Horizon and Time-Varying LQR](/courses/controls-gnc/modules/39-solve-finite-horizon-and-time-varying-lqr): The finite-horizon value at the end is prescribed. Starting that value at the beginning solves a different boundary problem; compare the terminal metric and time-varying gain schedule.
- [P49: Control a Constrained Plant with Model-Predictive Control](/courses/controls-gnc/modules/49-control-a-constrained-plant-with-model-predictive-control): MPC repeatedly solves a constrained horizon problem. A decreasing objective does not excuse an infeasible input or state, and finite horizon plus a fallback is not automatically a stability proof.
