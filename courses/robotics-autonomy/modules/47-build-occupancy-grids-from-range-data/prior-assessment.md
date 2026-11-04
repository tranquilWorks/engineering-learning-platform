## P47 evidence task

Why should the endpoint-only fault be described as missing free-space evidence rather than creating false-free cells?

Before running: Predict what an endpoint-only mapper can know about the free cells crossed by a beam, and distinguish unknown space from a false occupied measurement.

Collect a default record, one single-control sweep, the named fault and recovery. Record the parameter values, plotted quantities and units so another learner can reproduce the comparison.

Occupancy probability plots World y (m) against World x (m). Its series are Map, Hits. Central grid section plots Occupancy (1) against World x (m). Its series are Prob., Truth.

### Reasoning rubric

- Model: reconstruct a displayed value using `log_odds_next=clip(log_odds+inverse_sensor_evidence,-5,5)` and the actual state or geometry.
- Evidence: Increase the inverse-model hit probability at a fixed beam count. Reconstruct one hit and one free log-odds update, then inspect entropy and the unconfirmed-free fraction without treating stronger confidence as new independent data.
- Diagnosis: The mapper records occupied endpoints but skips the free cells that each ray actually traversed. It preserves beam geometry and evidence strength.
- Recovery and scope: Restore free-cell evidence, reset the prior grid and replay the same beams. Check whole probability rows and ray paths as well as aggregate entropy. State this boundary: Unobserved and occluded cells retain their prior; the unconfirmed-free fraction deliberately includes them and should not be read as a visible-cell false-positive rate. Known sensor pose, deterministic ranges, independent-cell updates and repeated-ray evidence are simplifying assumptions. Marginal entropy reduction does not prove calibrated joint uncertainty.

### Check your explanation

Its omitted negative updates leave crossed free cells at the 0.5 prior. They remain unknown; the algorithm has not asserted that occupied cells are free. The metric must describe the posterior that was actually produced.

A complete explanation contains a calculation, an observed comparison with units, the executed fault and a reproduced recovery. Name a setting that can hide the fault and a claim requiring evidence outside this model. This is a self-assessment; no learner score is stored.
