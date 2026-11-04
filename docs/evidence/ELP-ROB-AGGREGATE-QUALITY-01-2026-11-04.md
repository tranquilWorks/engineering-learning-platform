# Robotics/Autonomy — authored/software aggregate accepted (2026-11-04)

All 69 existing Robotics lessons now have distinct formative checkpoints and 13 cumulative portfolios; 25 prior evidence tasks are preserved verbatim. The review closes all nine course-caliber dimensions within the documented synthetic scope. Joint pose/map SLAM, actual one-to-one association, holdout-safe smoothing, bounded planning failure, measured timing recovery, tracked mobile navigation and guarded object placement have independently checked mechanisms.

Verification passed: 103 contract tests, 1733 quick tests, 1733 full tests; 345 independently calculated runtime cases and 345 real HTTP replays; 138 current-content desktop/mobile views and interactions, 26 portfolio visits, 13 web tests and 23 browser regressions. Four integrated plot views were rechecked on both viewports after visual corrections. See [review](../course-quality/robotics-aggregate-review.json), [exact evidence](../course-quality/robotics-aggregate-verification-summary.json) and [batch closeout](ELP-ROB-AGGREGATE-QUALITY-01-2026-11-04.md).

Implementation: [PR64](https://github.com/tranquilWorks/engineering-learning-platform/pull/64). Contract: [Control PR635](https://github.com/tranquilWorks/portfolio-control/pull/635). Source pins, original conversion artifacts and all other course content are preserved. DSP/Controls dispositions remain accepted; Vehicle aggregate remains blocked. Docker delivery is explicitly owner-deferred. Learner, manual screen-reader, MATLAB, hardware and production validation remain not_run.

Historical closeout notes below retain their original dates; the current machine-readable disposition is `course-caliber-status.yaml`.

## Scope and repaired mechanisms

The original 69-lesson inventory and thirteen source pins are unchanged. The original Robotics conversion manifest and verification schema retain their checksums; historical records are validated against that schema, while current referenced assessment inputs use a separate compatible assessment-verification schema. Only target identities changed in P01–P24 verification records; original experiment, lesson and source provenance remain intact.

P49 declares physical state scales for dimensionless information metrics. P50 adds one-to-one matching with independent enumeration. P51 jointly estimates headings and unknown landmarks, with gauge and Jacobian checks. P53 excludes its initialization sample from held-out evidence and compares RTS posteriors with independent batch QR. P59/P64 return bounded planning failures. P60 checks interpolated between-sample separation. P67 derives hold/recovery duration from executed events. P62/P69 execute actual arm and carried-object states with an independent Jacobian/DOP853 reference. P68 connects occupancy, KF, route and bounded-acceleration tracking, checking covariance and continuous clearance independently.

## Failed attempts and repairs

The first arm comparison exposed RK4 saturation-crossing error; eight substeps repaired it without widening tolerance. A table-envelope schema error was corrected before catalog acceptance. Initial browser review caught replacement of 25 prior tasks and duplicate portfolio headings; the tasks were restored verbatim and headings disambiguated. Visual review caught clipped plot titles and misleading connected landmark points; all four affected lessons were rechecked on desktop/mobile and current input digests reconciled.

The exploratory broad run recorded 12 failures, 1698 passes and 12 errors while editing continued. Reload-required errors came from changing accepted catalog inputs during that exploratory run. Remaining failures exposed historical active-contract, assessment-count, conversion-era and manifest assumptions. Their repairs preserve original DSP/source-prefix and numerical assertions, validate immutable historical Robotics conversions separately from current assessment inputs, and add current manifest/control/block preservation. The final required gates ran sequentially with lesson inputs frozen.

Playwright's primary download returned a Site Unavailable HTML document. Its compatible Microsoft fallback installed Chromium 141.0.7390.37; all accepted browser evidence records that version. The Docker command returned exit 2 because its CLI/daemon is unavailable; that is recorded as deferred/not_run, never as a host substitute or pass.

## Publication and rollback

Owner authorization covers scoped content completion, push and merge after verification. No workflow or branch protection was changed. Hosted CI remains separately reported and nonmandatory under the retained owner direction. Revert the isolated Robotics revision to PR63 to roll back; there is no learner-data migration, source-repository change, hardware action or production deployment.

## Final record checks

After the frozen-input gates passed, 21 acceptance/status tests passed, along with focused lint and evidence integrity checks. Retained text logs strip trailing whitespace only; the verification summary records separate raw and retained hashes. Sixteen reviewed desktop/mobile integration plots are retained in `../course-quality/robotics-aggregate-visuals/`.
