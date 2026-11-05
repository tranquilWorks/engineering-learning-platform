# A-BRAKES integration evidence

Integrate these existing lessons: P15, P48, P49, P50.

Required evidence: Balance axles, simulate slip control, and close stopping-energy and brake-temperature budgets including fade recovery.

## Derive and predict

Use P15: Close kinetic energy, stopping work and absorbed brake heat as separate quantities. Initial kinetic energy is m*v0²/2, so doubling initial speed quadruples energy. Integrate the actual resisting force over stopping distance and account for road losses before allocating brake heat. Peak temperature depends on the stated heat capacity and absorption fraction. Tire-limited braking can change force and distance while the same initial kinetic energy still has to leave the vehicle. Connect this result to at least one other listed lesson, identifying the exact quantity, units and assumption transferred across their interface.

## Compare connected mechanisms

Use P48: Calculate the requested-deceleration axle loads and explain why a clipped result is only a conditional allocation. Front load is static front weight plus m*a*h/L; rear loses the same amount. Ideal force fraction equals front dynamic load divided by mg if both axles share the same friction coefficient. Clipping front and rear brake requests separately can produce an achieved deceleration below the requested one. The displayed loads were computed from the request, so this one-pass study is not a self-consistent solution using the lower achieved acceleration. Diagnose the broken static-load allocation with axle utilization. Connect this result to at least one other listed lesson, identifying the exact quantity, units and assumption transferred across their interface.

## Diagnose and recover

Use P49: Derive brake torque from slip-rate control and identify the low-speed boundary of the simulation. With slip=1-r*omega/v, differentiate using wheel torque balance J*omega_dot=r*Fx-Tb and vehicle deceleration -Fx/m. The controller chooses torque to drive slip toward its target, subject to the requested-torque ceiling. Here target_slip also locates the synthetic tire-force peak, so sweeping it changes plant and controller together; it is not an independent target-optimization experiment. The wheel-speed projection at zero introduces a reaction not captured by the free wheel equation. Connect this result to at least one other listed lesson, identifying the exact quantity, units and assumption transferred across their interface.

## Integrate and defend the boundary

Use P50: Close each repeated-stop heat increment and derive the cooling recurrence before discussing fade. A 450 kJ stop deposits 0.75*450=337.5 kJ into a 45000 J/K lump, raising it by 7.5 K before cooling. Between stops, excess temperature decays toward ambient with time constant C/h. Sum absorbed heat, stored heat and rejected heat over all six stops. The fade factor follows peak temperature; final cooled temperature can hide that peak. The broken mode reports rejected heat without removing it from storage, so its energy ledger cannot close. Connect this result to at least one other listed lesson, identifying the exact quantity, units and assumption transferred across their interface.

## Required integration artifact

Deliver three explicitly separated results: the requested-deceleration axle allocation, the above-2-m/s ABS slip-control trajectory, and the repeated-stop thermal ledger. Show axle load and force sums, controller torque limits, wheel-lock behavior and absorbed/stored/rejected heat. Explain that the one-pass allocation does not re-solve loads using clipped achieved deceleration, the low-speed floor prevents an exact stopping-distance claim, and the thermal fade factor does not feed back into braking dynamics. Link these limitations to the extra coupled equations and measurements a real validation would require; do not merge the separate studies into an unexecuted integrated claim.

## Four-criterion rubric

1. Governing reasoning: equations, units and frame/sign conventions justify a numerical prediction; naming an algorithm alone earns no evidence.
2. Controlled comparison: two isolated sweeps and at least one limiting case distinguish mechanisms and make a falsifiable claim.
3. Diagnose and recover: identify the first failing assumption from actual outputs, restore it and demonstrate deterministic recovery.
4. Integration and scope: show the value passed between stages, an independently checked result, and a limitation that prevents a broader claim.

Retain inputs, selected outputs and your explanation as a cumulative artifact. No learner completion, automatic score, physical qualification or production acceptance is recorded.
