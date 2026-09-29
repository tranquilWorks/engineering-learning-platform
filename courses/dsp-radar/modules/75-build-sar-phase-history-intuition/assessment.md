### DSP-F75 · Audit coherent imaging and passive processing

**Competency DSP-C75:** A 5 GHz antenna visits positions at.2m spacing. R=sqrt(1000²+(x-xt)²), delay=2R/c and phase=-4pi(R-1000)/lambda. A .6 m Gaussian envelope supplies the raw fast-time ridge. Candidate-path phase compensation coherently sums ridge samples; this is a single known-range illustration, not an image former.

**Builds on:** [P17 — Perform Complex Downconversion by Hand](/courses/dsp-radar/modules/17-perform-complex-downconversion-by-hand); [P30 — Measure Range from Echo Delay](/courses/dsp-radar/modules/30-measure-range-from-echo-delay); [P36 — Measure Doppler from Pulse-to-Pulse Phase](/courses/dsp-radar/modules/36-measure-doppler-from-pulse-to-pulse-phase).

**Predict and investigate.** Change target_cross_range_m and aperture_length_m separately. Use phase and focus to explain why similar magnitude envelopes can correspond to different coherent images.

**Evidence to keep.** Write your prediction before manipulating controls. Record baseline settings, one-variable comparisons, the plotted quantity and its units, and the result after restoring the same settings. Use the existing lesson's named failure and recovery:

- Trigger: Enable broken_mode at baseline controls.
- Diagnose: Taking magnitude preserves the delay ridge but erases aperture phase, so correct path compensation cannot align the data.
- Recover: Return to the unchanged complex ridge samples. Controls crop a fixed401x201 noise record when aperture changes, preserving nested measurements rather than regenerating noise.

**Browser recovery.** Turn **Enable the named failure** on to capture the fault, then off while holding the other controls at the same values. Compare the recovered evidence with that same-settings healthy run. Use **Reset parameters** to restore the original baseline.

**Explain the relation.** `phase_history=-4 pi R(aperture_position)/lambda`. Relate each symbol to a displayed quantity and distinguish samples, seconds, frequency, phase and any power normalization that applies.

**Check your reasoning.** Slant range sets a two-way phase history. Moving the target shifts the path geometry; extending the aperture adds phase diversity. Removing phase prevents coherent alignment even if the range-amplitude ridge still looks plausible.

**Limit the claim.** Image focus relies on the assumed path and geometry. This point-scatterer model omits extended-scene scattering and real navigation errors.

**Completion standard.** A satisfactory explanation connects a prediction to measured browser evidence, uses the correct units, explains the failure causally, and identifies a model limit. Merely reproducing a favorable plot or reading this answer is not an assessment pass. No learner score or completion is stored.

Continue the domain assessment at [P83 — Compare Range-Doppler Processing with a Small STAP Processor](/courses/dsp-radar/modules/83-compare-range-doppler-processing-with-a-small-stap-processor).
