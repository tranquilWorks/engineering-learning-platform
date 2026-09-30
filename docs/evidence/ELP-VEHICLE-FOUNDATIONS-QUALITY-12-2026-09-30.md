# Verified Vehicle foundations revision — 2026-09-30

Vehicle P01–P12 now have corrected physical models and dimensioned plots, twelve substantial individual lessons and twelve browser-embedded Course checkpoints. This completes the first group of the owner-authorized twelve-plus-four Vehicle revision under ELP-VEHICLE-FOUNDATIONS-QUALITY-12. The exact baseline is target PR58 merge `607c716993be14e7b782897ab054a7f8478f5dc0`; control contract PR580 merged at `604c55bfa992cbdb6884f8257cb052cf4b1c7714` before activation. The development PR records integration; Portfolio Control closeout binds the final merge SHA.

Sixty independent local and sixty baked HTTP full-mechanism comparisons passed at 1e-10 absolute/relative tolerance. The 138 expanded regression tests include all 96 Vehicle runtime corners under the unchanged three-second limit, direct physical identities and preserved Robotics checks. Twenty-six closure regressions and three active-contract binding tests also passed. Final delivery passed 290 HTTP modules, 580 desktop/mobile pages, 280 checkpoint checks, twenty cumulative DSP checks, 166 real control/fault/recovery/reset sequences, 168 screenshots, 64 SVG text/legend layout checks and all 290 host/baked content identities. Twenty-two focused browser tests passed, and fifteen plot captures were visually inspected. Mandatory gates passed sequentially (contract: 103 tests in 104.59 seconds; quick: 1583 tests in 1659.85 seconds; full: 1583 tests in 1601.97 seconds). See [batch evidence](ELP-VEHICLE-FOUNDATIONS-QUALITY-12-2026-09-30.md) and [exact verification summary](../course-quality/vehicle-foundations-verification-summary.json).

**Four named findings remain: Controls 0, Robotics 0, Vehicle 4 (P13–P16).** All three non-DSP aggregate numerical, curriculum and capstone reassessments remain blocked; zero named findings does not establish aggregate acceptance. DSP retains its separate authored/software aggregate disposition. Complete this group's normal verified development merge and Portfolio Control closeout, then continue the already-authorized final four against a fresh exact-baseline contract. Inventory remains 288 engineering lessons plus two examples, with nine pinned source-only repositories.

Verified read-only nonroot development preview: `http://127.0.0.1:8776`; image `sha256:d844a5f9ed5ac979dda6e361a713caaa54aea3780210cfc5d8d47c6683b73d18`. Earlier final previews remain preserved. Hosted CI is separately reported and nonmandatory under owner direction; required local gates passed. Representative learners, manual screen-reader, MATLAB, measured vehicle, hardware, concurrent capacity and production validation remain unperformed.

## Models and independent formulations

- P01: Constant-Curvature Paths and Tire-Grip Demand. Trigonometric curvature and independent sinc/half-angle path integration.
- P02: Balance Traction, Road Loads and Acceleration. Signed force vector sum and Newton balance.
- P03: Balance Longitudinal Load Transfer. Two-by-two reaction and moment balance.
- P04: Project a Force Request onto the Friction Circle. Polar angle and norm projection.
- P05: Relate Signed Slip Ratio to Tire Force. Logistic evaluation of signed tire saturation.
- P06: Relate Slip-Angle Convention to Lateral Force. Logistic evaluation with opposite slip convention and degree conversion.
- P07: Solve and Check Steady Bicycle Equilibrium. Force/moment shares before tire compatibility; factorized historical fault matrix.
- P08: Interpret Understeer and Critical-Speed Boundaries. Static axle weights divided by stiffness; critical boundary and stable mask.
- P09: Derive Wheel Rate from Suspension Motion Ratio. Unit-displacement virtual work.
- P10: Observe a Second-Order Suspension Transient. Independent state-transition matrix exponential and eigenvalues.
- P11: Close the Roll-Moment and Axle-Transfer Balance. One-equation roll solve with physical axle moments.
- P12: Estimate Camber Thrust and Toe Scrub. Independent sine/cosine toe ratio and dimensional angle conversion.

