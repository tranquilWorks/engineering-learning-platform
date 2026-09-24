# Partition Lateral Load Transfer

This competency-derived Python-first lesson is not a source conversion and is not a measured-vehicle result. It is a bounded instructional model with explicit units and assumptions.

## Model and equations

- `M_roll=m a_y h`
- `Delta F_z,f t_f+Delta F_z,r t_r=M_roll`
- `M_elastic=M_roll-M_geometric`

Positive lateral force follows the declared body-axis convention, yaw moment is positive in the same turn direction, and all angles enter governing equations in radians unless a displayed axis says degrees.

## Baseline workflow

Set the controls to their defaults, predict the sign and dominant magnitude, run the model, and check the response plot, mechanism plot, scalar metrics, and invariant residual before interpreting the result.

## Two one-variable sweeps

Raise lateral acceleration alone, then shift elastic roll stiffness forward alone, separating total magnitude from distribution.

## Intentionally broken case

Distribute the full roll moment elastically after already adding geometric transfer, so roll-center contribution is counted twice.

## Recovery

Subtract geometric roll moment once, distribute only the elastic remainder, and verify moment closure.

## Limiting cases and invariants

- At zero lateral acceleration every transfer contribution and capacity loss tends to zero.
- With all elastic stiffness assigned to one axle, geometric transfer still remains at both axles.
- Front and rear geometric plus elastic transfer must reconstruct exactly one total roll moment before tire load sensitivity is evaluated.

## Independent evidence

The five retained scenarios are recomputed by the course-owned independent analytic and numerical reference. That reference imports no production experiment, consumes no production result, and perturbs no production value.

## Common mistakes

- Adding geometric load transfer on top of the full elastic total.
- Comparing axle transfer without accounting for track width.
- Assuming equal total tire capacity after unequal load sharing.

## Formative checks

1. Why is moment closure expressed with each axle track width?
2. Does moving elastic stiffness forward change the total roll moment?

## Teach-back

Explain where the geometric term goes when the elastic remainder is formed. Include the relevant units, sign convention, validity boundary, named broken behavior, and exact recovery check.
