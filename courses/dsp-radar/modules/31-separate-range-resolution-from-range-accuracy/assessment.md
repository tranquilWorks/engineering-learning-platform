### DSP-F31 · Carry range and Doppler through a radar design

**Competency DSP-C31:** A unit-energy Gaussian pulse separates matched-response width from isolated-target bias, standard deviation and RMSE over 128 trials.

**Builds on:** [P13 — Prove Zero-Padding Does Not Improve True Resolution](/courses/dsp-radar/modules/13-prove-zero-padding-does-not-improve-true-resolution); [P28 — Connect Thresholds to ROC Curves and Estimator Limits](/courses/dsp-radar/modules/28-connect-thresholds-to-roc-curves-and-estimator-limits); [P30 — Measure Range from Echo Delay](/courses/dsp-radar/modules/30-measure-range-from-echo-delay).

**Predict and investigate.** Compare bandwidth_mhz=2 and 8 at fixed target_separation_m, then vary separation. Use pair and accuracy to explain why an isolated target can be located more precisely than two targets can be separated.

**Evidence to keep.** Write your prediction before manipulating controls. Record baseline settings, one-variable comparisons, the plotted quantity and its units, and the result after restoring the same settings. Use the existing lesson's named failure and recovery:

- Trigger: Enable broken_mode at baseline controls.
- Diagnose: Selecting the two largest adjacent interpolated samples invents a second target within one crest.
- Recover: Disable the false count; count physical local maxima. Increase actual bandwidth to 8 MHz to resolve the baseline 22 m pair.

**Browser recovery.** Turn **Enable the named failure** on to capture the fault, then off while holding the other controls at the same values. Compare the recovered evidence with that same-settings healthy run. Use **Reset parameters** to restore the original baseline.

**Explain the relation.** `Delta R_resolution approximately c/(2 B)`. Relate each symbol to a displayed quantity and distinguish samples, seconds, frequency, phase and any power normalization that applies.

**Check your reasoning.** Larger bandwidth narrows the physical delay response. Higher SNR can reduce isolated-target location error without changing that bandwidth. Counting adjacent display samples as separate objects is not a resolution test.

**Limit the claim.** Resolution depends on the target pair, sidelobes and criterion, not only the nominal c/(2B) scale.

**Completion standard.** A satisfactory explanation connects a prediction to measured browser evidence, uses the correct units, explains the failure causally, and identifies a model limit. Merely reproducing a favorable plot or reading this answer is not an assessment pass. No learner score or completion is stored.

Continue the domain assessment at [P40 — Compare Coherent and Noncoherent Integration](/courses/dsp-radar/modules/40-compare-coherent-and-noncoherent-integration).
