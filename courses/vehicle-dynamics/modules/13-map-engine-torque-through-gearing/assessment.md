# P13 evidence task

## Prediction and baseline calculation

Before running, predict whether the 250 N·m, ratio-3 baseline reaches the traction cap. Calculate engine angular speed from V/R and the two gear ratios, convert it to RPM, and compute the force request with 90% efficiency. Report units at every step. Reproduce approximately 8785.71 N applied force, 195238.10 W delivered shaft power and 175714.29 W wheel power. Explain the remaining 19523.81 W using the declared loss assumption.

## Two controlled investigations

First hold ratio 4.2 and compare requested torques 260 and 270 N·m. Predict which side of the capacity boundary each occupies. Record requested force, applied force, delivered torque and curtailed request. The relevant threshold is about 263.195 N·m; do not claim the stepped control selected that exact boundary.

Then hold 320 N·m and vary ratio through three accessible values spanning the available range. Use the force-versus-ratio response and the separate RPM sweep together. Identify where applied force flattens while RPM continues to increase. Explain why these trends are compatible, and why comparing their numerical slopes without units would be meaningless.

## Failure and exact recovery

At 320 N·m and ratio 4.2, record the nominal budget: 287760 W delivered, 258984 W at the wheels, 28776 W declared drivetrain loss, and about 62106.67 W of curtailed request. Toggle the loss-omission fault without changing controls. Check both the force cap and the power-budget residual. If the applied force remains capped in both modes, explain why that agreement does not validate the faulty transmission calculation.

Disable the fault at the same inputs and verify restoration of the nominal budget. Reset parameters only afterward. Save your selected inputs and calculations with the evidence so another reader can reproduce the comparison.

## Reasoning rubric

A complete explanation distinguishes request, delivery, dissipation and curtailment; closes both power balances with units; locates the force-cap boundary; and diagnoses the executed fault even when force saturation hides a difference. It also explains why the kinematic RPM is not an engine-feasibility guarantee.

An incomplete explanation treats all missing requested power as heat, checks only the force cap, or changes inputs while comparing failure and recovery. Revise those parts before moving on. As a transfer question, state which axle-load and engine-speed constraints would be needed for a real rear-drive vehicle. This is formative evidence: no learner score is stored, and no measured-vehicle, hardware or course-wide acceptance is inferred.
