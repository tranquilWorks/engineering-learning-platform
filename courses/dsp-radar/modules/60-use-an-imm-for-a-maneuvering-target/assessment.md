### DSP-F60 · Explain a track from reports to identity

**Competency DSP-C60:** A shared six-state CV/CA model bank mixes states and covariances, including between-mean spread, before prediction. Log likelihoods normalize posterior mode probabilities; the blended covariance includes model disagreement.

**Builds on:** [P55 — Implement a Constant-Velocity Kalman Filter](/courses/dsp-radar/modules/55-implement-a-constant-velocity-kalman-filter); [P57 — Gate and Associate Detections by Nearest Neighbor](/courses/dsp-radar/modules/57-gate-and-associate-detections-by-nearest-neighbor); [P59 — Track Crossing Targets and Observe Association Failure](/courses/dsp-radar/modules/59-track-crossing-targets-and-observe-association-failure).

**Predict and investigate.** Increase mode_stay_probability and compare probability through the acceleration bursts. Explain why a zero-support maneuver mode cannot recover solely from a high likelihood.

**Evidence to keep.** Write your prediction before manipulating controls. Record baseline settings, one-variable comparisons, the plotted quantity and its units, and the result after restoring the same settings. Use the existing lesson's named failure and recovery:

- Trigger: Enable broken_mode at baseline controls.
- Diagnose: Identity transition probabilities and initial [1,0] make the maneuver mode unreachable even when its likelihood would fit better.
- Recover: Restore nonzero transition support and the [.85,.15] prior on the same measurements; disable the toggle to reproduce the selected IMM exactly.

**Browser recovery.** Turn **Enable the named failure** on to capture the fault, then off while holding the other controls at the same values. Compare the recovered evidence with that same-settings healthy run. Use **Reset parameters** to restore the original baseline.

**Explain the relation.** `P_mixed=sum_i mu_i (P_i+(x_i-xbar)(x_i-xbar)^T)`. Relate each symbol to a displayed quantity and distinguish samples, seconds, frequency, phase and any power normalization that applies.

**Check your reasoning.** IMM mixing combines within-model covariance and the spread between model means. Mode transition probabilities provide prior support; multiplying a zero prior by a likelihood leaves zero. More persistence can delay a legitimate switch.

**Limit the claim.** The mode library bounds the maneuvers represented. Favorable results for this trajectory do not prove arbitrary maneuver coverage.

**Completion standard.** A satisfactory explanation connects a prediction to measured browser evidence, uses the correct units, explains the failure causally, and identifies a model limit. Merely reproducing a favorable plot or reading this answer is not an assessment pass. No learner score or completion is stored.

Continue the domain assessment at [P60 — Use an IMM for a Maneuvering Target](/courses/dsp-radar/modules/60-use-an-imm-for-a-maneuvering-target).

### Cumulative assessment DSP-A06 — Explain a track from reports to identity

Distinguish clustering, state estimation, association, lifecycle and maneuver inference using report-driven histories.

**Evidence portfolio.** Work through the tasks below using the linked laboratories. Keep predictions, settings, dimensioned observations, failure diagnoses and recoveries together.

1. P53–P54: show how connectivity, minimum_cells and weights change reports, then trace prediction/correction through missing scans. Explain why cluster spread is not automatically a calibrated tracker covariance.
2. P55–P56: vary report uncertainty and geometry, recording gain, nis and bearing_innovation. Derive the range-times-angle uncertainty scale in metres and explain angular residual wrapping.
3. P57–P59: compare physical and Mahalanobis distances, trace confirmation/coasting/deletion, and diagnose a crossing-target identity switch. Distinguish duplicate report reuse from a wrong one-to-one association.
4. P60: compare mode_stay_probability and maneuver_acceleration_mps2. Record position_rmse, fixed_cv_rmse, probability_sum_error and probability; enable the zero-support failure and restore the same baseline.

**Assessment rubric.** All four criteria must be supported by your recorded evidence; a missing criterion means revise that part of the explanation.

- Reports and measurements, covariance proxies and calibrated uncertainties, and prediction and correction are kept distinct.
- Timing, units, nonlinear bearing geometry and innovation normalization explain observed residuals.
- A complete lifecycle/identity argument uses actual report histories and does not use truth inside the operational decision.
- IMM mixing includes between-model spread; mode support and finite-model limits explain failure and recovery.

**Laboratories:** [P53 — Group Detection Cells into Target Reports](/courses/dsp-radar/modules/53-group-detection-cells-into-target-reports); [P54 — Build an Alpha-Beta Tracker](/courses/dsp-radar/modules/54-build-an-alpha-beta-tracker); [P55 — Implement a Constant-Velocity Kalman Filter](/courses/dsp-radar/modules/55-implement-a-constant-velocity-kalman-filter); [P56 — Use an EKF for Range-Bearing Measurements](/courses/dsp-radar/modules/56-use-an-ekf-for-range-bearing-measurements); [P57 — Gate and Associate Detections by Nearest Neighbor](/courses/dsp-radar/modules/57-gate-and-associate-detections-by-nearest-neighbor); [P58 — Implement Track Initiation, Confirmation, Coasting, and Deletion](/courses/dsp-radar/modules/58-implement-track-initiation-confirmation-coasting-and-deletion); [P59 — Track Crossing Targets and Observe Association Failure](/courses/dsp-radar/modules/59-track-crossing-targets-and-observe-association-failure); [P60 — Use an IMM for a Maneuvering Target](/courses/dsp-radar/modules/60-use-an-imm-for-a-maneuvering-target).

**Boundary.** Truth is used for offline scoring in these synthetic scenes. The assessment does not establish field tracking reliability. This rubric is authored self-assessment guidance, not a record of learner validation.
