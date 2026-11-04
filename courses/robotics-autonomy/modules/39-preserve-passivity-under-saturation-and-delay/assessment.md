# P39 course checkpoint

## Predict and derive

Audit the energy tank when saturation and delayed commands occur.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `work_k=F_applied,k*v_k*dt; E_next=E-work_k`
- `F_requested=-900*x_delayed-0.4*v_delayed`
- `positive_work_applied=min(positive_work_requested,E_available)`

## Controlled comparison

- `round_trip_delay_ms`: 18.0 → 120.0. Hold the other controls at baseline and explain the mechanism before executing.
- `force_limit_n`: 25.0 → 80.0. Hold the other controls at baseline and explain the mechanism before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

Applied work, not requested work, must be charged to the tank; a nonnegative energy record requires actual command limiting.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

A discrete tank model is not a physical passivity certificate.

Competency links: PHYSICAL-INTERACTION, REALTIME-SAFETY. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.


# Retained scoped evidence task

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
