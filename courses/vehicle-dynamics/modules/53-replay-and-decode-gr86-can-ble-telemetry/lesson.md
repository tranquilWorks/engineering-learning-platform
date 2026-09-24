# Replay and Decode GR86 CAN/BLE Telemetry

This competency-derived Python-first lesson is not a source conversion and is not a measured-vehicle result. It uses the immutable synthetic GR86 protocol fixture and its declared public-source provenance.

## Model and equations

- `BLE=[CAN_ID_little_endian(4 bytes),CAN_payload]`
- `engine_speed=uint16_big_endian(bytes[0:2]) scale`
- `parity=(sequence,time,CAN_ID,payload)_CAN==(sequence,time,CAN_ID,payload)_BLE`

The transport identifier is little-endian, while documented multi-byte signals inside the CAN payload are big-endian. These are independent byte-order decisions.

## Baseline workflow

Replay the first 60 nominal CAN and BLE records, compare sequence, time, identifier, and payload, then decode engine and wheel speed into declared units. Inspect parity failures and engineering-value RMSE separately.

## Two one-variable sweeps

Increase only the replay limit to exercise more scheduled identifiers. Then change only engine scale to expose a calibration residual without changing transport parity.

## Intentionally broken case

Decode signal words as little-endian. Packet identity still passes, but the engineering values become physically inconsistent.

## Recovery

Preserve the BLE identifier layout, extract the unchanged CAN bytes, then apply each signal's documented byte range, big-endian order, scale, offset, and unit.

## Limiting cases and invariants

- The minimum replay still includes engine and wheel-speed frames.
- Nominal CAN and BLE packets remain byte-identical after removing the four-byte BLE identifier.
- Correct scale and byte order produce zero decode residual.

## Independent evidence

A separately formulated schedule and encoder reconstructs the retained scalar signatures without importing the production experiment or consuming its output.

## Common mistakes

- Applying one byte order to both transport framing and signal words.
- Treating packet equality as decoded-value validation.
- Losing units when a raw count becomes an engineering quantity.

## Formative checks

1. Why can parity remain zero while decode RMSE is large?
2. Which four BLE bytes carry the CAN identifier?

## Teach-back

Explain the two byte-order domains, replay provenance, signal scaling, parity invariant, named endian failure, and exact recovery.
