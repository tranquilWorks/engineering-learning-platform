# ELP-DSP-FIDELITY-P11-P20 evidence — 2026-09-24

## Scope and identities

This batch repairs exactly DSP/Radar P11-P20 from target baseline
`a24818f42ff267394ee4ec97727ddb7d1978e3f4`, tree
`1b5f62cc0adaa1796c459e7def317405cea4fe37`. Portfolio Control authorization
merged in PR #499 as commit `8306551de3f32f9cb15c38efb3f5ab1e886756f0`, tree
`32ce8c7b9c9129489877acebb85685ac6ab8894c`; the active contract blob is
`d4282cef4b773182e434ec5af6725ea8af207277`.

The read-only source remains commit
`5d73667a486df4a7b6c581e4c9406e810ed4f0f6`, tree
`7a3a0f9adce607e10097724c13745eace212f4e1`. Immutable identities retained by
the batch are:

- source map SHA-256: `5b2751769cf70d7c4faad148fecd2db16e7995982122777fa012bfbda7850bf5`
- conversion manifest SHA-256: `1244c6dea11ea11b880e0f26d54ce81dea42ea1ab4981d4d5180c440eb7890a4`
- course manifest SHA-256: `9950220969a64e5c7faed96ae1f8a2395339c7dbd292a9471c89001a2a5d0228`
- source curriculum SHA-256: `0b92e76efc1f72930fab730145326315219ab3813b8cbf17d32a33f507a4974f`
- source file-set SHA-256: `c2511015b195a48bd847bd1f1cdeed92384a10eddf0b23e755590af4fb66ddca`

P01-P10, P21-P84, every other course, and the source gitlink remain outside the
module-artifact edit scope. In `coverage.yaml`, only P11-P20
`target_content_digest` values are refreshed; identities, statuses, record paths,
blockers, the summary, and all other item digests remain retained.

## Source-fidelity matrix

| Item | Retained source flow and controls | Governing relation and independent signature | Named failure and recovery | Deliberate omission, limitation, and residual risk |
| --- | --- | --- | --- | --- |
| P11 | Complex tone/noise → explicit DFT and FFT → zero-based/signed bin map; record length and fractional-bin offset | `X[k]=Σx[n]e^-j2πkn/N`, `fk=kfs/N`; signature includes spacing, peak, signed/reported frequency, DFT error, neighbor magnitudes | One-based array index used as `k` shifts the axis one bin; recover with `k=index-1` and magnitude-gated phase | MATLAB figures omitted; a largest bin is not a general exact-frequency estimator. |
| P12 | Explicit rectangular, Hann, Hamming, Blackman, and flat-top windows; window and fractional-offset sweeps | `Xw[k]=Σx[n]w[n]e^-j2πkn/N`, coherent gain, main-lobe width, amplitude error, sidelobes, clean/noise metrics | Treat all nonpeak energy as noise; recover by separating deterministic window leakage from seeded noise | Dense FFT is display sampling, not extra resolution; finite seeded noise is not a distribution-wide claim. |
| P13 | One shared 512-sample two-tone record → 128-sample 1×/4×/16× padding and 128/256/512 measured-sample comparisons | `Δfdisplay=fs/NFFT`, `ΔfRayleigh=fs/Nrecord`; signature includes both scales and the 198/202 Hz valley ratio | Call display spacing physical resolution; recover by reporting the observation-derived scale separately | MATLAB figures omitted; the 4 Hz pair illustrates one finite-record criterion, not every estimator. |
| P14 | Full-record periodogram and explicit Hann Welch PSD → segment/overlap sweeps → 24 seeded probe repetitions | `Sxx=|X|²/(fsΣw²)` in V²/Hz; signature includes raw and correlation-adjusted effective averages, periodogram/Welch CV, and linear/log averaging | Average dB values and incur low bias; recover by averaging linear power before `10log10` | Effective-average count is the retained window-correlation approximation, not a universal confidence interval. |
| P15 | Explicit 90 Hz steady tone, gated 220–320 Hz chirp, 380 Hz 64-sample burst, and continuous-phase 156/174 Hz hop → Hann STFT | `Xm[k]=Σx[n+mH]w[n]e^-j2πkn/N`; signature includes frame count/spacing, window width, burst error, hop contrast | Pad a 64-sample window to 512 and call the 2 Hz grid physical resolution; recover the 64-sample main-lobe scale | MATLAB display behavior omitted; the bounded components illustrate, rather than exhaust, time-frequency analysis. |
| P16 | Real AM/PM carrier → explicit even-length FFT Hilbert mask → envelope, unwrapped phase, instantaneous frequency | Retain DC/Nyquist, double positive bins, zero negative bins; signature includes envelope/IF RMSE, suppression, minimum amplitude, spike, withheld count | Differentiate phase through a near-zero envelope; recover by requiring both adjacent analytic amplitudes above 0.05 V | Amplitude gating withholds evidence; it does not reconstruct unknowable phase through a null. |
| P17 | Real 240 Hz passband tone → negative-exponent complex LO → explicit 129-tap windowed-sinc LPF → group-delay exclusion and 2× calibration | `fBB=fc-fLO`; signature includes signed beat, calibrated amplitude/phase, sum-image suppression, wrong-sign and recovered estimates | Reverse oscillator sign and retain the wrong signed copy; recover `exp(-j2πfLOt)` | Fixed FIR/guard choices are teaching parameters, not receiver certification. |
| P18 | Conjugate complex rotations and identical real projections → centered spectra and signed phase increments → rate/offset aliases | `fa=((f+fs/2) mod fs)-fs/2`; signature includes expected aliases, measured signs, projection equality, discard-Q and recovery estimates | Discard Q so both rotations collapse to the same real cosine and zero sign estimate; recover full I+jQ | Synthetic complex samples do not validate a physical I/Q front end. |
| P19 | Inject DC, branch gain, and quadrature shear separately/together → mean, gain, shear correction in source order | Receiver equations for `Ir` and `Qr`; signature includes DC dBc, IRR, correlation, axis ratio, parameter estimates, broken/recovered IRR | Substitute a global rotation, which preserves image magnitude; recover with the inverse shear | Memoryless impairment model omits frequency-dependent analog imbalance and hardware drift. |
| P20 | Fractional-bin noisy phasor → peak-bin, log-parabolic FFT, coherent adjacent-phase estimates → de-rotated phase and 40-trial sweeps | Signature includes three frequency/phase estimates, coherence, wrapped endpoint, noise-free recovery, and low-amplitude gate | Divide a wrapped endpoint angle; recover coherent adjacent increments and reject coherence below 0.20 | The single-tone stationary model does not cover multi-tone, acceleration, or phase-noise estimators. |

