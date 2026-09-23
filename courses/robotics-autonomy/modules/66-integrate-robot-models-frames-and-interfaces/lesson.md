# Integrate robot models, frames, and interfaces

Robot integration fails at boundaries more often than inside a well-tested algorithm. An encoder driver can report valid numbers, a kinematic model can return invertible matrices, and a controller can publish commands, yet the physical tool pose is wrong because one boundary changed units, frame direction, or time semantics. This laboratory combines typed encoder conversion, a nontrivial planar frame graph, timestamp freshness, and an independent tool-pose comparison so that integration evidence cannot hide behind finite outputs.

## Model, derivation, and conventions

Two joint angles are encoded as counts with `4096` counts per revolution. The interface contract declares radians per count as `2 pi/4096`; an adjustable scale error represents calibration drift. Conversion occurs exactly once, before any trigonometry. The model then composes `T_base^shoulder`, `T_shoulder^elbow(q_1)`, and `T_elbow^tool(q_2)` in that order. The base-to-shoulder transform includes nonzero translation and rotation so an accidental identity assumption cannot pass.

Homogeneous transforms use column points and left multiplication. Each planar transform belongs to `SE(2)`: the upper-left block is a rotation and the final row is `[0,0,1]`. The inverse residual `||T T^{-1}-I||_F` checks group arithmetic. A separate endpoint error compares the composed tool translation with a measurement generated from the true joint state. These checks answer different questions: algebraic consistency does not establish semantic correctness.

Three interface stages carry message ages from zero to the selected skew. A `20 ms` freshness limit yields an explicit contract violation when exceeded. Unit and type violations are counted separately in the broken configuration.

## Predict before running

Predict that a small encoder scale error produces a small but nonzero endpoint discrepancy while transform inversion remains near machine precision. Increasing scale error alone should enlarge the discrepancy. Increasing timestamp skew alone should leave geometry unchanged but add a freshness violation. That separation is intentional: it lets reviewers identify which interface dimension changed.

Broken mode converts the decoded radians to numerical degrees and then supplies those degree values to sine and cosine as though they were radians. Every matrix remains finite and invertible. Predict that the inverse residual will still be tiny even though endpoint error becomes large. This is the central lesson: mathematical closure of the chosen representation cannot prove the inputs obey their declared contract.

## Baseline workflow

Run with `0.2 percent` encoder scale error and `8 ms` timestamp skew. Inspect the integrated chain and measured tool marker in the response plot. Their small separation is the physical integration residual. Confirm that the interface violation count is zero because every age is below `20 ms`.

Compare endpoint error with the frame inverse residual. The latter should be many orders of magnitude smaller. It verifies that the matrix can invert itself, not that the matrix describes the robot. A system review should retain both results: group checks catch malformed transforms, while independent pose evidence catches unit, ordering, calibration, and model defects.

## Two one-variable sweeps

For sweep one, increase only encoder scale error from `0.2` to `2.0 percent`. Timestamp skew, true pose, link lengths, and frame graph remain fixed. The endpoint should move away from the measured marker while inverse consistency remains excellent. This demonstrates a calibrated-parameter failure rather than a frame algebra failure.

For sweep two, restore scale error and increase only timestamp skew from `8` to `35 ms`. Geometry should return to baseline, but the freshness contract should report one violation. A stale message can contain the correct unit and plausible value; time validity is an independent interface dimension. Real systems must decide whether to hold, extrapolate, or fail safe instead of using stale state silently.

## Intentionally broken case

Broken mode represents two frequent integration shortcuts. First, it lacks a typed unit boundary, so a degree-valued number reaches an API that expects radians. Second, it bypasses unit and freshness checks, adding explicit contract violations. Because trigonometric functions accept any floating value, the error produces no exception. The frame matrix remains a valid rotation and the inverse residual passes.

The measured endpoint makes the semantic failure visible. In a physical robot, such a defect could send the tool through an obstacle while component tests stayed green. An even subtler version converts degrees to radians twice, producing a smaller but still dangerous error. Interface review must therefore trace both the declared unit and the location of conversion.

## Recovery

Recover by giving each joint message a schema that names position unit, source timestamp, frame or joint identifier, sequence, and validity. Convert raw counts to radians at the driver boundary exactly once. Reject or quarantine an age beyond the declared limit. Compose only transforms whose parent-child relationship matches the model graph, then compare at least one integrated endpoint with an independently observed pose.

For runtime recovery, retain the last certified state, command a safe hold, refresh the stale interface, and re-evaluate the full chain. Do not patch an endpoint by adding an unexplained offset; that hides rather than repairs the boundary error.

## Alternative and limiting cases

Three-dimensional robots use `SE(3)`, quaternions or rotation matrices, URDF-like model trees, and a transform buffer keyed by source time. Middleware interface definitions can encode units by convention, while stronger languages or generated wrappers can make units explicit types. Calibration optimizers estimate parameters from observations, but their outputs still require version and provenance contracts.

With zero scale error and fresh messages, endpoint discrepancy approaches floating precision. If every static transform is identity, wrong multiplication order may be invisible, so test fixtures need noncommuting rotations and translations. If timestamps share no clock basis, subtracting them is meaningless even when both are monotonic. If a chain contains a loop, every loop closure must be checked rather than assuming a tree.

## Independent evidence and MATLAB-style design boundary

The independent reference separately converts counts, builds each homogeneous transform, composes the frame chain, inverts it, computes message ages, and compares the tool endpoint. It imports no production experiment, consumes no production result, and perturbs no production value. Baseline, scale, time, broken, and recovery signatures are retained with identical declared units and tolerances.

No URDF parser, ROS transform graph, live encoder, MATLAB robotics toolbox, browser accessibility study, learner trial, physical HIL, calibration fixture, safety controller, or deployment was run. The model provides deterministic planar interface evidence only and does not certify an integrated robot.

## Engineering review checklist

- Declare unit, frame, source timestamp, identifier, and validity for every interface field.
- Convert raw measurements at one owned boundary exactly once.
- Use nontrivial transforms in order and inverse tests.
- Distinguish matrix validity from agreement with an independent physical observation.
- Reject stale or cross-clock timestamps before control use.
- Version model parameters and calibration scale with provenance.
- Keep parent-child transform direction explicit in names and tests.
- Define safe hold and refresh behavior for every contract failure.

## Common mistakes

Common errors mix degrees and radians, metres and millimetres, active and passive rotations, or parent-to-child with child-to-parent transforms. Other systems stamp a forwarded message with receipt time and erase its sensor age. A matrix round trip can pass after the same wrong convention is used in both directions. Developers may compare a model endpoint with a measurement derived from that same model, which is not independent evidence. Silent clipping and unexplained calibration offsets make later diagnosis harder.

## Focused check and teach-back

Explain why `T T^{-1}=I` can pass for the broken degree-as-radian chain. Identify the evidence that detects the semantic error. Then teach back the difference between encoder calibration error and timestamp staleness: one changes geometry, the other changes validity. State the transform multiplication convention and describe one nontrivial fixture that catches reversed order. Finally, name the safe behavior when a joint message is stale and the additional evidence required before claiming this integration on hardware.
