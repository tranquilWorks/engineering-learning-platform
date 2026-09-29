### DSP-F59 · Explain a track from reports to identity

**Competency DSP-C59:** Two existing tracks cross with alternating report order. Position and idealized Cartesian velocity residuals are normalized by their own uncertainties; 200 paired records measure identity failures.

**Builds on:** [P57 — Gate and Associate Detections by Nearest Neighbor](/courses/dsp-radar/modules/57-gate-and-associate-detections-by-nearest-neighbor); [P58 — Implement Track Initiation, Confirmation, Coasting, and Deletion](/courses/dsp-radar/modules/58-implement-track-initiation-confirmation-coasting-and-deletion).

**Predict and investigate.** Increase position_sigma_m, then scan_interval_s. Locate a swapped identity in identity and explain whether it came from an admissible wrong link or duplicate report reuse.

**Evidence to keep.** Write your prediction before manipulating controls. Record baseline settings, one-variable comparisons, the plotted quantity and its units, and the result after restoring the same settings. Use the existing lesson's named failure and recovery:

- Trigger: Enable broken_mode at baseline controls.
- Diagnose: Independent row minima allow both tracks to consume the same report. Even valid one-to-one position-only assignment can swap identities near a crossing.
- Recover: Restore row-and-column removal plus normalized velocity evidence on unchanged reports. Truth identities are used only for audit; auxiliary Cartesian velocity is an idealized feature.

**Browser recovery.** Turn **Enable the named failure** on to capture the fault, then off while holding the other controls at the same values. Compare the recovered evidence with that same-settings healthy run. Use **Reset parameters** to restore the original baseline.

**Explain the relation.** `assignment minimizes summed admissible link cost with unique reports`. Relate each symbol to a displayed quantity and distinguish samples, seconds, frequency, phase and any power normalization that applies.

**Check your reasoning.** Crossing targets can have nearly equal position costs; velocity evidence can disambiguate some cases. One-to-one matching avoids reuse but does not guarantee the correct identity, especially with sparse scans or uncertain motion.

**Limit the claim.** Offline truth labels diagnose identity errors; they are unavailable to the operational association step.

**Completion standard.** A satisfactory explanation connects a prediction to measured browser evidence, uses the correct units, explains the failure causally, and identifies a model limit. Merely reproducing a favorable plot or reading this answer is not an assessment pass. No learner score or completion is stored.

Continue the domain assessment at [P60 — Use an IMM for a Maneuvering Target](/courses/dsp-radar/modules/60-use-an-imm-for-a-maneuvering-target).
