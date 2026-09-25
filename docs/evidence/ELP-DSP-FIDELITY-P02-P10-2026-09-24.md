# ELP-DSP-FIDELITY-P02-P10 evidence — 2026-09-24

## Scope and identities

This batch repairs exactly DSP/Radar P02-P10 from target baseline `4b613a79bfe3cbd997e64e8372a58956533dae2c`, tree `9d7de9eb1399cdc541cc8475a2bc0a380c9c00e5`. Final Portfolio Control authorization is `0cb45fc2c4c2586d172b05d8b9a70a0957af3cd8` after merged control PRs #490, #491, #493, and #495.

The active contract has Git blob `454dbb1bc16dacd036f393d7c482e8e22be9f1e7`, identical to the file at the final control commit. The read-only source remains commit `5d73667a486df4a7b6c581e4c9406e810ed4f0f6`, tree `7a3a0f9adce607e10097724c13745eace212f4e1`.

Immutable target identities stayed unchanged:

- source map SHA-256: `5b2751769cf70d7c4faad148fecd2db16e7995982122777fa012bfbda7850bf5`
- conversion manifest SHA-256: `1244c6dea11ea11b880e0f26d54ce81dea42ea1ab4981d4d5180c440eb7890a4`
- course manifest SHA-256: `9950220969a64e5c7faed96ae1f8a2395339c7dbd292a9471c89001a2a5d0228`
- source curriculum SHA-256: `0b92e76efc1f72930fab730145326315219ab3813b8cbf17d32a33f507a4974f`
- source file-set SHA-256: `c2511015b195a48bd847bd1f1cdeed92384a10eddf0b23e755590af4fb66ddca`

P01, P11-P84, every other course, and the source gitlink are byte-identical to the target baseline. In `coverage.yaml`, only P02-P10 `target_content_digest` values changed; all identities, statuses, record paths, blockers, summary fields, and P01/P11-P84 digests are identical.

## Source-fidelity matrix

| Item | Retained source flow and controls | Governing relation and numeric signature | Named failure and recovery | Deliberate omission, limitation, and residual risk |
| --- | --- | --- | --- | --- |
| P02 | Dense sinusoid → timed measurements → linear interpolation; sample rate and clock offset sweeps | `x[n]=A cos(2πf(n+δ)/fs+φ)`; signature records `fs`, offset, count, interpolation RMSE, reflected-alias error, high-alias error | Force 7 Hz at 12 Sa/s; 5 Hz and 19 Hz candidates agree exactly. Recover with the declared 80 Sa/s bandlimit. | MATLAB window behavior omitted. Linear interpolation is illustrative, not ideal reconstruction; bandlimit knowledge remains required. |
| P03 | Input tone → signed fold → positive apparent tone with conditional phase reversal → recurrence estimate; input-frequency and sample-rate sweeps | `fa=f-round(f/fs)fs`; the second-order recurrence independently estimates `|fa|`; signature records input, rate, signed/apparent fold, estimate, agreement | Keep original phase after a negative fold so sample agreement fails. Recover by reversing phase and checking the recurrence. | MATLAB window behavior omitted. A finite noiseless record demonstrates convention fidelity, not a general noisy estimator guarantee. |
| P04 | Sinusoid → optional seeded triangular dither → bounded bipolar mid-rise quantizer → code saturation/error/SQNR; bit-depth and utilization sweeps | `Δ=2VFS/2^b`, `|e|≤Δ/2` when not overloaded, ideal `6.02b+1.76 dB`; signature records bits, amplitude, dither, step, SQNR, bound, clipping count | Drive beyond ±1 V so overload is distinct from quantization error. Recover at 0.9 V; codes remain in `[0,2^b-1]`. | Audio playback and MATLAB sound-device behavior omitted. Synthetic tone SQNR is deterministic software evidence only. |
| P05 | Seeded white/colored/narrowband/impulsive generation → separate mean removal and equal-RMS scaling → structural/tone metrics; colored-memory and interferer-offset sweeps | `xN=(x-mean(x)) σtarget/rms(x-mean(x))`; signature records controls, white RMS, colored lag-one, impulsive crest, tone error, normalization residual | Compare unequal-RMS raw records so shape and power are confounded. Recover by centering and renormalizing each family. | MATLAB interactive display omitted. Finite seeded statistics do not characterize every noise process. |
| P06 | Impulse responses for delay/moving average/echo/resonator → direct implementations and linear convolution; echo-delay and pole-radius sweeps | `y=x*h`; resonator recurrence and direct paths match convolution; signature records four equivalence errors and circular-wrap error | Use unpadded N-point circular convolution so the tail wraps. Recover with linear convolution or `N+M-1` padding. | MATLAB window behavior omitted. The bounded resonator is a teaching system, not identified hardware. |
| P07 | Pulse → three shifted signed path contributions → explicit accumulation/manual sum/NumPy convolution; middle-delay and signed-gain sweeps | `y[n]=Σk h[k]x[n-k]`; signature records controls, manual/convolution equality, overwrite error | Overwrite rather than add overlapping paths. Recover by accumulating every contribution with superposition. | MATLAB window behavior omitted. Three paths expose the mechanism but do not model a full propagation channel. |
| P08 | Asymmetric chip reference → seeded noisy insertion at zero-based delay → explicit-lag correlation and reversed-reference convolution; amplitude/noise plus separation views | `rxs[ℓ]=Σn x[n]s[n-ℓ]`; signature records amplitude, noise, separation, recovered/reported delay, alternate-form error | Report the full-convolution array index as delay, producing a reference-length-minus-one error. Recover through the lag vector. | MATLAB window behavior omitted. The separation view is finite deterministic resolution evidence, not a probability-of-detection claim. |
| P09 | Windowed-sinc FIR and stable low-pass biquad → magnitude/group delay/impulse/step/pulse/signal-noise/arithmetic views; FIR-tap and IIR-Q sweeps | FIR convolution and biquad difference equation; signature records taps, Q, IIR peak, FIR stopband power, multiply counts | Put a pole radius at 1.02 so the impulse grows. Recover at 0.98 and verify decay. | MATLAB filter-design/window behavior omitted. Coefficient quantization and implementation-specific arithmetic are not characterized. |
| P10 | Anti-alias FIR → 4:1 sample selection → zero insertion → gain-corrected reconstruction FIR; offending-tone and reconstruction-tap sweeps | `yd[n]=(x*hAA)[4n]`, `yu[4n]=yd[n]`, `xr=yu*hR`; signature records rates, folded frequency/amplitude, image amplitude, recovered low tone | Drop samples directly and leave inserted zeros unfiltered, exposing fold and image artifacts. Recover by filtering on the correct side of each rate change. | MATLAB window behavior omitted. This fixed 4:1 example does not certify arbitrary multistage designs. |

