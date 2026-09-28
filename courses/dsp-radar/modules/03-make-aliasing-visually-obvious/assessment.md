### DSP-F03 · Sample, identify and reconstruct

**Competency DSP-C03:** A sampler is a clock that records one amplitude every `1/fs` seconds. It does not count the oscillations that occur between clock ticks. If two continuous tones land on the same amplitude at every tick, the stored sequence cannot tell which tone was present. P02 established that samples are timed measurements rather than a continuous line. P03 follows that consequence into frequency: a continuous tone can make several whole turns between measurements without leaving evidence of those extra turns.

**Builds on:** [P02 — See Sampling as Taking Measurements](/courses/dsp-radar/modules/02-see-sampling-as-taking-measurements).

**Predict and investigate.** At 700 Hz input and 1000 samples/s, predict the signed and apparent alias. Use phase_check to decide whether a 300 Hz cosine needs the original or reversed phase.

**Evidence to keep.** Write your prediction before manipulating controls. Record baseline settings, one-variable comparisons, the plotted quantity and its units, and the result after restoring the same settings. Use the existing lesson's named failure and recovery:

- Trigger: Enable broken_mode.
- Diagnose: Keep the original phase after a negative signed fold, making the reflected alias miss the samples.
- Recover: Reverse phase after reflection and verify frequency independently from the sample recurrence.

**Browser recovery.** Turn **Violate the central model assumption** on to capture the fault, then off while holding the other controls at the same values. Compare the recovered evidence with that same-settings healthy run. Use **Reset parameters** to restore the original baseline.

**Explain the relation.** `f_alias=((f+fs/2) mod fs)-fs/2`. Relate each symbol to a displayed quantity and distinguish samples, seconds, frequency, phase and any power normalization that applies.

**Check your reasoning.** The signed alias is -300 Hz and the apparent real frequency is 300 Hz. Reversing the cosine frequency reverses its phase convention; matching only the spectral peak misses the broken phase reconstruction.

**Limit the claim.** At Nyquist, the signed endpoint convention is ambiguous; finite real samples alone cannot resolve the original analog frequency.

**Completion standard.** A satisfactory explanation connects a prediction to measured browser evidence, uses the correct units, explains the failure causally, and identifies a model limit. Merely reproducing a favorable plot or reading this answer is not an assessment pass. No learner score or completion is stored.

Continue the domain assessment at [P10 — Decimate and Interpolate Without Creating Artifacts](/courses/dsp-radar/modules/10-decimate-and-interpolate-without-creating-artifacts).
