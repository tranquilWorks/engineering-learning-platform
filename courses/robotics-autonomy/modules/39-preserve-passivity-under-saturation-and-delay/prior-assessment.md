## P39 evidence task

Why can a force remain within its actuator bound while violating the energy budget?

Before running: Predict why force saturation alone cannot guarantee that the accumulated port energy stays nonnegative.

Collect a default record, one single-control sweep, the named fault and recovery. Record the parameter values, plotted quantities and units so another learner can reproduce the comparison.

Port energy balance plots Energy (J) against Time (s). Its series are Tank, Zero. Requested and applied force plots Force (N) against Time (s). Its series are Requested, Applied.

### Reasoning rubric

- Model: reconstruct a displayed value using `work_k=F_applied,k*v_k*dt; E_next=E-work_k` and the actual state or geometry.
- Evidence: Increase delay at fixed force bound. Compare force phase, negative energy in bypass mode and actual removed work in normal mode. Avoid interpreting a monotonic delay slider as a proven stability threshold.
- Diagnosis: The fault bypasses the causal energy limiter while preserving the delayed request and saturation. The same actual-work update then reveals any reservoir deficit.
- Recovery and scope: Restore work limiting and compare applied force, sample work and every energy update. Verify conservation with the initial balance included. State this boundary: At a zero-velocity sample the port work is zero regardless of finite force. This is a prescribed-motion, sampled-work demonstration with ideal force application. It does not establish continuous-time passivity, a closed-loop delay margin or stability of a physical haptic system.

### Check your explanation

An amplitude bound limits each force value, whereas the budget limits accumulated force times velocity times sample duration. Repeated bounded positive work can exceed the initial energy; the causal work limiter must constrain the actual applied work.

A complete explanation contains a calculation, an observed comparison with units, the executed fault and a reproduced recovery. Name a setting that can hide the fault and a claim requiring evidence outside this model. This is a self-assessment; no learner score is stored.