Each item retains expected and actual numeric evidence for `baseline`, `sweep_1`, `sweep_2`, `broken`, and `recovery`. Expected signatures come from `remediation_reference_cases.py`, which imports no production experiment, consumes no production result, and perturbs no production value. Absolute and relative tolerances are `0.0001`; observed maximum errors are within tolerance. Evidence files deliberately use distinct serializations so retained-framework checks reject literal self-comparison.

## Structural and semantic prevention

- P02-P10 contain none of `primary_scale`, `secondary_scale`, `noise_db`, or shared `PHASE` dispatch.
- A normalized-AST test replaces identifiers and literals before comparing program shapes; all nine repaired experiments remain distinct.
- Focused invariants assert alias-family equality, wrong-phase failure, half-LSB and code bounds, equal-RMS recovery, direct/convolution equality, overlap accumulation, lag convention, pole growth/decay, and multirate artifact suppression.
- The retained Vehicle Dynamics terminal-contract test now reads its historical contract from merged target baseline `4b613a79bfe3cbd997e64e8372a58956533dae2c`; it no longer requires that completed batch to remain globally active. No Vehicle Dynamics course artifact or claim changed.

## Verification

| Gate | Result |
| --- | --- |
| Focused DSP fidelity, conversion, course, and caliber suite | `327 passed` |
| Full backend suite | `667 passed`, 3 pre-existing dependency deprecation warnings |
| Contract wrapper | `72 passed` |
| Quick wrapper | `667 passed`, same warnings |
| Full wrapper | passed; catalog check, `667 passed`, TypeScript, and production build |
| Deterministic catalog execution | passed: 6 courses, 290 modules, 290 interactive modules |
| Ruff on repaired modules, reference, and affected tests | passed |
| TypeScript | passed |
| Production web build | passed; existing Plotly chunk-size advisory only |
| Diff and authorized-scope checks | passed |
| Source, map, manifest, course, P01/P11-P84, and other-course cleanliness | passed |
| Coverage semantic-preservation check | only P02-P10 target digests changed; every other field identical |

Hosted CI is not required by owner direction for this batch.

## Claim boundary and next state

The remediation ledger derives 84 total items as one prior distinct item (P01), nine repaired items (P02-P10), and 74 pending items (P11-P84). This batch does not complete issue 441. DSP/Radar remains blocked at `numerically_verified`, `curriculum_covered`, and `capstone_integrated`, and P84 remains an unverified generic capstone implementation.

MATLAB runtime comparison, audio playback, browser/accessibility validation, representative learner validation, physical HIL/hardware, certification, release, deployment, credentials/settings, and production use were not performed.
