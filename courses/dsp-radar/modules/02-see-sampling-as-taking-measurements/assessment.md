### DSP-F02 · Sample, identify and reconstruct

**Competency DSP-C02:** Imagine a voltmeter that opens its eyes only at regularly spaced instants. For a continuous sinusoid \[ x(t)=A\cos(2\pi f_0t+\phi), \] a sampler with interval \(T_s=1/f_s\) stores \[ x[n]=x(nT_s)=A\cos\!\left(2\pi\frac{f_0}{f_s}n+\phi\right). \] The stored pair is the sample index (or its known time) and the measured amplitude. Nothing in that sequence directly records the path taken between two measurements. The baseline's dense curve is therefore a reference used by the experiment, not extra information available to the sampler.

**Builds on:** [P01 — Build a Sinusoid and a Complex Phasor](/courses/dsp-radar/modules/01-build-a-sinusoid-and-a-complex-phasor).

**Predict and investigate.** Change sample_rate_hz while keeping the analog signal fixed, then change clock_offset_samples. Identify which change alters sample spacing and which changes the sampling phase in measurements.

**Evidence to keep.** Write your prediction before manipulating controls. Record baseline settings, one-variable comparisons, the plotted quantity and its units, and the result after restoring the same settings. Use the existing lesson's named failure and recovery:

- Trigger: Enable broken_mode.
- Diagnose: Force 7 Hz under a 12 Sa/s clock so the reflected 5 Hz and high 19 Hz candidates agree at every measurement.
- Recover: Restore the declared 80 Sa/s bandlimited measurement model.

**Browser recovery.** Turn **Violate the central model assumption** on to capture the fault, then off while holding the other controls at the same values. Compare the recovered evidence with that same-settings healthy run. Use **Reset parameters** to restore the original baseline.

**Explain the relation.** `Ts=1/fs; x[n]=x(n Ts+t0)`. Relate each symbol to a displayed quantity and distinguish samples, seconds, frequency, phase and any power normalization that applies.

**Check your reasoning.** Rate changes the grid spacing; offset moves the grid relative to the waveform. More drawn connecting lines do not provide measurements between sample instants.

**Limit the claim.** An interpolated display is a reconstruction assumption, not an independent observation of the analog waveform.

**Completion standard.** A satisfactory explanation connects a prediction to measured browser evidence, uses the correct units, explains the failure causally, and identifies a model limit. Merely reproducing a favorable plot or reading this answer is not an assessment pass. No learner score or completion is stored.

Continue the domain assessment at [P10 — Decimate and Interpolate Without Creating Artifacts](/courses/dsp-radar/modules/10-decimate-and-interpolate-without-creating-artifacts).
