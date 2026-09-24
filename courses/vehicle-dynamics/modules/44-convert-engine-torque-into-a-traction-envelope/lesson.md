# Convert Engine Torque into a Traction Envelope

This competency-derived Python-first lesson is not a source conversion and is not a measured-vehicle result. It is a bounded instructional model with synthetic torque and tire parameters.

## Model and equations

- `T_e=220-6e-6(n_e-4500)^2`
- `F_engine=T_e i_g i_0 eta/r_t`
- `F_delivered=min(F_engine,mu F_z_driven)`

Engine speed is positive in `rpm`, torque in `N*m`, road force is positive forward in `N`, and road speed is positive forward in `m/s`. The fixed final drive, efficiency, driven load, and tire radius define the lesson boundary.

## Baseline workflow

Run the defaults, identify whether engine or tire capacity governs, and check that delivered force equals the lower envelope with zero residual.

## Two one-variable sweeps

Raise engine speed alone to move along the torque curve, then reduce gear ratio alone to separate engine torque from mechanical advantage.

## Intentionally broken case

Ignore the driven-tire capacity and deliver the larger engine-limited force.

## Recovery

Apply final drive, efficiency, and tire radius once, then take the minimum of engine force and tire capacity.

## Limiting cases and invariants

- Zero engine torque produces zero delivered force.
- An ample tire boundary leaves the engine curve governing.
- Delivered force cannot exceed either boundary.

## Independent evidence

Five retained scenarios are recomputed by a course-owned independent analytic reference that imports no production experiment or output.

## Common mistakes

- Multiplying by tire radius instead of dividing.
- Applying driveline efficiency in the wrong direction.
- Plotting engine force without enforcing the tire envelope.

## Formative checks

1. Which boundary governs the default point?
2. Why can a shorter gear stop improving delivered force?

## Teach-back

Explain the force path from crankshaft to road, with units, forward-positive sign convention, validity boundary, named broken behavior, and exact minimum-envelope recovery.
