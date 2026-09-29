### DSP-F62 · Defend an array estimate under mismatch

**Competency DSP-C62:** Coherent element phasors sum to the normalized array factor. Full 0.025-degree calculations measure interpolated half-power width, first nulls and sidelobes; the separate reviewed eight-element Hamming comparison shows its width/sidelobe tradeoff.

**Builds on:** [P11 — Make FFT Bins Concrete](/courses/dsp-radar/modules/11-make-fft-bins-concrete); [P12 — Separate Leakage from Noise](/courses/dsp-radar/modules/12-separate-leakage-from-noise); [P61 — See Phase Steering in a Uniform Linear Array](/courses/dsp-radar/modules/61-see-phase-steering-in-a-uniform-linear-array).

**Predict and investigate.** Compare elements=4 and 16, then increase spacing_wavelengths. Use beamwidth and alias to distinguish a narrower main beam from an unambiguous field of view.

**Evidence to keep.** Write your prediction before manipulating controls. Record baseline settings, one-variable comparisons, the plotted quantity and its units, and the result after restoring the same settings. Use the existing lesson's named failure and recovery:

- Trigger: Enable broken_mode at baseline controls.
- Diagnose: One-wavelength spacing while steering to +30 degrees produces an equally strong -30-degree grating lobe. A narrow main lobe alone is not unambiguous.
- Recover: Restore half-wavelength spacing on the same +30-degree steering case. The selected broadside scene returns exactly when the toggle is disabled.

**Browser recovery.** Turn **Enable the named failure** on to capture the fault, then off while holding the other controls at the same values. Compare the recovered evidence with that same-settings healthy run. Use **Reset parameters** to restore the original baseline.

**Explain the relation.** `array_factor=sum_m w_m exp(j m psi)`. Relate each symbol to a displayed quantity and distinguish samples, seconds, frequency, phase and any power normalization that applies.

**Check your reasoning.** Larger aperture generally narrows the mainlobe. Wider spacing can create grating lobes that match the desired beam, while taper lowers sidelobes at a beamwidth cost.

**Limit the claim.** A sharp maximum does not establish unique direction when spatial aliases are present.

**Completion standard.** A satisfactory explanation connects a prediction to measured browser evidence, uses the correct units, explains the failure causally, and identifies a model limit. Merely reproducing a favorable plot or reading this answer is not an assessment pass. No learner score or completion is stored.

Continue the domain assessment at [P68 — Build an Introductory STAP Clutter-Ridge Experiment](/courses/dsp-radar/modules/68-build-an-introductory-stap-clutter-ridge-experiment).
