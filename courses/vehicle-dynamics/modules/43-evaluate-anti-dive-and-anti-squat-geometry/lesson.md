# Evaluate Anti-Dive and Anti-Squat Geometry

This competency-derived Python-first lesson is not a source conversion and is not a measured-vehicle result. It is a bounded instructional model with explicit units and assumptions.

## Model and equations

- `anti_dive=eta_b tan(theta) L/h`
- `anti_squat=eta_d tan(theta) L/h`
- `Delta F_z=Delta F_geometry+Delta F_spring`

Positive lateral force follows the declared body-axis convention, positive bump is upward wheel travel, positive pitch and roll follow right-hand generalized coordinates, and all trigonometric equations use radians internally.

## Baseline workflow

Set the controls to their defaults, predict the sign and dominant magnitude, run the model, and check the response plot, mechanism plot, scalar metrics, and invariant residual before interpreting the result.

## Two one-variable sweeps

Raise force-line angle alone, then raise center-of-gravity height alone, separating geometry slope from vehicle leverage.

## Intentionally broken case

Send angle degrees directly into tangent, generating nonphysical anti percentages and a failed partition against the physical geometry.

## Recovery

Convert the force-line angle to radians once, bound the instructional geometry below lift, and partition the total transfer exactly once.

## Limiting cases and invariants

- At zero force-line angle, both anti percentages tend to zero and the spring-supported path carries the modeled transfer.
- As anti percentage approaches one within the non-lifting domain, the spring-supported share tends to zero.
- Anti geometry partitions one longitudinal load-transfer total between suspension links and spring-supported pitch; it does not create or remove load transfer.

## Independent evidence

The five retained scenarios are recomputed by the course-owned independent analytic and numerical reference. That reference imports no production experiment, consumes no production result, and perturbs no production value.

## Common mistakes

- Adding anti transfer on top of the total longitudinal transfer.
- Using degrees directly in tangent.
- Equating anti-dive percentage with reduced total tire load transfer.

## Formative checks

1. Does one hundred percent anti eliminate total longitudinal load transfer?
2. Why does greater center-of-gravity height reduce the anti percentage for fixed link angle?

## Teach-back

Explain which part of load transfer changes with anti geometry and which part cannot change. Include the relevant units, coordinate convention, validity boundary, named broken behavior, and exact recovery check.
