# DSP/Radar P53-P64 source-fidelity repair — 2026-09-27

## Authorization and immutable baseline

The owner explicitly approved merging PR #48 and the next twelve-lesson chunk.
PR #48 merged as `255427e3b3c6a31a66b74ad7f9836dad09b164e5`, tree
`3958e73ecf1914e4d2b5dee4a919c6b7275434f2`. Control PR #515 merged as
`549fd5867f2cd3b759a2af76e2a0be0350b8ee3c`; the active contract is byte-identical
to the merged control artifact and repo-profile binds that revision.

Branch: `codex/dsp-fidelity-p53-p64-20260927`. The batch began September 27;
verification completed September 28 UTC. It repairs twelve existing lessons,
without increasing inventory. P01-P52, P65-P84, other courses, platform/UI,
schemas, dependencies, workflows, course identity, source-map and conversion
manifest remain unchanged. Source pin remains
`5d73667a486df4a7b6c581e4c9406e810ed4f0f6`, read-only and clean.

## Source-specific processing and learner evidence

| Item | Retained processing | Failure and recovery |
| --- | --- | --- |
| P53 | 72×65 score scene, local plateau peaks, 8-connected groups, size filtering, excess-power weighted reports, extents/effective counts/shape proxies; size and exponent sweeps | Peak-only reporting promotes nuisance maxima; grouping and filtering recover physical reports |
| P54 | 81 one-second scans, explicit position/velocity prediction, innovation and alpha-beta correction, six missing-report coast scans, gain sweeps | Beta zero never learns initially unknown velocity; positive beta restores learning |
| P55 | 101-scan CV state, interval-acceleration Q and report R, gain, Joseph covariance, position/velocity uncertainty and NIS; separate Q/R sweeps | Zero Q over-trusts motion; underestimated R over-trusts reports; restore assumptions on the same data |
| P56 | Cartesian CV plus nonlinear range/bearing h and Jacobian, wrapped innovation, Joseph update, covariance ellipses, normalized residuals, bearing/R-geometry sweeps | Unwrapped branch-cut subtraction causes a spurious correction; wrap the angular residual |
| P57 | Three predicted tracks, six shuffled reports, covariance-specific Mahalanobis distances, gating, global greedy one-to-one assignment; gate/covariance sweeps | Ungated Euclidean distance selects clutter; covariance-aware gating recovers |
| P58 | Thirty scans, stable IDs, prediction/association/birth, M-of-N confirmation, coasting/deletion histories and reason events; M/coast sweeps | Immediate confirmation and effectively immortal tracks retain eight false tracks; managed policy recovers |
| P59 | Alternating report order, crossing geometry, normalized position/velocity costs, identity audit and 200 paired trials for noise/interval/separation | Independent row minima reuse one report on twelve baseline scans; row-and-column removal plus velocity evidence recover |
| P60 | Six-state CV/CA IMM, transition/mixing probabilities, mean-spread covariance, Joseph updates, log likelihoods and blended state/covariance; strength/persistence sweeps | Zero support makes maneuver mode unreachable; nonzero prior/transition support recovers |
| P61 | Geometry/time advance, complex sensor samples, wrapped/unwrapped phase, least-squares/adjacent phase inference; angle/spacing/frequency comparisons | One-wavelength direction-cosine aliases are indistinguishable; half-wavelength spacing recovers |
| P62 | Full 7201-angle coherent sum, interpolated HPBW, first nulls/sidelobes, aperture/spacing/Hamming comparisons, four seeded off-grid probes and element phasors | Steering +30 degrees at one wavelength creates an equal -30-degree grating lobe; half-wavelength spacing removes it |
| P63 | Source/sensor matrix, conjugate-normalized DAS, mean output power, alignment view; separation/aperture/SNR/snapshot comparisons | Wrong steering sign mirrors the named source scene; correct conjugation recovers |
| P64 | Phase-aligned squinted beams, sum/difference ratio, local monotone interpolation, sum guard/valid/clipped counts, squint/SNR sweeps | Right gain 1.12 biases noiseless boresight; measured inverse-gain correction recovers |

Every lesson preserves its pinned source text and guiding question, then adds
physical controls, prediction, two one-variable manipulations, explicit parameters
and equations, named failure/recovery, focused checks and teach-back. Plot axes
carry units and interpretation blocks are wired to the runtime. Shared helpers
cover presentation, explicitly specified input generators and repeated greedy
assignment; complete lesson algorithms remain distinct. Normalized-AST checks
extend through P64.

## Independent numerical evidence

Each lesson retains baseline, two sweeps, broken and recovery signatures: sixty
expected/actual comparisons with field units, parameters, source/production/
reference hashes, error extrema and 1e-8 absolute/scaled-relative limits.
The final replay passed all sixty; maximum absolute difference was
`2.0804691303055733e-11`. Expected values are never production imports, output
copies or perturbed production values. Exact equality is valid where independently
formulated computations agree.

