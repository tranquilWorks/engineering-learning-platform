### DSP-F12 · Defend a spectral and IQ measurement

**Competency DSP-C12:** A finite observation multiplies the tone by a window, so its deterministic window spectrum shifts around the tone independently of random noise.

**Builds on:** [P05 — Explore White, Colored, and Impulsive Noise](/courses/dsp-radar/modules/05-explore-white-colored-and-impulsive-noise); [P11 — Make FFT Bins Concrete](/courses/dsp-radar/modules/11-make-fft-bins-concrete).

**Predict and investigate.** At tone_bin_offset=0.35, compare Rectangular and Hann windows in leakage_spectrum. Record both sidelobe behavior and mainlobe width before choosing a window.

**Evidence to keep.** Write your prediction before manipulating controls. Record baseline settings, one-variable comparisons, the plotted quantity and its units, and the result after restoring the same settings. Use the existing lesson's named failure and recovery:

- Trigger: Enable broken_mode with the retained broken-case parameters.
- Diagnose: Call every clean nonpeak projection noise.
- Recover: Separate the known clean-window response from the independently seeded noise realization.

**Browser recovery.** Turn **Enable the named source failure** on to capture the fault, then off while holding the other controls at the same values. Compare the recovered evidence with that same-settings healthy run. Use **Reset parameters** to restore the original baseline.

**Explain the relation.** `Xw[k]=DFT{w[n] x[n]}`. Relate each symbol to a displayed quantity and distinguish samples, seconds, frequency, phase and any power normalization that applies.

**Check your reasoning.** Multiplication by a window convolves the signal spectrum with the window spectrum. Reduced sidelobes come with a wider mainlobe and changed coherent/noise gain; leakage from a tone remains structured rather than becoming random noise.

**Limit the claim.** A lower plotted floor may hide gain normalization. Compare equivalent units and gain corrections before interpreting amplitude or noise power.

**Completion standard.** A satisfactory explanation connects a prediction to measured browser evidence, uses the correct units, explains the failure causally, and identifies a model limit. Merely reproducing a favorable plot or reading this answer is not an assessment pass. No learner score or completion is stored.

Continue the domain assessment at [P20 — Estimate Tone Frequency and Phase from Noisy Samples](/courses/dsp-radar/modules/20-estimate-tone-frequency-and-phase-from-noisy-samples).
