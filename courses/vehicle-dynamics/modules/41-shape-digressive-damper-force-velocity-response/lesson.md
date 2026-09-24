# Shape Digressive Damper Force-Velocity Response

This competency-derived Python-first lesson is not a source conversion and is not a measured-vehicle result. It is a bounded instructional model with explicit units and assumptions.

## Model and equations

- `F=c_h v+(c_l-c_h)v/(1+|v|/v_k)`
- `dF/dv tends to c_l at v=0`
- `E_cycle=integral F(v) v dt`

Positive lateral force follows the declared body-axis convention, positive bump is upward wheel travel, positive pitch and roll follow right-hand generalized coordinates, and all trigonometric equations use radians internally.

## Baseline workflow

Set the controls to their defaults, predict the sign and dominant magnitude, run the model, and check the response plot, mechanism plot, scalar metrics, and invariant residual before interpreting the result.

## Two one-variable sweeps

Raise knee velocity alone, then raise high-speed coefficient alone, distinguishing transition location from asymptotic slope.

## Intentionally broken case

Multiply metre-per-second inputs by one thousand as though they were millimetres per second, overstating force and cycle energy.

## Recovery

Keep shaft velocity in metres per second for both the force law and the energy integral.

## Limiting cases and invariants

- As shaft velocity tends to zero, force tends to zero and tangent slope tends to the low-speed coefficient.
- At large velocity magnitude, tangent slope approaches the high-speed coefficient while force remains opposite motion by convention.
- The damper law is continuous, odd-symmetric, and dissipative, with the tangent slope transitioning from the low-speed coefficient toward the declared high-speed coefficient.

## Independent evidence

The five retained scenarios are recomputed by the course-owned independent analytic and numerical reference. That reference imports no production experiment, consumes no production result, and perturbs no production value.

## Common mistakes

- Calling any curved force law digressive without checking tangent slope.
- Integrating force instead of force times velocity for energy.
- Mixing millimetres per second with metres per second.

## Formative checks

1. Which derivative defines low-speed versus high-speed damping?
2. Why must cycle energy be nonnegative for a passive damper?

## Teach-back

Explain how knee velocity and high-speed coefficient alter different parts of the force-velocity curve. Include the relevant units, coordinate convention, validity boundary, named broken behavior, and exact recovery check.
