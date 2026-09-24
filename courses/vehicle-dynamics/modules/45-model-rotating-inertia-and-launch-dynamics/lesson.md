# Model Rotating Inertia and Launch Dynamics

This competency-derived Python-first lesson is not a source conversion and is not a measured-vehicle result. It uses bounded synthetic drivetrain and tire parameters.

## Model and equations

- `m_eq=sum(J_k i_k^2/r_t^2)`
- `a=(min(T_e i_g i_0 eta/r_t,F_tire)-F_resist)/(m+m_eq)`
- `W_drive-W_resist=Delta(E_translation+E_rotation)`

Vehicle speed and acceleration are positive forward; angular inertias are in `kg*m^2`, equivalent mass in `kg`, force in `N`, and energy in `J`.

## Baseline workflow

Run the default launch, inspect reflected mass and initial acceleration, then compare work input with translational plus rotational energy.

## Two one-variable sweeps

Raise launch torque alone, then raise driveline inertia alone to distinguish traction saturation from energy-storage cost.

## Intentionally broken case

Reflect driveline inertia through the inverse ratio and omit wheel inertia, yielding an implausibly small equivalent mass and failed energy closure.

## Recovery

Reflect engine, clutch, gearbox, shaft, and wheel inertia through each squared speed ratio and integrate the traction-limited acceleration.

## Limiting cases and invariants

- Vanishing rotating inertia recovers translational vehicle mass.
- Tire-limited launch force cannot rise with added engine torque.
- Launch work supplies both translational and rotating energy stores.

## Independent evidence

The five deterministic scenarios are independently reintegrated without importing production code or consuming production results.

## Common mistakes

- Using a linear rather than squared speed ratio.
- Omitting wheel inertia at tire speed.
- Checking only acceleration while ignoring energy closure.

## Formative checks

1. Why does engine-side inertia receive a large reflection factor?
2. When will more launch torque fail to shorten the launch?

## Teach-back

Explain the inertia reflection, integration bound, units, forward-positive convention, broken ratio direction, and energy-ledger recovery.
