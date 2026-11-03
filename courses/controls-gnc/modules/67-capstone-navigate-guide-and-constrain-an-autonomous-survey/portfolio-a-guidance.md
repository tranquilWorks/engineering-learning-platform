## Evidence portfolio A-GUIDANCE

This authored assessment joins P21, P22, P63, P64, P65, P67. It records no learner score. Use the linked labs below rather than inventing a single executable model that combines them.

### 1. Model and prediction

Check whether changing distance or move duration violates the generated trajectory's limits. Before running, calculate the governing relation and state the assumptions. Then compare your prediction with the actual plotted state, geometry or covariance.

### 2. Transfer and tradeoff

Explain the different moving-beacon guidance paths using the actual relative geometry. Record one change at a time, with units. Explain what knowledge transfers from the first lab and what model assumptions change; equal-looking curves are not evidence that the models are interchangeable.

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

- [P21: Generate a Feasible Trajectory](/courses/controls-gnc/modules/21-generate-a-feasible-trajectory): Time scaling changes velocity and acceleration at different powers of duration. A geometrically smooth reference may still demand infeasible actuator authority; check each derivative with its units.
- [P22: Implement Proportional Navigation](/courses/controls-gnc/modules/22-implement-proportional-navigation): The modeled acceleration uses a navigation constant, closing speed and line-of-sight rate. State the closing/angle conventions before interpreting a miss distance or saturation event.
- [P63: Follow a Straight Path with Nonlinear Line-of-Sight Guidance](/courses/controls-gnc/modules/63-follow-waypoints-and-paths-with-line-of-sight-guidance): The actual heading is minus atan(y/L); lateral speed is V times its sine. Exponential decay is valid only for small y/L, and reversing the sign causes growing error with a changing peak heading.
- [P64: Compare Civilian Moving-Beacon Guidance Trajectories](/courses/controls-gnc/modules/64-compare-pursuit-laws-and-proportional-navigation-variants): Closing speed, line-of-sight rate and turning geometry govern the trajectory. Compare bounded civilian synthetic paths under the same initial conditions rather than treating a smaller endpoint distance as universal superiority.
- [P65: Solve a Bounded Terminal Guidance Objective](/courses/controls-gnc/modules/65-enforce-terminal-and-actuator-aware-guidance-constraints): A finite control horizon trades terminal error against limits. If the desired terminal state is infeasible, report the residual and active bounds rather than silently declaring success from solver convergence.
- [P67: Capstone: Navigate, Guide, and Constrain an Autonomous Survey](/courses/controls-gnc/modules/67-capstone-navigate-guide-and-constrain-an-autonomous-survey): The planar survey applies LOS guidance and a bounded turn command to a simplified navigation estimate. GNSS age can trigger a hold even if cross-track error is small; inspect each requirement and the executed path.


## Integrated-sequence extension

Complete the integrated assessment in this lesson as well as the component tasks above. For each stage, retain the actual state, innovation, covariance or command history, identify its upstream input and downstream effect, and explain a failed case. Compare nominal, both control sweeps, fault and exact recovery. Use the four-criterion rubric above; do not substitute correct labels for an executed recurrence or frame transformation.
