# A-AUTONOMY integration evidence

Integrate these existing lessons: P20, P21, P64, P65.

Required evidence: Behavior, state, task-and-motion, multi-agent contract, failure propagation, and recovery evidence.

## Derive and predict

Use P20: Reconstruct a behavior-tree tick from child status and traversal order. Sequence and fallback nodes propagate running, success and failure differently; trace which children actually execute. Connect this result to at least one other listed lesson, identifying the exact quantity, units and assumption transferred across their interface.

## Compare connected mechanisms

Use P21: Show which guard permits a mission-state transition. State, event and guard jointly determine the next action; a recovery transition must preserve or explicitly reset its evidence. Connect this result to at least one other listed lesson, identifying the exact quantity, units and assumption transferred across their interface.

## Diagnose and recover

Use P64: Demonstrate recovery after a motion edge becomes infeasible. The symbolic plan must use geometric feasibility and retain the actual execution state when selecting an alternative. Connect this result to at least one other listed lesson, identifying the exact quantity, units and assumption transferred across their interface.

## Integrate and defend the boundary

Use P65: Check vertex and edge-swap conflicts in a reservation schedule. Robots can collide by sharing a cell or swapping cells during one step; waits and delayed starts remain part of the schedule. Connect this result to at least one other listed lesson, identifying the exact quantity, units and assumption transferred across their interface.

## Required integration artifact

Construct a state/event trace with preconditions, success guards, failure exits and recovery actions. In P64 force the first carry route to fail, show the blacklisted edge and compare the replacement route; then exhaust both alternatives and retain explicit failure with finite elapsed time. Contrast this with P62, where transfer cannot begin before grasp verification. For the multi-agent contract, identify whose state or intent is stale and how a locally valid plan can violate a shared constraint. No restart should erase the causal event that triggered recovery. Provide one counterexample to treating an action label as proof that its physical precondition occurred.

## Four-criterion rubric

1. Governing reasoning: equations, units and frame/sign conventions justify a numerical prediction; naming an algorithm alone earns no evidence.
2. Controlled comparison: two isolated sweeps and at least one limiting case distinguish mechanisms and make a falsifiable claim.
3. Diagnose and recover: identify the first failing assumption from actual outputs, restore it and demonstrate deterministic recovery.
4. Integration and scope: show the value passed between stages, an independently checked result, and a limitation that prevents a broader claim.

Retain inputs, selected outputs and your explanation as a cumulative artifact. No learner completion, automatic score, physical qualification or production acceptance is recorded.
