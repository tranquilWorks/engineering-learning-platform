## Evidence portfolio A-CONSTRAINTS

This authored assessment joins P11, P12, P21, P37, P45, P49, P65, P67. It records no learner score. Use the linked labs below rather than inventing a single executable model that combines them.

### 1. Model and prediction

Determine when a requested command is feasible and trace the plant driven by its applied value. Before running, calculate the governing relation and state the assumptions. Then compare your prediction with the actual plotted state, geometry or covariance.

### 2. Transfer and tradeoff

Compare a barrier condition evaluated along the actual state trajectory with the nominal command. Record one change at a time, with units. Explain what knowledge transfers from the first lab and what model assumptions change; equal-looking curves are not evidence that the models are interchangeable.

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

- [P11: Drive an Actuator into Saturation](/courses/controls-gnc/modules/11-drive-an-actuator-into-saturation): The actuator limit bounds applied command rather than requested command. Tracking can fail despite nominally stable poles if sufficient control authority is unavailable.
- [P12: Recover from Integrator Windup](/courses/controls-gnc/modules/12-recover-from-integrator-windup): The integrator retains its history during saturation; anti-windup feeds back the request/applied discrepancy. Recovery should compare the same demand duration and limit, not a more favorable test.
- [P21: Generate a Feasible Trajectory](/courses/controls-gnc/modules/21-generate-a-feasible-trajectory): Time scaling changes velocity and acceleration at different powers of duration. A geometrically smooth reference may still demand infeasible actuator authority; check each derivative with its units.
- [P37: Augment an Integral Servo and Limit Commands](/courses/controls-gnc/modules/37-augment-an-integral-servo-and-limit-commands): Integral action can reject a feasible constant load while command saturation prevents impossible equilibria. Track the integral state as well as position; a stable unsaturated design is not enough.
- [P45: Enforce Safety with a Control Barrier Filter](/courses/controls-gnc/modules/45-enforce-safety-with-a-control-barrier-filter): A safety filter must recompute its constraint at each evolving state. Check feasibility and realized barrier margin rather than assuming a projected command guarantees all future motion.
- [P49: Control a Constrained Plant with Model-Predictive Control](/courses/controls-gnc/modules/49-control-a-constrained-plant-with-model-predictive-control): MPC repeatedly solves a constrained horizon problem. A decreasing objective does not excuse an infeasible input or state, and finite horizon plus a fallback is not automatically a stability proof.
- [P65: Solve a Bounded Terminal Guidance Objective](/courses/controls-gnc/modules/65-enforce-terminal-and-actuator-aware-guidance-constraints): A finite control horizon trades terminal error against limits. If the desired terminal state is infeasible, report the residual and active bounds rather than silently declaring success from solver convergence.
- [P67: Capstone: Navigate, Guide, and Constrain an Autonomous Survey](/courses/controls-gnc/modules/67-capstone-navigate-guide-and-constrain-an-autonomous-survey): The planar survey applies LOS guidance and a bounded turn command to a simplified navigation estimate. GNSS age can trigger a hold even if cross-track error is small; inspect each requirement and the executed path.
