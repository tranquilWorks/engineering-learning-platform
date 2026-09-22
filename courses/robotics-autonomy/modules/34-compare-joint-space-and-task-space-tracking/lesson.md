# Compare Joint-Space and Task-Space Tracking

**Guiding question:** What assumptions and evidence make compare joint-space and task-space tracking defensible?

Build a deterministic numerical laboratory to compare joint-space and task-space tracking, expose its governing relation, and diagnose a named counterexample before recovery. This module is a Python-first native design authorized by the reviewed issue-440 competency map. It is not a conversion of the pinned MATLAB-oriented source course, and it remains deterministic software evidence.

## Why this lesson exists

Robotics failures often cross representation boundaries: geometry into velocity, images into pose, estimates into maps, plans into commands, or contact forces into actuator effort. A result is defensible only when those boundaries carry explicit frames, signs, units, timing, constraints, and uncertainty. This lesson therefore connects one design decision to a governing equation, an observable response, a named failure, and an exact recovery.

Before calculating, name the state, input, observation, and verdict. State which quantities are measured, which are modeled, and which are derived. A smooth curve is not evidence that a constraint was respected, an estimator was consistent, a path was collision free, or a contact remained passive.

## Model, derivation, and conventions

- $$tau=-K_q(q-q_d)$$
- $$F=-K_x(x-x_d)$$
- $$tau=J^T F$$

Derive the first relation from the physical, geometric, probabilistic, or algorithmic definition. Use the second relation to propagate the decision into a measurable consequence. Use the third as an invariant, feasibility condition, or audit relation. Keep every coordinate frame and sampling instant attached until the final scalar metric. The experiment evaluates these relations directly with bounded NumPy arrays; it does not call a remote solver or hide the mechanism behind a black-box robotics stack.

The three retained signature quantities are:

- `joint_error` (rad)
- `task_error` (m)
- `control_effort` (N*m)

Carry units through each substitution. Dimensionless ranks, probabilities, ratios, and flags are labeled `1` or `count`; physical displacement, time, force, torque, energy, velocity, and pixel quantities retain their named units. If a sum combines unlike units or a transform maps a vector without a frame convention, stop before interpreting a number.

## Predict before running

Joint and task tracking optimize different errors; Jacobian conditioning determines how joint error maps into Cartesian error and effort. Predict the sign and direction of all three signature changes before moving a slider. Identify the equation term responsible and one quantity that should remain invariant. This written prediction is the comparison point; post-hoc description is not the same as a test.

## Baseline workflow

1. Run the defaults with broken mode disabled and read the three signature metrics with units.
2. Inspect the response plot for task-level behavior, then the mechanism plot for the constraint, residual, energy, conditioning, or decision that explains it.
3. Reproduce one signature quantity from the displayed equations to one or two significant figures.
4. Check a limiting case before accepting the baseline.
5. Save the baseline parameters and signature so recovery can be tested exactly.

## Two one-variable sweeps

1. Hold `joint_gain_per_s` at `3.0 1/s` and sweep `jacobian_condition` from `1.0` through `4.0` to `40.0 1`.
2. Restore `jacobian_condition` to `4.0 1` and sweep `joint_gain_per_s` from `0.2` through `3.0` to `10.0 1/s`.

Change one variable at a time. For each endpoint, record the predicted direction, actual direction, metric delta, and the mechanism-plot feature that supports causality. If the result reverses direction, check for a branch, active constraint, singularity, gate, saturation, or feasibility transition rather than smoothing it away.

## Intentionally broken case

Broken mode treats task error as joint error and omits the Jacobian transpose. Broken mode is a falsifying counterexample, not a recommended alternative. Explain which assumption is violated before describing the visual symptom. Then locate the first intermediate quantity that departs from the baseline invariant; downstream task error alone rarely identifies the cause.

## Recovery

Choose the controlled coordinate explicitly, restore the correct map, and inspect task error together with joint effort. Recovery is complete only when the original default inputs and diagnostic signature return within the independent-reference tolerance. A different setting that happens to look better is mitigation, not recovery. Preserve the fault, detection, decision, and recovery sequence as separate evidence.

## Alternative and limiting cases

- At identity Jacobian, equally scaled joint and task laws coincide.
- Near singularity, small task corrections can demand large joint motion or effort.

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
