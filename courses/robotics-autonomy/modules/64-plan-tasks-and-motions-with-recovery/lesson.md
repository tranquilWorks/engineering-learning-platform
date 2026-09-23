# Plan tasks and motions with recovery

A symbolic plan can be logically valid while one of its motions is impossible. Conversely, a collision-free motion has no task value if its preconditions are false or it leaves the object in the wrong state. Task-and-motion planning connects these layers and must also handle discrepancies discovered during execution. This laboratory searches a bounded symbolic graph with predicted clearance predicates, monitors actual corridor margin, and recovers from a failed carry by excluding that edge and selecting a different grasp orientation.

## Model, derivation, and conventions

The discrete states are start, approach, top grasp, side grasp, and goal. Directed edges carry execution times and preconditions. The top-grasp route is cheaper, so the initial uniform-cost search prefers it when the predicted corridor width exceeds its `0.24 m` envelope. The side grasp rotates the carried object and needs only `0.16 m`, but grasping and transport take longer. Search minimizes accumulated edge cost over admissible transitions.

The width-model-error control separates prediction from execution. Actual width is predicted width minus error. When a carry begins, the monitor computes `m_e=w_actual-w_required(e)`. A negative margin invalidates that motion edge. Nominal execution records the failure, returns to the last certified approach state, adds the failed edge to a blacklist, and searches again. Replanning is bounded because the graph and set of removable carry edges are finite.

## Predict before running

At the baseline, predicted width `0.27 m` makes the cheaper top-grasp carry look feasible. A `5 cm` modelling error reduces actual width to `0.22 m`, so the top envelope has negative margin. Predict one detected failure and one replan. The side grasp should then fit with positive margin and reach the goal.

If only corridor width rises to `0.31 m`, actual width becomes `0.26 m`; the top route should execute without recovery. If only model error rises to `9 cm`, the top route fails more strongly while the side branch remains barely feasible. Broken mode should stop after the first failed top carry because it does not revise the search graph.

## Baseline workflow

Run the baseline and inspect cumulative task time. The trace includes approach, top grasp, failed carry, a bounded recovery action, and the replacement side branch. Because recovery performs extra work, successful execution takes longer than the initially predicted symbolic plan. That additional cost is honest evidence, not planner inefficiency hidden from the metric.

The clearance plot shows one negative attempt followed by one positive attempt. The task-success metric must be one, and motion replans must equal one. Those values together express the teaching invariant: the system is allowed to encounter a model discrepancy, but it may claim success only after the offending edge is excluded and an actually feasible replacement reaches the goal.

## Two one-variable sweeps

For sweep one, increase only predicted corridor width from `0.27 m` to `0.31 m`. Model error, graph costs, grasp envelopes, and recovery logic remain fixed. Actual clearance for the top grasp becomes positive, so the first plan completes with zero replans and lower executed time. This isolates environmental clearance rather than changing planner preferences.

For sweep two, restore corridor width and increase only geometry error from five to nine centimetres. The first carry margin becomes more negative. The side route still has a small positive margin, so recovery remains possible but less robust. The sweep demonstrates that planning with a nominal geometry is different from monitoring the executed geometry; both are required for an auditable autonomous task.

## Intentionally broken case

Broken mode still searches the symbolic graph and still measures the negative motion margin. Its failure is that the observation does not alter control flow. Execution terminates without blacklisting the top carry, returning to a certified state, or selecting the side grasp. Task success remains zero even though the symbolic plan had a goal node.

This captures a common integration defect: motion planners report failure, logs contain the error, but the executive has no recovery transition. Another broken implementation might retry the identical edge forever. The bounded example stops immediately so the failure is deterministic. In a real executive, retry budgets and escalation must be explicit to prevent both silent abandonment and unbounded loops.

## Recovery

Recover by attaching geometric preconditions and execution monitors to symbolic actions. When an action fails, preserve the observed constraint, invalidate the exact edge or parameterization that caused it, and roll back to a state whose physical truth is still known. Replan from that certified state rather than from the original start or an imagined postcondition. Here the object is returned to the approach state and the top-carry edge is blacklisted.

More complex recovery may update a belief state, request a new perception observation, choose a different grasp, move an obstacle, or ask a human. The essential rule is monotonic evidence: a failure must refine the next search problem. Clearing the error without changing assumptions is not recovery.

## Alternative and limiting cases

Hierarchical task networks encode domain methods; PDDL planners search symbolic operators; sampling-based task-and-motion planners alternate discrete decisions with continuous feasibility samples; constraint solvers optimize both together. Behavior trees can express fallback branches but still need state and feasibility semantics. The compact graph here is deliberately small enough to audit every edge and cost.

If actual corridor width exceeds the top envelope, no recovery is needed. If it lies between the side and top envelopes, the demonstrated fallback works. If it is below both envelopes, bounded search should report no plan rather than declare success. With zero model error, predicted and actual predicates agree. With an infinite retry policy and unchanged geometry, a naive executive can livelock; the blacklist prevents that limiting failure.

## Independent evidence and MATLAB-style design boundary

The independent reference constructs its own task graph, uniform-cost search, predicted clearance test, execution monitor, failed-edge set, and recovery trace. It imports no production experiment, consumes no production result, and perturbs no production value. The five retained signatures distinguish no-recovery success, stronger-model-error recovery, the intentionally broken stop, and exact baseline recovery.

No MATLAB task planner, motion library, perception system, browser accessibility review, learner validation, robot controller, physical HIL, safety case, or deployment was exercised. This is deterministic software evidence for a bounded transition system. It does not prove completeness in continuous configuration space or safe execution around people.

## Engineering review checklist

- Define symbolic preconditions and postconditions in physically measurable terms.
- Associate each motion edge with a configuration, clearance, and timeout contract.
- Distinguish predicted feasibility from execution-time observations.
- Roll back only to a state whose physical truth remains certified.
- Ensure a failed action changes the next search problem.
- Bound retries, replans, graph size, and total recovery time.
- Record failed parameterizations without over-blocking unrelated actions.
- Expose an explicit no-plan or escalation result when alternatives are exhausted.

## Common mistakes

Common errors mark a symbolic action complete when motion planning starts rather than when execution finishes, or assume a motion-plan success guarantees the scene stayed unchanged. Other systems retry the same edge with identical parameters, forget that the robot may now occupy a different pose, or roll back symbolic state without physically releasing the object. Overly broad blacklists can remove every useful action; overly narrow ones can repeat the collision. Comparing predicted and measured clearance with inconsistent object orientations is another subtle failure.

## Focused check and teach-back

Trace the baseline from start through failed top carry to successful side carry. State which edge is blacklisted, which state is certified for replanning, and why the side envelope fits. Explain why reaching a goal node in the initial symbolic plan is not task success. Then teach back the difference between a retry and a recovery: recovery incorporates new evidence into state or constraints. Finally, describe the correct result if actual width is smaller than both grasp envelopes and why silently widening a collision tolerance would violate the task contract.
