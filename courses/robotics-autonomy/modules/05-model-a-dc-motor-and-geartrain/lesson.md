# Model a DC Motor and Geartrain

**Guiding question:** What inputs, observable effects, and failure modes matter when you model a DC Motor and Geartrain?

## Concept and prediction

A DC motor converts current to torque and speed to back EMF. A reduction gear trades output speed for torque while reflecting load inertia and torque to the motor shaft.

Before running the model, predict this: Increasing voltage raises speed, while increasing reduction lowers output speed and reduces the motor-side load torque. Record the sign and approximate scale you expect, not only “more” or “less.”

## Model, symbols, and equations

- $$L\dot i=V-Ri-K_e\omega_m$$ — Applied voltage balances resistance, inductance, and back EMF.
- $$J_{eq}\dot\omega_m=K_t i-b\omega_m-\tau_L/N$$ — Motor torque accelerates reflected inertia and balances drag and reflected load.
- $$J_{eq}=J_m+J_L/N^2,\quad\omega_o=\omega_m/N$$ — An ideal reduction reflects inertia by $N^2$ and divides speed by $N$.

Symbols and units:

- $V$ — applied voltage (V); $i$ — armature current (A).
- $R,L$ — armature resistance (ohm) and inductance (H).
- $K_t$ — torque constant (N m/A); $K_e$ — back-EMF constant (V s/rad).
- $N$ — motor-speed/output-speed reduction ratio; $\omega_m,\omega_o$ — motor and output speed (rad/s).

Positive voltage, current, motor speed, and output speed share the drive direction. Positive load torque opposes that direction and is reflected to the motor as $\tau_L/N$.

## Manipulation: two one-variable sweeps

1. Sweep `voltage_v` through [6,12,18] while holding the other controls at baseline. Compare current transient and steady output speed.
2. Restore baseline, then sweep `gear_ratio` through [5,20,40]. Observe the speed/torque trade and reflected-load change.

The first plot shows the physical response. The second exposes the mechanism or residual that decides whether the result is trustworthy. Every axis states its unit.

## Evidence and limiting cases

Use the metric cards and both plots to test the prediction. The retained expected vectors are produced by an independent continuous-time linear state solution and steady-state torque balance; the actual vectors come from this Python experiment.

- At zero speed, back EMF is zero and current initially rises toward $V/R$.
- At steady state, both electrical and mechanical derivatives approach zero.
- With zero load torque, a larger ideal reduction lowers output speed even though motor speed is similar.

This is simulated software evidence. It does not demonstrate a physical robot, motor, encoder, IMU, bench, HIL, field, or production result.

## Intentionally broken assumption

**Missing back EMF.** The broken model sets $K_e=0$, allowing current to remain unrealistically high as speed rises. The final state disagrees with the independent continuous-time solution for the physical model.

## Explanation and recovery

Disable the no-back-EMF mode so generated voltage opposes applied voltage as speed rises. Recovery is complete only when the diagnostic signature returns to the independent reference tolerance and you can explain why.

## Common mistakes

- Multiplying load inertia by $N^2$ when reflecting it from output to motor.
- Using RPM in equations whose constants expect rad/s.

- Changing several controls at once and losing causal attribution.
- Treating a plausible plot as proof without checking units, residuals, and limiting cases.

## Focused check and teach-back

At baseline, identify one equation term changed by each sweep, reproduce the broken symptom, recover it, and cite one metric plus one plot feature as evidence. Then teach it back in two minutes: state the convention, derive the governing relationship, name the failed assumption, and explain why the recovery works.


## Deep derivation and conventions

The depth target for this module is to **derive electrical/mechanical coupling through gear ratio and reflected inertia**. Start from the physical or geometric constraint, not from the plotted curve. State which quantities are inputs, which are states, and which are observations; then carry the coordinate, sign, frame, sampling, or energy convention through every substitution. The retained convention is: Positive voltage, current, speed, and output direction agree; load torque opposes motion.

The governing relations are:

- $$L di/dt=V-Ri-K_e omega_m$$ — Voltage balances resistance, inductance, and back EMF.
- $$J_eq d omega_m/dt=K_t i-b omega_m-tau_L/N$$ — Motor torque accelerates reflected inertia and load.

