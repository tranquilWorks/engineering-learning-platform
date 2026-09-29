### DSP-F44 · Audit a detector's false-alarm claim

**Competency DSP-C44:** The normalized signed matched-filter score is Gaussian: H0 has mean zero and H1 shifts by √SNR. Threshold sweeps trade Pd against Pfa, while trial count sets rare-event resolution.

**Builds on:** [P27 — Use Monte Carlo Trials Instead of One Lucky Run](/courses/dsp-radar/modules/27-use-monte-carlo-trials-instead-of-one-lucky-run); [P28 — Connect Thresholds to ROC Curves and Estimator Limits](/courses/dsp-radar/modules/28-connect-thresholds-to-roc-curves-and-estimator-limits); [P43 — Use a Fixed Detection Threshold](/courses/dsp-radar/modules/43-use-a-fixed-detection-threshold).

**Predict and investigate.** Move threshold_sigma at fixed matched_snr_db. Convert a requested Pfa of 0.001 into an expected count over one million H0 cells and assess whether a small trial set can verify it.

**Evidence to keep.** Write your prediction before manipulating controls. Record baseline settings, one-variable comparisons, the plotted quantity and its units, and the result after restoring the same settings. Use the existing lesson's named failure and recovery:

- Trigger: Enable broken_mode at baseline controls.
- Diagnose: Selecting the 250 lowest H0 scores and placing a threshold at their maximum guarantees zero tuning crossings. The remaining bank crosses it: this selection-biased result cannot establish zero operational Pfa.
- Recover: Use the predetermined threshold and full independently generated H0/H1 banks. Disable the toggle for exact replay; finite Monte Carlo counts remain estimates.

**Browser recovery.** Turn **Enable the named failure** on to capture the fault, then off while holding the other controls at the same values. Compare the recovered evidence with that same-settings healthy run. Use **Reset parameters** to restore the original baseline.

**Explain the relation.** `E{false_alarms}=N_H0 Pfa`. Relate each symbol to a displayed quantity and distinguish samples, seconds, frequency, phase and any power normalization that applies.

**Check your reasoning.** The expectation is 1000 false alarms, not necessarily 1000 independent targets or tracks. A set of 500 trials expects only 0.5 alarms at that rate and cannot precisely estimate a rare tail.

**Limit the claim.** ROC points need trial counts and uncertainty. Correlated searched cells change count variance and invalidate naive independent-binomial intervals.

**Completion standard.** A satisfactory explanation connects a prediction to measured browser evidence, uses the correct units, explains the failure causally, and identifies a model limit. Merely reproducing a favorable plot or reading this answer is not an assessment pass. No learner score or completion is stored.

Continue the domain assessment at [P52 — Validate CFAR Pfa by Monte Carlo](/courses/dsp-radar/modules/52-validate-cfar-pfa-by-monte-carlo).
