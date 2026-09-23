# Execute perception-guided pick and place

A pick-and-place sequence crosses several model boundaries: pixels become an object pose, that pose moves through a camera extrinsic into the robot base, inverse kinematics selects a joint branch, and a task state machine decides whether contact is trustworthy enough to lift. Each step can produce a plausible number while the total pipeline is wrong. This laboratory makes the interfaces explicit with a deterministic planar camera, a two-link arm, and a nine-state manipulation sequence gated by physical pickup error.

## Model, derivation, and conventions

The camera reports an object point `p_c^o`. The calibrated base-to-camera transform is a translation `t_b^c` and planar rotation `R(theta_b^c)`. The base-frame estimate is `p_b^o=t_b^c+R(theta_b^c+delta theta)p_c^o`, where the yaw-error control represents extrinsic miscalibration. A deterministic position perturbation, scaled in centimetres, represents repeatable visual estimation error without claiming a sensor noise distribution.

For link lengths `l_1` and `l_2`, analytic inverse kinematics computes `cos(q_2)=(x^2+y^2-l_1^2-l_2^2)/(2l_1l_2)`. The selected elbow-down branch defines `q_2`, and `q_1` subtracts the second-link triangle angle from `atan2(y,x)`. Forward kinematics reconstructs the commanded endpoint. Reachability requires the cosine to lie within `[-1,1]`. The outer reach margin is `l_1+l_2-||p_b^o||`.

Nine conceptual states cover observe, transform, approach, descend, grasp, verify, lift, transfer, and release. The compact runtime reports all nine only when the estimate is reachable and the endpoint lies within the `0.055 m` physical pickup tolerance of the true object. Otherwise it stops after the attempted grasp evidence.

## Predict before running

Predict the baseline before execution. Small image-position and extrinsic errors should move the estimated object slightly but keep the endpoint inside the gripper tolerance. The arm should complete all states. Increasing visual position noise alone changes the translational component of the error. Increasing yaw error alone rotates the measured camera vector about the camera origin, so error grows with object distance.

Now predict the broken case. Camera coordinates are numerically similar in scale to base coordinates and remain within the arm workspace. An IK solver will therefore return finite joint angles. Nevertheless, omitting the translation and rotation makes the endpoint miss the physical object by far more than the grasp tolerance. Reachability is necessary but not sufficient for a valid pickup.

## Baseline workflow

Run with `1.2 cm` visual noise and `0.8 deg` camera yaw error. In the response plot, distinguish the true object, transformed estimate, and endpoint approach. The endpoint terminates at the estimate because the analytic kinematics is internally consistent. The pickup-position-error metric instead compares that endpoint with the true object, which is the task-relevant residual.

Inspect the mechanism plot. It displays distance from each interpolated approach endpoint to the true object and the gripper tolerance. Early approach samples can be far from the object without being failures; only the contact transition uses the threshold. Confirm that the final error is below tolerance, reach margin is positive, and the completed-state count is nine.

## Two one-variable sweeps

For sweep one, change only visual position noise from `1.2 cm` to `5.0 cm`. The camera extrinsic, object, arm, branch, and tolerance remain fixed. The endpoint follows the noisier transformed estimate, so pickup error increases. This isolates pose-translation sensitivity without conflating it with calibration.

For sweep two, restore visual noise and increase only camera yaw error to five degrees. Rotation error produces a lateral displacement proportional to the camera-frame range. Depending on the fixed tolerance, the state machine may refuse to lift even though IK reachability remains positive. That refusal is correct behavior: a planning component must not substitute geometric reachability for grasp verification.

## Intentionally broken case

Broken mode sends `p_c^o` directly to the arm as though it were `p_b^o`. This is a classic frame-identity assumption. No exception occurs because both are two-element metre vectors. The arm reaches the wrong coordinate precisely, so its own forward/inverse residual is nearly zero. A unit test confined to the kinematics function would pass.

The task-level comparison against the true object exposes the defect. The completed state count stops at four, representing an attempted descent and contact check without authorized lift. In a real system, blindly continuing could close on empty space, strike a fixture, or move an unsecured object. Broken mode therefore illustrates why state transitions require evidence from adjacent subsystems.

## Recovery

Recover by declaring the frame of every pose and applying the calibrated transform before IK. Check reachability without silently clipping an impossible cosine. Choose a branch compatible with joint limits and approach direction. At contact, compare a task-relevant residual or sensor confirmation with a documented tolerance. Only then allow lift and transfer.

Operational recovery also needs stale-transform detection, timestamp alignment, covariance propagation, collision checking along approach and retreat, gripper state feedback, and a safe place to put an uncertain object. Re-observation can reduce pose uncertainty, but it should not erase evidence of a calibration fault.

## Alternative and limiting cases

Three-dimensional systems use homogeneous transforms or `SE(3)` pose objects, six-degree-of-freedom IK, collision-aware motion planning, and grasp approach frames. Sampling-based IK or nonlinear optimization can include joint limits and obstacles directly. Visual servoing can close the loop in image or Cartesian space instead of committing to a single open-loop pose.

With zero visual and calibration error, the analytic endpoint coincides with the true point up to floating precision. At the outer workspace boundary, reach margin and manipulability collapse even if position error is zero. If the camera is colocated and aligned with the base, the broken identity assumption happens to be correct; that limiting case is why tests must include a nontrivial extrinsic. If object range approaches zero, yaw error contributes little translation error.

## Independent evidence and MATLAB-style design boundary

The independent calculation separately constructs the true and estimated camera transforms, solves the elbow-down IK equations, applies forward kinematics, and evaluates the same state-gating conditions. It imports no production experiment, consumes no production result, and perturbs no production value. Five scenario records retain frame-sensitive signatures independently from production outputs.

No live camera, fiducial detector, MATLAB Robotics System Toolbox, motion controller, gripper, browser accessibility session, learner validation, physical HIL, or robot-cell test was executed. Deterministic planar evidence demonstrates interface logic and failure detection only. It does not establish calibration accuracy, collision safety, or production throughput.

## Engineering review checklist

- Attach an explicit frame and timestamp to every pose.
- Verify transform direction and multiplication order with a nontrivial round trip.
- Propagate calibration and measurement uncertainty to a pickup tolerance decision.
- Reject unreachable IK instead of hiding it through cosine clipping.
- Check joint limits, branch continuity, and approach collision clearance.
- Gate lift on contact or pose evidence rather than commanded closure alone.
- Preserve separate evidence for estimation, kinematics, and task completion.
- Define retreat and re-observation behavior for failed contact.

## Common mistakes

Typical failures include treating camera and base frames as identical, applying the inverse extrinsic, mixing degrees and radians, or transforming position but not orientation. Other mistakes accept any finite IK result, ignore the second branch, compare the estimate with itself, or use a pixel threshold as a metre tolerance. A state machine can also advance because a gripper command was sent rather than because contact was verified. Finally, deterministic demo noise should not be presented as a calibrated stochastic sensor model.

## Focused check and teach-back

Write the camera-to-base point equation and identify which quantities are translations, rotations, and expressed frames. Explain why the broken endpoint can have a zero IK residual and still have a large pickup error. Then teach back the three gates for the lift transition: the target is transformed consistently, a valid joint solution exists, and physical contact error is within tolerance. Describe how increasing yaw error differs geometrically from increasing position noise, and state which additional sensor evidence you would require before using the sequence on hardware.
