### DSP-F22 · Recover a signal and justify uncertainty

**Competency DSP-C22:** FM phase slope moves while magnitude stays fixed. The smallest symmetric span containing 98% of retained RF line power is measured separately from Carson's approximation.

**Builds on:** [P16 — Create an Analytic Signal with the Hilbert Transform](/courses/dsp-radar/modules/16-create-an-analytic-signal-with-the-hilbert-transform); [P21 — Visualize AM as Carrier and Sidebands](/courses/dsp-radar/modules/21-visualize-am-as-carrier-and-sidebands).

**Predict and investigate.** Double deviation_hz, then double message_frequency_hz separately. Compare spectrum and phase_slope and state which control changes sideband spacing.

**Evidence to keep.** Write your prediction before manipulating controls. Record baseline settings, one-variable comparisons, the plotted quantity and its units, and the result after restoring the same settings. Use the existing lesson's named failure and recovery:

- Trigger: Enable broken_mode at baseline controls.
- Diagnose: An 8 kHz carrier with 5 kHz deviation exceeds 12 kHz Nyquist at 24 ksample/s; the observed phase increments wrap. Its aliased spectrum cannot certify occupied bandwidth.
- Recover: Resample the same physical failure at 30 ksample/s. The 10.2 kHz occupied span and positive guard are retained; finite-difference phase-slope error remains visible.

**Browser recovery.** Turn **Enable the named failure** on to capture the fault, then off while holding the other controls at the same values. Compare the recovered evidence with that same-settings healthy run. Use **Reset parameters** to restore the original baseline.

**Explain the relation.** `beta=Delta f/fm; B_Carson=2(Delta f+fm)`. Relate each symbol to a displayed quantity and distinguish samples, seconds, frequency, phase and any power normalization that applies.

**Check your reasoning.** Deviation sets peak instantaneous-frequency excursion, while message frequency sets spacing and changes the modulation index. Carson bandwidth is an engineering approximation; FM can have constant magnitude and changing phase.

**Limit the claim.** Sample-to-sample phase change must remain interpretable before differentiation. Aliased phase increments can give a smooth but wrong frequency estimate.

**Completion standard.** A satisfactory explanation connects a prediction to measured browser evidence, uses the correct units, explains the failure causally, and identifies a model limit. Merely reproducing a favorable plot or reading this answer is not an assessment pass. No learner score or completion is stored.

Continue the domain assessment at [P28 — Connect Thresholds to ROC Curves and Estimator Limits](/courses/dsp-radar/modules/28-connect-thresholds-to-roc-curves-and-estimator-limits).
