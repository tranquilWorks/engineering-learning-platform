### DSP-F80 · Audit coherent imaging and passive processing

**Competency DSP-C80:** A few millimeters of nonlinear path error creates order-one two-way phase error. Deramp an isolated strong range gate, integrate adjacent phase differences, and remove the common phase screen before focusing.

**Builds on:** [P16 — Create an Analytic Signal with the Hilbert Transform](/courses/dsp-radar/modules/16-create-an-analytic-signal-with-the-hilbert-transform); [P19 — Inject and Correct IQ Impairments](/courses/dsp-radar/modules/19-inject-and-correct-iq-impairments); [P75 — Build SAR Phase-History Intuition](/courses/dsp-radar/modules/75-build-sar-phase-history-intuition); [P77 — Focus SAR with Backprojection](/courses/dsp-radar/modules/77-focus-sar-with-backprojection).

**Predict and investigate.** Increase error_rms_wavelengths, then random_fraction. Compare screen and cut and explain why an isolated reference gate can estimate a common phase error.

**Evidence to keep.** Write your prediction before manipulating controls. Record baseline settings, one-variable comparisons, the plotted quantity and its units, and the result after restoring the same settings. Use the existing lesson's named failure and recovery:

- Trigger: Enable broken_mode at baseline controls.
- Diagnose: The named failure mixes 0.95 of a second range gate into the reference. Its different geometric phase contaminates the estimated common error and lowers recovered focus.
- Recover: Disable the mixed-reference failure and re-estimate from the unchanged isolated first gate. Absolute phase is unobservable here; compare centered phase and retain the known-geometry and isolated-gate assumptions.

**Browser recovery.** Turn **Enable the named failure** on to capture the fault, then off while holding the other controls at the same values. Compare the recovered evidence with that same-settings healthy run. Use **Reset parameters** to restore the original baseline.

**Explain the relation.** `phase_error_rms=4 pi path_error_rms/lambda`. Relate each symbol to a displayed quantity and distinguish samples, seconds, frequency, phase and any power normalization that applies.

**Check your reasoning.** Round-trip path error produces phase error proportional to 4 pi times error over wavelength. A suitable isolated scatterer exposes the common phase screen; contamination by another scatterer biases that estimate and can damage correction.

**Limit the claim.** Reference-based autofocus relies on scene and phase-screen assumptions. It is not a general solution for spatially varying motion errors.

**Completion standard.** A satisfactory explanation connects a prediction to measured browser evidence, uses the correct units, explains the failure causally, and identifies a model limit. Merely reproducing a favorable plot or reading this answer is not an assessment pass. No learner score or completion is stored.

Continue the domain assessment at [P83 — Compare Range-Doppler Processing with a Small STAP Processor](/courses/dsp-radar/modules/83-compare-range-doppler-processing-with-a-small-stap-processor).
