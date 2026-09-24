# Couple Downforce, Drag, Tires, and Stint Limits

This competency-derived Python-first lesson is not a source conversion and is not a measured-vehicle result. It couples bounded synthetic aero, tire, propulsion, energy, and thermal parameters.

## Model and equations

- `F_tire=mu_ref F_z,ref[(m g+F_down)/F_z,ref]^0.86`
- `a_usable=[min(F_tire,P/v)-F_drag]/m`
- `N_stint=min(E_stint/E_lap,N_thermal)`

Vehicle speed and acceleration are positive forward, downforce positive downward, drag positive opposite travel, force in `N`, energy in `MJ`, and stint length in laps.

## Baseline workflow

Run the coupled point, inspect downforce, drag, usable acceleration, lap energy, and the limiting lap count, then require zero coupling residual.

## Two one-variable sweeps

Raise speed alone, then raise available stint energy alone to separate aero-force coupling from budget limitation.

## Intentionally broken case

Double-count downforce in tire capacity and omit drag from both tractive-force and lap-energy budgets.

## Recovery

Add aerodynamic load once, apply tire load sensitivity, subtract drag once, and choose the earlier energy or thermal stint limit.

## Limiting cases and invariants

- Downforce and drag both tend to zero with speed squared.
- Unlimited energy does not remove the thermal lap limit.
- Every aerodynamic contribution enters each force or energy ledger exactly once.

## Independent evidence

A separately formulated coupled force-and-budget reference recomputes all five scenarios without production code or results.

## Common mistakes

- Treating downforce as linear tire capacity despite load sensitivity.
- Counting aero load twice.
- Omitting drag work from the stint energy budget.

## Formative checks

1. Why can more downforce yield less than proportional tire force?
2. Which limit binds the default stint?

## Teach-back

Explain the force signs, energy units, load-sensitivity exponent, bounded lap limit, double-counting failure, and exact coupled recovery.
