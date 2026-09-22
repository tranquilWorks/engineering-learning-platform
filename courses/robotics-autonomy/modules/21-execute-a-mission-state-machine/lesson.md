# Execute a Mission State Machine

**Guiding question:** What inputs, observable effects, and failure modes matter when you execute a Mission State Machine?

## Concept and prediction

A mission state machine makes operational modes and legal transitions explicit. Local progress events move the mission forward; timeouts and faults must have defined precedence and lead to a safe terminal or recovery state.

At baseline, the fault arrives during EXECUTE. Predict the final state, transition time, and how many active ticks are acceptable after the fault.

## Model, symbols, and equations

- $$s_{k+1}=\delta(s_k,e_k,g_k)$$ — deterministic transition function of state, events, and guards.
- $$g_{timeout}=[t-t_{entry}\ge T_w]$$ — state-local watchdog guard.
- $$g_{fault}\Rightarrow s_{k+1}=SAFE\quad\forall s_k\notin\{SAFE,COMPLETE\}$$ — global fault preemption.

Time units are seconds with a 0.1 s software tick. State codes are 0 INIT, 1 SEARCH, 2 TRACK, 3 EXECUTE, 4 SAFE, and 5 COMPLETE. Lower-level actions are abstracted; this lesson tests transition logic only.

## Manipulation: two one-variable sweeps

1. Sweep `target_detect_s` through [1,2,6]. Detection relative to watchdog and fault timing changes which guard fires first.
2. Restore baseline, then sweep `fault_time_s` through [3.5,5,10]. Early faults terminate safely; a fault after nominal completion does not retroactively change the terminal result.

The first plot shows state occupancy. The second aligns target-detection and fault events with transition timing.

## Evidence and limiting cases

The independent reference executes a separately stated transition table. Production uses explicit ordered guards and records the full state trace.

- If no progress event occurs before watchdog expiration, SEARCH transitions to SAFE.
- A fault simultaneous with local completion follows the specified global-fault precedence.
- A terminal SAFE state remains latched in this model; reset is outside the mission contract.

This is deterministic software logic evidence, not an operational mission, actuator, real-time target, physical HIL, or field result.

## Intentionally broken assumption

**Global fault transition omitted.** Broken mode allows local mission transitions to continue after the fault. The timeline can look orderly while the safety contract is violated.

## Explanation and recovery

Restore a fault-to-SAFE guard from every active state and evaluate it before local success. Then verify zero active ticks after the fault and an explicit terminal-state result.

## Common mistakes

- Defining a fault transition in only some states.
- Letting transition ordering make simultaneous fault/success behavior accidental.
- Reusing a state-entry timestamp after a transition.
- Confusing a state-machine simulation with real-time or physical safety validation.

## Focused check and teach-back

At baseline, cite final state, terminal time, unsafe ticks, and transitions. Remove the fault guard, recover it, and teach back state/event/guard separation, units, precedence, watchdog behavior, and terminal-state policy.


## Deep derivation and conventions

The depth target for this module is to **derive mission transition guards, invariants, and terminal/recovery states**. Start from the physical or geometric constraint, not from the plotted curve. State which quantities are inputs, which are states, and which are observations; then carry the coordinate, sign, frame, sampling, or energy convention through every substitution. The retained convention is: State codes progress INIT=0, SEARCH=1, TRACK=2, EXECUTE=3, with SAFE=4 and COMPLETE=5 terminal. Time advances in positive 0.1 s ticks.

The governing relations are:

- $$x_{k+1}=\delta(x_k,e_k)$$ — The transition function maps the current state and events to one next state.
- $$t-t_{enter}\ge T_{watchdog}$$ — A state timeout sends stalled execution to SAFE.

Read those equations as a chain of claims. The first relation establishes the mechanism; subsequent relations map it into a prediction that the experiment can expose. A derivation is incomplete if it drops a frame label, silently changes a sign, or combines unlike units. Here the unit ledger is: event, dwell, and terminal times: s; unsafe exposure and transition totals: integer counts. Before running Python, identify the dimensional unit of every term on both sides of one equation. If the units do not close, a numerical match is accidental.