## Evidence and claim boundaries

Retained expected arrays come from separate geometric, balance, virtual-work and state-transition formulations that neither import production nor consume production output. Actual arrays come from the live experiment. All comparisons retain 1e-10 absolute and relative tolerance and the three-second runtime limit. Five cases per lesson supplement 96 runtime corners and direct independent identities, including zero excitation, critical/neutral boundaries, energy flow, force capacity and signed conventions.

The former P07 default solution violated lateral force balance by about −59312.35 N and yaw-moment balance by +17136.73 N·m. A separate test executes the historical model and verifies the defect; the repaired nominal model closes both equations and distinguishes small-angle validity. The declared fault reproduces the incorrect speed factors for diagnosis. P10 now renders the actual ODE response across underdamped, critical, overdamped and negative-damping regimes, checked by matrix exponentials.

Unselected module bytes, P13–P24 reference definitions and outputs, source pins, competency graph, runtime limits and historical conversion records are preserved. P01/P02 retain source-derived nominal relations; their new executed faults are native revisions, not unchanged source equivalence. Earlier Robotics scope guards now prove their exact historical PR57-to-PR58 change while preserving all live physics tests.

Exploratory reference comparisons caught an arithmetic typo in the historical P07 fault reference, corrected before retention. Neutral K and repeated-pole roundoff handling are explicitly bounded and tested. No tolerance was relaxed. Automated Chromium and visual plot inspection do not substitute for representative learners or manual screen-reader acceptance.

Rollback is a normal revert of this isolated group followed by rebuilding the previous image. No persisted-data/schema migration or production deployment is involved. Hosted CI and account limits remain separately reported; required local gates are mandatory. The already-authorized final four lessons follow only after verified merge and a fresh exact-baseline contract.

## Final verification identity

All 129 frozen implementation, test, contract and status inputs remained unchanged during the final verification pipeline. The committed summary records their hashes, the exact image and gate-log hashes. The selected visual captures are bound to matching module content digests, so the inspected numerical/teaching payload is the same payload verified in the final image. The selected preflight image has been retired; the final preview remains available.

The final run passed every required local gate in order: contract: 103 tests in 104.59 seconds; quick: 1583 tests in 1659.85 seconds; full: 1583 tests in 1601.97 seconds. Final browser counts differ between interactions (166) and screenshots (168) because P01 was already a representative first-module interaction before this group. All twelve selected lessons nevertheless have both desktop and mobile fault/recovery/reset evidence. Synthetic checks are not representative-learner or physical acceptance.

## Development integration and rollback

Standing owner authorization permits the normal exact-head development merge after technical gates and review checks. Preserve the exact reviewed tree when merging, then reconcile Portfolio Control and activate P13–P16 only through a new exact-baseline contract. Reverting this isolated group and rebuilding the prior image restores the predecessor; no persisted-data or schema migration is required.

Hosted CI remains separate. Control contract PR580's hosted job did not start because GitHub reported an account payment/spending restriction. Historical source-checkout and Git-history failures in prior target hosted runs remain retained, without weakening any local gate or changing workflows, branch protections or account settings. This target PR's actual hosted state is recorded separately before merge.

## Confirmed predecessor hosted outcome

PR58 hosted frontend passed, backend failed and container was skipped. Its retained backend job log reports 84 failed, 1436 passed, 14 errors and three warnings in 624.11 seconds, including absent pinned source files and historical Git objects. This remains separate from PR58's required local 1534-test quick/full passes and complete baked browser/container verification. No hosted result is inferred from local success.

## Reachable controls and instruction verification

Review caught that the stepped P08 sliders cannot generally select the exact neutral-steer ratio, and the P10 damping slider cannot select the exact repeated-pole value. Their lessons and checkpoints now distinguish reachable nearby settings from exact algebraic boundary cases. Controls, models, references and tolerances were preserved. Twelve retained-content regression cases and all 24 selected baked pages passed after the correction; refreshed plot captures and baked checkpoint text were checked. The initial incomplete final browser run was intentionally stopped, and the full delivery plus mandatory sequential gates were rerun from newly frozen inputs. No partial browser run is counted as final acceptance.
