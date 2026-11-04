## Evidence portfolio A-ROBUST

This authored assessment joins P19, P20, P46, P48, P51, P66, P68. It records no learner score. Use the linked labs below rather than inventing a single executable model that combines them.

### 1. Model and prediction

Predict the effect of actual actuator gain and drag mismatch without redesigning the nominal controller. Before running, calculate the governing relation and state the assumptions. Then compare your prediction with the actual plotted state, geometry or covariance.

### 2. Transfer and tradeoff

Compare worst sampled sensitivity over the declared uncertainty interval with the nominal response. Record one change at a time, with units. Explain what knowledge transfers from the first lab and what model assumptions change; equal-looking curves are not evidence that the models are interchangeable.

### 3. Diagnose and recover

Trace each software-HIL verdict to delivered packet timing, dropped commands and expired actuator state. Enable its named fault, collect the evidence that discriminates the cause, recover at identical inputs and reset. Reconcile the actual requirement, state or history with the claimed recovery.

### 4. Defend the boundary

Software event simulation does not measure real buses, operating-system deadlines or physical actuators. Name which additional experiment or external course would be needed to extend this claim. Separate authored reasoning from a measured learner result.

### Four-criterion rubric

- **Model:** derive the chosen relation with conventions, units and an independently worked baseline value.
- **Evidence:** retain parameter values, predictions, actual plots/metrics and two separate control sweeps; explain any disagreement.
- **Diagnosis:** show a causal fault and exact-input recovery, including infeasible, singular or censored outcomes where applicable.
- **Integration and scope:** explain how the named competencies connect and where their models differ; retain all physical and learner-validation exclusions.

A complete portfolio meets all four criteria. Revise incomplete evidence; no aggregate learner pass is inferred from the presence of these instructions.

### Labs and individual reasoning targets

- [P19: Measure Sensitivity to Model Error](/courses/controls-gnc/modules/19-measure-sensitivity-to-model-error): Model error changes the physical loop while the nominal design remains fixed. Compare gain and drag sweeps independently; a robust claim must name the tested uncertainty family and performance measure.
- [P20: Compare Nominal and Robust Designs](/courses/controls-gnc/modules/20-compare-nominal-and-robust-designs): A conservative design can sacrifice nominal speed to maintain acceptable response under a declared mismatch. Compare both at the same physical plant and include effort or tracking penalties.
- [P46: Schedule Gains Across Operating Points](/courses/controls-gnc/modules/46-schedule-gains-across-operating-points): A table and interpolation rule produce an approximation. Sparse sampling can hide error between knots; matching a few endpoint gains does not establish uniform performance over the operating range.
- [P48: Bound Structured Uncertainty and Robust Performance](/courses/controls-gnc/modules/48-bound-structured-uncertainty-and-robust-performance): Robust performance names an uncertainty set and a performance quantity. Dimensionless normalized margins must not mix incompatible units; a sample grid is evidence for that grid, not an exact all-frequency theorem.
- [P51: Adapt a Parameter Estimate Online](/courses/controls-gnc/modules/51-adapt-a-parameter-estimate-online): Each RLS update uses a gain and covariance recursion. Forgetting changes the data weights; small covariance without sufficient excitation is not trustworthy certainty about the true parameters.
- [P66: Capstone: Identify, Control, Estimate, and Stress a Plant](/courses/controls-gnc/modules/66-capstone-identify-control-estimate-and-stress-a-plant): Identification rank must support both fitted coefficients. Stress changes the physical model while the design and estimator use the identified model; each requirement derives from recorded state, covariance or control evidence.
- [P68: Capstone: Verify a Faulted Software-HIL GNC Loop](/courses/controls-gnc/modules/68-capstone-verify-a-faulted-software-hil-gnc-loop): A watchdog must suppress actual applied output when a command expires. Distinguish late delivered packets from dropped source commands, and track the proportional-loop equilibrium rather than assuming unity tracking.
