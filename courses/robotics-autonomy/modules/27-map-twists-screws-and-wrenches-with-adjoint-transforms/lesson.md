# Map Twists, Screws, and Wrenches with Adjoint Transforms

**Guiding question:** What assumptions and evidence make map twists, screws, and wrenches with adjoint transforms defensible?

Build a deterministic numerical laboratory to map twists, screws, and wrenches with adjoint transforms, expose its governing relation, and diagnose a named counterexample before recovery. This module is a Python-first native design authorized by the reviewed issue-440 competency map. It is not a conversion of the pinned MATLAB-oriented source course, and it remains deterministic software evidence.

## Why this lesson exists

Robotics failures often cross representation boundaries: geometry into velocity, images into pose, estimates into maps, plans into commands, or contact forces into actuator effort. A result is defensible only when those boundaries carry explicit frames, signs, units, timing, constraints, and uncertainty. This lesson therefore connects one design decision to a governing equation, an observable response, a named failure, and an exact recovery.

Before calculating, name the state, input, observation, and verdict. State which quantities are measured, which are modeled, and which are derived. A smooth curve is not evidence that a constraint was respected, an estimator was consistent, a path was collision free, or a contact remained passive.

## Model, derivation, and conventions

- $$V_a=Ad_T V_b$$
- $$F_a=Ad_T^{-T} F_b$$
- $$F^T V is frame invariant$$

Derive the first relation from the physical, geometric, probabilistic, or algorithmic definition. Use the second relation to propagate the decision into a measurable consequence. Use the third as an invariant, feasibility condition, or audit relation. Keep every coordinate frame and sampling instant attached until the final scalar metric. The experiment evaluates these relations directly with bounded NumPy arrays; it does not call a remote solver or hide the mechanism behind a black-box robotics stack.

The three retained signature quantities are:

- `power_invariance_error` (W)
- `adjoint_roundtrip_error` (1)
- `screw_pitch` (m/rad)

Carry units through each substitution. Dimensionless ranks, probabilities, ratios, and flags are labeled `1` or `count`; physical displacement, time, force, torque, energy, velocity, and pixel quantities retain their named units. If a sum combines unlike units or a transform maps a vector without a frame convention, stop before interpreting a number.

## Predict before running

A twist and its dual wrench must transform contragrediently so instantaneous power is frame invariant. Predict the sign and direction of all three signature changes before moving a slider. Identify the equation term responsible and one quantity that should remain invariant. This written prediction is the comparison point; post-hoc description is not the same as a test.

## Baseline workflow

1. Run the defaults with broken mode disabled and read the three signature metrics with units.
2. Inspect the response plot for task-level behavior, then the mechanism plot for the constraint, residual, energy, conditioning, or decision that explains it.
3. Reproduce one signature quantity from the displayed equations to one or two significant figures.
4. Check a limiting case before accepting the baseline.
5. Save the baseline parameters and signature so recovery can be tested exactly.

## Two one-variable sweeps

1. Hold `angular_speed_rad_s` at `1.8 rad/s` and sweep `lever_arm_m` from `0.05` through `0.45` to `1.5 m`.
2. Restore `lever_arm_m` to `0.45 m` and sweep `angular_speed_rad_s` from `0.1` through `1.8` to `6.0 rad/s`.

Change one variable at a time. For each endpoint, record the predicted direction, actual direction, metric delta, and the mechanism-plot feature that supports causality. If the result reverses direction, check for a branch, active constraint, singularity, gate, saturation, or feasibility transition rather than smoothing it away.

## Intentionally broken case

Broken mode applies the twist adjoint to the wrench, violating duality and changing computed power. Broken mode is a falsifying counterexample, not a recommended alternative. Explain which assumption is violated before describing the visual symptom. Then locate the first intermediate quantity that departs from the baseline invariant; downstream task error alone rarely identifies the cause.

## Recovery

Use the inverse-transpose wrench transform and verify an adjoint/inverse round trip plus equal power. Recovery is complete only when the original default inputs and diagnostic signature return within the independent-reference tolerance. A different setting that happens to look better is mitigation, not recovery. Preserve the fault, detection, decision, and recovery sequence as separate evidence.

## Alternative and limiting cases

- At zero lever arm, translation-rotation coupling vanishes.
- A pure rotation screw has zero pitch when axial translation is zero.

Use one limit as a hand calculation and one as a numerical sweep. Limits reveal whether a formula is continuous, singular, or branch-dependent. An undefined limit must be reported as such; clipping it into a convenient finite value changes the model.

## Independent evidence and MATLAB-style design boundary

The design was reasoned from the displayed equations in the same model-first workflow normally used before a MATLAB/Simulink implementation, but the delivered implementation is Python/NumPy only. Expected signatures are stored by `expansion_reference_cases.py`, which imports no production experiment, consumes no production result, and perturbs no production value. Production signatures are retained separately for baseline, both one-variable sweeps, broken, and exact recovery scenarios.

Agreement supports only the displayed model, input set, fields, units, and tolerances. No licensed MATLAB runtime was executed, so the evidence makes no MATLAB numerical-parity claim. It also does not establish global optimality, field robustness, physical calibration, hardware timing, safety certification, or production readiness.

## Engineering review checklist

- Verify equation dimensions, coordinate frames, signs, timestamp direction, and branch conventions.
- Separate feasibility or safety from objective value and visual smoothness.
- Inspect conditioning, covariance, clearance, saturation, energy, or data age when relevant.
- Confirm the broken case changes the named mechanism and the recovery restores the baseline signature.
- State one assumption whose violation would invalidate the result even if every test here passed.

## Common mistakes

- Treating a local or finite-sample result as a global guarantee.
- Changing both controls and assigning causality to only one.
- Accepting endpoint checks where swept geometry, intermediate dynamics, or data freshness matter.
- Confusing a low residual with observability, correct association, feasibility, or physical truth.
- Claiming learner effectiveness, MATLAB parity, physical HIL, hardware safety, or certification from software fixtures.

## Focused check and teach-back

Calculate one baseline signature value, show one dimensional check, predict both sweeps, reproduce the named failure, and demonstrate exact recovery. Then teach the lesson back without starting from the plots: state the convention, derive the governing relationship, explain the invariant, identify the practical failure, and name the evidence boundary. Finish by naming the prerequisite module and the next mapped module that consumes this artifact.
