### DSP-F76 · Audit coherent imaging and passive processing

**Competency DSP-C76:** A 240-sample LFM echo is inserted at each quantized delay without wrapping. Independent per-row linear matched filtering divides by 240 and subtracts 239 filter-delay samples from the axis. Three targets retain complex aperture phase. Bandwidth controls the waveform; pair spacing affects a separate noiseless equal-target demonstration.

**Builds on:** [P31 — Separate Range Resolution from Range Accuracy](/courses/dsp-radar/modules/31-separate-range-resolution-from-range-accuracy); [P32 — Perform LFM Pulse Compression](/courses/dsp-radar/modules/32-perform-lfm-pulse-compression); [P75 — Build SAR Phase-History Intuition](/courses/dsp-radar/modules/75-build-sar-phase-history-intuition).

**Predict and investigate.** Increase bandwidth_mhz at fixed pair_spacing_m. Use compressed and phase to show what range compression accomplishes and what still requires azimuth processing.

**Evidence to keep.** Write your prediction before manipulating controls. Record baseline settings, one-variable comparisons, the plotted quantity and its units, and the result after restoring the same settings. Use the existing lesson's named failure and recovery:

- Trigger: Enable broken_mode at baseline controls.
- Diagnose: Magnitude-only range history retains identical range ridges but replaces each aperture phase by zero, destroying later coherent azimuth processing.
- Recover: Recover the retained original complex range-compressed record; lost phase cannot be reconstructed from magnitude. This lesson performs range compression only, not azimuth focusing.

**Browser recovery.** Turn **Enable the named failure** on to capture the fault, then off while holding the other controls at the same values. Compare the recovered evidence with that same-settings healthy run. Use **Reset parameters** to restore the original baseline.

**Explain the relation.** `range_response_width approximately c/(2 B)`. Relate each symbol to a displayed quantity and distinguish samples, seconds, frequency, phase and any power normalization that applies.

**Check your reasoning.** The conjugate matched filter narrows the range response and its delay must be removed from the axis. Retaining complex phase allows later aperture focusing; taking magnitude at this stage discards information needed downstream.

**Limit the claim.** Range compression alone does not focus cross-range. A narrower range trace does not establish two-dimensional image resolution.

**Completion standard.** A satisfactory explanation connects a prediction to measured browser evidence, uses the correct units, explains the failure causally, and identifies a model limit. Merely reproducing a favorable plot or reading this answer is not an assessment pass. No learner score or completion is stored.

Continue the domain assessment at [P83 — Compare Range-Doppler Processing with a Small STAP Processor](/courses/dsp-radar/modules/83-compare-range-doppler-processing-with-a-small-stap-processor).
