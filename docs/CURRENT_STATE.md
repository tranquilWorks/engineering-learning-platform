# Current state

`ELP-VEHICLE-PREP-00` is the issue-467 preparation batch from exact target baseline `8e5ff391f75f39218e51ed98aac8bcdb092550a0` (tree `bebb8579d33090a64201a7f2c8c4ad86595ada02`) and Portfolio Control contract revision `2fd02a1b72536ee6f4ff59357a74be7dc99c72c8`.

Vehicle Dynamics now has a platform-owned empty course shell, the byte-identical reviewed 67-module competency map, a 24-item source-conversion ledger, and deterministic synthetic GR86 CAN/RaceChrono BLE replay fixtures. The read-only source gitlink advances to `57264b3ffeb517ee5eb73e8957b9cd190d022457` (tree `d9e7267ba02c8d3d836c0ae481b80e91233eb81a`). P01 and P02 are recorded as implemented in that pinned source; P03-P24 remain source scaffolds. Coverage is 24 pending, zero converted, zero blocked, and zero placeholders.

The prep catalog contains six courses while preserving all 223 existing modules and interactive experiments. Vehicle Dynamics has zero learner modules. A separate exact-baseline Portfolio Control authorization is required before P01-P08 implementation begins.

The replay data is synthetic protocol evidence, not a captured drive. It contains no VIN, driver identity, real location, precise route, or vehicle capture. MATLAB runtime comparison, browser/accessibility validation, learner validation, firmware or BLE-radio execution, bench/vehicle/track testing, physical HIL/hardware, safety certification, release, deployment, credentials/settings, and production validation remain explicitly unperformed.
