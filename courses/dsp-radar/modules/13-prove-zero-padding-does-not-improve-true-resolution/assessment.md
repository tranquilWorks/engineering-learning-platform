### DSP-F13 · Defend a spectral and IQ measurement

**Competency DSP-C13:** Appending zeros samples the same finite-record transform more densely; acquiring shared additional samples changes the physical observation and its Rayleigh scale.

**Builds on:** [P11 — Make FFT Bins Concrete](/courses/dsp-radar/modules/11-make-fft-bins-concrete); [P12 — Separate Leakage from Noise](/courses/dsp-radar/modules/12-separate-leakage-from-noise).

**Predict and investigate.** Keep observation_multiplier=1 and compare padding_factor 1, 4 and 16. Then increase actual observation length. Use padded_spectrum and observation_sweep to test the two-tone resolution claim.

**Evidence to keep.** Write your prediction before manipulating controls. Record baseline settings, one-variable comparisons, the plotted quantity and its units, and the result after restoring the same settings. Use the existing lesson's named failure and recovery:

- Trigger: Enable broken_mode with the retained broken-case parameters.
- Diagnose: Treat fs/NFFT display spacing as true physical resolution.
- Recover: Report display spacing and the observation-derived Rayleigh scale separately.

**Browser recovery.** Turn **Enable the named source failure** on to capture the fault, then off while holding the other controls at the same values. Compare the recovered evidence with that same-settings healthy run. Use **Reset parameters** to restore the original baseline.

**Explain the relation.** `Delta f_display=fs/Nfft; Tobs=N/fs`. Relate each symbol to a displayed quantity and distinguish samples, seconds, frequency, phase and any power normalization that applies.

**Check your reasoning.** Padding samples the same finite-record transform more densely; it does not add information or narrow the underlying response. Acquiring a longer coherent record changes that response and can separate nearby tones.

**Limit the claim.** Peak interpolation can improve a single-tone estimate without resolving two tones. Display-bin spacing and physical resolution are separate quantities.

**Completion standard.** A satisfactory explanation connects a prediction to measured browser evidence, uses the correct units, explains the failure causally, and identifies a model limit. Merely reproducing a favorable plot or reading this answer is not an assessment pass. No learner score or completion is stored.

Continue the domain assessment at [P20 — Estimate Tone Frequency and Phase from Noisy Samples](/courses/dsp-radar/modules/20-estimate-tone-frequency-and-phase-from-noisy-samples).
