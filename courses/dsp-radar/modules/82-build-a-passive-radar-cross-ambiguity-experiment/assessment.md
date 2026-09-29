### DSP-F82 · Audit coherent imaging and passive processing

**Competency DSP-C82:** Cross-ambiguity multiplies surveillance by a conjugate delayed reference and a negative trial Doppler phasor before coherent summation. Least-squares direct-path cancellation reveals the delayed target.

**Builds on:** [P08 — Use Correlation to Find a Hidden Pattern](/courses/dsp-radar/modules/08-use-correlation-to-find-a-hidden-pattern); [P26 — Use LMS to Cancel an Interferer](/courses/dsp-radar/modules/26-use-lms-to-cancel-an-interferer); [P34 — Plot and Interpret the Ambiguity Function](/courses/dsp-radar/modules/34-plot-and-interpret-the-ambiguity-function); [P36 — Measure Doppler from Pulse-to-Pulse Phase](/courses/dsp-radar/modules/36-measure-doppler-from-pulse-to-pulse-phase); [P45 — Implement 1-D Cell-Averaging CFAR](/courses/dsp-radar/modules/45-implement-1-d-cell-averaging-cfar).

**Predict and investigate.** Increase target_delay_samples, then degrade reference_quality_db. Use raw, active and recovery to separate direct-path suppression from target contrast.

**Evidence to keep.** Write your prediction before manipulating controls. Record baseline settings, one-variable comparisons, the plotted quantity and its units, and the result after restoring the same settings. Use the existing lesson's named failure and recovery:

- Trigger: Enable broken_mode at baseline controls.
- Diagnose: Cancelling only 20 percent of the estimated direct term leaves the origin dominant. Poor reference quality also limits cancellation and coherent matching.
- Recover: Disable the failure to subtract the full estimated coefficient from the unchanged measured channels. Delay measures bistatic excess path c tau; geometry is still needed for target position.

**Browser recovery.** Turn **Enable the named failure** on to capture the fault, then off while holding the other controls at the same values. Compare the recovered evidence with that same-settings healthy run. Use **Reset parameters** to restore the original baseline.

**Explain the relation.** `excess_bistatic_path=c tau`. Relate each symbol to a displayed quantity and distinguish samples, seconds, frequency, phase and any power normalization that applies.

**Check your reasoning.** The cross-ambiguity delay measures excess bistatic path, so its length is c tau rather than the monostatic c tau/2. A noisy reference limits both coherent correlation and cancellation; removing a strong direct path can reveal a weaker echo.

**Limit the claim.** Excess path is not distance from a single sensor. Localization additionally requires transmitter/receiver geometry and enough independent constraints.

**Completion standard.** A satisfactory explanation connects a prediction to measured browser evidence, uses the correct units, explains the failure causally, and identifies a model limit. Merely reproducing a favorable plot or reading this answer is not an assessment pass. No learner score or completion is stored.

Continue the domain assessment at [P83 — Compare Range-Doppler Processing with a Small STAP Processor](/courses/dsp-radar/modules/83-compare-range-doppler-processing-with-a-small-stap-processor).