For a local linearization, discrete update, or geometric approximation, also state its domain. “Correct at the baseline” is weaker than “correct for the declared range under the declared assumptions.” This distinction matters because a robot can produce a smooth and plausible trajectory while violating the modeled constraint. The experiment therefore pairs the response plot with a mechanism or residual plot: one shows what happened, while the other tests why the explanation is credible.

## Alternative formulation and limiting analysis

The required comparison is to **compare nominal completion with timeout and retry exhaustion**. Work this comparison before tuning. An alternative formulation should agree on an invariant even if its intermediate coordinates differ; a limiting case should emerge continuously as a parameter approaches its boundary. A branch switch, singular limit, or zero denominator must be handled explicitly rather than hidden by clipping.

Retained limiting checks:

- A target event after the watchdog cannot rescue a timed-out SEARCH state.
- Terminal SAFE and COMPLETE states remain latched without an explicit reset.

Use at least one as a pencil-and-paper oracle. Substitute the limiting input into the displayed equations, predict the sign and scale of the result, and then inspect the relevant metric. If the limiting result disagrees, first test the convention and the limit-taking step; do not immediately retune an unrelated parameter. This procedure separates a model defect from a parameter choice.

## Practical failure analysis and recovery

The engineering failure to diagnose is **unreachable states, ambiguous guards, and unsafe reset**. In the executable counterexample, **Global fault transition omitted** is triggered by: Set broken_mode true. Its observable failure is: Local mission progress continues after the injected fault and can report COMPLETE. This is not merely a worse numerical score. It violates an assumption that must be named before the model can support a decision.

The recovery is: Evaluate a global fault guard before every nonterminal local transition. Recovery has three parts: remove the fault mechanism, restore the exact baseline inputs, and recheck the original invariant. A curve that looks calmer is not sufficient. The diagnostic signature must return within its retained independent-reference tolerance, and the mechanism plot must again satisfy the relevant sign, conservation, constraint, residual, timing, or consistency condition.

In practice, instrument the variable nearest the violated assumption. For geometry, log frame-resolved residuals; for dynamics and contact, log energy, effort, and saturation; for estimation, log innovations and covariance consistency; for planning and autonomy, log feasibility, guard, collision, or timing decisions. This makes the failure falsifiable and prevents a downstream controller or filter from masking it.

## Evidence workflow and formative check

Run the baseline, then preserve it while changing exactly one control per sweep:

- `target_detect_s` at [0.5, 2, 8]: A late target can delay progress or let the SEARCH watchdog win.
- `fault_time_s` at [1, 5, 11]: Earlier faults shorten active execution and route immediately to SAFE.

Before each run, write a directional prediction from one equation: increase, decrease, unchanged, or branch change. After the run, cite one metric and one plotted feature, including units. Then perform these checks:

1. **Numerical prediction:** calculate one baseline quantity to one or two significant figures without using the experiment output.
2. **Dimensional check:** show that one governing equation has consistent units.
3. **Invariant check:** identify a sign, bound, conservation relation, residual, or ordering that should survive the sweep.
4. **Counterexample:** enable the named broken case and explain which assumption fails before describing the visual symptom.
5. **Recovery:** disable the fault, restore the exact defaults, and verify the signature returns rather than merely improves.

Teach it back without referring to the plot first: state the convention, derive the relationship, predict one sweep, identify the practical failure, and explain why the recovery repairs the violated assumption. Only then use the plots as evidence. A strong answer distinguishes model validity, numerical agreement, and physical validation; none is a substitute for the others.

## Boundary and onward links

systems engineering owns formal requirements depth; P64-P68 integrate recovery. This lesson establishes its named Robotics competency and provides prerequisites for later mapped modules; it does not absorb the adjacent course's broader theory. The Python result remains deterministic software evidence. It does not claim MATLAB runtime equivalence, learner effectiveness, browser accessibility, physical robot or HIL operation, safety certification, or production readiness.
