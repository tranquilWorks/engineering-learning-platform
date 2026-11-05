# A-POWERTRAIN integration evidence

Integrate these existing lessons: P13, P14, P44, P45, P46, P47.

Required evidence: Reconcile torque, inertia, gearing, traction, differential, and shift constraints over a bounded acceleration scenario.

## Derive and predict

Use P13: Trace engine torque through gearing to wheel force and distinguish available from delivered power. At wheel radius r, available force is engine torque times gear and final-drive ratios times efficiency divided by r. Wheel power equals delivered force times road speed; if tire capacity clips force, available engine power is not all delivered as translational power. Increasing ratio raises wheel force but reduces road speed at a fixed engine speed. Retain both mechanical conversion and traction constraints in the ledger. Connect this result to at least one other listed lesson, identifying the exact quantity, units and assumption transferred across their interface.

## Compare connected mechanisms

Use P44: Calculate wheel force and road speed at one engine operating point, then identify the active traction constraint. At 5000 rpm the declared torque map gives 218.5 N m. With gear 3.2, final drive 4.1, efficiency 0.92 and radius 0.31 m, available wheel force is about 8507.69 N. Driven-tire capacity is 1.15*1450*9.81*0.45, about 7361.18 N, so delivered force is capped. Raising gearing can increase available force without increasing delivered force in this regime. Check utilization and rpm-to-speed conversion together. Connect this result to at least one other listed lesson, identifying the exact quantity, units and assumption transferred across their interface.

## Diagnose and recover

Use P46: Compare open and biased differential force allocation under separate wheel capacities and one total demand. With 3200 N per wheel and left mu=0.35, the left capacity is 1120 N. The open differential supplies at most 2240 N total. A bias ratio of four requests 4480 N on the right, but right capacity is only 1.15*3200=3680 N; the capped total is therefore 4800 N. Unlimited multiplication would exceed the high-grip contact. Check both wheel constraints and total demand rather than assuming the bias ratio is always achieved. Connect this result to at least one other listed lesson, identifying the exact quantity, units and assumption transferred across their interface.

## Integrate and defend the boundary

Use P47: Explain gear selection at a shared road speed and account for resistance during torque interruption. For each gear compute rpm=v*G*final_drive*60/(2*pi*r), reject rpm outside 1500–7000, and compare valid wheel forces. A shift sets drive force to zero for the declared delay, but rolling and aerodynamic resistance still decelerate the car. At 20 m/s the declared resistance is 180+0.38*400=332 N, giving -0.22897 m/s² for 1450 kg during interruption. Compare the full speed history and redline excess, not just the target time. Connect this result to at least one other listed lesson, identifying the exact quantity, units and assumption transferred across their interface.

## Required integration artifact

Build a bounded acceleration comparison with engine torque-map points, road-speed-to-rpm conversion, available wheel force, tire clipping, differential wheel capacities, reflected inertia and gear interruption. Retain at least one traction-limited and one engine-limited point. During a shift, compute the negative acceleration from road resistance and inspect the speed history. Distinguish a force crossover from a redline event, and a greedy gear choice from a globally optimized schedule. Mark a horizon-limited target time as censored. Close the work/energy ledger at the declared numerical resolution and identify the missing clutch or thermal effects.

## Four-criterion rubric

1. Governing reasoning: equations, units and frame/sign conventions justify a numerical prediction; naming an algorithm alone earns no evidence.
2. Controlled comparison: two isolated sweeps and at least one limiting case distinguish mechanisms and make a falsifiable claim.
3. Diagnose and recover: identify the first failing assumption from actual outputs, restore it and demonstrate deterministic recovery.
4. Integration and scope: show the value passed between stages, an independently checked result, and a limitation that prevents a broader claim.

Retain inputs, selected outputs and your explanation as a cumulative artifact. No learner completion, automatic score, physical qualification or production acceptance is recorded.
