# Fit Translation Consensus from Corrupted Image Matches



## Model, derivation, and conventions

`displacement_i=target_i-source_i; residual_i=||displacement_i-t_hat||`

`consensus(t)={i: residual_i<=threshold}; t_refit=mean(displacement_consensus)`

`false_acceptance=accepted_true_outliers/true_outlier_count`

Eighty synthetic source pixels form a ten-by-eight grid. The true second-image motion is the translation [5,-3] px. Small deterministic sinusoidal perturbations are added to genuine displacements. The outlier control chooses a count by floor(80*fraction), and a fixed permutation selects which correspondences are replaced. Their wrong displacements lie on a broad biased ring, well separated from the true compact translation cluster. Both normal and faulty fits receive exactly the same source pixels, targets, selected fraction and residual threshold.

The fitted geometric family is translation only. One correspondence therefore supplies a minimal candidate translation equal to its observed displacement. The normal algorithm exhaustively evaluates all eighty candidates. It computes the Euclidean pixel residual of every displacement relative to each candidate, counts residuals at or below the threshold, and chooses the largest consensus. Residual sum of squares breaks equal-support ties, followed by a deterministic candidate index. This is deterministic exhaustive consensus; it is not random RANSAC and supplies no random-sampling confidence or probability-of-success claim.

The winning inliers are refitted by averaging their displacement vectors, which solves the two-component least-squares translation problem. The algorithm then recomputes the residual mask and repeats the refit until the mask stabilizes or the declared iteration budget ends. The final accepted set is measured from the final fitted model, not copied from a known truth label. Ground-truth outlier labels are used only when evaluating the result. That separation prevents the demonstration from secretly giving the estimator the answer.

The first metric is the final accepted fraction among all eighty correspondences. The second is the Euclidean error between the fitted translation and [5,-3], in pixels. The third is the fraction of true synthetic outliers accepted by the final residual mask. If no true outliers exist, that rate has the explicitly defined value zero rather than an undefined division. An empty accepted set would be an unavailable-fit condition, not a fabricated zero-error estimate. The retained arrays contain displacements, candidate support, final residuals and truth labels so that a headline can be reconstructed.

The faulty comparison fits all eighty displacement vectors at once. This is the ordinary least-squares solution without consensus rejection. It still applies the selected residual threshold when reporting which observations agree with its fitted model; the threshold does not change the all-data estimate. Biased outliers move that estimate away from the true cluster and can simultaneously lower its accepted fraction. This gives a causal comparison between robust selection and a nonrobust fit instead of an error term directly proportional to the fault switch.

For a hand calculation, two noiseless genuine displacements [5,-3] and one gross mismatch [35,15] have all-data mean [15,3]. Its translation error is sqrt(10²+6²), approximately 11.66 px. A sufficiently tight consensus around the two genuine samples refits [5,-3]. The actual experiment uses eighty samples and small inlier perturbations, but the mechanism is the same: a mean responds to the magnitude of every included displacement, whereas consensus uses a bounded geometric acceptance rule before refitting.

A permissive threshold can admit wrong matches; a tight threshold can reject noisy genuine matches. More accepted correspondences therefore need not mean a better model. The synthetic outlier ring spreads wrong hypotheses, so even a high contamination fraction can leave the true compact cluster as the largest consensus. This is a property of this fixture, not a guarantee at the same outlier fraction in another scene. Coherent repeated textures could form a larger wrong cluster. Translation also excludes rotation, scale, perspective and epipolar geometry, so a real camera motion outside this family would invalidate the residual interpretation.

## Predict before running

Predict why a low average residual over selected correspondences is insufficient without checking support and known synthetic model error. Record the expected direction of change and an invariant before reading the computed result. State a condition under which the fault could be hidden, rather than assuming every faulty setting must look worse.

## Baseline workflow

Reset controls and disable the named fault. Use Match outlier fraction = 0.35 1; Consensus threshold = 2.0 px. Read the response curve, then connect it to the mechanism curve using the governing equations.

