### DSP-F52 · Audit a detector's false-alarm claim

**Competency DSP-C52:** Count false alarms from independent H0 trials and report a Wilson interval. Finite-N calibration matches iid exponential-power theory; correlated Gaussian and cellwise lognormal texture violate that model.

**Builds on:** [P27 — Use Monte Carlo Trials Instead of One Lucky Run](/courses/dsp-radar/modules/27-use-monte-carlo-trials-instead-of-one-lucky-run); [P44 — Build an Empirical Radar ROC Curve](/courses/dsp-radar/modules/44-build-an-empirical-radar-roc-curve); [P45 — Implement 1-D Cell-Averaging CFAR](/courses/dsp-radar/modules/45-implement-1-d-cell-averaging-cfar); [P51 — Stress CFAR with Clutter Edges, Sidelobes, and Multiple Targets](/courses/dsp-radar/modules/51-stress-cfar-with-clutter-edges-sidelobes-and-multiple-targets).

**Predict and investigate.** Compare the iid empirical interval with the requested design_pfa, then inspect correlated and textured cases. Explain why the exact iid formula and a finite estimate need not coincide.

**Evidence to keep.** Write your prediction before manipulating controls. Record baseline settings, one-variable comparisons, the plotted quantity and its units, and the result after restoring the same settings. Use the existing lesson's named failure and recovery:

- Trigger: Enable broken_mode at baseline controls.
- Diagnose: Using −ln(Pfa) on a finite reference mean raises actual Pfa. A small or zero count is also not evidence of zero operational risk.
- Recover: Restore N(Pfa^(−1/N)−1), retain all 200000 independent trials and the interval, and disclose the background model. Disable the toggle for exact finite-N replay.

**Browser recovery.** Turn **Enable the named failure** on to capture the fault, then off while holding the other controls at the same values. Compare the recovered evidence with that same-settings healthy run. Use **Reset parameters** to restore the original baseline.

**Explain the relation.** `Pfa_hat=false_alarms/N_independent_H0`. Relate each symbol to a displayed quantity and distinguish samples, seconds, frequency, phase and any power normalization that applies.

**Check your reasoning.** Independent H0 trials support a binomial uncertainty calculation; an empirical rate can differ from the design point within its interval. Correlation or texture changes the reference distribution and may cause systematic deviations.

**Limit the claim.** Confidence coverage refers to repeated experiments under assumptions. One interval containing the target rate does not prove a detector is universally calibrated.

**Completion standard.** A satisfactory explanation connects a prediction to measured browser evidence, uses the correct units, explains the failure causally, and identifies a model limit. Merely reproducing a favorable plot or reading this answer is not an assessment pass. No learner score or completion is stored.

Continue the domain assessment at [P52 — Validate CFAR Pfa by Monte Carlo](/courses/dsp-radar/modules/52-validate-cfar-pfa-by-monte-carlo).

### Cumulative assessment DSP-A05 — Audit a detector's false-alarm claim

Choose and assess adaptive detection statistics with explicit training, valid-cell and finite-trial assumptions.

**Evidence portfolio.** Work through the tasks below using the linked laboratories. Keep predictions, settings, dimensioned observations, failure diagnoses and recoveries together.

1. P41–P44: identify target fluctuation and background assumptions, then show how a fixed threshold responds to changed native noise/clutter scale. Translate a probability into an expected searched-cell count and distinguish that count from reports.
2. P45–P49: verify common-power scaling invariance, guard/training tradeoffs, equal-Pd/Pfa CFAR loss, and separately calibrated CA/GO/SO/OS behavior. Explain an OS rank's N-k strong-outlier capacity.
3. P50–P51: calculate the two-dimensional training-ring size and label untestable border cells separately from misses. Diagnose a target sidelobe crossing, a true H0 crossing and a masked target from their reference statistics.
4. P52: reset training_count=24 and design_pfa=0.001. Record active_alpha, active_alarm_count, active_measured_pfa, active_theoretical_pfa, wilson_lower and wilson_upper. Compare correlated_pfa and textured_pfa, then enable and recover broken_mode.

**Assessment rubric.** All four criteria must be supported by your recorded evidence; a missing criterion means revise that part of the explanation.

- CUT, guard, training and valid-cell denominators are explicit; linear power averaging and statistic-specific calibration are correct.
- The same requested Pfa is not presented as a guarantee in a nonhomogeneous or correlated scene.
- Detector choice explains both a benefit and a concrete failure; report count and target-response artifacts are not mislabeled as independent false alarms.
- The Monte Carlo result includes count, interval and assumptions, with failure/recovery on identical conditions.

**Laboratories:** [P41 — Model Ground Clutter and Swerling Targets](/courses/dsp-radar/modules/41-model-ground-clutter-and-swerling-targets); [P42 — Create a Full Range-Doppler Map](/courses/dsp-radar/modules/42-create-a-full-range-doppler-map); [P43 — Use a Fixed Detection Threshold](/courses/dsp-radar/modules/43-use-a-fixed-detection-threshold); [P44 — Build an Empirical Radar ROC Curve](/courses/dsp-radar/modules/44-build-an-empirical-radar-roc-curve); [P45 — Implement 1-D Cell-Averaging CFAR](/courses/dsp-radar/modules/45-implement-1-d-cell-averaging-cfar); [P46 — Vary CFAR Guard and Training Cells](/courses/dsp-radar/modules/46-vary-cfar-guard-and-training-cells); [P47 — Measure CFAR Loss](/courses/dsp-radar/modules/47-measure-cfar-loss); [P48 — Compare GO-CFAR and SO-CFAR at a Clutter Edge](/courses/dsp-radar/modules/48-compare-go-cfar-and-so-cfar-at-a-clutter-edge); [P49 — Use Ordered-Statistic CFAR with Interfering Targets](/courses/dsp-radar/modules/49-use-ordered-statistic-cfar-with-interfering-targets); [P50 — Apply 2-D CFAR to a Range-Doppler Map](/courses/dsp-radar/modules/50-apply-2-d-cfar-to-a-range-doppler-map); [P51 — Stress CFAR with Clutter Edges, Sidelobes, and Multiple Targets](/courses/dsp-radar/modules/51-stress-cfar-with-clutter-edges-sidelobes-and-multiple-targets); [P52 — Validate CFAR Pfa by Monte Carlo](/courses/dsp-radar/modules/52-validate-cfar-pfa-by-monte-carlo).

**Boundary.** Calibration is supported for the retained synthetic cases. Real clutter and operational false-alarm acceptance remain unvalidated. This rubric is authored self-assessment guidance, not a record of learner validation.
