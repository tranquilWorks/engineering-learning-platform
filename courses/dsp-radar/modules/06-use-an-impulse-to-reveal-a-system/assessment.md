### DSP-F06 · Sample, identify and reconstruct

**Competency DSP-C06:** The pinned source develops this physical relationship from deterministic measurements.

**Builds on:** [P01 — Build a Sinusoid and a Complex Phasor](/courses/dsp-radar/modules/01-build-a-sinusoid-and-a-complex-phasor); [P02 — See Sampling as Taking Measurements](/courses/dsp-radar/modules/02-see-sampling-as-taking-measurements).

**Predict and investigate.** Increase echo_delay_samples and resonator_radius separately. Use impulse_responses and equivalence to distinguish a translated echo from a longer decaying state response.

**Evidence to keep.** Write your prediction before manipulating controls. Record baseline settings, one-variable comparisons, the plotted quantity and its units, and the result after restoring the same settings. Use the existing lesson's named failure and recovery:

- Trigger: Enable broken_mode.
- Diagnose: Use an unpadded N-point circular convolution so the echo tail wraps to the record beginning.
- Recover: Use exact linear convolution and match delay, moving-average, echo, and resonator direct forms.

**Browser recovery.** Turn **Violate the central model assumption** on to capture the fault, then off while holding the other controls at the same values. Compare the recovered evidence with that same-settings healthy run. Use **Reset parameters** to restore the original baseline.

**Explain the relation.** `y[n]=sum_k h[k] x[n-k]`. Relate each symbol to a displayed quantity and distinguish samples, seconds, frequency, phase and any power normalization that applies.

**Check your reasoning.** Delay translates the echo in samples. Increasing a stable resonator radius toward one lengthens decay; convolution with the impulse response predicts an LTI system's output only under the same initial conditions.

**Limit the claim.** A finite displayed impulse response truncates the tail. Superposition and time invariance must hold before an impulse probe can characterize arbitrary inputs.

**Completion standard.** A satisfactory explanation connects a prediction to measured browser evidence, uses the correct units, explains the failure causally, and identifies a model limit. Merely reproducing a favorable plot or reading this answer is not an assessment pass. No learner score or completion is stored.

Continue the domain assessment at [P10 — Decimate and Interpolate Without Creating Artifacts](/courses/dsp-radar/modules/10-decimate-and-interpolate-without-creating-artifacts).
