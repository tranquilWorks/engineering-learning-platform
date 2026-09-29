### DSP-F49 · Audit a detector's false-alarm claim

**Competency DSP-C49:** OS-CFAR uses the kth ascending reference power and calibrates its product-form false-alarm law. Its N−k capacity is a strong-outlier limit, not immunity to arbitrary contamination.

**Builds on:** [P45 — Implement 1-D Cell-Averaging CFAR](/courses/dsp-radar/modules/45-implement-1-d-cell-averaging-cfar); [P46 — Vary CFAR Guard and Training Cells](/courses/dsp-radar/modules/46-vary-cfar-guard-and-training-cells); [P48 — Compare GO-CFAR and SO-CFAR at a Clutter Edge](/courses/dsp-radar/modules/48-compare-go-cfar-and-so-cfar-at-a-clutter-edge).

**Predict and investigate.** Change os_rank and compare the effect of strong contaminants. Explain the breakdown when the count exceeds N-k using the ascending order statistic.

**Evidence to keep.** Write your prediction before manipulating controls. Record baseline settings, one-variable comparisons, the plotted quantity and its units, and the result after restoring the same settings. Use the existing lesson's named failure and recovery:

- Trigger: Enable broken_mode at baseline controls.
- Diagnose: The failure selects rank 22 while retaining rank-18 alpha. Its homogeneous Pfa changes, so a Pd comparison no longer has equal calibration.
- Recover: Recompute alpha for the selected rank, inspect contamination count and strength, and state the lost outlier capacity. Disable the toggle for the selected rank-specific baseline.

**Browser recovery.** Turn **Enable the named failure** on to capture the fault, then off while holding the other controls at the same values. Compare the recovered evidence with that same-settings healthy run. Use **Reset parameters** to restore the original baseline.

**Explain the relation.** `strong_outlier_capacity=N-k for ascending rank k`. Relate each symbol to a displayed quantity and distinguish samples, seconds, frequency, phase and any power normalization that applies.

**Check your reasoning.** The kth of N sorted training powers can exclude up to N-k arbitrarily large outliers from the chosen rank. At one more contaminator the rank itself can be contaminated; changing k also requires a new false-alarm calibration.

**Limit the claim.** The outlier-capacity argument concerns large contamination, not every texture or correlated-background failure.

**Completion standard.** A satisfactory explanation connects a prediction to measured browser evidence, uses the correct units, explains the failure causally, and identifies a model limit. Merely reproducing a favorable plot or reading this answer is not an assessment pass. No learner score or completion is stored.

Continue the domain assessment at [P52 — Validate CFAR Pfa by Monte Carlo](/courses/dsp-radar/modules/52-validate-cfar-pfa-by-monte-carlo).
