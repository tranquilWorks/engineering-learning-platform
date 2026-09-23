# Replay, diagnose, and recover a timed robot system

A robot log is useful only when it preserves enough semantics to reproduce decisions. Bytes in a stable file format do not establish causality if source timestamps are missing, clock domains are confused, or arrival order replaces measurement order. This laboratory generates a bounded timed trajectory, removes a sensor interval, applies a drifting remote clock and deterministic delivery jitter, then compares causal source-time replay with a plausible but broken arrival-time playback.

## Model, derivation, and conventions

The reference position is `x(t)=sin(1.4t)` metres and velocity is its analytic derivative. Source samples occur every `20 ms`. A selectable interval beginning at `0.8 s` removes measurements. Remote timestamps scale source time by `1+drift`, while arrival time adds deterministic sinusoidal transport jitter. Source time, remote time, and arrival time are deliberately distinct fields.

Nominal replay advances `x_hat` with the last valid velocity and the fixed source-time increment. Available measurements blend into the estimate. When time since the last measurement exceeds `60 ms`, the diagnostic enters a safe hold and restores state from the next retained measurement checkpoint. Drift above `150 ppm` adds a separate clock fault. Replay error is RMS position difference over the source-time trace.

Broken replay sorts events by arrival, integrates nonnegative arrival deltas, weakly blends measurements, and never declares the missing source interval. It remains deterministic because jitter is deterministic, but it no longer reproduces source causality.

## Predict before running

Predict one dropout fault in the baseline and a short recovery latency at the next valid sample. RMS error should remain small because the estimator resets after the gap. Doubling dropout duration alone should increase propagation error before the checkpoint, even though recovery still occurs. Increasing clock drift alone past the review threshold should add a second diagnosed fault.

For broken replay, expect no diagnosed faults because the detector is absent. That zero is not good news. Arrival jitter changes event order and integration intervals, so RMS error rises. Recovery latency is represented by a large sentinel because the system never establishes a certified recovery.

## Baseline workflow

Run with `120 ms` dropout and `50 ppm` drift. In the state plot, compare the replay with the sinusoidal reference through the missing interval. The replay propagates temporarily, then snaps to the retained checkpoint. Confirm one diagnosed timing fault and `20 ms` recovery latency.

Inspect the remote-clock residual. At this short duration and modest drift, it remains below the displayed review limit. The plot is not a clock-synchronization proof; it shows the deterministic relation present in this fixture. The state error and timing diagnostics should be interpreted together because a small state error can occur by chance during a slow trajectory even when causality is wrong.

## Two one-variable sweeps

For sweep one, increase only dropout duration from `120` to `240 ms`. Sample period, clock drift, trajectory, update gain, and recovery rule remain unchanged. More samples are propagated without correction, so RMS error should increase. Fault count remains one because one contiguous interval disappeared.

For sweep two, restore dropout and increase only clock drift to `250 ppm`. The gap diagnosis still fires, and the clock audit adds a distinct fault. This distinction prevents one generic “timing problem” code from hiding whether data vanished or clocks diverged. A real recovery policy may tolerate one and stop on the other.

## Intentionally broken case

Broken mode replays delivery order. Network or middleware jitter can deliver a later source sample before an earlier one, so arrival order is not necessarily causal order. Clamping negative arrival deltas to zero makes the arithmetic finite while silently discarding elapsed dynamics. Weak measurement blending then masks discontinuities without correcting the state.

The broken trace is readable and repeatable, which makes it dangerous: a byte-identical rerun may still reconstruct the wrong history. Because it does not diagnose the source-time gap, it cannot prove safe hold or recovery. Logs intended for incident analysis must preserve original timestamps and the executive's fault decisions rather than recomputing them from arrival order alone.

## Recovery

Recover by recording monotonic source time, remote clock identity, arrival time, sequence number, schema version, and validity with each event. Sort or merge by source-time semantics, not file position alone. Detect missing intervals against the expected cadence. During a gap, propagate only within the declared uncertainty or enter safe hold. Resume from an explicit checkpoint and retain the transition as evidence.

For clock drift, estimate the mapping between domains and reject residual beyond policy. Never subtract timestamps from unrelated clocks without a mapping. Replaying commands also requires original saturation, scheduling, and fault-state data; otherwise the replay can invent behavior the robot never executed.

## Alternative and limiting cases

Event-sourced systems retain state transitions and rebuild materialized state. Rosbag-like archives retain typed messages and timestamps. Deterministic simulators can replay sensor streams against the same controller build. Distributed tracing adds causal spans across services. Hardware flight recorders may provide an independent monotonic clock and fail-safe event channel.

With no dropout and zero jitter, arrival and source order may coincide, so the broken method can appear correct. With constant velocity, integrating across a dropout can also look accurate; the sinusoid ensures changing dynamics. A log without timestamps cannot support causal replay. A very long dropout may exceed every checkpoint policy and must end in an unrecovered state rather than an optimistic reset.

## Independent evidence and MATLAB-style design boundary

The independent reference regenerates the analytic trajectory, missing interval, remote timestamps, deterministic arrival jitter, causal estimator, gap rule, drift rule, and broken arrival replay. It imports no production experiment, consumes no production result, and perturbs no production value. Five scenario signatures retain state error, fault count, and recovery latency.

No deployed robot log, middleware scheduler, network, MATLAB/Simulink data inspector, browser accessibility review, learner test, physical HIL, real-time operating system, safety case, or production incident was exercised. These results establish deterministic synthetic-log behavior only.

## Engineering review checklist

- Retain source, remote, and arrival timestamps without conflating them.
- Record clock identity, sequence, schema, validity, and software revision.
- Detect gaps against declared cadence and tolerance.
- Bound propagation uncertainty and define safe hold.
- Resume only from a retained valid checkpoint or measurement.
- Preserve original fault and recovery decisions in the log.
- Verify replay equality across repeated runs and software versions.
- Treat unreadable, stale, or cross-clock events as explicit failures.

## Common mistakes

Typical mistakes sort by file order, overwrite sensor time with receipt time, or use wall clocks that jump. Some replayers clamp negative time without reporting it, interpolate across faults, or recompute control with different saturation limits. A final-state match can hide a divergent intermediate trace. Another error counts zero diagnostics as evidence of health when the diagnostic itself never ran. Compression and serialization changes can also reorder events unless sequence semantics are retained.

## Focused check and teach-back

Define source time, remote time, and arrival time for one event. Explain why deterministic arrival-order playback can still be causally wrong. Then teach back the nominal response to a gap: detection, safe hold, checkpoint reset, and retained recovery transition. Predict which metric changes under longer dropout and which changes under larger clock drift. Finally, list the metadata required to reproduce a safety decision rather than merely redraw sensor values.
