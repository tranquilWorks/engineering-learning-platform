# Model Sensor and Actuator Dynamics

**Guiding question:** What inputs, observable effects, and failure modes matter when you model Sensor and Actuator Dynamics?

Separate actuator lag, sensor lag, clipping, and bias in one command chain. This native lab preserves the source experiment while making the levers, diagnostics, and recovery available directly in the learning platform.

## Predict before running

When command reversals are faster than either bandwidth, measured output should lag twice. Write down the mechanism you expect—not only the trace direction—before moving a control.

## Model and equations

- $$\tau_a\dot u_a+u_a=u_c$$ — The actuator filters and clips command.
- $$\tau_s\dot y_s+y_s=u_a+b_s$$ — The sensor adds its own lag and bias.

The GUI evaluates these equations deterministically. Read the metric cards and both plots together: a pleasing response can still conceal poor authority, weak conditioning, stale data, or invalid assumptions.

## Two one-variable sweeps

1. Sweep `actuator_time_constant_s` through [0.05, 0.2, 0.8]. Hold every other control fixed and explain the causal chain from equation to trace to metric.
2. Sweep `sensor_time_constant_s` through [0.05, 0.1, 0.6]. Compare the changed mechanism plot with your first prediction.

Do not tune both levers at once until you can identify which term each lever changes.

## Intentionally broken case

The broken case combines slow actuator/sensor dynamics with a command that reverses every 0.1 s. Predict the signature before enabling **broken mode**.

## Recovery

Disable the broken case and slow the command or increase component bandwidth. A recovery is complete only when you can name the failed assumption and point to the metric or trace that confirms it.

## Common mistakes

- Treating a simulation trace as proof about hardware or production behavior.
- Changing multiple controls at once and losing causal attribution.
- Reading only the final value while ignoring transient effort, conditioning, delay, or saturation.
- Hiding a failed assumption by retuning instead of reproducing and explaining it.

## Teach-back

In two minutes: state the governing equation, explain what each live lever changes, identify the broken assumption, and justify the recovery with one visible metric and one plot feature.

---

## Source lesson (retained and polished into this GUI)

# P23 lesson: Model Sensor and Actuator Dynamics

## Guiding question

What inputs, observable effects, and failure modes matter when you model Sensor and Actuator Dynamics?

## Compounds on P22

P22 turned relative position and line-of-sight rate into a lateral-acceleration request, then clipped that
request to idealized acceleration authority. P23 makes the next boundary explicit: a guidance request is an
input to an actuator, the actuator's applied motion is an input to a sensor, and the sensor report can lag
or differ from both. This module does not rerun the P22 engagement or claim an autopilot.

## Mental model and visible equations

Think of the actuator and sensor as two memories in series. Over a held-input interval, each time constant
decides how much old state remains:

```text
u_limited = clip(u, -a_max, +a_max)                 [m/s^2]
tau_a * da/dt + a = u_limited                       [s, m/s^2]
tau_s * dy/dt + y = a                               [s, m/s^2]
y_reported = y + bias                               [m/s^2]
alpha = exp(-dt/tau)                                [dimensionless]
```

A larger time constant makes `alpha` closer to one, preserving more old state. The exact source recurrence
keeps the governing operation visible and handles zero time constants as ideal devices. Equal positive
time constants use the finite repeated-pole limit rather than dividing by nearly zero.

## What the baseline reveals

The request alternates between `+20` and `-20 m/s^2` every `2 s`. With actuator `tau_a=0.2 s` and sensor
`tau_s=0.1 s`, applied acceleration moves first and the sensor report follows. Neither device changes
instantly; after each reversal there is a visible interval where stored state still has the old sign.

The baseline `30 m/s^2` limit is inactive and bias is zero, so the plots isolate dynamic lag. At the final
sample before the first reversal, applied and measured acceleration are about `19.9990` and `19.9980
m/s^2`; these values follow the independent constant-step equations, not a plotted-curve guess.

## Two isolated levers

- Increasing sensor `tau_s` changes measurement lag and sensor RMS error but cannot change the upstream
  command or actual actuator history. If actual motion changes during this sweep, the implementation has
  coupled the wrong states.
- Increasing actuator `tau_a` changes request-to-applied error and downstream measurement. It cannot change
  the request itself. A sensor cannot report motion the actuator never produced.

Magnitude limit and bias are different mechanisms. Saturation clips the actuator input before dynamics;
bias adds a static offset after sensor dynamics. Calling every mismatch “lag” hides those distinctions.

