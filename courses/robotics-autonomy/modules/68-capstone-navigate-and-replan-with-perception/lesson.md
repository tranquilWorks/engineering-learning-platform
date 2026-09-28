# Navigate from perception through a timed fault

The obstacle is not preloaded into the robot's map. Range observations must reveal it before the planner can avoid it. A dropout and an old packet test whether the robot can protect and then resume its mission using actual event history.

## Model, derivation, and conventions

The bounded grid spans $x=0\ldots8$, $y=0\ldots2$ m, with start $(0,0)$ and goal $(8,0)$. A static occupied cell is at $(4,0)$ and becomes observable within 2.5 m. A moving obstacle follows $\mathbf o(t)=(6,-2+v_ot)$ m.

Range packets arrive at 5 Hz. The selected percentage removes a contiguous group from a fixed 125-packet schedule starting at tick 7. A copy of source tick 3 arrives at tick 35. Healthy reception accepts only increasing source timestamps. Observed occupancy feeds A*; among equally short routes, the lexicographically first full path is selected.

A 1 Hz decision loop can move one grid edge during the next second. It holds if range age exceeds 0.6 s. This is a sampled decision guard, not an asynchronous emergency stop during an already selected segment. Moving-obstacle protection evaluates the entire candidate segment. For initial relative position $\mathbf r$ and relative displacement $\mathbf d$ over one second,

\[\tau_* = \operatorname{clip}\!\left(-\frac{\mathbf r\cdot\mathbf d}{\|\mathbf d\|^2},0,1\right),\qquad d_{min}=\|\mathbf r+\tau_*\mathbf d\|.\]

Distances are metres; $v_o$ is m/s. The controller waits if predicted separation is below 0.85 m. The recorded result measures the actually executed segment, including waits.

## Baseline workflow

Predict whether a direct shortest path remains acceptable after the static obstacle is seen. At 10% dropout, 12 source ticks are removed by nearest-integer rounding of 12.5 in this implementation. The last pre-gap observation ages, motion decisions pause, then fresh observations reveal the obstacle and a detour is planned.

As a worked separation example, move from $(5,0)$ to $(6,0)$ during $t=5\ldots6$ s while $v_o=0.3$ m/s. Then $\mathbf r=(-1,0.5)$ m and $\mathbf d=(1,-0.3)$ m; the minimum lies at the interval endpoint and is 0.2 m, so that candidate must be rejected. Checking only the initial distance would miss it.

Run the baseline and inspect the executed route, minimum-separation curve and requirement table. Minimum separation is about 0.958 m. Success requires zero static contacts, arrival at the goal, separation ≥0.85 m, no stale motion decision or missing fresh resume, and no accepted source-order inversion.

## Two one-variable sweeps

1. Keep obstacle speed 0.3 m/s; increase dropout from 10% to 40%. Predict a longer hold and later crossing. Compare the route timing and separation; later arrival can increase clearance rather than making every metric worse.
2. Restore 10% dropout; increase obstacle speed to 0.55 m/s. Predict when the obstacle clears the crossing. Inspect actual minimum separation along segments, not just distance at the crossing node.

## Intentionally broken case

The broken receiver admits the old packet, suppresses occupancy updates, ignores range expiry and predicts a frozen obstacle. The executed route therefore exposes static contacts, insufficient separation and source-order errors. None of the replay or recovery verdicts is assigned directly from the mode toggle.

## Recovery

Restore healthy processing without changing dropout or obstacle speed. The same event schedule must again produce a fresh-data resume, a replanned route and the original safe signature.

## Alternative and limiting cases

With no dropped range packets, no dropout-resume event is required. Source-order protection still rejects the independently injected old packet. Every executed healthy edge avoids known occupancy. Safety is only checked against the declared static cell and moving-point model; unknown obstacles, sensing errors and physical stopping distance remain outside this exercise.

## Independent evidence and MATLAB-style design boundary

The reference uses reverse breadth-first distance labels and greedy lexicographic route extraction instead of A*. It independently replays sensor times and computes relative-line closest approach in the complex plane. The five reference scenarios and physical segment checks test more than a preselected route.

## Common mistakes

Do not initialize the map from world truth, equate a percentage with a recovery event, or compare unsynchronized obstacle and robot positions. A wait is part of the executed trajectory and must be checked too.

## Focused check and teach-back

- Why does the reference need the same tie rule? Equally short spatial paths can cross the moving obstacle at different times.
- What proves recovery? A recorded motion decision after the gap using a fresh accepted source observation.
- Why is a single crossing-distance check insufficient? The closest approach may occur inside an edge.

## Cumulative assessment

Trace one obstacle observation into occupancy and a changed route; reconstruct a stale-data hold and fresh resume from timestamps; and independently calculate one segment's closest approach. Explain the failed broken-run requirements using those quantities.

## Predict before running

Before moving either control, write down three separate expectations: where the static cell first becomes observable, the first decision that sees an expired range timestamp, and whether the robot or moving obstacle reaches the crossing first. Keep these predictions separate. Occupancy depends on sensor range and source position; hold duration depends on packet timing; dynamic clearance depends on synchronized trajectories. The final success count cannot tell you which of these mechanisms you understood correctly.

## Engineering review checklist

Audit the sensor schedule before interpreting the path. Packet tick $k$ represents time $0.2k$ seconds. At 10% dropout, ticks 7–18 are absent, and tick 19 is the first fresh sample afterward. The source tick 3 copy arriving at tick 35 is old even though its transport arrival is recent. A receiver that uses arrival order as source order can rewind its evidence.

Audit one-second decisions separately from the faster observations. At a decision, the planner starts from the current grid cell, searches the current occupied set and chooses the next edge. Intermediate observations are generated along the continuous selected segment. The guard acts at the next decision; it does not claim braking or replanning at every intermediate sensor tick. This distinction limits what a “no stale motion decisions” result establishes.

Finally, derive why the independent search should agree. Unit-cost graph edges make breadth-first distance-to-goal labels exact. Choosing the lexicographically smallest neighbor whose label decreases by one produces the lexicographically smallest shortest route. Production A* instead orders candidates by estimated total cost and their entire path. Agreement therefore checks two search formulations under an explicitly shared tie convention, rather than forcing one arbitrary route into both outputs.

The binary occupancy update assumes exact detection of the one known world cell. There is no inverse sensor probability, log-odds accumulation, uncertainty map or SLAM correction in this capstone. A real system would need those mechanisms and stopping-distance analysis before extending its safety claim. The browser evidence establishes only this declared deterministic graph and moving-point model.
