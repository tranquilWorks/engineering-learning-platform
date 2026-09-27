# DSP/Radar P21-P28 fidelity repair — 2026-09-27

## Authorization and exact entry state

The owner approved merge of target PR #45 and continuing the plan. PR #45 merged
as `b7e684d595bd777602c9aa22cd489189efa6584b`, tree
`19a298703ab04794e855edffb8aa83a6f0e2ba83`. Reissued control PR #503 merged as
`12ea755ee75f9fe7bc142f052362938d9cefb4c9`. The active contract is byte-identical
to that merged control revision, and repo-profile.yaml records it.

Branch: `codex/dsp-fidelity-p21-p28-20260927`. Source pin remains
`5d73667a486df4a7b6c581e4c9406e810ed4f0f6`; source tree, source map,
conversion manifest, course identity, P01-P20, P29-P84, all other courses,
platform code, UI, schema, dependencies and workflow files are unchanged.

## Implemented learner behavior

| Item | Retained processing and visible evidence | Named failure and recovery |
| --- | --- | --- |
| P21 | 20 ksample/s conventional AM; single/multitone sidebands; signed/analytic envelopes; explicit mixer and 900 Hz lowpass; depth/frequency sweeps | 1.4 depth folds the magnitude envelope; coherent recovery preserves sign |
| P22 | Complex FM at 24 ksample/s; real RF/noisy spectrum; phase slope; Bessel-like line powers; measured 98% span versus Carson approximation | 8 kHz carrier plus 5 kHz deviation aliases; 30 ksample/s restores a 10.2 kHz occupied span and 1.9 kHz margin |
| P23 | 400 deterministic BPSK/QPSK symbols; bits, mapping, Es/Eb-consistent noise, IQ coordinates, sign decisions, BER; noise/phase sweeps | 55 degrees at 16 dB gives tight but wrong QPSK clusters; exact known inverse rotation restores decisions |
| P24 | 320 QPSK symbols, 8 samples/symbol, finite unit-energy RRC with singularity limits; rectangular comparison, convolution, matched delay, spectrum, eye and SER/EVM | Half-symbol timing corrupts decisions; aligned sampling restores the selected baseline |
| P25 | 480 pulse-shaped QPSK symbols; delayed complex paths, matched symbol response, eye, 31-tap finite ZF and regularized inverses, echo/lambda sweeps | [1,-0.999] creates a -60 dB null; lambda=0.01 lowers noise enhancement while residual distortion remains reported |
| P26 | Explicit 8-tap LMS on 6000 samples at 8 ksample/s; path changes at source sample 3001; 128-sample residual power, coefficients, reacquisition, spectra and correlation/step sweeps | Step 0.35 trips the finite guard; a zero-state replay at 0.006 restores stable cancellation and desired gain |
| P27 | 4000 independent 16-sample BPSK matched-filter trials; running BER, explicit 95% Wilson bounds, 100-trial block variability, count/SNR sweeps | Duplicating a lucky waveform gives false precision and an invalid independence flag; replaying the independent bank restores valid evidence |
| P28 | Separate 12000-trial H0/H1 banks; known 16-sample pulse; empirical/analytic ROC, all-trial amplitude bias/variance and CRLB over SNR | Detection-conditioned estimates acquire positive bias; restoring all H1 trials recovers the unbiased population |

All lessons preserve the pinned source lesson text and guiding question, then
add explicit control instructions, prediction, broken/recovery actions,
interpretation mistakes and teach-back. UI plots separate incompatible units.
Plot traces are bounded to 512 displayed samples; computation uses the complete
stated record. The generic platform controls and rendering are unchanged.

## Independent numerical evidence

Each item retains baseline, two one-variable sweeps, broken and recovery:
40 expected/actual pairs. Expected values are recomputed independently, never
imported from production or manufactured by perturbing production values.

Reference formulations include Fourier-series lowpass projection and analytic
signals (P21), Bessel powers and wrapped analytic phase differences (P22), real
coordinate decision algebra (P23), sinc-form pulses and FFT convolution (P24),
overlap-add propagation, inverse recurrence and augmented least squares (P25),
affine state-transition LMS updates (P26), projected noise and score-quadratic
Wilson roots (P27), and Gaussian sufficient statistics/tails (P28).

