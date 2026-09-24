# Couple Heave, Pitch, and Roll Modes

This competency-derived Python-first lesson is not a source conversion and is not a measured-vehicle result. It is a bounded instructional model with explicit units and assumptions.

## Model and equations

- `K=sum_i k_i q_i q_i^T`
- `K phi=lambda M phi`
- `f_n=sqrt(lambda)/(2 pi)`

Positive lateral force follows the declared body-axis convention, positive bump is upward wheel travel, positive pitch and roll follow right-hand generalized coordinates, and all trigonometric equations use radians internally.

## Baseline workflow

Set the controls to their defaults, predict the sign and dominant magnitude, run the model, and check the response plot, mechanism plot, scalar metrics, and invariant residual before interpreting the result.

## Two one-variable sweeps

Raise front rate alone, then rear rate alone, to separate pitch bias and modal-frequency changes.

## Intentionally broken case

Delete every off-diagonal stiffness term, producing plausible frequencies whose modes fail the original coupled eigen-equation.

## Recovery

Reassemble stiffness from all four corner geometry vectors and verify each eigenpair against the full physical matrix.

## Limiting cases and invariants

- With perfectly symmetric front and rear corner pairs, roll decouples from heave and pitch.
- If all corner rates scale together, frequencies scale with the square root of that factor while mode shapes are retained.
- Every reported coupled mode must satisfy the full physical generalized eigen-equation, including the off-diagonal terms created by corner geometry and rate asymmetry.

## Independent evidence

The five retained scenarios are recomputed by the course-owned independent analytic and numerical reference. That reference imports no production experiment, consumes no production result, and perturbs no production value.

## Common mistakes

- Treating a diagonal approximation as the physical matrix.
- Mixing mass with pitch or roll inertia.
- Sorting mode names without inspecting participation.

## Formative checks

1. Why can three positive frequencies still fail the model?
2. Which matrix terms reveal coupling most directly?

## Teach-back

Explain how you would prove a reported mode belongs to the full chassis model rather than a diagonal approximation. Include the relevant units, coordinate convention, validity boundary, named broken behavior, and exact recovery check.
