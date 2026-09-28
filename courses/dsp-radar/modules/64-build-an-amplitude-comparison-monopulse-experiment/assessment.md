### DSP-F64 · Defend an array estimate under mismatch

**Competency DSP-C64:** Phase-align squinted receive beams at boresight, form Sigma and Delta, and invert a monotone local ratio calibration. The sum guard, valid count and clipping count expose the estimator limits.

**Builds on:** [P28 — Connect Thresholds to ROC Curves and Estimator Limits](/courses/dsp-radar/modules/28-connect-thresholds-to-roc-curves-and-estimator-limits); [P61 — See Phase Steering in a Uniform Linear Array](/courses/dsp-radar/modules/61-see-phase-steering-in-a-uniform-linear-array); [P62 — Plot Array Factor, Beamwidth, and Grating Lobes](/courses/dsp-radar/modules/62-plot-array-factor-beamwidth-and-grating-lobes).

**Predict and investigate.** Change beam_squint_deg, then receiver_snr_db. Use calibration and sum_guard to decide which ratio samples support an angle estimate.

**Evidence to keep.** Write your prediction before manipulating controls. Record baseline settings, one-variable comparisons, the plotted quantity and its units, and the result after restoring the same settings. Use the existing lesson's named failure and recovery:

- Trigger: Enable broken_mode at baseline controls.
- Diagnose: Unknown right-channel gain 1.12 gives a nonzero angle for a noiseless boresight target. This named mismatch scene is separate from the selected noisy 2-degree target.
- Recover: Divide the right channel by the measured gain on unchanged boresight data. Disable the toggle for exact selected noisy-scene recovery. Calibration is local to +/-4 degrees; clipping is not evidence of accuracy outside that sector.

**Browser recovery.** Turn **Enable the named failure** on to capture the fault, then off while holding the other controls at the same values. Compare the recovered evidence with that same-settings healthy run. Use **Reset parameters** to restore the original baseline.

**Explain the relation.** `ratio=Delta/Sigma; theta approximately ratio/local_slope`. Relate each symbol to a displayed quantity and distinguish samples, seconds, frequency, phase and any power normalization that applies.

**Check your reasoning.** The difference-to-sum slope provides local angle sensitivity, but division by a small sum channel is unstable. Squint changes sensitivity and received sum power; gain mismatch can create angle bias even at high SNR.

**Limit the claim.** The linear calibration is local and bounded. Extrapolating its slope beyond the supported region invents accuracy.

**Completion standard.** A satisfactory explanation connects a prediction to measured browser evidence, uses the correct units, explains the failure causally, and identifies a model limit. Merely reproducing a favorable plot or reading this answer is not an assessment pass. No learner score or completion is stored.

Continue the domain assessment at [P68 — Build an Introductory STAP Clutter-Ridge Experiment](/courses/dsp-radar/modules/68-build-an-introductory-stap-clutter-ridge-experiment).
