# Transform Coordinates Between Frames

**Guiding question:** What inputs, observable effects, and failure modes matter when you transform Coordinates Between Frames?

## Concept and prediction

A rigid transform combines a rotation with a translation. Order and frame labels matter: rotating a body-frame vector and then adding the world-frame origin is not interchangeable with translating first.

Before running the model, predict this: A positive heading rotates body +x toward world +y before the robot-origin translation is added. Record the sign and approximate scale you expect, not only “more” or “less.”

## Model, symbols, and equations

- $${}^{W}\!p=R(\theta){}^{B}\!p+{}^{W}\!t_B$$ — Rotate the body-frame point, then translate it into the world frame.
- $$R(\theta)=\begin{bmatrix}\cos\theta&-\sin\theta\\\sin\theta&\cos\theta\end{bmatrix}$$ — Positive angles rotate counterclockwise in the x-y plane.
- $${}^{B}\!p=R(\theta)^T({}^{W}\!p-{}^{W}\!t_B)$$ — The inverse subtracts translation before applying the transpose.

Symbols and units:

- $R$ — dimensionless planar rotation matrix.
- $\theta$ — robot heading (degrees in the control, radians inside trigonometry).
- ${}^{B}p$ — point coordinates in the robot/body frame (m).
- ${}^{W}t_B$ and ${}^{W}p$ — robot origin and point in the world frame (m).

Frames are right-handed with +x forward/right and +y left/up. Superscripts name the coordinate frame; positive angles are counterclockwise.

## Manipulation: two one-variable sweeps

1. Sweep `heading_deg` through [-90,30,120] while holding the other controls at baseline. Trace how the same body point rotates around the robot origin.
2. Restore baseline, then sweep `point_x_m` through [-1,1.2,2.5]. Confirm that translation does not change the vector's length from the robot origin.

The first plot shows the physical response. The second exposes the mechanism or residual that decides whether the result is trustworthy. Every axis states its unit.

## Evidence and limiting cases

Use the metric cards and both plots to test the prediction. The retained expected vectors are produced by an independent matrix calculation plus inverse-transform invariant; the actual vectors come from this Python experiment.

- At $\theta=0$, the result is the body point plus the robot translation.
- At $\theta=90^\circ$, body $(x,y)$ maps to world offset $(-y,x)$.
- Forward then inverse transformation must recover the original point to roundoff.

This is simulated software evidence. It does not demonstrate a physical robot, motor, encoder, IMU, bench, HIL, field, or production result.

## Intentionally broken assumption

**Rotation-sign mismatch.** The forward transform uses $R(-\theta)$ while the inverse still assumes $R(\theta)$. The round-trip residual exposes the inconsistent frame convention.

## Explanation and recovery

Disable the reversed-rotation mode and use one declared body-to-world rotation convention in both directions. Recovery is complete only when the diagnostic signature returns to the independent reference tolerance and you can explain why.

## Common mistakes

- Feeding degrees directly to sine and cosine functions that expect radians.
- Adding translation before rotation without stating which frame contains the translation.

- Changing several controls at once and losing causal attribution.
- Treating a plausible plot as proof without checking units, residuals, and limiting cases.

## Focused check and teach-back

At baseline, identify one equation term changed by each sweep, reproduce the broken symptom, recover it, and cite one metric plus one plot feature as evidence. Then teach it back in two minutes: state the convention, derive the governing relationship, name the failed assumption, and explain why the recovery works.


## Deep derivation and conventions

The depth target for this module is to **derive homogeneous composition and inverse transforms under one frame notation**. Start from the physical or geometric constraint, not from the plotted curve. State which quantities are inputs, which are states, and which are observations; then carry the coordinate, sign, frame, sampling, or energy convention through every substitution. The retained convention is: Right-handed x-y frames use positive counterclockwise heading; degrees are converted to radians.

The governing relations are:

- $$p_W=R(theta)p_B+t_WB$$ — Rotate in the body frame, then translate in the world frame.
- $$p_B=R(theta)^T(p_W-t_WB)$$ — The inverse subtracts translation before transposed rotation.

