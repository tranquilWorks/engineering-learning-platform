### DSP-F53 · Explain a track from reports to identity

**Competency DSP-C53:** Eight-connected detection groups retain excess-power weighted centroids, extent and effective cell count. Morphology uncertainty proxies are not calibrated tracker measurement covariance.

**Builds on:** [P50 — Apply 2-D CFAR to a Range-Doppler Map](/courses/dsp-radar/modules/50-apply-2-d-cfar-to-a-range-doppler-map); [P51 — Stress CFAR with Clutter Edges, Sidelobes, and Multiple Targets](/courses/dsp-radar/modules/51-stress-cfar-with-clutter-edges-sidelobes-and-multiple-targets).

**Predict and investigate.** Compare minimum_cells 1, 3 and 18, then change weight_exponent. Explain which components survive and why a report centroid moves within an unchanged detection component.

**Evidence to keep.** Write your prediction before manipulating controls. Record baseline settings, one-variable comparisons, the plotted quantity and its units, and the result after restoring the same settings. Use the existing lesson's named failure and recovery:

- Trigger: Enable broken_mode at baseline controls.
- Diagnose: Peak-only reporting promotes disconnected sidelobes and false cells and quantizes position to cell centers.
- Recover: Restore grouping and minimum-size filtering on the identical score map; disable the toggle for exact selected-control recovery.

**Browser recovery.** Turn **Enable the named failure** on to capture the fault, then off while holding the other controls at the same values. Compare the recovered evidence with that same-settings healthy run. Use **Reset parameters** to restore the original baseline.

**Explain the relation.** `centroid=sum_i w_i position_i/sum_i w_i`. Relate each symbol to a displayed quantity and distinguish samples, seconds, frequency, phase and any power normalization that applies.

**Check your reasoning.** Connectivity groups cells, the size threshold rejects small groups, and excess-power weights set the centroid. A report's shape spread describes that cluster; it is not automatically the covariance of an unbiased target-location estimator.

**Limit the claim.** Cluster connectivity and target response can merge multiple physical targets. Report count is not a direct truth count.

**Completion standard.** A satisfactory explanation connects a prediction to measured browser evidence, uses the correct units, explains the failure causally, and identifies a model limit. Merely reproducing a favorable plot or reading this answer is not an assessment pass. No learner score or completion is stored.

Continue the domain assessment at [P60 — Use an IMM for a Maneuvering Target](/courses/dsp-radar/modules/60-use-an-imm-for-a-maneuvering-target).
