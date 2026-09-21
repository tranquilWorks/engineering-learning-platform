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
