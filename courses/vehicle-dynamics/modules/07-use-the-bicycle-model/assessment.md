## P07 evidence task

At the defaults calculate both tire forces from the displayed slips and verify the force and yaw-moment residuals. Repeat with the matrix fault active, keeping inputs fixed. Then increase steering and explain how an equilibrium-correct answer can still fall outside the small-angle approximation.

Record one prediction before running, then retain the actual selected input values, the relevant metric units and two observations from the plotted relationship. Use the nominal sweeps to isolate one variable at a time. Compare the fault and nominal responses at fixed inputs before resetting to the worked baseline. If the two curves coincide, decide whether the lesson's benign limit explains that outcome; a coincident curve is not automatically a successful fault test.

### Reasoning rubric

A correct calculation closes both independent balances at about 6823.316 N total lateral demand. The old matrix produces large nonzero residuals despite a finite solution. Credit requires both residuals with units and a separate discussion of angle validity; declaring every finite or balanced result physically valid is insufficient.

A complete explanation links a quantitative check to its governing relation, distinguishes the requested or formal model result from its stated physical validity, and explains the recovery causally. A partially supported answer reports the expected trend but omits units, an input convention or the fault mechanism. An unsupported answer uses the status badge or curve shape alone as proof. Revise the explanation until a reader could reproduce the comparison from your recorded inputs.

### Check your reasoning

At δ = 3° and V = 18 m/s, r = 0.287176585 rad/s and β ≈ −0.00787730 rad. Front and rear slips are about 0.041889789 and 0.030532346 rad. The axle forces are about 3770.081 and 3053.235 N, summing to mVr ≈ 6823.316 N. Their moments cancel within floating-point tolerance. A nonzero negative sideslip does not by itself imply an invalid left turn.

Do not accept a matrix inverse merely because it returns finite values. Check the original force and moment equations using the resulting tire forces. Do not confuse road-wheel steer with P01's steering-wheel angle or P06's opposite slip convention.

Before continuing, state one prediction this model cannot support. Use the specific limitations in the lesson, rather than a general statement that every simulation has limits. This checkpoint is a self-check: **no learner score is stored**, and completing it does not establish measured vehicle performance or learner acceptance.
