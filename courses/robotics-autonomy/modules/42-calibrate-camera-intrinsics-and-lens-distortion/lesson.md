# Fit Camera Intrinsics with Known Calibration Poses



## Model, derivation, and conventions

`u=f x+f k1 x(x²+y²)+cx; v=f y+f k1 y(x²+y²)+cy`

`beta=[f,f*k1,cx,cy]; beta_hat=argmin ||A beta-pixels||²`

`heldout_RMS=sqrt(mean(||predicted_pixel-true_pixel||²))`

The board has twelve known points, arranged as four columns and three rows over a 0.9 m by 0.6 m rectangle. Each selected view places that board at a known rotation and translation in front of the camera. Board coordinates and all extrinsic poses are supplied exactly. This is a bounded intrinsic-calibration problem, not a solver that simultaneously discovers board pose, focal length and lens distortion from photographs. Naming that distinction matters because unknown poses introduce additional degrees of freedom and ambiguities.

The camera uses square pixels, focal length 800 px, principal point [320,240] px and the selected first radial coefficient k1. A transformed board point gives normalized coordinates x=X/Z and y=Y/Z, with r²=x²+y². The lens multiplies both normalized coordinates by 1+k1*r² before focal scaling and principal-point translation. There is no tangential distortion, skew or second radial coefficient. The coordinate values are dimensionless, so k1 is dimensionless; f and principal-point components are in pixels. All constructed calibration points remain in front of the camera.

For these known poses the pixel equations are linear in four coefficients: f, the product f*k1, cx and cy. A horizontal observation supplies the row [x,x*r²,1,0], and its vertical partner supplies [y,y*r²,0,1]. Stacking actual observations creates a 2N by 4 system. Least squares fits those coefficients; k1 is subsequently recovered by dividing the fitted second coefficient by fitted focal length. That division requires nonzero focal length and a full-rank design. The diagnostics retain fitted parameters, rank and conditioning, rather than assuming that a count of views establishes identifiability.

Training observations include small deterministic horizontal and vertical pixel perturbations. They are not independent random samples, and a view-count sweep is not a Monte Carlo confidence experiment. Increasing the count adds actual distinct board poses and rows to the system. The useful question is whether those poses constrain the parameters and reduce prediction error; no fixed inverse-square-root formula assigns the result. The synthetic geometry keeps the radial map monotone across the sampled field even at the most negative allowed coefficient.

Four additional known poses supply forty-eight held-out points. They do not participate in fitting, and their targets use the noiseless synthetic camera. The first metric measures vector reprojection RMS across all forty-eight points. The second measures absolute focal-length bias as a percentage of 800 px. The third repeats the reprojection calculation over the outer quarter of those points by normalized radius. This is an edge-region check on the actual held-out set, not a claim to cover an entire physical sensor. A small training residual alone would miss an omitted distortion term whose bias grows away from the centre.

The fault removes the radial column and fits only common focal length and principal point. It retains the same selected k1, view count and observed pixels. Focal length may partly compensate for unmodeled distortion, which can make an apparently plausible estimate disagree with held-out geometry. At k1=0 the omitted term is physically absent, so the fault can be benign or even fit the deterministic noise differently. With default negative distortion, the full model gives a much smaller held-out residual than the restricted fit. That result follows from actually solving and reprojecting, not from an error penalty assigned to the fault switch.

A simple check uses x=0.2, y=0, k1=-0.18. The radial factor is 0.9928, so the horizontal offset from the principal point is 800*0.2*0.9928=158.848 px. Ignoring distortion predicts 160 px before any fitted compensation. The difference is already 1.152 px for this single point. More data cannot make a physically absent model term appear; the model must first contain the needed dependence.

## Predict before running

Predict whether adding more board views can eliminate held-out bias when the fitted model omits real radial distortion. Record the expected direction of change and an invariant before reading the computed result. State a condition under which the fault could be hidden, rather than assuming every faulty setting must look worse.

## Baseline workflow

