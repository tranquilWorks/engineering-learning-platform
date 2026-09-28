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
and absolute/scaled-relative limits 1e-8. Final full replay passed all sixty;
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
unused bindings, now corrected. The initial combined regression had 782 passes and one failure: the same 1e-6
serialization remained in the conversion sweep list. That record and its generator
are corrected; source-bound tests now verify JSON/YAML sweep-value agreement.
Final fixtures and all mandatory local gates passed for implementation
`24b721d3bb7b555411e24fcfe435f54151cc6512`:

- New suite: **99 passed in 57.45 seconds**, including all 248 control combinations.
- focused: **783 passed in 396.60s (0:06:36)**.
- contract: **72 passed in 84.45s (0:01:24)**.
- quick: **1163 passed, 3 warnings in 799.86s (0:13:19)**.
- full: **1163 passed, 3 warnings in 786.59s (0:13:06)**.
- Frontend typecheck/build and scoped lint passed. Existing Starlette/httpx and
  FastAPI ORJSON deprecations and the large Plotly chunk warning remain.
- Deterministic catalog passed: six courses / 290 modules / 290 interactive.
- API smoke passed twelve documents, 36 baseline/failure/recovery runs, twelve
  exact recoveries and twelve stale-revision rejections (422).
- Live TCP smoke passed health, catalog, HTML and twelve document/baseline runs.
- Scope audit passed 197 allowed paths, exactly twelve coverage digests, prior
  reference prefix, clean source pin and exact merged control contract.

