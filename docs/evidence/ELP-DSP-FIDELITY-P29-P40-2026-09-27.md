# DSP/Radar P29-P40 source-fidelity repair — 2026-09-27

## Authorization and baseline

The owner approved merge of target PR #46 and requested twelve lessons per batch.
PR #46 merged as `74fbe13828665783a97d047eae0c6dc6ef482745`, tree
`2ac9ed6889e18f531b6d01dba794b710a2f51996`. Control PR #505 merged as
`a4b075fe1e4fdb35d58802668d2631b9f465eba3`. The active contract is byte-identical
to that merged control artifact; repo-profile.yaml binds its revision.

Work branch: `codex/dsp-fidelity-p29-p40-20260927`. The twelve existing lessons
are repaired as one batch; this is not a course-inventory expansion. Canonical
DSP source remains at `5d73667a486df4a7b6c581e4c9406e810ed4f0f6`, read-only and
clean. P01-P28, P41-P84, other courses, source-map/conversion-manifest, course
identity, platform/UI, dependencies, schemas and workflows are unchanged.

## Learner-visible processing

| Item | Physical processing and comparison | Failure and recovery |
| --- | --- | --- |
| P29 | R^-4 monostatic budget; kTBF noise, measured private-noise power, threshold margin; RCS/frequency/power sweeps and one-variable sensitivities | Anchored R^-2 matches one point but loses only 20 dB/decade; restore both spreading trips |
| P30 | Fractional zero-extended pulse, nonnegative-lag matched sum, integer and parabolic estimates; sampling/fractional-delay/separation sweeps | cτ doubles reported monostatic range; restore cτ/2 |
| P31 | Unit-energy finite Gaussian pulse, physical peak count and width, single-target sub-bin location; 128-trial bias/std/RMSE across SNR | Two adjacent interpolated samples are falsely called targets; restore peak counting and show real wider-bandwidth resolution |
| P32 | Explicit complex LFM, two long overlapping echoes, conjugate-reversed filter and delay-corrected range axis; bandwidth/duration sweeps and separate FsT/BT gain labels | 0.55B replica loses peak height and broadens the response; restore exact transmitted replica |
| P33 | Cosine receive weighting, isolated width/PSLR, output SNR loss, noisy strong/weak scene and leakage margin; taper/separation sweeps | Full Hann at seven-sample spacing masks the weak target; restore validated 17-sample separation |
| P34 | Zero-filled delay-Doppler surfaces for rectangle/LFM/seeded code; delay/Doppler cuts, LFM ridge, duration/bandwidth/code-prefix sweeps | Circular delay wrapping invents full overlap at extreme delay; restore zero extension |
| P35 | Six explicit transmit/receive pulses, listening interval, analytic PRI folding and separately labeled sampled estimate; PRF/range sweeps | Unavailable transmit-pulse identity is assumed; restore apparent range modulo the ambiguity interval |
| P36 | Complex slow-time samples, adjacent-product and phase-slope estimates, windowed FFT; signed velocity/carrier/count sweeps | Magnitude-only processing erases Doppler phase and yields DC; restore coherent complex samples |
| P37 | Three range-envelope × slow-time-phasor components, 256×32 matrix, physical axes, profiles and selected-range Doppler; range/velocity sweeps | Magnitude matrix keeps peaks but loses phase; restore complex matrix orientation and samples |
| P38 | Explicit first/second slow-time differences on clutter/target/noise matrix; periodic nulls, target gain/SNR cost, measured 2x/6x noise-power gains | Fast-time differencing preserves clutter edges and changes shape; restore pulse-column differencing |
| P39 | Separate 4.0/5.3 kHz coherent dwells, direct two-pulse subtraction, normalized velocity response and maximum/OR fusion | Duplicate PRF supplies no diversity at the primary blind speed; restore a diverse PRF while retaining stationary/common-null limits |
| P40 | Known-phase alignment, complex cumulative sum and power sum; pulse-count detectability and Gaussian-jitter expectation | Quadrature error cycle cancels coherent sum but preserves energy; known-error derotation restores coherent fraction |

Each module preserves the original source lesson and guiding question, then adds
physical control instructions, prediction, manipulation, interpretation checks,
a named failure/recovery and teach-back. Source-specific calculations stay in
trusted course entrypoints. Shared presentation helpers do not supply the
physics; normalized-AST checks reject copied algorithm structure through P40.

## Independent numerical evidence

Each item retains baseline, two one-variable sweeps, broken and recovery:
sixty expected/actual pairs. Expected signatures use independent formulations:
log-domain power bookkeeping, overlap-add fractional propagation, SciPy
correlation/FFT convolution, polynomial peak fitting, modulate-then-correlate
ambiguity, remainder timing, real-coordinate phase products/direct DFTs,
selected-row component algebra, FIR filtering/analytic canceller gain, sine-form
blind-speed response, and analytic roots-of-unity/real-coordinate integration.
No reference imports production entrypoints or uses production outputs.

