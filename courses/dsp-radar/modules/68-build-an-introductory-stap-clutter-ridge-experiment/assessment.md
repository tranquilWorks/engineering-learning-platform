### DSP-F68 · Defend an array estimate under mismatch

**Competency DSP-C68:** The 64-channel vector stacks all eight sensors inside each of eight pulses. Clutter obeys normalized Doppler=.35 sin(theta). Joint covariance keeps angle-Doppler coupling that separate covariance estimates discard. The cell under test uses independent seeds and never trains covariance.

**Builds on:** [P38 — Implement a Two-Pulse and Three-Pulse MTI Canceller](/courses/dsp-radar/modules/38-implement-a-two-pulse-and-three-pulse-mti-canceller); [P41 — Model Ground Clutter and Swerling Targets](/courses/dsp-radar/modules/41-model-ground-clutter-and-swerling-targets); [P42 — Create a Full Range-Doppler Map](/courses/dsp-radar/modules/42-create-a-full-range-doppler-map); [P65 — Use MVDR/Capon Adaptive Beamforming](/courses/dsp-radar/modules/65-use-mvdr-capon-adaptive-beamforming).

**Predict and investigate.** Reduce training_cells and increase contamination_fraction. Compare fixed, separate and joint processors using components, not only the attractive shape of a notch.

**Evidence to keep.** Write your prediction before manipulating controls. Record baseline settings, one-variable comparisons, the plotted quantity and its units, and the result after restoring the same settings. Use the existing lesson's named failure and recovery:

- Trigger: Enable broken_mode at baseline controls.
- Diagnose: The named failure contaminates 40% of training cells with the actual slightly mismatched target. Unit response at the assumed steering does not prevent self-nulling at the actual steering.
- Recover: Restore unchanged clean training cells. This recovers the clean joint weight; removing a target component requires justified training selection, not knowledge available from every operational scene. Toggle off restores the selected contamination control.

**Browser recovery.** Turn **Enable the named failure** on to capture the fault, then off while holding the other controls at the same values. Compare the recovered evidence with that same-settings healthy run. Use **Reset parameters** to restore the original baseline.

**Explain the relation.** `space_time_steering=a_Doppler tensor a_space for the retained pulse-major vector ordering`. Relate each symbol to a displayed quantity and distinguish samples, seconds, frequency, phase and any power normalization that applies.

**Check your reasoning.** Joint space-time covariance captures the angle-Doppler coupling of clutter that separate filters discard. Limited support and target contamination corrupt the learned interference model; a unit constraint at an assumed direction does not guarantee actual target preservation.

**Limit the claim.** This small synthetic processor does not certify operational STAP convergence, calibration or clutter stationarity.

**Completion standard.** A satisfactory explanation connects a prediction to measured browser evidence, uses the correct units, explains the failure causally, and identifies a model limit. Merely reproducing a favorable plot or reading this answer is not an assessment pass. No learner score or completion is stored.

Continue the domain assessment at [P68 — Build an Introductory STAP Clutter-Ridge Experiment](/courses/dsp-radar/modules/68-build-an-introductory-stap-clutter-ridge-experiment).

### Cumulative assessment DSP-A07 — Defend an array estimate under mismatch

Relate array geometry and calibration to beamforming, subspace and adaptive space-time evidence.

**Evidence portfolio.** Work through the tasks below using the linked laboratories. Keep predictions, settings, dimensioned observations, failure diagnoses and recoveries together.

1. P61–P64: state the receive phase convention, calculate electrical spacing, and contrast beamwidth, grating lobes, conjugate steering and monopulse's local calibrated ratio. Record an ambiguous or guarded case as well as a favorable one.
2. P65–P66: compare snapshot support, diagonal loading, source separation and source count. Explain a small distortionless residual or sharp MUSIC peak that does not establish correct target performance.
3. P67: compare channel correction with noise covariance transformation. Explain why a one-angle calibration or accidental removal of source steering can fail away from calibration geometry.
4. P68: compare training_cells and contamination_fraction, recording active_scnr, fixed_scnr, separate_scnr, target_response, interference_output and distortionless_error. Show broken_mode and recovery and explain joint angle-Doppler coupling.

**Assessment rubric.** All four criteria must be supported by your recorded evidence; a missing criterion means revise that part of the explanation.

- Geometry, phase sign and electrical spacing account for both desired and aliased directions.
- Beam, monopulse and subspace estimates are supported by their relevant normalization, support and model assumptions.
- Calibration transforms noise as well as signal; a unit constraint is not confused with actual target protection.
- Joint adaptation's benefit and contamination/support failure are explained with component powers, dB units and exact recovery.

**Laboratories:** [P61 — See Phase Steering in a Uniform Linear Array](/courses/dsp-radar/modules/61-see-phase-steering-in-a-uniform-linear-array); [P62 — Plot Array Factor, Beamwidth, and Grating Lobes](/courses/dsp-radar/modules/62-plot-array-factor-beamwidth-and-grating-lobes); [P63 — Implement Conventional Delay-and-Sum Beamforming](/courses/dsp-radar/modules/63-implement-conventional-delay-and-sum-beamforming); [P64 — Build an Amplitude-Comparison Monopulse Experiment](/courses/dsp-radar/modules/64-build-an-amplitude-comparison-monopulse-experiment); [P65 — Use MVDR/Capon Adaptive Beamforming](/courses/dsp-radar/modules/65-use-mvdr-capon-adaptive-beamforming); [P66 — Estimate DOA with MUSIC](/courses/dsp-radar/modules/66-estimate-doa-with-music); [P67 — Inject Array Calibration and Mutual-Coupling Errors](/courses/dsp-radar/modules/67-inject-array-calibration-and-mutual-coupling-errors); [P68 — Build an Introductory STAP Clutter-Ridge Experiment](/courses/dsp-radar/modules/68-build-an-introductory-stap-clutter-ridge-experiment).

**Boundary.** This is a bounded synthetic array/STAP assessment, not a measured array calibration or operational adaptive-processing qualification. This rubric is authored self-assessment guidance, not a record of learner validation.
