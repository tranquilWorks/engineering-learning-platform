### DSP-F83 · Audit coherent imaging and passive processing

**Competency DSP-C83:** A joint space-time covariance adapts across the moving-platform clutter ridge. The conventional and adaptive maps use the same range record and explicitly normalized output power.

**Builds on:** [P41 — Model Ground Clutter and Swerling Targets](/courses/dsp-radar/modules/41-model-ground-clutter-and-swerling-targets); [P42 — Create a Full Range-Doppler Map](/courses/dsp-radar/modules/42-create-a-full-range-doppler-map); [P52 — Validate CFAR Pfa by Monte Carlo](/courses/dsp-radar/modules/52-validate-cfar-pfa-by-monte-carlo); [P65 — Use MVDR/Capon Adaptive Beamforming](/courses/dsp-radar/modules/65-use-mvdr-capon-adaptive-beamforming); [P68 — Build an Introductory STAP Clutter-Ridge Experiment](/courses/dsp-radar/modules/68-build-an-introductory-stap-clutter-ridge-experiment).

**Predict and investigate.** Compare training_cells below and above the space-time dimension, then increase contaminated_fraction. Use support, active and clean to explain rank and target mismatch.

**Evidence to keep.** Write your prediction before manipulating controls. Record baseline settings, one-variable comparisons, the plotted quantity and its units, and the result after restoring the same settings. Use the existing lesson's named failure and recovery:

- Trigger: Enable broken_mode at baseline controls.
- Diagnose: At baseline, target-like training contamination preserves the assumed unit response but increases interference output by over 20 dB. This failure is interference growth, not the target-null mechanism from P68.
- Recover: Disable the named failure and set contamination to zero to recompute from retained clean neighboring training cells and unchanged measurements. These normalized maps do not by themselves establish detection probability or false-alarm rate.

**Browser recovery.** Turn **Enable the named failure** on to capture the fault, then off while holding the other controls at the same values. Compare the recovered evidence with that same-settings healthy run. Use **Reset parameters** to restore the original baseline.

**Explain the relation.** `Rhat=(1/K) sum_k x_k x_k^H`. Relate each symbol to a displayed quantity and distinguish samples, seconds, frequency, phase and any power normalization that applies.

**Check your reasoning.** Sample covariance cannot have rank exceeding training support. Loading regularizes an undersupported estimate, but contaminated training can degrade output SCNR even while the assumed unit-response residual stays small.

**Limit the claim.** The small synthetic array and pulse ensemble support a mechanism demonstration, not deployment-level STAP performance or a universal training requirement.

**Completion standard.** A satisfactory explanation connects a prediction to measured browser evidence, uses the correct units, explains the failure causally, and identifies a model limit. Merely reproducing a favorable plot or reading this answer is not an assessment pass. No learner score or completion is stored.

Continue the domain assessment at [P83 — Compare Range-Doppler Processing with a Small STAP Processor](/courses/dsp-radar/modules/83-compare-range-doppler-processing-with-a-small-stap-processor).

### Cumulative assessment DSP-A09 — Audit coherent imaging and passive processing

Explain coherent image formation, motion correction and passive/adaptive processing while distinguishing their geometry and assumptions.

**Evidence portfolio.** Work through the tasks below using the linked laboratories. Keep predictions, settings, dimensioned observations, failure diagnoses and recoveries together.

1. P75–P79: trace complex phase history through range compression, backprojection and migration correction. Vary bandwidth and aperture separately; use phase, cuts and image evidence to distinguish range width, cross-range width, sampling ambiguity and image-grid spacing.
2. P80–P81: compare wavelength-normalized motion error, reference-gate autofocus and rotating-target imaging. Explain the separate envelope, phase and rotation-scale corrections and the failure from a contaminated reference.
3. P82: explain why delay means excess bistatic path c tau, then degrade reference_quality_db and compare raw, active and recovery. State what geometry is still required for localization.
4. P83: compare training_cells and contaminated_fraction, recording active_scnr, clean_scnr, distortionless_error, target_output_change and interference_output_change. Enable and recover the failure; compare its mechanism with the earlier P68 processor.

**Assessment rubric.** All four criteria must be supported by your recorded evidence; a missing criterion means revise that part of the explanation.

- Round-trip phase, interpolation direction and range-axis delay accounting form a consistent imaging explanation.
- Resolution, coherent gain, aliasing and grid density are separately supported by actual evidence.
- SAR, ISAR and passive geometry are distinguished; correction assumptions and lost data are explicit.
- The adaptive-processing diagnosis uses target and interference components, not only a unit constraint or attractive map, and reproduces recovery.

**Laboratories:** [P75 — Build SAR Phase-History Intuition](/courses/dsp-radar/modules/75-build-sar-phase-history-intuition); [P76 — Perform SAR Range Compression](/courses/dsp-radar/modules/76-perform-sar-range-compression); [P77 — Focus SAR with Backprojection](/courses/dsp-radar/modules/77-focus-sar-with-backprojection); [P78 — Observe and Correct Range-Cell Migration](/courses/dsp-radar/modules/78-observe-and-correct-range-cell-migration); [P79 — Compare SAR Resolution, Aperture Length, and Windowing](/courses/dsp-radar/modules/79-compare-sar-resolution-aperture-length-and-windowing); [P80 — Inject SAR Motion Error and Apply Autofocus](/courses/dsp-radar/modules/80-inject-sar-motion-error-and-apply-autofocus); [P81 — Form an ISAR Image from a Rotating Target](/courses/dsp-radar/modules/81-form-an-isar-image-from-a-rotating-target); [P82 — Build a Passive Radar Cross-Ambiguity Experiment](/courses/dsp-radar/modules/82-build-a-passive-radar-cross-ambiguity-experiment); [P83 — Compare Range-Doppler Processing with a Small STAP Processor](/courses/dsp-radar/modules/83-compare-range-doppler-processing-with-a-small-stap-processor).

**Boundary.** These are separate branch assessments. They are not components executed by the final pulsed-radar capstone and do not establish real-scene imaging quality. This rubric is authored self-assessment guidance, not a record of learner validation.
