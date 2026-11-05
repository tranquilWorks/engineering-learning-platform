# P14 course checkpoint

## Predict and derive

Decide whether a wheel-force crossover occurs before the engine reaches redline.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `Expanded torque polynomial with an independent closed-form crossing root and shifted-RPM evaluation`

## Controlled comparison

- `current_gear_ratio`: 2.188 → 1.4. Hold the other controls at baseline; predict and explain the change before executing.
- `next_gear_ratio`: 1.541 → 2.187. Hold the other controls at baseline; predict and explain the change before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

Compare the current and next gear at the same road speed, which means different engine speeds. Solve force equality only inside both gears' valid engine bands. If no crossing occurs before redline, report a redline-limited shift rather than inventing an intersection. A higher-ratio gear is not always faster because its torque-map point and speed range change. Check the selected event against both force and rpm traces.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

An instantaneous crossover analysis excludes shift interruption and driver or actuator latency; P47 adds a bounded interruption model.

Competency links: VD-POWERTRAIN. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.


# Retained scoped evidence task

# P14 evidence task

## Predict before comparing curves

At the default 2.188-to-1.541 ratios, predict whether the next gear catches current-gear wheel force before 7400 RPM. Calculate the post-shift RPM at redline using the ratio quotient. Evaluate the torque map at both engine speeds, then convert both torques to wheel forces. Retain your units and sign convention for the force gap.

Your evidence should distinguish approximately 5393.76 N current force from 4417.81 N next force at the default decision. Explain why a −975.95 N next-minus-current gap means the returned redline is not a force crossover. State what additional objective or constraint might still justify shifting there.

## Two ratio investigations

First hold next ratio 1.541 and vary current ratio through valid and invalid orderings. Record the decision label, available RPM metrics and force comparison. Explain why the nominal sweep omits invalid pairs while the main panel can still show formal curves.

Then hold current ratio 2.09 and select next ratios 1.5, 2.08 and 2.09. Predict the classification before each run. For 2.09 to 2.08, reproduce the crossover near 7399.34147 RPM and check actual force equality, approximately 5152.63672 N on each side. For equal ratios, report the decision as unavailable instead of inventing a zero or redline recommendation. Both near-equal values are reachable using the 0.001 steps.

## Failure and exact recovery

Keep the 2.09-to-2.08 pair selected and activate the torque-lookup fault. Record the still-correct kinematic post-shift RPM, wrong next-gear force curve, maximum lookup error and changed decision classification. Explain why correct kinematics alone cannot validate a torque lookup. Disable the fault without moving either ratio and verify recovery of the crossover. Reset only afterward.

## Reasoning rubric

A complete response distinguishes all three outcomes, applies the RPM ratio in the torque lookup, checks an actual force residual at the crossover, and separates a resolved decision from the sampled plot grid. It also explains why one coincident force point cannot validate the full faulty curve.

An incomplete response calls every 7400 RPM return a crossover, accepts equal/ascending ratios as an upshift, or assumes this simplified rule minimizes lap time. Identify the missing shift-duration or traction assumptions in your explanation. This is a formative comparison: no learner score is stored, and the results do not certify a real engine, gearbox, learner outcome or whole course.
