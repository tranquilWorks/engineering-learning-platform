# Compare Impedance and Ideal Admittance Contact Transients



## Model, derivation, and conventions

`m xddot+b xdot+(k_virtual+k_environment)x=0`

`contact_force=k_environment*x`

`E=0.5m xdot²+0.5(k_virtual+k_environment)x²; Edot=-b xdot²`

The model describes small contact perturbations about a maintained preload. The environment is an ideal bilateral linear spring, meaning signed displacement produces signed incremental force without contact separation. Its selected stiffness is added to virtual stiffness 150 N/m. Effective mass is 2 kg and virtual damping is selected in N s/m. This is deliberately a linear perturbation model; it does not simulate unilateral impact or the absolute preload needed to maintain contact.

The impedance response starts with displacement 0.01 m and zero velocity. Its force follows from the spring deflection while the mass moves under the closed-loop impedance equation. The admittance response represents an ideal inner position servo executing a virtual mass-spring-damper command. It starts at zero displacement with velocity 0.2 m/s, corresponding to an initial virtual momentum impulse. Under these ideal assumptions the two perturbations obey the same second-order equation, but their initial excitations differ. Their curves therefore illustrate response to displacement and momentum, not a universal ranking of controller architectures.

The total stored perturbation energy is one half mass times velocity squared plus one half combined stiffness times displacement squared. Differentiating and substituting the equation gives Edot=-b*v². Positive damping dissipates energy, zero damping conserves it, and negative damping injects it. The experiment computes the actual integrated state and energy, rather than drawing an assigned exponential envelope. Contact force is environment stiffness times actual displacement for each response.

The observation horizon is 0.4 s with 241 samples. The force metric is the greatest absolute contact force across both responses. The energy metric is the largest impedance-response stored energy. The settling metric considers only the impedance response and requires both normalized displacement and normalized velocity to remain inside a two-percent band for the rest of the sampled horizon. Displacement normalization is 0.01 m and velocity normalization is 0.2 m/s. If the condition is never maintained, the displayed value is the observation horizon and diagnostics mark it censored; it is not an estimated eventual settling time.

At environment stiffness 800 N/m, the initial impedance energy is 0.5*(800+150)*0.01²=0.0475 J and its initial contact force is 8 N. The initial admittance energy is 0.5*2*0.2²=0.04 J. These different stored energies help explain why comparing peak force alone cannot establish that one controller is better. For positive damping the subsequent energy should not exceed its own initial energy beyond numerical error.

The fault reverses damping in both equations. Even if displacement oscillates through zero, velocity can retain substantial energy. A force zero crossing is therefore not a recovery or settling event. Extremely large growth at high negative damping remains a software prediction within the finite horizon, not a credible physical actuator response.

## Predict before running

Predict the energy trend when damping is positive and when the same damping is given the wrong sign. Record the expected direction of change and an invariant before reading the computed result. State a condition under which the fault could be hidden, rather than assuming every faulty setting must look worse.

## Baseline workflow

Reset controls and disable the named fault. Use Environment stiffness = 800.0 N/m; Virtual damping = 45.0 N*s/m. Read the response curve, then connect it to the mechanism curve using the governing equations.

Contact perturbations plots Contact force (N) against Time (s). Its series are Impedance, Admittance. Stored contact energy plots Stored energy (J) against Time (s). Its series are Impedance, Admittance.

The default record is Peak contact-force perturbation: 8 N; Impedance settling observation: 0.361667 s; Maximum impedance stored energy: 0.0475 J. These computed values are a worked example for these settings, not acceptance limits for every experiment. Keep parameter values and units beside the result. A near-zero residual has meaning only in relation to the stated model and numerical precision.

## Two one-variable sweeps

1. Increase environment stiffness at fixed damping. Recalculate initial impedance force and energy, then compare oscillation frequency and the observed settling or censoring status.

2. Increase damping at fixed stiffness. Compare energy decay and the two state components. More damping does not imply a universally shorter transient because overdamping can slow displacement recovery.

Return to defaults between sweeps. Hold the other control fixed and record both a changing output and an expected invariant. Explain the physical or numerical path from the selected input to the observed response.

## Intentionally broken case

The fault changes b to negative b in the integrated impedance and virtual-admittance equations. The resulting positive energy derivative drives the observed growth.

Run the same parameter values with the fault enabled. Compare complete curves as well as summary metrics. Identify the actual operation that changed and calculate why it affects the measured result. A changed warning label is not numerical evidence.

## Recovery

Restore positive damping and repeat the same initial excitations. Check energy decay and both state-band conditions before interpreting settling.

Repeat a saved nominal setting and confirm that its values and curves return. Recovery must restore the governing mechanism and its evidence, not merely clear a warning.

## Alternative and limiting cases

At zero damping the ideal system conserves energy and generally does not settle. The maintained-preload linearization and ideal position servo exclude contact loss, actuator limits and servo bandwidth. A censored 0.4 s result is not a measured settling time.

## Independent evidence and MATLAB-style design boundary

The reference advances both state vectors using the exact two-by-two matrix exponential. Production integrates the differential equations with DOP853. Their complete state, energy and contact-force traces are compared.

Five retained cases cover baseline, two single-control sweeps, the named fault and recovery. Expected values come from the independent formulation; actual values come from the executable lesson. Absolute and relative comparison tolerances remain 1e-8. Full-state or geometric checks supplement these three-number signatures, which alone cannot establish correctness. MATLAB has not been executed and no MATLAB equivalence is claimed. Browser and container evidence is recorded separately. Agreement between synthetic implementations does not establish empirical model validity.

## Engineering review checklist

Reconstruct one displayed quantity from the actual state or geometric arrays. Check coordinate ordering, signs and units before comparing numbers. Explain which assumption each check constrains, and identify a defect that another check could miss. Preserve the baseline, one controlled sweep, fault and recovery as a reproducible evidence sequence. State the model boundary before making a broader engineering recommendation.

## Common mistakes

Do not infer correctness from a changing headline alone. At zero damping the ideal system conserves energy and generally does not settle.

Do not change both sliders at once and attribute the result to one cause. Separate a model assumption from a measured property, and a finite-horizon observation from a universal guarantee. Floating-point roundoff is not a physical effect; equally, an attractive plot is not a substitute for the governing calculation.

## Focused check and teach-back

Why does a reported value of 0.4 s not necessarily mean that the response settled at 0.4 s?

Answer rationale: The value can be the observation horizon with a censored status. Settling requires both normalized displacement and velocity to stay within the band; an oscillatory force zero crossing or the last available sample does not establish it.

Use the embedded Course checkpoint to explain your default, sweep, fault and recovery records to a colleague. Include one calculation with units, the causal diagnosis and an explicit untested boundary. This is a self-assessment; no learner score is stored.
