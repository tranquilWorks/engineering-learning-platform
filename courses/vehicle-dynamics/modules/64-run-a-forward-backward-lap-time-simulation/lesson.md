# Solve a periodic lap with a real energy budget

A speed profile must satisfy every segment, including the seam from the final point back to the first. Its energy limit must change its motion, rather than merely cap a displayed number.

## Model and equations

Use 128 midpoint segments on an ellipse with semiaxes 180 m and 90 m. Let $w_i=v_i^2$, $m=1450$ kg, tire force capacity $C=\mu mg$, drag coefficient $c=0.441\,\mathrm{kg/m}$ and rolling force $R=0.012mg$ N. Reserve $\sqrt{0.75}C$ for lateral force and $0.5C$ for longitudinal force, a conservative allocation inside the combined-force circle.

The discrete upstream-speed energy balance is

\[F_i=\frac{m(w_{i+1}-w_i)}{2ds_i}+cw_i+R,\quad -0.5C\le F_i\le\min(0.5C,210000/v_i).\]

Force is in newtons and segment work is $F_i ds_i$ joules. This is a declared spatial discretization, not exact continuous-time optimal control. Cyclic forward and backward passes reduce speeds until they converge. The curvature bound is $m w_i\kappa_i\le\sqrt{0.75}C$.

Positive tractive energy is $E=\sum\max(F_i ds_i,0)$. If it exceeds the selected budget, solve for a common squared-speed scale $\beta\in[0,1]$ using the actual work expression, then recheck forces. The rolling-work floor is $R\sum ds$. Below it, no positive-speed lap is feasible in this model. Negative work heats a 32 kg effective brake mass with specific heat 500 J/(kg·K): $T_b=20+E_{brake}/16000$ °C, with no cooling.

## Baseline workflow

Predict the effect of reducing the energy budget. For a 10 m segment with constant speed 20 m/s, drag plus rolling force is $0.441(20)^2+170.694=347.094$ N, requiring 3470.94 J even without acceleration. Kinetic-energy changes add or subtract work on other segments.

Run grip scale 1.15 and budget 3 MJ. The periodic reachable profile gives about 25.622 s, speeds 20.875–46.993 m/s, actual positive work 3 MJ and an adiabatic brake temperature about 165.50°C. Force excess is zero to numerical tolerance. The forward-only comparison curve has not received the final braking/budget constraints.

## Two one-variable sweeps

1. Keep budget 3 MJ and lower grip from 1.15 to 0.8. Compare curvature speeds, braking entry speeds and lap time. Locate the most restrictive bends on the curvature plot.
2. Restore grip 1.15 and lower budget to 0.8 MJ. Actual speed drops and lap time rises to about 51.979 s. Verify the work sum, not a clipped display, equals the budget.

## Intentionally broken case

The fault omits backward braking passes while retaining the real energy calculation. At baseline it produces a positive braking-force excess of roughly 4760 N. Because excess braking wastes work, the budget-scaled broken lap can actually be slower; do not assume every invalid model looks faster. The residual is derived from segment forces, with no added failure offset.

## Recovery

Restore both cyclic passes with the same grip and energy controls. Recheck the seam, force bounds, energy and recovered lap time.

## Limiting cases and invariants

A budget above unconstrained work leaves the speed profile unchanged. A budget below the rolling-work floor yields `budget_feasible=false`; zero lap time is an explicit finite sentinel, not completion. The zero-budget internal test must report infeasibility. As the grid is refined, lap estimates should converge. Healthy combined utilization stays within one, and both acceleration and braking residuals include the periodic seam.

## Independent evidence

The reference uses simultaneous Jacobi reachability instead of in-place passes, then solves the piecewise-linear $E(\beta)$ relation on its active segments rather than production bisection. Independent scenarios and direct wheel-work, seam, budget and refinement checks assess the actual mechanisms.

## Common mistakes

Do not cap a reported energy total without changing speeds, omit rolling work, infer brake temperature from positive energy, or append a fixed residual to make broken mode fail.

## Teach-back

- Why do both passes repeat around the loop? A downstream limit can propagate across the start/finish seam.
- Why can an invalid profile be slower under an energy cap? Unnecessary speed changes increase dissipated work.
- What does the temperature mean? A one-lap adiabatic bound for an assumed brake mass, not multi-lap thermal qualification.

## Formative checks

A profile uses 3 MJ but the budget is reduced to 0.8 MJ. Is reporting 0.8 MJ while keeping all speeds valid? No: positive segment work must be recomputed after changing motion. Calculate the adiabatic temperature rise from 1.6 MJ of braking work with the declared brake mass and heat capacity. Answer: 100 K, giving 120°C from a 20°C start.

This Python-first native lesson is not a source conversion and does not establish a measured-vehicle result.
