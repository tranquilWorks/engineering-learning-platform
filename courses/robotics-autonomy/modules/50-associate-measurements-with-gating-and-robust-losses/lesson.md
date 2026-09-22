# Associate Measurements with Gating and Robust Losses

**Guiding question:** Why are covariance gating and robust loss complementary defenses rather than interchangeable tuning knobs?

A state estimator cannot update from a measurement until it decides what generated that measurement. In a cluttered scene, the nearest return in Euclidean distance may not be statistically compatible with the predicted feature. Even after a plausible association is selected, a modest modeling error can leave a residual larger than the Gaussian model expects. Gating addresses the first problem; robust loss addresses the second. Reversing their order or using one as a substitute for the other permits an outlier to influence the state before the estimator has established that it belongs to the track.

This laboratory uses two two-dimensional innovations. Candidate 1 is a fixed inlier at $[0.60,-0.40]$ standard deviations. Candidate 2 is an outlier whose magnitude is controlled by the learner. The covariance has already whitened both coordinates, so squared Euclidean length in this space is the squared Mahalanobis distance. That compact setup exposes the complete decision sequence without hiding it inside a tracking library.

## Model, derivation, and conventions

For predicted measurement $\hat z_j=h_j(\hat x^-)$, innovation and innovation covariance are

$$\nu_j=z_j-\hat z_j,\qquad S_j=H_jP^-H_j^T+R_j.$$

Whitening with $S_j^{-1/2}$ gives $r_j=S_j^{-1/2}\nu_j$. The compatibility statistic is

$$d_j^2=\nu_j^TS_j^{-1}\nu_j=r_j^Tr_j.$$

The association gate accepts candidate $j$ only when $d_j^2\le\gamma$. The slider is expressed as a radial sigma threshold, so the displayed squared threshold is $\gamma=(\text{gate sigma})^2$. Once a candidate passes the gate, its residual contributes through the Huber loss

$$
\rho(r)=\begin{cases}
\tfrac12r^2,&|r|\le\delta\\
\delta(|r|-\tfrac12\delta),&|r|>\delta,
\end{cases}
$$

with $\delta=1.5$. The influence $\psi(r)=d\rho/dr$ grows linearly near zero and saturates at $\delta$. Saturation limits how much an accepted but imperfect factor can steer the update. It does not make an incompatible correspondence correct.

All innovation components are in standard-deviation units after whitening. Mahalanobis distance, gate threshold, loss, and influence are dimensionless. The two candidate indices are counts. No raw metres or pixels are combined until their uncertainty has mapped them into the common whitened space.

## Predict before running

At the default gate of 3 sigma, Candidate 1 should pass because its squared distance is $0.60^2+(-0.40)^2=0.52$, well below 9. Candidate 2 at 5 sigma has a second component equal to 35 percent of its first, so its squared distance exceeds 25 and should fail. Therefore the accepted-inlier flag and rejected-outlier flag should both be one, while accepted cost should contain only the small inlier contribution.

Predict the wide-gate sweep before trying it. An 8-sigma gate can admit the 5-sigma outlier. The Huber loss will limit its marginal influence, but total accepted cost must still increase. Predict the outlier-magnitude sweep separately: with the 3-sigma gate restored, moving the outlier farther away should not increase accepted cost because the incompatible candidate remains rejected.

## Baseline workflow

Run the default case and calculate Candidate 1's $d^2$ by hand. On the response plot, compare each candidate with the horizontal threshold. The decision is made in squared-distance space; do not compare a squared distance directly with the unsquared gate slider.

Next inspect the influence curve. For residual magnitudes below 1.5 sigma, Huber is identical to quadratic least squares. Beyond 1.5, influence stays bounded. Read the three metrics in decision order: the known inlier is accepted, the outlier is rejected, and the reported cost sums only accepted candidates. This order matters because a robust cost evaluated on every nearby feature is not a data-association policy.

## Two one-variable sweeps

