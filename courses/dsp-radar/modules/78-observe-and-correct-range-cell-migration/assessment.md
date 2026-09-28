### DSP-F78 · Audit coherent imaging and passive processing

**Competency DSP-C78:** A target moves across fast-range cells as its slant range changes. Sampling each row at r + DeltaR aligns the envelope while preserving the phase needed for coherent focusing.

**Builds on:** [P30 — Measure Range from Echo Delay](/courses/dsp-radar/modules/30-measure-range-from-echo-delay); [P75 — Build SAR Phase-History Intuition](/courses/dsp-radar/modules/75-build-sar-phase-history-intuition); [P76 — Perform SAR Range Compression](/courses/dsp-radar/modules/76-perform-sar-range-compression); [P77 — Focus SAR with Backprojection](/courses/dsp-radar/modules/77-focus-sar-with-backprojection).

**Predict and investigate.** Increase aperture_length_m and squint_offset_m separately. Use ridge and aligned to determine the interpolation direction before comparing the final image.

**Evidence to keep.** Write your prediction before manipulating controls. Record baseline settings, one-variable comparisons, the plotted quantity and its units, and the result after restoring the same settings. Use the existing lesson's named failure and recovery:

- Trigger: Enable broken_mode at baseline controls.
- Diagnose: The wrong-sign shift samples r - DeltaR. At the reviewed baseline it nearly doubles ridge migration and spreads the coherent profile.
- Recover: Disable the failure to repeat correct-sign interpolation from unchanged complex rows. Path-following image formation uses the same known geometry; it is not blind motion estimation.

**Browser recovery.** Turn **Enable the named failure** on to capture the fault, then off while holding the other controls at the same values. Compare the recovered evidence with that same-settings healthy run. Use **Reset parameters** to restore the original baseline.

**Explain the relation.** `aligned(r)=raw(r+Delta R)`. Relate each symbol to a displayed quantity and distinguish samples, seconds, frequency, phase and any power normalization that applies.

**Check your reasoning.** Sampling raw data at r+Delta R aligns the migrating response under the declared shift convention. Reversing the sign moves energy farther away. Envelope alignment still needs coherent phase compensation for focusing.

**Limit the claim.** Interpolation and finite support limit recovery. Data shifted outside the observed range window cannot be reconstructed by alignment alone.

**Completion standard.** A satisfactory explanation connects a prediction to measured browser evidence, uses the correct units, explains the failure causally, and identifies a model limit. Merely reproducing a favorable plot or reading this answer is not an assessment pass. No learner score or completion is stored.

Continue the domain assessment at [P83 — Compare Range-Doppler Processing with a Small STAP Processor](/courses/dsp-radar/modules/83-compare-range-doppler-processing-with-a-small-stap-processor).
