# Build a Range Sensor Model

**Guiding question:** What inputs, observable effects, and failure modes matter when you build a Range Sensor Model?

## Concept and prediction

A range sensor does not directly report the perpendicular distance to a surface. It reports distance along a ray, then adds noise, bias, quantization, missed returns, and saturation. Keeping geometry and sensor imperfections separate makes residuals diagnosable.

Before running the model, predict how a 3 m wall distance changes when the beam rotates from 0 deg to 60 deg. Also predict whether zero-mean noise can repair a biased geometric model.

## Model, symbols, and equations

- $$r_{\mathrm{true}}=d/\cos\theta$$ — intersection range for a planar wall whose normal is aligned with the sensor x-axis.
- $$z_k=\operatorname{clip}(r_{\mathrm{true}}+n_k,0,r_{\max})$$ — bounded measurement model.
- $$e_k=z_k-r_{\mathrm{model}}$$ — innovation or residual used to judge the model.

Symbols and units:

- $d$ — perpendicular wall distance (m).
- $\theta$ — beam angle from the wall normal (deg at the control, rad internally).
- $n_k$ — zero-mean deterministic test-noise sequence with selected standard deviation (m).
- $r_{\max}$ — maximum reportable range (m).

The sensor origin is at $(0,0)$, +x follows the wall normal, and positive angles rotate counterclockwise. Range is nonnegative.

## Manipulation: two one-variable sweeps

1. Sweep `beam_angle_deg` through [0,30,60] while holding the wall fixed. The slant range should follow the secant curve and double at 60 deg.
2. Restore baseline, then sweep `noise_std_m` through [0,0.02,0.2]. The residual RMS should grow while its mean remains near the geometric modeling error.

The sample plot separates repeatability from model bias. The angle plot exposes the geometric mechanism and the saturation ceiling. Every axis states its unit.

## Evidence and limiting cases

The retained expected vectors use a closed-form ray-plane intersection and a normalized independent noise pattern. The production experiment generates the measurement trace and diagnostic signature separately.

- At $\theta=0$, slant range equals perpendicular distance.
- As $|\theta|$ approaches 90 deg, ideal range grows without bound and a finite sensor saturates.
- At zero noise, any residual is model or saturation error, not randomness.

This is software simulation evidence. It is not a physical range-sensor, robot, bench, HIL, field, or production result.

## Intentionally broken assumption

**Normal-incidence shortcut.** Broken mode assumes $r=d$ at every beam angle. Oblique returns then acquire a deterministic positive residual that random noise cannot average away.

## Explanation and recovery

Disable the shortcut, restore $d/\cos\theta$, and verify that residual bias collapses until saturation dominates. Recovery is complete only when you can distinguish geometric error, random spread, and clipping in the plots.

## Common mistakes

- Adding sensor noise before establishing the correct ray geometry.
- Treating a maximum-range return as an ordinary unbiased sample.
- Mixing beam angle from the surface tangent with angle from the surface normal.
- Changing angle, noise, and maximum range together and losing causal attribution.

## Focused check and teach-back

At baseline, estimate the slant range by hand, cite the measured residual RMS, reproduce the broken bias, and recover it. Then teach it back: state the frame, derive the secant term, identify the saturation limit, and explain why averaging cannot fix the wrong geometry.


## Deep derivation and conventions

The depth target for this module is to **derive beam/range noise, clipping, dropout, and inverse observation assumptions**. Start from the physical or geometric constraint, not from the plotted curve. State which quantities are inputs, which are states, and which are observations; then carry the coordinate, sign, frame, sampling, or energy convention through every substitution. The retained convention is: The sensor is at the origin, +x follows the wall normal, and positive beam angle is counterclockwise.

The governing relations are:

- $$r=d/cos(theta)$$ — A planar-wall ray range grows with beam angle from the surface normal.
- $$z=clip(r+n,0,r_max)$$ — Noise and saturation act after geometry.

