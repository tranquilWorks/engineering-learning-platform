# Calibrate Sensor Extrinsics

**Guiding question:** What inputs, observable effects, and failure modes matter when you calibrate Sensor Extrinsics?

## Concept and prediction

Extrinsic calibration estimates the rigid transform from a sensor frame to the robot body frame. In two dimensions that transform contains one yaw angle and two translation components. Translation and rotation must be observable in the correspondence geometry.

Predict what the residual vectors will look like if the true sensor yaw is 12 deg but the calibration solves only translation. Will adding more correspondences remove that systematic pattern?

## Model, symbols, and equations

- $$\mathbf p_i^B=R(\psi_{BS})\mathbf p_i^S+\mathbf t_{BS}+\mathbf n_i$$ — sensor-to-body correspondence model.
- $$R^*=\arg\min_{R\in SO(2)}\sum_i\|\tilde{\mathbf p}_i^B-R\tilde{\mathbf p}_i^S\|^2$$ — centered rigid alignment.
- $$\mathbf t^*=\bar{\mathbf p}^B-R^*\bar{\mathbf p}^S$$ — translation recovered from centroids.

Superscripts identify the frame in which a point is expressed. +x is forward, +y is left, and positive yaw is counterclockwise. Units are metres for translation, millimetres for displayed residuals, and degrees at the interface but radians internally for yaw.

## Manipulation: two one-variable sweeps

1. Sweep `sensor_yaw_deg` through [-30,0,30]. A correct rigid fit should track yaw while keeping residual RMS near the noise floor.
2. Restore baseline, then sweep `noise_mm` through [0,2,20]. Parameter error and residual RMS should grow with correspondence noise.

The first plot overlays transformed sensor points and body-frame references. The second shows whether residual error is random or index-dependent.

## Evidence and limiting cases

The independent reference uses the closed-form planar Procrustes angle from cross/dot sums, whereas the production calibration uses an SVD-based proper-rotation solution.

- With zero yaw, translation-only and rigid fits coincide apart from noise.
- With zero noise and non-collinear correspondences, the rigid transform is recovered to numerical precision.
- Repeating one point cannot make rotation observable; spatially distributed correspondences are required.

This is simulated calibration evidence, not a physical metrology, robot, sensor, bench, HIL, or field result.

## Intentionally broken assumption

**Translation-only extrinsic.** Broken mode fixes $R=I$ and fits only the centroid offset. It can align the center but not the orientation.

## Explanation and recovery

Disable translation-only fitting, center both point sets, estimate the proper $SO(2)$ rotation, then recover translation. Reject a reflected solution by enforcing determinant +1.

## Common mistakes

- Reversing the body-to-sensor and sensor-to-body transform.
- Estimating translation before accounting for rotation.
- Using nearly coincident or collinear calibration poses and assuming all degrees of freedom are observable.
- Interpreting low residual on a narrow calibration set as guaranteed extrapolation accuracy.

## Focused check and teach-back

At baseline, cite estimated translation, yaw, and residual RMS. Reproduce the translation-only residual pattern, recover the rigid fit, and teach back the frame convention, observability requirement, equation order, and reflection check.
