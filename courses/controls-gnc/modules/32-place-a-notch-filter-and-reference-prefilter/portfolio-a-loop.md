## Evidence portfolio A-LOOP

This authored assessment joins P07, P08, P19, P30, P31, P32. It records no learner score. Use the linked labs below rather than inventing a single executable model that combines them.

### 1. Model and prediction

Reconcile a time-response oscillation with the loop margin and actuator-lag change. Before running, calculate the governing relation and state the assumptions. Then compare your prediction with the actual plotted state, geometry or covariance.

### 2. Transfer and tradeoff

Measure sensitivity, complementary sensitivity and effort together while shaping the loop. Record one change at a time, with units. Explain what knowledge transfers from the first lab and what model assumptions change; equal-looking curves are not evidence that the models are interchangeable.

### 3. Diagnose and recover

Place the notch relative to the actual resonance and distinguish it from a reference prefilter. Enable its named fault, collect the evidence that discriminates the cause, recover at identical inputs and reset. Reconcile the actual requirement, state or history with the claimed recovery.

### 4. Defend the boundary

The fixed resonance model omits uncertainty and changing structural modes. Name which additional experiment or external course would be needed to extend this claim. Separate authored reasoning from a measured learner result.

### Four-criterion rubric

- **Model:** derive the chosen relation with conventions, units and an independently worked baseline value.
- **Evidence:** retain parameter values, predictions, actual plots/metrics and two separate control sweeps; explain any disagreement.
- **Diagnosis:** show a causal fault and exact-input recovery, including infeasible, singular or censored outcomes where applicable.
- **Integration and scope:** explain how the named competencies connect and where their models differ; retain all physical and learner-validation exclusions.

A complete portfolio meets all four criteria. Revise incomplete evidence; no aggregate learner pass is inferred from the presence of these instructions.

### Labs and individual reasoning targets

- [P07: See Stability Margin in Time and Frequency](/courses/controls-gnc/modules/07-see-stability-margin-in-time-and-frequency): Added lag changes phase near crossover and can reduce stability margin even if low-frequency gain improves tracking. A positive gain margin alone does not summarize every crossover or delay effect.
- [P08: Reject a Disturbance with Feedback](/courses/controls-gnc/modules/08-reject-a-disturbance-with-feedback): The closed-loop sensitivity attenuates some disturbances but its attenuation varies with frequency. Identify the disturbance injection point before equating an output change to the loop gain.
- [P19: Measure Sensitivity to Model Error](/courses/controls-gnc/modules/19-measure-sensitivity-to-model-error): Model error changes the physical loop while the nominal design remains fixed. Compare gain and drag sweeps independently; a robust claim must name the tested uncertainty family and performance measure.
- [P30: Shape Sensitivity with Bode Loop Design](/courses/controls-gnc/modules/30-shape-sensitivity-with-bode-loop-design): For negative feedback S+T=1. Improving disturbance rejection in one frequency region can increase noise or effort elsewhere; an incorrect feedback denominator breaks the identity.
- [P31: Design Lead and Lag Compensation](/courses/controls-gnc/modules/31-design-lead-and-lag-compensation): Lead and lag are identified by their pole-zero ordering, not a component name. Swapping the lead pole and zero reverses the phase effect; compare the same frequencies and scaling.
- [P32: Place a Notch Filter and Reference Prefilter](/courses/controls-gnc/modules/32-place-a-notch-filter-and-reference-prefilter): A notch reduces loop transmission near its chosen center, while a prefilter changes reference content. Mistuning the notch can leave the physical resonance exposed even if reference motion looks smoother.
