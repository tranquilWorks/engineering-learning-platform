# DSP/Radar P41-P52 source-fidelity repair — 2026-09-27

## Authorization and immutable baseline

The owner requested the next batch after the PR #47 merge-and-continue question.
Target PR #47 merged as `f78831b23e46ff1cb9518a716ac8ba5aeab5a3ee`, tree
`ee7d2536b91b25b670dba34c222002e401fe6747`. Control PR #508 merged as
`47b907458622f3381bc93e5c19908a487c98774c`. The active batch is byte-identical
to the merged control artifact and repo-profile binds that revision.

Branch: `codex/dsp-fidelity-p41-p52-20260927`. This repairs twelve existing
lessons without expanding inventory. P01-P40, P53-P84, canonical source,
source-map/conversion-manifest, course identity, other courses, platform/UI,
schemas, dependencies and workflows remain unchanged. DSP source pin remains
`5d73667a486df4a7b6c581e4c9406e810ed4f0f6`, read-only and clean.

## Source-specific processing and learner evidence

| Item | Retained processing and comparisons | Failure and recovery |
| --- | --- | --- |
| P41 | Range-decaying separable AR(1) clutter plus white noise; correlations and distributions; steady/Swerling I-IV powers and 2000-trial integration; correlation/SNR controls | Global background threshold distorts range-wise Pfa; known-local-power normalization restores the model comparison |
| P42 | Explicit 48-sample LFM, moving targets and stationary clutter, 512×64 raw matrix; delay-corrected matched filter, normalized slow-time FFT, CPI/window sweeps | Fast-time FFT has frequency rows and pulse columns; restore the slow-time FFT and correct physical coordinates |
| P43 | One signed-amplitude threshold, 20000 separate H0/H1 trials, Gaussian probability curves, noise/pedestal sweeps, conditioned counts | Hidden true-RMS adaptation suppresses the intended fixed-threshold failure; restore native-amplitude threshold |
| P44 | Explicit signed 16-sample matched filter, 60000-trial H0/H1 banks, threshold/SNR ROCs, million-cell alarm budget, trial uncertainty | Cherry-picked lowest-score tuning bank reports zero alarms; restore predetermined threshold and full independent H0/H1 banks |
| P45 | Linear-power CA stencil, exact N=24 alpha, guarded CUT and omitted edges, slowly changing background and coherent point targets; Pfa/scale sweeps | Geometric mean from dB averaging lowers thresholds; restore arithmetic power mean |
| P46 | Sampled-sinc strong target, weak CUT, logistic background; guard leakage and training roughness/locality sweeps | Neighbor contaminates weak-CUT references without changing its power; larger guard excludes it on the same contaminated scene |
| P47 | 50000 paired CUT/independent-reference trials, N/Pfa sweeps, raw Pd and disclosed monotone inversion at Pd=.8, estimator spread | Known-noise multiplier gives an unfair apparent gain by overspending Pfa; restore finite-N calibration |
| P48 | Separately calibrated GO/SO probabilities, clutter-edge profile and 25000-trial contrast/one-side-contamination sweeps | Shared CA alpha and always-SO rule fail; calibrate each statistic and use GO for the protected edge comparison |
| P49 | Ascending rank statistic, product-form calibration, four interferers, 20000-trial count/strength/rank sweeps and N−k capacity | Rank 22 reuses rank-18 alpha; restore selected rank-specific calibration |
| P50 | 96×64 synthetic square-law map, exact rectangular-ring count, threshold/eligibility/decision maps, range/Doppler-width sweeps | Zero-filled missing references falsely admit border tests; restore complete-stencil eligibility, leaving the edge target untested |
| P51 | Combined edge/sidelobe/crowded/nonuniform scene; CA/GO/SO/OS statistics, misses, true H0 and response-artifact counts, disagreement causes; 12000-trial crowding | Shared CA alpha spoils equal nominal Pfa; restore all four statistic-specific scales |
| P52 | 200000 H0 trials in 2000-trial blocks, N/Pfa sweeps, running Wilson intervals, correlated/texture mismatch | Infinite-reference multiplier overspends Pfa; restore finite-N alpha and disclose model/finite-trial uncertainty |

Each lesson preserves its pinned source text and guiding question, then provides
physical labeled controls, prediction, two one-variable manipulations, source
parameters/equations, failure/recovery, focused checks and teach-back. All plots
have units and wired interpretation blocks. Shared helpers cover presentation
and explicit repeated CFAR primitives; complete lesson algorithms remain distinct.
Normalized-AST regression extends through P52.

## Independent numerical evidence

Each item has baseline, two one-variable sweeps, broken and recovery: sixty
expected/actual signatures with field units, input parameters, file hashes,
measured error extrema and `1e-8` absolute/scaled-relative limits. All sixty
passed; maximum absolute difference is `9.094947017729282e-13`.

Independent references never import production entrypoints or outputs. They use
SciPy IIR filtering for the AR field, direct DFTs and FFT convolution for the
range-Doppler chain, Gaussian survival functions, independent matched-score sums,
real-coordinate signal/noise powers, direct stencil summation, interpolation,
integration of min/max gamma densities with root solving for GO/SO, beta-function
OS calibration, summed-area rectangle subtraction for 2-D CFAR, and a quadratic
score-inequality solution for Wilson intervals. Common seeded input draws are
intentional; production calculations are not reference inputs.

