# A-AERO integration evidence

Integrate these existing lessons: P16, P31, P32, P50, P51, P52.

Required evidence: Couple drag, balance, ride height, tire load sensitivity, and thermal limits without double-counting available grip.

## Derive and predict

Use P16: Derive speed scaling for aerodynamic force and power, then distribute downforce between axles. At fixed coefficients, force is proportional to v² and drag power to v³. Doubling speed therefore gives four times drag but eight times drag power. Front and rear downforce must sum to the total, and their lever arms determine pitch moment. More downforce can improve grip while consuming power through drag; neither an axle split nor a favorable sign creates free energy. Connect this result to at least one other listed lesson, identifying the exact quantity, units and assumption transferred across their interface.

## Compare connected mechanisms

Use P32: Derive dissipated slip power and close accumulated work against stored heat plus cooling. Longitudinal slip work rate is the magnitude of Fx*v*kappa; lateral slip work rate uses Fy*v*tan(alpha). Each is newtons times metres per second, hence watts. Integrate those rates over time and compare with C*(T-T0) plus rejected heat. Removing cooling from the temperature update while continuing to report it in the ledger double-counts energy removal. A nonnegative power trace alone cannot prove thermal closure. Connect this result to at least one other listed lesson, identifying the exact quantity, units and assumption transferred across their interface.

## Diagnose and recover

Use P51: Predict how ride height shifts aero balance while speed changes all force magnitudes. At 80 mm, front coefficient is 0.58 and rear 0.72, so front balance is 0.58/1.30, about 44.62 percent. Dynamic pressure times area scales both with v². The pitch moment is rear force*1.5-front force*1.2; balance percentage alone does not determine its sign without lever arms. A millimetre value used as metres can yield absurd coefficients even though the v² scaling remains intact. Connect this result to at least one other listed lesson, identifying the exact quantity, units and assumption transferred across their interface.

## Integrate and defend the boundary

Use P52: Identify whether grip, power, energy or the declared thermal proxy limits the operating point. Tractive force is min(tire capacity,210000/v); acceleration subtracts drag before dividing by mass. At fixed speed, more energy increases energy-limited laps until the thermal-lap proxy becomes active. Downforce raises normal load once, with a sublinear load exponent; counting it twice inflates capacity. Per-lap energy includes 3.60 MJ plus drag times 4200 m. Acceleration and lap-count errors are scaled by 1 m/s² and 1 lap before combining into a dimensionless diagnostic. Connect this result to at least one other listed lesson, identifying the exact quantity, units and assumption transferred across their interface.

## Required integration artifact

Prepare a setup ledger with speed-squared force, speed-cubed power, front/rear balance, pitch moment, ride-height sensitivity and sublinear tire-load response. Track downforce exactly once into total normal load. Identify whether power or grip limits acceleration and whether energy or the declared thermal proxy limits stint length. Use separate units for per-lap energy and predicted laps. Compare the P52 empirical stint proxy with P50's integrated heat ledger and P67's adiabatic brake calculation, explicitly stating that none is a coupled measured thermal-performance model.

## Four-criterion rubric

1. Governing reasoning: equations, units and frame/sign conventions justify a numerical prediction; naming an algorithm alone earns no evidence.
2. Controlled comparison: two isolated sweeps and at least one limiting case distinguish mechanisms and make a falsifiable claim.
3. Diagnose and recover: identify the first failing assumption from actual outputs, restore it and demonstrate deterministic recovery.
4. Integration and scope: show the value passed between stages, an independently checked result, and a limitation that prevents a broader claim.

Retain inputs, selected outputs and your explanation as a cumulative artifact. No learner completion, automatic score, physical qualification or production acceptance is recorded.
