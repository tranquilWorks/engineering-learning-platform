# Compute Arm Forward Kinematics

**Guiding question:** What inputs, observable effects, and failure modes matter when you compute Arm Forward Kinematics?

## Concept and prediction

Forward kinematics composes joint rotations along a serial chain. The second link's world angle is the sum of the first and second relative joint angles.

Before running the model, predict this: Changing joint 1 rotates both links, while changing joint 2 rotates only the second link relative to the first. Record the sign and approximate scale you expect, not only “more” or “less.”

## Model, symbols, and equations

- $$x_e=L_1\cos q_1,\quad y_e=L_1\sin q_1$$ — The elbow is the endpoint of link 1.
- $$x_t=x_e+L_2\cos(q_1+q_2)$$ — The tool x coordinate includes the accumulated second-link angle.
- $$y_t=y_e+L_2\sin(q_1+q_2)$$ — The tool y coordinate uses the same accumulated angle.

Symbols and units:

- $q_1$ — base joint angle (deg at the control, rad internally).
- $q_2$ — elbow angle relative to link 1 (deg at the control, rad internally).
- $L_1,L_2$ — link lengths (m).
- $(x_e,y_e)$ and $(x_t,y_t)$ — elbow and tool positions in the base frame (m).

The base frame is right-handed with +x right and +y up. Positive joint angles are counterclockwise; $q_2=0$ means the links are collinear.

## Manipulation: two one-variable sweeps

1. Sweep `joint1_deg` through [-60,35,120] while holding the other controls at baseline. The entire arm should rigidly rotate about the base.
2. Restore baseline, then sweep `joint2_deg` through [-120,-45,60]. The elbow stays fixed while the tool sweeps a circle of radius $L_2$.

The first plot shows the physical response. The second exposes the mechanism or residual that decides whether the result is trustworthy. Every axis states its unit.

## Evidence and limiting cases

Use the metric cards and both plots to test the prediction. The retained expected vectors are produced by an independent closed-form trigonometric endpoint calculation; the actual vectors come from this Python experiment.

- At $q_1=q_2=0$, the tool is at $(L_1+L_2,0)$.
- The tool distance from the base cannot exceed $L_1+L_2$.
- Changing $q_2$ leaves the elbow coordinates unchanged.

This is simulated software evidence. It does not demonstrate a physical robot, motor, encoder, IMU, bench, HIL, field, or production result.

## Intentionally broken assumption

**Absolute second-joint angle.** The broken model projects link 2 using $q_2$ alone. It violates the serial-chain convention that the second link inherits the base rotation.

## Explanation and recovery

Disable absolute-joint-2 mode and accumulate serial joint angles before projecting each link. Recovery is complete only when the diagnostic signature returns to the independent reference tolerance and you can explain why.

## Common mistakes

- Treating a relative joint angle as a world-frame angle.
- Mixing degree-valued controls with radian-valued trigonometric functions.

- Changing several controls at once and losing causal attribution.
- Treating a plausible plot as proof without checking units, residuals, and limiting cases.

## Focused check and teach-back

At baseline, identify one equation term changed by each sweep, reproduce the broken symptom, recover it, and cite one metric plus one plot feature as evidence. Then teach it back in two minutes: state the convention, derive the governing relationship, name the failed assumption, and explain why the recovery works.


## Deep derivation and conventions

The depth target for this module is to **derive the two-link pose from ordered joint transforms**. Start from the physical or geometric constraint, not from the plotted curve. State which quantities are inputs, which are states, and which are observations; then carry the coordinate, sign, frame, sampling, or energy convention through every substitution. The retained convention is: Base +x is right, +y is up, and both relative joint angles are positive counterclockwise.

The governing relations are:

- $$p_e=L_1[cos(q_1),sin(q_1)]$$ — Link 1 locates the elbow.
- $$p_t=p_e+L_2[cos(q_1+q_2),sin(q_1+q_2)]$$ — Serial rotations accumulate at the tool.

