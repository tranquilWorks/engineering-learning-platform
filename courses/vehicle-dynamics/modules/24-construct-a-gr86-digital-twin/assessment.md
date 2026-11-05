# P24 course checkpoint

## Predict and derive

Trace the original digital-twin interface from drive force through motion to requirement residuals.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `a=min((F_drive-0.5*rho*CdA*v^2)/m,0.35*mu*g); r=clip(v*tan(delta/13)/L,+/-mu*g/v)`

## Controlled comparison

- `vehicle_mass_kg`: 1320 → 1150. Hold the other controls at baseline; predict and explain the change before executing.
- `tire_friction_coefficient`: 1 → 1.3. Hold the other controls at baseline; predict and explain the change before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

Force divided by mass produces acceleration; time integration produces speed; wheel steering in radians produces yaw demand; friction bounds lateral acceleration. Missing degree conversion can be roughly a factor of 57.3 before saturation masks the error. Check speed, yaw and position residual requirements separately, then restore the exact nominal inputs. A requirement count must be reconstructed from its underlying residuals.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

This original integrated teaching model omits calibration and detailed subsystems; the broader executed synthetic integration is P67.

Competency links: VD-SYSTEM-INTEGRATION. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
