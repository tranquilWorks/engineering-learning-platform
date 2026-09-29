### DSP-F84 · Defend the pulsed-radar processing chain

**Competency DSP-C84:** Trace unit-energy LFM through echoes, receiver correction, conjugate matched filtering, coherent Doppler, complete-stencil CA-CFAR, connected reports and gated tracking. Controls affect the retained first scan; the explicitly labeled eight-scan baseline shows a real scan-4 fade and coast.

**Builds on:** [P19 — Inject and Correct IQ Impairments](/courses/dsp-radar/modules/19-inject-and-correct-iq-impairments); [P32 — Perform LFM Pulse Compression](/courses/dsp-radar/modules/32-perform-lfm-pulse-compression); [P33 — Control Pulse-Compression Sidelobes](/courses/dsp-radar/modules/33-control-pulse-compression-sidelobes); [P42 — Create a Full Range-Doppler Map](/courses/dsp-radar/modules/42-create-a-full-range-doppler-map); [P50 — Apply 2-D CFAR to a Range-Doppler Map](/courses/dsp-radar/modules/50-apply-2-d-cfar-to-a-range-doppler-map); [P52 — Validate CFAR Pfa by Monte Carlo](/courses/dsp-radar/modules/52-validate-cfar-pfa-by-monte-carlo); [P53 — Group Detection Cells into Target Reports](/courses/dsp-radar/modules/53-group-detection-cells-into-target-reports); [P57 — Gate and Associate Detections by Nearest Neighbor](/courses/dsp-radar/modules/57-gate-and-associate-detections-by-nearest-neighbor); [P58 — Implement Track Initiation, Confirmation, Coasting, and Deletion](/courses/dsp-radar/modules/58-implement-track-initiation-confirmation-coasting-and-deletion).

**Predict and investigate.** Trace the selected scene through waveform, receiver, matched, range_doppler, detections and reports. Change design_pfa and replica_taper separately; use track and coast to explain the retained baseline scan-4 fade.

**Evidence to keep.** Write your prediction before manipulating controls. Record baseline settings, one-variable comparisons, the plotted quantity and its units, and the result after restoring the same settings. Use the existing lesson's named failure and recovery:

- Trigger: Enable broken_mode at baseline controls.
- Diagnose: Removing conjugation from the matched replica loses coherent compression gain and changes downstream detections. A fixed threshold also overreacts to the clutter edge; a report near the injected receiver spur is a false report, not target truth.
- Recover: Disable the failure to rerun the conjugate time-reversed replica on the identical calibrated cube. Reports drive tracking; truth is used only for offline scoring. Requested Pfa is not a guarantee for these correlated, nonhomogeneous cells.

**Browser recovery.** Turn **Enable the named failure** on to capture the fault, then off while holding the other controls at the same values. Compare the recovered evidence with that same-settings healthy run. Use **Reset parameters** to restore the original baseline.

**Explain the relation.** `R=c tau/2 (m); f_D=2 v/lambda (Hz), positive v approaching; threshold=alpha mean(training power)`. Relate each symbol to a displayed quantity and distinguish samples, seconds, frequency, phase and any power normalization that applies.

**Check your reasoning.** Compression requires conjugate phase alignment; CFAR crossings form components and reports before tracking. The eight-scan track is explicitly a retained baseline, not a new trajectory for every selected first-scan control. A fade leads to prediction/coasting rather than an invented observation.

**Limit the claim.** This is a pulsed-radar chain. It does not execute FMCW, virtual-array, SAR, ISAR or passive branches, and requested homogeneous-cell Pfa is not a guarantee in the correlated clutter scene. A model-valid toggle flag is not a target-detection or tracking-success verdict; use the computed counts and errors.

**Completion standard.** A satisfactory explanation connects a prediction to measured browser evidence, uses the correct units, explains the failure causally, and identifies a model limit. Merely reproducing a favorable plot or reading this answer is not an assessment pass. No learner score or completion is stored.

Continue the domain assessment at [P84 — Run the End-to-End Radar Processing Capstone](/courses/dsp-radar/modules/84-run-the-end-to-end-radar-processing-capstone).

### Cumulative assessment DSP-A10 — Defend the pulsed-radar processing chain

Trace the retained end-to-end pulsed-radar mechanism and distinguish selected-scene changes from its fixed baseline track demonstration.

**Evidence portfolio.** Work through the tasks below using the linked laboratories. Keep predictions, settings, dimensioned observations, failure diagnoses and recoveries together.

1. Reset design_pfa=0.001 and replica_taper=0. Trace waveform -> receiver -> matched -> range_doppler -> detections -> reports, recording the axes and physical quantity at each transition. Account for receiver_reconstruction_error in V and compression_peak_ratio.
2. Change design_pfa through 0.0001, 0.001 and 0.01 on the same selected corrected power map. Record detected_cells, clustered_reports, matched_truth_reports, false_reports and empirical_false_cell_rate; distinguish requested homogeneous-cell probability from this scene's empirical result.
3. Change replica_taper through 0, 0.5 and 1. Use taper_width and taper_visibility to explain a width/sidelobe/weak-target tradeoff. Enable broken_mode, diagnose missing replica conjugation from compression and downstream evidence, then disable it and verify the baseline returns.
4. Use track and coast to trace the retained eight-scan baseline. Record baseline_track_rmse in m, baseline_sequence_pd and scan_four_coast_count. Explain why scan four coasts and why selected first-scan controls do not create a different eight-scan track.

**Assessment rubric.** All four criteria must be supported by your recorded evidence; a missing criterion means revise that part of the explanation.

- Every stage is tied to an executed plot or metric, with delay, Doppler and amplitude/power units kept consistent.
- Crossings, components, reports, matches and false reports are distinguished; truth is used only for offline scoring.
- The selected-scene failure and exact recovery follow causal compression changes, and the taper tradeoff includes a measured cost.
- The baseline tracking sequence is labeled honestly, including the physical fade and coast. The scope explicitly excludes FMCW, arrays, SAR/ISAR and passive integration.

**Laboratories:** [P84 — Run the End-to-End Radar Processing Capstone](/courses/dsp-radar/modules/84-run-the-end-to-end-radar-processing-capstone).

**Boundary.** This is an independently checked synthetic pulsed-radar chain and a self-assessment rubric. It is not a record of a learner passing, MATLAB parity, physical radar validation or operational detection/tracking acceptance. This rubric is authored self-assessment guidance, not a record of learner validation.
