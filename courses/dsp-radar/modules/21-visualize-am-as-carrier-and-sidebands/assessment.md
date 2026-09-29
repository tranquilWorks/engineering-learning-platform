### DSP-F21 · Recover a signal and justify uncertainty

**Competency DSP-C21:** Multiplication creates carrier ± message-frequency lines; each sideband has depth/2 times the carrier amplitude. The multitone view retains both pairs.

**Builds on:** [P11 — Make FFT Bins Concrete](/courses/dsp-radar/modules/11-make-fft-bins-concrete); [P16 — Create an Analytic Signal with the Hilbert Transform](/courses/dsp-radar/modules/16-create-an-analytic-signal-with-the-hilbert-transform).

**Predict and investigate.** Increase modulation_depth through one while fixing message_frequency_hz. Explain the sideband changes in spectrum and the envelope detector's failure in recovery.

**Evidence to keep.** Write your prediction before manipulating controls. Record baseline settings, one-variable comparisons, the plotted quantity and its units, and the result after restoring the same settings. Use the existing lesson's named failure and recovery:

- Trigger: Enable broken_mode at baseline controls.
- Diagnose: At depth 1.4 the signed envelope crosses zero. Magnitude detection folds the negative envelope and distorts the message.
- Recover: The explicit coherent mixer and 900 Hz lowpass retain envelope sign, even during overmodulation. Disable the failure to restore the selected depth.

**Browser recovery.** Turn **Enable the named failure** on to capture the fault, then off while holding the other controls at the same values. Compare the recovered evidence with that same-settings healthy run. Use **Reset parameters** to restore the original baseline.

**Explain the relation.** `[1+m cos(2 pi fm t)] cos(2 pi fc t)`. Relate each symbol to a displayed quantity and distinguish samples, seconds, frequency, phase and any power normalization that applies.

**Check your reasoning.** Depth scales sideband amplitudes while message frequency sets their offsets. When the signed envelope crosses zero, magnitude folds its sign; synchronous recovery and envelope detection therefore differ.

**Limit the claim.** Envelope recovery assumes a nonnegative envelope and suitable carrier separation. A spectral sideband diagram alone does not prove a demodulator recovered the message.

**Completion standard.** A satisfactory explanation connects a prediction to measured browser evidence, uses the correct units, explains the failure causally, and identifies a model limit. Merely reproducing a favorable plot or reading this answer is not an assessment pass. No learner score or completion is stored.

Continue the domain assessment at [P28 — Connect Thresholds to ROC Curves and Estimator Limits](/courses/dsp-radar/modules/28-connect-thresholds-to-roc-curves-and-estimator-limits).
