# Capstone: Verify a Faulted Software-HIL GNC Loop

**Guiding question:** Does the integrated software-HIL loop meet traced timing, fault-response, and pass/fail requirements without claiming physical hardware?

Run deterministic timing and packet-fault accounting, exercise a fail-zero watchdog, and retain a requirements verdict plus physical-gap statement. This is a Python-first native design derived from the reviewed competency map. It is not presented as a conversion of the pinned MATLAB source and it stays inside deterministic software simulation.

## Why this lesson exists

The numerical result is not the objective by itself. The objective is to connect a design decision to a governing relation, an observable consequence, a failure mechanism, and a recovery check. Record the assumptions before interpreting any curve.

## Model and equations

$$\text{age=t_now-t_source}$$
$$\text{watchdog if age>deadline}$$
$$\text{pass=timing and tracking and fault-response requirements}$$

Carry units through the model. A pole or zero is reported in inverse seconds, angular frequency in radians per second, phase in degrees or radians as labeled, and dimensionless ratios as `1`. The experiment evaluates the displayed equations directly; it does not call a black-box synthesis toolbox.

## Predict before running

A software-HIL pass requires every named timing and fault-response requirement to pass; physical I/O and real-time scheduling remain an explicit evidence gap. State which output should move first and which quantity should remain invariant before changing a control.

## Baseline workflow

1. Run the defaults with broken mode disabled and read all three signature metrics.
2. Inspect the response plot for the external behavior, then the mechanism plot for the governing internal relation.
3. Check the units and limiting cases before accepting a stability, equivalence, or performance statement.
4. Save the baseline, change one variable only, and explain the direction of change from the equations.

## Requirements trace

- `TIME-1`: the deterministic one-way transport must stay within the `30 ms` deadline, giving zero deadline-miss fraction in the nominal case.
- `LOSS-1`: the injected packet-drop fraction must remain below `0.2` for the nominal pass envelope.
- `SAFE-1`: every injected drop or stale-packet event must produce at least the corresponding fail-zero watchdog activation; broken mode deliberately suppresses it.

`requirements_passed` is the conjunction of all three checks. The `80 ms` latency sweep fails `TIME-1`; the `0.5` drop sweep fails `LOSS-1`; broken mode also fails `SAFE-1`. Passing this deterministic software loop does not supply physical I/O timing, scheduler jitter, actuator, electromagnetic, or environmental evidence.

## Two one-variable sweeps

1. Hold `packet_drop_fraction` at `0.05 1` and sweep `one_way_latency_ms` from `0.0` through `12.0` to `80.0 ms`.
2. Restore `one_way_latency_ms` to `12.0 ms` and sweep `packet_drop_fraction` from `0.0` through `0.05` to `0.5 1`.

Do not tune both at once until you can attribute each metric change to one term in the equations. The retained evidence uses one endpoint from each sweep in addition to the baseline.

## Intentionally broken case

Broken mode holds the last command through stale/drop intervals and suppresses the watchdog, violating fail-zero behavior. Broken mode is a named counterexample, not an alternative design recommendation.

## Recovery

Restore timestamp checks and fail-zero watchdog, rerun the deterministic fault schedule, and retain the physical-HIL gap. The recovery case restores the exact baseline inputs so the evidence can prove that the failure is reversible rather than merely different.

## Limiting cases and invariants

- At zero latency and zero drops the software transport adds no age fault.
- A dropped packet changes command age; it does not by itself define the safe actuator action.

Teaching invariant: A software-HIL pass requires every named timing and fault-response requirement to pass; physical I/O and real-time scheduling remain an explicit evidence gap.

## Independent evidence

Expected signatures are produced by `expansion_reference_cases.py`, which imports no production experiment and consumes no production result. Production signatures are retained separately. Each baseline, two sweeps, broken case, and recovery case records fields, units, tolerances, measured error, and the named invariant. Agreement supports only these equations and scenarios; it is not MATLAB execution, broad robust certification, or physical validation.

## Common mistakes

- Reading a plotted shape without checking its sign convention, units, or contour/path definition.
- Treating a local, frequency-limited, or nominal result as a global guarantee.
- Changing both design controls and then assigning causality to one of them.
- Confusing a recovery that looks better with a recovery that restores the baseline invariant.
- Claiming source equivalence, physical hardware evidence, or learner effectiveness from this software-only lab.

## Teach-back

Derive one signature quantity from the displayed equations, explain what the broken case violates, and name one result that this lab cannot establish. Then describe how the two sweeps separate sensitivity to `one_way_latency_ms` from sensitivity to `packet_drop_fraction`.
