## Evidence portfolio A-NONLINEAR

This authored assessment joins P04, P43, P44, P46, P47. It records no learner score. Use the linked labs below rather than inventing a single executable model that combines them.

### 1. Model and prediction

Identify when a small-angle pendulum ceases to predict the nonlinear motion accurately. Before running, calculate the governing relation and state the assumptions. Then compare your prediction with the actual plotted state, geometry or covariance.

### 2. Transfer and tradeoff

Test the selected Lyapunov sublevel using the actual vector field and its boundary derivative. Record one change at a time, with units. Explain what knowledge transfers from the first lab and what model assumptions change; equal-looking curves are not evidence that the models are interchangeable.

### 3. Diagnose and recover

Explain an actual departure event when feedback cancellation uses a mismatched nonlinear model. Enable its named fault, collect the evidence that discriminates the cause, recover at identical inputs and reset. Reconcile the actual requirement, state or history with the claimed recovery.

### 4. Defend the boundary

Feedback linearization relies on the modeled input map and valid operating domain. Name which additional experiment or external course would be needed to extend this claim. Separate authored reasoning from a measured learner result.

### Four-criterion rubric

- **Model:** derive the chosen relation with conventions, units and an independently worked baseline value.
- **Evidence:** retain parameter values, predictions, actual plots/metrics and two separate control sweeps; explain any disagreement.
- **Diagnosis:** show a causal fault and exact-input recovery, including infeasible, singular or censored outcomes where applicable.
- **Integration and scope:** explain how the named competencies connect and where their models differ; retain all physical and learner-validation exclusions.

A complete portfolio meets all four criteria. Revise incomplete evidence; no aggregate learner pass is inferred from the presence of these instructions.

### Labs and individual reasoning targets

- [P04: Compare Linear and Nonlinear Pendulum Models](/courses/controls-gnc/modules/04-compare-linear-and-nonlinear-pendulum-models): The sine law and its tangent coincide only locally. Larger initial angles change restoring torque and period; agreement near the equilibrium is insufficient at large excursions.
- [P43: Use Phase Portraits to Separate Local and Global Stability](/courses/controls-gnc/modules/43-use-phase-portraits-to-separate-local-and-global-stability): The double-well potential has several equilibria. Reversing damping changes energy flow and local stability; distance from one well at a single oscillation phase is not a valid stability ranking.
- [P44: Certify Decay with Lyapunov Functions and Regions of Attraction](/courses/controls-gnc/modules/44-certify-decay-with-lyapunov-functions-and-regions-of-attraction): For V=x squared/2 and xdot=-x+b*x cubed, Vdot=-x squared+b*x fourth. Strict negativity requires a sublevel inside the nonzero equilibria, with the origin excluded from the strict test.
- [P46: Schedule Gains Across Operating Points](/courses/controls-gnc/modules/46-schedule-gains-across-operating-points): A table and interpolation rule produce an approximation. Sparse sampling can hide error between knots; matching a few endpoint gains does not establish uniform performance over the operating range.
- [P47: Cancel Nonlinearities with Feedback Linearization](/courses/controls-gnc/modules/47-cancel-nonlinearities-with-feedback-linearization): Cancellation leaves residual dynamics whose sign can change stability or produce finite escape. Report the event and finite validity interval rather than extending a plotted solution past departure.
