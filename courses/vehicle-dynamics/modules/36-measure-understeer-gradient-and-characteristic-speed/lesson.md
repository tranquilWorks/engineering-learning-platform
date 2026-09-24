# Measure Understeer Gradient and Characteristic Speed

This competency-derived Python-first lesson is not a source conversion and is not a measured-vehicle result. It is a bounded instructional model with explicit units and assumptions.

## Model and equations

- `K=W_f/C_f-W_r/C_r`
- `delta=L/R+K a_y/g`
- `V_char=sqrt(g L/K) for K>0`

Positive lateral force follows the declared body-axis convention, yaw moment is positive in the same turn direction, and all angles enter governing equations in radians unless a displayed axis says degrees.

## Baseline workflow

Set the controls to their defaults, predict the sign and dominant magnitude, run the model, and check the response plot, mechanism plot, scalar metrics, and invariant residual before interpreting the result.

## Two one-variable sweeps

Raise front stiffness alone, then lower rear stiffness alone, to see each axle move the gradient across handling classes.

## Intentionally broken case

Treat newtons per radian as newtons per degree, corrupting both the gradient magnitude and characteristic-speed calculation.

## Recovery

Restore stiffness units, classify the gradient sign, and compute characteristic speed only for the understeer case.

## Limiting cases and invariants

- At zero gradient the steer demand is purely geometric and characteristic speed is not finite.
- For negative gradient the instructional model classifies oversteer and does not invent a real characteristic speed.
- Characteristic speed is reported only for positive understeer gradient, and the steer law uses axle stiffness in newtons per radian.

## Independent evidence

The five retained scenarios are recomputed by the course-owned independent analytic and numerical reference. That reference imports no production experiment, consumes no production result, and perturbs no production value.

## Common mistakes

- Computing characteristic speed for an oversteer gradient.
- Using mass fractions where axle weight is required.
- Mixing stiffness per degree with stiffness per radian.

## Formative checks

1. Why is zero used instead of an imaginary characteristic speed for oversteer?
2. Which axle change makes the gradient more positive?

## Teach-back

Explain the domain check that must happen before quoting a characteristic speed. Include the relevant units, sign convention, validity boundary, named broken behavior, and exact recovery check.
