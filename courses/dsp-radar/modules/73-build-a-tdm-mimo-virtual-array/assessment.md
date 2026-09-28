### DSP-F73 · Resolve FMCW signs, timing and motion

**Competency DSP-C73:** Two TX at 0/2 wavelengths and four RX at 0:.5:1.5 create eight TX+RX positions. Tx-conjugate processing has negative spatial and Doppler phase. A lag-one estimate across 80 us same-TX cycles measures Doppler; correcting the 40 us slot offset restores virtual-array coherence.

**Builds on:** [P36 — Measure Doppler from Pulse-to-Pulse Phase](/courses/dsp-radar/modules/36-measure-doppler-from-pulse-to-pulse-phase); [P61 — See Phase Steering in a Uniform Linear Array](/courses/dsp-radar/modules/61-see-phase-steering-in-a-uniform-linear-array); [P62 — Plot Array Factor, Beamwidth, and Grating Lobes](/courses/dsp-radar/modules/62-plot-array-factor-beamwidth-and-grating-lobes); [P70 — Create an FMCW Range-Doppler Map](/courses/dsp-radar/modules/70-create-an-fmcw-range-doppler-map).

**Predict and investigate.** Compare velocity_mps=0 and 10 before and after compensation. Use geometry and motion to explain virtual aperture and the phase error between TX slots.

**Evidence to keep.** Write your prediction before manipulating controls. Record baseline settings, one-variable comparisons, the plotted quantity and its units, and the result after restoring the same settings. Use the existing lesson's named failure and recovery:

- Trigger: Enable broken_mode at baseline controls.
- Diagnose: Treating the named 10 m/s TDM record as simultaneous lets motion phase masquerade as angle.
- Recover: Multiply each virtual channel by exp(+j2pi fd slot_time) using the same-TX estimate. Recovery reuses the noisy record and assumes one unaliased target Doppler; the reviewed speed range lies below same-TX Nyquist.

**Browser recovery.** Turn **Enable the named failure** on to capture the fault, then off while holding the other controls at the same values. Compare the recovered evidence with that same-settings healthy run. Use **Reset parameters** to restore the original baseline.

**Explain the relation.** `virtual_position=TX_position+RX_position`. Relate each symbol to a displayed quantity and distinguish samples, seconds, frequency, phase and any power normalization that applies.

**Check your reasoning.** TX plus RX positions define virtual spatial samples, but TDM samples them at different times. Target motion adds a slot-dependent Doppler phase; estimating Doppler across same-TX cycles supports compensation.

**Limit the claim.** The virtual-array interpretation assumes a coherent target model over the switching schedule. Acceleration and unresolved targets can invalidate simple correction.

**Completion standard.** A satisfactory explanation connects a prediction to measured browser evidence, uses the correct units, explains the failure causally, and identifies a model limit. Merely reproducing a favorable plot or reading this answer is not an assessment pass. No learner score or completion is stored.

Continue the domain assessment at [P74 — Create a Micro-Doppler Spectrogram](/courses/dsp-radar/modules/74-create-a-micro-doppler-spectrogram).
