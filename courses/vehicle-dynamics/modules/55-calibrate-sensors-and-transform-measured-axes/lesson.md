# Calibrate Sensors and Transform Measured Axes

This competency-derived Python-first lesson is not a source conversion and is not a measured-vehicle result. Its acceleration, mounting, and bias values are synthetic.

## Model and equations

- `a_sensor=S_sensor R(-psi_mount)a_body+b_sensor`
- `a_body_hat=R(psi_mount)S_sensor^-1(a_sensor-b_sensor)`
- `yaw_body=yaw_measured-b_yaw`

Calibration operates in native sensor coordinates. The orthonormal rotation then maps forward-left sensor components into declared vehicle body axes.

## Baseline workflow

Generate a biased, scaled, rotated sensor vector, remove fixed sensor bias, divide by the declared axis scales, convert mounting yaw to radians, rotate into body axes, and remove yaw-rate bias. Check component residual and norm closure.

## Two one-variable sweeps

Change only yaw-rate bias, then change only mounting yaw. The first affects the scalar channel; the second changes the intermediate sensor components while the recovered body vector stays fixed.

## Intentionally broken case

Send degrees directly to sine and cosine and leave scale and bias errors in the calibrated channels.

## Recovery

Declare axes and signs, remove bias and scale before rotation, convert degrees once at the interface, and verify both component truth and the rotation norm invariant.

## Limiting cases and invariants

- Zero mounting yaw reduces the rotation to identity.
- Orthonormal rotation preserves vector norm.
- Correct bias removal recovers the same body vector for every permitted mounting angle.

## Independent evidence

A separate rotation-and-bias formulation recomputes all signatures without production imports or output.

## Common mistakes

- Removing bias after rotating it into an incompatible frame.
- Mixing left-positive and right-positive lateral axes.
- Passing degree values to radian trigonometric functions.

## Formative checks

1. Why does norm closure alone not prove correct axes?
2. Where must yaw-rate bias be removed?

## Teach-back

Explain sensor and body frames, bias order, radian conversion, norm closure, the degree-input failure, and recovery.
