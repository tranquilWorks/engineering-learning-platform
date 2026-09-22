# Solve Inverse Kinematics

**Guiding question:** What inputs, observable effects, and failure modes matter when you solve Inverse Kinematics?

## Concept and prediction

Inverse kinematics uses the law of cosines to find the elbow angle, then subtracts the triangle's internal angle from the target bearing to find the shoulder angle.

Before running the model, predict this: A reachable target generally has two mirror-image elbow branches with the same tool position. Record the sign and approximate scale you expect, not only “more” or “less.”

## Model, symbols, and equations

- $$c_2=\frac{x_d^2+y_d^2-L_1^2-L_2^2}{2L_1L_2}$$ — The law of cosines determines the elbow cosine.
- $$q_2=\operatorname{atan2}(\pm\sqrt{1-c_2^2},c_2)$$ — The sign selects elbow-up or elbow-down.
- $$q_1=\operatorname{atan2}(y_d,x_d)-\operatorname{atan2}(L_2\sin q_2,L_1+L_2\cos q_2)$$ — The shoulder correction aligns the link triangle with the target bearing.

Symbols and units:

- $(x_d,y_d)$ — requested tool target in the base frame (m).
- $L_1,L_2$ — link lengths (m).
- $q_1,q_2$ — solved shoulder and relative elbow angles (rad internally, deg in metrics).
- $c_2$ — dimensionless law-of-cosines value; reachability requires $|c_2|\le1$.

The base frame uses +x right, +y up, and positive counterclockwise angles. Elbow-up chooses the negative square-root branch in this declared convention.

## Manipulation: two one-variable sweeps

1. Sweep `target_x_m` through [0.4,1,1.4] while holding the other controls at baseline. Watch conditioning worsen near the outer reach boundary.
2. Restore baseline, then sweep `target_y_m` through [-0.8,0.4,1]. Confirm the shoulder angle follows the target quadrant.

The first plot shows the physical response. The second exposes the mechanism or residual that decides whether the result is trustworthy. Every axis states its unit.

## Evidence and limiting cases

Use the metric cards and both plots to test the prediction. The retained expected vectors are produced by an independent law-of-cosines solution followed by an independent forward-kinematics round trip; the actual vectors come from this Python experiment.

- Reachable radius lies between $|L_1-L_2|$ and $L_1+L_2$.
- At a fully extended boundary, both branches merge at $q_2=0$.
- An unreachable target is projected only for visualization and must retain a nonzero target residual.

This is simulated software evidence. It does not demonstrate a physical robot, motor, encoder, IMU, bench, HIL, field, or production result.

## Intentionally broken assumption

**Missing shoulder correction.** The broken solver points link 1 directly at the target and still applies the elbow angle. The tool misses the target even though the law-of-cosines elbow value looks plausible.

## Explanation and recovery

Disable the omitted-shoulder-correction mode and include the link-triangle angle in the shoulder solution. Recovery is complete only when the diagnostic signature returns to the independent reference tolerance and you can explain why.

## Common mistakes

- Clipping an unreachable target and then reporting zero original-target error.
- Selecting a branch without documenting the sign convention.

- Changing several controls at once and losing causal attribution.
- Treating a plausible plot as proof without checking units, residuals, and limiting cases.

## Focused check and teach-back

At baseline, identify one equation term changed by each sweep, reproduce the broken symptom, recover it, and cite one metric plus one plot feature as evidence. Then teach it back in two minutes: state the convention, derive the governing relationship, name the failed assumption, and explain why the recovery works.


## Deep derivation and conventions

The depth target for this module is to **derive cosine-law branches, reachability bounds, and residual checks**. Start from the physical or geometric constraint, not from the plotted curve. State which quantities are inputs, which are states, and which are observations; then carry the coordinate, sign, frame, sampling, or energy convention through every substitution. The retained convention is: Base +x is right, +y is up; elbow-up selects the negative sine branch.

The governing relations are:

- $$c_2=(x_d^2+y_d^2-L_1^2-L_2^2)/(2L_1L_2)$$ — Law of cosines determines the elbow.
- $$q_1=atan2(y_d,x_d)-atan2(L_2 sin(q_2),L_1+L_2 cos(q_2))$$ — Triangle correction determines the shoulder.

