# P31 course checkpoint

## Predict and derive

Close tire heat balance and apply the gas law using absolute temperature and pressure.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `C_th*dT/dt=Q_in-h*(T-T_amb)`
- `p/p_0=T_K/T_0K`
- `mu=mu_peak*exp(-((T-T_opt)/w_T)^2)*(1-k_p*(p-p_opt)^2)`

## Controlled comparison

- `heat_input_w`: 900 → 2200. Hold the other controls at baseline; predict and explain the change before executing.
- `ambient_temp_c`: 25 → -5. Hold the other controls at baseline; predict and explain the change before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

With C=15000 J/K and h=35 W/K, thermal time constant is C/h, about 428.57 s. A 900 W constant heat input approaches a 25.71 K temperature rise. Pressure scales with kelvin temperature, so 210 kPa at 293.15 K becomes 210*(T_C+273.15)/293.15 kPa. Celsius ratios can produce nonsense even if the plotted temperature is plausible. Separate the synthetic grip-temperature law from the thermodynamic ledger.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

Fixed volume, ideal gas and lumped cooling exclude carcass gradients, leakage, humidity and measured pressure/grip calibration.

Competency links: VD-TIRE-LONG, VD-TIRE-LAT, VD-AERO-ENERGY. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
