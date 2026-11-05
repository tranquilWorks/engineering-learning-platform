# A-PERFORMANCE integration evidence

Integrate these existing lessons: P09, P10, P11, P12, P21, P22, P23, P38, P39, P40, P41, P42, P43, P61, P62, P63, P64, P65, P67.

Required evidence: Construct track and g-g-v constraints, close a forward/backward lap simulation, and compare setup changes with a designed experiment.

## Derive and predict

Use P09: Use virtual work and spring energy to derive the squared motion-ratio law. With motion ratio defined as spring travel divided by wheel travel, spring displacement is r*z. Energy is k_s*(r*z)²/2, so wheel rate is k_s*r². At r=0.9 and k_s=35000 N/m, wheel rate is 28350 N/m. Using r instead of r² violates energy equivalence even if units still look correct. Explicitly distinguish this convention from the reciprocal convention used in some suspension references. Connect this result to at least one other listed lesson, identifying the exact quantity, units and assumption transferred across their interface.

## Compare connected mechanisms

Use P23: Preserve sector pairing and separate aero, tire and interaction effects in a setup comparison. The four baseline sectors sum to 116 s. Candidate-minus-baseline deltas must be paired by sector and sum to the lap delta. The declared aero, tire and interaction contributions must close that same delta. A shuffled sector pairing can leave a total unchanged while corrupting variability and explanation. Distinguish the 0.20 s decision threshold from uncertainty or a statistical significance claim. Connect this result to at least one other listed lesson, identifying the exact quantity, units and assumption transferred across their interface.

## Diagnose and recover

Use P43: Show that anti geometry changes the path carrying pitch transfer rather than the total transfer itself. Total longitudinal transfer is m*a*h/L. The declared anti-dive fraction is 0.70*tan(angle)*L/h, while anti-squat omits the 0.70 brake-distribution factor. Geometric and spring-supported contributions must sum to total transfer even when a fraction exceeds one and the spring contribution changes sign. At 5 degrees, use tan(5*pi/180), not tan(5). Explain why changing height affects both the total demand and the anti percentage. Connect this result to at least one other listed lesson, identifying the exact quantity, units and assumption transferred across their interface.

## Integrate and defend the boundary

Use P67: Defend the digital twin's complete interface ledger and explain what its uncertainty envelope does and does not mean. Fit stiffness and friction from separate synthetic linear/saturated samples and check the unused tire samples. Trace calibrated forces through individual wheel loads, gear selection, cyclic acceleration/braking and lap time. The 0.8 lateral and 0.6 longitudinal reserve fractions satisfy 0.8²+0.6²=1; neither reserve is independently available in full. Check minimum wheel load, load sum, power, brake and combined-grip bounds on every segment. Execute both friction endpoints to obtain a scenario envelope, and reject the double-downforce fault from the physical load ledger. Connect this result to at least one other listed lesson, identifying the exact quantity, units and assumption transferred across their interface.

## Required integration artifact

Build an auditable discrete-lap report: track closure and curvature refinement, speed-dependent force/power envelope, feasible constant-offset candidates, cyclic forward/backward speed constraints, propulsive energy and brake heat. Check the last-to-first segment explicitly and record an energy budget below the rolling-work floor as infeasible. Explain each reserve fraction and avoid assigning full tire capacity simultaneously to two directions. Compare time and penalized objective separately. Add a factorial setup analysis with main/interaction effect conventions and untouched validation points; identify the structural differences between that synthetic response surface and the executed lap model.

## Four-criterion rubric

1. Governing reasoning: equations, units and frame/sign conventions justify a numerical prediction; naming an algorithm alone earns no evidence.
2. Controlled comparison: two isolated sweeps and at least one limiting case distinguish mechanisms and make a falsifiable claim.
3. Diagnose and recover: identify the first failing assumption from actual outputs, restore it and demonstrate deterministic recovery.
4. Integration and scope: show the value passed between stages, an independently checked result, and a limitation that prevents a broader claim.

Retain inputs, selected outputs and your explanation as a cumulative artifact. No learner completion, automatic score, physical qualification or production acceptance is recorded.
