# DSP/Radar P65-P76 source-fidelity repair — 2026-09-28

## Authorization and immutable baseline

The owner approved merging PR #49 and starting the next grouping. PR #49
merged as `e28b041aff3f4e66cec2190e04a5d689be23f260`, tree
`4b3ee5c371db2835920c4c3d8b04cd29dab2954b`. Control PR #519 merged as
`f808efb4c719b884e63c670d4e064e1855f7b5cb`; active-batch is byte-identical to
that contract and repo-profile pins it. Branch: `codex/dsp-fidelity-p65-p76-20260928`.

The twelve existing lessons are repaired without inventory expansion. Preserve
P01-P64, P77-P84, source, other courses, platform/UI, schemas, dependencies,
workflows, course identity, source-map and conversion manifest. Source pin:
`5d73667a486df4a7b6c581e4c9406e810ed4f0f6`, read-only and clean.

## Processing and learner evidence

| Item | Source-specific processing | Named failure/recovery |
| --- | --- | --- |
| P65 | Covariance, trace loading, distortionless MVDR, component SINR, nested snapshots and mismatched-look loading | Singular solve refusal; tiny loading and wrong look suppress desired signal; loading and look correction recover |
| P66 | Bartlett/MUSIC, Hermitian eigensplit, separated peaks, separation/SNR/snapshot/source-count sweeps | Coherent sources collapse rank; overlapping subarray smoothing restores rank with reduced aperture |
| P67 | Gain/phase/position/coupling manifold, noisy known-source calibration, transformed noise covariance, Bartlett/Capon/MUSIC | Dividing out raw response also removes source steering; remove nominal phase before calibration |
| P68 | Sensor-within-pulse vectors, moving clutter ridge, target-free covariance, fixed/separate/joint weights and output accounting | Contaminated training suppresses mismatched target; clean training restores joint response |
| P69 | Centered chirp, delayed echo, valid-overlap dechirp, Hann FFT and interpolated beat | Missing monostatic round-trip factor doubles range; correct conversion reuses beat |
| P70 | Fast-time range transform followed by coherent slow-time Doppler transform, signed axes and prefix sweeps | Magnitude before slow FFT destroys velocity; retained complex range data recover |
| P71 | Moving delayed echo, signed lag-one beat estimate, coupled range bias and independent velocity correction | Wrong correction sign doubles bias; correct sign reuses measurement |
| P72 | Opposite chirp legs, signed beats, physical two-equation solve, range/velocity/noise sweeps | Cross-target beat pairing creates ghosts; reviewed correct association recovers from unchanged peaks |
| P73 | TX+RX geometry, physical/virtual response, TDM timing, same-TX Doppler and slot compensation | Moving target phase biases angle; per-slot correction reuses noisy record |
| P74 | Integrated scatterer motion phase, Hann STFT, speed/carrier/window comparisons | Magnitude erases signed bulk Doppler; original complex IQ recovers |
| P75 | Slant range, delay, two-way phase, Gaussian fast-time ridge, aperture and cross-range sweeps, candidate-path coherent sum | Magnitude ridge lacks focusing phase; original complex ridge recovers |
| P76 | Zero-extended delayed chirps, per-row linear matched filter, energy normalization and corrected range axis, bandwidth/pair-spacing sweeps | Magnitude retains range ridges but loses aperture phase; original complex compressed record recovers |

Each lesson preserves its pinned source text and guiding question, and adds
physical controls, prediction, two independent manipulations, intermediate plots,
named failure/recovery, checks and teach-back. Full calculations precede display
decimation; plots carry units and interpretations. Essential algorithms remain
distinct; only input formulas and small presentation/math helpers are shared.

## Independent numerical evidence

Sixty expected/actual comparisons cover baseline, two sweeps, broken and recovery
for each lesson, with parameters, field units, source/production/reference hashes
and absolute/scaled-relative limits 1e-8. Initial full replay passed all sixty;
maximum absolute difference was `1.223725121235475e-09`.

References never import production code or outputs. Alternate formulations use
Cholesky constrained solves, SVD covariance subspaces, generalized Hermitian
noise-aware eigenspaces, permuted STAP channel order, sparse direct Fourier sums,
separable direct DFTs, expanded chirp phase, a physical linear-system solve and
chirp-z peak evaluation, covariance-domain TDM scans and analytic array sums,
SciPy STFT plus Parseval energy, scalar candidate-path sums, and direct matched
inner products/autocorrelation for SAR compression. Private input uniforms use
modular exponentiation independently of the production recurrence.

