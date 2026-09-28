### DSP-F35 · Carry range and Doppler through a radar design

**Competency DSP-C35:** PRI=1/PRF and Ru=c/(2 PRF). Six explicit pulses show how a distant echo is assigned to the current listening interval.

**Builds on:** [P03 — Make Aliasing Visually Obvious](/courses/dsp-radar/modules/03-make-aliasing-visually-obvious); [P30 — Measure Range from Echo Delay](/courses/dsp-radar/modules/30-measure-range-from-echo-delay).

**Predict and investigate.** At prf_khz=20 and true_range_km=18, predict the apparent range in folded before running the failure case.

**Evidence to keep.** Write your prediction before manipulating controls. Record baseline settings, one-variable comparisons, the plotted quantity and its units, and the result after restoring the same settings. Use the existing lesson's named failure and recovery:

- Trigger: Enable broken_mode at baseline controls.
- Diagnose: The failure uses the transmitted pulse's true identity even though this receiver cannot observe it, reporting true range as unambiguous.
- Recover: Disable the failure to restore delay modulo PRI and the same seeded receive train. This diagnoses ambiguity; it does not recover true range.

**Browser recovery.** Turn **Enable the named failure** on to capture the fault, then off while holding the other controls at the same values. Compare the recovered evidence with that same-settings healthy run. Use **Reset parameters** to restore the original baseline.

**Explain the relation.** `R_unambiguous=c/(2 PRF)`. Relate each symbol to a displayed quantity and distinguish samples, seconds, frequency, phase and any power normalization that applies.

**Check your reasoning.** The unambiguous range is about 7.5 km using c approximately 3e8 m/s; 18 km folds to about 3 km. The receiver lacks the originating pulse index, so a precise folded delay alone cannot identify the true range.

**Limit the claim.** A second hypothesis or diversity is required to resolve ambiguity. The recorded fast-time span need not equal the full PRI range interval.

**Completion standard.** A satisfactory explanation connects a prediction to measured browser evidence, uses the correct units, explains the failure causally, and identifies a model limit. Merely reproducing a favorable plot or reading this answer is not an assessment pass. No learner score or completion is stored.

Continue the domain assessment at [P40 — Compare Coherent and Noncoherent Integration](/courses/dsp-radar/modules/40-compare-coherent-and-noncoherent-integration).
