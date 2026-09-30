# Detect Corners and Normalize Patch Orientation



## Model, derivation, and conventions

`H=det(M)-0.04*trace(M)²; M=smooth(gradient(I)*gradient(I)^T)`

`theta=atan2(sum(y*I),sum(x*I)) within a circular patch`

`descriptor=(rotated_sampled_patch-mean)/norm; distance=||d1-d2||2`

Two actual 96 by 96 synthetic grayscale images are sampled from a continuous scene. Nine separated, textured soft corners have different orientations and amplitudes. The second image samples the same scene after the selected in-plane rotation about image centre [47.5,47.5] px. Analytic resampling avoids introducing an additional interpolation policy into image generation, but detection and descriptors still operate on finite sampled pixels. This is a fixed-scale corner-and-patch laboratory, not an implementation of SIFT or a demonstration of general viewpoint invariance.

Horizontal and vertical finite differences estimate the sampled image gradient. Their squared and cross products are smoothed with the separable binomial weights [1,4,6,4,1]/16. Those entries form the local two-by-two structure tensor M. The Harris response is determinant(M) minus 0.04 times trace(M) squared. A corner has substantial intensity variation in two directions; a strong edge can have one large gradient direction without providing the same positional constraint. Image intensity and this response have arbitrary synthetic scales, so the threshold is expressed relative to the peak response of each image.

Candidates must exceed the selected positive response fraction, be maxima within a seven-pixel window, and lie outside an eight-pixel boundary exclusion. A deterministic descending-response order resolves candidate selection, and accepted centres must be more than six pixels apart. These operations actually determine the feature count. Increasing threshold can discard weak corners; it does not multiply an assigned count by a threshold formula. Rotation changes where corner structure falls on the sampling lattice, so the two images need not yield identical candidate counts even when they contain the same continuous scene.

For each accepted feature, an intensity centroid inside a circular radius-six patch gives an orientation angle through atan2. The descriptor samples a nine-by-nine intensity patch in that estimated frame using bilinear interpolation. Its mean is removed and the resulting vector is normalized to unit Euclidean length. Mean removal and normalization reduce simple brightness-offset and scale effects within this model; they do not guarantee robustness to arbitrary illumination or occlusion. Flat patches need a finite normalization floor, although the positive corner threshold normally avoids them in this fixture.

Evaluation transforms detected base-image coordinates by the known scene rotation and pairs them with nearby detected centres in the second image. A pair must lie within 2.5 px and use a target feature only once. This ground-truth geometry is used for evaluation, not to discover an unknown camera motion. Geometric repeatability is the number of accepted pairs divided by the number of base detections. Mean descriptor distance is computed only on those paired vectors. The final count is the number of detections in the rotated image. All three quantities are measured from detector and patch outputs rather than assigned by rotation angle.

The fault samples each descriptor in the image axes instead of its estimated orientation. It leaves both sampled images, corner responses, suppression and geometric pairing unchanged. Consequently geometric repeatability and detected count should agree across modes. A claim that this descriptor-only fault necessarily reduces corner repeatability would confuse distinct stages of a vision pipeline. At zero image rotation the two images coincide, and both descriptor treatments can give zero pair distance. At other rotations, orientation normalization commonly reduces the distance, but finite sampling, imperfect orientation and ambiguous patches prevent a universal guarantee.

Descriptor distance is dimensionless. For two unit vectors it lies between zero and two, with zero meaning identical normalized samples and two meaning opposite vectors. A low distance does not establish a unique feature match, and the geometric pairing used here must not be presented as a deployed matching algorithm. If no geometric pairs exist, the finite zero summary is marked unavailable rather than described as perfect matching. The patch-distance axis spans its dimensionless zero-to-two range, so near-zero roundoff is not magnified into apparent mismatch. The plotted image uses black for lower intensity and white for higher intensity. Its detected centres let the learner inspect what the feature count actually represents; the paired-distance curve supplies evidence about the separate descriptor stage.

## Predict before running

Predict which results should stay unchanged when descriptor orientation normalization is disabled while the detector and images stay fixed. Record the expected direction of change and an invariant before reading the computed result. State a condition under which the fault could be hidden, rather than assuming every faulty setting must look worse.

