# Trace Suspension Kinematics and Compliance

This competency-derived Python-first lesson is not a source conversion and is not a measured-vehicle result. It is a bounded instructional model with explicit units and assumptions.

## Model and equations

- `gamma=gamma_0+g_gamma z+c_gamma F_y`
- `toe=toe_0+g_toe z+c_toe F_y`
- `k_wheel=k_spring MR(z)^2`

Positive lateral force follows the declared body-axis convention, positive bump is upward wheel travel, positive pitch and roll follow right-hand generalized coordinates, and all trigonometric equations use radians internally.

## Baseline workflow

Set the controls to their defaults, predict the sign and dominant magnitude, run the model, and check the response plot, mechanism plot, scalar metrics, and invariant residual before interpreting the result.

## Two one-variable sweeps

Raise bump travel alone, then lateral force alone, so geometry and compliance contributions are separately visible.

## Intentionally broken case

Convert millimetres to metres but retain gradients stated per millimetre, suppressing bump camber, toe, and motion-ratio change.

## Recovery

Apply each gradient to its declared millimetre or newton input and recompute wheel rate from the recovered motion ratio.

## Limiting cases and invariants

- At zero travel and zero lateral force, alignment returns to the declared static camber and toe.
- With zero lateral force, the compliance contribution vanishes while bump kinematics and motion ratio remain.
- Kinematic gradients act on millimetres of wheel travel, compliance gradients act on newtons, and the two contributions superpose only under the declared sign convention.

## Independent evidence

The five retained scenarios are recomputed by the course-owned independent analytic and numerical reference. That reference imports no production experiment, consumes no production result, and perturbs no production value.

## Common mistakes

- Applying per-millimetre gradients to metres.
- Combining camber and toe without a sign convention.
- Using spring rate directly as wheel rate when motion ratio differs from one.

## Formative checks

1. Which output changes with bump even when lateral force is zero?
2. Why is wheel rate proportional to motion ratio squared?

## Teach-back

Separate the kinematic and compliance terms in the baseline camber and toe values. Include the relevant units, coordinate convention, validity boundary, named broken behavior, and exact recovery check.
