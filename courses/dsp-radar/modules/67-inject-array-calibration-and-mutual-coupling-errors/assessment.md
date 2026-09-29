### DSP-F67 · Defend an array estimate under mismatch

**Competency DSP-C67:** A known 10-degree calibration source estimates each composite response after removing nominal steering. Equalization also colors receiver noise; MUSIC whitens with diag(|equalizer|²). Coupling and position errors make the residual direction-dependent.

**Builds on:** [P19 — Inject and Correct IQ Impairments](/courses/dsp-radar/modules/19-inject-and-correct-iq-impairments); [P63 — Implement Conventional Delay-and-Sum Beamforming](/courses/dsp-radar/modules/63-implement-conventional-delay-and-sum-beamforming); [P65 — Use MVDR/Capon Adaptive Beamforming](/courses/dsp-radar/modules/65-use-mvdr-capon-adaptive-beamforming); [P66 — Estimate DOA with MUSIC](/courses/dsp-radar/modules/66-estimate-doa-with-music).

**Predict and investigate.** Increase error_scale and coupling_magnitude separately. Compare channels, phase and the corrected scans; explain why correcting data also changes the noise covariance.

**Evidence to keep.** Write your prediction before manipulating controls. Record baseline settings, one-variable comparisons, the plotted quantity and its units, and the result after restoring the same settings. Use the existing lesson's named failure and recovery:

- Trigger: Enable broken_mode at baseline controls.
- Diagnose: Dividing by the raw calibration response without removing its known steering phase makes the calibration source appear at boresight.
- Recover: Divide the measured response by nominal 10-degree steering before equalization. This repairs the known direction on unchanged data; it does not identify a global coupling inverse.

**Browser recovery.** Turn **Enable the named failure** on to capture the fault, then off while holding the other controls at the same values. Compare the recovered evidence with that same-settings healthy run. Use **Reset parameters** to restore the original baseline.

**Explain the relation.** `R_corrected=C R_measured C^H`. Relate each symbol to a displayed quantity and distinguish samples, seconds, frequency, phase and any power normalization that applies.

**Check your reasoning.** A channel correction transforms both signal and noise, so covariance must transform consistently. Dividing out a calibration source's steering by mistake can flatten the physical phase progression instead of identifying sensor errors.

**Limit the claim.** One-angle calibration may leave direction-dependent coupling residuals. Recovery in the retained fixture does not establish all-angle calibration.

**Completion standard.** A satisfactory explanation connects a prediction to measured browser evidence, uses the correct units, explains the failure causally, and identifies a model limit. Merely reproducing a favorable plot or reading this answer is not an assessment pass. No learner score or completion is stored.

Continue the domain assessment at [P68 — Build an Introductory STAP Clutter-Ridge Experiment](/courses/dsp-radar/modules/68-build-an-introductory-stap-clutter-ridge-experiment).
