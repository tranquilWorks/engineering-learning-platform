# Compare Setup Changes Quantitatively

> **Guiding question:** How can a setup comparison preserve pairing, quantify uncertainty, and avoid a confounded lap-time verdict?

## Physical model, pairing, and units

Four deterministic baseline sector times are 28, 35, 22, and 31 seconds. A candidate applies declared sector sensitivities to aero change `A`, tire-friction change `T`, and interaction `AT`. For sector `i`, `t_i,candidate = t_i,baseline(1 - 0.0008 A s_Ai - 0.002 T s_Ti - 0.00001 AT)`.

Candidate sector `i` must be paired with baseline sector `i`. Their differences sum to the lap delta. The calculation separately reports the aero main effect, tire main effect, and interaction; those contributions sum to the total delta. Paired standard error describes variation among sector deltas, while the decision rule asks whether total improvement exceeds 0.20 s. Negative delta means faster.

This is a Python-first native P23 design from a scaffold, not source- or MATLAB-runtime equivalence. Deterministic sensitivities teach comparison structure; they are not learned from track tests.

## Predict and sweep one variable at a time

1. Hold tire change at +5% and sweep aero change from -20 through +10 to +30%. Predict the aero main effect and interaction sign.
2. Restore aero +10% and sweep tire change from -10 through +5 to +15%. Predict the lap delta and threshold margin.

Do not use “faster” without a sign convention and declared threshold. Effect size and scatter answer different questions.

## Named broken behavior and exact recovery

**Broken behavior:** rotate the candidate labels so sector 2 is compared with baseline sector 1, and so on. Total candidate time happens to remain unchanged, but paired residual scatter becomes meaningless and the verdict is invalid. This is a useful warning: an aggregate can conceal broken experimental structure.

**Exact recovery:** match stable sector identities, compute differences before summaries, retain the interaction, and apply the -0.20 s threshold. Restore +10% aero and +5% tire change for the exact baseline.

## Limits and limiting cases

At zero changes all main and interaction effects vanish. With either factor zero, the interaction vanishes. The response surface is linear plus one interaction over a bounded teaching range. It omits repeat laps, weather, fuel, driver learning, tire temperature, causal randomization, confidence-interval coverage, and real measurement noise.

## Common mistakes

- Comparing different sectors because row order happens to match.
- Dropping interaction while changing two factors.
- Calling any negative delta practically meaningful.
- Treating deterministic standard error as a real sampling distribution.
- Reporting total time while hiding sector-level reversals.

## Formative checks

1. Verify that the three modeled contributions sum to lap delta.
2. Explain why a rotated pairing leaves total time unchanged.
3. State the sign and magnitude of the decision threshold.
4. Distinguish effect size, paired scatter, and causal evidence.

## Teach-back checklist

- [ ] I can preserve paired identities before aggregation.
- [ ] I predicted both one-variable sweeps.
- [ ] I can separate main effects and interaction.
- [ ] I diagnosed the named broken behavior and exact recovery.
- [ ] I can state why no track conclusion follows.

This is not measured-vehicle, driver, track, browser/learner, hardware/HIL, certification, release, or production evidence.
