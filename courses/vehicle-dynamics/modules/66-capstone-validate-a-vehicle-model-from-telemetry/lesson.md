# Execute a telemetry validation chain

This capstone uses the retained **synthetic protocol fixture**: 309 CAN frames and corresponding BLE packets over two seconds. It verifies a replay/analysis chain, not an actual car. Each TV requirement now names a computed quantity and threshold in the browser.

## Model and equations

First verify fixture hashes, the synthetic provenance manifest, sequence/time parity, the four-byte little-endian BLE CAN identifier and the remaining CAN bytes. Wheel speeds decode from four big-endian 16-bit values at $1/128$ km/h per count; divide by 3.6 to obtain m/s. Yaw uses $(u_{16}-32768)/100$ degrees/s and is converted to rad/s. The replay supplies 101 wheel-speed samples and a separate yaw schedule.

Fault severity $f$ adds logger time $t_L=(1+0.0008f)t+0.02f$ s. Three known sync markers fit its affine inverse. Synthetic sensor calibration uses $v_m=(1+0.02f)v+0.2f$ m/s and a zero-rate yaw bias $0.5f$ degrees/s. Two known speeds, 0 and 30 m/s, identify speed scale/bias; 15 m/s is an unused calibration check.

Align corrected samples onto the wheel source-time grid. Reconstruct heading with $\psi_{i+1}=\psi_i+r_i\Delta t$ and planar increments $v_i\Delta t(\cos\psi_i,\sin\psi_i)$. Estimate acceleration by a backward difference, avoiding future held-out samples.

The added force channel is explicitly synthetic:

\[F_i=1450a_i+0.45v_i^2+2\sin(0.9i)\quad[\mathrm N].\]

Mass is kg and the drag coefficient is kg/m. The fixture's separate IMU acceleration is not used as though it agreed with wheel-speed differentiation. Fit $F=ma+cv^2$ only before the chronological split. The held-out suffix never enters fitting. Residual covariance assumes this chosen linear model; column-normalized information eigenvalues diagnose identifiability without mixing raw physical units.

## Baseline workflow

Predict what a 1× fault severity does to an uncorrected 15 m/s calibration reading: $1.02(15)+0.2=15.5$ m/s, a 0.5 m/s error. Run validation fraction 0.3 and severity 1. The pipeline also flips a wheel-payload byte and inserts a duplicate BLE record. Healthy recovery compares them with an explicitly retained, valid redundant CAN stream.

Inspect reconstructed speed and held-out force residual. The baseline fit gives mass about 1450.035 kg and drag about 0.44929 kg/m; held-out RMS is about 1.460 N. All nine TV checks pass. The table separately displays provenance, clock, calibration, trajectory, state, held-out force, information, unresolved packets and recovered-speed closure. Thresholds are exercise requirements, not sensor specifications.

## Two one-variable sweeps

1. Keep severity 1 and reduce validation fraction from 0.3 to 0.2. More early samples enter fitting, but the remaining suffix is still unseen. Compare parameter estimates and held-out residual; do not demand monotonic improvement.
2. Restore fraction 0.3 and increase severity to 2. Larger timing/calibration offsets and a second corrupted wheel packet increase detected anomalies from two to three. Successful correction should recover nearly the same physical replay.

## Intentionally broken case

The broken chain skips time and sensor correction and leaves the actual corrupt/duplicate packets unresolved. It preserves the same chronological split. Measured calibration, trajectory, speed, force and recovery quantities then fail their checks; no TV status is assigned directly from the mode.

## Recovery

Restore alignment, calibration and redundant-stream recovery at identical controls. Verify zero unresolved anomalies and the recovered speed closure, then rerun the held-out prediction. A clean packet stream alone does not prove correct calibration.

## Limiting cases and invariants

With zero injected severity in an internal check, affine timing/calibration reduce to identity; the explicitly scheduled protocol fault still needs handling. Training indices precede all held-out indices, and backward differences use no future velocity. Parameter covariance is symmetric positive semidefinite. A rank-deficient acceleration/speed-squared design cannot identify mass and drag separately.

## Independent evidence

The reference reads only the shared raw fixture and manifest. It manually decodes bytes, uses two-point affine corrections, scalar trajectory integration and explicit two-column normal equations. Expected five-scenario results originate there; production outputs are recorded separately.

## Common mistakes

Do not mix CAN endian rules with BLE identifier endian rules, fit before aligning timestamps, leak validation samples into training, or treat synthetic force as measured telemetry. A small prediction residual can sometimes hide biased parameters; upstream calibration requirements still matter.

## Teach-back

- What makes packet recovery possible? A declared valid redundant CAN copy, not a guessed replacement value.
- Why normalize information columns? Acceleration and speed squared have different units; raw matrix conditioning is scale-dependent.
- Does covariance prove statistical coverage? No; the deterministic perturbation and assumed model do not validate coverage on physical data.

## Cumulative assessment

Decode a wheel frame with units, calculate one clock/calibration correction, identify the exact training/validation split, and trace one corrupt record into recovery. Explain which TV checks would still be needed if held-out residual alone looked small.

## Formative checks

At severity 1, a source event at 1 s has logger time 1.0208 s. Apply the inferred affine inverse and recover 1 s. Explain why subtracting the 0.02 s offset alone leaves a drift error. With 101 samples and validation fraction 0.3, the split index is 70: fit rows 1–69 and validate rows 70–100. The first acceleration row is excluded rather than treated as a physical derivative.

This Python-first native lesson is not a source conversion and does not establish a measured-vehicle result.
