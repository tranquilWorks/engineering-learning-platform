### DSP-F30 · Carry range and Doppler through a radar design

**Competency DSP-C30:** A zero-extended fractional echo is correlated with a one-microsecond pulse. Parabolic refinement locates the peak but does not add bandwidth.

**Builds on:** [P02 — See Sampling as Taking Measurements](/courses/dsp-radar/modules/02-see-sampling-as-taking-measurements); [P08 — Use Correlation to Find a Hidden Pattern](/courses/dsp-radar/modules/08-use-correlation-to-find-a-hidden-pattern); [P29 — Build a Radar Power-Budget Experiment](/courses/dsp-radar/modules/29-build-a-radar-power-budget-experiment).

**Predict and investigate.** Compare sample_rate_mhz=20 and 40 with delay_us fixed. Use correlation and ranging to distinguish finer bins from an improved waveform response.

**Evidence to keep.** Write your prediction before manipulating controls. Record baseline settings, one-variable comparisons, the plotted quantity and its units, and the result after restoring the same settings. Use the existing lesson's named failure and recovery:

- Trigger: Enable broken_mode at baseline controls.
- Diagnose: Using cτ reports twice the refined monostatic range.
- Recover: Disable the failure to restore cτ/2 with identical samples and correlation.

**Browser recovery.** Turn **Enable the named failure** on to capture the fault, then off while holding the other controls at the same values. Compare the recovered evidence with that same-settings healthy run. Use **Reset parameters** to restore the original baseline.

**Explain the relation.** `R=c tau/2; Delta R_bin=c/(2 fs)`. Relate each symbol to a displayed quantity and distinguish samples, seconds, frequency, phase and any power normalization that applies.

**Check your reasoning.** At 20 MHz, sample spacing is 50 ns and monostatic range-bin spacing is about 7.5 m. A sub-bin estimator uses response shape to estimate a delay more finely; it does not create a narrower response or resolve arbitrary target pairs.

**Limit the claim.** Two-way travel gives the factor of two. Fractional-delay interpolation, sampling and the retained waveform bandwidth each have separate error limits.

**Completion standard.** A satisfactory explanation connects a prediction to measured browser evidence, uses the correct units, explains the failure causally, and identifies a model limit. Merely reproducing a favorable plot or reading this answer is not an assessment pass. No learner score or completion is stored.

Continue the domain assessment at [P40 — Compare Coherent and Noncoherent Integration](/courses/dsp-radar/modules/40-compare-coherent-and-noncoherent-integration).
