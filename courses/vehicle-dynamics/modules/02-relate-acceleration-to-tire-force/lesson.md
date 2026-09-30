# Balance Traction, Road Loads and Acceleration

How much of the requested traction remains available to accelerate the vehicle?

## Physical model

Take forward force as positive, with mass m = 1320 kg and g = 9.81 m/s². Applied traction is min(F_request, μmg), with μ = 1. Rolling resistance is C_rr mg, C_rr = 0.015. Aerodynamic drag is ½ρ C_d A V², with ρ = 1.225 kg/m³, C_d = 0.31 and A = 2 m².

m a_x = F_applied − F_roll − F_drag.

The response is a signed force budget. Each ordinate is in newtons: positive traction, negative rolling resistance, negative drag and the model's net force. Acceleration is a separate metric in m/s². The net-force point is the sum of the first three points, not a fourth applied load to add again. Horizontal categories identify terms, not elapsed time.

The selectable requests end at 9000 N, below the declared 12949.2 N traction capacity. Consequently none of these controls reaches traction saturation. The cap is retained as an assumption, but this lesson cannot demonstrate its activation through the current request range.

\[
ma_x=F_{\mathrm{applied}}-C_{rr}mg-\tfrac12\rho C_d A V^2.
\]

## Worked baseline

For 4200 N and 20 m/s, rolling resistance is 194.238 N and drag is 151.900 N. The net force is 3853.862 N and acceleration is 2.91959 m/s². At 40 m/s, drag becomes 607.600 N, four times its previous value. The acceleration is then about 2.57437 m/s². Doubling speed does not quarter acceleration: only the quadratic drag term changes, while traction and rolling resistance remain fixed.

## Predict and sweep

Before moving a control, write a sign and a trend prediction with units. The two sweep panels always show the **nominal** relationship with the other selected input fixed, even while the fault toggle is active. The response panel follows the selected mode. The comparison panel shows both modes at identical inputs; it is not a time sequence of failure and repair.

1. Hold speed at 20 m/s and vary requested traction from 0 to 9000 N. Predict a straight acceleration curve of slope 1/1320 (m/s²)/N and an intercept below zero. Zero acceleration occurs at about 346.138 N, where traction balances the two road loads.
2. Hold traction at 4200 N and vary speed from 0 to 55 m/s. Predict decreasing acceleration with a quadratic speed dependence. Read rolling resistance as constant in this model, and use the drag equation to account for the curvature of the sweep.

## Named broken behavior

The fault omits both road loads from the acceleration calculation while continuing to display their physical magnitudes. The default acceleration becomes 4200/1320 = 3.18182 m/s². The force-balance residual is therefore 346.138 N. The gap grows with speed because aerodynamic drag grows. At zero speed the fault still differs: it also omitted the nonzero constant rolling term. A former saturation-bypass example was ineffective across this control range; the current omission produces a testable causal discrepancy.

## Exact recovery

Disable the fault without moving either input. Check that the selected response returns to the nominal member of the same-input comparison and explain which governing relation has been restored. Only then use **Reset parameters** to reproduce the worked baseline. Resetting inputs and repairing the model are separate actions; changing both at once prevents a causal comparison.

## Limits and limiting cases

This is an instantaneous force balance at a prescribed nonnegative speed. Constant rolling resistance is an approximation for a rolling vehicle, not a static-friction rule at rest. With zero request and zero speed the formula predicts negative acceleration; it is not a trustworthy simulation of a parked car spontaneously reversing. No gearbox, traction-control dynamics, speed integration or tire-load transfer is included.

## Common mistakes

Drag depends on V², while aerodynamic power would depend on V³. Do not label the force-budget chart as power or time response. A traction ceiling that never activates is not evidence that a saturation implementation has been tested.

## Formative checks

At 20 m/s, calculate the traction request for zero acceleration. Compare the nominal and road-load-omission results at that request. Repeat the force accounting at 40 m/s, keeping the request fixed. Explain the sign of acceleration in each case and the limitation of the zero-speed endpoint.

Check your reasoning: At 20 m/s the balancing request is 346.138 N. Nominal acceleration is zero; omission incorrectly predicts about 0.262226 m/s². At 40 m/s the nominal result becomes negative because drag rises by 455.7 N. A complete response names all three force terms and avoids treating the low-speed approximation as a start/stop simulator.

## Teach-back checklist

Explain the declared input convention and governing equation before describing the curve. Reproduce the worked calculation with units, account for both one-variable trends, and identify a discriminating fault test. Finish by naming the specific limiting case above and the physical effects omitted by this model. The embedded Course checkpoint asks for evidence and reasoning; no learner score is stored.

This is deterministic synthetic teaching evidence, **not measured-vehicle** validation, a MATLAB-runtime comparison, or representative-learner acceptance. The original conversion ledger remains historical. This revision verifies the declared native model and its revised fault independently; it does not claim unchanged full-source equivalence.
