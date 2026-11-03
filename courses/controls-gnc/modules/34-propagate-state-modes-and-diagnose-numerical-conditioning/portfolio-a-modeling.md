## Evidence portfolio A-MODELING

This authored assessment joins P01, P02, P03, P04, P13, P14, P25, P26, P34. It records no learner score. Use the linked labs below rather than inventing a single executable model that combines them.

### 1. Model and prediction

Predict how doubling stiffness changes static displacement and ringing while mass and damping stay fixed. Before running, calculate the governing relation and state the assumptions. Then compare your prediction with the actual plotted state, geometry or covariance.

### 2. Transfer and tradeoff

Use a zero input gain or coupling limit to distinguish controllability rank from control effort. Record one change at a time, with units. Explain what knowledge transfers from the first lab and what model assumptions change; equal-looking curves are not evidence that the models are interchangeable.

### 3. Diagnose and recover

Hold both decay rates fixed and change the angle between the eigenvectors. Enable its named fault, collect the evidence that discriminates the cause, recover at identical inputs and reset. Reconcile the actual requirement, state or history with the claimed recovery.

### 4. Defend the boundary

Roundoff reconstruction residual is not a physical state error bound. Name which additional experiment or external course would be needed to extend this claim. Separate authored reasoning from a measured learner result.

### Four-criterion rubric

- **Model:** derive the chosen relation with conventions, units and an independently worked baseline value.
- **Evidence:** retain parameter values, predictions, actual plots/metrics and two separate control sweeps; explain any disagreement.
- **Diagnosis:** show a causal fault and exact-input recovery, including infeasible, singular or censored outcomes where applicable.
- **Integration and scope:** explain how the named competencies connect and where their models differ; retain all physical and learner-validation exclusions.

A complete portfolio meets all four criteria. Revise incomplete evidence; no aggregate learner pass is inferred from the presence of these instructions.

### Labs and individual reasoning targets

- [P01: Watch a Mass-Spring-Damper Respond](/courses/controls-gnc/modules/01-watch-a-mass-spring-damper-respond): Static displacement follows F/k; natural frequency follows sqrt(k/m), while damping ratio changes with both k and m. Separate integration-driven energy growth from physical forced response.
- [P02: Build Intuition for Integrators and First-Order Systems](/courses/controls-gnc/modules/02-build-intuition-for-integrators-and-first-order-systems): The first-order response approaches its DC gain over its time constant; an integrator accumulates area. A slower pole changes approach time rather than converting the equilibrium into a ramp.
- [P03: Relate Poles to Visible Motion](/courses/controls-gnc/modules/03-relate-poles-to-visible-motion): A negative real part sets exponential decay; conjugate imaginary parts set angular frequency. The same endpoint can occur at different oscillation phases, so use the history and pole locations together.
- [P04: Compare Linear and Nonlinear Pendulum Models](/courses/controls-gnc/modules/04-compare-linear-and-nonlinear-pendulum-models): The sine law and its tangent coincide only locally. Larger initial angles change restoring torque and period; agreement near the equilibrium is insufficient at large excursions.
- [P13: Test Controllability](/courses/controls-gnc/modules/13-test-controllability): The span of B, AB and higher powers identifies reachable directions. A barely nonzero coupling can preserve rank yet make reaching a state poorly conditioned and expensive.
- [P14: Test Observability](/courses/controls-gnc/modules/14-test-observability): Observability involves C, CA and the state dynamics. Longer data may improve an existing weak direction, but identical or absent sensitivities retain a null space.
- [P25: Linearize a Nonlinear Plant Around an Operating Point](/courses/controls-gnc/modules/25-linearize-a-nonlinear-plant-around-an-operating-point): An equilibrium must first balance gravity torque. The Jacobian describes a local perturbation after that balance; a small Taylor error cannot excuse linearizing around an unbalanced state.
- [P26: Reduce Block Diagrams and Convert System Realizations](/courses/controls-gnc/modules/26-reduce-block-diagrams-and-convert-system-realizations): A coordinate realization preserves the full transfer relation. Dropping a nearly cancelled mode changes the model unless exact cancellation and the relevant input/output assumptions hold.
- [P34: Propagate State Modes and Diagnose Numerical Conditioning](/courses/controls-gnc/modules/34-propagate-state-modes-and-diagnose-numerical-conditioning): Eigenvalues remain stable while nearly parallel eigenvectors amplify coordinate sensitivity and transient cancellation. A tiny reconstruction error is not proof that the modal basis is well conditioned.
