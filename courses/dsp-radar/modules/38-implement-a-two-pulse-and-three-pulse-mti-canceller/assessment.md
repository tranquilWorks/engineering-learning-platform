### DSP-F38 · Carry range and Doppler through a radar design

**Competency DSP-C38:** [1,-1] and [1,-2,1] operate across coherent pulse columns. Stationary clutter cancels, while white-noise power grows by two and six. Valid outputs have N-1 and N-2 looks.

**Builds on:** [P09 — Compare FIR and IIR Filters by Behavior](/courses/dsp-radar/modules/09-compare-fir-and-iir-filters-by-behavior); [P36 — Measure Doppler from Pulse-to-Pulse Phase](/courses/dsp-radar/modules/36-measure-doppler-from-pulse-to-pulse-phase); [P37 — Build a Pulse-Doppler Data Matrix](/courses/dsp-radar/modules/37-build-a-pulse-doppler-data-matrix).

**Predict and investigate.** Compare the two-pulse and three-pulse outputs for slow_target_velocity_mps, then change prf_khz. Explain the benefit and cost of an additional difference.

**Evidence to keep.** Write your prediction before manipulating controls. Record baseline settings, one-variable comparisons, the plotted quantity and its units, and the result after restoring the same settings. Use the existing lesson's named failure and recovery:

- Trigger: Enable broken_mode at baseline controls.
- Diagnose: The failure differences neighboring range rows. Clutter varies across range, so its edges survive and the output has the wrong shape.
- Recover: Disable the failure to restore slow-time subtraction, correct output axes and the original seeded scene.

**Browser recovery.** Turn **Enable the named failure** on to capture the fault, then off while holding the other controls at the same values. Compare the recovered evidence with that same-settings healthy run. Use **Reset parameters** to restore the original baseline.

**Explain the relation.** `H2(z)=1-z^-1; H3(z)=(1-z^-1)^2`. Relate each symbol to a displayed quantity and distinguish samples, seconds, frequency, phase and any power normalization that applies.

**Check your reasoning.** Successive slow-time differences suppress DC clutter and produce progressively higher-order low-Doppler nulls. They also attenuate slow targets and amplify independent white noise according to squared tap weights.

**Limit the claim.** Subtracting adjacent range cells is a different operation. Normalization is needed before comparing target power or output SNR across cancellers.

**Completion standard.** A satisfactory explanation connects a prediction to measured browser evidence, uses the correct units, explains the failure causally, and identifies a model limit. Merely reproducing a favorable plot or reading this answer is not an assessment pass. No learner score or completion is stored.

Continue the domain assessment at [P40 — Compare Coherent and Noncoherent Integration](/courses/dsp-radar/modules/40-compare-coherent-and-noncoherent-integration).
