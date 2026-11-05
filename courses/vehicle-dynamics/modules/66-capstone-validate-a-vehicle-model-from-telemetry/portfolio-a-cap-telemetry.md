# A-CAP-TELEMETRY integration evidence

Integrate these existing lessons: P17, P18, P19, P20, P24, P25, P33, P52, P53, P54, P55, P56, P57, P58, P59, P60, P66.

Required evidence: Trace requirements from replay integrity through state reconstruction, held-out model validation, fault diagnosis, and recovery in P66.

## Derive and predict

Use P17: Decode the wheel-speed payload by hand and decide whether a correctly decoded frame is fresh enough to use. A raw count of 4608 equals hexadecimal 0x1200. Big-endian decoding followed by division by 128 gives 36 km/h, or 10 m/s. Reversing the bytes gives 18 counts and only 0.140625 km/h. Byte identity, engineering-value correctness and freshness are separate checks. A frame older than 100 ms is rejected even if its speed looks plausible; do not silently carry it forward as current evidence. Connect this result to at least one other listed lesson, identifying the exact quantity, units and assumption transferred across their interface.

## Compare connected mechanisms

Use P25: Compare path, body and wheel velocity components while proving norm preservation and checking direction. A planar rotation preserves vx²+vy² because R transpose times R is identity. Rotating a 10 m/s inertial x-vector into a frame turned 90 degrees gives approximately (0,-10) m/s under R(-psi). Norm preservation alone cannot expose using a degree value as radians: the wrong angle still makes an orthogonal matrix. Compare the actual expected components and inverse transform, not only the norm residual. Connect this result to at least one other listed lesson, identifying the exact quantity, units and assumption transferred across their interface.

## Diagnose and recover

Use P56: Trace heading integration and explain the sample-time factor in position correction. Yaw rate in degrees/s is converted to radians/s before multiplying by 0.05 s. Position prediction uses the previous heading and speed. The correction is gps_blend*dt*(GPS-prediction), so gps_blend acts as a rate in 1/s and its per-sample weight at 0.12 is 0.006. Changing the sample rate without retaining dt would change the observer. Separate integrated speed path length from the length of the GPS-corrected position curve. Connect this result to at least one other listed lesson, identifying the exact quantity, units and assumption transferred across their interface.

## Integrate and defend the boundary

Use P66: Trace a telemetry requirement from exact bytes through synchronization, calibration, reconstruction and untouched validation. Establish CAN/BLE payload identity before decoding, then fit clock rate/offset from the three explicit synchronization pairs. Apply the separate speed gain/bias calibration and yaw-bias correction before trajectory reconstruction. The force channel is synthetic 1450*a+0.45*v²+2*sin(0.9*i), not a claim about the fixture's IMU channel. Freeze the chronological fitting prefix before computing held-out residuals. For every passing requirement, identify its actual residual or event evidence and reproduce the injected fault and deterministic recovery. Connect this result to at least one other listed lesson, identifying the exact quantity, units and assumption transferred across their interface.

## Required integration artifact

Produce a requirement-by-requirement P66 dossier with source record identities, redundant CAN/BLE comparison, fault events, clock synchronization pairs, sensor calibration values, reconstructed states, chronological training/validation indices and held-out force residuals. Trace each pass/fail flag to an actual computed quantity and its threshold. Document that force observations are synthesized from acceleration and v² rather than taken from an unrelated fixture IMU field. Change fault severity and validation fraction separately, retain broken and recovered results, and explain why recovery relies on an intact redundant source. Keep the P67 physical-subsystem integration as a separate capstone.

## Four-criterion rubric

1. Governing reasoning: equations, units and frame/sign conventions justify a numerical prediction; naming an algorithm alone earns no evidence.
2. Controlled comparison: two isolated sweeps and at least one limiting case distinguish mechanisms and make a falsifiable claim.
3. Diagnose and recover: identify the first failing assumption from actual outputs, restore it and demonstrate deterministic recovery.
4. Integration and scope: show the value passed between stages, an independently checked result, and a limitation that prevents a broader claim.

Retain inputs, selected outputs and your explanation as a cumulative artifact. No learner completion, automatic score, physical qualification or production acceptance is recorded.
