### DSP-F36 · Carry range and Doppler through a radar design

**Competency DSP-C36:** Complex samples preserve pulse-to-pulse phase. Adjacent products, an unwrapped phase slope and a windowed FFT estimate signed Doppler; frequencies outside ±PRF/2 alias.

**Builds on:** [P01 — Build a Sinusoid and a Complex Phasor](/courses/dsp-radar/modules/01-build-a-sinusoid-and-a-complex-phasor); [P20 — Estimate Tone Frequency and Phase from Noisy Samples](/courses/dsp-radar/modules/20-estimate-tone-frequency-and-phase-from-noisy-samples); [P29 — Build a Radar Power-Budget Experiment](/courses/dsp-radar/modules/29-build-a-radar-power-budget-experiment).

**Predict and investigate.** Reverse velocity_mps at the same carrier_ghz. Explain the phase slope and compare it with the magnitude-only failure.

**Evidence to keep.** Write your prediction before manipulating controls. Record baseline settings, one-variable comparisons, the plotted quantity and its units, and the result after restoring the same settings. Use the existing lesson's named failure and recovery:

- Trigger: Enable broken_mode at baseline controls.
- Diagnose: Taking magnitude first erases phase: adjacent-product Doppler becomes zero and the FFT peaks at DC.
- Recover: Disable the failure to restore coherent I/Q and the identical private-seed samples.

**Browser recovery.** Turn **Enable the named failure** on to capture the fault, then off while holding the other controls at the same values. Compare the recovered evidence with that same-settings healthy run. Use **Reset parameters** to restore the original baseline.

**Explain the relation.** `fD=2 v/lambda; Delta phi=2 pi fD/PRF`. Relate each symbol to a displayed quantity and distinguish samples, seconds, frequency, phase and any power normalization that applies.

**Check your reasoning.** Monostatic Doppler is proportional to signed radial speed and inversely proportional to wavelength. Reversing speed reverses pulse-to-pulse phase slope; magnitude removes that coherent phase history.

**Limit the claim.** Pulse sampling aliases Doppler outside its unambiguous interval. State the approach/recession convention before interpreting sign.

**Completion standard.** A satisfactory explanation connects a prediction to measured browser evidence, uses the correct units, explains the failure causally, and identifies a model limit. Merely reproducing a favorable plot or reading this answer is not an assessment pass. No learner score or completion is stored.

Continue the domain assessment at [P40 — Compare Coherent and Noncoherent Integration](/courses/dsp-radar/modules/40-compare-coherent-and-noncoherent-integration).
