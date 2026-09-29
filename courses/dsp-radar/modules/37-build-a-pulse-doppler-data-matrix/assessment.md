### DSP-F37 · Carry range and Doppler through a radar design

**Competency DSP-C37:** Three separable range-envelope × slow-time-phasor components form a 256×32 complex matrix. The captured range span is shorter than the PRF ambiguity interval.

**Builds on:** [P30 — Measure Range from Echo Delay](/courses/dsp-radar/modules/30-measure-range-from-echo-delay); [P32 — Perform LFM Pulse Compression](/courses/dsp-radar/modules/32-perform-lfm-pulse-compression); [P36 — Measure Doppler from Pulse-to-Pulse Phase](/courses/dsp-radar/modules/36-measure-doppler-from-pulse-to-pulse-phase).

**Predict and investigate.** Change middle_target_range_m and middle_velocity_mps separately. Identify which data-matrix axis and phase history change.

**Evidence to keep.** Write your prediction before manipulating controls. Record baseline settings, one-variable comparisons, the plotted quantity and its units, and the result after restoring the same settings. Use the existing lesson's named failure and recovery:

- Trigger: Enable broken_mode at baseline controls.
- Diagnose: Taking magnitude of the matrix preserves target-looking range peaks but destroys the middle target's Doppler phase.
- Recover: Disable the failure to restore the complex matrix, row/column meaning and exact noise realization.

**Browser recovery.** Turn **Enable the named failure** on to capture the fault, then off while holding the other controls at the same values. Compare the recovered evidence with that same-settings healthy run. Use **Reset parameters** to restore the original baseline.

**Explain the relation.** `Delta R=c/(2 fs) (m); Delta v=lambda PRF/(2 Npulses) (m/s); x[fast_sample,pulse]`. Relate each symbol to a displayed quantity and distinguish samples, seconds, frequency, phase and any power normalization that applies.

**Check your reasoning.** Range moves the echo along fast-time samples; velocity changes coherent phase along pulse index. A slow-time FFT belongs along the pulse dimension, while waveform delay and compression determine the range response.

**Limit the claim.** The matrix is a finite observation. Its displayed range span, range resolution and PRF ambiguity interval are different quantities.

**Completion standard.** A satisfactory explanation connects a prediction to measured browser evidence, uses the correct units, explains the failure causally, and identifies a model limit. Merely reproducing a favorable plot or reading this answer is not an assessment pass. No learner score or completion is stored.

Continue the domain assessment at [P40 — Compare Coherent and Noncoherent Integration](/courses/dsp-radar/modules/40-compare-coherent-and-noncoherent-integration).
