# Account for Delayed Port Work with a Causal Energy Limiter



## Model, derivation, and conventions

`work_k=F_applied,k*v_k*dt; E_next=E-work_k`

`F_requested=-900*x_delayed-0.4*v_delayed`

`positive_work_applied=min(positive_work_requested,E_available)`

This is a sampled interaction-port calculation with prescribed motion. Position is x=0.02*sin(6*pi*t) m and velocity is its analytic derivative, sampled every 0.005 s for 401 force applications. The motion is imposed externally and is not integrated from force, so the example does not establish closed-loop mechanical stability. Positive F*v means the controller supplies mechanical power to that port; negative work means the port returns energy to the bookkeeping reservoir.

The requested spring-damper force uses delayed position and velocity, with stiffness 900 N/m and damping 0.4 N s/m. The selected round-trip delay is converted from milliseconds to seconds. Before delayed history exists, requested force is explicitly zero. After that, the delayed analytic samples define the request. The force-limit slider clips the request symmetrically before energy limiting. This order distinguishes an actuator amplitude bound from a work constraint.

The reservoir begins with 0.01 J. At each sample, compute candidate work from the saturated force, current prescribed velocity and the 0.005 s step. If candidate work is positive and exceeds available energy, scale the force so that the applied positive work spends only the available balance. Negative candidate work is accepted and replenishes the balance. Then update energy using the actual applied force. This is a causal rule: it uses only current work and the retained prior balance, never future samples.

There are 401 force and work samples but 402 energy values because the initial balance precedes the first application. Comparing these arrays without that one-step offset would create a false conservation error. The minimum-energy metric includes the initial and every updated balance. Tiny negative values near floating-point roundoff are numerical residuals; they are not evidence of a substantial energy debt. The saturation fraction measures how often the delayed request exceeds the amplitude bound, before the energy limiter acts.

The third metric is total positive work removed by the limiter, in joules. It accumulates the difference between candidate and applied work, rather than reporting an invented delay margin. Intervention count is retained as a diagnostic but can be sensitive to roundoff at an exactly empty reservoir, so it is not used as a strict numerical comparison signature. The plots show force requests versus applied force and the actual energy balance over time.

Broken mode bypasses the work limiter but retains delay, amplitude clipping and energy accounting. If the delayed force supplies more net work than the initial balance, energy becomes negative. Saturation may reduce that deficit but cannot by itself enforce the cumulative inequality. Conversely, a sufficiently dissipative setting can remain within budget even with the limiter bypassed; the fault is a missing enforcement mechanism, not a command to force every run to fail.

## Predict before running

Predict why force saturation alone cannot guarantee that the accumulated port energy stays nonnegative. Record the expected direction of change and an invariant before reading the computed result. State a condition under which the fault could be hidden, rather than assuming every faulty setting must look worse.

## Baseline workflow

Reset controls and disable the named fault. Use Round-trip delay = 18.0 ms; Force limit = 25.0 N. Read the response curve, then connect it to the mechanism curve using the governing equations.

Port energy balance plots Energy (J) against Time (s). Its series are Tank, Zero. Requested and applied force plots Force (N) against Time (s). Its series are Requested, Applied.

The default record is Minimum observed tank energy: -3.46945e-18 J; Force saturation fraction: 0 1; Active work removed by limiter: 2.18063 J. These computed values are a worked example for these settings, not acceptance limits for every experiment. Keep parameter values and units beside the result. A near-zero residual has meaning only in relation to the stated model and numerical precision.

## Two one-variable sweeps

1. Increase delay at fixed force bound. Compare force phase, negative energy in bypass mode and actual removed work in normal mode. Avoid interpreting a monotonic delay slider as a proven stability threshold.

2. Reduce force bound at fixed delay. Compare saturation fraction and supplied work. Explain why a bounded force can still accumulate too much positive work over repeated samples.

Return to defaults between sweeps. Hold the other control fixed and record both a changing output and an expected invariant. Explain the physical or numerical path from the selected input to the observed response.

## Intentionally broken case

The fault bypasses the causal energy limiter while preserving the delayed request and saturation. The same actual-work update then reveals any reservoir deficit.

Run the same parameter values with the fault enabled. Compare complete curves as well as summary metrics. Identify the actual operation that changed and calculate why it affects the measured result. A changed warning label is not numerical evidence.

## Recovery

Restore work limiting and compare applied force, sample work and every energy update. Verify conservation with the initial balance included.

Repeat a saved nominal setting and confirm that its values and curves return. Recovery must restore the governing mechanism and its evidence, not merely clear a warning.

## Alternative and limiting cases

At a zero-velocity sample the port work is zero regardless of finite force. This is a prescribed-motion, sampled-work demonstration with ideal force application. It does not establish continuous-time passivity, a closed-loop delay margin or stability of a physical haptic system.

## Independent evidence and MATLAB-style design boundary

The reference uses cumulative candidate work and its running maximum to derive the minimal reflection correction that keeps the balance nonnegative. This global mathematical identity independently checks the production causal sample loop.

Five retained cases cover baseline, two single-control sweeps, the named fault and recovery. Expected values come from the independent formulation; actual values come from the executable lesson. Absolute and relative comparison tolerances remain 1e-8. Full-state or geometric checks supplement these three-number signatures, which alone cannot establish correctness. MATLAB has not been executed and no MATLAB equivalence is claimed. Browser and container evidence is recorded separately. Agreement between synthetic implementations does not establish empirical model validity.

## Engineering review checklist

Reconstruct one displayed quantity from the actual state or geometric arrays. Check coordinate ordering, signs and units before comparing numbers. Explain which assumption each check constrains, and identify a defect that another check could miss. Preserve the baseline, one controlled sweep, fault and recovery as a reproducible evidence sequence. State the model boundary before making a broader engineering recommendation.

## Common mistakes

Do not infer correctness from a changing headline alone. At a zero-velocity sample the port work is zero regardless of finite force.

Do not change both sliders at once and attribute the result to one cause. Separate a model assumption from a measured property, and a finite-horizon observation from a universal guarantee. Floating-point roundoff is not a physical effect; equally, an attractive plot is not a substitute for the governing calculation.

## Focused check and teach-back

Why can a force remain within its actuator bound while violating the energy budget?

Answer rationale: An amplitude bound limits each force value, whereas the budget limits accumulated force times velocity times sample duration. Repeated bounded positive work can exceed the initial energy; the causal work limiter must constrain the actual applied work.

Use the embedded Course checkpoint to explain your default, sweep, fault and recovery records to a colleague. Include one calculation with units, the causal diagnosis and an explicit untested boundary. This is a self-assessment; no learner score is stored.
