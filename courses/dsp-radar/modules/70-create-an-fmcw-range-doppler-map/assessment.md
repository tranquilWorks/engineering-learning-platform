### DSP-F70 · Resolve FMCW signs, timing and motion

**Competency DSP-C70:** The 512x64 stop-and-hop scene separates two 20 m targets by signed velocity and a third at 23 m. Hann FFTs transform fast-time rows then coherent chirp columns. Tx conj(Rx) gives slow frequency -2v/lambda; the plotted velocity axis reverses that sign. Within-chirp Doppler coupling belongs to P71.

**Builds on:** [P11 — Make FFT Bins Concrete](/courses/dsp-radar/modules/11-make-fft-bins-concrete); [P36 — Measure Doppler from Pulse-to-Pulse Phase](/courses/dsp-radar/modules/36-measure-doppler-from-pulse-to-pulse-phase); [P37 — Build a Pulse-Doppler Data Matrix](/courses/dsp-radar/modules/37-build-a-pulse-doppler-data-matrix); [P42 — Create a Full Range-Doppler Map](/courses/dsp-radar/modules/42-create-a-full-range-doppler-map); [P69 — Derive FMCW Range from Beat Frequency](/courses/dsp-radar/modules/69-derive-fmcw-range-from-beat-frequency).

**Predict and investigate.** Increase fast_samples and chirps separately. Use raw, phase and map to explain which support controls fast-time versus slow-time bin spacing.

**Evidence to keep.** Write your prediction before manipulating controls. Record baseline settings, one-variable comparisons, the plotted quantity and its units, and the result after restoring the same settings. Use the existing lesson's named failure and recovery:

- Trigger: Enable broken_mode at baseline controls.
- Diagnose: Taking absolute value of range data before its slow-time FFT erases signed phase and collapses the isolated moving target near zero velocity.
- Recover: Retain the unchanged complex range data and transform the chirp dimension. Toggle off reproduces the selected coherent map exactly.

**Browser recovery.** Turn **Enable the named failure** on to capture the fault, then off while holding the other controls at the same values. Compare the recovered evidence with that same-settings healthy run. Use **Reset parameters** to restore the original baseline.

**Explain the relation.** `Delta f_slow=1/(Nchirps Tchirp)`. Relate each symbol to a displayed quantity and distinguish samples, seconds, frequency, phase and any power normalization that applies.

**Check your reasoning.** Range comes from fast-time beat frequency; velocity comes from coherent phase across chirps. Taking magnitude before slow-time processing destroys signed velocity evidence even if the range response remains recognizable.

**Limit the claim.** A longer coherent dwell assumes sufficiently stable motion and phase. More plotted samples alone do not establish independent resolution gains.

**Completion standard.** A satisfactory explanation connects a prediction to measured browser evidence, uses the correct units, explains the failure causally, and identifies a model limit. Merely reproducing a favorable plot or reading this answer is not an assessment pass. No learner score or completion is stored.

Continue the domain assessment at [P74 — Create a Micro-Doppler Spectrogram](/courses/dsp-radar/modules/74-create-a-micro-doppler-spectrogram).
