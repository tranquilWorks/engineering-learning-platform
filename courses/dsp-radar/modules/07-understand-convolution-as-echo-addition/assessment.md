### DSP-F07 · Sample, identify and reconstruct

**Competency DSP-C07:** The pinned source develops this physical relationship from deterministic measurements.

**Builds on:** [P06 — Use an Impulse to Reveal a System](/courses/dsp-radar/modules/06-use-an-impulse-to-reveal-a-system).

**Predict and investigate.** Change middle_echo_delay_samples, then make third_echo_gain more negative. Predict where cancellation occurs in echo_paths before checking sum_check.

**Evidence to keep.** Write your prediction before manipulating controls. Record baseline settings, one-variable comparisons, the plotted quantity and its units, and the result after restoring the same settings. Use the existing lesson's named failure and recovery:

- Trigger: Enable broken_mode.
- Diagnose: Overwrite rather than add samples where shifted signed echoes overlap.
- Recover: Accumulate every path so manual, explicit-sum, and NumPy convolution outputs agree.

**Browser recovery.** Turn **Violate the central model assumption** on to capture the fault, then off while holding the other controls at the same values. Compare the recovered evidence with that same-settings healthy run. Use **Reset parameters** to restore the original baseline.

**Explain the relation.** `y[n]=sum_i a_i x[n-d_i]`. Relate each symbol to a displayed quantity and distinguish samples, seconds, frequency, phase and any power normalization that applies.

**Check your reasoning.** A delay moves one scaled copy; negative gain subtracts it. The total is the samplewise sum of delayed paths, so cancellation depends on overlap and signal sign, not solely on path magnitudes.

**Limit the claim.** Record boundaries require explicit zero extension; circular wraparound would invent early echoes.

**Completion standard.** A satisfactory explanation connects a prediction to measured browser evidence, uses the correct units, explains the failure causally, and identifies a model limit. Merely reproducing a favorable plot or reading this answer is not an assessment pass. No learner score or completion is stored.

Continue the domain assessment at [P10 — Decimate and Interpolate Without Creating Artifacts](/courses/dsp-radar/modules/10-decimate-and-interpolate-without-creating-artifacts).
