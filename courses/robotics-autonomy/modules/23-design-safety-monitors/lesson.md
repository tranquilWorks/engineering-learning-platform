# Design Safety Monitors

**Guiding question:** What inputs, observable effects, and failure modes matter when you design Safety Monitors?

## Concept and prediction

A safety monitor independently checks whether commanded behavior remains inside a conservative envelope. For obstacle approach, the decision must include current speed, reaction delay, available deceleration, and margin—not only current distance.

Predict the baseline stopping distance and compare it with a fixed 0.1 m trigger. Which policy can stop before a 3 m obstacle?

## Model, symbols, and equations

- $$d_b=v^2/(2a)$$ — ideal constant-deceleration braking distance.
- $$d_{stop}=v t_r+d_b+d_m$$ — required separation including reaction travel and margin.
- $$d_{meas}\le d_{stop}\Rightarrow u_{safe}=BRAKE$$ — monitor intervention rule.

Speed uses m/s, distance uses metres, reaction time uses seconds, and deceleration magnitude uses m/s^2. +x points toward the obstacle. Positive separation means the robot has not reached it.

## Manipulation: two one-variable sweeps

1. Sweep `command_speed_m_s` through [0.5,2,3]. Braking distance grows with speed squared.
2. Restore baseline, then sweep `reaction_time_s` through [0,0.2,0.8]. The reaction component grows linearly with speed and delay.

The approach plot shows speed and separation. The mechanism plot directly compares available separation with the required stopping envelope.

## Evidence and limiting cases

The independent reference executes the stated discrete braking recurrence and checks the continuous kinematic stopping limit. Production maintains its own monitor and state trace.

- At zero speed, braking distance is zero but static margin remains.
- Infinite deceleration removes ideal braking distance but not sensing/decision delay.
- A monitor built on optimistic deceleration is not conservative.

This is software safety-logic simulation, not a certified safety function, physical brake test, robot, HIL, field, or production result.

## Intentionally broken assumption

**Distance-only trigger.** Broken mode waits until separation reaches 0.1 m. It ignores the robot's kinetic state and therefore intervenes after collision is unavoidable.

## Explanation and recovery

Restore the speed-dependent envelope, latch braking, and use conservative bounds supported by physical validation before deployment. The software plot demonstrates logic, not safety integrity.

## Common mistakes

- Comparing distance with stopping time or other mismatched units.
- Using nominal rather than worst-case deceleration and reaction delay.
- Allowing lower-priority commands to overwrite a safety stop.
- Calling simulated separation a certified stopping-distance result.

## Focused check and teach-back

At baseline, calculate braking and reaction distance, cite minimum separation and stop time, reproduce the late-trigger collision, and recover it. Teach back units, envelope terms, monitor priority, and the physical evidence still required.


## Deep derivation and conventions

The depth target for this module is to **derive monitor thresholds, hysteresis, latching, and safe-state logic**. Start from the physical or geometric constraint, not from the plotted curve. State which quantities are inputs, which are states, and which are observations; then carry the coordinate, sign, frame, sampling, or energy convention through every substitution. The retained convention is: Robot position and positive velocity point toward the obstacle. Separation is obstacle position minus robot position, so nonpositive separation indicates crossing.

The governing relations are:

- $$d_{req}=v t_r+v^2/(2a)+m$$ — The intervention envelope includes reaction travel, braking distance, and margin.
- $$v_{k+1}=\max(0,v_k-a\Delta t)$$ — A latched stop reduces speed monotonically at the validated deceleration bound.

Read those equations as a chain of claims. The first relation establishes the mechanism; subsequent relations map it into a prediction that the experiment can expose. A derivation is incomplete if it drops a frame label, silently changes a sign, or combines unlike units. Here the unit ledger is: position, separation, margin, and stopping envelope: m; speed: m/s; deceleration: m/s^2; reaction and stop time: s. Before running Python, identify the dimensional unit of every term on both sides of one equation. If the units do not close, a numerical match is accidental.

