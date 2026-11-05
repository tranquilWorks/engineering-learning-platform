# A-HANDLING integration evidence

Integrate these existing lessons: P07, P08, P29, P34, P35, P36, P37, P38.

Required evidence: Predict steady and transient yaw/sideslip behavior, locate linear-model limits, and recover a stable nonlinear case.

## Derive and predict

Use P07: Solve both steady bicycle equations and test the solution against independent force and yaw-moment balances. Steady sideslip rate is zero, but lateral acceleration is v*r, not zero. Thus Fyf+Fyr=m*v*r while a*Fyf-b*Fyr=0. The second equation requires Fyf/Fyr=b/a. A yaw solution alone cannot validate the first equation. Compare a zero-steer limit and a speed sweep, retaining the sign convention and the determinant or conditioning of the two-equation solve. Connect this result to at least one other listed lesson, identifying the exact quantity, units and assumption transferred across their interface.

## Compare connected mechanisms

Use P29: Derive the combined-slip projection and show why the two pure-slip maxima cannot generally coexist. Compute the unconstrained longitudinal and lateral forces first. If their norm exceeds mu*Fz, apply one common scale factor so their ratio is preserved. For equal requested components each at capacity, utilization is sqrt(2); correct projection reduces each to capacity/sqrt(2). The broken independent-channel result can look individually plausible while exceeding the shared contact budget. Compare both force components and the combined utilization. Connect this result to at least one other listed lesson, identifying the exact quantity, units and assumption transferred across their interface.

## Diagnose and recover

Use P36: Classify the sign of the understeer gradient and test its singular boundary without treating a sentinel as a speed. For the declared axle loads, K=Wf/Cf-Wr/Cr. Increasing front stiffness reduces K; increasing rear stiffness raises K. When K is positive, characteristic speed is sqrt(g*L/K); when negative, the separate linear critical speed is sqrt(-g*L/K). At neutral steer neither is finite. The plot omits an unavailable characteristic-speed point and the metric exposes applicability. Near neutrality, large speed sensitivity reflects the denominator, not a reliable operating limit. Connect this result to at least one other listed lesson, identifying the exact quantity, units and assumption transferred across their interface.

## Integrate and defend the boundary

Use P38: Derive wheel loads from the transferred amount and detect when a four-contact equilibrium becomes impossible. If T is the load moved, inner load is W/2-T and outer load W/2+T; their difference is 2T. Multiplying that difference by half-track gives T*track, the roll moment. Using +/-T/2 halves the moment and underestimates the load-sensitive capacity loss. First subtract geometric moment from total before distributing the elastic remainder. A negative requested inner load marks lift-off: the displayed capped capacity is only a bound and cannot close the original four-contact equilibrium. Connect this result to at least one other listed lesson, identifying the exact quantity, units and assumption transferred across their interface.

## Required integration artifact

Produce a handling report that compares the steady bicycle solution, DC frequency-response gain, understeer classification, nonlinear trim and full nonlinear transient. State when the lessons use different mass, geometry or stiffness constants and recompute a consistent comparison rather than equating incompatible numbers. For P37 retain trim validity/residual, both local poles, last trajectory time and maximum axle utilization. Include an unavailable or domain-limited case where appropriate. Explain why a restoring moment slice, stable linear poles and a feasible nonlinear maneuver are distinct claims. Recover identical inputs and demonstrate deterministic restoration.

## Four-criterion rubric

1. Governing reasoning: equations, units and frame/sign conventions justify a numerical prediction; naming an algorithm alone earns no evidence.
2. Controlled comparison: two isolated sweeps and at least one limiting case distinguish mechanisms and make a falsifiable claim.
3. Diagnose and recover: identify the first failing assumption from actual outputs, restore it and demonstrate deterministic recovery.
4. Integration and scope: show the value passed between stages, an independently checked result, and a limitation that prevents a broader claim.

Retain inputs, selected outputs and your explanation as a cumulative artifact. No learner completion, automatic score, physical qualification or production acceptance is recorded.
