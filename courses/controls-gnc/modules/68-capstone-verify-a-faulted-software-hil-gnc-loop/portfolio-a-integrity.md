## Evidence portfolio A-INTEGRITY

This authored assessment joins P62, P67, P68. It records no learner score. Use the linked labs below rather than inventing a single executable model that combines them.

### 1. Model and prediction

Compare actual residual-based detection and exclusion with the refitted solution and alarm threshold. Before running, calculate the governing relation and state the assumptions. Then compare your prediction with the actual plotted state, geometry or covariance.

### 2. Transfer and tradeoff

Reconcile actual survey position, estimated position, turn limits and stale-navigation hold events. Record one change at a time, with units. Explain what knowledge transfers from the first lab and what model assumptions change; equal-looking curves are not evidence that the models are interchangeable.

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

- [P62: Detect and Exclude a Synthetic Range Fault](/courses/controls-gnc/modules/62-monitor-navigation-integrity-and-exclude-faulty-measurements): Redundancy permits inconsistency detection under stated geometry. Excluding a suspect row changes the fitted position and residual structure; distinguish a synthetic threshold from a certified protection level.
- [P67: Capstone: Navigate, Guide, and Constrain an Autonomous Survey](/courses/controls-gnc/modules/67-capstone-navigate-guide-and-constrain-an-autonomous-survey): The planar survey applies LOS guidance and a bounded turn command to a simplified navigation estimate. GNSS age can trigger a hold even if cross-track error is small; inspect each requirement and the executed path.
- [P68: Capstone: Verify a Faulted Software-HIL GNC Loop](/courses/controls-gnc/modules/68-capstone-verify-a-faulted-software-hil-gnc-loop): A watchdog must suppress actual applied output when a command expires. Distinguish late delivered packets from dropped source commands, and track the proportional-loop equilibrium rather than assuming unity tracking.
