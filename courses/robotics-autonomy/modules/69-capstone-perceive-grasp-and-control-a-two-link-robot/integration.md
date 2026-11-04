# Executed pickup, transfer and placement

The earlier plots isolate geometric preflight and contact requirements. The plots below add an executed planar manipulation sequence. A reachable inverse-kinematics solution alone cannot establish placement: the arm must arrive with low speed, verify that the object lies within the gripper capture radius, support its weight, carry it to the destination, release it and retreat. Read the event table together with the object trajectory; an endpoint trace without object motion is not a successful transfer.

## Frames and observation

The camera reports a point in metres. The true object is the camera point (0.72, 0.18) transformed by a 25° rotation and a (0.28, 0.12) m translation into the vertical arm plane. The controlled vision error adds `(0.006, −0.0035) × vision_noise_cm` metres in camera coordinates. This is a deterministic perturbation, not a sampled noise distribution. The yaw control, where present, perturbs the estimated camera rotation; P69 fixes this residual at 0.8°. Broken mode omits the extrinsic entirely. Neither a correct IK calculation nor a stable servo can repair a point expressed in the wrong frame.

Before running, transform the baseline point by hand and compare the true and estimated coordinates. Predict whether the discrepancy exceeds the 0.055 m capture tolerance. Increasing the signed perturbation need not monotonically increase total error: translational and angular errors can partly cancel. Test that prediction with two isolated sweeps rather than assuming that every larger control value must worsen the result.

## Arm dynamics and control

The arm has link lengths 0.75 and 0.55 m, point masses 1.0 and 0.7 kg at the link endpoints, and a 0.45 kg object added to the second endpoint while attached. Joint angles are measured counterclockwise from the horizontal; gravity points downward. Links have no distributed inertia. With `c = cos(q₂)` and second endpoint mass `m₂`, the inertia matrix is

$$M=\begin{bmatrix}(m_1+m_2)l_1^2+m_2l_2^2+2m_2l_1l_2c&m_2l_2^2+m_2l_1l_2c\\m_2l_2^2+m_2l_1l_2c&m_2l_2^2\end{bmatrix}.$$

The plant integrates `M q̈ + C + g + 0.025 q̇ = τ`. Coriolis terms are `C₁ = −m₂l₁l₂ sin(q₂)(2q̇₁q̇₂ + q̇₂²)` and `C₂ = m₂l₁l₂ sin(q₂)q̇₁²`. The gravity vector is the gradient of endpoint gravitational potential. A computed-torque controller requests `M[36(q*−q)−12q̇] + C + g + 0.025q̇`, then clips each actual torque to ±25 N m. Without clipping and model mismatch, each joint error obeys a critically damped second-order equation with natural frequency 6 rad/s. During clipping that simplification no longer holds: the coupled plant must be integrated.

The task logic runs every 0.01 s; eight RK4 substeps resolve saturation crossings inside each task tick. The independent reference constructs inertia and bias forces from Cartesian endpoint Jacobians and uses adaptive DOP853 integration. Comparing whole joint, endpoint and object histories checks more than a terminal success flag. This is a deterministic rigid-link simulation with exact controller mass parameters; it does not establish robustness to uncertain payload, flexible links, contact impulses or real actuators.

## Events, grasp and release

The phase indices are 1 observe/transform, 2 approach, 3 close gripper, 4 verify grasp, 5 lift, 6 transfer, 7 release, 8 retreat, 9 failure and 10 completed. Phase transitions are evaluated at task ticks. Approach, lift, transfer and retreat require joint target error below 0.005 rad and speed below 0.015 rad/s. A phase that fails to complete in five seconds terminates with an explicit failure.

Normal force ramps to 10 N per jaw at 30 N/s. Attachment requires both the geometric capture test and `2 μ F ≥ m_object g`. At 10 N the minimum coefficient is `0.45 × 9.81 / 20 = 0.220725`. P62 fixes μ = 0.5; P69 exposes it. With μ = 0.1, increasing visual accuracy cannot make the grasp support the object. Verify that the object remains at its original position in this failure, rather than following the arm because the task requested a transfer.

Once attached, the object follows the actual endpoint with the measured initial grasp offset preserved. The transfer IK target compensates this offset, so the object—not merely the gripper—approaches (0.50, 0.55) m. Release detaches the object onto an ideal support surface and ramps the force down. The object then remains fixed while the arm retreats 0.15 m above the target. Completion additionally requires placement error below 0.02 m. This ideal supported release does not simulate falling, bouncing, slip, finger geometry or force closure in three dimensions. The earlier scalar impedance/energy-tank experiment in P69 is a separate contact study; its tank state does not drive this jaw-force ramp.

## Diagnose and recover

First keep yaw/friction at baseline and sweep vision perturbation. Compare grasp offset, actual carried-object trajectory and placement error; explain why offset compensation can yield accurate placement after a moderately inaccurate pickup. Next isolate yaw in P62 or friction in P69. Find the boundary where attachment is rejected, identify the event that fails and show that transfer never begins. Enable broken mode without changing numeric controls: skipping the camera transform should produce a geometric miss. Restore healthy mode and verify the complete event sequence and deterministic return of the trajectory.

Report the event times, maximum applied torque, pickup error and final object error with units. Identify which findings come from the geometric preflight, which from the separate contact study, and which from this executed sequence. A successful simulation establishes only this bounded planar model. It supplies no hardware, perception-dataset, human assessment or physical grasp qualification.
