## P56 evidence task

Why must the final smoother covariance equal the filter covariance, and why is a fixed 35 percent improvement incorrect?

Before running: Predict which sample cannot benefit from the backward pass, and whether smaller model covariance guarantees smaller error in every realization.

Collect the default result, one single-control sweep, the named fault and recovery. Record controls and units beside the evidence.

Executed estimates plots Position (m) against Time (s). Its series are Synthetic truth, Forward filter, Reported smoother. Filter/smoother covariance plots Position variance (m²) against Time (s). Its series are Filtered covariance, Reported smoothed covariance.

### Reasoning rubric

- Model: use `x[k+1]=x[k]+w[k]; y[k]=x[k]+v[k]; Q=q m²; R=r m²` to reconstruct a quantity from the executed mechanism.
- Evidence: Increase process variance from 0.08 to 0.5 m² while holding measurement variance at 0.4 m². Compare the entire forward and backward variance curves; large process uncertainty weakens the coupling between adjacent states.
- Diagnosis: Broken mode skips the backward recursion and reports the forward filter as the smoother. Both controls still generate the data and filter covariance.
- Recovery and scope: Disable the fault and reset the two variances. Confirm the last means and variances remain equal while earlier covariance usually falls. State this limit: At the final sample no future measurement exists, so filter and smoother coincide. Positive q and r maintain positive covariance. A smoother uses a completed record and is not causal real-time estimation. Model covariance and realized RMSE answer different questions.

### Check your explanation

The backward recursion is initialized by the final filtered pair. Earlier reductions depend on the retained covariance ratios and future observations; no universal percentage follows. A lower posterior covariance describes the model distribution, not guaranteed improvement for every observed truth trace.

A complete answer includes the calculation or geometric construction, an observed comparison with units, fault/recovery evidence and the stated limitation. This is a self-assessment; no learner score is stored.
