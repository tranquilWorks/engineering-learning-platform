### DSP-F48 · Audit a detector's false-alarm claim

**Competency DSP-C48:** GO protects the high side of a clutter edge; SO can preserve a weak target when one reference side is contaminated. Each statistic needs its own homogeneous calibration.

**Builds on:** [P41 — Model Ground Clutter and Swerling Targets](/courses/dsp-radar/modules/41-model-ground-clutter-and-swerling-targets); [P45 — Implement 1-D Cell-Averaging CFAR](/courses/dsp-radar/modules/45-implement-1-d-cell-averaging-cfar); [P46 — Vary CFAR Guard and Training Cells](/courses/dsp-radar/modules/46-vary-cfar-guard-and-training-cells).

**Predict and investigate.** Increase clutter_step_db and then interferer_power_db. Locate cases where GO protects the high-background side and cases where SO preserves a weak target.

**Evidence to keep.** Write your prediction before manipulating controls. Record baseline settings, one-variable comparisons, the plotted quantity and its units, and the result after restoring the same settings. Use the existing lesson's named failure and recovery:

- Trigger: Enable broken_mode at baseline controls.
- Diagnose: Always choosing SO because it preserved one weak target causes excess high-side edge crossings. A shared CA multiplier also fails to give GO and SO the same nominal Pfa.
- Recover: Restore statistic-specific calibration and choose GO for the protected edge-false-alarm comparison. Disable the toggle; retain the separate SO advantage under one-sided contamination.

**Browser recovery.** Turn **Enable the named failure** on to capture the fault, then off while holding the other controls at the same values. Compare the recovered evidence with that same-settings healthy run. Use **Reset parameters** to restore the original baseline.

**Explain the relation.** `GO=max(left_mean,right_mean); SO=min(left_mean,right_mean)`. Relate each symbol to a displayed quantity and distinguish samples, seconds, frequency, phase and any power normalization that applies.

**Check your reasoning.** GO uses the larger side mean and can suppress edge false alarms while masking targets near contaminated references. SO uses the smaller mean and can help under one-sided interference, but its calibration differs.

**Limit the claim.** Neither rule universally dominates. Applying CA's multiplier to a different reference statistic breaks a fair equal-Pfa comparison.

**Completion standard.** A satisfactory explanation connects a prediction to measured browser evidence, uses the correct units, explains the failure causally, and identifies a model limit. Merely reproducing a favorable plot or reading this answer is not an assessment pass. No learner score or completion is stored.

Continue the domain assessment at [P52 — Validate CFAR Pfa by Monte Carlo](/courses/dsp-radar/modules/52-validate-cfar-pfa-by-monte-carlo).
