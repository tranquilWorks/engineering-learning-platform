### DSP-F32 · Carry range and Doppler through a radar design

**Competency DSP-C32:** The conjugate-reversed chirp compresses long overlapping echoes. Bandwidth sets width; duration supplies energy. FsT and BT use different input-noise references.

**Builds on:** [P08 — Use Correlation to Find a Hidden Pattern](/courses/dsp-radar/modules/08-use-correlation-to-find-a-hidden-pattern); [P22 — Relate FM Deviation to Bandwidth](/courses/dsp-radar/modules/22-relate-fm-deviation-to-bandwidth); [P30 — Measure Range from Echo Delay](/courses/dsp-radar/modules/30-measure-range-from-echo-delay); [P31 — Separate Range Resolution from Range Accuracy](/courses/dsp-radar/modules/31-separate-range-resolution-from-range-accuracy).

**Predict and investigate.** Double bandwidth_mhz while fixing pulse_duration_us, then double duration at fixed bandwidth. Record compression width and the normalization used by duration_gain.

**Evidence to keep.** Write your prediction before manipulating controls. Record baseline settings, one-variable comparisons, the plotted quantity and its units, and the result after restoring the same settings. Use the existing lesson's named failure and recovery:

- Trigger: Enable broken_mode at baseline controls.
- Diagnose: A 0.55B replica leaves phase mismatch: the isolated peak loses height and broadens on the same reference scale.
- Recover: Disable the failure to use the exact transmitted replica and reproduce the baseline seeded record.

**Browser recovery.** Turn **Enable the named failure** on to capture the fault, then off while holding the other controls at the same values. Compare the recovered evidence with that same-settings healthy run. Use **Reset parameters** to restore the original baseline.

**Explain the relation.** `h[n]=conjugate(s[L-1-n])`. Relate each symbol to a displayed quantity and distinguish samples, seconds, frequency, phase and any power normalization that applies.

**Check your reasoning.** Bandwidth primarily sets compressed width; duration changes energy and time-bandwidth product under the declared amplitude convention. The conjugate time-reversed replica coherently aligns phase and differs fundamentally from an unconjugated copy.

**Limit the claim.** A processing-gain number is incomplete without input/output noise bandwidth and pulse-energy normalization.

**Completion standard.** A satisfactory explanation connects a prediction to measured browser evidence, uses the correct units, explains the failure causally, and identifies a model limit. Merely reproducing a favorable plot or reading this answer is not an assessment pass. No learner score or completion is stored.

Continue the domain assessment at [P40 — Compare Coherent and Noncoherent Integration](/courses/dsp-radar/modules/40-compare-coherent-and-noncoherent-integration).
