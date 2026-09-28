### DSP-F61 · Defend an array estimate under mismatch

**Competency DSP-C61:** A positive broadside angle advances arrival time and creates positive spatial phase under exp(+j2pi f t). Unwrapped least-squares and adjacent-sensor phase estimates reveal the direction.

**Builds on:** [P01 — Build a Sinusoid and a Complex Phasor](/courses/dsp-radar/modules/01-build-a-sinusoid-and-a-complex-phasor); [P17 — Perform Complex Downconversion by Hand](/courses/dsp-radar/modules/17-perform-complex-downconversion-by-hand); [P36 — Measure Doppler from Pulse-to-Pulse Phase](/courses/dsp-radar/modules/36-measure-doppler-from-pulse-to-pulse-phase).

**Predict and investigate.** Change arrival_angle_deg sign at fixed spacing_wavelengths. Use geometry and phase to reconcile propagation delay with the declared complex receive convention.

**Evidence to keep.** Write your prediction before manipulating controls. Record baseline settings, one-variable comparisons, the plotted quantity and its units, and the result after restoring the same settings. Use the existing lesson's named failure and recovery:

- Trigger: Enable broken_mode at baseline controls.
- Diagnose: At one wavelength, direction cosines .6 and -.4 produce identical sensor phasors. The wrapped step infers the wrong direction; more averaging cannot remove this ambiguity.
- Recover: Use half-wavelength spacing for the same true angle, frequency, phase and sensor count. The named noiseless alias recovery is distinct from the selected noisy scene; disable the toggle to restore that scene.

**Browser recovery.** Turn **Enable the named failure** on to capture the fault, then off while holding the other controls at the same values. Compare the recovered evidence with that same-settings healthy run. Use **Reset parameters** to restore the original baseline.

**Explain the relation.** `Delta phi=+2 pi (d/lambda) sin(theta); delay slope=-d sin(theta)/c`. Relate each symbol to a displayed quantity and distinguish samples, seconds, frequency, phase and any power normalization that applies.

**Check your reasoning.** The interelement phase increment depends on electrical spacing and sine of bearing. Reversing bearing reverses the slope; different physical spacing and wavelength can yield the same electrical spacing.

**Limit the claim.** Wrapped phases can make distinct directions indistinguishable. State angle origin and sign before applying a steering vector.

**Completion standard.** A satisfactory explanation connects a prediction to measured browser evidence, uses the correct units, explains the failure causally, and identifies a model limit. Merely reproducing a favorable plot or reading this answer is not an assessment pass. No learner score or completion is stored.

Continue the domain assessment at [P68 — Build an Introductory STAP Clutter-Ridge Experiment](/courses/dsp-radar/modules/68-build-an-introductory-stap-clutter-ridge-experiment).
