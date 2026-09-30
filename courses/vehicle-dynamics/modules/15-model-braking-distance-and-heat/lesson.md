# Close the Braking Work and Heat Budgets

A stopping-distance calculation and a heat calculation answer different questions. The first describes how motion changes under force. The second accounts for the energy removed from that motion. A model can draw a plausible speed curve and still allocate too much heat. In this lesson, use mechanical and thermal balances as separate checks rather than assuming that one correct result validates everything else.

## Physical model: constant-force stopping

The vehicle is a 1320 kg translating mass on a level road. Initial speed V is positive and braking force opposes motion. The control specifies a requested force magnitude; the applied magnitude is capped at μmg, with μ = 1.05 and g = 9.81 m/s². The resulting capacity is 13596.66 N. Deceleration magnitude a = F/m is positive, while the velocity derivative is negative.

\[
v(t)=V-at,\qquad x(t)=Vt-\frac12at^2,
\qquad t_s=\frac{V}{a},\qquad d=\frac{V^2}{2a}.
\]

The displayed trajectory runs only from brake application to the stop. It does not continue constant braking through zero speed into reverse motion. The area under the speed-time curve is stopping distance, and its constant negative slope is −a. Distance, time and speed therefore have different units and are displayed separately rather than joined on a generic response axis.

Mechanical work must close the initial kinetic-energy budget:

\[
W=Fd=E_0=\frac12mV^2,\qquad P_{\mathrm{brake}}(t)=Fv(t).
\]

Stronger braking changes the rate of energy removal, not the initial energy at fixed V. Instantaneous braking power starts at FV and falls to zero with speed. The full retained response includes distance, remaining kinetic energy, work and power as well as the plotted speed curve.

## Heat partition and normal loads

The nominal heat model assigns 85% of stopping work to a combined rotor thermal mass of 28 kg with specific heat 460 J/(kg·K). The remaining 15% is a declared aggregate other-heat category. This partition is assumed, not measured. Rotor temperature rise is

\[
\Delta T=\frac{0.85W}{28\times460}.
\]

A temperature rise has the same numerical magnitude in kelvin and degrees Celsius. It is not an absolute rotor temperature, a surface hot-spot prediction or a cooling history. At intermediate times the same heat fractions apply to accumulated stopping work.

The model also checks longitudinal load transfer. Static front load is 0.53mg, CG height is 0.50 m and wheelbase is 2.57 m. Braking shifts ΔF_z = Fh/L from rear to front. Front and rear normal loads must sum to mg, and the added front reaction must provide the declared pitch moment. A positive total-load sum alone does not prove either axle is nonnegative. Nor does this model allocate braking force between axles; it cannot certify an individual-tire friction budget or brake-bias setting.

## Worked baseline

At 30 m/s and a 10000 N request, the request is below capacity. Deceleration is approximately 7.57576 m/s², stopping time 3.96 s and distance 59.4 m. Initial kinetic energy and total stopping work are both 594000 J. Rotor heat is 504900 J, other heat 89100 J, and rotor temperature rise about 39.20031 °C. Front and rear normal loads are approximately 8808.60 N and 4140.60 N.

Raise the request to 18000 N at the same initial speed. Applied force is capped at 13596.66 N, so the stop becomes about 2.91248 s and 43.68720 m. The initial energy, nominal heat split and final temperature rise remain the same. Calculate the larger initial braking power from FV, then explain why a faster energy-transfer rate can coexist with unchanged total heat.

## Predict and sweep

1. Hold the force request at 10000 N and compare initial speeds 10, 20 and 40 m/s. The primary sweep shows stopping distance in metres. Predict quadratic distance and temperature-rise growth but linear stopping-time growth. Doubling speed multiplies initial energy by four; it does not merely double the heat burden.
2. Hold initial speed at 30 m/s and vary force request from 1000 to 18000 N. The secondary sweep shows distance decreasing until the cap produces a plateau. Accessible requests 13500 and 14000 N bracket the 13596.66 N threshold. Check applied force rather than treating an above-cap request as additional deceleration.

Both sweep panels retain the nominal model. The main speed curve follows the selected mode, while the comparison panel deliberately plots rotor temperature rise versus the same stopping time. Read its °C axis separately from the main panel’s m/s axis.

## Named broken behavior and exact recovery

The fault assigns 100% of stopping work to the rotors while keeping the other 15% heat category. It therefore double counts a 15% portion of the available energy. It does not bypass the tire cap or alter the stopping trajectory. At the default input, allocated heat exceeds initial energy by 89100 J and rotor rise becomes about 46.11801 °C. The displayed heat-budget residual divided by initial energy is 0.15.

Toggle the fault without moving either control. Explain why the speed curves can agree while the temperature comparison and heat budget disagree. Disable the fault at the same inputs, verify restoration of the 85/15 split, and reset only afterward. This separates a model repair from a parameter change.

## Limits and limiting cases

Cooling, drag, road grade, wheel rotational energy, fade, ABS transients, brake bias and measured thermal behavior are omitted. The model supports reasoning about a declared constant-force stop and energy partition; it is not a safe stopping-distance guarantee or a real brake-system qualification.

## Common mistakes

A larger force request above capacity does not produce additional deceleration. Temperature rise is not absolute temperature. An unchanged speed curve cannot certify the heat allocation, because this fault acts only on the thermal budget.

## Formative checks

Why does a stronger stop at fixed initial speed have the same final nominal heat? Check your reasoning: the kinetic-energy difference is fixed, while force changes its removal rate and stopping distance. Verify that the fault instead allocates 115% of that energy.

## Teach-back checklist

Use the speed-curve slope and area, close work and heat separately, and check axle-load sums and signs. Distinguish a restored heat partition from a parameter reset. This is synthetic teaching evidence, not measured-vehicle validation.