Match residuals plots Residual (px) against Match index (1). Its series are Residual, Limit. Observed displacements plots Vertical (px) against Horizontal (px). Its series are Matches, Fitted.

The default record is Accepted correspondence fraction: 0.65 1; Translation error: 0.00983041 px; True-outlier acceptance rate: 0 1. These computed values are a worked example for these settings, not acceptance limits for every experiment. Keep parameter values and units beside the result. A near-zero residual has meaning only in relation to the stated model and numerical precision.

## Two one-variable sweeps

1. Increase outlier fraction at a fixed threshold. Track support, actual translation error and false acceptance together; explain why a spread-out wrong-match distribution can remain rejectable even at high contamination.

2. Sweep residual threshold at a fixed outlier fraction. Identify the tradeoff between discarding genuine noisy matches and admitting wrong ones; do not use accepted fraction alone as the success criterion.

Return to defaults between sweeps. Hold the other control fixed and record both a changing output and an expected invariant. Explain the physical or numerical path from the selected input to the observed response.

## Intentionally broken case

The estimator replaces exhaustive consensus and inlier refitting with least squares over every observed displacement. The selected threshold remains active for evaluation.

Run the same parameter values with the fault enabled. Compare complete curves as well as summary metrics. Identify the actual operation that changed and calculate why it affects the measured result. A changed warning label is not numerical evidence.

## Recovery

Restore consensus on the same data, then reconstruct the translation from the actual accepted displacements and inspect residuals on both genuine and wrong matches.

Repeat a saved nominal setting and confirm that its values and curves return. Recovery must restore the governing mechanism and its evidence, not merely clear a warning.

## Alternative and limiting cases

The fitted motion is a two-dimensional translation and the search is exhaustive, not random RANSAC or general epipolar estimation. Zero outliers can hide the selection fault. Coherent wrong clusters, model mismatch and threshold choice can defeat consensus; the synthetic contamination fraction alone does not define a guarantee.

## Independent evidence and MATLAB-style design boundary

The reference computes an all-pairs displacement-distance matrix to score hypotheses and uses a separate least-squares refit on the resulting mask. It independently checks the transform, residuals, labels and accepted set.

Five retained cases cover baseline, two single-control sweeps, the named fault and recovery. Expected values come from the independent formulation; actual values come from the executable lesson. Absolute and relative comparison tolerances remain 1e-8. Full-state or geometric checks supplement these three-number signatures, which alone cannot establish correctness. MATLAB has not been executed and no MATLAB equivalence is claimed. Browser and container evidence is recorded separately. Agreement between synthetic implementations does not establish empirical model validity.

## Engineering review checklist

Reconstruct one displayed quantity from the actual state or geometric arrays. Check coordinate ordering, signs and units before comparing numbers. Explain which assumption each check constrains, and identify a defect that another check could miss. Preserve the baseline, one controlled sweep, fault and recovery as a reproducible evidence sequence. State the model boundary before making a broader engineering recommendation.

## Common mistakes

Do not infer correctness from a changing headline alone. The fitted motion is a two-dimensional translation and the search is exhaustive, not random RANSAC or general epipolar estimation.

Do not change both sliders at once and attribute the result to one cause. Separate a model assumption from a measured property, and a finite-horizon observation from a universal guarantee. Floating-point roundoff is not a physical effect; equally, an attractive plot is not a substitute for the governing calculation.

## Focused check and teach-back

Why is a large consensus insufficient to prove that the recovered image motion is correct?

Answer rationale: A wrong but coherent group can be larger than the genuine group, and an overly broad threshold can count incompatible displacements as support. Inspect the model family, residuals and independent truth or validation, not just the accepted fraction.

Use the embedded Course checkpoint to explain your default, sweep, fault and recovery records to a colleague. Include one calculation with units, the causal diagnosis and an explicit untested boundary. This is a self-assessment; no learner score is stored.
