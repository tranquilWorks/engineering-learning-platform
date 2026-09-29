### DSP-F63 · Defend an array estimate under mismatch

**Competency DSP-C63:** The narrowband sensor matrix X=A S+N is matched by w=a(theta)/M. Hermitian steering aligns the chosen direction before mean squared output measures spatial response.

**Builds on:** [P08 — Use Correlation to Find a Hidden Pattern](/courses/dsp-radar/modules/08-use-correlation-to-find-a-hidden-pattern); [P27 — Use Monte Carlo Trials Instead of One Lucky Run](/courses/dsp-radar/modules/27-use-monte-carlo-trials-instead-of-one-lucky-run); [P61 — See Phase Steering in a Uniform Linear Array](/courses/dsp-radar/modules/61-see-phase-steering-in-a-uniform-linear-array); [P62 — Plot Array Factor, Beamwidth, and Grating Lobes](/courses/dsp-radar/modules/62-plot-array-factor-beamwidth-and-grating-lobes).

**Predict and investigate.** Compare elements and source_snr_db separately. Use alignment and scan to explain how conjugate steering sums the desired phase pattern and why a sign error mirrors the estimate.

**Evidence to keep.** Write your prediction before manipulating controls. Record baseline settings, one-variable comparisons, the plotted quantity and its units, and the result after restoring the same settings. Use the existing lesson's named failure and recovery:

- Trigger: Enable broken_mode at baseline controls.
- Diagnose: Reversing the steering phase convention mirrors the named -20/+30 degree scene. The failure keeps sensor data fixed and changes only the steering sign.
- Recover: Restore the conjugate steering convention on that same named scene. Disable the toggle to return exactly to the selected -20/+25 degree baseline. Fixed phase weights assume narrowband signals.

**Browser recovery.** Turn **Enable the named failure** on to capture the fault, then off while holding the other controls at the same values. Compare the recovered evidence with that same-settings healthy run. Use **Reset parameters** to restore the original baseline.

**Explain the relation.** `y=w^H x`. Relate each symbol to a displayed quantity and distinguish samples, seconds, frequency, phase and any power normalization that applies.

**Check your reasoning.** The beamformer projects sensor samples onto the assumed steering vector. Aperture controls geometric discrimination; SNR and snapshot averaging control noisy evidence. These are different routes to a clearer scan.

**Limit the claim.** Unresolved coherent or closely spaced sources can merge. A scan peak is conditioned on the assumed array geometry and calibration.

**Completion standard.** A satisfactory explanation connects a prediction to measured browser evidence, uses the correct units, explains the failure causally, and identifies a model limit. Merely reproducing a favorable plot or reading this answer is not an assessment pass. No learner score or completion is stored.

Continue the domain assessment at [P68 — Build an Introductory STAP Clutter-Ridge Experiment](/courses/dsp-radar/modules/68-build-an-introductory-stap-clutter-ridge-experiment).
