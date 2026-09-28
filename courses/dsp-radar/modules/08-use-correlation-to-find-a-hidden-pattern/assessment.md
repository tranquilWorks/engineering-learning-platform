### DSP-F08 · Sample, identify and reconstruct

**Competency DSP-C08:** Use correlation to locate a known pattern and distinguish weak evidence from unresolved nearby peaks.

**Builds on:** [P05 — Explore White, Colored, and Impulsive Noise](/courses/dsp-radar/modules/05-explore-white-colored-and-impulsive-noise); [P06 — Use an Impulse to Reveal a System](/courses/dsp-radar/modules/06-use-an-impulse-to-reveal-a-system).

**Predict and investigate.** Decrease target_amplitude at fixed noise_sigma, then reduce target_separation_samples. Use correlation to distinguish weak detection from merged peaks.

**Evidence to keep.** Write your prediction before manipulating controls. Record baseline settings, one-variable comparisons, the plotted quantity and its units, and the result after restoring the same settings. Use the existing lesson's named failure and recovery:

- Trigger: Enable broken_mode.
- Diagnose: Report the full-convolution array index as delay without subtracting reference length minus one.
- Recover: Map the peak through the explicit lag vector and confirm reversed-reference convolution equivalence.

**Browser recovery.** Turn **Violate the central model assumption** on to capture the fault, then off while holding the other controls at the same values. Compare the recovered evidence with that same-settings healthy run. Use **Reset parameters** to restore the original baseline.

**Explain the relation.** `rxy[k]=sum_n x[n] conjugate(y[n-k])`. Relate each symbol to a displayed quantity and distinguish samples, seconds, frequency, phase and any power normalization that applies.

**Check your reasoning.** Correlation coherently sums the known pattern at candidate lags. More signal increases peak contrast, but two closely spaced patterns can overlap within the correlation response even if each would be detectable alone.

**Limit the claim.** The lag sign follows the declared correlation convention. The largest peak in one noisy record does not establish detection probability.

**Completion standard.** A satisfactory explanation connects a prediction to measured browser evidence, uses the correct units, explains the failure causally, and identifies a model limit. Merely reproducing a favorable plot or reading this answer is not an assessment pass. No learner score or completion is stored.

Continue the domain assessment at [P10 — Decimate and Interpolate Without Creating Artifacts](/courses/dsp-radar/modules/10-decimate-and-interpolate-without-creating-artifacts).
