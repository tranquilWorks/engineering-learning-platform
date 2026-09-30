## P43 evidence task

Why should the orientation fault leave geometric repeatability unchanged even when descriptor distances increase?

Before running: Predict which results should stay unchanged when descriptor orientation normalization is disabled while the detector and images stay fixed.

Collect a default record, one single-control sweep, the named fault and recovery. Record the parameter values, plotted quantities and units so another learner can reproduce the comparison.

Detected corners plots Row (px) against Column (px). Its series are Image, Corners. Paired patch distance plots Distance (1) against Pair index (1). Its series are Distance.

### Reasoning rubric

- Model: reconstruct a displayed value using `H=det(M)-0.04*trace(M)²; M=smooth(gradient(I)*gradient(I)^T)` and the actual state or geometry.
- Evidence: Raise the relative corner threshold at a fixed rotation. Inspect the actual detected centres and pairing count, then distinguish changes in detector coverage from changes in descriptor distance.
- Diagnosis: Only descriptor orientation normalization is disabled. Detection, image formation and ground-truth geometric pairing remain identical.
- Recovery and scope: Restore orientation-based sampling and compare the same paired patches. Confirm that feature counts remain fixed across the fault/recovery comparison. State this boundary: This is a fixed-scale synthetic corner detector and normalized intensity descriptor; it makes no SIFT, scale, perspective or general illumination-invariance claim. Zero rotation can hide the orientation fault. Empty matching sets have an unavailable-distance status, and low distance alone does not establish unique correspondence.

### Check your explanation

Repeatability is measured from detected positions and known image geometry. The fault changes only how a patch is sampled into a descriptor after detection; it cannot retroactively change those feature centres.

A complete explanation contains a calculation, an observed comparison with units, the executed fault and a reproduced recovery. Name a setting that can hide the fault and a claim requiring evidence outside this model. This is a self-assessment; no learner score is stored.
