# Cumulative portfolio A-ESTIMATION

Integrate these existing lessons: P10, P13, P14, P15, P49, P50, P53.

Required evidence: Covariance, innovation, gate, particle, observability, multi-rate, and consistency evidence.

## Derive and predict

Use P10: Predict position drift from a constant accelerometer bias. Velocity bias grows linearly and position bias quadratically with coast time; angular and translational errors have different units. Connect this result to at least one other listed lesson, identifying the exact quantity, units and assumption transferred across their interface.

## Compare connected mechanisms

Use P14: Trace a wheel/absolute-position observation through EKF prediction and correction. The motion Jacobian propagates pose covariance; an innovation changes state through its gain and must also update covariance. Connect this result to at least one other listed lesson, identifying the exact quantity, units and assumption transferred across their interface.

## Diagnose and recover

Use P49: Predict which state direction becomes unobservable without excitation. The stacked whitened measurement rows determine rank; sample rate cannot recover a state absent from every row. Connect this result to at least one other listed lesson, identifying the exact quantity, units and assumption transferred across their interface.

## Integrate and defend the boundary

Use P53: Distinguish a backward smoother from a causal filter with smaller error bars. Future measurements affect past states through the smoothing gain; held-out observations audit errors separately from fitting. Connect this result to at least one other listed lesson, identifying the exact quantity, units and assumption transferred across their interface.

## Four-criterion rubric

1. Governing reasoning: equations, units and frame/sign conventions justify a numerical prediction; naming an algorithm alone earns no evidence.
2. Controlled comparison: two isolated sweeps and at least one limiting case distinguish mechanisms and make a falsifiable claim.
3. Diagnose and recover: identify the first failing assumption from actual outputs, restore it and demonstrate deterministic recovery.
4. Integration and scope: show the value passed between stages, an independently checked result, and a limitation that prevents a broader claim.

Retain inputs, selected outputs and your explanation as a cumulative artifact. No learner completion, automatic score, physical qualification or production acceptance is recorded.
