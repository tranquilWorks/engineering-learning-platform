# Map Aero Balance and Ride-Height Sensitivity

This competency-derived Python-first lesson is not a source conversion and is not a measured-vehicle result. Its coefficients are bounded synthetic aerodynamic parameters.

## Model and equations

- `C_Lf=0.58-2.2(h_f[m]-0.080)`
- `F_df=0.5 rho A v^2 C_Lf`, `F_dr=0.5 rho A v^2 C_Lr`
- `balance_f=F_df/(F_df+F_dr)`, `M_pitch=1.50 F_dr-1.20 F_df`

Speed is positive forward, downforce positive downward, drag positive opposite motion, and positive pitch moment follows the declared rear-minus-front convention. Ride-height input is `mm` and is converted to `m` once.

## Baseline workflow

Run the reference height and speed, inspect front/rear forces, drag, balance, and pitch moment, then require zero unit residual.

## Two one-variable sweeps

Raise speed alone, then raise front ride height alone to distinguish speed-squared scale from balance sensitivity.

## Intentionally broken case

Insert the millimetre control value into a coefficient law calibrated in metres.

## Recovery

Convert millimetres to metres once, evaluate front and rear forces separately, and retain their signed moment arms.

## Limiting cases and invariants

- All aerodynamic forces tend to zero with speed squared.
- Reference ride height recovers the reference front coefficient.
- Front balance includes both axle contributions.

## Independent evidence

An independent coefficient-and-force calculation recomputes all five scenarios without production execution.

## Common mistakes

- Feeding millimetres into a metre-based sensitivity.
- Omitting rear downforce from balance.
- Using force magnitude without its pitch moment arm.

## Formative checks

1. Why is front balance speed-independent in this bounded map?
2. How does raising the front alter pitch moment here?

## Teach-back

Explain the unit boundary, force signs, speed-squared law, coefficient validity range, named unit failure, and exact conversion recovery.
