# Solve a Local Six-Degree-of-Freedom Landmark Pose



## Model, derivation, and conventions

`pixel_i=project(R*landmark_i+t); R in SO(3), t in metres`

`delta=argmin ||J*delta+pixel_residual||²`

`R_next=exp([delta_rotation]x)*R; t_next=t+delta_translation`

Forty available three-dimensional landmarks lie on an ellipsoid with unequal axis scales. Their coordinates are known in an object frame, and the visible-count control chooses points distributed across that set. Even a four-point selection spans the object rather than taking four neighbouring points from one small region. The chosen points are noncoplanar in this fixture. This is a synthetic local perspective-n-point problem with full rotation and translation, not an assigned position-error law based on landmark count.

The true object-to-camera rotation has rotation vector [0.18,-0.1,0.25] rad, and its translation is [0.15,-0.1,3.2] m. The camera has focal length 800 px, principal point [320,240] px and square pixels. Actual projected points receive deterministic horizontal and vertical perturbations scaled by the selected noise amplitude. The amplitude is a controlled pixel scale, not a Gaussian standard deviation estimated from repeated trials. Visibility count and noise remain the same between the normal and faulty comparison.

The solver starts at identity rotation and translation [0,0,3] m, regardless of the chosen noise, count or mode. This initializer is near the declared solution and deliberately chooses a local positive-depth branch. It is not computed from the true pose. Four noncoplanar points can support local estimation here, but that does not establish global uniqueness, resolve all PnP ambiguities or guarantee recovery from an arbitrary camera placement. Every candidate accepted by the line search must keep all selected points more than 0.2 m in front of the camera.

At each iteration the model transforms the actual landmarks, computes predicted pixels and stacks their residuals. The analytic projection Jacobian has entries proportional to f/Z and -f*X/Z² or -f*Y/Z². A small left rotation perturbation changes a rotated object point by its cross-product matrix, while translation contributes an identity block. Combining these gives the pixel Jacobian for all six pose increments. Least squares computes an increment. Backtracking accepts a step when positive depth is maintained and the pixel objective does not increase beyond a 1e-13 numerical allowance. For increments below 1e-7, the solver permits a full local refinement step because a rounded cost comparison can otherwise stall further accuracy; positive depth is still required. Thus exact monotonicity at floating-point scale is not a claimed invariant.

Rotation updates use the exponential map, so the estimate remains an orthogonal matrix with determinant one instead of allowing nine unrelated matrix entries to drift. Translation updates are expressed in camera-frame metres. The solver records actual objective, gradient or increment information and its termination condition. A tiny increment, a stalled search and the maximum iteration budget describe different numerical outcomes. A stable residual at a budget limit must not be relabeled as guaranteed convergence simply to make a teaching example appear successful.

The faulty fit uses focal length 650 px while the observations were generated with 800 px. Pose can compensate partially for that mismatch by changing depth and orientation, so a tolerable pixel residual may coexist with a biased metric pose. Increasing landmark count adds constraints but cannot make the wrong focal calibration correct. In normal mode, zero observation noise offers a useful reconstruction limit; under the calibration fault, zero added noise does not remove model error. That contrast separates data perturbation from an incorrect estimator assumption.

Translation error is the Euclidean difference from the synthetic truth in metres. Rotation error is the geodesic angle of the relative rotation, evaluated with an atan2 formulation that stays numerically meaningful near zero. Reprojection RMS is computed from actual residual vectors in pixels. These are distinct dimensions and should not be summed into an undimensioned pose score. The complete rotation, translation, depths, predicted pixels, Jacobian rank and solver history remain available for verification. Full column rank is a local identifiability check; it does not itself establish conditioning, robustness or global uniqueness.

A hand check at zero rotation places an object point [0.1,0,0] m at camera translation [0,0,3] m. Its horizontal offset is 800*0.1/3, about 26.67 px. A solver using 650 px can mimic that one horizontal offset by reducing depth, illustrating why one residual cannot identify both calibration and pose. Multiple noncoplanar points constrain the tradeoff more strongly, but a wrong calibrated model still changes the optimum.

## Predict before running

Predict whether more visible landmarks can repair a focal-calibration error, and distinguish residual fit from actual pose accuracy. Record the expected direction of change and an invariant before reading the computed result. State a condition under which the fault could be hidden, rather than assuming every faulty setting must look worse.

