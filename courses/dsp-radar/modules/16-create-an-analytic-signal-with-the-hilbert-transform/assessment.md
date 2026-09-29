### DSP-F16 · Defend a spectral and IQ measurement

**Competency DSP-C16:** The even-length FFT Hilbert mask constructs a one-sided analytic signal whose magnitude, unwrapped phase, and phase derivative describe envelope and instantaneous frequency.

**Builds on:** [P01 — Build a Sinusoid and a Complex Phasor](/courses/dsp-radar/modules/01-build-a-sinusoid-and-a-complex-phasor); [P09 — Compare FIR and IIR Filters by Behavior](/courses/dsp-radar/modules/09-compare-fir-and-iir-filters-by-behavior); [P11 — Make FFT Bins Concrete](/courses/dsp-radar/modules/11-make-fft-bins-concrete).

**Predict and investigate.** Vary envelope_depth and phase_deviation_rad separately. Use waveform_envelope and reliability_gate to decide where phase differentiation is trustworthy.

**Evidence to keep.** Write your prediction before manipulating controls. Record baseline settings, one-variable comparisons, the plotted quantity and its units, and the result after restoring the same settings. Use the existing lesson's named failure and recovery:

- Trigger: Enable broken_mode with the retained broken-case parameters.
- Diagnose: Differentiate phase while the analytic envelope is noise-dominated near zero.
- Recover: Withhold estimates unless both adjacent amplitudes exceed 0.05 V.

**Browser recovery.** Turn **Enable the named source failure** on to capture the fault, then off while holding the other controls at the same values. Compare the recovered evidence with that same-settings healthy run. Use **Reset parameters** to restore the original baseline.

**Explain the relation.** `f_inst=(fs/(2 pi)) Delta unwrap(arg(z))`. Relate each symbol to a displayed quantity and distinguish samples, seconds, frequency, phase and any power normalization that applies.

**Check your reasoning.** The analytic signal's magnitude estimates an envelope under the signal-separation assumptions. Unwrapped phase slope gives Hz after multiplication by fs/(2 pi); phase near a vanishing envelope is poorly determined.

**Limit the claim.** The Hilbert construction does not make every multicomponent signal admit a unique physical instantaneous frequency.

**Completion standard.** A satisfactory explanation connects a prediction to measured browser evidence, uses the correct units, explains the failure causally, and identifies a model limit. Merely reproducing a favorable plot or reading this answer is not an assessment pass. No learner score or completion is stored.

Continue the domain assessment at [P20 — Estimate Tone Frequency and Phase from Noisy Samples](/courses/dsp-radar/modules/20-estimate-tone-frequency-and-phase-from-noisy-samples).
