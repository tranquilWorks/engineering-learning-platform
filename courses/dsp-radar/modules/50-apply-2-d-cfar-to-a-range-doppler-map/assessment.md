### DSP-F50 · Audit a detector's false-alarm claim

**Competency DSP-C50:** The two-dimensional CA stencil is the outer rectangle minus the full guard rectangle. The exact training count sets alpha; only complete windows define calibrated tests.

**Builds on:** [P42 — Create a Full Range-Doppler Map](/courses/dsp-radar/modules/42-create-a-full-range-doppler-map); [P45 — Implement 1-D Cell-Averaging CFAR](/courses/dsp-radar/modules/45-implement-1-d-cell-averaging-cfar); [P46 — Vary CFAR Guard and Training Cells](/courses/dsp-radar/modules/46-vary-cfar-guard-and-training-cells).

**Predict and investigate.** Calculate the rectangular ring's training-cell count from the displayed inner and outer half-widths. Explain why the border target lacks a valid full stencil.

**Evidence to keep.** Write your prediction before manipulating controls. Record baseline settings, one-variable comparisons, the plotted quantity and its units, and the result after restoring the same settings. Use the existing lesson's named failure and recovery:

- Trigger: Enable broken_mode at baseline controls.
- Diagnose: Zero-padding missing border powers while retaining the full N produces artificially low finite thresholds and makes an edge target appear testable.
- Recover: Retain decisions only inside the complete-stencil eligibility mask. The border target remains untested rather than missed. Disable the toggle to restore that policy.

**Browser recovery.** Turn **Enable the named failure** on to capture the fault, then off while holding the other controls at the same values. Compare the recovered evidence with that same-settings healthy run. Use **Reset parameters** to restore the original baseline.

**Explain the relation.** `N_training=(2 Tr+1)(2 Td+1)-(2 Gr+1)(2 Gd+1), with T the outer half-widths and G the excluded guard half-widths in bins`. Relate each symbol to a displayed quantity and distinguish samples, seconds, frequency, phase and any power normalization that applies.

**Check your reasoning.** The count is outer rectangle area minus the excluded inner rectangle. Cells without the full ring are untestable under the retained rule; filling missing training cells with zeros falsely lowers their threshold.

**Limit the claim.** Untestable is different from a tested miss. A map's displayed border should not be included blindly in a Pfa denominator.

**Completion standard.** A satisfactory explanation connects a prediction to measured browser evidence, uses the correct units, explains the failure causally, and identifies a model limit. Merely reproducing a favorable plot or reading this answer is not an assessment pass. No learner score or completion is stored.

Continue the domain assessment at [P52 — Validate CFAR Pfa by Monte Carlo](/courses/dsp-radar/modules/52-validate-cfar-pfa-by-monte-carlo).
