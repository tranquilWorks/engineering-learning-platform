# Transform Coordinates Between Frames

**Guiding question:** What inputs, observable effects, and failure modes matter when you transform Coordinates Between Frames?

## Concept and prediction

A rigid transform combines a rotation with a translation. Order and frame labels matter: rotating a body-frame vector and then adding the world-frame origin is not interchangeable with translating first.

Before running the model, predict this: A positive heading rotates body +x toward world +y before the robot-origin translation is added. Record the sign and approximate scale you expect, not only “more” or “less.”

## Model, symbols, and equations

- $${}^{W}\!p=R(\theta){}^{B}\!p+{}^{W}\!t_B$$ — Rotate the body-frame point, then translate it into the world frame.
- $$R(\theta)=\begin{bmatrix}\cos\theta&-\sin\theta\\\sin\theta&\cos\theta\end{bmatrix}$$ — Positive angles rotate counterclockwise in the x-y plane.
- $${}^{B}\!p=R(\theta)^T({}^{W}\!p-{}^{W}\!t_B)$$ — The inverse subtracts translation before applying the transpose.

Symbols and units:

- $R$ — dimensionless planar rotation matrix.
- $\theta$ — robot heading (degrees in the control, radians inside trigonometry).
- ${}^{B}p$ — point coordinates in the robot/body frame (m).
- ${}^{W}t_B$ and ${}^{W}p$ — robot origin and point in the world frame (m).

Frames are right-handed with +x forward/right and +y left/up. Superscripts name the coordinate frame; positive angles are counterclockwise.

## Manipulation: two one-variable sweeps

1. Sweep `heading_deg` through [-90,30,120] while holding the other controls at baseline. Trace how the same body point rotates around the robot origin.
2. Restore baseline, then sweep `point_x_m` through [-1,1.2,2.5]. Confirm that translation does not change the vector's length from the robot origin.

The first plot shows the physical response. The second exposes the mechanism or residual that decides whether the result is trustworthy. Every axis states its unit.

## Evidence and limiting cases

Use the metric cards and both plots to test the prediction. The retained expected vectors are produced by an independent matrix calculation plus inverse-transform invariant; the actual vectors come from this Python experiment.

- At $\theta=0$, the result is the body point plus the robot translation.
- At $\theta=90^\circ$, body $(x,y)$ maps to world offset $(-y,x)$.
- Forward then inverse transformation must recover the original point to roundoff.

This is simulated software evidence. It does not demonstrate a physical robot, motor, encoder, IMU, bench, HIL, field, or production result.

## Intentionally broken assumption

**Rotation-sign mismatch.** The forward transform uses $R(-\theta)$ while the inverse still assumes $R(\theta)$. The round-trip residual exposes the inconsistent frame convention.

## Explanation and recovery

Disable the reversed-rotation mode and use one declared body-to-world rotation convention in both directions. Recovery is complete only when the diagnostic signature returns to the independent reference tolerance and you can explain why.

## Common mistakes

- Feeding degrees directly to sine and cosine functions that expect radians.
- Adding translation before rotation without stating which frame contains the translation.

- Changing several controls at once and losing causal attribution.
- Treating a plausible plot as proof without checking units, residuals, and limiting cases.

## Focused check and teach-back

At baseline, identify one equation term changed by each sweep, reproduce the broken symptom, recover it, and cite one metric plus one plot feature as evidence. Then teach it back in two minutes: state the convention, derive the governing relationship, name the failed assumption, and explain why the recovery works.

