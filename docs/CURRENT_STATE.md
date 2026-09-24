# Current state

`ELP-VEHICLE-P01-P08` is the authorized issue-467 first implementation batch from exact target baseline `7188d370b52dd9812634ae431fa652525d081634` (tree `3953708c5c04c18a53ede4adda021f0612874aba`) and Portfolio Control authorization `4f5f5078297df9713a97eb2459c6909aa6965f5b`.

Vehicle Dynamics implements P01-P08: path kinematics, force balance, longitudinal load transfer, friction-circle allocation, longitudinal and lateral tire slip, the linear bicycle model, and understeer/oversteer behavior. P01-P02 retain implemented-source comparison provenance; P03-P08 are Python-first native designs from reviewed scaffold identities. Coverage is eight converted and 16 pending, with zero blocked or placeholder items.

The catalog contains six courses, 231 modules, and 231 interactive experiments. P09-P16 is next and requires a separate exact-baseline authorization.

The replay data is synthetic protocol evidence, not a captured drive. It contains no VIN, driver identity, real location, precise route, or vehicle capture. MATLAB runtime comparison, browser/accessibility validation, learner validation, firmware or BLE-radio execution, bench/vehicle/track testing, physical HIL/hardware, safety certification, release, deployment, credentials/settings, and production validation remain explicitly unperformed.
