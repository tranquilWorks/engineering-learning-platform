# Solve and Check Steady Bicycle Equilibrium

Does a finite bicycle-model solution actually satisfy both force and yaw-moment equilibrium?

## Physical model

Use a left-positive body frame, positive counterclockwise yaw rate r, speed V, and sideslip β. The input is **road-wheel steer** δ, unlike P01's steering-wheel input. Distances from the centre of gravity are l_f = 1.15 m and l_r = 1.42 m, giving L = 2.57 m. Mass is 1320 kg; axle cornering stiffnesses are C_f = 90000 and C_r = 100000 N/rad.

Define force-positive axle slips α_f = δ − β − l_f r/V and α_r = −β + l_r r/V. Forces are F_yf = C_f α_f and F_yr = C_r α_r. This angle convention is the negative of P06's velocity-minus-wheel angle.

Steady balance requires F_yf + F_yr = mVr and l_f F_yf − l_r F_yr = 0. Solving balance first gives F_yf = mVr l_r/L and F_yr = mVr l_f/L. Substituting those into tire compatibility gives r = δ/[L/V + (mV/L)(l_r/C_f − l_f/C_r)], then β = l_r r/V − F_yr/C_r. This is also an independent way to check the matrix solution used by the live model.

The response is a family of steady yaw rates versus prescribed speed, not a yaw transient. Both residual metrics have their own physical units: N and N·m.

\[
F_{yf}+F_{yr}=mVr,\qquad l_f F_{yf}-l_r F_{yr}=0.
\]

## Worked baseline

At δ = 3° and V = 18 m/s, r = 0.287176585 rad/s and β ≈ −0.00787730 rad. Front and rear slips are about 0.041889789 and 0.030532346 rad. The axle forces are about 3770.081 and 3053.235 N, summing to mVr ≈ 6823.316 N. Their moments cancel within floating-point tolerance. A nonzero negative sideslip does not by itself imply an invalid left turn.

## Predict and sweep

Before moving a control, write a sign and a trend prediction with units. The two sweep panels always show the **nominal** relationship with the other selected input fixed, even while the fault toggle is active. The response panel follows the selected mode. The comparison panel shows both modes at identical inputs; it is not a time sequence of failure and repair.

1. Keep V = 18 m/s and vary road-wheel steer from −8° to +8°. Predict a linear odd yaw response because the model linearizes steering and tire force. Check force and moment residuals as well as yaw sign.
2. Keep δ = 3° and vary speed from 3 to 40 m/s. Predict that yaw will not simply follow the kinematic Vδ/L law: axle compliance enters the denominator. At larger excitation, inspect the separate small-angle assumption even if algebraic equilibrium still closes.

## Named broken behavior

The toggle reproduces inconsistent speed factors in the old matrix: the lateral coefficient is divided by speed where it should not be, while the yaw coefficient loses a required division by speed. A finite matrix result is still obtained, but it no longer solves the declared balances. At defaults the old solution has force residual about −59312.35 N and yaw-moment residual about +17136.73 N·m. The same-input comparison exposes a different yaw curve, and the two residual metrics identify why the change is wrong. Zero steer is benign for this fault because the homogeneous solution is zero.

## Exact recovery

Disable the fault without moving either input. Check that the selected response returns to the nominal member of the same-input comparison and explain which governing relation has been restored. Only then use **Reset parameters** to reproduce the worked baseline. Resetting inputs and repairing the model are separate actions; changing both at once prevents a causal comparison.

## Limits and limiting cases

This is a linear steady-state bicycle model with axle-level forces and constant speed. It has no tire saturation, transient yaw dynamics, roll, load sensitivity or actuator lag. The lesson separately checks |δ|, |β| and both |α| against an 8° small-angle teaching bound. Equilibrium correctness and approximation validity are different questions: tiny balance residuals do not make large-angle predictions physically validated. The response curve can include points outside that approximation; it remains a formal linear-model sweep.

## Common mistakes

Do not accept a matrix inverse merely because it returns finite values. Check the original force and moment equations using the resulting tire forces. Do not confuse road-wheel steer with P01's steering-wheel angle or P06's opposite slip convention.

## Formative checks

At the defaults calculate both tire forces from the displayed slips and verify the force and yaw-moment residuals. Repeat with the matrix fault active, keeping inputs fixed. Then increase steering and explain how an equilibrium-correct answer can still fall outside the small-angle approximation.

Check your reasoning: A correct calculation closes both independent balances at about 6823.316 N total lateral demand. The old matrix produces large nonzero residuals despite a finite solution. Credit requires both residuals with units and a separate discussion of angle validity; declaring every finite or balanced result physically valid is insufficient.

## Teach-back checklist

Explain the declared input convention and governing equation before describing the curve. Reproduce the worked calculation with units, account for both one-variable trends, and identify a discriminating fault test. Finish by naming the specific limiting case above and the physical effects omitted by this model. The embedded Course checkpoint asks for evidence and reasoning; no learner score is stored.

This is deterministic synthetic teaching evidence, **not measured-vehicle** validation, a MATLAB-runtime comparison, or representative-learner acceptance. The original conversion ledger remains historical. This revision verifies the declared native model and its revised fault independently; it does not claim unchanged full-source equivalence.
