# Check collision geometry and smooth paths

A global planner often returns a jagged polyline because its graph contains only a finite set of vertices. Shortcut smoothing removes unnecessary bends by replacing subsequences with straight segments. The operation sounds harmless: choose two waypoints and connect them. Its correctness depends entirely on collision geometry. Free endpoints do not imply a free segment, and a point-robot check does not protect a robot with nonzero radius.

## Model, derivation, and conventions

The robot is a disk of selectable radius moving among circular obstacles. Instead of sweeping the disk explicitly, configuration-space geometry inflates each obstacle by the robot radius and treats the robot centre as a point. For a proposed segment from `a` to `b` and obstacle centre `c`, the closest parameter is

`t*=clip(((c-a)^T(b-a))/||b-a||^2,0,1)`.

The closest finite-segment point is `a+t*(b-a)`. Signed clearance is its distance to `c` minus obstacle radius and robot radius. A negative value means penetration; zero means tangency. Clipping is essential because the closest point on the infinite supporting line may lie beyond an endpoint.

The input polyline is deliberately safe but longer than necessary. Shortcut attempts use a deterministic sequence of waypoint pairs. A candidate replaces all intermediate waypoints only when its complete segment has nonnegative clearance. Accepted shortcuts cannot increase length because Euclidean distance obeys the triangle inequality. After smoothing, every retained segment is audited again.

## Predict before running

Predict that path length will be nonincreasing with accepted attempts. It may remain flat when a proposed chord is unsafe or when no intermediate waypoint exists. Increasing robot radius expands configuration-space obstacles and can reject shortcuts that were valid for a smaller footprint. With zero attempts, the original verified polyline must return unchanged. In broken mode, endpoint-only tests will accept the direct start-to-goal chord, yielding the shortest possible length and negative swept clearance.

## Baseline workflow

Run with a `0.3 m` robot radius and thirty attempts. The response plot places path and inflated obstacle boundaries in the same metric frame. The route should pass above the obstacles, with a visibly positive but possibly small margin at its limiting segment. The path-length metric sums Euclidean segment lengths in metres.

Inspect minimum swept clearance before celebrating a shorter route. It is the minimum over all obstacle/segment pairs after inflation. The colliding-segment count must be zero. The mechanism plot shows current length after each attempt; its staircase shape distinguishes rejected proposals from accepted shortcuts. Any upward step would violate the shortcut rule or indicate inconsistent units.

The straight-line lower bound is ten metres because start and goal share a horizontal coordinate difference of ten metres. It is not a feasible lower bound under obstacles; it is merely geometric. The safe path is expected to remain above it.

## Two one-variable sweeps

First change only robot radius from `0.3 m` to `0.6 m`. The obstacle drawings expand, and some aggressive chords become invalid. Expect the accepted path to be at least as constrained, usually longer. Notice that its minimum signed clearance need not decrease: choosing a different homotopy or segment can produce a larger final margin even though the configuration-space free set shrank.

For the second sweep, restore the `0.3 m` radius and reduce shortcut attempts from thirty to one. This preserves geometry while limiting optimization effort. The result should remain collision-free but retain more original bends and a longer path. That comparison separates feasibility, which must hold at every budget, from smoothing quality, which improves with additional valid attempts.

## Intentionally broken case

Broken mode checks each proposed shortcut endpoint as a zero-radius point and ignores the interior. Since start and goal lie outside every obstacle, it eventually accepts their direct chord. The reported length reaches the geometric lower bound, but the signed-clearance calculation—still performed correctly for the final audit—is negative and the collision count is positive.

This is a useful adversarial case because many visualization reviews miss it. Markers at endpoints look safe, and a thin line can be hard to compare with the actual footprint. Configuration-space inflation and a numerical margin make the violation unambiguous.

## Recovery

Recover by using one footprint-aware collision primitive everywhere. Inflate obstacles by the current robot radius. For every candidate, compute the clipped closest point on the entire finite segment for every obstacle. Accept only if all signed margins are nonnegative. Preserve the original path if no valid shortcut exists.

Then audit the completed path independently of the accept loop. A production planner should also include numerical clearance tolerance, map uncertainty, localization uncertainty, and interpolation used by the downstream controller. Here the exact deterministic geometry isolates the foundational invariant before those margins are added.

## Alternative and limiting cases

Polygonal robots and obstacles can use Minkowski sums, separating-axis tests, or support mappings rather than circle inflation. Three-dimensional systems require swept-volume or continuous-collision methods. Discrete sampling along a segment is simpler but can tunnel through a thin obstacle unless sampling resolution is derived from geometry and motion bounds.

If robot radius tends to zero, the configuration-space obstacles reduce to physical obstacles for a point robot. If every obstacle is removed, direct start-to-goal replacement is valid and triangle inequality makes it optimal for Euclidean length. If the input path is already two points, no smoothing can occur. Tangency at exactly zero clearance is mathematically valid here but would usually receive a positive operational margin.

## Independent evidence and MATLAB-style design boundary

The independent reference reconstructs the original waypoints, deterministic pair schedule, exact clipped projection, and inflation logic without importing the production experiment. Five cases retain path length, minimum clearance, and collision count for baseline, radius, attempt budget, endpoint-only failure, and exact recovery.

No MATLAB runtime comparison was run, though the vector projection is directly expressible in MATLAB. The evidence does not validate polygon meshes, a robot description, browser accessibility, learner effectiveness, physical dimensions, localization uncertainty, controller tracking, HIL, certification, or release.

## Engineering review checklist

- Express path, obstacles, and footprint in one named frame and unit.
- Inflate geometry by the complete footprint or a justified conservative bound.
- Clip line projection to the finite segment.
- Require nonnegative margin for every obstacle and segment.
- Verify accepted replacements never increase path length.
- Re-audit the final path independently.
- Record the geometry and map revisions used to approve it.

## Common mistakes

Typical mistakes include testing endpoints only, sampling too coarsely, forgetting robot radius, subtracting radius twice, using distance to the infinite line, and mixing squared distance with an unsquared radius. Another subtle error evaluates a shortcut against obstacles but not workspace boundaries. Smoothing can also destroy dynamic feasibility even when geometry remains valid; P59 adds the missing state and acceleration constraints.

## Focused check and teach-back

Derive the projection parameter and explain why its clipping distinguishes a segment from a line. Then explain configuration-space inflation in physical language: which body moves, which geometry grows, and why the result is equivalent for a disk robot. Finish by teaching back why a ten-metre broken path can be numerically shorter, graphically appealing, and still categorically worse than the longer recovered path.
