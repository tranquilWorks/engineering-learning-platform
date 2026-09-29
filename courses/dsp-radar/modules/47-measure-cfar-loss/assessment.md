### DSP-F47 · Audit a detector's false-alarm claim

**Competency DSP-C47:** CFAR loss is a horizontal SNR difference at the same Pd and Pfa. Finite reference counts make the threshold uncertain; the disclosed monotone envelope only permits inversion of finite-trial curves.

**Builds on:** [P28 — Connect Thresholds to ROC Curves and Estimator Limits](/courses/dsp-radar/modules/28-connect-thresholds-to-roc-curves-and-estimator-limits); [P44 — Build an Empirical Radar ROC Curve](/courses/dsp-radar/modules/44-build-an-empirical-radar-roc-curve); [P45 — Implement 1-D Cell-Averaging CFAR](/courses/dsp-radar/modules/45-implement-1-d-cell-averaging-cfar).

**Predict and investigate.** Compare training_count values while keeping design_pfa and the detection-probability target fixed. Explain which curves actually support a CFAR-loss claim.

**Evidence to keep.** Write your prediction before manipulating controls. Record baseline settings, one-variable comparisons, the plotted quantity and its units, and the result after restoring the same settings. Use the existing lesson's named failure and recovery:

- Trigger: Enable broken_mode at baseline controls.
- Diagnose: Reusing −ln(Pfa) on an estimated mean gives a smaller apparent SNR penalty by increasing actual false alarms. It is not an equal-Pfa comparison.
- Recover: Restore N(Pfa^(−1/N)−1), keep paired CUT trials and independent references, and compare at Pd=.8. Disable the toggle to reproduce the properly calibrated selected curve.

**Browser recovery.** Turn **Enable the named failure** on to capture the fault, then off while holding the other controls at the same values. Compare the recovered evidence with that same-settings healthy run. Use **Reset parameters** to restore the original baseline.

**Explain the relation.** `CFAR_loss_dB=SNR_CFAR_dB-SNR_known_noise_dB at equal Pd,Pfa`. Relate each symbol to a displayed quantity and distinguish samples, seconds, frequency, phase and any power normalization that applies.

**Check your reasoning.** CFAR loss compares required SNR at equal Pd and Pfa with a known-noise reference. Finite training adds uncertainty; an apparently smaller SNR requirement achieved by relaxing false alarms is not lower CFAR loss.

**Limit the claim.** The calibration and fluctuating-target assumptions must match between detectors; a single scene's hit count is insufficient.

**Completion standard.** A satisfactory explanation connects a prediction to measured browser evidence, uses the correct units, explains the failure causally, and identifies a model limit. Merely reproducing a favorable plot or reading this answer is not an assessment pass. No learner score or completion is stored.

Continue the domain assessment at [P52 — Validate CFAR Pfa by Monte Carlo](/courses/dsp-radar/modules/52-validate-cfar-pfa-by-monte-carlo).
