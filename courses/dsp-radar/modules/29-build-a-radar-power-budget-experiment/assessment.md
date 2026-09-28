### DSP-F29 · Carry range and Doppler through a radar design

**Competency DSP-C29:** Echo power follows Pt Gt Gr λ² σ / ((4π)³ R⁴ L); noise follows kTBF. Positive margin is not detection probability.

**Builds on:** [P05 — Explore White, Colored, and Impulsive Noise](/courses/dsp-radar/modules/05-explore-white-colored-and-impulsive-noise); [P28 — Connect Thresholds to ROC Curves and Estimator Limits](/courses/dsp-radar/modules/28-connect-thresholds-to-roc-curves-and-estimator-limits).

**Predict and investigate.** Double a range on power and compare the power change with changing transmit_power_kw. Explain why agreement at one reference range cannot validate the spreading exponent.

**Evidence to keep.** Write your prediction before manipulating controls. Record baseline settings, one-variable comparisons, the plotted quantity and its units, and the result after restoring the same settings. Use the existing lesson's named failure and recovery:

- Trigger: Enable broken_mode at baseline controls.
- Diagnose: The anchored R^-2 model agrees at 40 km but loses only 20 dB per decade. It omits one propagation trip.
- Recover: Disable the failure to restore R^-4 and the same private noise bank.

**Browser recovery.** Turn **Enable the named failure** on to capture the fault, then off while holding the other controls at the same values. Compare the recovered evidence with that same-settings healthy run. Use **Reset parameters** to restore the original baseline.

**Explain the relation.** `Pr proportional to Pt sigma/R^4`. Relate each symbol to a displayed quantity and distinguish samples, seconds, frequency, phase and any power normalization that applies.

**Check your reasoning.** With the other monostatic far-field factors fixed, doubling range reduces received power by sixteen, about 12 dB. Transmit power enters linearly; doubling power cannot compensate for doubling range.

**Limit the claim.** The ideal budget omits environment-dependent propagation and target variability. A numerical margin is not a measured detection range.

**Completion standard.** A satisfactory explanation connects a prediction to measured browser evidence, uses the correct units, explains the failure causally, and identifies a model limit. Merely reproducing a favorable plot or reading this answer is not an assessment pass. No learner score or completion is stored.

Continue the domain assessment at [P40 — Compare Coherent and Noncoherent Integration](/courses/dsp-radar/modules/40-compare-coherent-and-noncoherent-integration).
