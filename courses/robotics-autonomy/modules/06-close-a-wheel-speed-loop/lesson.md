# Close a Wheel-Speed Loop

**Guiding question:** What inputs, observable effects, and failure modes matter when you close a Wheel-Speed Loop?

## Concept and prediction

A PI controller commands motor voltage from speed error. The plant and controller are sampled, and the actuator clips voltage, so discrete-time scaling and anti-windup are part of the model—not implementation details.

Before running the model, predict this: Proportional gain speeds the first correction; integral gain removes residual error but can accumulate badly during saturation. Record the sign and approximate scale you expect, not only “more” or “less.”

## Model, symbols, and equations

- $$e_k=\omega_c-\omega_k,\quad u_k=K_p e_k+K_i I_k$$ — PI feedback combines present and accumulated error.
- $$I_{k+1}=I_k+T_s e_k$$ — The integral state has units of radians and must include sample time.
- $$\omega_{k+1}=\omega_k+\frac{T_s}{\tau}(K u_{sat,k}-\omega_k)$$ — A first-order wheel plant responds to saturated voltage.

Symbols and units:

- $\omega_c,\omega$ — commanded and measured wheel speed (rad/s).
- $K_p$ — proportional gain (V/(rad/s)); $K_i$ — integral gain (V/rad).
- $I$ — accumulated angular error (rad); $T_s$ — sample interval (s).
- $u_{sat}$ — voltage after actuator saturation (V); $\tau$ — plant time constant (s).

Positive voltage produces positive wheel speed. Error is command minus measurement. Conditional integration freezes the integrator only when saturation and error would push farther into saturation.

## Manipulation: two one-variable sweeps

1. Sweep `kp_v_per_rad_s` through [0.5,1.5,3.5] while holding the other controls at baseline. Compare rise time and proportional effort before changing integral action.
2. Restore baseline, then sweep `ki_v_per_rad` through [0.5,4,10]. Compare steady error, overshoot, and saturation duration.

The first plot shows the physical response. The second exposes the mechanism or residual that decides whether the result is trustworthy. Every axis states its unit.

## Evidence and limiting cases

Use the metric cards and both plots to test the prediction. The retained expected vectors are produced by an independent separately formulated discrete recurrence with explicit saturation logic; the actual vectors come from this Python experiment.

- With $K_i=0$, proportional control can leave a steady error.
- With command zero and zero initial state, every state remains zero.
- Removing voltage saturation should make anti-windup inactive.

This is simulated software evidence. It does not demonstrate a physical robot, motor, encoder, IMU, bench, HIL, field, or production result.

## Intentionally broken assumption

**Unscaled discrete integrator.** The broken controller adds $e_k$ instead of $T_s e_k$. Its effective integral gain is one hundred times larger at the 10 ms sample time, producing saturation and windup.

## Explanation and recovery

Disable the unscaled integrator so error is accumulated as error times sample interval and saturation can pause harmful windup. Recovery is complete only when the diagnostic signature returns to the independent reference tolerance and you can explain why.

## Common mistakes

- Using continuous-time integral gain in a recurrence without multiplying by sample time.
- Judging tracking without also looking at voltage saturation and integral state.

- Changing several controls at once and losing causal attribution.
- Treating a plausible plot as proof without checking units, residuals, and limiting cases.

## Focused check and teach-back

At baseline, identify one equation term changed by each sweep, reproduce the broken symptom, recover it, and cite one metric plus one plot feature as evidence. Then teach it back in two minutes: state the convention, derive the governing relationship, name the failed assumption, and explain why the recovery works.


## Deep derivation and conventions

The depth target for this module is to **derive closed-loop wheel-speed error dynamics with actuator limits**. Start from the physical or geometric constraint, not from the plotted curve. State which quantities are inputs, which are states, and which are observations; then carry the coordinate, sign, frame, sampling, or energy convention through every substitution. The retained convention is: Error is command minus measurement; positive voltage creates positive wheel speed.

The governing relations are:

- $$u_k=K_p e_k+K_i I_k$$ — PI control combines current and accumulated error.
- $$I_(k+1)=I_k+T_s e_k$$ — The discrete integral must include sample time.