Read those equations as a chain of claims. The first relation establishes the mechanism; subsequent relations map it into a prediction that the experiment can expose. A derivation is incomplete if it drops a frame label, silently changes a sign, or combines unlike units. Here the unit ledger is: voltage: V; current: A; speed: rad/s; torque: N m. Before running Python, identify the dimensional unit of every term on both sides of one equation. If the units do not close, a numerical match is accidental.

For a local linearization, discrete update, or geometric approximation, also state its domain. “Correct at the baseline” is weaker than “correct for the declared range under the declared assumptions.” This distinction matters because a robot can produce a smooth and plausible trajectory while violating the modeled constraint. The experiment therefore pairs the response plot with a mechanism or residual plot: one shows what happened, while the other tests why the explanation is credible.

## Alternative formulation and limiting analysis

The required comparison is to **compare no-load, stalled, and ideal-resistance limits**. Work this comparison before tuning. An alternative formulation should agree on an invariant even if its intermediate coordinates differ; a limiting case should emerge continuously as a parameter approaches its boundary. A branch switch, singular limit, or zero denominator must be handled explicitly rather than hidden by clipping.

Retained limiting checks:

- Initial back EMF is zero at rest.
- Steady electrical and mechanical derivatives approach zero.

Use at least one as a pencil-and-paper oracle. Substitute the limiting input into the displayed equations, predict the sign and scale of the result, and then inspect the relevant metric. If the limiting result disagrees, first test the convention and the limit-taking step; do not immediately retune an unrelated parameter. This procedure separates a model defect from a parameter choice.

## Practical failure analysis and recovery

The engineering failure to diagnose is **unit, sign, saturation, and neglected-inductance errors**. In the executable counterexample, **Missing back EMF** is triggered by: Set broken_mode true. Its observable failure is: The speed-proportional generated voltage is removed. This is not merely a worse numerical score. It violates an assumption that must be named before the model can support a decision.

The recovery is: Set broken_mode false and restore K_e omega_m. Recovery has three parts: remove the fault mechanism, restore the exact baseline inputs, and recheck the original invariant. A curve that looks calmer is not sufficient. The diagnostic signature must return within its retained independent-reference tolerance, and the mechanism plot must again satisfy the relevant sign, conservation, constraint, residual, timing, or consistency condition.

In practice, instrument the variable nearest the violated assumption. For geometry, log frame-resolved residuals; for dynamics and contact, log energy, effort, and saturation; for estimation, log innovations and covariance consistency; for planning and autonomy, log feasibility, guard, collision, or timing decisions. This makes the failure falsifiable and prevents a downstream controller or filter from masking it.

## Evidence workflow and formative check

Run the baseline, then preserve it while changing exactly one control per sweep:

- `voltage_v` at [6, 12, 18]: Voltage changes current transient and steady speed.
- `gear_ratio` at [5, 20, 40]: Reduction trades output speed for torque and reflection.

Before each run, write a directional prediction from one equation: increase, decrease, unchanged, or branch change. After the run, cite one metric and one plotted feature, including units. Then perform these checks:

1. **Numerical prediction:** calculate one baseline quantity to one or two significant figures without using the experiment output.
2. **Dimensional check:** show that one governing equation has consistent units.
3. **Invariant check:** identify a sign, bound, conservation relation, residual, or ordering that should survive the sweep.
4. **Counterexample:** enable the named broken case and explain which assumption fails before describing the visual symptom.
5. **Recovery:** disable the fault, restore the exact defaults, and verify the signature returns rather than merely improves.

Teach it back without referring to the plot first: state the convention, derive the relationship, predict one sweep, identify the practical failure, and explain why the recovery repairs the violated assumption. Only then use the plots as evidence. A strong answer distinguishes model validity, numerical agreement, and physical validation; none is a substitute for the others.

## Boundary and onward links

power electronics owns device switching and drive-circuit depth. This lesson establishes its named Robotics competency and provides prerequisites for later mapped modules; it does not absorb the adjacent course's broader theory. The Python result remains deterministic software evidence. It does not claim MATLAB runtime equivalence, learner effectiveness, browser accessibility, physical robot or HIL operation, safety certification, or production readiness.
