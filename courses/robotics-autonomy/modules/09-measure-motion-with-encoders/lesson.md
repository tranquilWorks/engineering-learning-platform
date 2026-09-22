# Measure Motion with Encoders

**Guiding question:** What inputs, observable effects, and failure modes matter when you measure Motion with Encoders?

## Concept and prediction

An incremental quadrature encoder converts shaft angle into integer edge counts. Angle resolution is finite, and velocity is inferred from count differences over a sample interval.

Before running the model, predict this: More counts per revolution reduces angle quantization, while higher sample rate changes how many count increments appear in each velocity estimate. Record the sign and approximate scale you expect, not only “more” or “less.”

## Model, symbols, and equations

- $$C_k=\operatorname{round}\!\left(\frac{4N\theta_k}{2\pi}\right)$$ — Quadrature decoding yields four count edges per encoder line.
- $$\hat\theta_k=\frac{2\pi C_k}{4N}$$ — Counts reconstruct a quantized shaft angle.
- $$\hat\omega_k=\frac{\hat\theta_k-\hat\theta_{k-1}}{T_s}$$ — Sampled velocity comes from finite differences.

Symbols and units:

- $N$ — encoder lines per revolution; $C$ — cumulative quadrature edge count.
- $\theta,\hat\theta$ — true and reconstructed angle (rad).
- $\omega,\hat\omega$ — true and estimated speed (rad/s).
- $T_s$ — sample interval (s); RPM is converted by $2\pi/60$.

Positive shaft rotation increases count. The control states physical lines/rev; the decoder must explicitly apply the x4 quadrature edge factor.

## Manipulation: two one-variable sweeps

1. Sweep `counts_per_rev` through [128,1024,4096] while holding the other controls at baseline. Compare the angle-error stair steps and RMS error.
2. Restore baseline, then sweep `sample_rate_hz` through [10,50,200]. Compare velocity quantization at different count increments per sample.

The first plot shows the physical response. The second exposes the mechanism or residual that decides whether the result is trustworthy. Every axis states its unit.

## Evidence and limiting cases

Use the metric cards and both plots to test the prediction. The retained expected vectors are produced by an independent integer count equation and analytic quantization bound; the actual vectors come from this Python experiment.

- At zero speed, all counts and estimated velocities remain zero.
- Angle error magnitude is bounded by half a decoded count, $\pi/(4N)$.
- For an exact integer number of counts per sample, the velocity estimate is exact after the first sample.

This is simulated software evidence. It does not demonstrate a physical robot, motor, encoder, IMU, bench, HIL, field, or production result.

## Intentionally broken assumption

**Missing quadrature factor.** The broken decoder divides edge counts by $N$ rather than $4N$. It reports four times the true angle and speed.

## Explanation and recovery

Disable the missing-quadrature-factor mode and decode with four edges per encoder line. Recovery is complete only when the diagnostic signature returns to the independent reference tolerance and you can explain why.

## Common mistakes

- Confusing encoder lines with decoded quadrature edges.
- Computing RPM directly from counts without including sample time.

- Changing several controls at once and losing causal attribution.
- Treating a plausible plot as proof without checking units, residuals, and limiting cases.

## Focused check and teach-back

At baseline, identify one equation term changed by each sweep, reproduce the broken symptom, recover it, and cite one metric plus one plot feature as evidence. Then teach it back in two minutes: state the convention, derive the governing relationship, name the failed assumption, and explain why the recovery works.


## Deep derivation and conventions

The depth target for this module is to **derive count-to-angle conversion, wrap behavior, and quantization bound**. Start from the physical or geometric constraint, not from the plotted curve. State which quantities are inputs, which are states, and which are observations; then carry the coordinate, sign, frame, sampling, or energy convention through every substitution. The retained convention is: Positive shaft rotation increases count; the UI value is lines/rev and decoding explicitly applies x4.

The governing relations are:

- $$C_k=round(4N theta_k/(2pi))$$ — Quadrature yields four edges per encoder line.
- $$theta_hat=2pi C_k/(4N)$$ — Count scaling reconstructs quantized angle.