Each module's `evidence/provenance.json` binds the reference/production file
hashes, function, parameters and signature-field units. Conversion records bind
each retained expected/actual file hash, error extrema and tolerances. Both
absolute and scaled relative signature errors must be <= `1e-8`; largest
measured absolute difference is `1.7763568394002505e-13`. Existing P02-P20
reference source remains an exact byte prefix, and their modules/fixtures are
unchanged. Normalized-AST anti-template checks now extend through P28.

The scientific checks also assert limiting behavior and named failure mechanisms:
FM sweep bandwidths; pulse energy/symmetry and finite singularities; modulation
noise-energy scaling; deep-null distortion/noise tradeoff; desired-signal gain
and LMS reacquisition; independence validity and shrinking uncertainty; and
monotone ROC/variance with explicit estimator-population recovery.

## Porting choices and limitations

NumPy seeded streams are reproducible software inputs, not MATLAB RNG parity.
P25 uses a fixed 3920-sample noise bank for all channel cases, explicitly replacing
the MATLAB script's sequential noise draws. Its regularizer is the source's
finite least-squares penalty on path coefficients, not an exact colored-noise
Wiener-filter claim. RRC truncation is retained in the sampled pulse/channel
response. P23 recovery assumes a known carrier rotation; no acquisition loop
is implied. P26's guarded output ends at the stop point, with no fabricated tail;
reacquisition sentinel 3001 explicitly means not reacquired. P27 exposes nominal
Wilson limits as invalid for duplicated observations. P28 does not apply an
unbiased CRLB claim to the detection-selected population.

MATLAB figure-window cleanup/console output becomes bounded plots and metrics.
MATLAB execution, audio, browser/accessibility review, representative learner
validation, physical hardware/HIL, certification, release/deployment and
production validation were not performed. No course-level completion is claimed.

## Verification

Required local checks are in `contracts/verification.yaml`. Verified so far:

- Source-attested focused DSP suite: 405 passed.
- New P21-P28 suite: 60 passed, including 40 five-scenario comparisons.
- Contract wrapper: 72 passed.
- Scoped Python lint: passed.
- Deterministic catalog: 6 courses, 290 modules, 290 interactive, no errors.
- API smoke: eight module documents, 24 baseline/broken/recovery executions,
  exact recovery and eight stale-revision rejections passed using TestClient.
- Scope audit: only allowed paths; exactly eight coverage digest changes;
  source submodule clean; previous independent-reference source byte-identical.

The final quick/full results and exact-head review status are recorded below
when complete. The full wrapper includes `scripts/verify.sh`, generated-schema
validation, deterministic catalog, every API test, frontend typecheck and build.
Final label-only refinement clarifies selected FM and stable LMS reference
metrics during a broken demonstration; numerical values are unchanged.

A preliminary regression exposed YAML 1.1 parsing of JSON exponent notation:
`1e-08` was treated as text. Conversion records now serialize the same numeric
threshold as `1.0e-08`, preserving the gate. Existing lesson-title/check headings
were restored, and a smoke harness expectation was corrected to the API's existing
422 stale-revision response. No validator, scientific threshold or API behavior
was weakened to obtain a pass.

## Hosted CI and control state

Control PR #503 passed `validate-control-plane.sh` locally (252 root tests,
one unrelated GitG-source skip; 33 ELP, six analog-camera and 15 Tranquility
tests; schema/inventory checks and shellcheck). Hosted control run 36291560041
could not start because GitHub reported account billing/spending-limit trouble.
Normal authorized merge succeeded without an access-control bypass.

Target PR #45's final hosted run did execute: 723 tests passed; two source/history
checks failed because checkout lacked the DSP submodule and historical vehicle
commit `4b613a79bfe3cbd997e64e8372a58956533dae2c`. Frontend passed. That workflow
setup debt remains separate and outside this DSP contract. Required local checks
retain the source/history gates; hosted CI is not a completion requirement under
the retained owner policy. Target protected-branch merge still requires approval.

## Remaining work and rollback

Ledger: one already-distinct, nineteen prior repairs, eight current repairs,
fifty-six pending; total 84. Issue 441 remains open for P29-P84. Whole-course
numerical, curriculum and capstone stages remain blocked. The next source item
is P29 after this batch's verification and merge, under a newly scoped contract.

Rollback: revert this isolated batch to the merged numerical replay baseline.
No source data, platform migration, learner state or deployment changes occur.
