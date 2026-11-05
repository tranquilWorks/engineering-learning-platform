# P62 course checkpoint

## Predict and derive

Construct the feasible acceleration envelope from tire-force and engine-power constraints at the same speed.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `down=0.5 rho A Cl v^2 N; drag=0.5 rho A Cd v^2 N; capacity=mu(mg+down) N`
- `Fx=min(capacity cos(theta),P/v); Fy=capacity sin(theta); ax=(Fx-drag)/m`
- `demand utilization=hypot(Fx,Fy)/capacity; power demand=Fx*v W`

## Controlled comparison

- `speed_m_s`: 45 → 20. Hold the other controls at baseline; predict and explain the change before executing.
- `friction_coefficient`: 1.2 → 1.5. Hold the other controls at baseline; predict and explain the change before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

Total force capacity is mu*(mg+downforce). For a requested direction, compute Fx and Fy, then cap positive Fx by P/v while preserving the already-declared lateral component. The resulting point must satisfy the shared tire norm and power limit. At v=45 m/s a 210 kW power ceiling corresponds to 4666.67 N before drag. Subtract drag only when converting force to acceleration, and distinguish propulsion from braking.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

The envelope uses a simplified aggregate tire bound and fixed aero coefficients; it is not a transient maneuver or a calibrated four-wheel model.

Competency links: VD-PERFORMANCE-OPTIMIZATION. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
