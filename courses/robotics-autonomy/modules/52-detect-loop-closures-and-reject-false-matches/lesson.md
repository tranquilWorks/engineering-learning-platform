# Detect Loop Closures and Reject False Matches

**Guiding question:** What independent evidence is required before a visually plausible revisit is allowed to constrain the pose graph?

Loop closure is unusually asymmetric. A correct closure can remove accumulated drift across an entire map; one false closure can fold distant corridors together and corrupt every downstream pose. Appearance retrieval is valuable because it searches a large history cheaply, but repeated structures, lighting changes, and perceptual aliasing make similarity a proposal mechanism—not geometric proof.

This laboratory keeps the stages separate. A descriptor score proposes a candidate. A geometric residual verifies whether the implied relative pose agrees with matched geometry. Only a candidate that passes both tests becomes a graph factor. A Huber-style influence weight then bounds the leverage of the accepted factor. Three reported quantities make the chain auditable: inserted closure weight, normalized robust cost, and induced map deformation.

## Model, derivation, and conventions

Let $s\in[0,1]$ be appearance similarity. A candidate is proposed when

$$s\ge s_{\min}=0.70.$$

Proposal says only that two observations look alike. The front end next estimates a relative transform from geometric correspondences and computes a translation residual $r_g$ in metres. The candidate is eligible for insertion only when

$$\|r_g\|\le r_{\max}=0.30\ \mathrm{m}.$$

For an inserted factor, normalize $u=r_g/r_{\max}$. The Huber influence weight is

$$w(u)=\frac{\psi(u)}{u}=\min\left(1,\frac{1}{|u|}\right),$$

with the continuous value $w(0)=1$. The effective closure weight reported by the lesson is $s\,w(u)$. Its robust cost is $\rho(u)=u^2/2$ for $|u|\le1$ and $|u|-1/2$ outside. Rejected candidates receive zero graph weight even though their diagnostic cost can still be displayed.

The map-deformation metric is a deliberately small surrogate proportional to inserted weight and residual. It is not a full graph reoptimization; P51 owns that mechanism. Here it makes the consequence of insertion visible while keeping the teaching focus on verification order. Descriptor similarity, weight, and normalized cost are dimensionless. Geometric residual and deformation are metres.

## Predict before running

At the baseline, $s=0.78$ passes the appearance threshold and $r_g=0.12$ m passes the 0.30 m geometric gate. Because the normalized residual is 0.4, Huber remains in its quadratic region and the geometric influence weight is one. Predict an inserted weight of 0.78 and small deformation.

Raising similarity to 1.0 while holding geometry fixed should increase inserted weight but should not change geometric cost. Raising residual to 2.0 m while restoring similarity to 0.78 should fail geometric verification. Predict zero insertion and zero map deformation even though the diagnostic robust cost for that rejected hypothesis is large.

## Baseline workflow

Run the default candidate and inspect the appearance plot. The controlled candidate is one of four scores; only its score changes. Identify every candidate above 0.70, but do not infer that all of them are valid loops. The plot intentionally shows why retrieval can produce multiple plausible locations.

Next inspect the influence plot. Up to 0.30 m, influence is one. Beyond the robust transition it decays as inverse residual, while the geometric gate drops eligibility to zero. These are separate curves: the robustifier describes what would happen to an accepted factor, and the gate describes whether the factor should exist at all.

Use the metrics to narrate the pipeline in order: appearance proposal, geometric pass, inserted weight, robust cost, deformation. If you start from map deformation alone, you cannot distinguish a correctly rejected loop from a loop that was never proposed.

## Two one-variable sweeps

For Sweep 1, hold residual at 0.12 m and move descriptor score from 0 through 0.78 to 1.0. Below 0.70, the candidate is not proposed and graph weight is zero. At the threshold, insertion changes discretely because geometry already passes. Above it, weight grows with score while robust cost remains unchanged. That discontinuity is a decision boundary, not numerical noise.

