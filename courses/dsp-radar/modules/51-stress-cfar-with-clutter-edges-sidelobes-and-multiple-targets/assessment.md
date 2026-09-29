### DSP-F51 · Audit a detector's false-alarm claim

**Competency DSP-C51:** No single CFAR rule wins across clutter edges, sidelobes and crowded targets. Inspect the reference statistic behind each disagreement and distinguish modeled response artifacts from true H0 crossings.

**Builds on:** [P33 — Control Pulse-Compression Sidelobes](/courses/dsp-radar/modules/33-control-pulse-compression-sidelobes); [P41 — Model Ground Clutter and Swerling Targets](/courses/dsp-radar/modules/41-model-ground-clutter-and-swerling-targets); [P48 — Compare GO-CFAR and SO-CFAR at a Clutter Edge](/courses/dsp-radar/modules/48-compare-go-cfar-and-so-cfar-at-a-clutter-edge); [P49 — Use Ordered-Statistic CFAR with Interfering Targets](/courses/dsp-radar/modules/49-use-ordered-statistic-cfar-with-interfering-targets); [P50 — Apply 2-D CFAR to a Range-Doppler Map](/courses/dsp-radar/modules/50-apply-2-d-cfar-to-a-range-doppler-map).

**Predict and investigate.** Locate one miss and one excess crossing in the combined scene. Compare CA, GO, SO and OS reference statistics before assigning a cause.

**Evidence to keep.** Write your prediction before manipulating controls. Record baseline settings, one-variable comparisons, the plotted quantity and its units, and the result after restoring the same settings. Use the existing lesson's named failure and recovery:

- Trigger: Enable broken_mode at baseline controls.
- Diagnose: Applying CA alpha to GO, SO and OS while claiming equal nominal Pfa makes the detector comparison unfair.
- Recover: Restore all four statistic-specific scale factors on the same scene; disable the toggle. Nonhomogeneous scenes can still depart from homogeneous Pfa calibration.

**Browser recovery.** Turn **Enable the named failure** on to capture the fault, then off while holding the other controls at the same values. Compare the recovered evidence with that same-settings healthy run. Use **Reset parameters** to restore the original baseline.

**Explain the relation.** `threshold=alpha times selected reference statistic`. Relate each symbol to a displayed quantity and distinguish samples, seconds, frequency, phase and any power normalization that applies.

**Check your reasoning.** An edge, interfering target and target sidelobe alter different parts of the reference set. Detector disagreements follow those statistics and their calibrated multipliers; a target's sidelobe crossing is not automatically an independent H0 false alarm.

**Limit the claim.** Use truth only for offline labeling. Do not feed target truth into the operational detector to manufacture a favorable verdict.

**Completion standard.** A satisfactory explanation connects a prediction to measured browser evidence, uses the correct units, explains the failure causally, and identifies a model limit. Merely reproducing a favorable plot or reading this answer is not an assessment pass. No learner score or completion is stored.

Continue the domain assessment at [P52 — Validate CFAR Pfa by Monte Carlo](/courses/dsp-radar/modules/52-validate-cfar-pfa-by-monte-carlo).
