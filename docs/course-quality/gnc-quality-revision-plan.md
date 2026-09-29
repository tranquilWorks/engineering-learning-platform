# Controls/GNC quality revision: twelve existing lessons

Contract ELP-GNC-SEMANTIC-QUALITY-12 was merged in Portfolio Control PR551 at
6d81736bba58cc05f6ccc78e4a3ad66386d731bb. The exact target baseline is PR54 merge
00983cab0599b1ce3a613a2cc8ef42eb7b45f0b4. This batch changes no inventory or
prerequisite edges and preserves all DSP, Robotics and Vehicle payloads.

| Lesson | Repair | Independent method |
| --- | --- | --- |
| P36 | Full position/velocity feedback acceleration; separately dimensioned gains | Polynomial/DC coefficients and analytic state derivatives |
| P38 | Declared-cost CARE and actual augmented plant/observer history | Closed-form double-integrator CARE and observer polynomial |
| P42 | Actual integral peak, bounded manual command and censored recovery | Piecewise-affine sampled transitions |
| P43 | Integrated double-well phase portrait and energy/work balance | Implicit Radau versus explicit DOP853 |
| P45 | Barrier filter reevaluated at each state | Linear/geometric closed-form sampled trajectory |
| P46 | Real gain table, interpolation and measured grid error | Independent secant interpolation |
| P47 | Nonlinear residual dynamics with explicit departure event | Reciprocal-state solution and analytic event time |
| P48 | Declared uncertainty interval and dimensionless sensitivity | Independent complex transfer evaluation |
| P49 | Constrained horizon optimization and receding-horizon application | Scalar Bellman/Riccati policy and KKT/feasibility checks |
| P50 | Excitation, actual ARX fit and separate free-run validation | Convolution and two-column normal equations |
| P51 | Actual RLS estimate/gain/covariance updates | Weighted batch information calculation |
| P55 | Actual sigma points and transformed moments; accurate component title | Gaussian moments and missing-correction identity |

Every selected lesson has an individually authored Course checkpoint, model
explanation, worked example, two sweeps, fault/recovery, limits and answer rationale.
P55 keeps its stable route while its visible title states the actual unscented
transform scope. Mean and covariance weights have different normalization rules.

Verification must retain five independent cases per lesson at absolute/relative
1e-8 tolerances, physical and negative checks, all control corners through the
unchanged runtime, 290 HTTP and 580 desktop/mobile pages, all 84 DSP and twelve
new Controls checkpoints, and actual control/fault/recovery/reset with drawn plots.
Run contract, quick and full sequentially after browser work finishes. Record
failed attempts; do not infer concurrent capacity or learner outcomes.

The twelve selected findings closed after independent numerical and actual
browser checks passed. Forty-eight remain: Controls seven, Robotics twenty-five
and Vehicle sixteen; all three aggregate reviews stay blocked. No MATLAB,
manual screen-reader, representative-learner, hardware or production acceptance.
