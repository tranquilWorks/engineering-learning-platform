# Compute Arm Forward Kinematics

**Guiding question:** What inputs, observable effects, and failure modes matter when you compute Arm Forward Kinematics?

## Concept and prediction

Forward kinematics composes joint rotations along a serial chain. The second link's world angle is the sum of the first and second relative joint angles.

Before running the model, predict this: Changing joint 1 rotates both links, while changing joint 2 rotates only the second link relative to the first. Record the sign and approximate scale you expect, not only “more” or “less.”

## Model, symbols, and equations

- $$x_e=L_1\cos q_1,\quad y_e=L_1\sin q_1$$ — The elbow is the endpoint of link 1.
- $$x_t=x_e+L_2\cos(q_1+q_2)$$ — The tool x coordinate includes the accumulated second-link angle.
- $$y_t=y_e+L_2\sin(q_1+q_2)$$ — The tool y coordinate uses the same accumulated angle.

Symbols and units:

- $q_1$ — base joint angle (deg at the control, rad internally).
- $q_2$ — elbow angle relative to link 1 (deg at the control, rad internally).
- $L_1,L_2$ — link lengths (m).
- $(x_e,y_e)$ and $(x_t,y_t)$ — elbow and tool positions in the base frame (m).

The base frame is right-handed with +x right and +y up. Positive joint angles are counterclockwise; $q_2=0$ means the links are collinear.

## Manipulation: two one-variable sweeps

1. Sweep `joint1_deg` through [-60,35,120] while holding the other controls at baseline. The entire arm should rigidly rotate about the base.
2. Restore baseline, then sweep `joint2_deg` through [-120,-45,60]. The elbow stays fixed while the tool sweeps a circle of radius $L_2$.

The first plot shows the physical response. The second exposes the mechanism or residual that decides whether the result is trustworthy. Every axis states its unit.

## Evidence and limiting cases

Use the metric cards and both plots to test the prediction. The retained expected vectors are produced by an independent closed-form trigonometric endpoint calculation; the actual vectors come from this Python experiment.

- At $q_1=q_2=0$, the tool is at $(L_1+L_2,0)$.
- The tool distance from the base cannot exceed $L_1+L_2$.
- Changing $q_2$ leaves the elbow coordinates unchanged.

This is simulated software evidence. It does not demonstrate a physical robot, motor, encoder, IMU, bench, HIL, field, or production result.

## Intentionally broken assumption

**Absolute second-joint angle.** The broken model projects link 2 using $q_2$ alone. It violates the serial-chain convention that the second link inherits the base rotation.

## Explanation and recovery

Disable absolute-joint-2 mode and accumulate serial joint angles before projecting each link. Recovery is complete only when the diagnostic signature returns to the independent reference tolerance and you can explain why.

## Common mistakes

- Treating a relative joint angle as a world-frame angle.
- Mixing degree-valued controls with radian-valued trigonometric functions.

- Changing several controls at once and losing causal attribution.
- Treating a plausible plot as proof without checking units, residuals, and limiting cases.

## Focused check and teach-back

At baseline, identify one equation term changed by each sweep, reproduce the broken symptom, recover it, and cite one metric plus one plot feature as evidence. Then teach it back in two minutes: state the convention, derive the governing relationship, name the failed assumption, and explain why the recovery works.

