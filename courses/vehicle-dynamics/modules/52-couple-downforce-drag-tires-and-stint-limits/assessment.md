# P52 course checkpoint

## Predict and derive

Identify whether grip, power, energy or the declared thermal proxy limits the operating point.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `F_tire=mu_ref F_z,ref[(m g+F_down)/F_z,ref]^0.86`
- `a_usable=[min(F_tire,P/v)-F_drag]/m`
- `N_stint=min(E_stint/E_lap,N_thermal)`

## Controlled comparison

- `speed_m_s`: 55 → 70. Hold the other controls at baseline; predict and explain the change before executing.
- `stint_energy_mj`: 120 → 180. Hold the other controls at baseline; predict and explain the change before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

Tractive force is min(tire capacity,210000/v); acceleration subtracts drag before dividing by mass. At fixed speed, more energy increases energy-limited laps until the thermal-lap proxy becomes active. Downforce raises normal load once, with a sublinear load exponent; counting it twice inflates capacity. Per-lap energy includes 3.60 MJ plus drag times 4200 m. Acceleration and lap-count errors are scaled by 1 m/s² and 1 lap before combining into a dimensionless diagnostic.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

The thermal-lap expression is an empirical teaching proxy, not an integrated temperature model. P50 and P67 provide different, explicitly bounded thermal ledgers.

Competency links: VD-AERO-ENERGY, VD-SYSTEM-INTEGRATION. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