## Baseline workflow

Reset controls and disable the named fault. Use Relative corner threshold = 0.12 1; Image rotation = 25.0 deg. Read the response curve, then connect it to the mechanism curve using the governing equations.

Detected corners plots Row (px) against Column (px). Its series are Image, Corners. Paired patch distance plots Distance (1) against Pair index (1). Its series are Distance.

The default record is Geometric repeatability: 1 1; Mean paired descriptor distance: 0.177203 1; Rotated-image detections: 8 count. These computed values are a worked example for these settings, not acceptance limits for every experiment. Keep parameter values and units beside the result. A near-zero residual has meaning only in relation to the stated model and numerical precision.

## Two one-variable sweeps

1. Raise the relative corner threshold at a fixed rotation. Inspect the actual detected centres and pairing count, then distinguish changes in detector coverage from changes in descriptor distance.

2. Change rotation at a fixed threshold, including zero and a quarter turn. Compare oriented and image-axis descriptors while checking that geometric detections and repeatability agree between modes at each setting.

Return to defaults between sweeps. Hold the other control fixed and record both a changing output and an expected invariant. Explain the physical or numerical path from the selected input to the observed response.

## Intentionally broken case

Only descriptor orientation normalization is disabled. Detection, image formation and ground-truth geometric pairing remain identical.

Run the same parameter values with the fault enabled. Compare complete curves as well as summary metrics. Identify the actual operation that changed and calculate why it affects the measured result. A changed warning label is not numerical evidence.

## Recovery

Restore orientation-based sampling and compare the same paired patches. Confirm that feature counts remain fixed across the fault/recovery comparison.

Repeat a saved nominal setting and confirm that its values and curves return. Recovery must restore the governing mechanism and its evidence, not merely clear a warning.

## Alternative and limiting cases

This is a fixed-scale synthetic corner detector and normalized intensity descriptor; it makes no SIFT, scale, perspective or general illumination-invariance claim. Zero rotation can hide the orientation fault. Empty matching sets have an unavailable-distance status, and low distance alone does not establish unique correspondence.

## Independent evidence and MATLAB-style design boundary

The reference separately constructs image coordinates, uses explicit finite differences and two-dimensional convolution for the tensor, performs window maxima selection, and evaluates bilinear interpolation from its four pixel weights. Full images, responses, detections, orientations and descriptors are compared.

Five retained cases cover baseline, two single-control sweeps, the named fault and recovery. Expected values come from the independent formulation; actual values come from the executable lesson. Absolute and relative comparison tolerances remain 1e-8. Full-state or geometric checks supplement these three-number signatures, which alone cannot establish correctness. MATLAB has not been executed and no MATLAB equivalence is claimed. Browser and container evidence is recorded separately. Agreement between synthetic implementations does not establish empirical model validity.

## Engineering review checklist

Reconstruct one displayed quantity from the actual state or geometric arrays. Check coordinate ordering, signs and units before comparing numbers. Explain which assumption each check constrains, and identify a defect that another check could miss. Preserve the baseline, one controlled sweep, fault and recovery as a reproducible evidence sequence. State the model boundary before making a broader engineering recommendation.

## Common mistakes

Do not infer correctness from a changing headline alone. This is a fixed-scale synthetic corner detector and normalized intensity descriptor; it makes no SIFT, scale, perspective or general illumination-invariance claim.

Do not change both sliders at once and attribute the result to one cause. Separate a model assumption from a measured property, and a finite-horizon observation from a universal guarantee. Floating-point roundoff is not a physical effect; equally, an attractive plot is not a substitute for the governing calculation.

## Focused check and teach-back

Why should the orientation fault leave geometric repeatability unchanged even when descriptor distances increase?

Answer rationale: Repeatability is measured from detected positions and known image geometry. The fault changes only how a patch is sampled into a descriptor after detection; it cannot retroactively change those feature centres.

Use the embedded Course checkpoint to explain your default, sweep, fault and recovery records to a colleague. Include one calculation with units, the causal diagnosis and an explicit untested boundary. This is a self-assessment; no learner score is stored.
