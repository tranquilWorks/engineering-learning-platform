### DSP-F41 · Audit a detector's false-alarm claim

**Competency DSP-C41:** Clutter has a range-dependent mean and memory. Swerling I/III hold power through a dwell; II/IV redraw every pulse. Equal average SNR does not imply equal integration stability.

**Builds on:** [P05 — Explore White, Colored, and Impulsive Noise](/courses/dsp-radar/modules/05-explore-white-colored-and-impulsive-noise); [P27 — Use Monte Carlo Trials Instead of One Lucky Run](/courses/dsp-radar/modules/27-use-monte-carlo-trials-instead-of-one-lucky-run); [P37 — Build a Pulse-Doppler Data Matrix](/courses/dsp-radar/modules/37-build-a-pulse-doppler-data-matrix); [P40 — Compare Coherent and Noncoherent Integration](/courses/dsp-radar/modules/40-compare-coherent-and-noncoherent-integration).

**Predict and investigate.** Increase range_correlation while holding the scene's mean-power convention fixed. Explain why different Swerling models retain different variability after pulse integration.

**Evidence to keep.** Write your prediction before manipulating controls. Record baseline settings, one-variable comparisons, the plotted quantity and its units, and the result after restoring the same settings. Use the existing lesson's named failure and recovery:

- Trigger: Enable broken_mode at baseline controls.
- Diagnose: One global white-background threshold overspends false alarms near the radar and underspends them farther away.
- Recover: Normalize by the known local expected clutter-plus-noise power. This is an oracle-background comparison, not an estimated CFAR algorithm; disable the toggle to replay it.

**Browser recovery.** Turn **Enable the named failure** on to capture the fault, then off while holding the other controls at the same values. Compare the recovered evidence with that same-settings healthy run. Use **Reset parameters** to restore the original baseline.

**Explain the relation.** `P=abs(z)^2 (normalized power); amplitude=sqrt(P)`. Relate each symbol to a displayed quantity and distinguish samples, seconds, frequency, phase and any power normalization that applies.

**Check your reasoning.** Within-dwell persistence versus pulse-to-pulse fluctuation determines how averaging reduces target-power variation. Correlation and spatially changing clutter power violate the simple identical-independent background assumed by many threshold formulas.

**Limit the claim.** The model is synthetic and finite. Matching its mean power does not validate a real clutter distribution or target fluctuation model.

**Completion standard.** A satisfactory explanation connects a prediction to measured browser evidence, uses the correct units, explains the failure causally, and identifies a model limit. Merely reproducing a favorable plot or reading this answer is not an assessment pass. No learner score or completion is stored.

Continue the domain assessment at [P52 — Validate CFAR Pfa by Monte Carlo](/courses/dsp-radar/modules/52-validate-cfar-pfa-by-monte-carlo).
