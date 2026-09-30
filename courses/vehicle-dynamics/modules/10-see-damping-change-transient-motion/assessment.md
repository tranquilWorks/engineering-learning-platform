## P10 evidence task

At k = 35000 N/m compare the default c = 3200 with accessible slider settings just below and above the calculated critical value 6480.74 N·s/m, and with 8000 N·s/m. The stepped slider cannot select that exact critical value: classify the selected settings from ζ and describe the exact repeated-pole case algebraically. Explain the curve shapes. Activate negative damping at each selected setting and use the sign of dE/dt to justify instability. State what the displayed four-time-constant metric does and does not establish.

Record one prediction before running, then retain the actual selected input values, the relevant metric units and two observations from the plotted relationship. Use the nominal sweeps to isolate one variable at a time. Compare the fault and nominal responses at fixed inputs before resetting to the worked baseline. If the two curves coincide, decide whether the lesson's benign limit explains that outcome; a coincident curve is not automatically a successful fault test.

### Reasoning rubric

The three nominal cases are underdamped, critical and overdamped. Positive c dissipates perturbation energy; negative c injects it whenever velocity is nonzero. Four slow-pole time constants describes a decay scale, not a measured tolerance-based settling time, and is unavailable for the unstable model. Full credit requires interpreting the finite time window.

A complete explanation links a quantitative check to its governing relation, distinguishes the requested or formal model result from its stated physical validity, and explains the recovery causally. A partially supported answer reports the expected trend but omits units, an input convention or the fault mechanism. An unsupported answer uses the status badge or curve shape alone as proof. Revise the explanation until a reader could reproduce the comparison from your recorded inputs.

### Check your reasoning

At c = 3200 N·s/m and k = 35000 N/m, ω_n ≈ 10.8012 rad/s, f_n ≈ 1.71907 Hz and ζ ≈ 0.493771. The envelope decay rate is c/(2m) = 5.33333 1/s, so four envelope time constants is 0.75 s. The critical damping value at this stiffness is about 6480.74 N·s/m. Moving above that value eliminates oscillation but eventually slows the dominant pole.

Do not extrapolate 4/(ζω_n) as a universal settling formula through the overdamped regime. Do not confuse a bounded plotting window with stable dynamics. A decaying oscillation and a slow monotonic tail can share the same final equilibrium.

Before continuing, state one prediction this model cannot support. Use the specific limitations in the lesson, rather than a general statement that every simulation has limits. This checkpoint is a self-check: **no learner score is stored**, and completing it does not establish measured vehicle performance or learner acceptance.
