# Decode and Plot CAN Signals

> **Guiding question:** How do byte order, scale, DLC, and freshness turn a raw CAN frame into a trustworthy engineering signal?

## Physical model, protocol, and units

This laboratory treats CAN identifier `0x139` as a documented eight-byte frame. The first wheel-speed field occupies bytes 0 and 1 in big-endian order. If `H` and `L` are the unsigned bytes, `count = 256H + L` and `speed_kmh = count / 128`. The SI conversion is `speed_m_s = speed_kmh / 3.6`. The baseline `0x12 0x00` therefore means 4608 counts, 36 km/h, or 10 m/s.

A decoder is more than a scale. It must check identifier, DLC, field layout, timestamp order, and freshness. This bounded model declares a 100 ms freshness limit and nine plotted samples. A round trip multiplies the decoded value by 128; a correct lossless decode returns the original count. Raw counts are unsigned, timestamps increase in milliseconds, and speed is a magnitude in the vehicle-forward direction.

The implementation is a Python-first native design derived from the reviewed P17 identity and synthetic protocol fixture. Its source folder was scaffolded; this is not source- or MATLAB-runtime equivalence.

## Predict and sweep one variable at a time

1. Hold frame age at 40 ms and predict the engineering value for 0, 4608, and 65535 counts. The response must be linear and nonnegative.
2. Restore 4608 counts and sweep age through 0, 100, and 250 ms. Decoded speed stays unchanged, but the last case is stale and invalid.

This separation matters: plausible payload values do not make an old frame current. Conversely, a fresh timestamp cannot repair the wrong byte order.

## Named broken behavior and exact recovery

**Broken behavior:** reverse the high and low bytes. `0x1200` becomes `0x0012`; the engineering value changes and the round-trip count error is nonzero. The invalid flag is explicit even though the plot remains finite.

**Exact recovery:** restore big-endian order, DLC 8, the 1/128 scale, and age at or below 100 ms. Set 4608 counts and 40 ms to reproduce the baseline signature exactly.

## Limits and limiting cases

Zero count produces zero speed. Maximum count remains bounded by the unsigned 16-bit field. Exactly 100 ms is accepted; any greater age is stale. The lab decodes one documented field and does not model arbitration, bus loading, bit timing, electrical faults, multiplexing, counter/CRC policies, or a complete DBC.

## Common mistakes

- Applying little-endian byte order because the host CPU is little-endian.
- Multiplying by 128 instead of dividing by the documented scale denominator.
- Ignoring DLC, identifier, timestamp, or freshness because the value “looks right.”
- Plotting mixed timestamps as though their arrival order were source time.
- Calling synthetic replay measured track telemetry.

## Formative checks

1. Decode `0x1200` by hand in counts, km/h, and m/s.
2. Explain why age changes validity but not payload value.
3. Use the round-trip residual to diagnose the endian defect.
4. State which protocol checks remain outside this bounded decoder.

## Teach-back checklist

- [ ] I can state identifier, DLC, bytes, byte order, scale, and units.
- [ ] I predicted both one-variable sweeps.
- [ ] I diagnosed the named broken behavior and exact recovery.
- [ ] I can distinguish a finite plot from a valid frame.
- [ ] I can state the evidence boundary.

This is not measured-vehicle, firmware, radio, bench, track, hardware/HIL, certification, release, or production evidence.
