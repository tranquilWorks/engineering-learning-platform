# A-CONTROL integration evidence

Integrate these existing lessons: P05, P06, P08, P34, P35, P36, P37, P38, P39, P40, P61, P69.

Required evidence: Tracking, effort, gravity, interaction energy, force error, passivity, delay, saturation, and recovery checks.

## Derive and predict

Use P05: Predict current and speed when gear ratio changes under load. Back EMF couples speed to current; gearing changes reflected inertia and output torque rather than creating mechanical power. Connect this result to at least one other listed lesson, identifying the exact quantity, units and assumption transferred across their interface.

## Compare connected mechanisms

Use P35: Explain the effect of payload mismatch on computed-torque compensation. Model cancellation uses inertia, coupling and gravity; feedback corrects residual error only within available effort. Connect this result to at least one other listed lesson, identifying the exact quantity, units and assumption transferred across their interface.

## Diagnose and recover

Use P39: Audit the energy tank when saturation and delayed commands occur. Applied work, not requested work, must be charged to the tank; a nonnegative energy record requires actual command limiting. Connect this result to at least one other listed lesson, identifying the exact quantity, units and assumption transferred across their interface.

## Integrate and defend the boundary

Use P69: Connect visual pose, arm motion, grasp force and object placement. A grasp verdict must depend on executed arm/contact behavior and the object's final state; unrelated successful components do not prove integration. Connect this result to at least one other listed lesson, identifying the exact quantity, units and assumption transferred across their interface.

## Required integration artifact

Trace a commanded motion through desired acceleration, applied torque, actual joint motion and endpoint error. Show where clipping invalidates ideal computed-torque error dynamics. Compare this with the contact-energy experiment: compute stored elastic energy and account for the tank before interpreting force tracking as stable interaction. In P69 retain both the contact-study outputs and executed manipulation events, explicitly identifying that the tank does not drive the jaw-force ramp. Diagnose one actuator-limited failure and one insufficient-grasp-support failure; they require different repairs. Verify return to baseline after each fault and retain control effort as well as tracking error.

## Four-criterion rubric

1. Governing reasoning: equations, units and frame/sign conventions justify a numerical prediction; naming an algorithm alone earns no evidence.
2. Controlled comparison: two isolated sweeps and at least one limiting case distinguish mechanisms and make a falsifiable claim.
3. Diagnose and recover: identify the first failing assumption from actual outputs, restore it and demonstrate deterministic recovery.
4. Integration and scope: show the value passed between stages, an independently checked result, and a limitation that prevents a broader claim.

Retain inputs, selected outputs and your explanation as a cumulative artifact. No learner completion, automatic score, physical qualification or production acceptance is recorded.
