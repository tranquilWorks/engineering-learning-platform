# Observe a Second-Order Suspension Transient

Does more damping always shorten the response, and what changes when damping becomes negative?

## Physical model

The plotted displacement is a real second-order step response. A 300 kg mass starts at x = 0 and velocity v = 0, while its equilibrium steps to x_eq = 0.01 m. It obeys m ẍ + c ẋ + k(x − x_eq) = 0. Natural angular frequency is ω_n = √(k/m); damping ratio is ζ = c/(2√(km)).

For 0 < ζ < 1, the response oscillates with a decaying envelope. At ζ = 1 it has a repeated real pole. For ζ > 1 it has two negative real poles and a slow non-oscillatory tail. The implementation evaluates the proper analytic form for each regime; an independent matrix exponential checks the full displacement, velocity and acceleration arrays.

Define perturbation energy E = ½m v² + ½k(x − x_eq)². Differentiating and using the ODE gives dE/dt = −c v². This identity directly distinguishes dissipation from energy injection.

The reported four slow-pole time constants equals 4 divided by the slowest positive decay rate. It is a time-scale estimate, not a universal measured settling time. For negative damping no decay time exists and the metric is **Unavailable**.

\[
m\ddot x+c\dot x+k(x-x_{\mathrm{eq}})=0,\qquad \frac{dE}{dt}=-c\dot x^2.
\]

## Worked baseline

At c = 3200 N·s/m and k = 35000 N/m, ω_n ≈ 10.8012 rad/s, f_n ≈ 1.71907 Hz and ζ ≈ 0.493771. The envelope decay rate is c/(2m) = 5.33333 1/s, so four envelope time constants is 0.75 s. The critical damping value at this stiffness is about 6480.74 N·s/m. Moving above that value eliminates oscillation but eventually slows the dominant pole.

## Predict and sweep

Before moving a control, write a sign and a trend prediction with units. The two sweep panels always show the **nominal** relationship with the other selected input fixed, even while the fault toggle is active. The response panel follows the selected mode. The comparison panel shows both modes at identical inputs; it is not a time sequence of failure and repair.

1. Keep k = 35000 N/m and vary c from 400 to 8000 N·s/m. Predict decreasing overshoot through the underdamped regime, critical behavior near 6480.74, and an overdamped tail beyond it. The primary sweep displays ζ; use the actual response to judge transient shape.
2. Keep c = 3200 N·s/m and vary k from 15000 to 70000 N/m. Predict increasing natural frequency and decreasing ζ. The secondary sweep shows f_n in Hz, so it must not be read as a damping-ratio curve. Compare response times only after checking the displayed time axis.

## Named broken behavior

The fault reverses c, making the damping force inject energy. The energy identity changes to dE/dt ≥ 0 and the equilibrium becomes unstable. The nominal and faulty curves use the same selected inputs and identical time samples. The finite display window is capped at eight seconds and at three growth time constants of the negative-damping system. This bounds the plotted excursion for readability; it does not imply the unstable system eventually settles. Turning the toggle off restores positive damping.

## Exact recovery

Disable the fault without moving either input. Check that the selected response returns to the nominal member of the same-input comparison and explain which governing relation has been restored. Only then use **Reset parameters** to reproduce the worked baseline. Resetting inputs and repairing the model are separate actions; changing both at once prevents a causal comparison.

## Limits and limiting cases

The model represents an equilibrium step of a linear mass-spring-damper, not a full quarter-car road-input model with a separate unsprung mass. The shown time window can end before nominal settling, especially in an overdamped case. A repeated-pole discriminant within 1e−12 s⁻² is treated as critical to avoid a spurious tiny frequency from floating-point roundoff. No percentage settling tolerance is measured. Internal unavailable sentinels for unstable overshoot/time must not be interpreted as physical values.

## Common mistakes

Do not extrapolate 4/(ζω_n) as a universal settling formula through the overdamped regime. Do not confuse a bounded plotting window with stable dynamics. A decaying oscillation and a slow monotonic tail can share the same final equilibrium.

## Formative checks

At k = 35000 N/m compare the default c = 3200 with accessible slider settings just below and above the calculated critical value 6480.74 N·s/m, and with 8000 N·s/m. The stepped slider cannot select that exact critical value: classify the selected settings from ζ and describe the exact repeated-pole case algebraically. Explain the curve shapes. Activate negative damping at each selected setting and use the sign of dE/dt to justify instability. State what the displayed four-time-constant metric does and does not establish.

Check your reasoning: The three nominal cases are underdamped, critical and overdamped. Positive c dissipates perturbation energy; negative c injects it whenever velocity is nonzero. Four slow-pole time constants describes a decay scale, not a measured tolerance-based settling time, and is unavailable for the unstable model. Full credit requires interpreting the finite time window.

## Teach-back checklist

Explain the declared input convention and governing equation before describing the curve. Reproduce the worked calculation with units, account for both one-variable trends, and identify a discriminating fault test. Finish by naming the specific limiting case above and the physical effects omitted by this model. The embedded Course checkpoint asks for evidence and reasoning; no learner score is stored.

This is deterministic synthetic teaching evidence, **not measured-vehicle** validation, a MATLAB-runtime comparison, or representative-learner acceptance. The original conversion ledger remains historical. This revision verifies the declared native model and its revised fault independently; it does not claim unchanged full-source equivalence.
