### DSP-F79 · Audit coherent imaging and passive processing

**Competency DSP-C79:** Frequency sums set range resolution; phase-coherent aperture sums set cross-range resolution. Hamming weighting lowers sidelobes at the cost of a wider mainlobe.

**Builds on:** [P12 — Separate Leakage from Noise](/courses/dsp-radar/modules/12-separate-leakage-from-noise); [P31 — Separate Range Resolution from Range Accuracy](/courses/dsp-radar/modules/31-separate-range-resolution-from-range-accuracy); [P62 — Plot Array Factor, Beamwidth, and Grating Lobes](/courses/dsp-radar/modules/62-plot-array-factor-beamwidth-and-grating-lobes); [P77 — Focus SAR with Backprojection](/courses/dsp-radar/modules/77-focus-sar-with-backprojection); [P78 — Observe and Correct Range-Cell Migration](/courses/dsp-radar/modules/78-observe-and-correct-range-cell-migration).

**Predict and investigate.** Change bandwidth_mhz and aperture_length_m separately. Use range and cross to assign each resolution change, then inspect sampling for ambiguity.

**Evidence to keep.** Write your prediction before manipulating controls. Record baseline settings, one-variable comparisons, the plotted quantity and its units, and the result after restoring the same settings. Use the existing lesson's named failure and recovery:

- Trigger: Enable broken_mode at baseline controls.
- Diagnose: The named 5 m platform spacing undersamples aperture phase, creating near-unity cross-range copies about 3 m apart. A narrow mainlobe alone does not establish unambiguous localization.
- Recover: Disable the failure to recompute the same seeded scene with dense 0.25 m aperture sampling. This is reacquisition with a reviewed sampling grid, not recovery of missing information from the sparse image.

**Browser recovery.** Turn **Enable the named failure** on to capture the fault, then off while holding the other controls at the same values. Compare the recovered evidence with that same-settings healthy run. Use **Reset parameters** to restore the original baseline.

**Explain the relation.** `delta_cross_range approximately lambda R/(2 aperture_length)`. Relate each symbol to a displayed quantity and distinguish samples, seconds, frequency, phase and any power normalization that applies.

**Check your reasoning.** Bandwidth controls the range response; aperture extent controls cross-range discrimination. Hamming weighting reduces sidelobes but widens the mainlobe. Sparse spatial sampling can yield a sharp aliased peak that is not a unique image.

**Limit the claim.** Nominal resolution formulas assume the stated geometry and adequate sampling. Report the measured criterion and sidelobes alongside width.

**Completion standard.** A satisfactory explanation connects a prediction to measured browser evidence, uses the correct units, explains the failure causally, and identifies a model limit. Merely reproducing a favorable plot or reading this answer is not an assessment pass. No learner score or completion is stored.

Continue the domain assessment at [P83 — Compare Range-Doppler Processing with a Small STAP Processor](/courses/dsp-radar/modules/83-compare-range-doppler-processing-with-a-small-stap-processor).
