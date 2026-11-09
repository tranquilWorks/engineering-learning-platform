# P13 course checkpoint

## Predict and derive

Trace engine torque through gearing to wheel force and distinguish available from delivered power.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `Shaft-power and traction-limited work formulation, inverted to delivered force and torque`

## Controlled comparison

- `engine_torque_n_m`: 250.0 → 80.0. Hold the other controls at baseline; predict and explain the change before executing.
- `gear_ratio`: 3.0 → 4.2. Hold the other controls at baseline; predict and explain the change before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

At wheel radius r, available force is engine torque times gear and final-drive ratios times efficiency divided by r. Wheel power equals delivered force times road speed; if tire capacity clips force, available engine power is not all delivered as translational power. Increasing ratio raises wheel force but reduces road speed at a fixed engine speed. Retain both mechanical conversion and traction constraints in the ledger.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

This bounded driveline study does not resolve clutch slip, engine transients or tire heating.

Competency links: VD-POWERTRAIN. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.


# Retained scoped evidence task

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
