# Construct a GR86 Digital Twin

> **Guiding question:** How should a baseline digital twin connect interfaces, residuals, and requirements without claiming physical-vehicle validation?

## Physical model, interfaces, and units

This software-only baseline integrates 61 samples over 12 seconds. A deterministic drive-force history and quadratic drag give free longitudinal acceleration `(F_drive - F_drag)/m`, capped by `0.35 mu g`. Speed is integrated in m/s. Synthetic steering enters in degrees, is converted to radians exactly once, divided by the 13:1 steering ratio, and mapped to kinematic yaw `r = v tan(delta_wheel)/L` with `L = 2.57 m`. A friction-derived yaw bound limits `|r| <= mu g/v`.

Midpoint heading integrates global x and y. A separate nominal run at 1320 kg and `mu=1.0`, plus small deterministic observation offsets, is the synthetic telemetry reference. The twin reports speed, position, and yaw-rate RMSE; final speed; integrated distance; a 2400 m lap-time proxy; and three traceable residual requirements (`<1 m/s`, `<3 m`, `<0.05 rad/s`).

This Python-first native P24 integration derives from the reviewed scaffold. “GR86” names the curriculum target and declared parameter baseline; it does not mean a physical car, real telemetry, source equivalence, or MATLAB-runtime comparison was validated.

## Predict and sweep one variable at a time

1. Hold friction at 1.0 and sweep mass from 1150 through 1320 to 1500 kg. Predict speed residual and lap-time proxy changes.
2. Restore 1320 kg and sweep friction from 0.70 through 1.0 to 1.30. Predict when traction and yaw bounds change the residuals.

Trace cause and unit across each interface: force → acceleration → speed → yaw/path → residual → requirement. A small scalar residual cannot excuse a broken interface.

## Named broken behavior and exact recovery

**Broken behavior:** divide the steering-degree number by the steering ratio but never convert degrees to radians. The wheel angle becomes about 57 times too large; yaw saturates and position/yaw residual requirements fail. Output remains bounded by the friction cap and is explicitly invalid.

**Exact recovery:** convert steering degrees with `pi/180` exactly once before applying the steering ratio. Restore 1320 kg and `mu=1.0`; all three residual requirements and the exact baseline signature return.

## Limits and limiting cases

Higher mass reduces free acceleration; lower friction tightens traction and yaw bounds. At zero steering, yaw is zero and the path is locally straight. This baseline omits engine maps, gear selection, tire slip states, suspension, aero balance, road grade, thermal states, actuator dynamics, parameter calibration, real CAN/GPS/IMU ingestion, uncertainty propagation, and closed-loop validation.

## Common mistakes

- Treating degrees as radians at a subsystem boundary.
- Comparing residuals produced from different input histories.
- Tuning parameters on the same samples and calling the result validation.
- Treating requirement count as proof of physical fidelity.
- Calling synthetic nominal observations real GR86 telemetry.

## Formative checks

1. Trace every unit from drive force to lap proxy.
2. Explain why yaw is bounded by lateral acceleration capacity.
3. Identify which residual exposes the steering defect first.
4. State what data and tests physical validation would require.

## Teach-back checklist

- [ ] I can trace the integrated model interfaces.
- [ ] I predicted both one-variable sweeps.
- [ ] I can map each residual to its requirement.
- [ ] I diagnosed the named broken behavior and exact recovery.
- [ ] I can distinguish a software baseline from physical validation.

This is not measured-vehicle, real-GR86, firmware, radio, bench, vehicle/track, browser/accessibility, learner, physical HIL/hardware, certification, release, or production evidence.