References use connected-component labeling and image moments, a sparse batch
solve of alpha-beta recursion, covariance subtraction rather than Joseph form,
a reordered EKF state with Cholesky solves, whitened diagonal residuals and
sorted admissible edges, an object/event lifecycle, scalar crossing-trial
association, total-second-moment IMM mixing, polynomial phase fitting, analytic
finite geometric array sums, covariance-domain Bartlett power, and centered-array
monopulse patterns with scalar channel sums. Input sequences are shared by
specification, not executable imports. Physical tests additionally check topology,
coasting, Jacobians, covariance, one-to-one assignment, truth isolation, mode
support, phase signs, aliases, normalization, calibration guards and clipping.

The exact prior reference prefix is 118814 bytes, SHA-256
`eee1c963fa051806d29581553be723bc8580ccbccdd1b7f00ea8492a776fac5c`.
Earlier reference source and fixtures remain unchanged; historical provenance
continues to bind its original prefix. Only twelve coverage digests change.

## Porting choices and limits

- P53-P56 preserve equations and seeds using private NumPy row-major draws;
  their random streams are not MATLAB streams. P57-P64 retain source private
  Park-Miller/Box-Muller formulas and ordering, including P58's zero uniform
  offset and the array complex-noise convention. P62's seed controls only its
  four off-grid probes. No MATLAB runtime was executed.
- P53's uncertainty values are uncalibrated morphology proxies, not measurement
  covariance R. Truth audits report-component survival only. Plateau selection
  retains one row-major representative, including extended equal plateaus.
- P54 drops unavailable reports rather than inventing measurements. P55/P56
  exclude fifteen warmup scans from aggregate errors; P54 excludes ten.
  Mixed-state covariance eigenvalues are numerical PSD diagnostics, not a
  physical uncertainty with a single unit.
- P56 bearing-R sweeps retain the reviewed initial covariance. Its range control
  changes the separate ray-geometry uncertainty demonstration, not target truth.
  The 25 m Jacobian singularity guard remains. A single NIS trace cannot establish
  ensemble consistency or a field tracking guarantee.
- P57 covariance scaling changes predicted covariance only, preserving report R.
  Greedy assignment is not an optimal global solver. P58 counts the birth hit,
  deletes tentative tracks that fail their age-N window, and deletes confirmed
  tracks only when consecutive misses exceed the coast budget. IDs are not reused.
- P59 begins with known separated pre-crossing states as specified by the source;
  subsequent truth cannot influence association. Cartesian velocity reports are
  idealized extra evidence. The 200 paired seeds are 5901–6100; vectorizing trials
  preserves the source sequence, alternating report order and column-major tie
  order. Finite trial frequencies are not operational failure probabilities.
- P60 mixes covariance including between-model mean spread, uses log-domain
  weights and retains zero support in the broken mode. The fixed CV comparison
  and the IMM use identical position reports.
- P61's named alias is noiseless and fixes direction cosines .6/-.4 at one
  wavelength; it is distinct from the selected noisy scene. The frequency
  comparison shows ideal electrical equivalence at fixed physical spacing.
- P62's Hamming comparison explicitly fixes the reviewed M=8, half-wavelength
  geometry; selected controls affect uniform-array and aperture/spacing plots.
  Full-grid calculations drive metrics; display decimation preserves zero,
  prominent peaks and endpoints. Source figure/console layout becomes native plots.
- P63 input SNR is per-source, per-sensor. Its named sign failure uses seed 6315
  and sources -20/+30 degrees; the regular scene uses -20/+25. A separate seeded
  0 dB record supplies snapshot prefixes. Background masks exclude neighborhoods
  of the relevant scan peaks; ripple uses sample standard deviation. Fixed phase
  steering assumes narrowband data.
- P64's named mismatch is a noiseless boresight scene, separate from the selected
  noisy 2-degree target. Calibration is local to +/-4 degrees; estimates clip to
  endpoints and report clipping/validity counts. The coherent ratio is
  Re(mean Delta / mean Sigma), not mean of snapshot ratios. Sum guard is .15.
- No browser/accessibility, representative learner, hardware/HIL, certification,
  deployment or production validation is claimed.

## Verification

Control PR #515 passed the full control-plane validator: 252 root tests with one
unrelated GitG-source skip, six analog-camera, 33 ELP and 15 Tranquility tests,
plus schemas/inventory and shellcheck. Final portfolio validation passed after
clarifying P59's named report-reuse failure. Hosted control run 36359159348,
job 108732735610, failed without executing any steps; the authorized normal
merge succeeded. No hosted validation pass is claimed.

The initial new DSP suite passed **99 tests in 37.07 seconds**. Direct checks
covered 240 offered control combinations with finite output under 1 MB; the
slowest pre-polish run was approximately .21 seconds. Scoped lint passed.
Final presentation review added P53 velocity-centroid evidence, P55 velocity
uncertainty, P56 normalized innovations, P62 source probes/element phasors and
P63 sensor data. The preliminary combined run was deliberately interrupted for
these additions. Final references, fixtures and mandatory local gates passed for implementation
`a70eaf9ec22d5229a8f2a26b071083d411b4ced6`:

