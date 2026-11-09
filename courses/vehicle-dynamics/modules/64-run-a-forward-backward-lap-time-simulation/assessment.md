# P64 course checkpoint

## Predict and derive

Close every periodic segment's force and energy ledger, including the final segment back to the first.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `F_i=m(v_next^2-v_i^2)/(2 ds_i)+c*v_i^2+R N on a periodic grid`
- `-0.5 mu mg<=F_i<=min(0.5 mu mg,P/v_i); m v_i^2 kappa_i<=sqrt(0.75)mu mg`
- `E=sum max(F_i ds_i,0) J; scale v^2 by beta to meet budget; E>=R*length`
- `brake_temperature=20 degC+sum max(-F_i ds_i,0)/(32 kg*500 J/(kg K))`

## Controlled comparison

- `grip_scale`: 1.15 → 0.8. Hold the other controls at baseline; predict and explain the change before executing.
- `energy_limit_mj`: 3.0 → 0.8. Hold the other controls at baseline; predict and explain the change before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

Segment force is m*(v_next²-v²)/(2*ds)+drag+rolling resistance. Check traction, power, braking and lateral reserve at each segment. Available energy must at least cover rolling resistance times track length; below that floor the model must report infeasibility rather than a zero-speed successful lap. Distinguish propulsive work from brake heat and count downforce only where actually modeled. A uniform squared-speed scaling can enforce an energy budget but still needs the force bounds rechecked.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

The discrete synthetic lap uses prescribed force reserves and a lumped adiabatic brake temperature, not a validated optimal-control or fade-coupled model.

Competency links: VD-PERFORMANCE-OPTIMIZATION. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
