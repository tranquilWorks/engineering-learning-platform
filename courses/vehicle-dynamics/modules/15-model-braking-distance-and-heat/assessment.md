# P15 course checkpoint

## Predict and derive

Close kinetic energy, stopping work and absorbed brake heat as separate quantities.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `Kinetic-energy/work stop solution and fractional stopping-time energy trajectory`

## Controlled comparison

- `initial_speed_m_s`: 30.0 → 5.0. Hold the other controls at baseline; predict and explain the change before executing.
- `requested_brake_force_n`: 10000.0 → 18000.0. Hold the other controls at baseline; predict and explain the change before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

Initial kinetic energy is m*v0²/2, so doubling initial speed quadruples energy. Integrate the actual resisting force over stopping distance and account for road losses before allocating brake heat. Peak temperature depends on the stated heat capacity and absorption fraction. Tire-limited braking can change force and distance while the same initial kinetic energy still has to leave the vehicle.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

The lumped heat ledger is not rotor stress, fade qualification or a complete low-speed ABS model.

Competency links: VD-BRAKES. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.


# Retained scoped evidence task

# P15 evidence task

## Predict the two budgets

Before running the baseline, calculate the tire-force cap and decide whether the 10000 N request reaches it. At 30 m/s, derive the stopping time and distance from constant deceleration, then verify Fd = ½mV². Your record should include approximately 3.96 s, 59.4 m and 594000 J. Explain which area and slope on the speed-time plot correspond to distance and acceleration.

Allocate the energy using the declared 85% rotor and 15% other-heat fractions. Divide rotor heat by the combined heat capacity to obtain the temperature rise. Distinguish this approximately 39.20031 °C rise from an absolute temperature, and state the assumed initial-temperature information that would be needed for the latter.

## Two one-variable sweeps

First hold 10000 N and compare initial speeds 10, 20 and 40 m/s. Predict the ratios of stopping distance, stop time and final temperature rise before collecting results. Check that your explanation uses quadratic energy scaling rather than a linear speed analogy.

Then hold 30 m/s and compare requests 10000, 13500, 14000 and 18000 N. Identify where the cap binds. Explain why the last two requests cannot continue reducing distance in this model. Compare the initial braking powers using FV, while verifying that total stopping work and the final nominal temperature rise remain unchanged at fixed initial speed.

## Failure and recovery evidence

Return to 30 m/s and 10000 N. Activate the heat-allocation fault without changing either input. Record the unchanged stopping trajectory, increased rotor temperature rise and 0.15 normalized heat-budget residual. Convert that residual back to approximately 89100 J and identify the duplicated energy allocation. Disable the fault at the same inputs and verify restoration of the heat budget before resetting parameters.

## Reasoning rubric

A complete response independently closes force/work, heat allocation and axle-load balances; respects the tire cap; and explains how a thermal fault can leave a mechanically correct trajectory unchanged. It identifies that the temperature is a bulk rise and names an omitted cooling or brake-bias mechanism.

An incomplete response accepts the model solely because the stopping distance looks plausible, equates stronger braking with more initial kinetic energy, or reads a requested force as an applied force above the cap. Revise those claims using the selected numerical evidence. This is formative work: no learner score is stored, and synthetic plots do not establish measured stopping performance, hardware safety or whole-course acceptance.