Every pair binds units, inputs, file hashes, error extrema and absolute/scaled
relative tolerances of `1e-8`. Maximum observed absolute difference is
`2.2737367544323206e-13`. Per-module `evidence/provenance.json` binds reference
and production hashes, reference byte count, source pin and field units.
The prior 67205-byte P02-P28 reference source is an exact byte prefix. Historical
P21-P28 provenance checks now verify that original prefix; no prior module or
fixture is rewritten to follow the appended file's hash.

Scientific tests cover R^-4 scaling, half-bin versus sub-bin range, peak counting,
SNR-dependent accuracy, replica mismatch, sidelobe/width/noise tradeoffs,
zero-filled ambiguity, PRI folding, phase loss, matrix axes, clutter cancellation,
noise-power gain, blind nulls and coherent/noncoherent normalization. All offered
control combinations run with finite results below the output-size ceiling.

## Porting choices and limits

- NumPy private seeds preserve deterministic software trials, not MATLAB RNG
  streams. Matrix noise is drawn in NumPy row-major order.
- Vectorized sums and linear convolution replace explicit MATLAB accumulation
  loops while preserving zero extension, conjugate reversal and lag conventions.
  Independent algorithms and physical limiting cases check those conventions.
- P30 retains the source piecewise-linear fractional delay, not a bandlimited
  RF propagation claim. P31 retains sampled-bin half-power width; P32-P34 use
  interpolated crossings. Those width definitions are deliberately distinct.
- P34's duration control changes rectangle/LFM only; the source code comparison
  stays at 13 chips. The 26 µs rectangle is a cut-only sweep. Complete surfaces
  use all delays and 101 Doppler bins; displayed heatmaps retain zero coordinates
  and the strongest local row/column peaks while decimating the remaining points.
- P35 reports rounded-sample timing separately from the analytic PRF interval.
  Rounding a noninteger samples-per-PRI introduces a small timeline-grid error.
- P36 reports signed sampled Doppler; combinations beyond ±PRF/2 alias. P37/P38
  retain Gaussian range responses and omit transmitted waveform/propagation;
  range migration is negligible only under the stated short-dwell model.
- P39 combines separate coherent dwells noncoherently. The illustrative threshold
  is not CFAR or a detection-probability claim; common nulls can remain.
- P40's Gaussian-jitter curve is an ensemble expectation; its quadrature cycle
  is a prescribed clean failure. Recovery assumes actual phase errors are known,
  and is not an acquisition/tracking estimator.
- MATLAB figure cleanup and console presentation become metrics and plots.
  Line displays retain at most 512 points; heatmaps at most 128 columns/64 rows.
  Calculations use the full bounded arrays. No browser/accessibility, MATLAB
  execution, representative learner, hardware/HIL, certification, deployment or
  production validation was performed.

## Verification

Exact required commands are in `contracts/verification.yaml` and the active
batch. New P29-P40 tests: **90 passed**. All sixty independent comparisons and
scoped lint passed. Combined DSP, contract, quick/full, deterministic catalog,
API/live preview, source/scope and frontend checks are being finalized below.

A preliminary regression exposed four missing lesson labels; the interactive
sections now explicitly name sweeps, the broken case and the guiding question.
An older byte-inequality check rejected independently computed exact matches.
For P29-P40 that heuristic is replaced by hash-bound independent provenance and
fresh reference replay; all numeric tolerances and saved-pair error checks are
retained. No expected value was perturbed to force a nonzero difference. The
corrected content/evidence checks passed 168 cases. Concurrent broad checks
also caused timing failures in unchanged P26 and robotics P58; the required
final suites run serially without increasing any timeout. A live server with
cached pre-edit revisions correctly rejected a stale run; restarting the local
preview loads the current catalog before final HTTP checks.

Control PR #505 passed `scripts/validate-control-plane.sh`; a second portfolio
validation passed after the P34 description was corrected to the source's
circular-delay-wrap failure. Hosted control job 108644756202 failed before
executing any steps. The authorized normal control merge succeeded.

Target PR #46 final hosted run 36293685961 had 775 passes and ten failures:
nine checks could not find the uninitialized DSP source submodule and one could
not find historical vehicle commit `4b613a79bfe3cbd997e64e8372a58956533dae2c`.
Frontend passed and container was skipped. These checks pass in the complete
local checkout. Hosted CI is not a completion requirement under retained owner
direction; workflow changes are outside this DSP contract.

## Continuation and rollback

Ledger: one already-distinct, twenty-seven prior repairs, twelve current repairs,
forty-four pending; total 84. Inventory remains six courses / 290 modules /
290 interactive experiments. Issue 441 stays open for P41-P84. Whole-course
numerical/curriculum/capstone maturity remains blocked. The next proposed group
is P41-P52 after this batch's completion/merge and its own scoped contract.
The owner preference for twelve-item groups is retained in both handoffs.

Rollback reverts this isolated batch to the merged PR #46 baseline. No persisted
learner state, source-data migration or deployment changes occur. Protected
target merge remains subject to separate owner approval.
