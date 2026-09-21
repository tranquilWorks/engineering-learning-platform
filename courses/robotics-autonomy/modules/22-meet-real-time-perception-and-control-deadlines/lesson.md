# Meet Real-Time Perception and Control Deadlines

**Guiding question:** What inputs, observable effects, and failure modes matter when you meet Real-Time Perception and Control Deadlines?

## Concept and prediction

Real-time correctness requires the right result before its deadline. CPU utilization alone does not establish schedulability: priority assignment, preemption, release phasing, WCET, and per-task deadlines determine response time.

The default tasks are control $(T=20,C=5)$ ms, perception $(50,18)$ ms, and planning $(100,25)$ ms. Predict total utilization and control response when planning is incorrectly given highest priority.

## Model, symbols, and equations

- $$U=\sum_i C_i/T_i$$ — processor utilization.
- $$R_i=C_i+\sum_{j\in hp(i)}\left\lceil R_i/T_j\right\rceil C_j$$ — fixed-point worst-case response time.
- $$R_i\le D_i$$ — deadline acceptance criterion.

Periods, WCETs, response times, deadlines, and the schedule axis use milliseconds. Task code 0 is control, 1 perception, and 2 planning. Deadlines equal periods, releases are synchronous, and scheduling is preemptive fixed-priority.

## Manipulation: two one-variable sweeps

1. Sweep `control_wcet_ms` through [1,5,10]. Control utilization and interference on lower-priority tasks grow directly.
2. Restore baseline, then sweep `perception_wcet_ms` through [5,18,30]. Planning response grows and may cross its deadline.

The schedule plot shows every dispatched millisecond. The bar plot compares worst observed response with each deadline.

## Evidence and limiting cases

Production uses a one-millisecond scheduler trace. The independent oracle uses a release-to-release event scheduler and separately applies fixed-point response-time equations with the selected priority order.

- Utilization above one guarantees overload on one processor, but utilization below one does not guarantee every arbitrary priority assignment.
- A highest-priority task has response time equal to its WCET in this interference model.
- Average execution time cannot substitute for a justified WCET bound.

This is deterministic software scheduling evidence, not measured target jitter, OS latency, hardware execution time, HIL timing, or production capacity.

## Intentionally broken assumption

**Priorities reversed.** Broken mode gives the longest-period planning task highest priority and the 20 ms control task lowest. Its critical-instant response bound is 48 ms; accumulated control backlog produces a 51 ms observed response within the default 100 ms trace. Both miss the 20 ms deadline despite $U=0.86$.

## Explanation and recovery

Restore rate-monotonic ordering, recompute fixed-point response times, and compare each result with its deadline. A real system must separately account for blocking, jitter, interrupts, multicore effects, and measured WCET evidence.

## Common mistakes

- Declaring a task set safe because utilization is below 100%.
- Using average timing instead of WCET.
- Reporting throughput while ignoring individual latency/deadline requirements.
- Treating a millisecond simulator as physical target timing evidence.

## Focused check and teach-back

At baseline, calculate utilization, cite each response time, reverse priorities, and recover them. Teach back period/WCET/deadline units, priority interference, the fixed-point equation, and the evidence missing from a physical system claim.
