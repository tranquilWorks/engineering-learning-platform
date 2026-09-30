## P33 evidence task

Why can increasing the allowed speed cease to shorten the move?

Before running: Predict why distance divided by the speed limit is too short for a rest-to-rest cubic trajectory.

Collect a default record, one single-control sweep, the named fault and recovery. Record the parameter values, plotted quantities and units so another learner can reproduce the comparison.

Synchronized velocities plots Velocity (rad/s) against Time (s). Its series are Joint 1, Joint 2, Speed +, Speed −. Joint accelerations plots Acceleration (rad/s²) against Time (s). Its series are Joint 1, Joint 2.

### Reasoning rubric

- Model: reconstruct a displayed value using `q_i=d_i(3s²-2s³); s=t/T` and the actual state or geometry.
- Evidence: Increase displacement while holding speed bound fixed. Compare the linear speed-duration requirement with the square-root acceleration-duration requirement; identify which one sets the applied time.
- Diagnosis: The fault applies a fixed one-second duration instead of the derived duration. It then differentiates the actual applied cubic, so speed and acceleration violations follow from the trajectory.
- Recovery and scope: Restore derived timing and inspect both speed and acceleration constraints. A small speed excess alone cannot certify acceleration feasibility. State this boundary: At zero displacement the trajectory is stationary; the interactive displacement range remains positive to keep a nonzero duration. A short move or generous limits can make one second feasible, so the named fault does not guarantee a violation at every setting. Endpoint acceleration is nonzero and torque limits are absent.

### Check your explanation

The acceleration requirement then sets the shared duration. For the fixed cubic, speed scales as 1/T while acceleration scales as 1/T²; both constraints must be satisfied, and the larger required time wins.

A complete explanation contains a calculation, an observed comparison with units, the executed fault and a reproduced recovery. Name a setting that can hide the fault and a claim requiring evidence outside this model. This is a self-assessment; no learner score is stored.