Read those equations as a chain of claims. The first relation establishes the mechanism; subsequent relations map it into a prediction that the experiment can expose. A derivation is incomplete if it drops a frame label, silently changes a sign, or combines unlike units. Here the unit ledger is: target and links: m; solution angles: deg in metrics, rad internally; residual: m. Before running Python, identify the dimensional unit of every term on both sides of one equation. If the units do not close, a numerical match is accidental.

For a local linearization, discrete update, or geometric approximation, also state its domain. “Correct at the baseline” is weaker than “correct for the declared range under the declared assumptions.” This distinction matters because a robot can produce a smooth and plausible trajectory while violating the modeled constraint. The experiment therefore pairs the response plot with a mechanism or residual plot: one shows what happened, while the other tests why the explanation is credible.

## Alternative formulation and limiting analysis

The required comparison is to **compare elbow-up/down and boundary singularity**. Work this comparison before tuning. An alternative formulation should agree on an invariant even if its intermediate coordinates differ; a limiting case should emerge continuously as a parameter approaches its boundary. A branch switch, singular limit, or zero denominator must be handled explicitly rather than hidden by clipping.

Retained limiting checks:

- Reachable radius lies between |L1-L2| and L1+L2.
- Both branches merge at full extension.

Use at least one as a pencil-and-paper oracle. Substitute the limiting input into the displayed equations, predict the sign and scale of the result, and then inspect the relevant metric. If the limiting result disagrees, first test the convention and the limit-taking step; do not immediately retune an unrelated parameter. This procedure separates a model defect from a parameter choice.

## Practical failure analysis and recovery

The engineering failure to diagnose is **silently clipping an unreachable target**. In the executable counterexample, **Missing shoulder correction** is triggered by: Set broken_mode true. Its observable failure is: The first link points directly at the target before applying q2. This is not merely a worse numerical score. It violates an assumption that must be named before the model can support a decision.

The recovery is: Set broken_mode false and restore the link-triangle correction. Recovery has three parts: remove the fault mechanism, restore the exact baseline inputs, and recheck the original invariant. A curve that looks calmer is not sufficient. The diagnostic signature must return within its retained independent-reference tolerance, and the mechanism plot must again satisfy the relevant sign, conservation, constraint, residual, timing, or consistency condition.

In practice, instrument the variable nearest the violated assumption. For geometry, log frame-resolved residuals; for dynamics and contact, log energy, effort, and saturation; for estimation, log innovations and covariance consistency; for planning and autonomy, log feasibility, guard, collision, or timing decisions. This makes the failure falsifiable and prevents a downstream controller or filter from masking it.

## Evidence workflow and formative check

Run the baseline, then preserve it while changing exactly one control per sweep:

- `target_x_m` at [0.4, 1, 1.4]: Conditioning changes near the reach boundary.
- `target_y_m` at [-0.8, 0.4, 1]: The shoulder follows the target quadrant.

Before each run, write a directional prediction from one equation: increase, decrease, unchanged, or branch change. After the run, cite one metric and one plotted feature, including units. Then perform these checks:

1. **Numerical prediction:** calculate one baseline quantity to one or two significant figures without using the experiment output.
2. **Dimensional check:** show that one governing equation has consistent units.
3. **Invariant check:** identify a sign, bound, conservation relation, residual, or ordering that should survive the sweep.
4. **Counterexample:** enable the named broken case and explain which assumption fails before describing the visual symptom.
5. **Recovery:** disable the fault, restore the exact defaults, and verify the signature returns rather than merely improves.

Teach it back without referring to the plot first: state the convention, derive the relationship, predict one sweep, identify the practical failure, and explain why the recovery repairs the violated assumption. Only then use the plots as evidence. A strong answer distinguishes model validity, numerical agreement, and physical validation; none is a substitute for the others.

## Boundary and onward links

P28-P29 own Jacobian conditioning and redundant inverse kinematics. This lesson establishes its named Robotics competency and provides prerequisites for later mapped modules; it does not absorb the adjacent course's broader theory. The Python result remains deterministic software evidence. It does not claim MATLAB runtime equivalence, learner effectiveness, browser accessibility, physical robot or HIL operation, safety certification, or production readiness.
