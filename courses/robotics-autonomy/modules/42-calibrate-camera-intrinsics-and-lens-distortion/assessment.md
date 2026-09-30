## P42 evidence task

Why can a low training error and an apparently sensible focal length still fail to establish a calibrated camera?

Before running: Predict whether adding more board views can eliminate held-out bias when the fitted model omits real radial distortion.

Collect a default record, one single-control sweep, the named fault and recovery. Record the parameter values, plotted quantities and units so another learner can reproduce the comparison.

Held-out residuals plots Residual (px) against Point index (1). Its series are Residual. Fitted radial model plots Radial factor (1) against Radius (1). Its series are True, Fitted.

### Reasoning rubric

- Model: reconstruct a displayed value using `u=f x+f k1 x(x²+y²)+cx; v=f y+f k1 y(x²+y²)+cy` and the actual state or geometry.
- Evidence: Change k1 while holding the number of views fixed. Compare held-out and outer-region errors in both modes, and include k1=0 to expose the case where removing distortion is physically appropriate.
- Diagnosis: The fit omits the radial-distortion column while the observations retain the selected lens distortion. No control value or measured residual is overwritten.
- Recovery and scope: Restore the full four-coefficient fit using the same observations. Confirm the held-out and outer-region residuals and reconstruct k1 from the fitted coefficient product. State this boundary: Known board poses and coordinates are exact; this does not perform joint pose/intrinsic calibration, feature extraction or real lens calibration. At zero radial distortion the omitted-column fault may be hidden. Deterministic noise, finite pose coverage, and conditioning limit generalization; more views do not guarantee monotonically smaller error.

### Check your explanation

An omitted radial term can be absorbed partly into focal length and principal point over the training geometry. Held-out rays, especially away from the optical centre, reveal the wrong spatial dependence; rank and coverage must also be checked.

A complete explanation contains a calculation, an observed comparison with units, the executed fault and a reproduced recovery. Name a setting that can hide the fault and a claim requiring evidence outside this model. This is a self-assessment; no learner score is stored.
