# A-ID integration evidence

Integrate these existing lessons: P20, P33, P58, P59, P60, P66.

Required evidence: Use separated estimation and validation windows, report identifiability and uncertainty, and reject a misleading fit.

## Derive and predict

Use P20: Explain why speed diversity is needed to identify both rolling resistance and quadratic drag. Regress resistance against a constant column and v². If every speed is the same, those columns are dependent: many intercept/drag pairs fit the data. Separate estimation samples from held-out samples before solving. A rank-deficient branch returning a zero coefficient or standard-error placeholder has not established exact knowledge. Report rank and excitation alongside residuals, and predict why a wider speed span improves parameter separation. Connect this result to at least one other listed lesson, identifying the exact quantity, units and assumption transferred across their interface.

## Compare connected mechanisms

Use P58: Prove that later observations cannot change a fit computed only from the training prefix. With 80 samples and training fraction 0.65, the first 52 rows estimate two stiffnesses and 28 rows remain unused until validation. Solve the two-column least-squares problem on that prefix and retain its parameter vector before examining later residuals. Perturb only held-out force observations: training coefficients and training error must remain unchanged while validation error may change. The broken mode leaks all rows into fitting and substitutes training error for validation error. Connect this result to at least one other listed lesson, identifying the exact quantity, units and assumption transferred across their interface.

## Diagnose and recover

Use P60: Classify missing, duplicate, inverted and malformed records before deciding what can actually be recovered. Dropping sequence 37 and truncating 89 create two unusable expected records in the full fixture; a duplicate at 52 and inversion at 71/72 are different faults. Deduplicate and sort only valid records, and enforce the declared reordering window. Recovery means a valid ordered subset, not inventing the missing payloads. Compare record identities and payload lengths with the nominal fixture, then replay the same diagnosis after reset. Connect this result to at least one other listed lesson, identifying the exact quantity, units and assumption transferred across their interface.

## Integrate and defend the boundary

Use P66: Trace a telemetry requirement from exact bytes through synchronization, calibration, reconstruction and untouched validation. Establish CAN/BLE payload identity before decoding, then fit clock rate/offset from the three explicit synchronization pairs. Apply the separate speed gain/bias calibration and yaw-bias correction before trajectory reconstruction. The force channel is synthetic 1450*a+0.45*v²+2*sin(0.9*i), not a claim about the fixture's IMU channel. Freeze the chronological fitting prefix before computing held-out residuals. For every passing requirement, identify its actual residual or event evidence and reproduce the injected fault and deterministic recovery. Connect this result to at least one other listed lesson, identifying the exact quantity, units and assumption transferred across their interface.

## Required integration artifact

Submit a reproducible split manifest, design matrix, excitation/rank evidence, parameter estimates, residual history and conditional uncertainty calculation. Freeze the fit before touching held-out rows; perturb only those rows and demonstrate unchanged training parameters. Compare singular values under excitation scaling, residual lag correlation and unused-point error. Distinguish a two-parameter truth-containment count from repeated-trial interval coverage, and a rank-deficient zero placeholder from zero uncertainty. Include a rejected apparently good fit and state which independent evidence caused rejection.

## Four-criterion rubric

1. Governing reasoning: equations, units and frame/sign conventions justify a numerical prediction; naming an algorithm alone earns no evidence.
2. Controlled comparison: two isolated sweeps and at least one limiting case distinguish mechanisms and make a falsifiable claim.
3. Diagnose and recover: identify the first failing assumption from actual outputs, restore it and demonstrate deterministic recovery.
4. Integration and scope: show the value passed between stages, an independently checked result, and a limitation that prevents a broader claim.

Retain inputs, selected outputs and your explanation as a cumulative artifact. No learner completion, automatic score, physical qualification or production acceptance is recorded.
