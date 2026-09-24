# Simulate ABS Slip Control and Wheel Lockup

This competency-derived Python-first lesson is not a source conversion and is not a measured-vehicle result. It is a bounded quarter-vehicle simulation with synthetic tire behavior.

## Model and equations

- `kappa=(v-r omega)/max(v,0.5)`
- `I omega_dot=F_x r-T_brake`, `m v_dot=-F_x`
- `T_brake=F_x r+(I/r)[v k(kappa_target-kappa)-(1-kappa)v_dot]`

Vehicle speed and wheel rotation are positive forward; braking slip is positive when wheel circumferential speed falls below vehicle speed. Time is in `s`, force in `N`, and torque in `N*m`.

## Baseline workflow

Run the modulated case, inspect peak slip and target error, and require no lock flag plus near-zero wheel-dynamics residual.

## Two one-variable sweeps

Raise target slip alone, then raise requested brake torque alone to separate controller target from actuator authority.

## Intentionally broken case

Disable modulation and apply the full requested torque until the wheel locks.

## Recovery

Compute signed slip from vehicle and wheel speed, command a bounded slip rate, and close the wheel torque balance at every fixed step.

## Limiting cases and invariants

- Zero brake torque produces zero braking slip and deceleration.
- Excess unmodulated torque drives wheel speed to zero before vehicle speed.
- Recovered ABS remains near target slip without sustained lock.

## Independent evidence

A separately formulated deterministic time integration recomputes every retained scenario without production imports or outputs.

## Common mistakes

- Reversing the braking-slip sign.
- Controlling wheel speed without accounting for vehicle deceleration.
- Claiming good braking from stopping distance alone while the wheel is locked.

## Formative checks

1. Why does tire force fall after excessive slip?
2. Which torque terms must balance at steady target slip?

## Teach-back

Explain the slip sign, fixed sample interval, wheel and vehicle states, lock verdict, unmodulated failure, and modulation recovery with units.
