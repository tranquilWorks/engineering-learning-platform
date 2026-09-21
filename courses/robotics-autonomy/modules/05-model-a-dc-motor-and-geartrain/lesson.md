# Model a DC Motor and Geartrain

**Guiding question:** What inputs, observable effects, and failure modes matter when you model a DC Motor and Geartrain?

## Concept and prediction

A DC motor converts current to torque and speed to back EMF. A reduction gear trades output speed for torque while reflecting load inertia and torque to the motor shaft.

Before running the model, predict this: Increasing voltage raises speed, while increasing reduction lowers output speed and reduces the motor-side load torque. Record the sign and approximate scale you expect, not only “more” or “less.”

## Model, symbols, and equations

- $$L\dot i=V-Ri-K_e\omega_m$$ — Applied voltage balances resistance, inductance, and back EMF.
- $$J_{eq}\dot\omega_m=K_t i-b\omega_m-\tau_L/N$$ — Motor torque accelerates reflected inertia and balances drag and reflected load.
- $$J_{eq}=J_m+J_L/N^2,\quad\omega_o=\omega_m/N$$ — An ideal reduction reflects inertia by $N^2$ and divides speed by $N$.

Symbols and units:

- $V$ — applied voltage (V); $i$ — armature current (A).
- $R,L$ — armature resistance (ohm) and inductance (H).
- $K_t$ — torque constant (N m/A); $K_e$ — back-EMF constant (V s/rad).
- $N$ — motor-speed/output-speed reduction ratio; $\omega_m,\omega_o$ — motor and output speed (rad/s).

Positive voltage, current, motor speed, and output speed share the drive direction. Positive load torque opposes that direction and is reflected to the motor as $\tau_L/N$.

## Manipulation: two one-variable sweeps

1. Sweep `voltage_v` through [6,12,18] while holding the other controls at baseline. Compare current transient and steady output speed.
2. Restore baseline, then sweep `gear_ratio` through [5,20,40]. Observe the speed/torque trade and reflected-load change.

The first plot shows the physical response. The second exposes the mechanism or residual that decides whether the result is trustworthy. Every axis states its unit.

## Evidence and limiting cases

Use the metric cards and both plots to test the prediction. The retained expected vectors are produced by an independent continuous-time linear state solution and steady-state torque balance; the actual vectors come from this Python experiment.

- At zero speed, back EMF is zero and current initially rises toward $V/R$.
- At steady state, both electrical and mechanical derivatives approach zero.
- With zero load torque, a larger ideal reduction lowers output speed even though motor speed is similar.

This is simulated software evidence. It does not demonstrate a physical robot, motor, encoder, IMU, bench, HIL, field, or production result.

## Intentionally broken assumption

**Missing back EMF.** The broken model sets $K_e=0$, allowing current to remain unrealistically high as speed rises. The final state disagrees with the independent continuous-time solution for the physical model.

## Explanation and recovery

Disable the no-back-EMF mode so generated voltage opposes applied voltage as speed rises. Recovery is complete only when the diagnostic signature returns to the independent reference tolerance and you can explain why.

## Common mistakes

- Multiplying load inertia by $N^2$ when reflecting it from output to motor.
- Using RPM in equations whose constants expect rad/s.

- Changing several controls at once and losing causal attribution.
- Treating a plausible plot as proof without checking units, residuals, and limiting cases.

## Focused check and teach-back

At baseline, identify one equation term changed by each sweep, reproduce the broken symptom, recover it, and cite one metric plus one plot feature as evidence. Then teach it back in two minutes: state the convention, derive the governing relationship, name the failed assumption, and explain why the recovery works.

