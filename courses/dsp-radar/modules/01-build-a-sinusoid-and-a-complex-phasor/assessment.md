### DSP-F01 · Sample, identify and reconstruct

**Competency DSP-C01:** A real sinusoid is the in-phase projection of a constant-radius complex phasor whose angular position advances by a signed phase increment at every sample.

**Builds on:** Complex numbers, trigonometry and the course's stated entry prerequisites..

**Predict and investigate.** Set frequency_hz to its negative while preserving amplitude and phase. Explain the direction of the IQ orbit and the first sample before inspecting rotation_direction.

**Evidence to keep.** Write your prediction before manipulating controls. Record baseline settings, one-variable comparisons, the plotted quantity and its units, and the result after restoring the same settings. Use the existing lesson's named failure and recovery:

- Trigger: Enable the forced 5 Hz at 8 Sa/s alias mode.
- Diagnose: The samples admit a 3 Hz cosine explanation because 5 Hz lies above the 4 Hz Nyquist boundary.
- Recover: Disable alias mode and restore 200 Sa/s, giving 40 samples per cycle.

**Browser recovery.** Turn **Force the 5 Hz at 8 Sa/s broken case** on to capture the fault, then off while holding the other controls at the same values. Compare the recovered evidence with that same-settings healthy run. Use **Reset parameters** to restore the original baseline.

**Explain the relation.** `z[n]=A exp(j(2 pi f n/fs+phi))`. Relate each symbol to a displayed quantity and distinguish samples, seconds, frequency, phase and any power normalization that applies.

**Check your reasoning.** The initial point stays A exp(j phi); phase increments change sign. Magnitude remains A, while the real projection alone cannot generally identify rotation direction.

**Limit the claim.** Distinguish finite sampled rotation from a continuous rotating object; frequencies separated by fs are observationally equivalent. At zero frequency no cycle exists: the guarded finite samples-per-cycle readout is not a physical cycle count.

**Completion standard.** A satisfactory explanation connects a prediction to measured browser evidence, uses the correct units, explains the failure causally, and identifies a model limit. Merely reproducing a favorable plot or reading this answer is not an assessment pass. No learner score or completion is stored.

Continue the domain assessment at [P10 — Decimate and Interpolate Without Creating Artifacts](/courses/dsp-radar/modules/10-decimate-and-interpolate-without-creating-artifacts).
