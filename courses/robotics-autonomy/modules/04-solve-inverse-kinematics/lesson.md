# Solve Inverse Kinematics

**Guiding question:** What inputs, observable effects, and failure modes matter when you solve Inverse Kinematics?

## Concept and prediction

Inverse kinematics uses the law of cosines to find the elbow angle, then subtracts the triangle's internal angle from the target bearing to find the shoulder angle.

Before running the model, predict this: A reachable target generally has two mirror-image elbow branches with the same tool position. Record the sign and approximate scale you expect, not only “more” or “less.”

## Model, symbols, and equations

- $$c_2=\frac{x_d^2+y_d^2-L_1^2-L_2^2}{2L_1L_2}$$ — The law of cosines determines the elbow cosine.
- $$q_2=\operatorname{atan2}(\pm\sqrt{1-c_2^2},c_2)$$ — The sign selects elbow-up or elbow-down.
- $$q_1=\operatorname{atan2}(y_d,x_d)-\operatorname{atan2}(L_2\sin q_2,L_1+L_2\cos q_2)$$ — The shoulder correction aligns the link triangle with the target bearing.

Symbols and units:

- $(x_d,y_d)$ — requested tool target in the base frame (m).
- $L_1,L_2$ — link lengths (m).
- $q_1,q_2$ — solved shoulder and relative elbow angles (rad internally, deg in metrics).
- $c_2$ — dimensionless law-of-cosines value; reachability requires $|c_2|\le1$.

The base frame uses +x right, +y up, and positive counterclockwise angles. Elbow-up chooses the negative square-root branch in this declared convention.

## Manipulation: two one-variable sweeps

1. Sweep `target_x_m` through [0.4,1,1.4] while holding the other controls at baseline. Watch conditioning worsen near the outer reach boundary.
2. Restore baseline, then sweep `target_y_m` through [-0.8,0.4,1]. Confirm the shoulder angle follows the target quadrant.

The first plot shows the physical response. The second exposes the mechanism or residual that decides whether the result is trustworthy. Every axis states its unit.

## Evidence and limiting cases

Use the metric cards and both plots to test the prediction. The retained expected vectors are produced by an independent law-of-cosines solution followed by an independent forward-kinematics round trip; the actual vectors come from this Python experiment.

- Reachable radius lies between $|L_1-L_2|$ and $L_1+L_2$.
- At a fully extended boundary, both branches merge at $q_2=0$.
- An unreachable target is projected only for visualization and must retain a nonzero target residual.

This is simulated software evidence. It does not demonstrate a physical robot, motor, encoder, IMU, bench, HIL, field, or production result.

## Intentionally broken assumption

**Missing shoulder correction.** The broken solver points link 1 directly at the target and still applies the elbow angle. The tool misses the target even though the law-of-cosines elbow value looks plausible.

## Explanation and recovery

Disable the omitted-shoulder-correction mode and include the link-triangle angle in the shoulder solution. Recovery is complete only when the diagnostic signature returns to the independent reference tolerance and you can explain why.

## Common mistakes

- Clipping an unreachable target and then reporting zero original-target error.
- Selecting a branch without documenting the sign convention.

- Changing several controls at once and losing causal attribution.
- Treating a plausible plot as proof without checking units, residuals, and limiting cases.

## Focused check and teach-back

At baseline, identify one equation term changed by each sweep, reproduce the broken symptom, recover it, and cite one metric plus one plot feature as evidence. Then teach it back in two minutes: state the convention, derive the governing relationship, name the failed assumption, and explain why the recovery works.

