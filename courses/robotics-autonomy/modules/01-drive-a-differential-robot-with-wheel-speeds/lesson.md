# Drive a Differential Robot with Wheel Speeds

**Guiding question:** How do left and right wheel speeds determine a differential-drive robot's path?

## Concept and prediction

A differential drive has one body-forward velocity from the average wheel rim speed and one yaw rate from their difference. Constant commands trace a line, circle, or in-place rotation.

Before running the model, predict this: Equal wheel speeds make a straight line; increasing the right-minus-left speed bends the path counterclockwise. Record the sign and approximate scale you expect, not only “more” or “less.”

## Model, symbols, and equations

- $$v=\frac{r}{2}(\omega_R+\omega_L)$$ — The mean wheel rim speed is the body-forward speed.
- $$\Omega=\frac{r}{b}(\omega_R-\omega_L)$$ — Wheel-speed difference divided by track width sets positive counterclockwise yaw.
- $$x=\frac{v}{\Omega}\sin(\Omega t),\quad y=\frac{v}{\Omega}[1-\cos(\Omega t)]$$ — For nonzero yaw rate, the exact pose follows a circular arc.

Symbols and units:

- $r$ — wheel radius (m); $b$ — wheel track (m).
- $\omega_L,\omega_R$ — left and right angular speeds (rad/s).
- $v$ — body-forward speed (m/s); $\Omega$ — yaw rate (rad/s).
- $x,y$ — robot-center position (m); heading is positive counterclockwise (rad or deg).

The world frame starts at the robot center with +x forward and +y left. Positive wheel speed drives forward; positive yaw is counterclockwise.

## Manipulation: two one-variable sweeps

1. Sweep `left_wheel_rad_s` through [-6,6,12] while holding the other controls at baseline. Watch average and difference create spin, arc, and opposite-curvature motion.
2. Restore baseline, then sweep `track_width_m` through [0.2,0.35,0.7]. For the same wheel-speed difference, a wider track must reduce yaw rate.

The first plot shows the physical response. The second exposes the mechanism or residual that decides whether the result is trustworthy. Every axis states its unit.

## Evidence and limiting cases

Use the metric cards and both plots to test the prediction. The retained expected vectors are produced by an independent closed-form source-model calculation; the actual vectors come from this Python experiment.

- When $\omega_L=\omega_R$, $\Omega=0$ and the arc limit becomes $x=vt, y=0$.
- When $\omega_R=-\omega_L$, $v=0$ and the center rotates in place.
- Doubling $b$ at fixed wheel speeds halves $\Omega$.

This is simulated software evidence. It does not demonstrate a physical robot, motor, encoder, IMU, bench, HIL, field, or production result.

## Intentionally broken assumption

**Decoupled translation.** The broken model accumulates heading but keeps translating along world +x. It violates the body-to-world velocity rotation and produces zero lateral displacement during a turn.

## Explanation and recovery

Disable the decoupled-translation mode so the instantaneous heading rotates the velocity vector. Recovery is complete only when the diagnostic signature returns to the independent reference tolerance and you can explain why.

## Common mistakes

- Mapping one wheel directly to world x and the other to world y.
- Confusing commanded wheel angular speed with rim speed or achieved speed under slip.

- Changing several controls at once and losing causal attribution.
- Treating a plausible plot as proof without checking units, residuals, and limiting cases.

## Focused check and teach-back

At baseline, identify one equation term changed by each sweep, reproduce the broken symptom, recover it, and cite one metric plus one plot feature as evidence. Then teach it back in two minutes: state the convention, derive the governing relationship, name the failed assumption, and explain why the recovery works.