Read those equations as a chain of claims. The first relation establishes the mechanism; subsequent relations map it into a prediction that the experiment can expose. A derivation is incomplete if it drops a frame label, silently changes a sign, or combines unlike units. Here the unit ledger is: position: m; heading control: deg; trigonometric angle: rad. Before running Python, identify the dimensional unit of every term on both sides of one equation. If the units do not close, a numerical match is accidental.

For a local linearization, discrete update, or geometric approximation, also state its domain. “Correct at the baseline” is weaker than “correct for the declared range under the declared assumptions.” This distinction matters because a robot can produce a smooth and plausible trajectory while violating the modeled constraint. The experiment therefore pairs the response plot with a mechanism or residual plot: one shows what happened, while the other tests why the explanation is credible.

## Alternative formulation and limiting analysis

The required comparison is to **compare active versus passive interpretation and a round trip**. Work this comparison before tuning. An alternative formulation should agree on an invariant even if its intermediate coordinates differ; a limiting case should emerge continuously as a parameter approaches its boundary. A branch switch, singular limit, or zero denominator must be handled explicitly rather than hidden by clipping.

Retained limiting checks:

- Zero heading reduces to translation.
- Forward then inverse transformation recovers the input point.

Use at least one as a pencil-and-paper oracle. Substitute the limiting input into the displayed equations, predict the sign and scale of the result, and then inspect the relevant metric. If the limiting result disagrees, first test the convention and the limit-taking step; do not immediately retune an unrelated parameter. This procedure separates a model defect from a parameter choice.

## Practical failure analysis and recovery

The engineering failure to diagnose is **frame-order and handedness mismatch**. In the executable counterexample, **Rotation-sign mismatch** is triggered by: Set broken_mode true. Its observable failure is: Forward rotation uses the opposite sign from the inverse. This is not merely a worse numerical score. It violates an assumption that must be named before the model can support a decision.

The recovery is: Set broken_mode false and use the declared rotation in both directions. Recovery has three parts: remove the fault mechanism, restore the exact baseline inputs, and recheck the original invariant. A curve that looks calmer is not sufficient. The diagnostic signature must return within its retained independent-reference tolerance, and the mechanism plot must again satisfy the relevant sign, conservation, constraint, residual, timing, or consistency condition.

In practice, instrument the variable nearest the violated assumption. For geometry, log frame-resolved residuals; for dynamics and contact, log energy, effort, and saturation; for estimation, log innovations and covariance consistency; for planning and autonomy, log feasibility, guard, collision, or timing decisions. This makes the failure falsifiable and prevents a downstream controller or filter from masking it.

## Evidence workflow and formative check

Run the baseline, then preserve it while changing exactly one control per sweep:

- `heading_deg` at [-90, 30, 120]: The point rotates around the robot origin.
- `point_x_m` at [-1, 1.2, 2.5]: The vector length from robot origin is preserved.

Before each run, write a directional prediction from one equation: increase, decrease, unchanged, or branch change. After the run, cite one metric and one plotted feature, including units. Then perform these checks:

1. **Numerical prediction:** calculate one baseline quantity to one or two significant figures without using the experiment output.
2. **Dimensional check:** show that one governing equation has consistent units.
3. **Invariant check:** identify a sign, bound, conservation relation, residual, or ordering that should survive the sweep.
4. **Counterexample:** enable the named broken case and explain which assumption fails before describing the visual symptom.
5. **Recovery:** disable the fault, restore the exact defaults, and verify the signature returns rather than merely improves.

Teach it back without referring to the plot first: state the convention, derive the relationship, predict one sweep, identify the practical failure, and explain why the recovery repairs the violated assumption. Only then use the plots as evidence. A strong answer distinguishes model validity, numerical agreement, and physical validation; none is a substitute for the others.

## Boundary and onward links

P26-P27 extend this planar foundation to SE(3), twists, screws, and adjoints. This lesson establishes its named Robotics competency and provides prerequisites for later mapped modules; it does not absorb the adjacent course's broader theory. The Python result remains deterministic software evidence. It does not claim MATLAB runtime equivalence, learner effectiveness, browser accessibility, physical robot or HIL operation, safety certification, or production readiness.
