# Localize with a Particle Filter

**Guiding question:** What inputs, observable effects, and failure modes matter when you localize with a Particle Filter?

## Concept and prediction

A particle filter represents a probability distribution with weighted state samples. Motion spreads hypotheses, measurement likelihoods concentrate them, and resampling allocates finite particles to the posterior. Unlike a Gaussian filter, it can preserve multiple hypotheses and cyclic state geometry.

Predict what happens to effective sample size when sensor noise becomes very small, and why more particles do not repair a wrong measurement model.

## Model, symbols, and equations

- $$x_k^{(i)}\sim p(x_k\mid x_{k-1}^{(i)},u_k)$$ — particle motion update.
- $$\tilde w_k^{(i)}=p(z_k\mid x_k^{(i)}),\quad w_k^{(i)}=\tilde w_k^{(i)}/\sum_j\tilde w_k^{(j)}$$ — likelihood and normalization.
- $$N_{\mathrm{eff}}=1/\sum_i(w_k^{(i)})^2$$ — weight-degeneracy diagnostic.

Position is measured in metres on a 20 m cyclic corridor. Positive motion advances toward increasing coordinate and wraps at 20 m. The landmark is at the wrap boundary, so its correct range is $\min(x,20-x)$.

## Manipulation: two one-variable sweeps

1. Sweep `particle_count` through [100,400,1000]. Sampling roughness should shrink, while the underlying model bias remains unchanged.
2. Restore baseline, then sweep `sensor_noise_m` through [0.1,0.4,1.5]. Narrow likelihoods concentrate belief aggressively and can collapse effective sample size.

The histogram displays the final posterior. The mechanism plot tracks position error and normalized effective sample size through each update.

## Evidence and limiting cases

Production and reference paths independently evaluate the stated deterministic bootstrap-filter recurrence; neither imports the other. The fixed quasi-noise sequence makes numerical comparisons repeatable.

- Zero motion noise preserves deterministic offsets between resampling events.
- Infinite sensor noise approaches uniform weighting and leaves motion prediction dominant.
- Increasing particle count reduces Monte Carlo granularity but cannot correct a topologically wrong range model.

This is software localization evidence, not physical ranging, robot, bench, HIL, field, or production validation.

## Intentionally broken assumption

**Non-cyclic landmark range.** Broken mode uses $|x|$ instead of the minimum wrapped distance. Particles just below 20 m then look far from the landmark even though they are physically adjacent to it.

## Explanation and recovery

Disable the non-cyclic model, compute distance on the state manifold, normalize likelihoods in a bounded way, and resample systematically. Confirm both position error and ESS behavior.

## Common mistakes

- Averaging cyclic particle coordinates arithmetically across the wrap boundary.
- Resampling unnormalized weights.
- Treating low ESS as estimation error rather than a diversity warning.
- Increasing particle count to mask a wrong motion or sensor model.

## Focused check and teach-back

At baseline, cite final cyclic error, posterior spread, and minimum ESS. Reproduce the wrap-model failure, recover it, and teach back the probability steps, units, cyclic mean, and what ESS can and cannot prove.
