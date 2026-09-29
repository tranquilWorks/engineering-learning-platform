### DSP-F74 · Resolve FMCW signs, timing and motion

**Competency DSP-C74:** Three scatterers integrate torso and opposite sinusoidal limb velocities into -4pi displacement/lambda phase. Explicit Hann windows use 75% overlap and a 2048-point FFT. The negative raw frequency axis is reversed so positive means approaching. Longer windows narrow frequency response but blur motion timing.

**Builds on:** [P15 — Use a Spectrogram to See Time-Varying Frequency](/courses/dsp-radar/modules/15-use-a-spectrogram-to-see-time-varying-frequency); [P36 — Measure Doppler from Pulse-to-Pulse Phase](/courses/dsp-radar/modules/36-measure-doppler-from-pulse-to-pulse-phase); [P70 — Create an FMCW Range-Doppler Map](/courses/dsp-radar/modules/70-create-an-fmcw-range-doppler-map).

**Predict and investigate.** Compare swing_speed_mps and window_samples separately. Use velocity and spectrogram to predict the torso line and limb extrema without confusing STFT smearing with different motion.

**Evidence to keep.** Write your prediction before manipulating controls. Record baseline settings, one-variable comparisons, the plotted quantity and its units, and the result after restoring the same settings. Use the existing lesson's named failure and recovery:

- Trigger: Enable broken_mode at baseline controls.
- Diagnose: Absolute value of the slow-time IQ record removes carrier phase and signed bulk Doppler; magnitude fluctuations cannot reconstruct the original motion phase.
- Recover: Use the retained unchanged complex IQ record. The plots use full STFT calculations; display coordinates are decimated and zero-padding is not independent frequency resolution.

**Browser recovery.** Turn **Enable the named failure** on to capture the fault, then off while holding the other controls at the same values. Compare the recovered evidence with that same-settings healthy run. Use **Reset parameters** to restore the original baseline.

**Explain the relation.** `fD(t)=2 v_radial(t)/lambda`. Relate each symbol to a displayed quantity and distinguish samples, seconds, frequency, phase and any power normalization that applies.

**Check your reasoning.** Monostatic Doppler scales with radial speed and inverse wavelength. Longer windows refine frequency discrimination while mixing more motion time; denser overlap does not undo that support tradeoff.

**Limit the claim.** The synthetic kinematic signature is not evidence that a classifier can identify real people, activities or targets.

**Completion standard.** A satisfactory explanation connects a prediction to measured browser evidence, uses the correct units, explains the failure causally, and identifies a model limit. Merely reproducing a favorable plot or reading this answer is not an assessment pass. No learner score or completion is stored.

Continue the domain assessment at [P74 — Create a Micro-Doppler Spectrogram](/courses/dsp-radar/modules/74-create-a-micro-doppler-spectrogram).

### Cumulative assessment DSP-A08 — Resolve FMCW signs, timing and motion

Separate FMCW delay/Doppler, multi-target pairing, virtual-array timing and time-varying Doppler under explicit conventions.

**Evidence portfolio.** Work through the tasks below using the linked laboratories. Keep predictions, settings, dimensioned observations, failure diagnoses and recoveries together.

1. P69–P70: derive the signed beat for the chosen mixer order and label fast-time/slow-time axes. Change fast_samples and chirps separately; contrast physical bandwidth and coherent duration with display bin spacing.
2. P71–P72: reverse velocity, calculate the stationary-formula bias and explain signed up/down beat combinations. Show an algebraically plausible ghost caused by incorrect multi-target pairing.
3. P73: draw TX+RX virtual positions and account for inter-TX time. Compare stationary and moving targets, then explain why same-TX Doppler supports phase compensation.
4. P74: record bulk_doppler, limb_low, limb_high, window_duration and native_frequency_scale for two window_samples values. Enable magnitude-only broken_mode, identify the lost signed motion evidence and restore it.

**Assessment rubric.** All four criteria must be supported by your recorded evidence; a missing criterion means revise that part of the explanation.

- Round-trip delay, mixer sign and Doppler signs remain consistent across all conversions.
- Additional information needed to separate unknowns is named; two-slope algebra is not treated as solved target association.
- Virtual spatial aperture includes its sampling times and motion assumptions.
- Micro-Doppler reasoning uses Hz, ms and velocity consistently and distinguishes window support from display density, including recovery.

**Laboratories:** [P69 — Derive FMCW Range from Beat Frequency](/courses/dsp-radar/modules/69-derive-fmcw-range-from-beat-frequency); [P70 — Create an FMCW Range-Doppler Map](/courses/dsp-radar/modules/70-create-an-fmcw-range-doppler-map); [P71 — Expose FMCW Range-Doppler Coupling](/courses/dsp-radar/modules/71-expose-fmcw-range-doppler-coupling); [P72 — Use Up/Down Triangular Chirps to Separate Range and Velocity](/courses/dsp-radar/modules/72-use-up-down-triangular-chirps-to-separate-range-and-velocity); [P73 — Build a TDM-MIMO Virtual Array](/courses/dsp-radar/modules/73-build-a-tdm-mimo-virtual-array); [P74 — Create a Micro-Doppler Spectrogram](/courses/dsp-radar/modules/74-create-a-micro-doppler-spectrogram).

**Boundary.** No real target classification, deployed MIMO calibration or automotive radar performance is claimed. This rubric is authored self-assessment guidance, not a record of learner validation.
