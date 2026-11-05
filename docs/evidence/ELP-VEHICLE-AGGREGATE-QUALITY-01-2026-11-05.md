# Vehicle Dynamics/Motorsport — content revised; broad verification blocked (2026-11-05)

The final remaining engineering course has 67 distinct checkpoints and 14 cumulative portfolios, preserving all 16 prior scoped assessment tasks. The review repairs load transfer, nonlinear stability, modal units, shift resistance and conditional covariance; actual desktop/mobile inspection also corrected clipped plot labels. Independent checks cover complete nonlinear state/covariance histories and both capstone ledgers.

Passing evidence: 335 runtime comparisons, 335 real HTTP comparisons, 134 current-content desktop/mobile views and interactions, 28 portfolio visits, 62 focused Vehicle tests, 13 web tests and23 browser regressions. Each runtime/HTTP replay includes ten complete-history comparisons. See [current evidence](../course-quality/vehicle-aggregate-verification-summary.json), [review plan](../course-quality/vehicle-aggregate-review-plan.md) and [actual captures](../course-quality/vehicle-aggregate-visuals/manifest.json).

Required broad verification remains blocked by three-second timeouts in unchanged DSP and Robotics lessons. An earlier contract run passed 103 tests; later attempts still failed, and the quiet quick run reached309 passes before DSP P52 timed out. Single-CPU affinity passed the targeted P52 test but did not resolve the subsequent contract failure. No timeout, sample count, tolerance, other-course payload or generic runtime was changed. Automatic approval review rejected a NumPy environment change as outside the content-only scope; installed NumPy remains 2.5.4.

[Target PR65](https://github.com/tranquilWorks/engineering-learning-platform/pull/65) and [Control PR636](https://github.com/tranquilWorks/portfolio-control/pull/636) remain drafts. Vehicle aggregate maturity is not promoted and neither PR is merged. Docker remains owner-deferred. Learner, manual screen-reader, MATLAB, measured vehicle, hardware and production validation remain not_run.


## Scope preservation and rollback

P01–16 numerical entrypoints and all P01–24 original lessons/verification records remain byte-identical. P17–24 add presentation wrappers only; stripping those wrappers produces the exact original numerical AST. All source pins, historical conversion artifacts and other course payloads are preserved. Revert this isolated revision to baseline9c27f567399cf2fcb9728fb104b2d573fcac5652 to roll back; no learner data migration exists.

Failed, stale-input and intermediate visual attempts remain archived separately. The accepted browser evidence reconciles the134-view base report with18 current rechecks. Eight selected real PNGs are bound to report and content hashes. No failed attempt is counted as a pass.
