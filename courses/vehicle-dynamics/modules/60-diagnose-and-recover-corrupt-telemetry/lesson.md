# Diagnose and Recover Corrupt Telemetry

This competency-derived Python-first lesson is not a source conversion and is not a measured-vehicle result. It applies a declared fault plan to the immutable synthetic GR86 BLE replay fixture.

## Model and equations

- `missing=expected_sequences-valid_unique_sequences`
- `malformed={k where payload_length(k)!=4+DLC(k)}`
- `recovered=sort(unique(valid_packets)) subject to bounded reorder window`

The injected faults are one missing sequence, one duplicate, one adjacent inversion, and one truncated payload. The malformed record is also absent from the valid recovered sequence set.

## Baseline workflow

Load nominal records and the fault plan, apply operations in order, count each fault class, reject invalid payload length, deduplicate valid packets, apply bounded reordering, and verify the recovered-record ledger.

## Two one-variable sweeps

Reduce only the inspection limit, then reduce only the reorder window to zero. The first limits which declared faults enter the window; the second makes the inversion unrecoverable without affecting other diagnoses.

## Intentionally broken case

Trust every arrival as complete, unique, well formed, and correctly ordered. This reports no faults and accepts the corrupted record count as recovered.

## Recovery

Compare payload length with nominal DLC, retain separate missing and malformed diagnoses, remove duplicates, reorder only inside policy, and never synthesize the missing payload.

## Limiting cases and invariants

- A fault outside the inspection limit is not counted.
- A zero reorder window rejects the inverted record from the ordered recovery.
- Malformed payloads never enter the valid recovered set.

## Independent evidence

A separate sequence-set and policy calculation derives all fault counts and recovery totals without importing production code or consuming its result.

## Common mistakes

- Counting malformed data as valid because a sequence field exists.
- Deduplicating before retaining a duplicate diagnostic.
- Sorting every packet without enforcing a bounded recovery policy.

## Formative checks

1. Why does malformed sequence 89 also appear missing from valid data?
2. Which corruption can be corrected without inventing a payload?

## Teach-back

Explain fixture provenance, four fault classes, valid-set construction, bounded reordering, trust-everything failure, and exact recovery.
