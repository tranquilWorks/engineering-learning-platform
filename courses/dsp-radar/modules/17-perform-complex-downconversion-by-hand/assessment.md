### DSP-F17 · Defend a spectral and IQ measurement

**Competency DSP-C17:** A negative-exponent complex oscillator translates the positive RF copy to the signed difference frequency and its mirror to a distant sum image.

**Builds on:** [P01 — Build a Sinusoid and a Complex Phasor](/courses/dsp-radar/modules/01-build-a-sinusoid-and-a-complex-phasor); [P09 — Compare FIR and IIR Filters by Behavior](/courses/dsp-radar/modules/09-compare-fir-and-iir-filters-by-behavior); [P11 — Make FFT Bins Concrete](/courses/dsp-radar/modules/11-make-fft-bins-concrete).

**Predict and investigate.** Compare lo_frequency_hz=240 and 276, then change lo_phase_rad by pi/2. Use mixer_spectrum to locate the difference and image terms before filtering.

**Evidence to keep.** Write your prediction before manipulating controls. Record baseline settings, one-variable comparisons, the plotted quantity and its units, and the result after restoring the same settings. Use the existing lesson's named failure and recovery:

- Trigger: Enable broken_mode with the retained broken-case parameters.
- Diagnose: Reverse the oscillator sign and select the wrong signed RF copy.
- Recover: Restore exp(-j2pi fLO t), group-delay handling, and the explicit factor of two.

**Browser recovery.** Turn **Enable the named source failure** on to capture the fault, then off while holding the other controls at the same values. Compare the recovered evidence with that same-settings healthy run. Use **Reset parameters** to restore the original baseline.

**Explain the relation.** `f_baseband=f_signal-f_LO`. Relate each symbol to a displayed quantity and distinguish samples, seconds, frequency, phase and any power normalization that applies.

**Check your reasoning.** Complex multiplication shifts the signal by the signed LO frequency. LO phase rotates baseband phase; it does not change the difference frequency. The low-pass filter must suppress the unwanted mixed image.

**Limit the claim.** A difference term outside the retained passband is attenuated. A real mixer does not preserve the same signed-frequency information as a complex one.

**Completion standard.** A satisfactory explanation connects a prediction to measured browser evidence, uses the correct units, explains the failure causally, and identifies a model limit. Merely reproducing a favorable plot or reading this answer is not an assessment pass. No learner score or completion is stored.

Continue the domain assessment at [P20 — Estimate Tone Frequency and Phase from Noisy Samples](/courses/dsp-radar/modules/20-estimate-tone-frequency-and-phase-from-noisy-samples).