## Broken bandwidth-separation case

The baseline allows many actuator and sensor time constants within one command plateau. The broken case
reverses the request every `0.1 s` while `tau_a=0.8 s` and `tau_s=0.6 s`. The request changes faster than
either device can settle: actual peak collapses below `3 m/s^2`, measured peak remains below `1 m/s^2`,
and the sensor can report the previous sign after the command reverses.

This is not numerical instability—the exact recurrence remains finite and bounded. It is a recognizable
bandwidth mismatch caused by an input time scale that violates the assumed separation from device dynamics.

## Misconceptions to correct directly

- Requested, limited, applied, sensed, and reported acceleration are different signals.
- A sensor time constant cannot change actual actuator motion in this feed-forward cascade.
- A larger time constant means slower response, not a larger final value for a constant bounded input.
- Saturation is a magnitude constraint; lag is stored dynamic state; bias is a static reporting offset.
- A stale signal can have the wrong sign even when every equation is stable and correctly implemented.
- Exact zero-order-hold arithmetic is still a model, not identified hardware dynamics.
- Static and independent Python simulation evidence do not prove MATLAB execution or rendered UI behavior.
- No bench, HIL, field, calibration, timing, fault-tolerance, or production evidence was produced.

Ask one observation question at a time. Request the teach-back only after executable checks pass.

## Source walkthrough

# P23 walkthrough: Model Sensor and Actuator Dynamics

## Learner sequence

1. Read the guiding question and P22 connection before running code.
2. Predict only which signal changes sign last after a baseline command reversal.
3. Visualize request, applied acceleration, and measured acceleration in `m/s^2`. Name their order without
   explaining it yet.
4. Visualize request-minus-applied and applied-minus-sensed errors. Identify where each error peaks.
5. Read the two first-order equations and connect each visible delay to its stored state and time constant.
6. Sweep only sensor time constant `[0 0.02 0.05 0.1 0.2 0.4] s`. Verify that command and actual actuator
   histories do not move while measurement error and stale-sign duration change.
7. Explain the changed view from `alpha_s=exp(-dt/tau_s)`, not from MATLAB plotting mechanics.
8. Reset sensor `tau_s=0.1 s`, then sweep only actuator time constant `[0 0.05 0.1 0.2 0.4 0.8] s`.
   Compare request-to-applied RMS error, peak applied acceleration, and downstream stale-sign time.
9. Explain why a sensor cannot report motion the actuator did not produce. Then distinguish time constant,
   magnitude limit, and sensor bias by the signal boundary each affects.
10. Run the broken `0.1 s` reversal case with actuator `tau_a=0.8 s` and sensor `tau_s=0.6 s`. Identify
    attenuated peaks and opposite-sign intervals, name the violated bandwidth-separation assumption, and
    restore the exact baseline.
11. Run `run_module_checks("P23")`, answer one interpretation prompt at a time, and give the required
    two-sentence teach-back.

No MATLAB-runtime, rendered-UI, calibration, actuator-characterization, bench, HIL, field, or physical
evidence is claimed by this walkthrough.

## Source checks

# P23 checks: Model Sensor and Actuator Dynamics

Run `run_module_checks("P23")`, then answer one prompt at a time:

1. Which inputs define command timing, actuator dynamics and authority, sensor dynamics and bias, and the
   bounded simulation grid? Include units.
2. Why does increasing sensor time constant leave the actual actuator history exactly unchanged?
3. Why does increasing actuator time constant affect both actual and measured acceleration but not the
   requested history?
4. How can you distinguish actuator saturation, dynamic lag, and sensor bias from their visible symptoms?
5. What does the zero-time-constant limit mean, and why does the equal-time-constant case need a finite
   repeated-pole expression?
6. In the broken case, why can measured acceleration retain the wrong sign even though the recurrence is
   stable and bounded?
7. What identification, calibration, timing, fault, bench, HIL, and field evidence is still required before
   using this model as a physical sensor or actuator claim?

## Teach-back

In exactly two sentences, name command half-period, actuator time constant, actuator limit, sensor time
constant, and sensor bias. Then explain how the two stored states create request-to-motion and
motion-to-measurement lag, and why fast reversals break the bandwidth-separation assumption.

The source and independent oracle provide static and simulated evidence only. No MATLAB-runtime,
rendered-UI, MATLAB numerical-fidelity, bench, HIL, field, or production validation is claimed.