For a local linearization, discrete update, or geometric approximation, also state its domain. “Correct at the baseline” is weaker than “correct for the declared range under the declared assumptions.” This distinction matters because a robot can produce a smooth and plausible trajectory while violating the modeled constraint. The experiment therefore pairs the response plot with a mechanism or residual plot: one shows what happened, while the other tests why the explanation is credible.

## Alternative formulation and limiting analysis

The required comparison is to **compare nuisance alarm, missed detection, and sensor disagreement**. Work this comparison before tuning. An alternative formulation should agree on an invariant even if its intermediate coordinates differ; a limiting case should emerge continuously as a parameter approaches its boundary. A branch switch, singular limit, or zero denominator must be handled explicitly rather than hidden by clipping.

Retained limiting checks:

- At zero speed the dynamic braking and reaction terms vanish, leaving only margin.
- Smaller available deceleration increases required braking distance.

Use at least one as a pencil-and-paper oracle. Substitute the limiting input into the displayed equations, predict the sign and scale of the result, and then inspect the relevant metric. If the limiting result disagrees, first test the convention and the limit-taking step; do not immediately retune an unrelated parameter. This procedure separates a model defect from a parameter choice.

## Practical failure analysis and recovery

The engineering failure to diagnose is **single-point monitor failure and unsafe automatic reset**. In the executable counterexample, **Fixed-distance stop trigger** is triggered by: Set broken_mode true. Its observable failure is: The monitor waits for 0.1 m regardless of speed and crosses the obstacle before stopping. This is not merely a worse numerical score. It violates an assumption that must be named before the model can support a decision.

The recovery is: Use the speed-dependent envelope with conservative reaction and deceleration bounds. Recovery has three parts: remove the fault mechanism, restore the exact baseline inputs, and recheck the original invariant. A curve that looks calmer is not sufficient. The diagnostic signature must return within its retained independent-reference tolerance, and the mechanism plot must again satisfy the relevant sign, conservation, constraint, residual, timing, or consistency condition.

In practice, instrument the variable nearest the violated assumption. For geometry, log frame-resolved residuals; for dynamics and contact, log energy, effort, and saturation; for estimation, log innovations and covariance consistency; for planning and autonomy, log feasibility, guard, collision, or timing decisions. This makes the failure falsifiable and prevents a downstream controller or filter from masking it.

## Evidence workflow and formative check

Run the baseline, then preserve it while changing exactly one control per sweep:

- `command_speed_m_s` at [0.5, 2, 3]: Braking distance grows quadratically with speed and moves intervention earlier.
- `reaction_time_s` at [0, 0.2, 0.8]: Longer reaction bounds add linear travel to the required envelope.

Before each run, write a directional prediction from one equation: increase, decrease, unchanged, or branch change. After the run, cite one metric and one plotted feature, including units. Then perform these checks:

1. **Numerical prediction:** calculate one baseline quantity to one or two significant figures without using the experiment output.
2. **Dimensional check:** show that one governing equation has consistent units.
3. **Invariant check:** identify a sign, bound, conservation relation, residual, or ordering that should survive the sweep.
4. **Counterexample:** enable the named broken case and explain which assumption fails before describing the visual symptom.
5. **Recovery:** disable the fault, restore the exact defaults, and verify the signature returns rather than merely improves.

Teach it back without referring to the plot first: state the convention, derive the relationship, predict one sweep, identify the practical failure, and explain why the recovery repairs the violated assumption. Only then use the plots as evidence. A strong answer distinguishes model validity, numerical agreement, and physical validation; none is a substitute for the others.

## Boundary and onward links

reliability/FDIR owns certification and coverage depth. This lesson establishes its named Robotics competency and provides prerequisites for later mapped modules; it does not absorb the adjacent course's broader theory. The Python result remains deterministic software evidence. It does not claim MATLAB runtime equivalence, learner effectiveness, browser accessibility, physical robot or HIL operation, safety certification, or production readiness.
