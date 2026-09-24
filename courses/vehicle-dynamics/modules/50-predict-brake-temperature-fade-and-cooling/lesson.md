# Predict Brake Temperature, Fade, and Cooling

This competency-derived Python-first lesson is not a source conversion and is not a measured-vehicle result. Its repeated-stop energies and thermal constants are synthetic.

## Model and equations

- `Delta T_stop=eta E_stop/C_brake`
- `C_brake dT/dt=-h_c(T-T_ambient)`
- `E_absorbed=Delta E_stored+E_rejected`

Temperature is in `degC` for differences, heat capacity in `J/K`, cooling coefficient in `W/K`, time in `s`, and energy in `J` or reported `kJ`.

## Baseline workflow

Apply six fixed-energy stops separated by cooling intervals, then inspect peak/final temperature, rejected heat, fade, and ledger residual.

## Two one-variable sweeps

Raise energy per stop alone, then raise cooling coefficient alone to separate heating severity from recovery rate.

## Intentionally broken case

Count convective rejection in the ledger but omit the same heat flow from the temperature state update.

## Recovery

Apply absorbed stop energy, integrate convective loss over each bounded interval, and close absorbed energy against storage plus rejection.

## Limiting cases and invariants

- Zero absorbed stop energy leaves the rotor at ambient.
- Zero cooling produces no rejected heat.
- The thermal energy residual must vanish in the recovered model.

## Independent evidence

The five scenarios are independently time-stepped using the declared heat-capacity and convection relations.

## Common mistakes

- Mixing kilojoules and joules.
- Applying cooling to the ledger but not the state.
- Evaluating fade only from final rather than peak temperature.

## Formative checks

1. Why can final temperature understate fade exposure?
2. What terms must sum to absorbed energy?

## Teach-back

Explain the heat-flow sign, temperature and energy units, bounded stop sequence, hidden-cooling failure, and exact energy-balance recovery.
