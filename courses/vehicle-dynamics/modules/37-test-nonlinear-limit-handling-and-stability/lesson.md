# Test Nonlinear Limit Handling and Stability

This competency-derived Python-first lesson is not a source conversion and is not a measured-vehicle result. It is a bounded instructional model with explicit units and assumptions.

## Model and equations

- `F_y=mu F_z tanh(C_alpha alpha/(mu F_z))`
- `M_z=a F_yf-b F_yr`
- `S=-partial M_z/partial beta`

Positive lateral force follows the declared body-axis convention, yaw moment is positive in the same turn direction, and all angles enter governing equations in radians unless a displayed axis says degrees.

## Baseline workflow

Set the controls to their defaults, predict the sign and dominant magnitude, run the model, and check the response plot, mechanism plot, scalar metrics, and invariant residual before interpreting the result.

## Two one-variable sweeps

Raise steer alone, then lower friction alone, to approach the capacity boundary by two distinct mechanisms.

## Intentionally broken case

Use uncapped linear axle forces at limit steer, allowing utilization above one while retaining a plausible-looking yaw curve.

## Recovery

Restore the bounded nonlinear force law and recompute utilization and local yaw-moment slope together.

## Limiting cases and invariants

- At small steer the bounded force law approaches the linear cornering-stiffness relation.
- At very large slip the bounded axle force approaches but does not exceed its friction capacity.
- A limit-handling verdict requires both a restoring yaw-moment slope and axle utilizations no greater than the declared friction boundary.

## Independent evidence

The five retained scenarios are recomputed by the course-owned independent analytic and numerical reference. That reference imports no production experiment, consumes no production result, and perturbs no production value.

## Common mistakes

- Interpreting a negative yaw-moment slope without checking tire capacity.
- Using total vehicle normal load at both axles.
- Extending the linear tire law into saturation.

## Formative checks

1. Why can a smooth yaw-moment curve still be physically impossible?
2. What does capacity excess equal when both axles respect their limits?

## Teach-back

State the two independent conditions you would require before calling this operating point recoverable. Include the relevant units, sign convention, validity boundary, named broken behavior, and exact recovery check.
