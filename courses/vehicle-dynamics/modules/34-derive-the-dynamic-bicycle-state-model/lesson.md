# Derive the Dynamic Bicycle State Model

This competency-derived Python-first lesson is not a source conversion and is not a measured-vehicle result. It is a bounded instructional model with explicit units and assumptions.

## Model and equations

- `m U (beta_dot+r)=F_yf+F_yr`
- `I_z r_dot=a F_yf-b F_yr`
- `x_dot=A(U,C_f,C_r)x+B delta`

Positive lateral force follows the declared body-axis convention, yaw moment is positive in the same turn direction, and all angles enter governing equations in radians unless a displayed axis says degrees.

## Baseline workflow

Set the controls to their defaults, predict the sign and dominant magnitude, run the model, and check the response plot, mechanism plot, scalar metrics, and invariant residual before interpreting the result.

## Two one-variable sweeps

Raise speed alone to inspect dynamic stability, then raise front cornering stiffness alone to inspect axle balance.

## Intentionally broken case

Reverse the rear lateral-force sign inside the state equations; the computed equilibrium no longer closes the physical force and moment balances.

## Recovery

Restore the rear-force sign, solve the two-state equilibrium, and confirm both residuals return to numerical zero.

## Limiting cases and invariants

- At zero steer the linear equilibrium is zero sideslip and zero yaw rate.
- As speed approaches the lower model boundary, the steady linear solution remains finite but is not a parking-speed model.
- With the declared SAE-style lateral-force signs, the steady state closes both lateral-force and yaw-moment balance and stable poles have negative real part.

## Independent evidence

The five retained scenarios are recomputed by the course-owned independent analytic and numerical reference. That reference imports no production experiment, consumes no production result, and perturbs no production value.

## Common mistakes

- Mixing body sideslip with front tire slip angle.
- Dropping the minus sign in the rear axle moment.
- Using degrees inside equations whose stiffness is declared per radian.

## Formative checks

1. Why does yaw inertia affect the poles but not the static moment-balance equation?
2. Which residual exposes a rear-force sign error most directly?

## Teach-back

Explain why a stable pole calculation is insufficient when the force convention itself is wrong. Include the relevant units, sign convention, validity boundary, named broken behavior, and exact recovery check.
