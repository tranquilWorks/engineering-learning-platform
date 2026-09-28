### DSP-F66 · Defend an array estimate under mismatch

**Competency DSP-C66:** Ten sensors estimate R, split its Hermitian eigenspaces, and scan 1/||E_n^H a||². The independent sources share fixed private waveforms/noise across sweeps; two separated local peaks are selected without truth.

**Builds on:** [P27 — Use Monte Carlo Trials Instead of One Lucky Run](/courses/dsp-radar/modules/27-use-monte-carlo-trials-instead-of-one-lucky-run); [P61 — See Phase Steering in a Uniform Linear Array](/courses/dsp-radar/modules/61-see-phase-steering-in-a-uniform-linear-array); [P63 — Implement Conventional Delay-and-Sum Beamforming](/courses/dsp-radar/modules/63-implement-conventional-delay-and-sum-beamforming); [P65 — Use MVDR/Capon Adaptive Beamforming](/courses/dsp-radar/modules/65-use-mvdr-capon-adaptive-beamforming).

**Predict and investigate.** Reduce source_separation_deg and source_snr_db. Use eigenvalues, spectrum and count to explain how coherence and an incorrect source count change the noise-subspace interpretation.

**Evidence to keep.** Write your prediction before manipulating controls. Record baseline settings, one-variable comparisons, the plotted quantity and its units, and the result after restoring the same settings. Use the existing lesson's named failure and recovery:

- Trigger: Enable broken_mode at baseline controls.
- Diagnose: Coherent sources collapse the second signal eigenvalue; assuming two independent sources can create false MUSIC directions.
- Recover: Average four overlapping seven-element subarray covariances on unchanged coherent data. This restores rank at the cost of aperture. Missing peak sets use an explicit 80-degree penalty; counts expose incompleteness. Toggle off restores selected independent-source data.

**Browser recovery.** Turn **Enable the named failure** on to capture the fault, then off while holding the other controls at the same values. Compare the recovered evidence with that same-settings healthy run. Use **Reset parameters** to restore the original baseline.

**Explain the relation.** `P_MUSIC(theta)=1/(a^H En En^H a)`. Relate each symbol to a displayed quantity and distinguish samples, seconds, frequency, phase and any power normalization that applies.

**Check your reasoning.** MUSIC relies on separating signal and noise subspaces. Coherent sources reduce covariance rank; spatial smoothing can restore rank while sacrificing effective aperture. Specifying the wrong source count changes the projector.

**Limit the claim.** A narrow pseudospectrum peak is not a calibrated confidence interval or an unconditional resolution guarantee.

**Completion standard.** A satisfactory explanation connects a prediction to measured browser evidence, uses the correct units, explains the failure causally, and identifies a model limit. Merely reproducing a favorable plot or reading this answer is not an assessment pass. No learner score or completion is stored.

Continue the domain assessment at [P68 — Build an Introductory STAP Clutter-Ridge Experiment](/courses/dsp-radar/modules/68-build-an-introductory-stap-clutter-ridge-experiment).
