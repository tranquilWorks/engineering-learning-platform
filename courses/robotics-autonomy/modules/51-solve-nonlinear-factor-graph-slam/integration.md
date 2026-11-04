# Joint pose and unknown-landmark estimation

The earlier graph above is a useful localization component: its landmarks are supplied as known coordinates. Here the map itself is unknown. Every robot pose has east position, north position and heading, and each of three landmarks contributes two unknown coordinates. With N poses, the optimizer therefore has 3N+6 variables. It cannot obtain a map by merely drawing the supplied world geometry; observations must constrain both robot and landmark variables.

## State, measurement and frame conventions

Write a robot pose as (p_i, theta_i), with R_i rotating body vectors into world coordinates. Landmark j has world coordinate l_j. A body-frame landmark observation predicts R_i^T(l_j-p_i). Our synthetic sensor reports this two-component displacement in metres. It is a calibrated Cartesian landmark sensor, not an executed feature detector, a camera triangulator or a probabilistic range-bearing sensor. Correspondence IDs are known in this experiment.

Adjacent odometry predicts R_i^T(p_(i+1)-p_i) and theta_(i+1)-theta_i. Translation and heading have separate standard deviations: 0.03 m and 0.015 rad. Landmark coordinates are whitened by 0.025 m. The final-to-first positional closure uses max(loop_noise_m, 0.02 m), while its angular scale is 0.02 rad. The selected control changes both the synthetic closure displacement and its declared uncertainty. Explain why this is different from increasing measurement weight while leaving an identical observation fixed.

Headings are continuous, unwrapped coordinates. The synthetic circuit increases heading by 2 pi; the closure subtracts that known turn before forming its angular residual. The scope is consequently a single initialized planar circuit, not unrestricted angle unwrapping or global place recognition. The generated world truth supplies synthetic measurements and evaluation plots. Optimizer residuals consume odometry, landmark observations and an explicit first-pose prior, never an array of true landmark coordinates.

## Derive one Jacobian row

For the landmark residual r=R_i^T(l_j-p_i)-z_ij, the position derivative is -R_i^T and the landmark derivative is R_i^T. If S rotates a vector counterclockwise by ninety degrees, the heading derivative is -S R_i^T(l_j-p_i). This last column is essential: treating body-frame observations as world-frame displacements discards heading information.

Consider theta_i=pi/2, p_i=(0,0) m and l_j=(1,0) m. The body-frame observation is (0,-1) m. A small positive heading perturbation changes its first component in the negative direction. Work through the sign using the rotation matrix rather than memorizing a derivative. Our finite-perturbation tests check every Jacobian column, including loop closure, against the residual function.

The optimizer solves J delta approximately equal to -r using a sparse least-squares iteration. It backtracks when a candidate raises the weighted objective, then relinearizes at the updated state. The convergence plot is the squared norm of all whitened residuals; it is dimensionless. A decreasing objective establishes progress on this initialized problem, not uniqueness, global optimality or a calibrated uncertainty estimate. No covariance coverage claim is made.

## Gauge freedom is a physical symmetry

Without an absolute prior, translating or rotating every pose and landmark together leaves all body observations unchanged. There are three planar gauge directions: two translations and one rotation. Adding more relative observations does not remove them. Healthy mode anchors the first pose with a 0.01 m positional scale and 0.01 rad heading scale.

Broken mode removes that prior and starts the entire map and trajectory in a translated and rotated frame. The relative residual can still become small while absolute coordinates disagree with the world plot. This is an intentional diagnostic, not a failed optimizer. The independent check aligns the free solution by one rigid transform before comparing its geometry. It separately checks that the production Jacobian annihilates all three gauge directions; an arbitrary hidden anchor would fail that test.

## Predict, sweep and interpret

At the default 30 poses and 0.08 m closure control, predict that the three landmarks remain near their generating locations and that multiple nonlinear iterations reduce the objective. Inspect both map estimates and the objective rather than using the earlier component graph's signature as evidence of joint SLAM.

For the first sweep, vary loop_noise_m while holding pose count fixed. The closure measurement becomes more displaced but, above the 0.02 m floor, also less trusted. Expect a balance among odometry, repeated landmark observations and closure. Do not infer a monotone landmark-error law merely from a monotone control.

For the second sweep, restore closure noise and vary pose_count. This changes the discretization and number of observations around the same circuit. More observations provide more information, but the deterministic perturbations also sample different phases. Raw objective values sum different numbers of residuals and therefore cannot directly rank accuracy across different pose counts.

Enable broken mode and compare the aligned shape with the absolute coordinates. Restore the prior without altering either numeric control. Recovery should reproduce the original deterministic anchored solution. If the solution does not return, investigate initialization, stale state or an unintended persistent map before changing numerical tolerances.

## Independent evidence and assessment

The production implementation uses real analytic Jacobians and a Gauss-Newton line search. The separate reference expresses rotations and observations with complex numbers, obtains numerical derivatives and uses a trust-region least-squares optimizer. Tests compare every estimated pose and landmark, the final objective, and the gauge behavior at small, default, large and off-grid control settings. Agreement is supplemented by the finite-perturbation Jacobian check; sharing a residual mistake between two solvers would otherwise remain possible.

Submit four pieces of evidence: derive the heading column for the worked observation; compare anchored and gauge-aligned free solutions; explain one closure-noise sweep using both measurement and weighting changes; and demonstrate deterministic recovery. A response that only reports a small final residual is incomplete because an unanchored graph can achieve that result in an arbitrary frame.

The prerequisite is the linear joint pose/landmark graph in P16; P26 supplies planar/spatial pose conventions, P49 explains information rank, and P50/P52 cover association and false-loop handling. This experiment uses known correspondences and deterministic small perturbations. It does not execute data association, loop detection, incremental sparse elimination, three-dimensional SLAM or real-sensor validation.

For the distinction between pose-only and landmark-variable graphs, see the primary [GTSAM factor-graph tutorial](https://gtsam.org/tutorials/intro.html). The equations, generated scene and implementations here are independently authored for this bounded lesson.
