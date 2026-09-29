### DSP-F58 · Explain a track from reports to identity

**Competency DSP-C58:** Predict and associate reports before updating an explicit M-of-N lifecycle. Stable IDs record birth, tentative confirmation, coasting and deletion; truth labels enter only the final audit.

**Builds on:** [P54 — Build an Alpha-Beta Tracker](/courses/dsp-radar/modules/54-build-an-alpha-beta-tracker); [P55 — Implement a Constant-Velocity Kalman Filter](/courses/dsp-radar/modules/55-implement-a-constant-velocity-kalman-filter); [P57 — Gate and Associate Detections by Nearest Neighbor](/courses/dsp-radar/modules/57-gate-and-associate-detections-by-nearest-neighbor).

**Predict and investigate.** Compare confirmation_hits=3 with 4, then change coast_limit_scans. Trace a specific sequence in lifecycle from tentative through confirmed, coasting and deleted.

**Evidence to keep.** Write your prediction before manipulating controls. Record baseline settings, one-variable comparisons, the plotted quantity and its units, and the result after restoring the same settings. Use the existing lesson's named failure and recovery:

- Trigger: Enable broken_mode at baseline controls.
- Diagnose: The 1-of-1 policy with a 30-scan coast allowance confirms eight isolated false tracks and keeps them active through this record.
- Recover: Restore the selected M-of-4 and coast policy on identical reports; disabling the toggle reproduces the selected managed history exactly.

**Browser recovery.** Turn **Enable the named failure** on to capture the fault, then off while holding the other controls at the same values. Compare the recovered evidence with that same-settings healthy run. Use **Reset parameters** to restore the original baseline.

**Explain the relation.** `confirm when M hits occur in the last N scans`. Relate each symbol to a displayed quantity and distinguish samples, seconds, frequency, phase and any power normalization that applies.

**Check your reasoning.** Confirmation counts evidence within a finite history window. Coasting propagates a track without a measurement; deletion follows the configured consecutive-miss rule. Longer persistence can retain a real target but also retain a false track.

**Limit the claim.** A deleted identifier and a newly initiated track must not be silently treated as uninterrupted identity.

**Completion standard.** A satisfactory explanation connects a prediction to measured browser evidence, uses the correct units, explains the failure causally, and identifies a model limit. Merely reproducing a favorable plot or reading this answer is not an assessment pass. No learner score or completion is stored.

Continue the domain assessment at [P60 — Use an IMM for a Maneuvering Target](/courses/dsp-radar/modules/60-use-an-imm-for-a-maneuvering-target).
