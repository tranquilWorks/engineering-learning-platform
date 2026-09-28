### DSP-F46 · Audit a detector's false-alarm claim

**Competency DSP-C46:** Guards exclude target response; training cells estimate background. Larger windows can smooth fluctuations while mixing different background powers. Inspect leakage, locality and excluded edges together.

**Builds on:** [P33 — Control Pulse-Compression Sidelobes](/courses/dsp-radar/modules/33-control-pulse-compression-sidelobes); [P45 — Implement 1-D Cell-Averaging CFAR](/courses/dsp-radar/modules/45-implement-1-d-cell-averaging-cfar).

**Predict and investigate.** Increase guard_cells, then training_cells separately. Use the threshold traces to show a case where target leakage and background locality compete.

**Evidence to keep.** Write your prediction before manipulating controls. Record baseline settings, one-variable comparisons, the plotted quantity and its units, and the result after restoring the same settings. Use the existing lesson's named failure and recovery:

- Trigger: Enable broken_mode at baseline controls.
- Diagnose: The named failure injects the source neighbor at cell 126 into the weak cell 138 reference window (T=12,G=4). Its CUT power is unchanged while its threshold rises.
- Recover: At the same contaminated scene, use G=12 and T=12 to exclude that neighbor and recover the weak target. This consumes more edge cells. Disable the toggle to restore the selected uncontaminated baseline.

**Browser recovery.** Turn **Enable the named failure** on to capture the fault, then off while holding the other controls at the same values. Compare the recovered evidence with that same-settings healthy run. Use **Reset parameters** to restore the original baseline.

**Explain the relation.** `threshold=alpha mean(training_power)`. Relate each symbol to a displayed quantity and distinguish samples, seconds, frequency, phase and any power normalization that applies.

**Check your reasoning.** Guards reduce leakage of target response into the estimate. More clean training cells stabilize the estimate but span a larger neighborhood that may cross clutter transitions or include other targets.

**Limit the claim.** A guard width adequate for one waveform or window can be insufficient after the target response broadens.

**Completion standard.** A satisfactory explanation connects a prediction to measured browser evidence, uses the correct units, explains the failure causally, and identifies a model limit. Merely reproducing a favorable plot or reading this answer is not an assessment pass. No learner score or completion is stored.

Continue the domain assessment at [P52 — Validate CFAR Pfa by Monte Carlo](/courses/dsp-radar/modules/52-validate-cfar-pfa-by-monte-carlo).
