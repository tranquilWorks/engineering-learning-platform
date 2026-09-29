### DSP-F14 · Defend a spectral and IQ measurement

**Competency DSP-C14:** A periodogram estimates one record; Welch averages correctly scaled Hann-windowed segment powers and trades resolution for lower realization variance.

**Builds on:** [P05 — Explore White, Colored, and Impulsive Noise](/courses/dsp-radar/modules/05-explore-white-colored-and-impulsive-noise); [P11 — Make FFT Bins Concrete](/courses/dsp-radar/modules/11-make-fft-bins-concrete); [P12 — Separate Leakage from Noise](/courses/dsp-radar/modules/12-separate-leakage-from-noise).

**Predict and investigate.** Compare segment_length 256 and 1024 on the same total record, then change overlap_fraction. Check psd_comparison and explain how integrating its units returns power.

**Evidence to keep.** Write your prediction before manipulating controls. Record baseline settings, one-variable comparisons, the plotted quantity and its units, and the result after restoring the same settings. Use the existing lesson's named failure and recovery:

- Trigger: Enable broken_mode with the retained broken-case parameters.
- Diagnose: Average logarithmic dB samples and introduce Jensen bias.
- Recover: Average V^2/Hz linearly, then apply 10 log10 once.

**Browser recovery.** Turn **Enable the named source failure** on to capture the fault, then off while holding the other controls at the same values. Compare the recovered evidence with that same-settings healthy run. Use **Reset parameters** to restore the original baseline.

**Explain the relation.** `power=sum_k PSD[k] Delta f`. Relate each symbol to a displayed quantity and distinguish samples, seconds, frequency, phase and any power normalization that applies.

**Check your reasoning.** PSD has units of power per Hz, so summing density times bin width estimates power. Shorter segments give coarser frequency discrimination and more averages. Overlapped segments share samples and are not independent trials.

**Limit the claim.** Welch smoothing reduces variance under stationarity assumptions. More overlap alone does not multiply independent information or remove bias from a nonstationary record.

**Completion standard.** A satisfactory explanation connects a prediction to measured browser evidence, uses the correct units, explains the failure causally, and identifies a model limit. Merely reproducing a favorable plot or reading this answer is not an assessment pass. No learner score or completion is stored.

Continue the domain assessment at [P20 — Estimate Tone Frequency and Phase from Noisy Samples](/courses/dsp-radar/modules/20-estimate-tone-frequency-and-phase-from-noisy-samples).
