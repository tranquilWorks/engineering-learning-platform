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


## Deep derivation and conventions

The depth target for this module is to **derive importance weighting, effective sample size, and resampling**. Start from the physical or geometric constraint, not from the plotted curve. State which quantities are inputs, which are states, and which are observations; then carry the coordinate, sign, frame, sampling, or energy convention through every substitution. The retained convention is: Position increases around a 20 m cyclic corridor and wraps at 20 m; landmark distance uses the shorter wrapped arc.

The governing relations are:

- $$w_i proportional to p(z|x_i)$$ — Measurement likelihood reweights particle hypotheses.
- $$N_eff=1/sum(w_i^2)$$ — Effective sample size reports weight concentration.

Read those equations as a chain of claims. The first relation establishes the mechanism; subsequent relations map it into a prediction that the experiment can expose. A derivation is incomplete if it drops a frame label, silently changes a sign, or combines unlike units. Here the unit ledger is: position and noise: m; weights and ESS fraction: dimensionless; particle count: particles. Before running Python, identify the dimensional unit of every term on both sides of one equation. If the units do not close, a numerical match is accidental.

For a local linearization, discrete update, or geometric approximation, also state its domain. “Correct at the baseline” is weaker than “correct for the declared range under the declared assumptions.” This distinction matters because a robot can produce a smooth and plausible trajectory while violating the modeled constraint. The experiment therefore pairs the response plot with a mechanism or residual plot: one shows what happened, while the other tests why the explanation is credible.

## Alternative formulation and limiting analysis

The required comparison is to **compare uniform weights, likelihood collapse, and particle-count scaling**. Work this comparison before tuning. An alternative formulation should agree on an invariant even if its intermediate coordinates differ; a limiting case should emerge continuously as a parameter approaches its boundary. A branch switch, singular limit, or zero denominator must be handled explicitly rather than hidden by clipping.

Retained limiting checks:

- Infinite sensor noise approaches uniform weighting.
- Zero motion noise preserves deterministic particle offsets between resampling events.

Use at least one as a pencil-and-paper oracle. Substitute the limiting input into the displayed equations, predict the sign and scale of the result, and then inspect the relevant metric. If the limiting result disagrees, first test the convention and the limit-taking step; do not immediately retune an unrelated parameter. This procedure separates a model defect from a parameter choice.

## Practical failure analysis and recovery

The engineering failure to diagnose is **sample impoverishment and non-deterministic evaluation**. In the executable counterexample, **Non-cyclic landmark range** is triggered by: Set broken_mode true. Its observable failure is: The likelihood uses straight coordinate distance at the wrap boundary. This is not merely a worse numerical score. It violates an assumption that must be named before the model can support a decision.

The recovery is: Set broken_mode false and evaluate measurement distance on the cyclic state manifold. Recovery has three parts: remove the fault mechanism, restore the exact baseline inputs, and recheck the original invariant. A curve that looks calmer is not sufficient. The diagnostic signature must return within its retained independent-reference tolerance, and the mechanism plot must again satisfy the relevant sign, conservation, constraint, residual, timing, or consistency condition.

In practice, instrument the variable nearest the violated assumption. For geometry, log frame-resolved residuals; for dynamics and contact, log energy, effort, and saturation; for estimation, log innovations and covariance consistency; for planning and autonomy, log feasibility, guard, collision, or timing decisions. This makes the failure falsifiable and prevents a downstream controller or filter from masking it.

## Evidence workflow and formative check

Run the baseline, then preserve it while changing exactly one control per sweep:

- `particle_count` at [100, 400, 1000]: Higher count reduces sampling granularity without repairing model bias.
- `sensor_noise_m` at [0.1, 0.4, 1.5]: Narrow likelihoods concentrate weights and reduce ESS.

Before each run, write a directional prediction from one equation: increase, decrease, unchanged, or branch change. After the run, cite one metric and one plotted feature, including units. Then perform these checks:

1. **Numerical prediction:** calculate one baseline quantity to one or two significant figures without using the experiment output.
2. **Dimensional check:** show that one governing equation has consistent units.
3. **Invariant check:** identify a sign, bound, conservation relation, residual, or ordering that should survive the sweep.
4. **Counterexample:** enable the named broken case and explain which assumption fails before describing the visual symptom.
5. **Recovery:** disable the fault, restore the exact defaults, and verify the signature returns rather than merely improves.

Teach it back without referring to the plot first: state the convention, derive the relationship, predict one sweep, identify the practical failure, and explain why the recovery repairs the violated assumption. Only then use the plots as evidence. A strong answer distinguishes model validity, numerical agreement, and physical validation; none is a substitute for the others.

## Boundary and onward links

statistics curricula own particle-method proofs; Robotics retains localization mechanics. This lesson establishes its named Robotics competency and provides prerequisites for later mapped modules; it does not absorb the adjacent course's broader theory. The Python result remains deterministic software evidence. It does not claim MATLAB runtime equivalence, learner effectiveness, browser accessibility, physical robot or HIL operation, safety certification, or production readiness.
