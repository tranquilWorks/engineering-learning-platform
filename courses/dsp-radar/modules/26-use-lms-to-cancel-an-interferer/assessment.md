### DSP-F26 · Recover a signal and justify uncertainty

**Competency DSP-C26:** Each sample predicts the coupled reference, subtracts it, then updates eight taps by mu*error*reference. The desired two-tone output should remain; zero output is not the objective.

**Builds on:** [P05 — Explore White, Colored, and Impulsive Noise](/courses/dsp-radar/modules/05-explore-white-colored-and-impulsive-noise); [P07 — Understand Convolution as Echo Addition](/courses/dsp-radar/modules/07-understand-convolution-as-echo-addition); [P25 — Create and Equalize a Multipath Channel](/courses/dsp-radar/modules/25-create-and-equalize-a-multipath-channel).

**Predict and investigate.** Compare step_size values and then reduce reference_correlation. Explain the coefficient and error histories around the channel change using coefficients and convergence.

**Evidence to keep.** Write your prediction before manipulating controls. Record baseline settings, one-variable comparisons, the plotted quantity and its units, and the result after restoring the same settings. Use the existing lesson's named failure and recovery:

- Trigger: Enable broken_mode at baseline controls.
- Diagnose: Step 0.35 exceeds the white-Gaussian mean-square reference limit 0.2. The guard stops before weights exceed 10000 or error exceeds one million; no unsafe tail is fabricated.
- Recover: Reset all taps and replay the same seed at step 0.006 with the correlated reference. Reacquisition requires 64 consecutive coefficient errors below 0.08; sentinel 3001 means not reacquired.

**Browser recovery.** Turn **Enable the named failure** on to capture the fault, then off while holding the other controls at the same values. Compare the recovered evidence with that same-settings healthy run. Use **Reset parameters** to restore the original baseline.

**Explain the relation.** `w[n+1]=w[n]+mu u[n] e[n]`. Relate each symbol to a displayed quantity and distinguish samples, seconds, frequency, phase and any power normalization that applies.

**Check your reasoning.** A larger LMS step can adapt faster but increases excess error and can violate stability. A correlated reference exposes cancelable interference; the retained desired signal means successful residual power should not become zero.

**Limit the claim.** A reference that contains desired-signal leakage can cancel the quantity we want. One bounded run does not certify every input covariance or step size.

**Completion standard.** A satisfactory explanation connects a prediction to measured browser evidence, uses the correct units, explains the failure causally, and identifies a model limit. Merely reproducing a favorable plot or reading this answer is not an assessment pass. No learner score or completion is stored.

Continue the domain assessment at [P28 — Connect Thresholds to ROC Curves and Estimator Limits](/courses/dsp-radar/modules/28-connect-thresholds-to-roc-curves-and-estimator-limits).
