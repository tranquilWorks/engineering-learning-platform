# Triangulate Calibrated Stereo Rays and Propagate Pixel Noise



## Model, derivation, and conventions

`point_hat=midpoint(closest_points_on_calibrated_rays)`

`depth_truth=f*baseline/disparity; f=520 px`

`Sigma_point=J_pixels*Sigma_pixels*J_pixels^T; sigma_Z=sqrt(Sigma_point[2,2])`

The left camera defines the world frame, with its centre at the origin and its positive z axis forward. The right centre is [B,0,0] m, where B is the selected baseline, and the right camera has a known yaw of 0.04 rad. Both use focal length 520 px and a common zero principal-point offset. The selected disparity d defines a true point with depth Z=520*B/d and normalized left direction [0.08,0.04,1]. Because the right camera is rotated, d is the rectified construction disparity, not simply the difference between the two raw observed horizontal coordinates.

The model projects that true point through both actual camera poses to create four pixel observations. Each pixel pair defines a camera ray. The normal triangulator rotates the right ray into the left/world frame and computes the closest points on the two rays by a three-by-two least-squares solve. Their midpoint is the estimated three-dimensional point. With the exact noiseless observations and correct calibration, the rays intersect up to numerical roundoff. This is an executed geometric reconstruction, not merely reporting the value fB/d that was used to construct the scene.

Broken mode assumes the right camera is parallel to the left and omits its known yaw when interpreting the observed right pixel. The observed pixels themselves do not change. The resulting rays can be skew, so their closest-point midpoint need not lie exactly on either ray. The model reprojects the estimated point through the true cameras and computes the RMS Euclidean pixel discrepancy over the two views. The faulty calibration therefore produces a measured reprojection residual through actual geometry. Assigning a fixed residual whenever a switch is on would miss dependence on the selected baseline and disparity.

The first metric is the estimated world z coordinate in metres. The second is predicted standard deviation of that depth under an explicit observation-noise model. The third is the actual two-view reprojection RMS in pixels for the current deterministic estimate. Noise is not randomly injected into that estimate: uncertainty and realized error are separate quantities. The wrong calibration can even report a smaller predicted uncertainty around a biased depth. That covariance is conditional on its assumed ray model and does not include calibration bias. Each of the four pixel components is assumed independent with standard deviation 0.5/sqrt(2) px, giving 0.5 px disparity standard deviation for an ideal parallel horizontal pair.

The uncertainty calculation differentiates the actual closest-ray least-squares solution with respect to all four observed pixel components. Production differentiates the normal equations analytically, including how each ray changes with its pixels. Multiplying that Jacobian by the declared pixel covariance and its transpose gives a three-dimensional covariance; the square root of its z diagonal entry is the reported depth standard deviation. The independent reference uses a closed dot-product ray solution and complex-step differentiation. Their agreement constrains the uncertainty calculation without turning a first-order approximation into a measured confidence interval.

For parallel cameras, the familiar derivative is dZ/dd=-fB/d², so sigma_Z is approximately fB*sigma_d/d². At B=0.18 m and d=28 px, the construction depth is about 3.343 m. The actual yawed-ray calculation determines its own uncertainty and should be compared with that parallel limiting intuition rather than forced to equal it. Increasing B at fixed selected d moves the synthetic point farther away; both depth and its absolute uncertainty can increase. The common recommendation that a larger baseline improves precision at fixed physical range holds a different variable fixed.

Very small disparity makes depth weakly constrained, and a first-order Gaussian covariance becomes a poor description when noise is not small relative to disparity. The interactive range remains positive and finite, but the farthest cases should still be read as an ill-conditioned measurement geometry. The model excludes calibration uncertainty, correspondence mistakes, occlusion and a real stereo matcher. A small noiseless reprojection error establishes consistency with the assumed cameras; it does not establish accurate metric depth if those camera poses are themselves wrong.

## Predict before running

Predict how depth and depth uncertainty change when baseline increases while the selected rectified disparity, rather than physical range, is held fixed. Record the expected direction of change and an invariant before reading the computed result. State a condition under which the fault could be hidden, rather than assuming every faulty setting must look worse.

## Baseline workflow

