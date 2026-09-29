### DSP-F77 · Audit coherent imaging and passive processing

**Competency DSP-C77:** For each image pixel, predict slant range, interpolate the complex range row, cancel its two-way phase, and sum aperture looks. More coherent looks narrow the cross-range response.

**Builds on:** [P08 — Use Correlation to Find a Hidden Pattern](/courses/dsp-radar/modules/08-use-correlation-to-find-a-hidden-pattern); [P75 — Build SAR Phase-History Intuition](/courses/dsp-radar/modules/75-build-sar-phase-history-intuition); [P76 — Perform SAR Range Compression](/courses/dsp-radar/modules/76-perform-sar-range-compression).

**Predict and investigate.** Compare aperture_looks and then introduce path_error_m. Use cuts and phase to explain why a small path error can reduce focus despite a similar range envelope.

**Evidence to keep.** Write your prediction before manipulating controls. Record baseline settings, one-variable comparisons, the plotted quantity and its units, and the result after restoring the same settings. Use the existing lesson's named failure and recovery:

- Trigger: Enable broken_mode at baseline controls.
- Diagnose: The named failure assumes a sinusoidal 10 mm ground-range path error. Misaligned phasors reduce the true-pixel gain despite unchanged measurements.
- Recover: Disable the failure and restore path error to 0 m; refocus the retained complex input with correct geometry.

**Browser recovery.** Turn **Enable the named failure** on to capture the fault, then off while holding the other controls at the same values. Compare the recovered evidence with that same-settings healthy run. Use **Reset parameters** to restore the original baseline.

**Explain the relation.** `image(pixel)=sum_looks sample(range_to_pixel) exp(j 4 pi R/lambda)`. Relate each symbol to a displayed quantity and distinguish samples, seconds, frequency, phase and any power normalization that applies.

**Check your reasoning.** Backprojection samples the range response for each hypothesized pixel and compensates its round-trip phase before summation. Millimetre-scale path errors can produce substantial phase error at short wavelength and spoil coherent gain.

**Limit the claim.** Separate aperture extent, sampling density and image-grid spacing; adding grid pixels is not equivalent to adding coherent measurements.

**Completion standard.** A satisfactory explanation connects a prediction to measured browser evidence, uses the correct units, explains the failure causally, and identifies a model limit. Merely reproducing a favorable plot or reading this answer is not an assessment pass. No learner score or completion is stored.

Continue the domain assessment at [P83 — Compare Range-Doppler Processing with a Small STAP Processor](/courses/dsp-radar/modules/83-compare-range-doppler-processing-with-a-small-stap-processor).
