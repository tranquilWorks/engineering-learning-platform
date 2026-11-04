## Evidence portfolio A-DIGITAL

This authored assessment joins P09, P10, P11, P12, P23, P35, P37, P40, P41, P42. It records no learner score. Use the linked labs below rather than inventing a single executable model that combines them.

### 1. Model and prediction

Predict how controller sample period changes a discrete integral update and the actual closed-loop path. Before running, calculate the governing relation and state the assumptions. Then compare your prediction with the actual plotted state, geometry or covariance.

### 2. Transfer and tradeoff

Compare exact ZOH, Euler pole mapping and alias-equivalent sampled tones at the same sample interval. Record one change at a time, with units. Explain what knowledge transfers from the first lab and what model assumptions change; equal-looking curves are not evidence that the models are interchangeable.

### 3. Diagnose and recover

Predict the command jump when switching from manual to automatic control and explain the recovery criterion. Enable its named fault, collect the evidence that discriminates the cause, recover at identical inputs and reset. Reconcile the actual requirement, state or history with the claimed recovery.

### 4. Defend the boundary

A censored recovery is a lower bound on time, not an exact settling measurement. Name which additional experiment or external course would be needed to extend this claim. Separate authored reasoning from a measured learner result.

### Four-criterion rubric

- **Model:** derive the chosen relation with conventions, units and an independently worked baseline value.
- **Evidence:** retain parameter values, predictions, actual plots/metrics and two separate control sweeps; explain any disagreement.
- **Diagnosis:** show a causal fault and exact-input recovery, including infeasible, singular or censored outcomes where applicable.
- **Integration and scope:** explain how the named competencies connect and where their models differ; retain all physical and learner-validation exclusions.

A complete portfolio meets all four criteria. Revise incomplete evidence; no aggregate learner pass is inferred from the presence of these instructions.

### Labs and individual reasoning targets

- [P09: Discretize a Continuous Controller](/courses/controls-gnc/modules/09-discretize-a-continuous-controller): Integral accumulation includes the sample interval; omitting or misapplying it changes the effective gain. Compare identical physical time spans rather than equal sample counts only.
- [P10: Expose Delay and Sampling Limits](/courses/controls-gnc/modules/10-expose-delay-and-sampling-limits): Time delay adds frequency-dependent phase; a fast sample rate does not remove an independent transport delay. Interpret failure using the actual delayed path instead of nominal continuous poles.
- [P11: Drive an Actuator into Saturation](/courses/controls-gnc/modules/11-drive-an-actuator-into-saturation): The actuator limit bounds applied command rather than requested command. Tracking can fail despite nominally stable poles if sufficient control authority is unavailable.
- [P12: Recover from Integrator Windup](/courses/controls-gnc/modules/12-recover-from-integrator-windup): The integrator retains its history during saturation; anti-windup feeds back the request/applied discrepancy. Recovery should compare the same demand duration and limit, not a more favorable test.
- [P23: Model Sensor and Actuator Dynamics](/courses/controls-gnc/modules/23-model-sensor-and-actuator-dynamics): The controller acts on delayed measurement and drives a lagged actuator. Their phase and amplitude effects occur at different loop locations, so matching time constants does not make them interchangeable.
- [P35: Compare Discretization Methods and Aliasing](/courses/controls-gnc/modules/35-compare-discretization-methods-and-aliasing): The exact scalar pole is exp(aT), whereas Euler uses 1+aT. A stable continuous pole can map to an unstable Euler pole; sampled sinusoidal frequency is ambiguous modulo sampling frequency.
- [P37: Augment an Integral Servo and Limit Commands](/courses/controls-gnc/modules/37-augment-an-integral-servo-and-limit-commands): Integral action can reject a feasible constant load while command saturation prevents impossible equilibria. Track the integral state as well as position; a stable unsaturated design is not enough.
- [P40: Quantify Quantization and Sampling Jitter](/courses/controls-gnc/modules/40-quantify-quantization-and-sampling-jitter): Quantization error shrinks with code spacing, but timing error depends on waveform slope and jitter. Separate the two error traces before assigning combined SNR improvement to resolution.
- [P41: Cross Rate Transitions and Execution Delay](/courses/controls-gnc/modules/41-cross-rate-transitions-and-execution-delay): A held sample accumulates age within its rate period; transport/execution delay adds another contribution. A nominal phase-lag number alone does not prove data freshness for every tick.
- [P42: Switch Controllers Bumplessly with Anti-Windup](/courses/controls-gnc/modules/42-switch-controllers-bumplessly-with-anti-windup): Bumpless transfer initializes integral state to match the existing command. Anti-windup then uses the actual saturation discrepancy; a recovery beyond the finite observation window is censored, not an observed success.
