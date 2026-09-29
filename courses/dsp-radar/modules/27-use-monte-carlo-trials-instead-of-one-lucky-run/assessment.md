### DSP-F27 · Recover a signal and justify uncertainty

**Competency DSP-C27:** Every BPSK trial uses its own 16-sample noise waveform and a unit-energy rectangular matched filter. Running error counts are Bernoulli observations; Wilson bounds quantify finite-sample uncertainty.

**Builds on:** [P05 — Explore White, Colored, and Impulsive Noise](/courses/dsp-radar/modules/05-explore-white-colored-and-impulsive-noise); [P23 — Build BPSK and QPSK Constellation Intuition](/courses/dsp-radar/modules/23-build-bpsk-and-qpsk-constellation-intuition).

**Predict and investigate.** Compare trial_count=100 and 4000 at fixed ebn0_db. Use blocks and running_ber to explain why repeated copies of a trial cannot narrow uncertainty legitimately.

**Evidence to keep.** Write your prediction before manipulating controls. Record baseline settings, one-variable comparisons, the plotted quantity and its units, and the result after restoring the same settings. Use the existing lesson's named failure and recovery:

- Trigger: Enable broken_mode at baseline controls.
- Diagnose: Repeating one lucky correct waveform creates one unique statistic, zero errors, and a misleadingly narrow nominal interval. The independence validity flag is false, so that interval has no binomial coverage claim.
- Recover: Rebuild the independent bank from seed 2701. The bank and decisions reproduce exactly, while block variability remains visible. More trials reduce uncertainty; they do not improve the underlying detector.

**Browser recovery.** Turn **Enable the named failure** on to capture the fault, then off while holding the other controls at the same values. Compare the recovered evidence with that same-settings healthy run. Use **Reset parameters** to restore the original baseline.

**Explain the relation.** `p_hat=errors/independent_trials`. Relate each symbol to a displayed quantity and distinguish samples, seconds, frequency, phase and any power normalization that applies.

**Check your reasoning.** Independent observations increase effective sample size; binomial interval width typically scales like inverse square root of trial count away from extremes. Duplicates retain the same information even if an incorrect denominator grows.

**Limit the claim.** Zero observed errors does not imply zero error probability. State the interval and independent trial count, especially in rare-event regimes.

**Completion standard.** A satisfactory explanation connects a prediction to measured browser evidence, uses the correct units, explains the failure causally, and identifies a model limit. Merely reproducing a favorable plot or reading this answer is not an assessment pass. No learner score or completion is stored.

Continue the domain assessment at [P28 — Connect Thresholds to ROC Curves and Estimator Limits](/courses/dsp-radar/modules/28-connect-thresholds-to-roc-curves-and-estimator-limits).