Read those equations as a chain of claims. The first relation establishes the mechanism; subsequent relations map it into a prediction that the experiment can expose. A derivation is incomplete if it drops a frame label, silently changes a sign, or combines unlike units. Here the unit ledger is: distance and range: m; beam angle: deg control, rad internal; noise: m. Before running Python, identify the dimensional unit of every term on both sides of one equation. If the units do not close, a numerical match is accidental.

For a local linearization, discrete update, or geometric approximation, also state its domain. “Correct at the baseline” is weaker than “correct for the declared range under the declared assumptions.” This distinction matters because a robot can produce a smooth and plausible trajectory while violating the modeled constraint. The experiment therefore pairs the response plot with a mechanism or residual plot: one shows what happened, while the other tests why the explanation is credible.

## Alternative formulation and limiting analysis

The required comparison is to **compare no return, maximum range, and zero-noise limits**. Work this comparison before tuning. An alternative formulation should agree on an invariant even if its intermediate coordinates differ; a limiting case should emerge continuously as a parameter approaches its boundary. A branch switch, singular limit, or zero denominator must be handled explicitly rather than hidden by clipping.

Retained limiting checks:

- At zero angle, slant and perpendicular distance are equal.
- Near ninety degrees, ideal range diverges and a finite sensor saturates.

Use at least one as a pencil-and-paper oracle. Substitute the limiting input into the displayed equations, predict the sign and scale of the result, and then inspect the relevant metric. If the limiting result disagrees, first test the convention and the limit-taking step; do not immediately retune an unrelated parameter. This procedure separates a model defect from a parameter choice.

## Practical failure analysis and recovery

The engineering failure to diagnose is **using range as a point without sensor pose or uncertainty**. In the executable counterexample, **Normal-incidence shortcut** is triggered by: Set broken_mode true. Its observable failure is: The model substitutes perpendicular distance for oblique slant range. This is not merely a worse numerical score. It violates an assumption that must be named before the model can support a decision.

The recovery is: Set broken_mode false and intersect the ray with the wall. Recovery has three parts: remove the fault mechanism, restore the exact baseline inputs, and recheck the original invariant. A curve that looks calmer is not sufficient. The diagnostic signature must return within its retained independent-reference tolerance, and the mechanism plot must again satisfy the relevant sign, conservation, constraint, residual, timing, or consistency condition.

In practice, instrument the variable nearest the violated assumption. For geometry, log frame-resolved residuals; for dynamics and contact, log energy, effort, and saturation; for estimation, log innovations and covariance consistency; for planning and autonomy, log feasibility, guard, collision, or timing decisions. This makes the failure falsifiable and prevents a downstream controller or filter from masking it.

## Evidence workflow and formative check

Run the baseline, then preserve it while changing exactly one control per sweep:

- `beam_angle_deg` at [0, 30, 60]: Slant range follows the secant curve.
- `noise_std_m` at [0, 0.02, 0.2]: Residual RMS grows while geometric bias remains identifiable.

Before each run, write a directional prediction from one equation: increase, decrease, unchanged, or branch change. After the run, cite one metric and one plotted feature, including units. Then perform these checks:

1. **Numerical prediction:** calculate one baseline quantity to one or two significant figures without using the experiment output.
2. **Dimensional check:** show that one governing equation has consistent units.
3. **Invariant check:** identify a sign, bound, conservation relation, residual, or ordering that should survive the sweep.
4. **Counterexample:** enable the named broken case and explain which assumption fails before describing the visual symptom.
5. **Recovery:** disable the fault, restore the exact defaults, and verify the signature returns rather than merely improves.

Teach it back without referring to the plot first: state the convention, derive the relationship, predict one sweep, identify the practical failure, and explain why the recovery repairs the violated assumption. Only then use the plots as evidence. A strong answer distinguishes model validity, numerical agreement, and physical validation; none is a substitute for the others.

## Boundary and onward links

P47-P48 turn range observations into maps and registered geometry. This lesson establishes its named Robotics competency and provides prerequisites for later mapped modules; it does not absorb the adjacent course's broader theory. The Python result remains deterministic software evidence. It does not claim MATLAB runtime equivalence, learner effectiveness, browser accessibility, physical robot or HIL operation, safety certification, or production readiness.
