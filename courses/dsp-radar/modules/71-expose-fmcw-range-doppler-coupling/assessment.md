### DSP-F71 · Resolve FMCW signs, timing and motion

**Competency DSP-C71:** With approaching-positive velocity, Rx has +fd but Tx conj(Rx) yields fbeat=S tau-fd. The frozen-delay 45 m model measures lag-one signed frequency. A single chirp cannot identify both range and velocity; correction uses independently supplied velocity.

**Builds on:** [P36 — Measure Doppler from Pulse-to-Pulse Phase](/courses/dsp-radar/modules/36-measure-doppler-from-pulse-to-pulse-phase); [P69 — Derive FMCW Range from Beat Frequency](/courses/dsp-radar/modules/69-derive-fmcw-range-from-beat-frequency); [P70 — Create an FMCW Range-Doppler Map](/courses/dsp-radar/modules/70-create-an-fmcw-range-doppler-map).

**Predict and investigate.** Reverse velocity_mps at fixed bandwidth_mhz, then increase bandwidth. Explain the signed bias in ranges when a moving target is interpreted with the stationary formula.

**Evidence to keep.** Write your prediction before manipulating controls. Record baseline settings, one-variable comparisons, the plotted quantity and its units, and the result after restoring the same settings. Use the existing lesson's named failure and recovery:

- Trigger: Enable broken_mode at baseline controls.
- Diagnose: Subtracting fd again gives the wrong-sign correction and doubles the ideal stationary range bias.
- Recover: Add the independently known signed fd to the unchanged beat before converting delay to range.

**Browser recovery.** Turn **Enable the named failure** on to capture the fault, then off while holding the other controls at the same values. Compare the recovered evidence with that same-settings healthy run. Use **Reset parameters** to restore the original baseline.

**Explain the relation.** `f_beat=S tau-fD; stationary_range_bias=-c fD/(2 S)`. Relate each symbol to a displayed quantity and distinguish samples, seconds, frequency, phase and any power normalization that applies.

**Check your reasoning.** A beat contains both delay and Doppler under the chosen convention. The same beat can represent multiple range/speed pairs; increasing slope reduces the range-equivalent Doppler bias, but correction needs independent velocity information.

**Limit the claim.** One chirp's beat alone cannot identify both unknowns without additional assumptions or measurements.

**Completion standard.** A satisfactory explanation connects a prediction to measured browser evidence, uses the correct units, explains the failure causally, and identifies a model limit. Merely reproducing a favorable plot or reading this answer is not an assessment pass. No learner score or completion is stored.

Continue the domain assessment at [P74 — Create a Micro-Doppler Spectrogram](/courses/dsp-radar/modules/74-create-a-micro-doppler-spectrogram).
