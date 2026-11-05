# P26 course checkpoint

## Predict and derive

Use concavity to predict the loss from unequal tire loading at fixed total normal load.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `F_peak(F_z)=mu_ref*F_ref*(F_z/F_ref)^n`
- `mu(F_z)=F_peak(F_z)/F_z`
- `Delta_F=2*F_peak(F_z)-F_peak(F_z*(1-lambda))-F_peak(F_z*(1+lambda))`

## Controlled comparison

- `normal_load_n`: 3500 → 6500. Hold the other controls at baseline; predict and explain the change before executing.
- `load_exponent`: 0.88 → 0.72. Hold the other controls at baseline; predict and explain the change before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

Peak force is 1.25*3500*(Fz/3500)^n. With n=0.88, doubling Fz multiplies peak force by 2^0.88, about 1.84, so effective friction decreases. For equal tires carrying W/2 each, concavity gives f(W/2-T)+f(W/2+T) no greater than 2*f(W/2). The exponent-one broken mode removes that penalty. Read effective friction on its own axis and compare capacity losses in newtons.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

The empirical exponent is declared, not fitted to measured tire data; extrapolation to zero contact or extreme loads needs care.

Competency links: VD-TIRE-LONG, VD-TIRE-LAT. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
