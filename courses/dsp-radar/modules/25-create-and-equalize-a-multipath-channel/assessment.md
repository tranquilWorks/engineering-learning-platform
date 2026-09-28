### DSP-F25 · Recover a signal and justify uncertainty

**Competency DSP-C25:** Delayed pulse-shaped paths smear neighboring QPSK symbols. A 31-tap causal inverse cancels the leading response; regularization also penalizes tap energy.

**Builds on:** [P07 — Understand Convolution as Echo Addition](/courses/dsp-radar/modules/07-understand-convolution-as-echo-addition); [P09 — Compare FIR and IIR Filters by Behavior](/courses/dsp-radar/modules/09-compare-fir-and-iir-filters-by-behavior); [P24 — See Pulse Shaping and Matched Filtering](/courses/dsp-radar/modules/24-see-pulse-shaping-and-matched-filtering).

**Predict and investigate.** Increase echo_gain, then regularization. Use channel_spectrum, noise_gain and constellation to distinguish inverse-channel correction from noise amplification.

**Evidence to keep.** Write your prediction before manipulating controls. Record baseline settings, one-variable comparisons, the plotted quantity and its units, and the result after restoring the same settings. Use the existing lesson's named failure and recovery:

- Trigger: Enable broken_mode at baseline controls.
- Diagnose: The [1,-0.999] path has a -60 dB DC null. Finite ZF inversion boosts noise and leaves a tail: its symbol EVM and noise gain reveal the cost.
- Recover: The deep-null comparison uses lambda=0.01, nearest the 18 dB noise variance in the source grid. Regularization reduces noise enhancement but retains reported residual distortion; it does not perfectly recover lost information.

**Browser recovery.** Turn **Enable the named failure** on to capture the fault, then off while holding the other controls at the same values. Compare the recovered evidence with that same-settings healthy run. Use **Reset parameters** to restore the original baseline.

**Explain the relation.** `(H^H H+lambda I)g=H^H d, with H the finite convolution matrix and d the desired delayed impulse`. Relate each symbol to a displayed quantity and distinguish samples, seconds, frequency, phase and any power normalization that applies.

**Check your reasoning.** A near-null makes unregularized inversion large. Regularization limits that gain and can reduce EVM while retaining some channel distortion; the best noise/distortion tradeoff depends on the assumed noise level.

**Limit the claim.** A known synthetic channel and stationary noise are assumptions. Recovery here does not demonstrate adaptation to an unknown time-varying channel.

**Completion standard.** A satisfactory explanation connects a prediction to measured browser evidence, uses the correct units, explains the failure causally, and identifies a model limit. Merely reproducing a favorable plot or reading this answer is not an assessment pass. No learner score or completion is stored.

Continue the domain assessment at [P28 — Connect Thresholds to ROC Curves and Estimator Limits](/courses/dsp-radar/modules/28-connect-thresholds-to-roc-curves-and-estimator-limits).
