## Evidence portfolio A-STATE

This authored assessment joins P13, P14, P15, P17, P18, P34, P36, P37. It records no learner score. Use the linked labs below rather than inventing a single executable model that combines them.

### 1. Model and prediction

Use a zero input gain or coupling limit to distinguish controllability rank from control effort. Before running, calculate the governing relation and state the assumptions. Then compare your prediction with the actual plotted state, geometry or covariance.

### 2. Transfer and tradeoff

Show how feedforward changes nominal tracking while feedback reacts to disturbances and mismatch. Record one change at a time, with units. Explain what knowledge transfers from the first lab and what model assumptions change; equal-looking curves are not evidence that the models are interchangeable.

### 3. Diagnose and recover

Compare integral load rejection with the requested and limited command at identical authority. Enable its named fault, collect the evidence that discriminates the cause, recover at identical inputs and reset. Reconcile the actual requirement, state or history with the claimed recovery.

### 4. Defend the boundary

The normalized first-order servo is not a complete second-order mechanical plant. Name which additional experiment or external course would be needed to extend this claim. Separate authored reasoning from a measured learner result.

### Four-criterion rubric

- **Model:** derive the chosen relation with conventions, units and an independently worked baseline value.
- **Evidence:** retain parameter values, predictions, actual plots/metrics and two separate control sweeps; explain any disagreement.
- **Diagnosis:** show a causal fault and exact-input recovery, including infeasible, singular or censored outcomes where applicable.
- **Integration and scope:** explain how the named competencies connect and where their models differ; retain all physical and learner-validation exclusions.

A complete portfolio meets all four criteria. Revise incomplete evidence; no aggregate learner pass is inferred from the presence of these instructions.

### Labs and individual reasoning targets

- [P13: Test Controllability](/courses/controls-gnc/modules/13-test-controllability): The span of B, AB and higher powers identifies reachable directions. A barely nonzero coupling can preserve rank yet make reaching a state poorly conditioned and expensive.
- [P14: Test Observability](/courses/controls-gnc/modules/14-test-observability): Observability involves C, CA and the state dynamics. Longer data may improve an existing weak direction, but identical or absent sensitivities retain a null space.
- [P15: Build a State Observer](/courses/controls-gnc/modules/15-build-a-state-observer): Stable observer error poles govern transient convergence when the model and measurement are valid. A persistent sensor bias is a forced error; faster poles do not make a biased measurement true.
- [P17: Balance State Error and Control Effort with LQR](/courses/controls-gnc/modules/17-balance-state-error-and-control-effort-with-lqr): The LQR objective trades state cost against input cost; larger state weight generally changes gains and effort. It does not impose hard actuator constraints unless those constraints are modeled separately.
- [P18: Use Feedforward and Feedback Together](/courses/controls-gnc/modules/18-use-feedforward-and-feedback-together): Feedforward uses the reference and model to anticipate required effort; feedback corrects measured error. A perfect nominal trace with feedforward alone does not prove rejection of model error.
- [P34: Propagate State Modes and Diagnose Numerical Conditioning](/courses/controls-gnc/modules/34-propagate-state-modes-and-diagnose-numerical-conditioning): Eigenvalues remain stable while nearly parallel eigenvectors amplify coordinate sensitivity and transient cancellation. A tiny reconstruction error is not proof that the modal basis is well conditioned.
- [P36: Place State-Feedback Poles and Track References](/courses/controls-gnc/modules/36-place-state-feedback-poles-and-track-references): Both position and velocity terms contribute acceleration. Changing only the prefilter moves the equilibrium without moving closed-loop poles, so tracking error and pole stability are different tests.
- [P37: Augment an Integral Servo and Limit Commands](/courses/controls-gnc/modules/37-augment-an-integral-servo-and-limit-commands): Integral action can reject a feasible constant load while command saturation prevents impossible equilibria. Track the integral state as well as position; a stable unsaturated design is not enough.
