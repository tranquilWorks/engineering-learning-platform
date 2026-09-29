### DSP-F54 · Explain a track from reports to identity

**Competency DSP-C54:** Predict x+=T v, form the available-report innovation, and correct position by alpha r and velocity by beta r/T. Missing reports coast without invented measurements.

**Builds on:** [P36 — Measure Doppler from Pulse-to-Pulse Phase](/courses/dsp-radar/modules/36-measure-doppler-from-pulse-to-pulse-phase); [P53 — Group Detection Cells into Target Reports](/courses/dsp-radar/modules/53-group-detection-cells-into-target-reports).

**Predict and investigate.** Change alpha_gain and beta_gain independently, then inspect missing-scan behavior. Explain why beta zero cannot learn an initially unknown speed.

**Evidence to keep.** Write your prediction before manipulating controls. Record baseline settings, one-variable comparisons, the plotted quantity and its units, and the result after restoring the same settings. Use the existing lesson's named failure and recovery:

- Trigger: Enable broken_mode at baseline controls.
- Diagnose: Setting beta to zero leaves the initially zero velocity unlearned, causing persistent position lag.
- Recover: Restore positive beta on the same measurements; reset the controls and disable the failure for exact recovery.

**Browser recovery.** Turn **Enable the named failure** on to capture the fault, then off while holding the other controls at the same values. Compare the recovered evidence with that same-settings healthy run. Use **Reset parameters** to restore the original baseline.

**Explain the relation.** `x_plus=x_minus+alpha residual; v_plus=v_minus+beta residual/dt`. Relate each symbol to a displayed quantity and distinguish samples, seconds, frequency, phase and any power normalization that applies.

**Check your reasoning.** Alpha corrects predicted position from the innovation; beta updates velocity with the innovation divided by scan interval. Without a report, prediction propagates the prior state instead of inventing a measurement.

**Limit the claim.** Gain choices encode a tracking compromise. A deterministic trajectory does not establish robustness to every maneuver or clutter condition.

**Completion standard.** A satisfactory explanation connects a prediction to measured browser evidence, uses the correct units, explains the failure causally, and identifies a model limit. Merely reproducing a favorable plot or reading this answer is not an assessment pass. No learner score or completion is stored.

Continue the domain assessment at [P60 — Use an IMM for a Maneuvering Target](/courses/dsp-radar/modules/60-use-an-imm-for-a-maneuvering-target).
