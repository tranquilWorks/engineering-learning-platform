### DSP-F69 · Resolve FMCW signs, timing and motion

**Competency DSP-C69:** An 80 MHz sampled,40 us centered chirp returns after tau=2R/c. Only valid overlap is mixed as Tx conj(Rx), giving positive beat S tau. A Hann window and 65536-point FFT interpolate the beat; zero-padding does not improve the physical c/(2B) resolution.

**Builds on:** [P17 — Perform Complex Downconversion by Hand](/courses/dsp-radar/modules/17-perform-complex-downconversion-by-hand); [P22 — Relate FM Deviation to Bandwidth](/courses/dsp-radar/modules/22-relate-fm-deviation-to-bandwidth); [P30 — Measure Range from Echo Delay](/courses/dsp-radar/modules/30-measure-range-from-echo-delay); [P31 — Separate Range Resolution from Range Accuracy](/courses/dsp-radar/modules/31-separate-range-resolution-from-range-accuracy).

**Predict and investigate.** Double target_range_m or bandwidth_mhz separately. Use mixer and conversion to predict the beat and distinguish range-bin spacing from bandwidth-limited resolution.

**Evidence to keep.** Write your prediction before manipulating controls. Record baseline settings, one-variable comparisons, the plotted quantity and its units, and the result after restoring the same settings. Use the existing lesson's named failure and recovery:

- Trigger: Enable broken_mode at baseline controls.
- Diagnose: Using R=c fbeat/S omits round-trip propagation and doubles the same estimate.
- Recover: Restore R=c fbeat/(2S) without changing the observed beat.

**Browser recovery.** Turn **Enable the named failure** on to capture the fault, then off while holding the other controls at the same values. Compare the recovered evidence with that same-settings healthy run. Use **Reset parameters** to restore the original baseline.

**Explain the relation.** `f_beat=S tau and R=c tau/2 for the stationary TX times conjugate(RX) convention`. Relate each symbol to a displayed quantity and distinguish samples, seconds, frequency, phase and any power normalization that applies.

**Check your reasoning.** Delay is twice range divided by propagation speed; chirp slope converts delay into signed beat frequency under the chosen mixer order. Increasing slope changes the range-to-frequency mapping, while the valid overlap limits the sampled record.

**Limit the claim.** The stationary single-target formula neglects Doppler. Sign, overlap and beat aliasing must be checked before interpreting a range estimate.

**Completion standard.** A satisfactory explanation connects a prediction to measured browser evidence, uses the correct units, explains the failure causally, and identifies a model limit. Merely reproducing a favorable plot or reading this answer is not an assessment pass. No learner score or completion is stored.

Continue the domain assessment at [P74 — Create a Micro-Doppler Spectrogram](/courses/dsp-radar/modules/74-create-a-micro-doppler-spectrogram).
