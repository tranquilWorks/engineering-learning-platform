### DSP-F11 · Defend a spectral and IQ measurement

**Competency DSP-C11:** A finite record is projected onto zero-based complex-sinusoid bins; signed frequency is the bin label times fs/N, not the one-based storage index.

**Builds on:** [P01 — Build a Sinusoid and a Complex Phasor](/courses/dsp-radar/modules/01-build-a-sinusoid-and-a-complex-phasor); [P02 — See Sampling as Taking Measurements](/courses/dsp-radar/modules/02-see-sampling-as-taking-measurements).

**Predict and investigate.** At N=64 and fs=1024 Hz, predict the 144 Hz tone's zero-based bin. Change tone_bin_offset to 0.5 and compare neighboring_bins; then enable the indexing failure.

**Evidence to keep.** Write your prediction before manipulating controls. Record baseline settings, one-variable comparisons, the plotted quantity and its units, and the result after restoring the same settings. Use the existing lesson's named failure and recovery:

- Trigger: Enable broken_mode with the retained broken-case parameters.
- Diagnose: Use a one-based array index directly as k and shift the reported frequency by one bin.
- Recover: Convert index to zero-based k before applying f=k fs/N.

**Browser recovery.** Turn **Enable the named source failure** on to capture the fault, then off while holding the other controls at the same values. Compare the recovered evidence with that same-settings healthy run. Use **Reset parameters** to restore the original baseline.

**Explain the relation.** `Delta f=fs/N`. Relate each symbol to a displayed quantity and distinguish samples, seconds, frequency, phase and any power normalization that applies.

**Check your reasoning.** Bin spacing is 16 Hz and the on-bin tone occupies bin 9. A fractional-bin tone spreads energy. The broken label adds one bin spacing without changing the underlying samples or transform, so a plausible spectrum can carry a wrong frequency axis.

**Limit the claim.** Changing record length changes the observation duration as well as the grid. The peak-bin estimate is quantized and is not the true frequency for every offset.

**Completion standard.** A satisfactory explanation connects a prediction to measured browser evidence, uses the correct units, explains the failure causally, and identifies a model limit. Merely reproducing a favorable plot or reading this answer is not an assessment pass. No learner score or completion is stored.

Continue the domain assessment at [P20 — Estimate Tone Frequency and Phase from Noisy Samples](/courses/dsp-radar/modules/20-estimate-tone-frequency-and-phase-from-noisy-samples).