Reset controls and disable the named fault. Use Radial distortion k1 = -0.18 1; Known board poses = 18.0 count. Read the response curve, then connect it to the mechanism curve using the governing equations.

Held-out residuals plots Residual (px) against Point index (1). Its series are Residual. Fitted radial model plots Radial factor (1) against Radius (1). Its series are True, Fitted.

The default record is Held-out reprojection RMS: 0.00630801 px; Focal-length bias: 0.00406989 %; Outer-region reprojection RMS: 0.00778727 px. These computed values are a worked example for these settings, not acceptance limits for every experiment. Keep parameter values and units beside the result. A near-zero residual has meaning only in relation to the stated model and numerical precision.

## Two one-variable sweeps

1. Change k1 while holding the number of views fixed. Compare held-out and outer-region errors in both modes, and include k1=0 to expose the case where removing distortion is physically appropriate.

2. Change view count at fixed nonzero distortion. Inspect actual rank, conditioning, fitted focal length and held-out residual; explain why the restricted fit can retain systematic bias despite more rows.

Return to defaults between sweeps. Hold the other control fixed and record both a changing output and an expected invariant. Explain the physical or numerical path from the selected input to the observed response.

## Intentionally broken case

The fit omits the radial-distortion column while the observations retain the selected lens distortion. No control value or measured residual is overwritten.

Run the same parameter values with the fault enabled. Compare complete curves as well as summary metrics. Identify the actual operation that changed and calculate why it affects the measured result. A changed warning label is not numerical evidence.

## Recovery

Restore the full four-coefficient fit using the same observations. Confirm the held-out and outer-region residuals and reconstruct k1 from the fitted coefficient product.

Repeat a saved nominal setting and confirm that its values and curves return. Recovery must restore the governing mechanism and its evidence, not merely clear a warning.

## Alternative and limiting cases

Known board poses and coordinates are exact; this does not perform joint pose/intrinsic calibration, feature extraction or real lens calibration. At zero radial distortion the omitted-column fault may be hidden. Deterministic noise, finite pose coverage, and conditioning limit generalization; more views do not guarantee monotonically smaller error.

## Independent evidence and MATLAB-style design boundary

The reference independently constructs transformed board coordinates and the regression rows, solves the normal equations, and reprojects separate held-out poses. Production uses a direct least-squares factorization. Full fitted parameters and residual arrays supplement the signature.

Five retained cases cover baseline, two single-control sweeps, the named fault and recovery. Expected values come from the independent formulation; actual values come from the executable lesson. Absolute and relative comparison tolerances remain 1e-8. Full-state or geometric checks supplement these three-number signatures, which alone cannot establish correctness. MATLAB has not been executed and no MATLAB equivalence is claimed. Browser and container evidence is recorded separately. Agreement between synthetic implementations does not establish empirical model validity.

## Engineering review checklist

Reconstruct one displayed quantity from the actual state or geometric arrays. Check coordinate ordering, signs and units before comparing numbers. Explain which assumption each check constrains, and identify a defect that another check could miss. Preserve the baseline, one controlled sweep, fault and recovery as a reproducible evidence sequence. State the model boundary before making a broader engineering recommendation.

## Common mistakes

Do not infer correctness from a changing headline alone. Known board poses and coordinates are exact; this does not perform joint pose/intrinsic calibration, feature extraction or real lens calibration.

Do not change both sliders at once and attribute the result to one cause. Separate a model assumption from a measured property, and a finite-horizon observation from a universal guarantee. Floating-point roundoff is not a physical effect; equally, an attractive plot is not a substitute for the governing calculation.

## Focused check and teach-back

Why can a low training error and an apparently sensible focal length still fail to establish a calibrated camera?

Answer rationale: An omitted radial term can be absorbed partly into focal length and principal point over the training geometry. Held-out rays, especially away from the optical centre, reveal the wrong spatial dependence; rank and coverage must also be checked.

Use the embedded Course checkpoint to explain your default, sweep, fault and recovery records to a colleague. Include one calculation with units, the causal diagnosis and an explicit untested boundary. This is a self-assessment; no learner score is stored.
