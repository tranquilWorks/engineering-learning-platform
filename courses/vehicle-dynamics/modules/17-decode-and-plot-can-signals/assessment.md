# P17 course checkpoint

## Predict and derive

Decode the wheel-speed payload by hand and decide whether a correctly decoded frame is fresh enough to use.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `count=256*byte0+byte1; speed_kmh=count/128; speed_m_s=speed_kmh/3.6`

## Controlled comparison

- `raw_count`: 4608 → 0. Hold the other controls at baseline; predict and explain the change before executing.
- `frame_age_ms`: 40 → 250. Hold the other controls at baseline; predict and explain the change before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

A raw count of 4608 equals hexadecimal 0x1200. Big-endian decoding followed by division by 128 gives 36 km/h, or 10 m/s. Reversing the bytes gives 18 counts and only 0.140625 km/h. Byte identity, engineering-value correctness and freshness are separate checks. A frame older than 100 ms is rejected even if its speed looks plausible; do not silently carry it forward as current evidence.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

This protocol fixture is synthetic and covers a declared identifier and byte layout, not all GR86 firmware or a live bus.

Competency links: VD-TELEMETRY-PROTOCOL. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
