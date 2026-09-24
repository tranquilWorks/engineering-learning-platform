# Analyze Yaw and Sideslip Frequency Response

This competency-derived Python-first lesson is not a source conversion and is not a measured-vehicle result. It is a bounded instructional model with explicit units and assumptions.

## Model and equations

- `(j omega I-A) X=B Delta`
- `G_r(j omega)=r/Delta`
- `omega=2 pi f`

Positive lateral force follows the declared body-axis convention, yaw moment is positive in the same turn direction, and all angles enter governing equations in radians unless a displayed axis says degrees.

## Baseline workflow

Set the controls to their defaults, predict the sign and dominant magnitude, run the model, and check the response plot, mechanism plot, scalar metrics, and invariant residual before interpreting the result.

## Two one-variable sweeps

Raise speed alone, then raise steering frequency alone, so operating-point and excitation effects remain distinguishable.

## Intentionally broken case

Insert hertz directly where radians per second is required; the response then fails the complex equation at the declared frequency.

## Recovery

Apply omega equals two pi f before the complex solve and recheck magnitude, phase, and residual.

## Limiting cases and invariants

- As frequency approaches zero, the complex solution approaches the steady-state gain.
- At high frequency, state magnitudes diminish while phase lag grows within the bounded linear model.
- Every reported complex response must satisfy the declared state equation at omega equal to two pi times the excitation frequency in hertz.

## Independent evidence

The five retained scenarios are recomputed by the course-owned independent analytic and numerical reference. That reference imports no production experiment, consumes no production result, and perturbs no production value.

## Common mistakes

- Treating hertz and radians per second as interchangeable.
- Plotting magnitude without phase.
- Calling a DC gain a finite-frequency response.

## Formative checks

1. Why is the complex-equation residual a stronger check than a smooth Bode curve?
2. What should the response approach as frequency tends to zero?

## Teach-back

Describe how the same bicycle model can appear responsive in DC yet lag badly at a rapid steering input. Include the relevant units, sign convention, validity boundary, named broken behavior, and exact recovery check.
