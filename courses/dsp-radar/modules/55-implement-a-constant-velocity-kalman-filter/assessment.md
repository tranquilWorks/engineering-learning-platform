### DSP-F55 · Explain a track from reports to identity

**Competency DSP-C55:** Q=sigma_a² G Gᵀ admits interval acceleration; R=sigma_z² describes report noise. The Kalman gain and Joseph covariance update expose evolving trust and single-record NIS.

**Builds on:** [P27 — Use Monte Carlo Trials Instead of One Lucky Run](/courses/dsp-radar/modules/27-use-monte-carlo-trials-instead-of-one-lucky-run); [P53 — Group Detection Cells into Target Reports](/courses/dsp-radar/modules/53-group-detection-cells-into-target-reports); [P54 — Build an Alpha-Beta Tracker](/courses/dsp-radar/modules/54-build-an-alpha-beta-tracker).

**Predict and investigate.** Increase report_sigma_m and compare gain, error and nis. Then change acceleration uncertainty and explain how its units enter process covariance.

**Evidence to keep.** Write your prediction before manipulating controls. Record baseline settings, one-variable comparisons, the plotted quantity and its units, and the result after restoring the same settings. Use the existing lesson's named failure and recovery:

- Trigger: Enable broken_mode at baseline controls.
- Diagnose: Zero process noise over-trusts the constant-velocity model. A separate sigma_z=.5 m comparison over-trusts noisy reports; neither mismatch changes the actual data.
- Recover: Restore the selected Q and R assumptions on the identical seeded record; disable the toggle for exact recovery. A single NIS record does not establish ensemble consistency.

**Browser recovery.** Turn **Enable the named failure** on to capture the fault, then off while holding the other controls at the same values. Compare the recovered evidence with that same-settings healthy run. Use **Reset parameters** to restore the original baseline.

**Explain the relation.** `K=P_minus H^T/(H P_minus H^T+R)`. Relate each symbol to a displayed quantity and distinguish samples, seconds, frequency, phase and any power normalization that applies.

**Check your reasoning.** Higher assumed measurement variance generally reduces measurement gain. Process covariance must use the state transition's time powers and acceleration units; normalized innovations compare residual magnitude with predicted uncertainty.

**Limit the claim.** One mean NIS near its expected value is a diagnostic, not an ensemble consistency proof. Model mismatch can persist despite plausible position tracks.

**Completion standard.** A satisfactory explanation connects a prediction to measured browser evidence, uses the correct units, explains the failure causally, and identifies a model limit. Merely reproducing a favorable plot or reading this answer is not an assessment pass. No learner score or completion is stored.

Continue the domain assessment at [P60 — Use an IMM for a Maneuvering Target](/courses/dsp-radar/modules/60-use-an-imm-for-a-maneuvering-target).
