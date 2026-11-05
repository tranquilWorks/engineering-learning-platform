# P50 course checkpoint

## Predict and derive

Close each repeated-stop heat increment and derive the cooling recurrence before discussing fade.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `Delta T_stop=eta E_stop/C_brake`
- `C_brake dT/dt=-h_c(T-T_ambient)`
- `E_absorbed=Delta E_stored+E_rejected`

## Controlled comparison

- `stop_energy_kj`: 450 → 650. Hold the other controls at baseline; predict and explain the change before executing.
- `cooling_coefficient_w_k`: 65 → 110. Hold the other controls at baseline; predict and explain the change before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

A 450 kJ stop deposits 0.75*450=337.5 kJ into a 45000 J/K lump, raising it by 7.5 K before cooling. Between stops, excess temperature decays toward ambient with time constant C/h. Sum absorbed heat, stored heat and rejected heat over all six stops. The fade factor follows peak temperature; final cooled temperature can hide that peak. The broken mode reports rejected heat without removing it from storage, so its energy ledger cannot close.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

The empirical fade law is evaluated from temperature but does not feed back into the stop energy or distance. This is a thermal study, not coupled brake-performance qualification.

Competency links: VD-BRAKES, VD-AERO-ENERGY. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