- focused: **684 passed in 324.13s (0:05:24)**.
- contract: **72 passed in 72.57s (0:01:12)**.
- quick: **1064 passed, 3 warnings in 899.08s (0:14:59)**.
- full: **1064 passed, 3 warnings in 810.89s (0:13:30)**.
- Frontend typecheck/build and scoped lint passed. Existing Starlette/httpx and
  FastAPI ORJSON deprecations and the large Plotly chunk warning remain.
- Deterministic catalog passed: six courses / 290 modules / 290 interactive.
- API smoke passed twelve documents, 36 baseline/failure/recovery runs, twelve
  exact recoveries and twelve stale-revision rejections (422).
- Live TCP smoke passed health, catalog, HTML and twelve document/baseline runs.
- Scope audit passed 196 allowed paths, exactly twelve coverage digests, prior
  reference prefix, clean source pin and exact merged control contract.

[PR #49](https://github.com/tranquilWorks/engineering-learning-platform/pull/49) is ready for review.
The final follow-up commit changes only this evidence, CURRENT_STATE and HANDOFF.
Heavy suites are not repeated for those documentation-only changes.
Local preview: http://127.0.0.1:8765/courses/dsp-radar/modules/53-group-detection-cells-into-target-reports

Hosted [quality run 36361268320](https://github.com/tranquilWorks/engineering-learning-platform/actions/runs/36361268320) for implementation `a70eaf9ec22d5229a8f2a26b071083d411b4ced6` passed frontend, generated-schema and deterministic-catalog steps. Backend finished with **46 failed, 1018 passed, 3 warnings in 394.77 seconds**: 45 source-attestation checks lack the canonical DSP checkout, and one historical-contract check lacks Git object `4b613a79bfe3cbd997e64e8372a58956533dae2c`. Static Python checks and container were skipped. These checks pass in the complete local checkout; hosted CI is nonmandatory under retained owner direction, and its checkout prerequisites remain outside this batch. No hosted backend or container pass is claimed.

Verification runs serially with `OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
MKL_NUM_THREADS=1`, using the existing local toolchain and preserving all tests,
numerical tolerances and three-second runtime limits. Hosted CI is nonmandatory
under retained owner direction. Missing hosted source/history prerequisites are
outside this DSP contract and will be reported separately from local evidence.

Local run artifacts are retained in ignored `.state/`; SHA-256 binds the
recorded evidence without adding raw logs outside the approved Markdown path.

| Artifact | SHA-256 |
| --- | --- |
| `p53-focused.txt` | `2dc016132e5f592e2a30520595f7201b1ecad1e03dfd95698f4adfa1d2d9481f` |
| `p53-contract.txt` | `dd6bb89add63d284d6fc403f3bbd06a023d6d949eab67d271d6062602825c477` |
| `p53-quick.txt` | `e165dfcc62ec8eca3cd5b91aa53c891c10323abce3fae825406e9eca353e0c70` |
| `p53-full.txt` | `d1ac7b0e7f3f3dd052514b0bfe048032dfaaeefb348e17e9f3aae37507d8a58b` |
| `p53-lint.txt` | `82b3e6a6c090a57601d22943bd23fca9218d1031dbe5a7b754092f9a156b4f18` |
| `p53-catalog.json` | `e0ec19a3f9adf17cab941b6e63ba2fd0a89f5a0ca177b6997a4b612d0462e484` |
| `p53-scope.json` | `3d1852ae6da6727ee6b333476391834e13c3b82ef5aa64be203e9b63e7747220` |
| `p53-http-smoke.json` | `59d24960a780c94226bbd3646955857f378279dd493ccbe52b9c869ddaff66ab` |
| `p53-live-preview.json` | `ee66e8865ae77d76dbe6545e375dd2cd650a444ad2ffede03a52f38e66d85015` |
| `p53-reference-summary.json` | `dfe21251821a2fbd919ee563e7bceff4058ca32170a539f5c65ea3ece3b0b510` |
| `p53-hosted-failures.txt` | `4ff0934d4fe91eac130b3bd58dfd85f87e30ad291f0239c81598c1f11f1437dc` |

## Continuation and rollback

Ledger: one distinct, fifty-one prior repairs, twelve current repairs, twenty
pending; total 84. Inventory remains six courses / 290 modules / 290 interactive.
P65-P84 and whole-course numerical/curriculum/capstone maturity remain blocked;
issue 441 stays open. Next proposed group is P65-P76 after this batch merges
and a fresh scoped contract is approved. Prefer twelve lessons per group.

Rollback reverts this isolated batch to merged PR #48. No persisted learner-state
migration or deployment changes occur. Protected target merge requires separate
owner approval; current approval covered PR #48 and this batch's implementation.
