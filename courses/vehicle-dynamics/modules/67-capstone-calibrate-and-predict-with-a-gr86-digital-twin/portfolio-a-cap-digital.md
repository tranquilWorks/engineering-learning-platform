# A-CAP-DIGITAL integration evidence

Integrate these existing lessons: P05, P06, P13, P14, P15, P16, P21, P22, P23, P24, P26, P27, P28, P29, P30, P31, P32, P33, P37, P38, P44, P45, P46, P47, P48, P49, P50, P51, P52, P60, P61, P62, P63, P64, P65, P67.

Required evidence: Trace requirements from calibrated subsystems through coupled lap prediction, uncertainty, setup comparison, a cumulative failure, and exact recovery in P67.

## Derive and predict

Use P05: Explain the sign and local slope of longitudinal tire force and distinguish stiffness from peak force. A signed slip input must produce an odd force response in this symmetric model: reversing slip reverses force. Near zero, differentiate the declared law to obtain stiffness; at larger slip compare force with mu*Fz. Increasing load can raise capacity without changing the interpretation of slip as a dimensionless ratio. Use a negative-slip prediction to expose a sign or percent-versus-fraction error that a positive baseline could hide. Connect this result to at least one other listed lesson, identifying the exact quantity, units and assumption transferred across their interface.

## Compare connected mechanisms

Use P28: Show why slip-angle and camber excitation must be distinguishable to estimate two stiffnesses. The design matrix has columns alpha and gamma, both in radians, and force is C_alpha*alpha+C_gamma*gamma. If gamma is proportional to alpha, the columns lose rank and only a combination of stiffnesses is identifiable. One degree is pi/180 rad, so a 70000 N/rad coefficient predicts about 1221.73 N per degree in the uncapped linear region. Check held-out predictions and units for both coefficients. Connect this result to at least one other listed lesson, identifying the exact quantity, units and assumption transferred across their interface.

## Diagnose and recover

Use P48: Calculate the requested-deceleration axle loads and explain why a clipped result is only a conditional allocation. Front load is static front weight plus m*a*h/L; rear loses the same amount. Ideal force fraction equals front dynamic load divided by mg if both axles share the same friction coefficient. Clipping front and rear brake requests separately can produce an achieved deceleration below the requested one. The displayed loads were computed from the request, so this one-pass study is not a self-consistent solution using the lower achieved acceleration. Diagnose the broken static-load allocation with axle utilization. Connect this result to at least one other listed lesson, identifying the exact quantity, units and assumption transferred across their interface.

## Integrate and defend the boundary

Use P67: Defend the digital twin's complete interface ledger and explain what its uncertainty envelope does and does not mean. Fit stiffness and friction from separate synthetic linear/saturated samples and check the unused tire samples. Trace calibrated forces through individual wheel loads, gear selection, cyclic acceleration/braking and lap time. The 0.8 lateral and 0.6 longitudinal reserve fractions satisfy 0.8²+0.6²=1; neither reserve is independently available in full. Check minimum wheel load, load sum, power, brake and combined-grip bounds on every segment. Execute both friction endpoints to obtain a scenario envelope, and reject the double-downforce fault from the physical load ledger. Connect this result to at least one other listed lesson, identifying the exact quantity, units and assumption transferred across their interface.

## Required integration artifact

Produce a P67 interface and requirement dossier from tire calibration through gear maps, individual normal loads, tire capacity, periodic speed propagation, offset selection, energy and brake heat. Recompute wheel-load sums and combined-force utilization on every segment, including the closing segment. Explain the 0.8/0.6 capacity reserve, minimum-load domain and nine-candidate path search. Compare nominal and both friction-endpoint runs as a bounded scenario envelope, not confidence coverage. Trace the double-downforce fault to physical ledger failure even if lap time improves, then prove exact deterministic recovery. Explicitly separate adiabatic temperature from fade feedback and synthetic parameter calibration from real GR86 validation.

## Four-criterion rubric

1. Governing reasoning: equations, units and frame/sign conventions justify a numerical prediction; naming an algorithm alone earns no evidence.
2. Controlled comparison: two isolated sweeps and at least one limiting case distinguish mechanisms and make a falsifiable claim.
3. Diagnose and recover: identify the first failing assumption from actual outputs, restore it and demonstrate deterministic recovery.
4. Integration and scope: show the value passed between stages, an independently checked result, and a limitation that prevents a broader claim.

Retain inputs, selected outputs and your explanation as a cumulative artifact. No learner completion, automatic score, physical qualification or production acceptance is recorded.