[PR #50](https://github.com/tranquilWorks/engineering-learning-platform/pull/50) is ready for review.
The final follow-up commit changes only this evidence, CURRENT_STATE and HANDOFF.
Heavy suites are not repeated for those documentation-only changes.
Local preview: http://127.0.0.1:8765/courses/dsp-radar/modules/65-use-mvdr-capon-adaptive-beamforming

Hosted [run 36373961548](https://github.com/tranquilWorks/engineering-learning-platform/actions/runs/36373961548)
for implementation `24b721d3bb7b555411e24fcfe435f54151cc6512` completed with
frontend success and backend **58 failed, 1105 passed, 3 warnings in 792.21 seconds**.
All 58 failures were classified: 56 P21-P76 source-lesson reads and one P11-P20
source identity check lack the private DSP source checkout; one unchanged vehicle
framework test lacks historical Git object `4b613a79bfe3cbd997e64e8372a58956533dae2c`.
Hosted schema and deterministic catalog checks passed; backend lint was skipped
after the test failure. Hosted CI remains nonmandatory under retained owner
direction. Workflows and all tests remain unchanged except approved batch tests;
no hosted backend pass is claimed.

A subsequent combined run was interrupted after 186 passes and 75 setup errors
when unchanged P26 exceeded its three-second catalog timeout on the busy shared
host. Its isolated runs completed in 1.586, 1.470 and 1.496 seconds. A further run on cores 5 and 2 had 782 passes and one instance of the same P26
timeout. The successful focused run used less-contended cores 4, 5, 6 and 7.
The first quick run had 1162 passes and one timeout in unchanged robotics P58
(clearance 0.8 m). Isolated repeated timings were 1.551, 1.473 and 1.474 seconds.
A second quick run using normal scheduler load balancing also had 1162 passes and
one P58 timeout, this time its default during catalog validation. No CPU quota
throttling was present; default timings on cores 2, 3, 5 and 9 were 2.959, 2.529,
1.828 and 1.560 seconds. A third quick run on core 9 again timed out at robotics P58 with 1162 passes.
The full run then passed all 1163 tests plus frontend checks on core 9, followed
by the final quick check on the same setup. Numerical library threads remained bounded;
no runtime limit, test or numerical tolerance was relaxed.

Verification runs serially with `OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
MKL_NUM_THREADS=1`. All tests, tolerances and three-second runtime limits remain
intact. Hosted CI is nonmandatory by retained owner direction; checkout-related
limitations remain separate from mandatory local evidence.

Local run artifacts are retained in ignored `.state/`; SHA-256 binds the
recorded evidence without adding raw logs outside the approved Markdown path.

| Artifact | SHA-256 |
| --- | --- |
| `p65-quick-third-robotics-timeout.txt` | `e98f0a15f3da2dc6ec6348d6423c2449d92a6bf28d1ba8048ca785f78d136f31` |
| `p65-quick-second-robotics-timeout.txt` | `83a559e61cb6446b8848302f8c53af93c08969b5c710e1c804c57bb76417927a` |
| `p65-robotics58-default-timing.json` | `e47578e6537d01cde516c10a2e60d35a494d7fd246a157a71128f772d79e4c41` |
| `p65-quick-initial-robotics-timeout.txt` | `9691e7721b7769aa8cd9a10de6e1207fadb2e08dd634219340667904e7a03d54` |
| `p65-robotics58-timing.json` | `7ebcc864fa203efdd688a1888e69f9053f748fb0fbf15b51561321083773ce57` |
| `p65-focused-affinity-timeout.txt` | `702f9d6cf579bb42a7c0485f6cb654ab07a23b53e7cb8da68275d1a1c6611e6c` |
| `p65-focused-initial-catalog-timeout.txt` | `4c5e8151063a33ac1db270980a1e37acb9e31bdbb97956f8231895366d042b30` |
| `p65-verification-cpus.json` | `8ec7f48bc06f29ffb58b45c5c12b9c645f122d47991d832db9f2d43d52e52591` |
| `p65-p26-timing.json` | `93af558dd2fdbfe194b64dc4bb602d7890e7bcad30c5ec132e649e07f80f0fd0` |
| `p65-focused-initial-sweep-format.txt` | `739109f9ce77aac2d5012e88309375254f45545dab17d7fbb39e5a8f90e51183` |
| `p65-sweep-format-regression.txt` | `14046b7018951855bc7ade52584bdc36f9b1e885dd25cb31dd9cb64725a38be6` |
| `p65-new-tests-final.txt` | `63901fd3324438f03d20700f91e54a1d6fab7c73147659c21bb43f1233a5672a` |
| `p65-focused.txt` | `3dae002853a94a2eac9d7069d9c9dd48157aeeb14f6d7b7f9d039a0616f2af44` |
| `p65-contract.txt` | `7dcf5ced8cf3871977ffa477d707f147e9d96140dfcca654663df2ab3d7367a6` |
| `p65-quick.txt` | `650fa2b5b965b59dfbbb87a6d162701a7da92deb623b9d37d73a4edc405a0ffd` |
| `p65-full.txt` | `f7c77d3ca5594ea41587bae6b908da743abdb196c5d75980b0d52a4201ed1298` |
| `p65-lint.txt` | `82b3e6a6c090a57601d22943bd23fca9218d1031dbe5a7b754092f9a156b4f18` |
| `p65-catalog.json` | `e0ec19a3f9adf17cab941b6e63ba2fd0a89f5a0ca177b6997a4b612d0462e484` |
| `p65-scope.json` | `e6f437c5bd42f5162f32a6086f49890d3acd00a0abcba206a4154ccb642003a9` |
| `p65-http-smoke.json` | `0940a7aece30d48b2e9cec4febe4910cc5346307325d4d4c69cb03aefafbe21a` |
| `p65-live-preview.json` | `f1c85abf7945a951ac1c8066b0ba9a2a345fe4f656c059454d9465a5b7a3108d` |
| `p65-reference-summary.json` | `5350b6b7ff75e59d4393640bedd1e27d4a1a02c3baaf7ac78c859184080c6386` |
| `p65-hosted-failures.txt` | `7cd016944d96ec1262cdfe68e57e1987df6f9b35588dd1f258d73058a60826a9` |

## Continuation and rollback

Ledger: one distinct, sixty-three prior repairs, twelve current repairs, eight pending,
total 84. Inventory stays six courses / 290 modules / 290 interactive. P77-P84 and
whole-course numerical/curriculum/capstone maturity remain blocked; issue 441
stays open. The final remainder is P77-P84 after this batch merges and a fresh
scoped contract is approved.

Rollback reverts this isolated batch to merged PR #49. No persisted learner-state
migration or deployment changes occur. Protected target merge requires separate
owner approval; current approval covered #49 and this batch's implementation.
