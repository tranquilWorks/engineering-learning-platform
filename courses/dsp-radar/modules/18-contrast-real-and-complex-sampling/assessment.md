### DSP-F18 · Defend a spectral and IQ measurement

**Competency DSP-C18:** Positive and negative complex rotations have opposite phase progression and signed spectra, but projection onto the real axis makes the two cosines identical.

**Builds on:** [P02 — See Sampling as Taking Measurements](/courses/dsp-radar/modules/02-see-sampling-as-taking-measurements); [P03 — Make Aliasing Visually Obvious](/courses/dsp-radar/modules/03-make-aliasing-visually-obvious); [P17 — Perform Complex Downconversion by Hand](/courses/dsp-radar/modules/17-perform-complex-downconversion-by-hand).

**Predict and investigate.** At offset_frequency_hz=160, compare sample_rate_hz=2048 and 256. Use iq_rotation and centered_spectra to explain the signed complex alias.

**Evidence to keep.** Write your prediction before manipulating controls. Record baseline settings, one-variable comparisons, the plotted quantity and its units, and the result after restoring the same settings. Use the existing lesson's named failure and recovery:

- Trigger: Enable broken_mode with the retained broken-case parameters.
- Diagnose: Discard Q and try to infer rotation direction from the identical real projections.
- Recover: Retain both I and Q and interpret the centered signed spectrum.

**Browser recovery.** Turn **Enable the named source failure** on to capture the fault, then off while holding the other controls at the same values. Compare the recovered evidence with that same-settings healthy run. Use **Reset parameters** to restore the original baseline.

**Explain the relation.** `f_alias=((f+fs/2) mod fs)-fs/2`. Relate each symbol to a displayed quantity and distinguish samples, seconds, frequency, phase and any power normalization that applies.

**Check your reasoning.** At 256 samples/s, +160 Hz folds to -96 Hz. The opposite complex rotation folds oppositely, while a real projection combines conjugate components and loses that distinction.

**Limit the claim.** Complex sampling avoids conjugate overlap only within its chosen bandwidth and convention; it does not abolish aliasing.

**Completion standard.** A satisfactory explanation connects a prediction to measured browser evidence, uses the correct units, explains the failure causally, and identifies a model limit. Merely reproducing a favorable plot or reading this answer is not an assessment pass. No learner score or completion is stored.

Continue the domain assessment at [P20 — Estimate Tone Frequency and Phase from Noisy Samples](/courses/dsp-radar/modules/20-estimate-tone-frequency-and-phase-from-noisy-samples).
