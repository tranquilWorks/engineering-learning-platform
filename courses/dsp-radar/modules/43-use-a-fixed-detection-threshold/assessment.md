### DSP-F43 · Audit a detector's false-alarm claim

**Competency DSP-C43:** One absolute signed-amplitude threshold is calibrated for zero-mean Gaussian noise at RMS 1. Increasing noise or adding a pedestal changes its false-alarm rate; H0 and H1 counts use separate denominators.

**Builds on:** [P28 — Connect Thresholds to ROC Curves and Estimator Limits](/courses/dsp-radar/modules/28-connect-thresholds-to-roc-curves-and-estimator-limits); [P41 — Model Ground Clutter and Swerling Targets](/courses/dsp-radar/modules/41-model-ground-clutter-and-swerling-targets); [P42 — Create a Full Range-Doppler Map](/courses/dsp-radar/modules/42-create-a-full-range-doppler-map).

**Predict and investigate.** Double noise_rms without changing the threshold, then increase clutter_pedestal. Explain the native-unit crossing rate and why normalizing by the true RMS changes the experiment.

**Evidence to keep.** Write your prediction before manipulating controls. Record baseline settings, one-variable comparisons, the plotted quantity and its units, and the result after restoring the same settings. Use the existing lesson's named failure and recovery:

- Trigger: Enable broken_mode at baseline controls.
- Diagnose: Dividing by each true RMS silently changes the detector into an oracle-adaptive threshold. A flat Pfa curve would no longer demonstrate a fixed threshold.
- Recover: Restore the single threshold in native amplitude units. Disable the toggle to recover the selected noise/pedestal experiment; pedestal and RMS changes remain physically visible.

**Browser recovery.** Turn **Enable the named failure** on to capture the fault, then off while holding the other controls at the same values. Compare the recovered evidence with that same-settings healthy run. Use **Reset parameters** to restore the original baseline.

**Explain the relation.** `Pfa=P(native_amplitude>fixed_threshold | H0)`. Relate each symbol to a displayed quantity and distinguish samples, seconds, frequency, phase and any power normalization that applies.

**Check your reasoning.** A fixed amplitude threshold becomes less extreme as noise scale grows, so false alarms increase. An oracle rescaling tracks the true background and is no longer the same fixed-threshold detector.

**Limit the claim.** A stationary distribution underlies a fixed-threshold calibration; nonstationary clutter can invalidate that calibration without a coding error.

**Completion standard.** A satisfactory explanation connects a prediction to measured browser evidence, uses the correct units, explains the failure causally, and identifies a model limit. Merely reproducing a favorable plot or reading this answer is not an assessment pass. No learner score or completion is stored.

Continue the domain assessment at [P52 — Validate CFAR Pfa by Monte Carlo](/courses/dsp-radar/modules/52-validate-cfar-pfa-by-monte-carlo).
