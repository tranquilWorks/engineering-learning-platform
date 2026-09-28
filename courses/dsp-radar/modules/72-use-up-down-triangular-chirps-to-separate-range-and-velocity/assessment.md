### DSP-F72 · Resolve FMCW signs, timing and motion

**Competency DSP-C72:** Signed legs satisfy fup=S tau-fd and fdown=-S tau-fd. Their difference isolates delay and negative sum isolates Doppler. Single-target estimates use lag-one phase; the separate two-target scene uses separated interpolated FFT peaks.

**Builds on:** [P69 — Derive FMCW Range from Beat Frequency](/courses/dsp-radar/modules/69-derive-fmcw-range-from-beat-frequency); [P71 — Expose FMCW Range-Doppler Coupling](/courses/dsp-radar/modules/71-expose-fmcw-range-doppler-coupling).

**Predict and investigate.** Compare positive and negative velocity_mps at a fixed target_range_m. Use beats to identify the signed sum and difference that isolate delay and Doppler, then inspect pairing_range.

**Evidence to keep.** Write your prediction before manipulating controls. Record baseline settings, one-variable comparisons, the plotted quantity and its units, and the result after restoring the same settings. Use the existing lesson's named failure and recovery:

- Trigger: Enable broken_mode at baseline controls.
- Diagnose: Sorting signed up/down peak lists in the same order cross-pairs the two targets and creates plausible ghost reports.
- Recover: Reverse the down list for this reviewed association and solve using unchanged detections. This requires correct association evidence and is not a general multi-target matching algorithm. Disable the toggle for the selected single-target result.

**Browser recovery.** Turn **Enable the named failure** on to capture the fault, then off while holding the other controls at the same values. Compare the recovered evidence with that same-settings healthy run. Use **Reset parameters** to restore the original baseline.

**Explain the relation.** `R=c(f_up-f_down)/(4 S); v=-lambda(f_up+f_down)/4`. Relate each symbol to a displayed quantity and distinguish samples, seconds, frequency, phase and any power normalization that applies.

**Check your reasoning.** Opposite chirp slopes change the delay term's sign according to the mixer convention while Doppler retains its corresponding term. Combining correctly paired signed beats separates the unknowns; pairing different targets can create a ghost.

**Limit the claim.** The two-slope algebra does not solve multi-target association. Magnitudes alone may discard the sign information required by the equations.

**Completion standard.** A satisfactory explanation connects a prediction to measured browser evidence, uses the correct units, explains the failure causally, and identifies a model limit. Merely reproducing a favorable plot or reading this answer is not an assessment pass. No learner score or completion is stored.

Continue the domain assessment at [P74 — Create a Micro-Doppler Spectrogram](/courses/dsp-radar/modules/74-create-a-micro-doppler-spectrogram).
