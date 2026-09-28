### DSP-F04 · Sample, identify and reconstruct

**Competency DSP-C04:** P02 treated samples as measurements taken at discrete times, and P03 showed that the timing choice can make frequencies ambiguous. P04 keeps those sample times fixed and asks a different question: how precisely can each stored sample describe voltage? Imagine a ruler whose marks are voltage bins. More ADC bits add more marks inside the same input range. A wider full-scale range spaces the marks farther apart. A signal that uses only a small part of the ruler touches few marks even if many are available. A signal beyond the ruler is not measured more coarsely—it is cut off at the end, which is clipping.

**Builds on:** [P02 — See Sampling as Taking Measurements](/courses/dsp-radar/modules/02-see-sampling-as-taking-measurements).

**Predict and investigate.** Compare 6 and 7 bits at amplitude_v=0.9, then increase amplitude to the converter limit. Use error and the clipped-sample count to separate quantization from overload.

**Evidence to keep.** Write your prediction before manipulating controls. Record baseline settings, one-variable comparisons, the plotted quantity and its units, and the result after restoring the same settings. Use the existing lesson's named failure and recovery:

- Trigger: Enable broken_mode.
- Diagnose: Overdrive the ±1 V converter so saturation error exceeds the half-LSB quantization bound.
- Recover: Return the peak to 0.9 V and distinguish dithered quantization from clipping.

**Browser recovery.** Turn **Add deterministic triangular dither** on to capture the fault, then off while holding the other controls at the same values. Compare the recovered evidence with that same-settings healthy run. Use **Reset parameters** to restore the original baseline.

**Explain the relation.** `Delta=2 V_full_scale/2^B`. Relate each symbol to a displayed quantity and distinguish samples, seconds, frequency, phase and any power normalization that applies.

**Check your reasoning.** The 6-bit step over the 2 V span is 0.03125 V; 7 bits halves it. The half-step error bound applies to unclipped samples, not an overdriven waveform. Dither changes correlation as well as error power.

**Limit the claim.** The ideal 6.02 B+1.76 dB law assumes a full-scale sinusoid and a suitable quantization-error model; it is not a universal measured SQNR.

**Completion standard.** A satisfactory explanation connects a prediction to measured browser evidence, uses the correct units, explains the failure causally, and identifies a model limit. Merely reproducing a favorable plot or reading this answer is not an assessment pass. No learner score or completion is stored.

Continue the domain assessment at [P10 — Decimate and Interpolate Without Creating Artifacts](/courses/dsp-radar/modules/10-decimate-and-interpolate-without-creating-artifacts).
