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