For Sweep 1, hold the outlier at 5 sigma and widen the gate from 0.5 through 3 to 8 sigma. A gate below the inlier magnitude rejects even the correct return; this is a false negative caused by overconfidence or an overly strict threshold. At 8 sigma, the outlier is admitted. Record the gate crossing and the increase in accepted robust cost.

For Sweep 2, restore the 3-sigma gate and vary the outlier from 0.5 through 5 to 12 sigma. At small magnitude, the second candidate can be statistically compatible, so rejecting it solely because it was labeled “outlier” would be cheating. At large magnitude, the gate should reject it regardless of the Huber delta. This sweep separates semantic ground truth from the evidence actually available to the estimator.

## Intentionally broken case

Broken mode sets a tight nominal gate but bypasses the comparison, accepts both candidates, and applies an unbounded quadratic cost. Its incompatible candidate is 11 sigma in the first whitened coordinate and 3.85 sigma in the second. The resulting cost is orders of magnitude larger than the inlier contribution, and the rejected-outlier flag becomes zero.

This models a common failure: a front end forwards the best descriptor match, and the optimizer assumes the match is already valid. A later robustifier cannot fully undo a state update that has already crossed into the wrong attraction basin. The broken plot shows influence continuing to grow with residual instead of saturating.

## Recovery

Recovery restores the baseline inputs and the decision pipeline: predict, whiten, gate, then robustly optimize accepted residuals. Verify exact return of all three signature fields. A wider gate that happens to converge is not recovery because it changes the statistical decision. A smaller Huber delta is not recovery because it treats the symptom after accepting the wrong source.

In an operational tracker, recovery should also clear or quarantine the corrupted association history, because state bias changes future predictions and gates. This deterministic lesson has no persistent state, so it demonstrates only one update's logic.

## Alternative and limiting cases

At zero innovation, $d^2=0$ and any positive gate accepts the candidate. At infinite covariance, a fixed raw residual can appear deceptively small after whitening; therefore covariance credibility is a prerequisite for meaningful gating. At zero covariance, even tiny raw errors become enormous, which signals overconfidence rather than perfect sensing.

Joint compatibility tests extend the scalar gate when several measurements compete for a common hypothesis. Nearest-neighbor, probabilistic data association, and multi-hypothesis tracking differ in how they manage competing hypotheses, but all still require explicit uncertainty and a rule for incompatible evidence.

## Independent evidence and MATLAB-style design boundary

Independent scenario evidence evaluates the closed-form distances, gate decisions, and Huber cost without importing or executing the production experiment. Production evidence separately records the learner-facing path. Both use the exact scenario parameters and units. Recovery repeats the baseline input rather than copying a prior output.

The laboratory is Python/NumPy only. No MATLAB tracking toolbox, ROS perception stack, camera, lidar, or field dataset was executed. Agreement proves the displayed two-candidate calculation, not a probability of correct association in a real environment, not covariance calibration, and not robustness to correlated clutter.

## Engineering review checklist

- Confirm innovation sign and coordinate order match the measurement Jacobian.
- Whiten with the full innovation covariance, including cross-correlation when present.
- Compare $d^2$ with a squared threshold and document the chosen probability level.
- Apply robust loss only after association eligibility is established.
- Log rejected candidates and gate values so false negatives are diagnosable.
- Test a correct inlier, a borderline candidate, a large outlier, and exact recovery.

## Common mistakes

- Gating raw Euclidean distance while ignoring anisotropic covariance.
- Comparing $d^2$ with a gate specified in sigma rather than sigma squared.
- Treating Huber or Cauchy loss as a substitute for correspondence verification.
- Tuning the gate on the same data used to claim performance.
- Forgetting that underestimated covariance rejects good measurements.
- Summing rejected residuals into the optimizer cost and calling them harmless diagnostics.

## Focused check and teach-back

Compute the inlier's squared Mahalanobis distance and state why it passes the default gate. Explain why the 5-sigma candidate is rejected before Huber is consulted. Then describe what changes under the 8-sigma sweep and why bounded influence does not certify the match. Finish with the claim boundary: deterministic software evidence for one whitened two-candidate update, with no MATLAB runtime, learner validation, browser accessibility test, or physical sensor experiment.