The exact 90006-byte prior reference prefix is preserved, SHA-256
`639080c7d5ee1da82ee8753edf755d41b68631ba751622b55c074a33d84fc09d`.
Historical P29-P40 provenance now verifies its bound prefix rather than the
extended file hash; prior modules and fixtures remain untouched. Exact matches
are accepted via independent provenance and fresh replay; no expected value is
perturbed to manufacture inequality. Per-item provenance binds source,
production, reference byte count/hash, scenarios and signature units.

## Porting choices and limits

- NumPy private seeds 4101–5201 and row-major draws reproduce this port, not
  MATLAB random streams. Vectorized sums preserve stated equations; source
  console/figure housekeeping becomes web plots and metrics.
- P41 global-versus-local recovery assumes known local expected power; it is
  an oracle-background comparison, not a new estimated CFAR method. Probability
  histograms retain finite visible ranges. Target detection uses its own
  independent noise-only calibration bank.
- P42 shorter CPIs are prefixes of the same full noisy scene. Rounded delays,
  47-sample filter-delay removal, approaching-positive velocity and window-sum
  normalization are explicit. Wrong-axis output keeps its real coordinates.
- P43’s profile is the separate reference-background illustration. RMS and
  pedestal sweeps isolate their variables; combined control settings are valid.
- P44’s remaining bank after lowest-score selection is selection-biased; it is
  not described as independent validation. Recovery uses full H0/H1 banks and
  a predetermined threshold. Pd bars are approximate finite-binomial intervals.
- P46’s named contamination demonstration fixes T=12/G=4 and recovers at G=12;
  selected controls operate the uncontaminated scene. Recovery does not change
  the weak CUT’s observed power.
- P47 reports raw Pd and maximum monotone adjustment; loss is interpolated at
  Pd=.8 for a nonfluctuating complex target, not a universal radar loss formula.
- P48 baseline references intentionally contain only background to isolate edge
  probes. Profile targets add power; Monte Carlo weak targets add coherent
  amplitude. P49 recalibrates every rank and distinguishes strong-outlier
  capacity from general robustness.
- P50 is a synthetic power-map lesson, not a second waveform simulation.
  Missing border references are excluded from valid decisions; an untested
  target is distinguished from a miss. The iid alpha is illustrative under the
  nonuniform background, with no achieved-Pfa guarantee.
- P51 separates modeled response artifacts from true H0 crossings. Edge-zone
  noncenter sweep counts explicitly include artifacts. Detailed diagnostics
  retain CUT power, thresholds, decisions and the cause of each disagreement.
- P52 retains 200000 independent trials, 2000-trial blocks and N up to 64 in
  its reference-count sweep. Interactive selected N is bounded at 24 to retain
  the source random-work ceiling for mismatch trials. A common component makes
  samples within a trial correlated; trials remain independent. Texture is
  independently drawn per cell with log standard deviation .9 and unit mean.
- Full arrays drive calculations. Lines display at most 512 points and heatmaps
  at most 128 columns/64 rows, preserving zero coordinates and prominent peaks.
  No browser/accessibility, MATLAB execution, representative learner, hardware,
  certification, deployment or production validation is claimed.

## Verification

Required commands remain in `contracts/verification.yaml`. Control PR #508
passed `scripts/validate-control-plane.sh`: 252 root tests with one unrelated
GitG-source skip, six analog-camera, 33 ELP and 15 Tranquility tests, plus
schemas/inventory and shellcheck. Hosted control run 36346443093, job
108696410242, failed without executing any steps; the authorized normal merge
succeeded. Source-specific independent replay and scoped
lint pass. Broader focused, contract, quick/full, catalog, service and frontend
validation is in progress; this document does not yet assert those gates pass.

The first new-test run passed 89 checks and failed only the appended-section
separator assertion; the prior-prefix hash itself passed. That assertion now
matches the formatted new section. No physical tolerance or gate was weakened.
An initial combined DSP run passed **585 tests in 248.58 seconds**. Final
resource review then released completed Monte Carlo blocks and changed P47 to
column-wise score formation/comparison, reducing temporary allocation without
changing the model. Final replay and regressions follow those changes.
The final regressions include source binding, independent replay, all offered
control combinations, physical limits, calibration, edge eligibility, plot
wiring, finite bounded output and target-preserving heatmap coordinates.

Hosted source/history checkout limitations were present on PR #47; hosted CI
is not mandatory under retained owner direction. Local source/history gates
remain mandatory. Any new hosted results will be reported separately from local
validation; workflow changes remain outside this contract.

## Continuation and rollback

Ledger: one already-distinct, thirty-nine prior repairs, twelve current repairs,
thirty-two pending; total 84. Inventory remains six courses / 290 modules /
290 interactive. P53-P84 and whole-course numerical/curriculum/capstone maturity
remain blocked; issue 441 stays open. Next proposed group is P53-P64 after this
batch’s verification/merge and its own scoped contract. Prefer twelve at a time.

Rollback reverts this isolated batch to merged PR #47. No persisted learner-state
migration or deployment changes occur. Protected target merge requires separate
owner approval.