Reset controls and disable the named fault. Use Stereo baseline = 0.18 m; Rectified construction disparity = 28.0 px. Read the response curve, then connect it to the mechanism curve using the governing equations.

Triangulated depth plots Depth (m) against Disparity (px). Its series are Estimate, True. Pixel-noise uncertainty plots Depth sigma (m) against Disparity (px). Its series are Sigma, Selected.

The default record is Triangulated depth: 3.34286 m; Predicted depth standard deviation: 0.0597086 m; Two-view reprojection RMS: 9.36681e-14 px. These computed values are a worked example for these settings, not acceptance limits for every experiment. Keep parameter values and units beside the result. A near-zero residual has meaning only in relation to the stated model and numerical precision.

## Two one-variable sweeps

1. Increase baseline while holding selected rectified disparity fixed. Record the resulting change in scene depth and uncertainty, and explain why this is different from comparing two baselines viewing the same fixed-range point.

2. Increase disparity at a fixed baseline. Compare estimated depth, predicted uncertainty and reprojection residual, then examine the low-disparity end where first-order uncertainty is least trustworthy.

Return to defaults between sweeps. Hold the other control fixed and record both a changing output and an expected invariant. Explain the physical or numerical path from the selected input to the observed response.

## Intentionally broken case

The triangulator treats the yawed right camera as parallel while preserving its actual observed pixels and the selected geometry. Reprojection is evaluated through the true camera poses.

Run the same parameter values with the fault enabled. Compare complete curves as well as summary metrics. Identify the actual operation that changed and calculate why it affects the measured result. A changed warning label is not numerical evidence.

## Recovery

Restore the right-camera ray rotation, solve the closest-ray system again and verify both the reconstructed point and actual two-view residual.

Repeat a saved nominal setting and confirm that its values and curves return. Recovery must restore the governing mechanism and its evidence, not merely clear a warning.

## Alternative and limiting cases

The deterministic estimate uses noiseless synthetic correspondences; its covariance is a first-order prediction under independent pixel noise, not an observed confidence interval. Positive disparity avoids the infinite-depth singularity but does not make low-disparity geometry well conditioned. Calibration uncertainty, matching errors and occlusion are excluded.

## Independent evidence and MATLAB-style design boundary

The reference separately projects the scene, normalizes the two directions and solves the dot-product closest-ray equations. Complex-step derivatives of that formulation check the production analytic pixel Jacobian and propagated depth variance.

Five retained cases cover baseline, two single-control sweeps, the named fault and recovery. Expected values come from the independent formulation; actual values come from the executable lesson. Absolute and relative comparison tolerances remain 1e-8. Full-state or geometric checks supplement these three-number signatures, which alone cannot establish correctness. MATLAB has not been executed and no MATLAB equivalence is claimed. Browser and container evidence is recorded separately. Agreement between synthetic implementations does not establish empirical model validity.

## Engineering review checklist

Reconstruct one displayed quantity from the actual state or geometric arrays. Check coordinate ordering, signs and units before comparing numbers. Explain which assumption each check constrains, and identify a defect that another check could miss. Preserve the baseline, one controlled sweep, fault and recovery as a reproducible evidence sequence. State the model boundary before making a broader engineering recommendation.

## Common mistakes

Do not infer correctness from a changing headline alone. The deterministic estimate uses noiseless synthetic correspondences; its covariance is a first-order prediction under independent pixel noise, not an observed confidence interval.

Do not change both sliders at once and attribute the result to one cause. Separate a model assumption from a measured property, and a finite-horizon observation from a universal guarantee. Floating-point roundoff is not a physical effect; equally, an attractive plot is not a substitute for the governing calculation.

## Focused check and teach-back

Why can increasing baseline increase displayed depth uncertainty in this particular sweep?

Answer rationale: The control holds rectified disparity fixed, so increasing baseline also moves the constructed point farther away. The fixed-range precision benefit of a larger baseline answers a different experiment; the held variable must be stated.

Use the embedded Course checkpoint to explain your default, sweep, fault and recovery records to a colleague. Include one calculation with units, the causal diagnosis and an explicit untested boundary. This is a self-assessment; no learner score is stored.