Read those equations as a chain of claims. The first relation establishes the mechanism; subsequent relations map it into a prediction that the experiment can expose. A derivation is incomplete if it drops a frame label, silently changes a sign, or combines unlike units. Here the unit ledger is: speed: rad/s; voltage: V; integral error: rad; sample time: s. Before running Python, identify the dimensional unit of every term on both sides of one equation. If the units do not close, a numerical match is accidental.

For a local linearization, discrete update, or geometric approximation, also state its domain. “Correct at the baseline” is weaker than “correct for the declared range under the declared assumptions.” This distinction matters because a robot can produce a smooth and plausible trajectory while violating the modeled constraint. The experiment therefore pairs the response plot with a mechanism or residual plot: one shows what happened, while the other tests why the explanation is credible.

## Alternative formulation and limiting analysis

The required comparison is to **compare proportional bandwidth with the open-loop motor**. Work this comparison before tuning. An alternative formulation should agree on an invariant even if its intermediate coordinates differ; a limiting case should emerge continuously as a parameter approaches its boundary. A branch switch, singular limit, or zero denominator must be handled explicitly rather than hidden by clipping.

Retained limiting checks:

- Zero command and zero state remain zero.
- With Ki=0, proportional control may retain steady error.

Use at least one as a pencil-and-paper oracle. Substitute the limiting input into the displayed equations, predict the sign and scale of the result, and then inspect the relevant metric. If the limiting result disagrees, first test the convention and the limit-taking step; do not immediately retune an unrelated parameter. This procedure separates a model defect from a parameter choice.

## Practical failure analysis and recovery

The engineering failure to diagnose is **encoder sign reversal, saturation, and integral windup**. In the executable counterexample, **Unscaled discrete integrator** is triggered by: Set broken_mode true. Its observable failure is: Error is accumulated without multiplying by the 10 ms sample interval. This is not merely a worse numerical score. It violates an assumption that must be named before the model can support a decision.

The recovery is: Set broken_mode false and restore sample scaling plus anti-windup. Recovery has three parts: remove the fault mechanism, restore the exact baseline inputs, and recheck the original invariant. A curve that looks calmer is not sufficient. The diagnostic signature must return within its retained independent-reference tolerance, and the mechanism plot must again satisfy the relevant sign, conservation, constraint, residual, timing, or consistency condition.

In practice, instrument the variable nearest the violated assumption. For geometry, log frame-resolved residuals; for dynamics and contact, log energy, effort, and saturation; for estimation, log innovations and covariance consistency; for planning and autonomy, log feasibility, guard, collision, or timing decisions. This makes the failure falsifiable and prevents a downstream controller or filter from masking it.

## Evidence workflow and formative check

Run the baseline, then preserve it while changing exactly one control per sweep:

- `kp_v_per_rad_s` at [0.5, 1.5, 3.5]: Proportional gain changes the first correction.
- `ki_v_per_rad` at [0.5, 4, 10]: Integral gain changes residual error and saturation.

Before each run, write a directional prediction from one equation: increase, decrease, unchanged, or branch change. After the run, cite one metric and one plotted feature, including units. Then perform these checks:

1. **Numerical prediction:** calculate one baseline quantity to one or two significant figures without using the experiment output.
2. **Dimensional check:** show that one governing equation has consistent units.
3. **Invariant check:** identify a sign, bound, conservation relation, residual, or ordering that should survive the sweep.
4. **Counterexample:** enable the named broken case and explain which assumption fails before describing the visual symptom.
5. **Recovery:** disable the fault, restore the exact defaults, and verify the signature returns rather than merely improves.

Teach it back without referring to the plot first: state the convention, derive the relationship, predict one sweep, identify the practical failure, and explain why the recovery repairs the violated assumption. Only then use the plots as evidence. A strong answer distinguishes model validity, numerical agreement, and physical validation; none is a substitute for the others.

## Boundary and onward links

Controls/GNC owns general loop-shaping theory; P34-P35 apply multijoint robot control. This lesson establishes its named Robotics competency and provides prerequisites for later mapped modules; it does not absorb the adjacent course's broader theory. The Python result remains deterministic software evidence. It does not claim MATLAB runtime equivalence, learner effectiveness, browser accessibility, physical robot or HIL operation, safety certification, or production readiness.
