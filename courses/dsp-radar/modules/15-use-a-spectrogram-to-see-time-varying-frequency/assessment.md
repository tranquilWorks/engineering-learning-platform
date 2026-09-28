### DSP-F15 · Defend a spectral and IQ measurement

**Competency DSP-C15:** An explicit sliding-window DFT turns a composite time record into local PSD frames whose window length controls time-frequency tradeoff.

**Builds on:** [P11 — Make FFT Bins Concrete](/courses/dsp-radar/modules/11-make-fft-bins-concrete); [P12 — Separate Leakage from Noise](/courses/dsp-radar/modules/12-separate-leakage-from-noise).

**Predict and investigate.** Compare window_length 64 and 512 for the short burst, then increase overlap. Use spectrogram and window_sweep to separate time support from display time step.

**Evidence to keep.** Write your prediction before manipulating controls. Record baseline settings, one-variable comparisons, the plotted quantity and its units, and the result after restoring the same settings. Use the existing lesson's named failure and recovery:

- Trigger: Enable broken_mode with the retained broken-case parameters.
- Diagnose: Zero-pad a 64-sample window to 512 and call its 2 Hz grid physical resolution.
- Recover: Use the 64-sample Hann main-lobe scale for physical resolution.

**Browser recovery.** Turn **Enable the named source failure** on to capture the fault, then off while holding the other controls at the same values. Compare the recovered evidence with that same-settings healthy run. Use **Reset parameters** to restore the original baseline.

**Explain the relation.** `Twindow=L/fs; Delta t_hop=H/fs`. Relate each symbol to a displayed quantity and distinguish samples, seconds, frequency, phase and any power normalization that applies.

**Check your reasoning.** A longer window pools more time and narrows frequency bins, smearing abrupt changes. More overlap reduces hop size but does not shorten each window's support or undo that tradeoff.

**Limit the claim.** A bright ridge's time coordinate depends on frame alignment. Edge padding and low-energy frames need separate interpretation.

**Completion standard.** A satisfactory explanation connects a prediction to measured browser evidence, uses the correct units, explains the failure causally, and identifies a model limit. Merely reproducing a favorable plot or reading this answer is not an assessment pass. No learner score or completion is stored.

Continue the domain assessment at [P20 — Estimate Tone Frequency and Phase from Noisy Samples](/courses/dsp-radar/modules/20-estimate-tone-frequency-and-phase-from-noisy-samples).
