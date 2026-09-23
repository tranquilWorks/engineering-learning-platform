# Coordinate a mobile manipulator

A mobile manipulator can reach a task by moving its base, its arm, or both. Treating those subsystems independently often produces a fully stretched arm, poor manipulability, unnecessary base travel, or a target that remains outside the composite workspace. This laboratory searches bounded base placements and analytic two-link configurations together, chooses a tradeoff between locomotion and arm conditioning, and executes synchronized trajectories in one world frame.

## Model, derivation, and conventions

The base translates along the world x axis to `x_b`. The arm base is `[x_b,0]`, and the world target is `p_t`. Each candidate therefore presents the arm with the relative target `p_rel=p_t-[x_b,0]`. The same two-link inverse equations used for a fixed manipulator determine whether the relative target lies inside the annular arm workspace and compute an elbow-down joint pair.

Planar manipulability is `w(q)=|det J|=l_1 l_2 |sin(q_2)|` with units square metres. It vanishes when the elbow is straight or folded. For each reachable base candidate, the score is `rho_b |x_b|+0.18/(w+0.025)`. The first term discourages base travel; the reciprocal term discourages singular arm configurations. A deterministic grid bounds the optimization and makes every candidate auditable.

After selection, base position and joint angles interpolate over a common four-second interval. At each sample, forward kinematics uses the simultaneous base and arm state. The final composite endpoint, not an arm-only endpoint, is compared with the world target.

## Predict before running

The baseline target lies beyond the fixed arm's `1.30 m` outer reach. Predict that a base-frozen controller must either reject the target or stretch toward it with residual error and nearly zero manipulability. The coordinated planner should move the base forward enough to place the target comfortably inside the arm workspace, then select a bent-elbow solution.

Increasing target distance alone should increase the necessary base translation while preserving a small endpoint residual. Increasing base-motion weight alone should favor less travel and a more extended arm, reducing manipulability. The exact selected grid point may change discontinuously because the candidate set is discrete; that is expected and should not be confused with numerical nondeterminism.

## Baseline workflow

Run with target x distance `1.8 m` and base-motion weight `0.7`. The response plot shows the end-effector trajectory in the world frame, the final base-elbow-endpoint mechanism, and the target. Confirm that the endpoint error is near floating precision. The base-travel metric states how much locomotion enabled the reach.

Inspect the manipulability value. It is not a probability or normalized score; its units are square metres for this planar position Jacobian. A positive value indicates that the selected elbow retains local Cartesian motion authority. In the synchronization plot, base and arm progress end together. Real systems may choose different velocity profiles, but final-state composition must still use states from a coherent time.

## Two one-variable sweeps

For sweep one, change only target x distance from `1.8 m` to `2.1 m`. Keep the vertical target coordinate, candidate grid, link lengths, and cost weights fixed. The base should travel farther because arm reach is unchanged. Endpoint error should remain near zero because every accepted candidate satisfies analytic reachability.

For sweep two, restore the target and increase only base-motion weight from `0.7` to `2.5`. This makes locomotion expensive relative to manipulability. The chosen base may remain farther back, requiring the arm to extend more and reducing `w(q)`. The comparison demonstrates a design trade: avoiding base motion can degrade dexterity even when position reach remains exact.

## Intentionally broken case

Broken mode freezes the base at zero. Rather than rejecting the unreachable target, it projects the relative target onto the outer arm radius and solves IK there. This mimics a common saturation shortcut. The endpoint is finite and points in the correct direction, but it falls short of the actual target. The elbow is almost straight, so manipulability collapses.

The defect is not that saturation exists; bounded actuators and workspaces require it. The defect is silently substituting the saturated command for task completion. A local arm controller could report perfect tracking of that clipped endpoint while the manipulation task still fails. The composite endpoint metric preserves the original world target and exposes the residual.

## Recovery

Recover by searching base and arm decisions in one coordinate model. Reject arm configurations outside the workspace, score dexterity explicitly, and retain the selected base with its matching joint state. Plan collision-free base motion and arm motion, synchronize them under velocity and acceleration limits, and recompute the composite endpoint from time-aligned states.

If no candidate is feasible, report the task as unreachable or ask a higher-level planner for a different stance, grasp, or object approach. Do not expand the candidate bounds or clip the target without updating the task contract. On hardware, recovery also needs localization confidence, footprint clearance, stability constraints, cable limits, and safe arm posture during driving.

## Alternative and limiting cases

Whole-body inverse kinematics can place base pose and joint variables in one nonlinear optimization with equality, collision, joint-limit, and stability constraints. Task-priority control can allocate instantaneous velocity between base and arm using a combined Jacobian. Reachability maps precompute good base regions for repeated tasks. The grid used here trades smooth optimality for transparent bounded evidence.

If the target lies well inside the arm workspace, sufficiently large base cost correctly selects zero travel. At full extension, position remains mathematically reachable but manipulability is zero. If base travel is unbounded, almost any planar target becomes reachable, yet navigation and time costs dominate. If the vertical target approaches zero, elbow-up and elbow-down branches become symmetric in position but may differ in collision clearance.

## Independent evidence and MATLAB-style design boundary

The independent reference rebuilds the base candidate grid, solves reachability and elbow angle for every candidate, evaluates planar manipulability and the stated cost, and applies composite forward kinematics. It imports no production experiment, consumes no production output, and perturbs no production value. Scenario evidence separately records the target-distance sweep, cost-weight sweep, fixed-base failure, and recovery.

This deterministic model does not run MATLAB, a navigation stack, a whole-body controller, localization, browser accessibility validation, learner testing, physical HIL, or a mobile manipulator. It does not certify stability, collision avoidance, timing, or safety. The software evidence is limited to the stated planar placement and synchronization invariant.

## Engineering review checklist

- Express base pose, arm kinematics, and target in a common world frame.
- Reject unreachable relative targets before applying analytic IK.
- Score manipulability or joint margin rather than distance alone.
- Keep each candidate base pose paired with its own arm solution.
- Verify composite forward kinematics against the original task target.
- Synchronize states before evaluating a moving-base arm endpoint.
- Add footprint, self-collision, environment, stability, and cable constraints for hardware.
- Define an explicit unreachable outcome and escalation path.

## Common mistakes

Frequent mistakes include solving arm IK before choosing the base, adding base and arm coordinates from different frames, or optimizing base distance without checking singularity. A developer may clip an unreachable target and later compare forward kinematics only with the clipped value. Other errors normalize manipulability without declaring units, mix base progress and arm progress from different timestamps, or assume a reachable final pose implies a collision-free trajectory. Whole-body coordination also fails when the arm extends outside the footprint during navigation without being represented in collision geometry.

## Focused check and teach-back

Derive the relative arm target after a candidate base translation. Explain why `l_1 l_2 |sin(q_2)|` collapses at full extension and why that matters even with zero final position error. Then teach back the baseline tradeoff: base travel buys arm conditioning and reach. Identify what broken mode clips, which target the task still requires, and why the resulting controller-level tracking claim cannot establish task completion. Finally, list the additional constraints needed before the same coordination policy could command a physical platform.