Every item retains separate expected and actual numeric evidence for `baseline`,
`sweep_1`, `sweep_2`, `broken`, and `recovery`. Expected signatures come from
`remediation_reference_cases.py`, which imports no production experiment,
consumes no production result, and perturbs no production value. Absolute and
relative tolerances are `0.0001`; all 50 comparisons pass. Expected files use
compact JSON and actual files use indented JSON so framework checks also reject
literal self-comparison.

## Structural and semantic prevention

- P11-P20 contain none of `primary_scale`, `secondary_scale`, `noise_db`, or
  shared `PHASE` dispatch.
- A normalized-AST check replaces identifiers and literals before comparing
  P02-P20; all nineteen repaired program shapes remain distinct.
- Focused checks cover explicit-DFT equality, leakage/noise separation, padding
  versus observation, correct PSD scaling and averaging order, STFT resolution,
  analytic-signal gating, complex-LO sign, discard-Q ambiguity, ordered I/Q
  correction, wrapped phase, and coherence rejection.
- P02-P10 evidence and behavior remain under their existing regression suite.

## Verification

| Gate | Result |
| --- | --- |
| Focused DSP fidelity, conversion, course, and caliber suite | `345 passed` |
| Full backend suite | `685 passed`, 3 dependency deprecation warnings |
| Contract wrapper | `72 passed` |
| Quick wrapper | `685 passed`, same warnings |
| Full wrapper | passed: deterministic catalog, `685 passed`, TypeScript, and production build |
| Deterministic catalog execution | passed: 6 courses, 290 modules, 290 interactive modules |
| Ruff on repaired modules, reference, and affected tests | passed |
| TypeScript | passed |
| Production web build | passed; existing Plotly chunk-size advisory only |
| Diff and authorized-scope checks | passed |
| Source and immutable-range cleanliness | passed; coverage changed only P11-P20 target digests |

Hosted CI is not required by owner direction for this batch.

## Claim boundary and next state

The remediation ledger derives 84 total items as one already-distinct item
(P01), nine prior-batch repairs (P02-P10), ten current-batch repairs (P11-P20),
and 64 pending items (P21-P84). This batch does not complete issue 441.
DSP/Radar remains blocked at `numerically_verified`, `curriculum_covered`, and
`capstone_integrated`; P84 remains an unverified generic capstone implementation.

MATLAB runtime comparison, audio playback, browser/accessibility validation,
representative learner validation, physical HIL/hardware, certification,
release, deployment, credentials/settings, and production use were not performed.
