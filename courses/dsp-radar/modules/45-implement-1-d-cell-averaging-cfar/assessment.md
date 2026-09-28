### DSP-F45 · Audit a detector's false-alarm claim

**Competency DSP-C45:** CA-CFAR averages 24 linear-power references and uses α=N(Pfa^(−1/N)−1). Only complete windows are eligible; scaling the entire scene preserves decisions.

**Builds on:** [P27 — Use Monte Carlo Trials Instead of One Lucky Run](/courses/dsp-radar/modules/27-use-monte-carlo-trials-instead-of-one-lucky-run); [P43 — Use a Fixed Detection Threshold](/courses/dsp-radar/modules/43-use-a-fixed-detection-threshold); [P44 — Build an Empirical Radar ROC Curve](/courses/dsp-radar/modules/44-build-an-empirical-radar-roc-curve).

**Predict and investigate.** Multiply scene_power_scale by a common factor while keeping design_pfa fixed. Explain the unchanged decisions using the CUT and training estimate, then enable the wrong-average failure.

**Evidence to keep.** Write your prediction before manipulating controls. Record baseline settings, one-variable comparisons, the plotted quantity and its units, and the result after restoring the same settings. Use the existing lesson's named failure and recovery:

- Trigger: Enable broken_mode at baseline controls.
- Diagnose: Averaging dB powers computes a geometric mean, lowers the noise estimate, and breaks the exponential-power calibration.
- Recover: Restore the arithmetic mean in linear power, retain the guard/CUT exclusion and skip incomplete edge windows. Disable the toggle to replay the selected scene.

**Browser recovery.** Turn **Enable the named failure** on to capture the fault, then off while holding the other controls at the same values. Compare the recovered evidence with that same-settings healthy run. Use **Reset parameters** to restore the original baseline.

**Explain the relation.** `alpha=N(Pfa^(-1/N)-1)`. Relate each symbol to a displayed quantity and distinguish samples, seconds, frequency, phase and any power normalization that applies.

**Check your reasoning.** Both CUT power and its training mean scale together, so their comparison is invariant. The CA multiplier is calibrated for a mean of linear exponential powers; averaging dB values changes the statistic.

**Limit the claim.** The exact alpha law assumes independent homogeneous cells and a training set independent of the CUT.

**Completion standard.** A satisfactory explanation connects a prediction to measured browser evidence, uses the correct units, explains the failure causally, and identifies a model limit. Merely reproducing a favorable plot or reading this answer is not an assessment pass. No learner score or completion is stored.

Continue the domain assessment at [P52 — Validate CFAR Pfa by Monte Carlo](/courses/dsp-radar/modules/52-validate-cfar-pfa-by-monte-carlo).
