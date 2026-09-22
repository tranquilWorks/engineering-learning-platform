# Capstone: Navigate, Guide, and Constrain an Autonomous Survey

**Guiding question:** Can navigation, path guidance, plant limits, and monitoring close an autonomous survey requirement set?

Combine dropout-driven navigation uncertainty, LOS cross-track behavior, turn-rate constraint, and a monitor alarm into an integrated survey verdict. This is a Python-first native design derived from the reviewed competency map. It is not presented as a conversion of the pinned MATLAB source and it stays inside deterministic software simulation.

## Why this lesson exists

The numerical result is not the objective by itself. The objective is to connect a design decision to a governing relation, an observable consequence, a failure mechanism, and a recovery check. Record the assumptions before interpreting any curve.

## Model and equations

$$\text{P_nav grows during GNSS dropout}$$
$$\text{chi_c=chi_path-atan(e_y/L)}$$
$$\text{|chi_dot|<=chi_dot_max and monitor residuals}$$

Carry units through the model. A pole or zero is reported in inverse seconds, angular frequency in radians per second, phase in degrees or radians as labeled, and dimensionless ratios as `1`. The experiment evaluates the displayed equations directly; it does not call a black-box synthesis toolbox.

## Predict before running

The survey passes only when navigation uncertainty, cross-track error, turn-rate constraint, and monitor response satisfy their separate requirements. State which output should move first and which quantity should remain invariant before changing a control.

## Baseline workflow

1. Run the defaults with broken mode disabled and read all three signature metrics.
2. Inspect the response plot for the external behavior, then the mechanism plot for the governing internal relation.
3. Check the units and limiting cases before accepting a stability, equivalence, or performance statement.
4. Save the baseline, change one variable only, and explain the direction of change from the equations.

## Requirements trace

- `NAV-1`: maximum cross-track error must remain below `10 m` throughout the declared GNSS-dropout family.
- `ACT-1`: applied turn rate must remain at or below the selected limit, so reported violation is exactly `0 deg/s`.
- `MON-1`: a dropout longer than `3 s` must raise the navigation monitor alarm.
- `SURVEY-PASS`: all three upstream requirements must pass; the diagnostic record exposes the conjunction instead of inferring success from one plot.

These are software-survey requirements only. They do not establish terrain clearance, perception safety, flight worthiness, or physical vehicle performance.

## Two one-variable sweeps

1. Hold `turn_rate_limit_deg_s` at `12.0 deg/s` and sweep `gnss_dropout_s` from `0.0` through `4.0` to `20.0 s`.
2. Restore `gnss_dropout_s` to `4.0 s` and sweep `turn_rate_limit_deg_s` from `3.0` through `12.0` to `30.0 deg/s`.

Do not tune both at once until you can attribute each metric change to one term in the equations. The retained evidence uses one endpoint from each sweep in addition to the baseline.

## Intentionally broken case

Broken mode disables the monitor and commands unconstrained turns during the longest dropout. Broken mode is a named counterexample, not an alternative design recommendation.

## Recovery

Restore uncertainty-aware guidance, enforce the turn-rate limit, and require the monitor to alarm on the injected dropout fault. The recovery case restores the exact baseline inputs so the evidence can prove that the failure is reversible rather than merely different.

## Limiting cases and invariants

- At zero dropout navigation covariance does not accumulate outage growth.
- Applied turn rate never exceeds its declared limit in the constrained case.

Teaching invariant: The survey passes only when navigation uncertainty, cross-track error, turn-rate constraint, and monitor response satisfy their separate requirements.

## Independent evidence

Expected signatures are produced by `expansion_reference_cases.py`, which imports no production experiment and consumes no production result. Production signatures are retained separately. Each baseline, two sweeps, broken case, and recovery case records fields, units, tolerances, measured error, and the named invariant. Agreement supports only these equations and scenarios; it is not MATLAB execution, broad robust certification, or physical validation.

## Common mistakes

- Reading a plotted shape without checking its sign convention, units, or contour/path definition.
- Treating a local, frequency-limited, or nominal result as a global guarantee.
- Changing both design controls and then assigning causality to one of them.
- Confusing a recovery that looks better with a recovery that restores the baseline invariant.
- Claiming source equivalence, physical hardware evidence, or learner effectiveness from this software-only lab.

## Teach-back

Derive one signature quantity from the displayed equations, explain what the broken case violates, and name one result that this lab cannot establish. Then describe how the two sweeps separate sensitivity to `gnss_dropout_s` from sensitivity to `turn_rate_limit_deg_s`.
