# Cumulative portfolio A-SAFETY

Integrate these existing lessons: P22, P23, P24, P39, P60, P65, P67.

Required evidence: Timing, data age, monitor coverage, bounded fallback, fault injection, pass/fail, and non-certification boundaries.

## Derive and predict

Use P22: Compute a deadline miss from release, execution and response time. Interference and blocking affect completion time; utilization alone does not prove every job meets its deadline. Connect this result to at least one other listed lesson, identifying the exact quantity, units and assumption transferred across their interface.

## Compare connected mechanisms

Use P24: Follow a delayed command through a watchdog and virtual plant. Source age determines command validity; fail-zero behavior and plant response must be visible after packet loss. Connect this result to at least one other listed lesson, identifying the exact quantity, units and assumption transferred across their interface.

## Diagnose and recover

Use P60: Explain why a short prediction horizon changes avoidance decisions. The selected acceleration is applied to the plant and the horizon is recomputed; a frozen-obstacle prediction uses the wrong future state. Connect this result to at least one other listed lesson, identifying the exact quantity, units and assumption transferred across their interface.

## Integrate and defend the boundary

Use P67: Measure recovery latency from the actual accepted event sequence. Source time and arrival time serve different roles; stale rejection, gap detection and fresh-state recovery must be observable. Connect this result to at least one other listed lesson, identifying the exact quantity, units and assumption transferred across their interface.

## Four-criterion rubric

1. Governing reasoning: equations, units and frame/sign conventions justify a numerical prediction; naming an algorithm alone earns no evidence.
2. Controlled comparison: two isolated sweeps and at least one limiting case distinguish mechanisms and make a falsifiable claim.
3. Diagnose and recover: identify the first failing assumption from actual outputs, restore it and demonstrate deterministic recovery.
4. Integration and scope: show the value passed between stages, an independently checked result, and a limitation that prevents a broader claim.

Retain inputs, selected outputs and your explanation as a cumulative artifact. No learner completion, automatic score, physical qualification or production acceptance is recorded.
