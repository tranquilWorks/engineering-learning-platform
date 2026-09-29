### DSP-F42 · Audit a detector's false-alarm claim

**Competency DSP-C42:** Fast-time matched filtering separates range; the slow-time FFT separates signed velocity. Targets can share either coordinate and remain distinct in the two-dimensional map.

**Builds on:** [P11 — Make FFT Bins Concrete](/courses/dsp-radar/modules/11-make-fft-bins-concrete); [P12 — Separate Leakage from Noise](/courses/dsp-radar/modules/12-separate-leakage-from-noise); [P32 — Perform LFM Pulse Compression](/courses/dsp-radar/modules/32-perform-lfm-pulse-compression); [P37 — Build a Pulse-Doppler Data Matrix](/courses/dsp-radar/modules/37-build-a-pulse-doppler-data-matrix); [P40 — Compare Coherent and Noncoherent Integration](/courses/dsp-radar/modules/40-compare-coherent-and-noncoherent-integration).

**Predict and investigate.** Compare pulse_count=32 and 64, then alter hann_weight. Use the map to distinguish velocity-bin spacing, leakage and range resolution.

**Evidence to keep.** Write your prediction before manipulating controls. Record baseline settings, one-variable comparisons, the plotted quantity and its units, and the result after restoring the same settings. Use the existing lesson's named failure and recovery:

- Trigger: Enable broken_mode at baseline controls.
- Diagnose: FFT along fast time creates fast-time frequency, not Doppler. Relabeling pulse columns as velocity cannot repair it.
- Recover: Restore delay-corrected range compression, apply the selected slow-time window and FFT across pulse columns; disable the toggle for the exact selected map.

**Browser recovery.** Turn **Enable the named failure** on to capture the fault, then off while holding the other controls at the same values. Compare the recovered evidence with that same-settings healthy run. Use **Reset parameters** to restore the original baseline.

**Explain the relation.** `Delta v=lambda PRF/(2 Npulses)`. Relate each symbol to a displayed quantity and distinguish samples, seconds, frequency, phase and any power normalization that applies.

**Check your reasoning.** Longer coherent dwell refines Doppler spacing, while the range waveform remains unchanged. Slow-time tapering trades spectral sidelobes against width and coherent gain. Transforming the fast-time axis as Doppler produces the wrong physical interpretation.

**Limit the claim.** Finite target separations and window shape determine resolution; finer bins alone do not guarantee two separable peaks.

**Completion standard.** A satisfactory explanation connects a prediction to measured browser evidence, uses the correct units, explains the failure causally, and identifies a model limit. Merely reproducing a favorable plot or reading this answer is not an assessment pass. No learner score or completion is stored.

Continue the domain assessment at [P52 — Validate CFAR Pfa by Monte Carlo](/courses/dsp-radar/modules/52-validate-cfar-pfa-by-monte-carlo).
