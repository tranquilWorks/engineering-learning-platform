### DSP-F05 · Sample, identify and reconstruct

**Competency DSP-C05:** Distinguish equal-RMS noise processes by spectrum and correlation, and separate random noise from coherent interference.

**Builds on:** [P01 — Build a Sinusoid and a Complex Phasor](/courses/dsp-radar/modules/01-build-a-sinusoid-and-a-complex-phasor).

**Predict and investigate.** Increase colored_memory while retaining noise_rms_v, then move interferer_offset_hz. Explain why equal RMS does not imply equal spectrum or lag correlation.

**Evidence to keep.** Write your prediction before manipulating controls. Record baseline settings, one-variable comparisons, the plotted quantity and its units, and the result after restoring the same settings. Use the existing lesson's named failure and recovery:

- Trigger: Enable broken_mode.
- Diagnose: Compare raw white, colored, narrowband, and impulsive records at unequal RMS.
- Recover: Mean-center and renormalize every record to the same target RMS.

**Browser recovery.** Turn **Violate the central model assumption** on to capture the fault, then off while holding the other controls at the same values. Compare the recovered evidence with that same-settings healthy run. Use **Reset parameters** to restore the original baseline.

**Explain the relation.** `Rxx[k]=E{x[n] x[n-k]}`. Relate each symbol to a displayed quantity and distinguish samples, seconds, frequency, phase and any power normalization that applies.

**Check your reasoning.** RMS is an aggregate power measure. Memory redistributes that power and raises temporal dependence; a coherent interferer contributes structured spectral energy that averaging does not make white.

**Limit the claim.** A finite seeded record is not an ensemble proof. Distinguish impulsive outliers, correlated noise and deterministic interference before choosing a noise model.

**Completion standard.** A satisfactory explanation connects a prediction to measured browser evidence, uses the correct units, explains the failure causally, and identifies a model limit. Merely reproducing a favorable plot or reading this answer is not an assessment pass. No learner score or completion is stored.

Continue the domain assessment at [P10 — Decimate and Interpolate Without Creating Artifacts](/courses/dsp-radar/modules/10-decimate-and-interpolate-without-creating-artifacts).