Read those equations as a chain of claims. The first relation establishes the mechanism; subsequent relations map it into a prediction that the experiment can expose. A derivation is incomplete if it drops a frame label, silently changes a sign, or combines unlike units. Here the unit ledger is: encoder resolution: lines/rev; count: integer edge; angle: rad; speed: rpm control and rad/s result. Before running Python, identify the dimensional unit of every term on both sides of one equation. If the units do not close, a numerical match is accidental.

For a local linearization, discrete update, or geometric approximation, also state its domain. “Correct at the baseline” is weaker than “correct for the declared range under the declared assumptions.” This distinction matters because a robot can produce a smooth and plausible trajectory while violating the modeled constraint. The experiment therefore pairs the response plot with a mechanism or residual plot: one shows what happened, while the other tests why the explanation is credible.

## Alternative formulation and limiting analysis

The required comparison is to **compare increasing resolution with a stationary shaft**. Work this comparison before tuning. An alternative formulation should agree on an invariant even if its intermediate coordinates differ; a limiting case should emerge continuously as a parameter approaches its boundary. A branch switch, singular limit, or zero denominator must be handled explicitly rather than hidden by clipping.

Retained limiting checks:

- Zero speed yields constant counts.
- Angle error is bounded by half a decoded count.

Use at least one as a pencil-and-paper oracle. Substitute the limiting input into the displayed equations, predict the sign and scale of the result, and then inspect the relevant metric. If the limiting result disagrees, first test the convention and the limit-taking step; do not immediately retune an unrelated parameter. This procedure separates a model defect from a parameter choice.

## Practical failure analysis and recovery

The engineering failure to diagnose is **missed counts, aliasing, backlash, and wrap discontinuity**. In the executable counterexample, **Missing quadrature factor** is triggered by: Set broken_mode true. Its observable failure is: Edge counts are divided by lines rather than four times lines. This is not merely a worse numerical score. It violates an assumption that must be named before the model can support a decision.

The recovery is: Set broken_mode false and decode x4 quadrature edges. Recovery has three parts: remove the fault mechanism, restore the exact baseline inputs, and recheck the original invariant. A curve that looks calmer is not sufficient. The diagnostic signature must return within its retained independent-reference tolerance, and the mechanism plot must again satisfy the relevant sign, conservation, constraint, residual, timing, or consistency condition.

In practice, instrument the variable nearest the violated assumption. For geometry, log frame-resolved residuals; for dynamics and contact, log energy, effort, and saturation; for estimation, log innovations and covariance consistency; for planning and autonomy, log feasibility, guard, collision, or timing decisions. This makes the failure falsifiable and prevents a downstream controller or filter from masking it.

## Evidence workflow and formative check

Run the baseline, then preserve it while changing exactly one control per sweep:

- `counts_per_rev` at [128, 1024, 4096]: Resolution changes quantization error.
- `sample_rate_hz` at [10, 50, 200]: Count increments per sample change speed steps.

Before each run, write a directional prediction from one equation: increase, decrease, unchanged, or branch change. After the run, cite one metric and one plotted feature, including units. Then perform these checks:

1. **Numerical prediction:** calculate one baseline quantity to one or two significant figures without using the experiment output.
2. **Dimensional check:** show that one governing equation has consistent units.
3. **Invariant check:** identify a sign, bound, conservation relation, residual, or ordering that should survive the sweep.
4. **Counterexample:** enable the named broken case and explain which assumption fails before describing the visual symptom.
5. **Recovery:** disable the fault, restore the exact defaults, and verify the signature returns rather than merely improves.

Teach it back without referring to the plot first: state the convention, derive the relationship, predict one sweep, identify the practical failure, and explain why the recovery repairs the violated assumption. Only then use the plots as evidence. A strong answer distinguishes model validity, numerical agreement, and physical validation; none is a substitute for the others.

## Boundary and onward links

DSP/Radar owns general sampling theory; Robotics retains encoder embodiment. This lesson establishes its named Robotics competency and provides prerequisites for later mapped modules; it does not absorb the adjacent course's broader theory. The Python result remains deterministic software evidence. It does not claim MATLAB runtime equivalence, learner effectiveness, browser accessibility, physical robot or HIL operation, safety certification, or production readiness.
