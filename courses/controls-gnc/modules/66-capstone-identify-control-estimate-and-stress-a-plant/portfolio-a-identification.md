## Evidence portfolio A-IDENTIFICATION

This authored assessment joins P50, P51, P66. It records no learner score. Use the linked labs below rather than inventing a single executable model that combines them.

### 1. Model and prediction

Show why rich excitation and held-out validation are separate requirements for identification. Before running, calculate the governing relation and state the assumptions. Then compare your prediction with the actual plotted state, geometry or covariance.

### 2. Transfer and tradeoff

Relate recursive least squares estimates and covariance to an independently weighted batch fit. Record one change at a time, with units. Explain what knowledge transfers from the first lab and what model assumptions change; equal-looking curves are not evidence that the models are interchangeable.

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

- [P50: Identify and Validate a Dynamic Model from Excitation Data](/courses/controls-gnc/modules/50-identify-and-validate-a-dynamic-model-from-excitation-data): A low fitting residual can arise from uninformative data or overfitting. Rank and excitation establish identifiability; independent free-run validation checks whether the fitted dynamics predict new behavior.
- [P51: Adapt a Parameter Estimate Online](/courses/controls-gnc/modules/51-adapt-a-parameter-estimate-online): Each RLS update uses a gain and covariance recursion. Forgetting changes the data weights; small covariance without sufficient excitation is not trustworthy certainty about the true parameters.
- [P66: Capstone: Identify, Control, Estimate, and Stress a Plant](/courses/controls-gnc/modules/66-capstone-identify-control-estimate-and-stress-a-plant): Identification rank must support both fitted coefficients. Stress changes the physical model while the design and estimator use the identified model; each requirement derives from recorded state, covariance or control evidence.
