# Compute Operational Inertia and Dynamically Consistent Torque



## Model, derivation, and conventions

`Lambda=(J M^-1 J^T)^-1; Jbar=M^-1 J^T Lambda`

`N_tau=I-J^T Jbar^T; tau_secondary=N_tau tau_raw`

`xddot=J M^-1(tau_primary+tau_secondary)`

A planar three-revolute-joint arm has link lengths [1,0.8,0.6] m and a two-dimensional endpoint position task. Its fixed pose is [0.4,-1.2/sqrt(c),0.8/sqrt(c)] rad, where c is the geometry slider. The slider does not directly set a matrix condition number; the actual Jacobian condition is computed from that pose. The mass slider scales link masses [1,0.8,0.6] kg and adds 0.03 times the same scale to each joint's rotor inertia in kg m².

Each link mass is concentrated at its midpoint. Cartesian centre-of-mass Jacobians give M as the sum of mass times J_com transpose J_com, plus the positive rotor-inertia diagonal. This construction gives a symmetric positive-definite joint inertia with genuine coupling. The endpoint Jacobian J has two rows and three columns. The task inertia Lambda is the inverse of J M inverse J transpose, expressed in kilograms for this translational task. The third metric is its largest eigenvalue, so the direction with greatest apparent mass determines it.

This is an instantaneous acceleration experiment at zero joint velocity. Consequently the Jdot*qdot term is zero. Gravity is assumed exactly compensated outside the incremental calculation. Desired task acceleration is [0.4,-0.2] m/s². The primary torque is J transpose Lambda times that desired acceleration. Substituting into the zero-velocity plant gives the requested task acceleration. The lesson makes no claim about maintaining that result through a moving trajectory without updating the model.

A raw secondary torque [0.5,-0.3,0.7] N m is projected with N_tau=I-J transpose Jbar transpose. This torque projector is related to the dynamically consistent inverse, not simply the Euclidean velocity null projector. Its decisive property is J M inverse N_tau=0. The secondary torque may have a nonzero Euclidean task projection yet produce zero task acceleration after the physical inertia acts. Conversely, a torque satisfying J*tau=0 need not satisfy J M inverse tau=0.

The response plot varies the fraction of secondary torque and shows actual task acceleration; compare it with the specified desired acceleration. The mechanism plot varies a unit task direction and computes directional inertia. The first two metrics measure total acceleration error and secondary acceleration leakage; both have units m/s², not velocity or force. A small numerical leakage checks the stated local algebra. It does not demonstrate posture convergence, collision avoidance, joint limits or robustness to a wrong inertia model.

Broken mode substitutes I-J pseudoinverse J as the torque projector. That familiar matrix correctly suppresses Euclidean task velocity when used on a joint-velocity command, but torque first passes through M inverse. The resulting acceleration leakage is calculated from the actual torque and physical inertia, which makes the distinction observable.

## Predict before running

Predict whether a torque in the Euclidean null space of J necessarily produces zero task acceleration. Record the expected direction of change and an invariant before reading the computed result. State a condition under which the fault could be hidden, rather than assuming every faulty setting must look worse.

## Baseline workflow

Reset controls and disable the named fault. Use Link mass scale = 2.0 kg; Pose straightness parameter = 5.0 1. Read the response curve, then connect it to the mechanism curve using the governing equations.

Resulting task acceleration plots Acceleration (m/s²) against Torque fraction (1). Its series are Actual x, Actual y. Directional task inertia plots Inertia (kg) against Task direction (rad). Its series are Inertia.

The default record is Actual task acceleration error: 5.55112e-16 m/s^2; Secondary acceleration leakage: 3.65494e-16 m/s^2; Largest task inertia eigenvalue: 4.97711 kg. These computed values are a worked example for these settings, not acceptance limits for every experiment. Keep parameter values and units beside the result. A near-zero residual has meaning only in relation to the stated model and numerical precision.

## Two one-variable sweeps

1. Increase link mass scale at fixed geometry. The operational inertia scales with mass. The same raw secondary torque has less acceleration effect as mass grows, while correct primary compensation still requests the selected task acceleration.

2. Increase the straightness parameter at fixed mass. Compare actual conditioning, directional inertia and faulty secondary leakage. Explain the result through J and M rather than treating the slider value as measured conditioning.

Return to defaults between sweeps. Hold the other control fixed and record both a changing output and an expected invariant. Explain the physical or numerical path from the selected input to the observed response.

## Intentionally broken case

The fault projects secondary torque with a Euclidean velocity-null projector. It preserves the raw torque, physical inertia and primary task command, then computes the resulting acceleration.

Run the same parameter values with the fault enabled. Compare complete curves as well as summary metrics. Identify the actual operation that changed and calculate why it affects the measured result. A changed warning label is not numerical evidence.

## Recovery

Restore the dynamically consistent torque projector and compare acceleration with and without the secondary torque. Check J M inverse tau_secondary directly.

Repeat a saved nominal setting and confirm that its values and curves return. Recovery must restore the governing mechanism and its evidence, not merely clear a warning.

## Alternative and limiting cases

At zero secondary fraction both modes reduce to the same primary task command. This is a local zero-velocity calculation with exact gravity compensation. A moving task requires Jdot*qdot, updated geometry and an actual trajectory controller.

## Independent evidence and MATLAB-style design boundary

The reference differentiates link-centre and endpoint coordinates with complex steps, then solves a constrained block system for operational inertia and null acceleration. Its faulty comparison uses a cross-product null basis instead of the production pseudoinverse projector.

Five retained cases cover baseline, two single-control sweeps, the named fault and recovery. Expected values come from the independent formulation; actual values come from the executable lesson. Absolute and relative comparison tolerances remain 1e-8. Full-state or geometric checks supplement these three-number signatures, which alone cannot establish correctness. MATLAB has not been executed and no MATLAB equivalence is claimed. Browser and container evidence is recorded separately. Agreement between synthetic implementations does not establish empirical model validity.

## Engineering review checklist

Reconstruct one displayed quantity from the actual state or geometric arrays. Check coordinate ordering, signs and units before comparing numbers. Explain which assumption each check constrains, and identify a defect that another check could miss. Preserve the baseline, one controlled sweep, fault and recovery as a reproducible evidence sequence. State the model boundary before making a broader engineering recommendation.

## Common mistakes

Do not infer correctness from a changing headline alone. At zero secondary fraction both modes reduce to the same primary task command.

Do not change both sliders at once and attribute the result to one cause. Separate a model assumption from a measured property, and a finite-horizon observation from a universal guarantee. Floating-point roundoff is not a physical effect; equally, an attractive plot is not a substitute for the governing calculation.

## Focused check and teach-back

Why is J times secondary torque equal to zero the wrong condition for preserving task acceleration?

Answer rationale: Torque is converted to joint acceleration through M inverse. At zero velocity the task effect is J M inverse tau_secondary, so a torque projector must cancel that quantity. The Euclidean null condition applies directly to joint velocity, not arbitrary torque.

Use the embedded Course checkpoint to explain your default, sweep, fault and recovery records to a colleague. Include one calculation with units, the causal diagnosis and an explicit untested boundary. This is a self-assessment; no learner score is stored.