For Sweep 2, restore score to 0.78 and move geometric residual from 0 through 0.12 to 2.0 m. Inside the gate, the candidate can enter. Outside 0.30 m, it is rejected and deformation returns to zero. The robust diagnostic continues to grow only to illustrate how incompatible the proposed match was. Do not interpret a finite robust cost as permission to insert it.

## Intentionally broken case

Broken mode represents an appearance-only loop detector. It finds a high score of 0.95, skips geometric verification, inserts a contradictory 1.8 m closure, and applies full quadratic influence. The factor receives high weight precisely because the image looks convincing. Normalized cost becomes large and the deformation surrogate jumps by orders of magnitude.

This is perceptual aliasing: two distinct places share similar visual structure. Warehouses, office corridors, parking garages, and road intersections commonly create it. Once inserted, the false constraint can pull a local optimizer into a self-consistent but wrong configuration. A low residual after reoptimization would not retroactively validate the association because the map may have deformed to satisfy the bad factor.

## Recovery

Recovery reinstates independent geometric verification and the robust factor, then restores the exact baseline score and residual. Confirm that all signature fields return to baseline. Deleting the visibly bad map segment without repairing the acceptance policy is not recovery. Lowering all loop weights also is not recovery; it sacrifices good closures while leaving the same false-positive mechanism.

In a persistent SLAM system, recovery would quarantine the suspect factor, restore a pre-insertion checkpoint or reoptimize without it, and replay the acceptance evidence. This stateless lesson models the decision but not graph rollback.

## Alternative and limiting cases

At $r_g=0$, a verified candidate receives full geometric influence. At very large residual, Huber influence tends toward zero, but an appearance-only system can still insert the factor. At score exactly 0.70, the stated convention uses an inclusive threshold. Production code must specify this boundary to avoid inconsistent front-end behavior.

RANSAC inlier count, epipolar consistency, PnP reprojection error, scan-registration fitness, and covariance-aware pose residual are possible geometric tests. They are not interchangeable, but each should be based on evidence independent enough from the retrieval descriptor that the same alias does not pass both stages for the same reason.

## Independent evidence and MATLAB-style design boundary

The independent reference evaluates threshold decisions, normalized residual, Huber cost, and weight for the exact five scenarios without importing the production entrypoint. The production runtime separately generates plots and diagnostics. Expected and actual evidence remain distinct files.

No image database, feature extractor, RANSAC solver, MATLAB vision toolbox, ROS bag, or physical camera/lidar was used. The lesson validates decision logic, not real precision-recall, dataset generalization, map rollback, or safety. Appearance score and deformation are controlled surrogates, not field-calibrated quantities.

## Engineering review checklist

- Treat retrieval output as a hypothesis and retain the alternative candidates.
- Use a geometric verifier whose failure modes are not identical to the descriptor's.
- Declare score and residual thresholds, units, and inclusive/exclusive boundaries.
- Log the transform, inlier set, covariance, robust weight, and graph insertion decision.
- Test repeated structure, low texture, viewpoint change, and a known true revisit.
- Preserve a way to remove a suspect factor and replay optimization.

## Common mistakes

- Inserting the highest descriptor score directly into the graph.
- Using robust loss as the only false-loop defense.
- Evaluating loop quality only after the graph deforms to accommodate it.
- Reporting retrieval precision without geometric-verification precision.
- Tuning thresholds on the same route used for final evidence.
- Hiding rejected candidates, making false negatives impossible to diagnose.

## Focused check and teach-back

For the baseline, calculate normalized residual, Huber region, and inserted weight. For the 2 m sweep endpoint, explain why diagnostic cost is finite but graph weight is zero. Then describe the broken aliasing sequence from high appearance score to map deformation. Finish with the boundary: deterministic scalar decision evidence only; no real imagery, MATLAB, learner/accessibility validation, hardware HIL, certification, release, or production claim.
