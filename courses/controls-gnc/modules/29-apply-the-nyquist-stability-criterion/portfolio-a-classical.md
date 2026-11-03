## Evidence portfolio A-CLASSICAL

This authored assessment joins P03, P05, P06, P07, P08, P27, P28, P29. It records no learner score. Use the linked labs below rather than inventing a single executable model that combines them.

### 1. Model and prediction

Connect visible decay and oscillation to the real and imaginary parts of the displayed poles. Before running, calculate the governing relation and state the assumptions. Then compare your prediction with the actual plotted state, geometry or covariance.

### 2. Transfer and tradeoff

Compare feedback disturbance rejection at zero frequency and at a higher disturbance frequency. Record one change at a time, with units. Explain what knowledge transfers from the first lab and what model assumptions change; equal-looking curves are not evidence that the models are interchangeable.

### 3. Diagnose and recover

Count open-loop unstable poles before interpreting a Nyquist winding around minus one. Enable its named fault, collect the evidence that discriminates the cause, recover at identical inputs and reset. Reconcile the actual requirement, state or history with the claimed recovery.

### 4. Defend the boundary

A finite sampled contour can miss critical behavior, especially near imaginary-axis crossings. Name which additional experiment or external course would be needed to extend this claim. Separate authored reasoning from a measured learner result.

### Four-criterion rubric

- **Model:** derive the chosen relation with conventions, units and an independently worked baseline value.
- **Evidence:** retain parameter values, predictions, actual plots/metrics and two separate control sweeps; explain any disagreement.
- **Diagnosis:** show a causal fault and exact-input recovery, including infeasible, singular or censored outcomes where applicable.
- **Integration and scope:** explain how the named competencies connect and where their models differ; retain all physical and learner-validation exclusions.

A complete portfolio meets all four criteria. Revise incomplete evidence; no aggregate learner pass is inferred from the presence of these instructions.

### Labs and individual reasoning targets

- [P03: Relate Poles to Visible Motion](/courses/controls-gnc/modules/03-relate-poles-to-visible-motion): A negative real part sets exponential decay; conjugate imaginary parts set angular frequency. The same endpoint can occur at different oscillation phases, so use the history and pole locations together.
- [P05: Close a Loop with Proportional Control](/courses/controls-gnc/modules/05-close-a-loop-with-proportional-control): Closing the loop changes the denominator as well as the reference response. A smaller steady error can coexist with larger transient effort, and incorrect feedback sign can destabilize the state.
- [P06: Tune a PID by Observing Each Term](/courses/controls-gnc/modules/06-tune-a-pid-by-observing-each-term): Integral action accumulates error and derivative action responds to the modeled rate. A transient improvement must be interpreted alongside actuator demand; increasing every gain obscures the causal mechanism.
- [P07: See Stability Margin in Time and Frequency](/courses/controls-gnc/modules/07-see-stability-margin-in-time-and-frequency): Added lag changes phase near crossover and can reduce stability margin even if low-frequency gain improves tracking. A positive gain margin alone does not summarize every crossover or delay effect.
- [P08: Reject a Disturbance with Feedback](/courses/controls-gnc/modules/08-reject-a-disturbance-with-feedback): The closed-loop sensitivity attenuates some disturbances but its attenuation varies with frequency. Identify the disturbance injection point before equating an output change to the loop gain.
- [P27: Predict Transients and Steady-State Error from System Type](/courses/controls-gnc/modules/27-predict-transients-and-steady-state-error-from-system-type): Damping changes the decay envelope and ringing; natural frequency scales time. A four-time-constant rule is an estimate, and an unstable response has no legitimate settling-time certification.
- [P28: Trace a Root Locus and Select Feedback Gain](/courses/controls-gnc/modules/28-trace-a-root-locus-and-select-feedback-gain): Closed-loop roots determine nominal linear stability; a root crossing into the right half-plane invalidates a stable design claim even if a short trace is initially small.
- [P29: Apply the Nyquist Stability Criterion](/courses/controls-gnc/modules/29-apply-the-nyquist-stability-criterion): The relation between winding and closed-loop unstable poles depends on the declared contour convention. Verify polynomial pole counting as a separate check; a visually small loop is insufficient.
