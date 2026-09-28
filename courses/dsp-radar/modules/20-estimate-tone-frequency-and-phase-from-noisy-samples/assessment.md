### DSP-F20 · Defend a spectral and IQ measurement

**Competency DSP-C20:** A noisy rotating complex phasor supports grid, sub-bin, and coherent phase-step frequency estimates plus de-rotated circular initial-phase estimates.

**Builds on:** [P05 — Explore White, Colored, and Impulsive Noise](/courses/dsp-radar/modules/05-explore-white-colored-and-impulsive-noise); [P11 — Make FFT Bins Concrete](/courses/dsp-radar/modules/11-make-fft-bins-concrete); [P16 — Create an Analytic Signal with the Hilbert Transform](/courses/dsp-radar/modules/16-create-an-analytic-signal-with-the-hilbert-transform); [P19 — Inject and Correct IQ Impairments](/courses/dsp-radar/modules/19-inject-and-correct-iq-impairments).

**Predict and investigate.** Compare record_sample_count=64 and 512 at snr_db=8, then lower SNR. Use frequency_estimators and phase_estimators to distinguish one estimate from bias and spread across trials.

**Evidence to keep.** Write your prediction before manipulating controls. Record baseline settings, one-variable comparisons, the plotted quantity and its units, and the result after restoring the same settings. Use the existing lesson's named failure and recovery:

- Trigger: Enable broken_mode with the retained broken-case parameters.
- Diagnose: Divide a wrapped first-to-last endpoint phase and report a many-turn record as less than one turn.
- Recover: Use coherent adjacent increments, circular phase error, and reject low-coherence amplitude evidence.

**Browser recovery.** Turn **Enable the named source failure** on to capture the fault, then off while holding the other controls at the same values. Compare the recovered evidence with that same-settings healthy run. Use **Reset parameters** to restore the original baseline.

**Explain the relation.** `phase_error=arg(exp(j(phi_est-phi_true)))`. Relate each symbol to a displayed quantity and distinguish samples, seconds, frequency, phase and any power normalization that applies.

**Check your reasoning.** More coherent samples generally improve information, but estimators have different failure modes. Phase errors must be wrapped before averaging; a 2 pi jump is not a physical phase error. Low magnitude or lost phase coherence invalidates phase-slope reasoning.

**Limit the claim.** A single favorable realization cannot establish accuracy or a bound. Identify the repeated-trial population and any reliability gate.

**Completion standard.** A satisfactory explanation connects a prediction to measured browser evidence, uses the correct units, explains the failure causally, and identifies a model limit. Merely reproducing a favorable plot or reading this answer is not an assessment pass. No learner score or completion is stored.

Continue the domain assessment at [P20 — Estimate Tone Frequency and Phase from Noisy Samples](/courses/dsp-radar/modules/20-estimate-tone-frequency-and-phase-from-noisy-samples).

### Cumulative assessment DSP-A02 — Defend a spectral and IQ measurement

Distinguish spectral display, physical resolution and uncertainty, and explain signed IQ processing through calibration and estimation.

**Evidence portfolio.** Work through the tasks below using the linked laboratories. Keep predictions, settings, dimensioned observations, failure diagnoses and recoveries together.

1. P11: reset to 64 samples and zero tone-bin offset. Predict bin_spacing=16 Hz and zero-based peak_bin=9 for the 144 Hz tone. Enable broken_mode and explain the one-bin reported-frequency error without asserting that the transform itself changed.
2. P12–P15: compare window sidelobes and width, padding versus additional observations, PSD integration and STFT support. Record each relevant plot and its axes; explicitly distinguish V²/Hz from power per bin and overlap from independent observations.
3. P16–P19: trace analytic phase, complex mixing, signed aliasing and IQ correction. Use the P18 160 Hz tone at 256 samples/s to predict -96 Hz; show why real projections discard rotation direction and why DC removal alone does not correct branch shear.
4. P20: compare record_sample_count 64 and 512 at snr_db=8, then a lower SNR. Record frequency_estimators and phase_estimators, distinguish trial spread from one favorable result, and show broken_mode recovery at the same controls.

**Assessment rubric.** All four criteria must be supported by your recorded evidence; a missing criterion means revise that part of the explanation.

- Correct bin arithmetic and diagnosis of the label failure; physical resolution is not inferred from zero padding.
- Window/PSD/STFT comparisons retain normalization, bandwidth, duration and units.
- Signed LO and sampling conventions explain the IQ trajectory and calibration stages.
- Estimator bias/spread and wrapped phase are discussed with the low-magnitude reliability limit; exact recovery is demonstrated.

**Laboratories:** [P11 — Make FFT Bins Concrete](/courses/dsp-radar/modules/11-make-fft-bins-concrete); [P12 — Separate Leakage from Noise](/courses/dsp-radar/modules/12-separate-leakage-from-noise); [P13 — Prove Zero-Padding Does Not Improve True Resolution](/courses/dsp-radar/modules/13-prove-zero-padding-does-not-improve-true-resolution); [P14 — Compare Periodogram and Welch PSD Estimates](/courses/dsp-radar/modules/14-compare-periodogram-and-welch-psd-estimates); [P15 — Use a Spectrogram to See Time-Varying Frequency](/courses/dsp-radar/modules/15-use-a-spectrogram-to-see-time-varying-frequency); [P16 — Create an Analytic Signal with the Hilbert Transform](/courses/dsp-radar/modules/16-create-an-analytic-signal-with-the-hilbert-transform); [P17 — Perform Complex Downconversion by Hand](/courses/dsp-radar/modules/17-perform-complex-downconversion-by-hand); [P18 — Contrast Real and Complex Sampling](/courses/dsp-radar/modules/18-contrast-real-and-complex-sampling); [P19 — Inject and Correct IQ Impairments](/courses/dsp-radar/modules/19-inject-and-correct-iq-impairments); [P20 — Estimate Tone Frequency and Phase from Noisy Samples](/courses/dsp-radar/modules/20-estimate-tone-frequency-and-phase-from-noisy-samples).

**Boundary.** The linked evidence is a learner synthesis of distinct experiments; it is not a claim that P20 executes every preceding IQ stage. This rubric is authored self-assessment guidance, not a record of learner validation.
