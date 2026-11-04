## Evidence portfolio A-MIMO

This authored assessment joins P13, P14, P33. It records no learner score. Use the linked labs below rather than inventing a single executable model that combines them.

### 1. Model and prediction

Use a zero input gain or coupling limit to distinguish controllability rank from control effort. Before running, calculate the governing relation and state the assumptions. Then compare your prediction with the actual plotted state, geometry or covariance.

### 2. Transfer and tradeoff

Explain why a longer observation window cannot restore a fundamentally missing measured direction. Record one change at a time, with units. Explain what knowledge transfers from the first lab and what model assumptions change; equal-looking curves are not evidence that the models are interchangeable.

### 3. Diagnose and recover

Compare static decoupling, relative gain and dynamic singular values before choosing channel pairing. Enable its named fault, collect the evidence that discriminates the cause, recover at identical inputs and reset. Reconcile the actual requirement, state or history with the claimed recovery.

### 4. Defend the boundary

This two-input/two-output example is not full control allocation or MIMO robust synthesis. Name which additional experiment or external course would be needed to extend this claim. Separate authored reasoning from a measured learner result.

### Four-criterion rubric

- **Model:** derive the chosen relation with conventions, units and an independently worked baseline value.
- **Evidence:** retain parameter values, predictions, actual plots/metrics and two separate control sweeps; explain any disagreement.
- **Diagnosis:** show a causal fault and exact-input recovery, including infeasible, singular or censored outcomes where applicable.
- **Integration and scope:** explain how the named competencies connect and where their models differ; retain all physical and learner-validation exclusions.

A complete portfolio meets all four criteria. Revise incomplete evidence; no aggregate learner pass is inferred from the presence of these instructions.

### Labs and individual reasoning targets

- [P13: Test Controllability](/courses/controls-gnc/modules/13-test-controllability): The span of B, AB and higher powers identifies reachable directions. A barely nonzero coupling can preserve rank yet make reaching a state poorly conditioned and expensive.
- [P14: Test Observability](/courses/controls-gnc/modules/14-test-observability): Observability involves C, CA and the state dynamics. Longer data may improve an existing weak direction, but identical or absent sensitivities retain a null space.
- [P33: Measure MIMO Interaction, Zeros, and Decoupling](/courses/controls-gnc/modules/33-measure-mimo-interaction-zeros-and-decoupling): A DC inverse can reduce static cross coupling without cancelling dynamic interaction at every frequency. Regularization trades inversion sensitivity against a residual; transmission zeros constrain the attainable behavior.
