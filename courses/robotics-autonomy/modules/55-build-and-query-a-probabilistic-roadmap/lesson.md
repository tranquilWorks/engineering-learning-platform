# Build and query a probabilistic roadmap

Sampling-based planners trade a complete geometric decomposition for a graph assembled from collision-free configurations. A probabilistic roadmap (PRM) is especially useful when one environment will receive many start–goal queries: build an expensive reusable connectivity graph offline, then answer each query with ordinary graph search. That separation is powerful only if the local planner is trustworthy. A graph can be dense, connected, and numerically well behaved while its edges pass directly through obstacles.

## Model, derivation, and conventions

The laboratory uses a two-dimensional rectangular workspace in metres, a circular robot footprint, and two circular obstacles. Collision checking occurs in configuration space by inflating every obstacle radius by the robot radius. A point `q` is free when its distance from every obstacle centre exceeds the inflated radius. A segment is free when the minimum distance from the obstacle centre to the complete segment exceeds that same radius.

Samples come from a deterministic two-dimensional Halton sequence with bases two and three. Low-discrepancy sampling covers the box more evenly than a short pseudorandom stream and makes exact replay possible. Start and goal are inserted explicitly. Samples inside inflated obstacles are rejected. For each pair closer than the selected connection radius, the local planner checks the swept segment before inserting an undirected weighted edge. Edge weight is Euclidean length in metres.

The online query uses Dijkstra search. Its objective is `J(path)=sum ||q_i-q_j||` over selected edges. Because every weight is nonnegative, settling the goal proves the shortest graph path. It does not prove the continuous optimum; PRM approximates free-space connectivity through its finite samples and connection policy.

## Predict before running

Before execution, predict the competing effects of sample count and connection radius. More free samples can represent narrow passages but increase pair checks. A larger connection radius can reduce graph-path detours, yet it also creates more candidate segments that must be collision tested. Neither parameter permits skipping the local planner. In broken mode, expect the shortest graph route to be shorter and to contain at least one colliding edge. That is not a useful improvement: it solves the wrong graph.

## Baseline workflow

Run one hundred samples with a `2.0 m` radius. The response plot shows all retained configurations, the shortest query path, and the boundaries of inflated obstacles. Because roadmap samples are plotted in their deterministic sequence rather than as graph edges, focus on the highlighted shortest path. Its segments should remain outside both boundaries.

Read the three metrics together. Path length measures graph cost. Colliding path edges is the post-query continuous-geometry audit and must be zero. Settled vertex fraction shows how much of the roadmap Dijkstra had to explore before proving the goal cost. A value near one is possible when many alternatives have similar cost; it does not imply failure.

The mechanism plot compares candidate pairs within the connection radius with edges retained after filtering. Their difference is geometric work made explicit. A roadmap that reports only vertex count hides the most important correctness operation.

## Two one-variable sweeps

First reduce only sample count from one hundred to fifty. The fixed start, goal, obstacles, robot radius, and connection radius remain unchanged. Expect a sparser graph and usually a longer route. The exact settled fraction may rise or fall because its denominator also changes. The key requirement is still a finite, collision-free query result.

Next restore one hundred samples and increase only connection radius from `2.0 m` to `3.0 m`. More candidate edges appear, and collision checking should reject any chord through an inflated obstacle. A shorter graph path is plausible because longer valid shortcuts become available. If collision count rises, the radius has incorrectly changed collision semantics rather than only neighborhood selection.

## Intentionally broken case

Broken mode accepts every within-radius pair without evaluating segment geometry. Samples themselves remain free, so a superficial review of the vertex cloud looks correct. Dijkstra then rationally selects low-cost chords through obstacles. This failure is common when a team validates sampled states but treats interpolation as harmless.

Endpoint safety does not imply edge safety. Two points on opposite sides of a circle can each have large clearance while the segment between them crosses its centre. The broken output deliberately preserves this distinction: graph connectivity remains excellent, path length improves, and the continuous collision count exposes the invalid result.

## Recovery

Recover by making one collision model authoritative for both sampling and local connections. Inflate obstacles once using the robot footprint. For each candidate edge, project each obstacle centre onto the finite segment using a clipped scalar parameter, then compare the resulting distance with the inflated radius. Insert the edge only if every obstacle passes.

After Dijkstra returns a vertex sequence, repeat the segment audit as a defense-in-depth check. In a deployed system, the builder should also retain map and footprint revisions with the roadmap. A valid graph for one payload or inflation margin may be unsafe after the robot geometry changes.

## Alternative and limiting cases

A k-nearest PRM connects a fixed number of neighbors instead of using a metric radius. PRM* varies connection scale with sample count to obtain asymptotic optimality under assumptions that this compact lesson does not claim. Lazy PRM postpones many edge checks until a candidate query path needs them; it can save work when most of the graph is never queried, but it must remove invalid edges and repeat the search.

As radius tends to zero, isolated vertices dominate and the query fails despite abundant free samples. As radius grows across the entire workspace, pair count becomes quadratic and collision checking dominates. In an obstacle-free box every candidate segment is valid, so the local filter retains all within-radius edges. Narrow passages remain a probabilistic weakness: deterministic low-discrepancy coverage improves repeatability, not completeness at a fixed budget.

## Independent evidence and MATLAB-style design boundary

The independent calculation regenerates Halton points, performs its own point and segment tests, builds its own adjacency lists, and solves the weighted query without importing the production entrypoint. Retained evidence compares all three signature fields for baseline, both sweeps, the intentionally unchecked graph, and exact recovery.

The model is software-only and dependency-light. Its vector operations could be expressed in MATLAB, but no MATLAB runtime parity was run. No browser or accessibility inspection, learner study, ROS cost-map integration, physical footprint measurement, hardware timing, certification, or deployment claim is made.

## Engineering review checklist

- Record workspace, map, and robot-footprint revisions with the roadmap.
- Reject samples using the same inflated geometry used for edges.
- Check the entire finite segment, not its infinite supporting line or endpoints.
- Store edge weights in metres and keep them nonnegative.
- Distinguish graph reachability from continuous executability.
- Bound sample and pair counts before runtime use.
- Revalidate the returned path even when construction was checked.

## Common mistakes

Frequent errors include forgetting robot-radius inflation, connecting through obstacles, confusing a connection radius with obstacle clearance, using a line projection without clipping to the segment, and treating an empty query as zero path length. Another mistake changes the sample generator between construction and evidence replay, which makes performance comparisons meaningless. Finally, a larger connected component is not automatically better: invalid edges make the component look stronger precisely when it is less trustworthy.

## Focused check and teach-back

Derive the scalar projection used to find the closest point from a circle centre to a segment. Explain why clipping that scalar to `[0,1]` is necessary. Then teach back the offline/online PRM split and identify which operations belong to each phase. Conclude by explaining how the broken roadmap can have free vertices, a finite shortest path, and still command a collision.
