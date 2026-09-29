### DSP-F57 · Explain a track from reports to identity

**Competency DSP-C57:** Predict each track and form S=H P^- Hᵀ+R. Gate squared Mahalanobis distances, then greedily select the nearest remaining valid pair with row-and-column removal.

**Builds on:** [P53 — Group Detection Cells into Target Reports](/courses/dsp-radar/modules/53-group-detection-cells-into-target-reports); [P55 — Implement a Constant-Velocity Kalman Filter](/courses/dsp-radar/modules/55-implement-a-constant-velocity-kalman-filter); [P56 — Use an EKF for Range-Bearing Measurements](/courses/dsp-radar/modules/56-use-an-ekf-for-range-bearing-measurements).

**Predict and investigate.** Increase covariance_scale at a fixed gate_d2, then widen the gate. Explain why the closest report in metres need not be the closest in distance and why reports must remain unique across assignments.

**Evidence to keep.** Write your prediction before manipulating controls. Record baseline settings, one-variable comparisons, the plotted quantity and its units, and the result after restoring the same settings. Use the existing lesson's named failure and recovery:

- Trigger: Enable broken_mode at baseline controls.
- Diagnose: Ungated Euclidean matching favors a cross-ellipse clutter report over a plausible residual along the high-uncertainty direction.
- Recover: Restore track-specific covariance distances and the gate on unchanged reports. Truth IDs audit correctness only and never enter association.

**Browser recovery.** Turn **Enable the named failure** on to capture the fault, then off while holding the other controls at the same values. Compare the recovered evidence with that same-settings healthy run. Use **Reset parameters** to restore the original baseline.

**Explain the relation.** `d2=innovation^T S^-1 innovation`. Relate each symbol to a displayed quantity and distinguish samples, seconds, frequency, phase and any power normalization that applies.

**Check your reasoning.** Mahalanobis distance scales the innovation by predicted covariance. A larger uncertainty ellipse admits more candidates; one-to-one assignment prevents two tracks from consuming the same report even when both links are individually plausible.

**Limit the claim.** A valid gate only declares plausibility. It does not prove identity or eliminate clutter ambiguity.

**Completion standard.** A satisfactory explanation connects a prediction to measured browser evidence, uses the correct units, explains the failure causally, and identifies a model limit. Merely reproducing a favorable plot or reading this answer is not an assessment pass. No learner score or completion is stored.

Continue the domain assessment at [P60 — Use an IMM for a Maneuvering Target](/courses/dsp-radar/modules/60-use-an-imm-for-a-maneuvering-target).
