# A-TELEMETRY integration evidence

Integrate these existing lessons: P17, P53, P54, P60.

Required evidence: Replay exact synthetic GR86 CAN and BLE fixtures, verify packet/decode identity, detect ordering/dropout faults, and recover the canonical signal table.

## Derive and predict

Use P17: Decode the wheel-speed payload by hand and decide whether a correctly decoded frame is fresh enough to use. A raw count of 4608 equals hexadecimal 0x1200. Big-endian decoding followed by division by 128 gives 36 km/h, or 10 m/s. Reversing the bytes gives 18 counts and only 0.140625 km/h. Byte identity, engineering-value correctness and freshness are separate checks. A frame older than 100 ms is rejected even if its speed looks plausible; do not silently carry it forward as current evidence. Connect this result to at least one other listed lesson, identifying the exact quantity, units and assumption transferred across their interface.

## Compare connected mechanisms

Use P53: Verify transport identity separately from engineering-value decoding and keep unlike channels on separate axes. The BLE payload starts with the CAN identifier encoded little-endian, followed by the original data bytes. The engine-speed field inside those bytes is big-endian with its own rpm/count scale; transport and signal byte orders need not match. Byte-for-byte parity can therefore pass while a signal decoder is wrong. Engine residuals are divided by 1 rpm and wheel-speed residuals by 1 km/h before their dimensionless RMS is combined. Connect this result to at least one other listed lesson, identifying the exact quantity, units and assumption transferred across their interface.

## Diagnose and recover

Use P54: Apply the known clock offset before interpolation and quantify the gaps created by drops. Source time equals reference time plus the declared offset. At 12 ms, subtract 0.012 s before resampling; this example applies a known offset rather than estimating it from data. The base period is 20 ms and an isolated missing interior sample creates a 40 ms interpolation span. Record maximum gap and interpolation error separately. Endpoint extension by the interpolator is not a new measurement. Connect this result to at least one other listed lesson, identifying the exact quantity, units and assumption transferred across their interface.

## Integrate and defend the boundary

Use P60: Classify missing, duplicate, inverted and malformed records before deciding what can actually be recovered. Dropping sequence 37 and truncating 89 create two unusable expected records in the full fixture; a duplicate at 52 and inversion at 71/72 are different faults. Deduplicate and sort only valid records, and enforce the declared reordering window. Recovery means a valid ordered subset, not inventing the missing payloads. Compare record identities and payload lengths with the nominal fixture, then replay the same diagnosis after reset. Connect this result to at least one other listed lesson, identifying the exact quantity, units and assumption transferred across their interface.

## Required integration artifact

Retain fixture identifiers and hashes, sequence/timestamps, exact CAN identifier bytes, BLE framing and decoded engineering values for a small replay excerpt. Demonstrate little-endian identifier framing alongside big-endian signal decoding and show a case where byte parity passes but interpretation fails. Classify each injected drop, duplicate, inversion and malformed payload by record identity. Recover only valid records within the declared reorder window and preserve the unrecoverable missing set. Explain freshness independently of value correctness. State that all inputs are synthetic protocol fixtures and no live bus or radio was exercised.

## Four-criterion rubric

1. Governing reasoning: equations, units and frame/sign conventions justify a numerical prediction; naming an algorithm alone earns no evidence.
2. Controlled comparison: two isolated sweeps and at least one limiting case distinguish mechanisms and make a falsifiable claim.
3. Diagnose and recover: identify the first failing assumption from actual outputs, restore it and demonstrate deterministic recovery.
4. Integration and scope: show the value passed between stages, an independently checked result, and a limitation that prevents a broader claim.

Retain inputs, selected outputs and your explanation as a cumulative artifact. No learner completion, automatic score, physical qualification or production acceptance is recorded.
