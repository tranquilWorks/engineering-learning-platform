### DSP-F39 · Carry range and Doppler through a radar design

**Competency DSP-C39:** A two-pulse canceller nulls fd=m PRF. Separate 4.0 and 5.3 kHz dwells move nonzero blind speeds; their normalized magnitudes are fused by maximum, not complex addition.

**Builds on:** [P35 — Create Unambiguous-Range Aliasing](/courses/dsp-radar/modules/35-create-unambiguous-range-aliasing); [P38 — Implement a Two-Pulse and Three-Pulse MTI Canceller](/courses/dsp-radar/modules/38-implement-a-two-pulse-and-three-pulse-mti-canceller).

**Predict and investigate.** Use a diverse secondary_prf_khz and then an equal-PRF comparison. Explain which primary blind-speed targets can be recovered and which common null remains.

**Evidence to keep.** Write your prediction before manipulating controls. Record baseline settings, one-variable comparisons, the plotted quantity and its units, and the result after restoring the same settings. Use the existing lesson's named failure and recovery:

- Trigger: Enable broken_mode at baseline controls.
- Diagnose: Using 4.0 kHz twice duplicates the same blind-speed holes. A repeated observation supplies no PRF diversity.
- Recover: Disable the failure and select 5.3 kHz for the primary first-blind-speed target. The zero-velocity null and possible shared nonzero nulls remain.

**Browser recovery.** Turn **Enable the named failure** on to capture the fault, then off while holding the other controls at the same values. Compare the recovered evidence with that same-settings healthy run. Use **Reset parameters** to restore the original baseline.

**Explain the relation.** `v_blind=k lambda PRF/2`. Relate each symbol to a displayed quantity and distinguish samples, seconds, frequency, phase and any power normalization that applies.

**Check your reasoning.** Blind speeds occur where pulse-to-pulse phase increments are integer turns. Different PRFs move the nonzero nulls, while repeated identical PRF dwells do not add the needed diversity. Zero Doppler remains a shared cancellation null.

**Limit the claim.** Combining detections from multiple dwells does not by itself solve every ambiguity or establish a joint false-alarm rate.

**Completion standard.** A satisfactory explanation connects a prediction to measured browser evidence, uses the correct units, explains the failure causally, and identifies a model limit. Merely reproducing a favorable plot or reading this answer is not an assessment pass. No learner score or completion is stored.

Continue the domain assessment at [P40 — Compare Coherent and Noncoherent Integration](/courses/dsp-radar/modules/40-compare-coherent-and-noncoherent-integration).
