### DSP-F24 · Recover a signal and justify uncertainty

**Competency DSP-C24:** The explicit RRC singularity limits produce a finite unit-energy pulse. The conjugate reversed receiver filter peaks after the total transmit/receive delay; finite truncation leaves measurable ISI.

**Builds on:** [P07 — Understand Convolution as Echo Addition](/courses/dsp-radar/modules/07-understand-convolution-as-echo-addition); [P08 — Use Correlation to Find a Hidden Pattern](/courses/dsp-radar/modules/08-use-correlation-to-find-a-hidden-pattern); [P23 — Build BPSK and QPSK Constellation Intuition](/courses/dsp-radar/modules/23-build-bpsk-and-qpsk-constellation-intuition).

**Predict and investigate.** Compare span_symbols=2 and 8 at fixed rolloff. Account for both filter delays before interpreting decisions and the eye opening.

**Evidence to keep.** Write your prediction before manipulating controls. Record baseline settings, one-variable comparisons, the plotted quantity and its units, and the result after restoring the same settings. Use the existing lesson's named failure and recovery:

- Trigger: Enable broken_mode at baseline controls.
- Diagnose: Sampling four samples late is a half-symbol timing error. Even a correct matched filter cannot open the constellation at the wrong sampling instant.
- Recover: Align samples at len(pulse)-1 plus multiples of eight. Compare aligned noisy EVM, noiseless residual ISI, and the rectangular reference.

**Browser recovery.** Turn **Enable the named failure** on to capture the fault, then off while holding the other controls at the same values. Compare the recovered evidence with that same-settings healthy run. Use **Reset parameters** to restore the original baseline.

**Explain the relation.** `group_delay_each=(L-1)/2 samples`. Relate each symbol to a displayed quantity and distinguish samples, seconds, frequency, phase and any power normalization that applies.

**Check your reasoning.** The combined transmit/receive delay is the sum of each linear-phase filter's delay. Longer finite support better approximates the intended pulse pair and can reduce residual ISI, while rolloff trades bandwidth against pulse shape.

**Limit the claim.** An infinite-duration zero-ISI property is only approximated by truncated filters. Sampling at the wrong delay can obscure an otherwise correct matched filter.

**Completion standard.** A satisfactory explanation connects a prediction to measured browser evidence, uses the correct units, explains the failure causally, and identifies a model limit. Merely reproducing a favorable plot or reading this answer is not an assessment pass. No learner score or completion is stored.

Continue the domain assessment at [P28 — Connect Thresholds to ROC Curves and Estimator Limits](/courses/dsp-radar/modules/28-connect-thresholds-to-roc-curves-and-estimator-limits).