The exact prior reference prefix is 154384 bytes, SHA-256
`3e335831c25b63a7ef02dd6a6ced2e39b42deb2a57f2597252c02ffcd0ee5bb8`.
Prior fixtures and module bytes are preserved; only twelve coverage digests change.

## Porting choices and limits

- Private source input formulas use zero-offset Park–Miller uniforms. P65-P72
  split radius/phase blocks; P73-P76 interleave them. Input matrices preserve
  column-major ordering. No MATLAB runtime was executed.
- P65 finite sample covariance includes desired energy. The constraint protects
  the assumed look only. Loading is not a universal cure for manifold mismatch.
- P66 local-peak selection does not consult truth. Missing pairs receive a finite
  80-degree error penalty plus explicit peak count. Smoothing assumes a uniform
  array and coherent spatial stationarity; it reduces aperture.
- P67 receiver noise is added after the impaired manifold, as in the source.
  Equalization transforms its covariance. One-angle calibration does not identify
  an angle-independent inverse of coupling and element-position errors.
- P68 clutter and target models are idealized. Training and test-cell seeds are
  separate. Truth only supplies modeled output accounting. Removing contamination
  requires justified training selection, not an operational truth oracle.
- P69 zero-padding interpolates spectral peaks; physical resolution remains
  c/(2B). P70 is stop-and-hop and intentionally defers within-chirp coupling to
  P71. Its truth-defined neighborhoods audit peaks without forming transforms.
- P71 freezes delay within the chirp and uses independently supplied velocity.
  P72's separate two-target recovery requires correct beat association; reversing
  the reviewed down list is not a general multi-target association solver.
- P73 negative spatial and slow-time phase follows source mixer convention.
  Same-TX Doppler compensation assumes a single unaliased target Doppler. Its
  selected noisy record, noiseless pair-resolution scene and named moving-target
  failure are explicitly separate.
- P74 positive plotted Doppler means approaching; the negative FFT axis is
  reversed. STFT time labels are window centers. Carrier/speed comparisons retain
  their source seeds; window comparisons reuse the selected record. Spectrogram
  resolution depends on window duration, not just FFT length.
- P75 shorter-aperture controls crop a fixed full-aperture noise record, retaining
  the source baseline and isolating aperture changes. The coherent score uses a
  known range ridge and is not a full image former.
- P76 round-to-nearest integer delays have at most half-sample quantization.
  FFT convolution is explicitly zero-padded and checked against direct matched
  filtering; it preserves all 401 aperture rows and subtracts 239 delay samples.
  Pair spacing changes a separate equal-target example. No azimuth focusing claim.
- No browser/accessibility, representative learner, hardware/HIL, certification,
  deployment or production validation is claimed.

## Verification

Control validation passed: 252 root tests (one unrelated GitG-source skip), six
analog-camera tests, 33 ELP tests, 15 Tranquility tests, schemas/inventory and
shellcheck. Hosted control run 36371608371 job 108768970492 failed with zero executed
steps. No hosted pass claim.

Sixty independent comparisons passed. Initial runtime smoke found one NumPy
boolean serialization issue in a SAR diagnostic; it was converted to a native
boolean. The first new suite had 97 passes and two failures: YAML treated
1e-6 as text, fixed with explicit 1.0e-6 serialization; a new STAP assertion
incorrectly required 10 dB target attenuation, replaced by a half-power-loss check
alongside the retained source-required 10 dB SCNR loss. Scoped lint also identified
unused bindings, now corrected. Final fixtures and all required gates are being
rerun; no passing gate is inferred from these initial checks.

Verification runs serially with `OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
MKL_NUM_THREADS=1`. All tests, tolerances and three-second runtime limits remain
intact. Hosted CI is nonmandatory by retained owner direction; checkout-related
limitations remain separate from mandatory local evidence.

## Continuation and rollback

Ledger: one distinct, sixty-three prior repairs, twelve current repairs, eight pending,
total 84. Inventory stays six courses / 290 modules / 290 interactive. P77-P84 and
whole-course numerical/curriculum/capstone maturity remain blocked; issue 441
stays open. The final remainder is P77-P84 after this batch merges and a fresh
scoped contract is approved.

Rollback reverts this isolated batch to merged PR #49. No persisted learner-state
migration or deployment changes occur. Protected target merge requires separate
owner approval; current approval covered #49 and this batch's implementation.
