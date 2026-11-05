# P34 course checkpoint

## Predict and derive

Derive the two-state bicycle matrix from axle forces and verify its steady state by physical balances.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `m U (beta_dot+r)=F_yf+F_yr`
- `I_z r_dot=a F_yf-b F_yr`
- `x_dot=A(U,C_f,C_r)x+B delta`

## Controlled comparison

- `speed_m_s`: 25 → 40. Hold the other controls at baseline; predict and explain the change before executing.
- `front_cornering_n_rad`: 70000 → 95000. Hold the other controls at baseline; predict and explain the change before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

Use beta_dot=(Fyf+Fyr)/(m*v)-r and r_dot=(a*Fyf-b*Fyr)/Iz. The -r term is essential even when tire forces are linear. At steady turn, zero state derivatives still require nonzero m*v*r lateral force. Changing the rear stiffness sign can produce unstable poles while a linear solver still returns numbers. Compare eigenvalues, the independently reconstructed force balance and the separately labeled sideslip and yaw-rate axes.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

This linear constant-speed system omits saturation and actuator/tire dynamics. Pole stability does not establish a large-steer maneuver's feasibility.

Competency links: VD-HANDLING-LINEAR. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
