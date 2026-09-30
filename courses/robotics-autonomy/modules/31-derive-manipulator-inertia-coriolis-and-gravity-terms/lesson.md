# Construct Manipulator Inertia, Coriolis and Gravity Terms



## Model, derivation, and conventions

`M(q) qddot+C(q,qdot) qdot+g(q)=tau`

`kinetic_energy=0.5 qdot^T M(q) qdot`

`S=Mdot-2C; S+S^T=0`

Two ideal point masses define this planar arm. The first mass is 1 kg at the end of a 0.7 m proximal link. The second mass is 0.8 kg plus the selected payload at the end of a 0.5 m distal link. The links themselves are massless. Joint angles are relative revolute angles, measured from the horizontal through cumulative orientation. The shoulder is 0.4 rad, the selected elbow angle is converted from degrees, and the declared instantaneous joint rate is [0.6,-0.35] rad/s. Gravity is 9.81 m/s² downward.

Writing a=m1*l1²+m2*(l1²+l2²), b=m2*l1*l2 and d=m2*l2² gives M=[[a+2b cos(q2),d+b cos(q2)],[d+b cos(q2),d]]. This matrix comes from Cartesian kinetic energy of the two masses. Its symmetry and positive eigenvalues ensure positive kinetic energy for every nonzero joint velocity at the selected configuration. The two positive physical masses and nonzero link lengths keep the matrix positive definite throughout the displayed elbow sweep, including a straight arm; a kinematic position singularity does not imply a singular joint inertia.

Let h=b sin(q2). The velocity matrix used here is C=[[-h*v2,-h*(v1+v2)],[h*v1,0]]. Individual Coriolis matrices depend on convention, but C times velocity must represent the correct generalized velocity forces. For this Christoffel convention, Mdot-2C is skew symmetric. The displayed defect is the Frobenius norm ||S+Sᵀ||, with S=Mdot−2C, computed from an analytic mass derivative along the declared rate. This unnormalised defect is twice the conventional symmetric-part norm; the identity is zero under either normalization. Units are kg m²/s, equivalent to rotational damping units, and the defect is not itself a torque or energy.

Potential energy is 9.81*((m1+m2)*l1*sin(q1)+m2*l2*sin(q1+q2)). Differentiating it gives the gravity vector. The shoulder component is the third metric and can change sign with geometry; it is not an absolute maximum across all poses. The plots independently sweep elbow angle from -pi to pi, showing inertia eigenvalues and gravity torque while the metrics refer to the selected pose. Read that distinction before comparing a plotted extreme with a headline value.

At elbow zero, h vanishes and every displayed Coriolis entry is zero even though the robot can be moving. Omitting one entry is then invisible to this local skew test. Away from alignment, dropping C12 leaves the same positive inertia matrix but breaks the kinetic-energy cancellation. This is why one positive-definiteness check cannot certify the entire dynamics model.

## Predict before running

Predict whether positive inertia alone can reveal a missing Coriolis coupling. Record the expected direction of change and an invariant before reading the computed result. State a condition under which the fault could be hidden, rather than assuming every faulty setting must look worse.

## Baseline workflow

Reset controls and disable the named fault. Use Payload mass = 1.0 kg; Elbow angle = 55.0 deg. Read the response curve, then connect it to the mechanism curve using the governing equations.

Joint inertia eigenvalues plots Inertia (kg·m²) against Elbow angle (rad). Its series are Min eig, Max eig. Joint gravity torques plots Torque (N·m) against Elbow angle (rad). Its series are Joint 1, Joint 2.

The default record is Minimum inertia eigenvalue: 0.172497 kg*m^2; Symmetric skew-identity defect: 0 kg*m^2/s; Shoulder gravity torque: 19.5578 N*m. These computed values are a worked example for these settings, not acceptance limits for every experiment. Keep parameter values and units beside the result. A near-zero residual has meaning only in relation to the stated model and numerical precision.

## Two one-variable sweeps

1. Increase payload at fixed elbow angle. Compare both inertia eigenvalues and the shoulder gravity component. The normal skew defect stays near roundoff even though the underlying mass derivative and Coriolis entries grow.

2. Sweep elbow angle through zero and a bent pose at fixed payload. Inspect the gravity sign and actual inertia eigenvalues. Enable the fault at both poses to identify the zero-sine blind spot.

Return to defaults between sweeps. Hold the other control fixed and record both a changing output and an expected invariant. Explain the physical or numerical path from the selected input to the observed response.

## Intentionally broken case

The fault removes C12 while preserving the physical mass and gravity calculations. The symmetric part of Mdot-2C therefore measures an executed missing coupling.

Run the same parameter values with the fault enabled. Compare complete curves as well as summary metrics. Identify the actual operation that changed and calculate why it affects the measured result. A changed warning label is not numerical evidence.

## Recovery

Restore C12 and repeat the bent-pose comparison. Check positive eigenvalues, the skew identity and the gravity vector separately.

Repeat a saved nominal setting and confirm that its values and curves return. Recovery must restore the governing mechanism and its evidence, not merely clear a warning.

## Alternative and limiting cases

At elbow zero or pi the omitted sine coupling vanishes, so this fault can be locally hidden. The point-mass model excludes distributed link inertia, friction, elasticity and motor dynamics; it is an instantaneous identity check, not a trajectory experiment.

## Independent evidence and MATLAB-style design boundary

The reference builds mass from Cartesian point-mass Jacobians, obtains mass and potential derivatives by complex steps, and constructs C from Christoffel symbols. It checks M, C, Mdot and gravity separately.

Five retained cases cover baseline, two single-control sweeps, the named fault and recovery. Expected values come from the independent formulation; actual values come from the executable lesson. Absolute and relative comparison tolerances remain 1e-8. Full-state or geometric checks supplement these three-number signatures, which alone cannot establish correctness. MATLAB has not been executed and no MATLAB equivalence is claimed. Browser and container evidence is recorded separately. Agreement between synthetic implementations does not establish empirical model validity.

## Engineering review checklist

Reconstruct one displayed quantity from the actual state or geometric arrays. Check coordinate ordering, signs and units before comparing numbers. Explain which assumption each check constrains, and identify a defect that another check could miss. Preserve the baseline, one controlled sweep, fault and recovery as a reproducible evidence sequence. State the model boundary before making a broader engineering recommendation.

## Common mistakes

Do not infer correctness from a changing headline alone. At elbow zero or pi the omitted sine coupling vanishes, so this fault can be locally hidden.

Do not change both sliders at once and attribute the result to one cause. Separate a model assumption from a measured property, and a finite-horizon observation from a universal guarantee. Floating-point roundoff is not a physical effect; equally, an attractive plot is not a substitute for the governing calculation.

## Focused check and teach-back

Why does a positive minimum inertia eigenvalue not prove that the velocity forces are correct?

Answer rationale: Positive inertia certifies the kinetic-energy quadratic form. A missing C entry leaves that form unchanged while breaking the skew identity at a bent moving configuration. The tests constrain different parts of the dynamics.

Use the embedded Course checkpoint to explain your default, sweep, fault and recovery records to a colleague. Include one calculation with units, the causal diagnosis and an explicit untested boundary. This is a self-assessment; no learner score is stored.
