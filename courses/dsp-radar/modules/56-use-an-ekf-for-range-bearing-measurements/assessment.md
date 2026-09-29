### DSP-F56 · Explain a track from reports to identity

**Competency DSP-C56:** Cartesian CV prediction meets nonlinear range/bearing through an explicit Jacobian. Bearing innovations are wrapped, covariance uses Joseph form, and r sigma_theta exposes increasing tangential uncertainty.

**Builds on:** [P16 — Create an Analytic Signal with the Hilbert Transform](/courses/dsp-radar/modules/16-create-an-analytic-signal-with-the-hilbert-transform); [P55 — Implement a Constant-Velocity Kalman Filter](/courses/dsp-radar/modules/55-implement-a-constant-velocity-kalman-filter).

**Predict and investigate.** Compare geometry_range_m at fixed bearing_sigma_deg. Use bearing_innovation to diagnose a near-full-turn residual at the angle boundary.

**Evidence to keep.** Write your prediction before manipulating controls. Record baseline settings, one-variable comparisons, the plotted quantity and its units, and the result after restoring the same settings. Use the existing lesson's named failure and recovery:

- Trigger: Enable broken_mode at baseline controls.
- Diagnose: Subtracting angles across +/-180 degrees without wrapping creates a near-full-turn innovation and a spurious Cartesian correction.
- Recover: Wrap only the angular innovation with atan2(sin(delta),cos(delta)); preserve the same polar data and restore the selected assumptions.

**Browser recovery.** Turn **Enable the named failure** on to capture the fault, then off while holding the other controls at the same values. Compare the recovered evidence with that same-settings healthy run. Use **Reset parameters** to restore the original baseline.

**Explain the relation.** `bearing_residual=atan2(sin(delta),cos(delta))`. Relate each symbol to a displayed quantity and distinguish samples, seconds, frequency, phase and any power normalization that applies.

**Check your reasoning.** Tangential position uncertainty grows approximately as range times angular uncertainty in radians. Wrapping the angular innovation into its principal interval avoids treating equivalent bearings as a nearly 2 pi discrepancy.

**Limit the claim.** EKF linearization is local. Large uncertainties, poor geometry or an incorrect Jacobian can invalidate the covariance interpretation.

**Completion standard.** A satisfactory explanation connects a prediction to measured browser evidence, uses the correct units, explains the failure causally, and identifies a model limit. Merely reproducing a favorable plot or reading this answer is not an assessment pass. No learner score or completion is stored.

Continue the domain assessment at [P60 — Use an IMM for a Maneuvering Target](/courses/dsp-radar/modules/60-use-an-imm-for-a-maneuvering-target).
