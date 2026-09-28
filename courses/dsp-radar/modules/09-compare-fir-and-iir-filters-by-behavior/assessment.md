### DSP-F09 · Sample, identify and reconstruct

**Competency DSP-C09:** The pinned source develops this physical relationship from deterministic measurements.

**Builds on:** [P06 — Use an Impulse to Reveal a System](/courses/dsp-radar/modules/06-use-an-impulse-to-reveal-a-system); [P07 — Understand Convolution as Echo Addition](/courses/dsp-radar/modules/07-understand-convolution-as-echo-addition); [P08 — Use Correlation to Find a Hidden Pattern](/courses/dsp-radar/modules/08-use-correlation-to-find-a-hidden-pattern).

**Predict and investigate.** Change fir_taps and iir_q separately; compare frequency_behavior with time_behavior. Explain a case where a narrower response also rings longer.

**Evidence to keep.** Write your prediction before manipulating controls. Record baseline settings, one-variable comparisons, the plotted quantity and its units, and the result after restoring the same settings. Use the existing lesson's named failure and recovery:

- Trigger: Enable broken_mode.
- Diagnose: Move a resonator pole radius to 1.02 so its impulse envelope grows.
- Recover: Move the radius to 0.98 and verify a decaying response.

**Browser recovery.** Turn **Violate the central model assumption** on to capture the fault, then off while holding the other controls at the same values. Compare the recovered evidence with that same-settings healthy run. Use **Reset parameters** to restore the original baseline.

**Explain the relation.** `H(z)=B(z)/A(z)`. Relate each symbol to a displayed quantity and distinguish samples, seconds, frequency, phase and any power normalization that applies.

**Check your reasoning.** FIR support controls finite memory and typically its transition width. IIR poles encode continuing state; increasing resonance can lengthen settling. Similar magnitude responses need not have the same phase or transient response.

**Limit the claim.** A stable-looking short plot does not prove pole stability. A pole reaching the unit circle changes the long-time conclusion.

**Completion standard.** A satisfactory explanation connects a prediction to measured browser evidence, uses the correct units, explains the failure causally, and identifies a model limit. Merely reproducing a favorable plot or reading this answer is not an assessment pass. No learner score or completion is stored.

Continue the domain assessment at [P10 — Decimate and Interpolate Without Creating Artifacts](/courses/dsp-radar/modules/10-decimate-and-interpolate-without-creating-artifacts).
