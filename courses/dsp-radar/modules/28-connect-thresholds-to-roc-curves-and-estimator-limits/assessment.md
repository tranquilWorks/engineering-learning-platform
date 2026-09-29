### DSP-F28 · Recover a signal and justify uncertainty

**Competency DSP-C28:** Normalize the known-pulse matched filter by noise standard deviation. Independent H0/H1 banks trace Gaussian-tail ROC probabilities. The all-trial amplitude estimator attains variance sigma²/pulse energy under known timing and white Gaussian noise.

**Builds on:** [P08 — Use Correlation to Find a Hidden Pattern](/courses/dsp-radar/modules/08-use-correlation-to-find-a-hidden-pattern); [P20 — Estimate Tone Frequency and Phase from Noisy Samples](/courses/dsp-radar/modules/20-estimate-tone-frequency-and-phase-from-noisy-samples); [P27 — Use Monte Carlo Trials Instead of One Lucky Run](/courses/dsp-radar/modules/27-use-monte-carlo-trials-instead-of-one-lucky-run).

**Predict and investigate.** Raise threshold_sigma at fixed matched_snr_db. Use roc and selection to explain both the detection tradeoff and amplitude bias after selecting only detections.

**Evidence to keep.** Write your prediction before manipulating controls. Record baseline settings, one-variable comparisons, the plotted quantity and its units, and the result after restoring the same settings. Use the existing lesson's named failure and recovery:

- Trigger: Enable broken_mode at baseline controls.
- Diagnose: Keeping only detected H1 trials selects high amplitude estimates. Its positive bias invalidates the unbiased-estimator claim; a smaller selected variance is not evidence of beating the unbiased CRLB.
- Recover: Restore all 12000 independent H1 trials before estimating amplitude. The recovered bias and SNR-dependent variance are checked separately from the detector operating point.

**Browser recovery.** Turn **Enable the named failure** on to capture the fault, then off while holding the other controls at the same values. Compare the recovered evidence with that same-settings healthy run. Use **Reset parameters** to restore the original baseline.

**Explain the relation.** `Pfa=P(score>threshold | H0)`. Relate each symbol to a displayed quantity and distinguish samples, seconds, frequency, phase and any power normalization that applies.

**Check your reasoning.** A higher threshold generally lowers both Pfa and Pd. Selecting large observations truncates the estimation sample and shifts its mean, so conditional estimator behavior cannot be compared blindly with an unconditional unbiased bound.

**Limit the claim.** A theoretical estimator limit depends on model and regularity assumptions. It is not a guaranteed error for every finite record or selected subset.

**Completion standard.** A satisfactory explanation connects a prediction to measured browser evidence, uses the correct units, explains the failure causally, and identifies a model limit. Merely reproducing a favorable plot or reading this answer is not an assessment pass. No learner score or completion is stored.

Continue the domain assessment at [P28 — Connect Thresholds to ROC Curves and Estimator Limits](/courses/dsp-radar/modules/28-connect-thresholds-to-roc-curves-and-estimator-limits).

### Cumulative assessment DSP-A03 — Recover a signal and justify uncertainty

Relate modulation, matched filtering and adaptation to decision statistics and defensible finite-trial uncertainty.

**Evidence portfolio.** Work through the tasks below using the linked laboratories. Keep predictions, settings, dimensioned observations, failure diagnoses and recoveries together.

1. P21–P23: explain AM sideband offsets versus amplitudes, FM deviation versus message frequency, and QPSK bit decisions versus visually compact clusters. Carry units and Eb/Es normalization through the comparison.
2. P24–P25: count both filter delays, inspect residual ISI, and compare equalizer distortion with noise_gain. Explain why a regularized inverse can improve decisions while retaining some channel-response error.
3. P26: change step_size and reference_correlation separately, record coefficients and convergence at the channel change, then show failure/recovery. Explain the desired signal that should remain in the residual.
4. P27–P28: compare independent trial counts and threshold choices. Record running_ber, roc and selection; explain how duplicated trials and detection-conditioned amplitude estimates create different statistical errors.

**Assessment rubric.** All four criteria must be supported by your recorded evidence; a missing criterion means revise that part of the explanation.

- Modulation and symbol-energy arguments match the displayed conventions and units.
- Timing, ISI, inversion and adaptation form a causal explanation supported by actual plots.
- Trial count means independent observations; rare-event and selection uncertainty are explicit.
- Failure/recovery reproduces the same input condition and states why a bound or a small error is conditional on its model.

**Laboratories:** [P21 — Visualize AM as Carrier and Sidebands](/courses/dsp-radar/modules/21-visualize-am-as-carrier-and-sidebands); [P22 — Relate FM Deviation to Bandwidth](/courses/dsp-radar/modules/22-relate-fm-deviation-to-bandwidth); [P23 — Build BPSK and QPSK Constellation Intuition](/courses/dsp-radar/modules/23-build-bpsk-and-qpsk-constellation-intuition); [P24 — See Pulse Shaping and Matched Filtering](/courses/dsp-radar/modules/24-see-pulse-shaping-and-matched-filtering); [P25 — Create and Equalize a Multipath Channel](/courses/dsp-radar/modules/25-create-and-equalize-a-multipath-channel); [P26 — Use LMS to Cancel an Interferer](/courses/dsp-radar/modules/26-use-lms-to-cancel-an-interferer); [P27 — Use Monte Carlo Trials Instead of One Lucky Run](/courses/dsp-radar/modules/27-use-monte-carlo-trials-instead-of-one-lucky-run); [P28 — Connect Thresholds to ROC Curves and Estimator Limits](/courses/dsp-radar/modules/28-connect-thresholds-to-roc-curves-and-estimator-limits).

**Boundary.** No communication-channel field performance or universal convergence guarantee is inferred from seeded software trials. This rubric is authored self-assessment guidance, not a record of learner validation.
