### DSP-F81 · Audit coherent imaging and passive processing

**Competency DSP-C81:** Target rotation projects scatterers onto changing range directions. Range compression precedes the signed angle FFT; translation correction removes both envelope migration and carrier phase.

**Builds on:** [P36 — Measure Doppler from Pulse-to-Pulse Phase](/courses/dsp-radar/modules/36-measure-doppler-from-pulse-to-pulse-phase); [P74 — Create a Micro-Doppler Spectrogram](/courses/dsp-radar/modules/74-create-a-micro-doppler-spectrogram); [P77 — Focus SAR with Backprojection](/courses/dsp-radar/modules/77-focus-sar-with-backprojection); [P80 — Inject SAR Motion Error and Apply Autofocus](/courses/dsp-radar/modules/80-inject-sar-motion-error-and-apply-autofocus).

**Predict and investigate.** Change angular_aperture_deg and rotation_rate_deg_s separately. Use aligned_profiles and image to distinguish envelope alignment, phase correction and cross-range scaling.

**Evidence to keep.** Write your prediction before manipulating controls. Record baseline settings, one-variable comparisons, the plotted quantity and its units, and the result after restoring the same settings. Use the existing lesson's named failure and recovery:

- Trigger: Enable broken_mode at baseline controls.
- Diagnose: Omitting the known centroid translation correction spreads energy and shifts the apparent shape. A faster rotation alone cannot replace alignment.
- Recover: Disable the failure and multiply the original frequency history by the opposite translational phase. The small-angle cross-range approximation and uniform aspect sampling remain explicit assumptions.

**Browser recovery.** Turn **Enable the named failure** on to capture the fault, then off while holding the other controls at the same values. Compare the recovered evidence with that same-settings healthy run. Use **Reset parameters** to restore the original baseline.

**Explain the relation.** `x=-lambda f_D/(2 omega) near broadside, with omega in rad/s and the retained receive-phase convention`. Relate each symbol to a displayed quantity and distinguish samples, seconds, frequency, phase and any power normalization that applies.

**Check your reasoning.** Angular extent controls accumulated aspect diversity, while rotation rate changes dwell time and Doppler-to-cross-range conversion. At identical angular support this ideal angle-domain image need not change just because rotation is faster. Translation affects both range envelope and phase; correcting only one can leave a blurred or misplaced image.

**Limit the claim.** A rigid rotating point-scatterer model and known rotation convention bound the interpretation. Unknown rotation scale creates cross-range ambiguity.

**Completion standard.** A satisfactory explanation connects a prediction to measured browser evidence, uses the correct units, explains the failure causally, and identifies a model limit. Merely reproducing a favorable plot or reading this answer is not an assessment pass. No learner score or completion is stored.

Continue the domain assessment at [P83 — Compare Range-Doppler Processing with a Small STAP Processor](/courses/dsp-radar/modules/83-compare-range-doppler-processing-with-a-small-stap-processor).
