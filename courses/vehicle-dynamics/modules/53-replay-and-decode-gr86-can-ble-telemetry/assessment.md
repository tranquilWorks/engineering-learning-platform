# P53 course checkpoint

## Predict and derive

Verify transport identity separately from engineering-value decoding and keep unlike channels on separate axes.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `BLE=[CAN_ID_little_endian(4 bytes),CAN_payload]`
- `engine_speed=uint16_big_endian(bytes[0:2]) scale`
- `parity=(sequence,time,CAN_ID,payload)_CAN==(sequence,time,CAN_ID,payload)_BLE`

## Controlled comparison

- `record_limit`: 60 → 96. Hold the other controls at baseline; predict and explain the change before executing.
- `engine_scale_rpm_count`: 0.25 → 0.27. Hold the other controls at baseline; predict and explain the change before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

The BLE payload starts with the CAN identifier encoded little-endian, followed by the original data bytes. The engine-speed field inside those bytes is big-endian with its own rpm/count scale; transport and signal byte orders need not match. Byte-for-byte parity can therefore pass while a signal decoder is wrong. Engine residuals are divided by 1 rpm and wheel-speed residuals by 1 km/h before their dimensionless RMS is combined.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

The fixture explicitly declares synthetic provenance. Correct replay does not establish live GR86 bus access, measured behavior or coverage of every identifier.

Competency links: VD-TELEMETRY-PROTOCOL. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