## Baseline workflow

Reset controls and disable the named fault. Use Deterministic pixel-noise amplitude = 1.2 px; Visible landmarks = 12.0 count. Read the response curve, then connect it to the mechanism curve using the governing equations.

Observed and fitted pixels plots Image y (px) against Image x (px). Its series are Observed, Fitted. Pose-fit objective plots Half SSE (px²) against Iteration (count). Its series are Objective.

The default record is Translation error: 0.00154307 m; Rotation error: 0.394672 deg; Landmark reprojection RMS: 0.983971 px. These computed values are a worked example for these settings, not acceptance limits for every experiment. Keep parameter values and units beside the result. A near-zero residual has meaning only in relation to the stated model and numerical precision.

## Two one-variable sweeps

1. Increase pixel-noise amplitude at a fixed landmark count. Compare actual translation, rotation and reprojection errors, and inspect the solver status instead of assuming every local fit has converged.

2. Increase visible count at a fixed noise amplitude. Compare normal and wrong-calibration fits; explain why additional constraints can improve a local estimate without eliminating model bias or guaranteeing monotonic error reduction.

Return to defaults between sweeps. Hold the other control fixed and record both a changing output and an expected invariant. Explain the physical or numerical path from the selected input to the observed response.

## Intentionally broken case

The estimator uses focal length 650 px for observations generated with 800 px. The actual selected points, pixel noise, initializer and positive-depth condition remain unchanged.

Run the same parameter values with the fault enabled. Compare complete curves as well as summary metrics. Identify the actual operation that changed and calculate why it affects the measured result. A changed warning label is not numerical evidence.

## Recovery

Restore focal length 800 px, rerun from the declared initializer and compare the fitted transform, pixel residuals and local rank under the same observations.

Repeat a saved nominal setting and confirm that its values and curves return. Recovery must restore the governing mechanism and its evidence, not merely clear a warning.

## Alternative and limiting cases

This solves a local six-degree-of-freedom pose from a near initializer and a synthetic noncoplanar object; it makes no global PnP uniqueness or arbitrary-initialization claim. The noise sequence is deterministic, visible points are selected by a fixed rule, and solver budget or stalling status remains meaningful even when two independent estimates agree closely.

## Independent evidence and MATLAB-style design boundary

The reference independently constructs landmarks and observations, parameterizes rotation by explicit Euler matrices and solves nonlinear least squares with complex-step pixel derivatives. Production uses rotation-vector increments and an analytic Jacobian. Full rotations, translations and reprojected arrays are compared.

Five retained cases cover baseline, two single-control sweeps, the named fault and recovery. Expected values come from the independent formulation; actual values come from the executable lesson. Absolute and relative comparison tolerances remain 1e-8. Full-state or geometric checks supplement these three-number signatures, which alone cannot establish correctness. MATLAB has not been executed and no MATLAB equivalence is claimed. Browser and container evidence is recorded separately. Agreement between synthetic implementations does not establish empirical model validity.

## Engineering review checklist

Reconstruct one displayed quantity from the actual state or geometric arrays. Check coordinate ordering, signs and units before comparing numbers. Explain which assumption each check constrains, and identify a defect that another check could miss. Preserve the baseline, one controlled sweep, fault and recovery as a reproducible evidence sequence. State the model boundary before making a broader engineering recommendation.

## Common mistakes

Do not infer correctness from a changing headline alone. This solves a local six-degree-of-freedom pose from a near initializer and a synthetic noncoplanar object; it makes no global PnP uniqueness or arbitrary-initialization claim.

Do not change both sliders at once and attribute the result to one cause. Separate a model assumption from a measured property, and a finite-horizon observation from a universal guarantee. Floating-point roundoff is not a physical effect; equally, an attractive plot is not a substitute for the governing calculation.

## Focused check and teach-back

Why can a low pixel residual coexist with a biased translation estimate?

Answer rationale: Pose can compensate partly for incorrect focal calibration, and noisy data are fitted within the assumed model. Residual consistency is different from agreement with independent metric truth; inspect calibration, geometry and the full transform.

Use the embedded Course checkpoint to explain your default, sweep, fault and recovery records to a colleague. Include one calculation with units, the causal diagnosis and an explicit untested boundary. This is a self-assessment; no learner score is stored.
