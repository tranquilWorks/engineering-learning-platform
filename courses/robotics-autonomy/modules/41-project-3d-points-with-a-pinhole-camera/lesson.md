# Transform and Project Points Through a Pinhole Camera



## Model, derivation, and conventions

`p_camera=R^T(p_world-camera_origin)`

`u=f X/Z; v=f Y/Z, accepted only when Z>0.05 m`

`depth_sensitivity=f sqrt(X²+Y²)/Z²`

The camera origin in world coordinates is [0.2,-0.1,1] m and its orientation is a rotation of 0.3 rad about the world y axis. The camera's local positive z axis points forward. World points form a 121-point cloud with x from -0.4 to 0.4 m, y fixed at 0.2 m, and z equal to selected depth plus a sweep from -3.2 to zero metres. The depth slider therefore shifts the world cloud; it is not the camera-frame depth of every point.

A world point first subtracts camera origin and then rotates by R transpose into camera coordinates. Its resulting components X,Y,Z determine projection and visibility. Accepted rays require Z greater than the declared near plane of 0.05 m. This excludes points behind the camera and points too close to the projection singularity. The accepted subset can be empty, in which case projection summary metrics are explicitly unavailable and represented by finite zero sentinels with an availability diagnostic. Those zeros must not be interpreted as a perfectly centred visible cloud.

For accepted points, pixel coordinates relative to the optical centre are u=f*X/Z and v=f*Y/Z. The focal-length slider is in pixels, with square pixels and no principal-point offset or lens distortion in this model. The radius metric is the largest sqrt(u²+v²) across accepted rays. Holding X and Y fixed while perturbing camera depth gives derivative magnitude f*sqrt(X²+Y²)/Z² in pixels per metre. It is a local partial derivative, not the total derivative of moving the world cloud along its tilted-camera trajectory.

The first plot uses a separate diagnostic line of world points with x=0.4 m, y=0.2 m and depth from 0.1 to 12 m. It shows accepted horizontal image coordinates against world depth and stays available even if the selected cloud is entirely rejected. The depth-offset slider affects the selected cloud and its metrics, not this fixed diagnostic line. The second plot shows the selected cloud's actual camera depth against world x, including the near-plane threshold. The latter remains informative even when no rays are accepted. Rejecting invalid points before division keeps the plotted projection finite; it does not conceal their existence, because rejected counts and true camera coordinates are retained. The reconstructed camera rays are also compared against the physically transformed points.

Broken mode skips the pose transformation and treats world coordinates as camera coordinates. It decides acceptance using world z and projects world x,y directly. The third metric counts rays accepted by that faulty rule whose true camera depth is at or behind the near plane. It counts actual geometry failures, not a mode flag. Some far-away clouds can have zero invalid accepted rays while still having wrong pixel locations, so that count is one diagnostic rather than a complete calibration test.

For a simple hand check, a camera-frame point [0.1,0.05,2] m and focal length 800 pixels projects to [40,20] pixels. Doubling focal length doubles both coordinates. Doubling depth at fixed X,Y halves both coordinates and reduces the local depth sensitivity by a factor of four. These relations must be applied after the coordinate transformation; substituting a world height into the denominator is exactly the convention error under study.

## Predict before running

Predict why a positive world height is insufficient to decide whether a point lies in front of a rotated camera. Record the expected direction of change and an invariant before reading the computed result. State a condition under which the fault could be hidden, rather than assuming every faulty setting must look worse.

## Baseline workflow

Reset controls and disable the named fault. Use Focal length = 520.0 px; World cloud depth offset = 3.0 m. Read the response curve, then connect it to the mechanism curve using the governing equations.

Projection over depth plots Image x (px) against World depth (m). Its series are Projection. Camera-frame depths plots Camera depth (m) against World x (m). Its series are Depth, Near plane.

The default record is Maximum accepted image radius: 2881.29 px; Maximum accepted depth sensitivity: 37902.4 px/m; Invalid camera rays incorrectly accepted: 0 count. These computed values are a worked example for these settings, not acceptance limits for every experiment. Keep parameter values and units beside the result. A near-zero residual has meaning only in relation to the stated model and numerical precision.

## Two one-variable sweeps

1. Increase focal length at fixed world-cloud depth. Accepted point count stays unchanged, while pixel radius and depth sensitivity scale linearly. Explain why focal length does not decide front-versus-behind geometry.

2. Shift the world cloud with the depth control at fixed focal length. Inspect true camera depths, accepted count and the near-plane crossings. Compare faulty acceptance with actual transformed coordinates.

Return to defaults between sweeps. Hold the other control fixed and record both a changing output and an expected invariant. Explain the physical or numerical path from the selected input to the observed response.

## Intentionally broken case

The fault omits camera translation and rotation, using world coordinates for projection and acceptance. Invalid accepted rays are counted against the correctly transformed physical geometry.

Run the same parameter values with the fault enabled. Compare complete curves as well as summary metrics. Identify the actual operation that changed and calculate why it affects the measured result. A changed warning label is not numerical evidence.

## Recovery

Restore the world-to-camera transform and compare accepted rays, pixel locations and reprojection residual. A zero invalid-ray count alone does not certify a calibrated projection.

Repeat a saved nominal setting and confirm that its values and curves return. Recovery must restore the governing mechanism and its evidence, not merely clear a warning.

## Alternative and limiting cases

At an empty accepted set, zero-valued projection summaries are unavailable sentinels, not visible on-axis points. A far cloud may hide the faulty visibility count while retaining wrong pixels. The model excludes lens distortion, occlusion, image bounds, calibration uncertainty and camera noise.

## Independent evidence and MATLAB-style design boundary

The reference computes rotated camera components explicitly and derives projection and sensitivity from ray ratios, independently of the production matrix transform. It compares the entire camera cloud, accepted mask and projected pixels.

Five retained cases cover baseline, two single-control sweeps, the named fault and recovery. Expected values come from the independent formulation; actual values come from the executable lesson. Absolute and relative comparison tolerances remain 1e-8. Full-state or geometric checks supplement these three-number signatures, which alone cannot establish correctness. MATLAB has not been executed and no MATLAB equivalence is claimed. Browser and container evidence is recorded separately. Agreement between synthetic implementations does not establish empirical model validity.

## Engineering review checklist

Reconstruct one displayed quantity from the actual state or geometric arrays. Check coordinate ordering, signs and units before comparing numbers. Explain which assumption each check constrains, and identify a defect that another check could miss. Preserve the baseline, one controlled sweep, fault and recovery as a reproducible evidence sequence. State the model boundary before making a broader engineering recommendation.

## Common mistakes

Do not infer correctness from a changing headline alone. At an empty accepted set, zero-valued projection summaries are unavailable sentinels, not visible on-axis points.

Do not change both sliders at once and attribute the result to one cause. Separate a model assumption from a measured property, and a finite-horizon observation from a universal guarantee. Floating-point roundoff is not a physical effect; equally, an attractive plot is not a substitute for the governing calculation.

## Focused check and teach-back

Why can the faulty projection report zero invalid accepted rays and still be wrong?

Answer rationale: All points may genuinely lie in front of the camera while the omitted translation and rotation still change their ray directions and pixels. Visibility is only one condition; coordinate transformation and reprojection agreement must also be checked.

Use the embedded Course checkpoint to explain your default, sweep, fault and recovery records to a colleague. Include one calculation with units, the causal diagnosis and an explicit untested boundary. This is a self-assessment; no learner score is stored.
