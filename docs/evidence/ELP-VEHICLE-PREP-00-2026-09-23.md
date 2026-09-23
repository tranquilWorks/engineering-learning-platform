# ELP-VEHICLE-PREP-00 evidence — 2026-09-23

## Authorized identities

- Portfolio Control issue: `tranquilWorks/portfolio-control#467`.
- Reviewed competency map merge: `53c3878760ea0e08255714b1b1ff0456f8d8dfed`.
- Prep authorization: PR #469, amended by PRs #470, #472, and #473; active contract revision `2fd02a1b72536ee6f4ff59357a74be7dc99c72c8`.
- Target baseline: commit `8e5ff391f75f39218e51ed98aac8bcdb092550a0`, tree `bebb8579d33090a64201a7f2c8c4ad86595ada02`.
- Vehicle Dynamics source: commit `57264b3ffeb517ee5eb73e8957b9cd190d022457`, tree `d9e7267ba02c8d3d836c0ae481b80e91233eb81a`.
- Source curriculum SHA-256: `c452996e5253ec7e547a64cccd4aa8af60dc5f4106311d1dec25ec8d5c48eba6`.
- Reviewed map SHA-256: `87dae868d7e3a0181062a4fd42ff316513b0f6f35c053cb56b5d73b9c56bde6d`.
- Source ledger: 150 exact files; aggregate SHA-256 `15de22f8396cf978e80e55f2ed7541234804913c81dbef71cb85c81508472d11`.

## Preparation result

- Added an empty platform-owned `vehicle-dynamics` course shell.
- Mirrored the reviewed 67-module map byte-for-byte and validated its schema, ordered identities, prerequisite and reciprocal competency closure, eight bounded batches, fourteen assessments, and two capstones.
- Installed exact P01-P24 source, conversion, and coverage ledgers.
- Recorded P01-P02 as implemented in the pinned source and P03-P24 as source scaffolds.
- Coverage is total 24, pending 24, converted 0, blocked 0, placeholder 0.
- No `courses/vehicle-dynamics/modules` directory exists and no lesson was implemented.
- Advanced only the read-only Vehicle Dynamics source gitlink. Every other source gitlink remains unchanged.

## Synthetic GR86 CAN/BLE replay evidence

- Protocol source: `tranquilWorks/gr86-cca-telemetry` commit `f5d13fce5fcfc23a914f7da39e5bb448c56ed6b7`, tree `3c4edb0083fa93af8114497c145a7248bafd7ade`.
- Fixture classification: `synthetic_protocol_fixture`; `measured_vehicle_data=false`.
- Nominal replay: 309 CAN records and 309 RaceChrono BLE notifications.
- Each BLE packet retained the four-byte little-endian CAN identifier followed by the exact CAN data bytes.
- A separately formulated raw-byte decoder checked documented GR86 identifiers, byte order, scale, offset, units, and fixed anchor values without consulting generated decoded fields.
- Fault replay independently diagnosed missing sequences 37 and 89, duplicate 52, adjacent inversion 72→71, malformed sequence 89, and 307 recoverable unique valid records.
- Privacy exclusions passed: no VIN, driver identity, real location, precise route, or vehicle capture.

## Local verification

| Gate | Result |
| --- | --- |
| Vehicle prep + course-caliber focused tests | 21 passed |
| Retained DSP/Radar regression | 300 passed |
| Retained Controls/GNC regression | 118 passed |
| Retained Robotics/Autonomy regression | 97 passed |
| Contract suite | 72 passed |
| Quick backend suite | 612 passed, 3 dependency deprecation warnings |
| Full verification | 612 passed, deterministic catalog passed, TypeScript passed, production Vite build passed |
| Deterministic catalog | 6 courses, 223 modules, 223 interactive; no errors |
| Ruff | Target tests passed; exact fixture scripts passed with the contract's narrow I001/E731/RUF007 exclusions |
| Diff/source checks | `git diff --check` passed; Vehicle and DSP source checkouts clean |

The first full run stopped after the passing backend suite because local `node_modules` was absent. Dependencies were installed from the declared package manifests with package-lock creation disabled; no dependency manifest or lockfile changed. The exact full command was rerun and passed frontend typecheck and production build. Vite retained its existing large Plotly chunk warning.

## Claim boundary

This batch establishes governed preparation only. The catalog has six courses and preserves all 223 previously implemented interactive modules, while Vehicle Dynamics contains zero learner modules. The replay package is deterministic synthetic protocol evidence, not measured vehicle evidence.

MATLAB runtime comparison, browser/accessibility validation, learner validation, firmware execution, BLE-radio behavior, CAN electrical behavior, RaceChrono application behavior, bench testing, vehicle or track testing, physical HIL/hardware, safety certification, release, deployment, credentials/settings, and production validation were not performed.

A separate exact-baseline `ELP-VEHICLE-P01-P08` Portfolio Control contract must merge before any Vehicle Dynamics lesson implementation.