Read those equations as a chain of claims. The first relation establishes the mechanism; subsequent relations map it into a prediction that the experiment can expose. A derivation is incomplete if it drops a frame label, silently changes a sign, or combines unlike units. Here the unit ledger is: joint controls: deg; trigonometric angles: rad; link and endpoint coordinates: m. Before running Python, identify the dimensional unit of every term on both sides of one equation. If the units do not close, a numerical match is accidental.

For a local linearization, discrete update, or geometric approximation, also state its domain. “Correct at the baseline” is weaker than “correct for the declared range under the declared assumptions.” This distinction matters because a robot can produce a smooth and plausible trajectory while violating the modeled constraint. The experiment therefore pairs the response plot with a mechanism or residual plot: one shows what happened, while the other tests why the explanation is credible.

## Alternative formulation and limiting analysis

The required comparison is to **compare equal-link symmetry and a zero-length limiting link**. Work this comparison before tuning. An alternative formulation should agree on an invariant even if its intermediate coordinates differ; a limiting case should emerge continuously as a parameter approaches its boundary. A branch switch, singular limit, or zero denominator must be handled explicitly rather than hidden by clipping.

Retained limiting checks:

- Zero joint angles fully extend the arm on +x.
- Tool radius never exceeds L1+L2.

Use at least one as a pencil-and-paper oracle. Substitute the limiting input into the displayed equations, predict the sign and scale of the result, and then inspect the relevant metric. If the limiting result disagrees, first test the convention and the limit-taking step; do not immediately retune an unrelated parameter. This procedure separates a model defect from a parameter choice.

## Practical failure analysis and recovery

The engineering failure to diagnose is **degrees/radians and link-order mistakes**. In the executable counterexample, **Absolute second-joint angle** is triggered by: Set broken_mode true. Its observable failure is: Link 2 uses q2 instead of q1+q2. This is not merely a worse numerical score. It violates an assumption that must be named before the model can support a decision.

The recovery is: Set broken_mode false and accumulate upstream joint angles. Recovery has three parts: remove the fault mechanism, restore the exact baseline inputs, and recheck the original invariant. A curve that looks calmer is not sufficient. The diagnostic signature must return within its retained independent-reference tolerance, and the mechanism plot must again satisfy the relevant sign, conservation, constraint, residual, timing, or consistency condition.

In practice, instrument the variable nearest the violated assumption. For geometry, log frame-resolved residuals; for dynamics and contact, log energy, effort, and saturation; for estimation, log innovations and covariance consistency; for planning and autonomy, log feasibility, guard, collision, or timing decisions. This makes the failure falsifiable and prevents a downstream controller or filter from masking it.

## Evidence workflow and formative check

Run the baseline, then preserve it while changing exactly one control per sweep:

- `joint1_deg` at [-60, 35, 120]: The whole arm rotates about the base.
- `joint2_deg` at [-120, -45, 60]: The tool circles a fixed elbow.

Before each run, write a directional prediction from one equation: increase, decrease, unchanged, or branch change. After the run, cite one metric and one plotted feature, including units. Then perform these checks:

1. **Numerical prediction:** calculate one baseline quantity to one or two significant figures without using the experiment output.
2. **Dimensional check:** show that one governing equation has consistent units.
3. **Invariant check:** identify a sign, bound, conservation relation, residual, or ordering that should survive the sweep.
4. **Counterexample:** enable the named broken case and explain which assumption fails before describing the visual symptom.
5. **Recovery:** disable the fault, restore the exact defaults, and verify the signature returns rather than merely improves.

Teach it back without referring to the plot first: state the convention, derive the relationship, predict one sweep, identify the practical failure, and explain why the recovery repairs the violated assumption. Only then use the plots as evidence. A strong answer distinguishes model validity, numerical agreement, and physical validation; none is a substitute for the others.

## Boundary and onward links

P26-P28 provide the spatial and differential continuation. This lesson establishes its named Robotics competency and provides prerequisites for later mapped modules; it does not absorb the adjacent course's broader theory. The Python result remains deterministic software evidence. It does not claim MATLAB runtime equivalence, learner effectiveness, browser accessibility, physical robot or HIL operation, safety certification, or production readiness.
