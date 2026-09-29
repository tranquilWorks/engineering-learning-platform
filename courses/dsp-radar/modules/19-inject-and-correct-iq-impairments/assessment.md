### DSP-F19 · Defend a spectral and IQ measurement

**Competency DSP-C19:** DC shifts the I/Q center, branch-gain mismatch stretches the trajectory, and quadrature error shears it while creating a conjugate image.

**Builds on:** [P17 — Perform Complex Downconversion by Hand](/courses/dsp-radar/modules/17-perform-complex-downconversion-by-hand); [P18 — Contrast Real and Complex Sampling](/courses/dsp-radar/modules/18-contrast-real-and-complex-sampling).

**Predict and investigate.** Compare i_gain=1 and 1.3, then quadrature_error_deg=0 and 15. Inspect trajectory and correction_stages before deciding which calibration terms are required.

**Evidence to keep.** Write your prediction before manipulating controls. Record baseline settings, one-variable comparisons, the plotted quantity and its units, and the result after restoring the same settings. Use the existing lesson's named failure and recovery:

- Trigger: Enable broken_mode with the retained broken-case parameters.
- Diagnose: Apply a global rotation, which preserves desired and image magnitudes.
- Recover: Remove mean, normalize gains, and invert shear in that source order.

**Browser recovery.** Turn **Enable the named source failure** on to capture the fault, then off while holding the other controls at the same values. Compare the recovered evidence with that same-settings healthy run. Use **Reset parameters** to restore the original baseline.

**Explain the relation.** `[I_measured,Q_measured]^T=M [I,Q]^T+b`. Relate each symbol to a displayed quantity and distinguish samples, seconds, frequency, phase and any power normalization that applies.

**Check your reasoning.** Gain imbalance stretches the IQ orbit; quadrature error shears it and creates an image. DC removal addresses translation, while inversion of the calibrated branch matrix addresses gain and shear.

**Limit the claim.** A calibration inferred from unsuitable or changing data may not transfer. Image rejection is finite and must be stated with its signal/noise assumptions.

**Completion standard.** A satisfactory explanation connects a prediction to measured browser evidence, uses the correct units, explains the failure causally, and identifies a model limit. Merely reproducing a favorable plot or reading this answer is not an assessment pass. No learner score or completion is stored.

Continue the domain assessment at [P20 — Estimate Tone Frequency and Phase from Noisy Samples](/courses/dsp-radar/modules/20-estimate-tone-frequency-and-phase-from-noisy-samples).
