### DSP-F23 · Recover a signal and justify uncertainty

**Competency DSP-C23:** Both maps have unit symbol energy, but QPSK carries two bits per symbol. At equal Eb/N0 its noise standard deviation per coordinate is smaller by sqrt(2).

**Builds on:** [P05 — Explore White, Colored, and Impulsive Noise](/courses/dsp-radar/modules/05-explore-white-colored-and-impulsive-noise); [P18 — Contrast Real and Complex Sampling](/courses/dsp-radar/modules/18-contrast-real-and-complex-sampling); [P20 — Estimate Tone Frequency and Phase from Noisy Samples](/courses/dsp-radar/modules/20-estimate-tone-frequency-and-phase-from-noisy-samples).

**Predict and investigate.** Keep ebn0_db fixed and increase phase_error_deg. Use bit_mapping, constellation and phase_sweep to explain why a compact cluster can still decode incorrectly.

**Evidence to keep.** Write your prediction before manipulating controls. Record baseline settings, one-variable comparisons, the plotted quantity and its units, and the result after restoring the same settings. Use the existing lesson's named failure and recovery:

- Trigger: Enable broken_mode at baseline controls.
- Diagnose: At 55 degrees and 16 dB, QPSK clusters are tight but cross the fixed receiver sign boundaries. More SNR does not fix the wrong phase reference.
- Recover: Multiply the received QPSK samples by the exact inverse carrier rotation before sign decisions. This demonstration assumes the phase error is known; it does not implement carrier acquisition.

**Browser recovery.** Turn **Enable the named failure** on to capture the fault, then off while holding the other controls at the same values. Compare the recovered evidence with that same-settings healthy run. Use **Reset parameters** to restore the original baseline.

**Explain the relation.** `Es=log2(M) Eb`. Relate each symbol to a displayed quantity and distinguish samples, seconds, frequency, phase and any power normalization that applies.

**Check your reasoning.** Bit errors depend on decision regions and labeling as well as noise spread. Es/Eb depends on bits per symbol, so equal Eb/N0 requires consistent BPSK/QPSK noise normalization.

**Limit the claim.** Symbol error and bit error are distinct. A seeded constellation is illustrative; probability claims require repeated independent decisions.

**Completion standard.** A satisfactory explanation connects a prediction to measured browser evidence, uses the correct units, explains the failure causally, and identifies a model limit. Merely reproducing a favorable plot or reading this answer is not an assessment pass. No learner score or completion is stored.

Continue the domain assessment at [P28 — Connect Thresholds to ROC Curves and Estimator Limits](/courses/dsp-radar/modules/28-connect-thresholds-to-roc-curves-and-estimator-limits).
