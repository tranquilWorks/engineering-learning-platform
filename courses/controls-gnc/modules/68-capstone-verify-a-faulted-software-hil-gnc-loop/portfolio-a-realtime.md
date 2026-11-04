## Evidence portfolio A-REALTIME

This authored assessment joins P23, P24, P33, P41, P68. It records no learner score. Use the linked labs below rather than inventing a single executable model that combines them.

### 1. Model and prediction

Trace how a sensor lag and actuator lag alter the measured and applied paths separately. Before running, calculate the governing relation and state the assumptions. Then compare your prediction with the actual plotted state, geometry or covariance.

### 2. Transfer and tradeoff

Compare static decoupling, relative gain and dynamic singular values before choosing channel pairing. Record one change at a time, with units. Explain what knowledge transfers from the first lab and what model assumptions change; equal-looking curves are not evidence that the models are interchangeable.

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

- [P23: Model Sensor and Actuator Dynamics](/courses/controls-gnc/modules/23-model-sensor-and-actuator-dynamics): The controller acts on delayed measurement and drives a lagged actuator. Their phase and amplitude effects occur at different loop locations, so matching time constants does not make them interchangeable.
- [P24: Close the Loop Through a Hardware-in-the-Loop Plant](/courses/controls-gnc/modules/24-close-the-loop-through-a-hardware-in-the-loop-plant): A controller period and one-way latency affect command arrival and sample age. A simulated plant loop can validate its timing model and recovery logic while leaving real buses and devices entirely untested.
- [P33: Measure MIMO Interaction, Zeros, and Decoupling](/courses/controls-gnc/modules/33-measure-mimo-interaction-zeros-and-decoupling): A DC inverse can reduce static cross coupling without cancelling dynamic interaction at every frequency. Regularization trades inversion sensitivity against a residual; transmission zeros constrain the attainable behavior.
- [P41: Cross Rate Transitions and Execution Delay](/courses/controls-gnc/modules/41-cross-rate-transitions-and-execution-delay): A held sample accumulates age within its rate period; transport/execution delay adds another contribution. A nominal phase-lag number alone does not prove data freshness for every tick.
- [P68: Capstone: Verify a Faulted Software-HIL GNC Loop](/courses/controls-gnc/modules/68-capstone-verify-a-faulted-software-hil-gnc-loop): A watchdog must suppress actual applied output when a command expires. Distinguish late delivered packets from dropped source commands, and track the proportional-loop equilibrium rather than assuming unity tracking.
