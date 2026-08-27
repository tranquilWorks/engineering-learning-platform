# Close the Loop Through a Hardware-in-the-Loop Plant

**Guiding question:** What inputs, observable effects, and failure modes matter when you close the Loop Through a Hardware-in-the-Loop Plant?

Close a virtual controller/plant protocol loop with latency, drops, watchdog, and cancellation. This native lab preserves the source experiment while making the levers, diagnostics, and recovery available directly in the learning platform.

## Predict before running

Latency and dropped packets should increase command age; the watchdog must fail to zero rather than hold forever. Write down the mechanism you expect—not only the trace direction—before moving a control.

## Model and equations

- $$u_k=K_p(r-y_k)-K_d\dot y_k$$ — A sampled controller computes timestamped commands.
- $$u=0\;\text{if age}>T_w$$ — The virtual plant watchdog removes stale authority safely.

The GUI evaluates these equations deterministically. Read the metric cards and both plots together: a pleasing response can still conceal poor authority, weak conditioning, stale data, or invalid assumptions.

## Two one-variable sweeps

1. Sweep `controller_period_s` through [0.02, 0.05, 0.15]. Hold every other control fixed and explain the causal chain from equation to trace to metric.
2. Sweep `one_way_latency_s` through [0.0, 0.01, 0.06]. Compare the changed mechanism plot with your first prediction.

Do not tune both levers at once until you can identify which term each lever changes.

## Intentionally broken case

The broken case drops every second command with a 0.1 s controller period, 0.04 s one-way latency, and 0.12 s watchdog. Predict the signature before enabling **broken mode**.

## Recovery

Disable the broken case to restore fresh commands. This is a software-only virtual protocol/plant lesson; it does not claim physical HIL execution. A recovery is complete only when you can name the failed assumption and point to the metric or trace that confirms it.

## Common mistakes

- Treating a simulation trace as proof about hardware or production behavior.
- Changing multiple controls at once and losing causal attribution.
- Reading only the final value while ignoring transient effort, conditioning, delay, or saturation.
- Hiding a failed assumption by retuning instead of reproducing and explaining it.

## Teach-back

In two minutes: state the governing equation, explain what each live lever changes, identify the broken assumption, and justify the recovery with one visible metric and one plot feature.

---

## Source lesson (retained and polished into this GUI)

# P24 lesson: Close the Loop Through a Hardware-in-the-Loop Plant

## Guiding question

What inputs, observable effects, and failure modes matter when you close the Loop Through a Hardware-in-the-Loop Plant?

## Compounds on P23

P23 showed that requested, limited, applied, sensed, and reported motion are different signals. P24 retains
that boundary and asks what happens when the controller and plant side exchange those values as timestamped
messages. A mathematically correct controller can still act on an old measurement; a correct plant can
still hold an old command; a receiver can deliberately replace stale input with safe zero.

P10 already distinguished sample spacing from computation delay. P24 compounds that idea into two
transport directions, explicit timestamps, loss, watchdog state, cancellation ordering, and a mechanical
plant that never pauses for software.

## Visible equations and event order

The virtual plant is a mass `m` with viscous damping `c=1.2 N*s/m`:

```text
x_dot = v
m*v_dot = u_applied - c*v
u_request = clip(Kp*(r-x_measured) - Kd*v_measured, -u_max, +u_max)
Kp = 18 N/m, Kd = 8 N*s/m, u_max = 30 N
```

For a held force during one plant tick `dt`, `a=exp(-c*dt/m)` and the source evaluates

```text
v_next = a*v + (1-a)*u/c
x_next = x + (m/c)*(1-a)*v + (dt/c - m*(1-a)/c^2)*u
```

At each integer tick the model evaluates cancellation first; a cancellation invalidates queued work before
anything can arrive at that same timestamp. Otherwise the plant enqueues a measurement on a controller
release, delivers any measurement due now, computes from the newest delivered timestamp, enqueues or drops
the command, delivers any command due now, evaluates command age, and then propagates the plant. This order
makes zero latency a genuine same-tick limit and makes the safety precedence testable.

## What the baseline reveals

The position plot answers whether the loop tracks. The protocol view answers why: measurement age shows
how old the controller's information is, controller force shows what software requested, and applied force
shows what crossed the plant-side boundary after latency and watchdog logic.

The controller period `T_c`, one-way latency `L`, watchdog timeout `T_w`, command-drop schedule, cancel time,
plant mass, plant tick, and virtual duration are inputs. Observable effects include timestamp age, packet
counts, tracking error, peak position and velocity, requested versus applied force, and watchdog duration.

## Two isolated levers

- Increasing only `L` moves measurement and command deliveries later. It does not change controller release
  times, plant parameters, or plant integration. Measurement age is the earliest visible effect; tracking
  changes downstream.
- Increasing only `T_c` reduces update count and holds each delivered sample and command longer. It does
  not coarsen the `0.01 s` plant tick, so the changed trajectory is a feedback-release effect rather than a
  plotting or solver-resolution artifact.

Faster is not automatically proof of a good interface, and slower is not automatically unsafe. The point
of each sweep is to isolate which clock moved and then observe its downstream effect.

## Broken command continuity and explicit safe states

Dropping every second command when the controller sends every `0.1 s` creates `0.2 s` delivery gaps. A
`0.12 s` watchdog refuses to hold the last force that long, so it repeatedly substitutes zero. The
recognizable symptom is not just position error: the protocol-state plot shows exactly when a dropped
packet leads to a stale command and safe-zero action. Removing only the drops recovers continuous delivery.

Cancellation is different from timeout. At the declared cancel timestamp it immediately invalidates every
queued command and forces zero, even if a command was due on that same tick. Neither action proves the
plant is physically safe; it proves only the declared software-emulator rule.

## Misconceptions to correct directly

- A plant does not pause while a controller waits for packets.
- Controller period, one-way latency, measurement age, and command age are different quantities.
- A computed command is not an applied command until it crosses the plant-side boundary.
- Packet loss does not itself apply zero; the receiver's age policy decides when to stop holding stale data.
- Watchdog timeout and cancellation have different triggers, but both use a declared zero-force fallback.
- Bounded virtual state does not prove closed-loop stability for untested dynamics or safe physical motion.
- The word HIL in the curriculum title does not turn a software emulator into physical HIL evidence.
- Static and independent simulated evidence do not prove MATLAB execution, UI rendering, real-time timing,
  protocol compatibility, target scheduling, hardware I/O, bench behavior, or field performance.

Ask one observation question at a time. Request the teach-back only after executable checks pass.

## Source walkthrough

# P24 walkthrough: Close the Loop Through a Hardware-in-the-Loop Plant

## Learner sequence

1. Read the guiding question and P23 connection before running code.
2. Predict only which baseline view changes first when one-way latency grows: timestamp age, applied force,
   or mechanical position.
3. Visualize reference and virtual plant position in metres. Name the baseline tracking transition without
   explaining it yet.
4. Visualize measurement age in seconds and requested versus applied force in newtons. Identify the first
   interval where transport separates the two force signals.
5. Read the packet event order and exact mass–damper transition. Explain why the plant keeps moving while a
   measurement or command is in flight.
6. Sweep only one-way latency `[0.01 0.02 0.04 0.06 0.08] s`. Observe timestamp age first, then tracking
   RMS and peak position.
7. Reset latency to `0.01 s`, sweep only controller period `[0.02 0.04 0.05 0.1 0.2] s`, and observe fewer
   command packets, older held measurements, and the coarsest loop's changed response.
8. Explain why the second sweep did not change the `0.01 s` plant integration tick.
9. Run the broken `0.1 s` controller, `0.04 s` latency, `0.12 s` watchdog, drop-every-second-command case.
   Identify a dropped command, its stale interval, and the later safe-zero state as separate transitions.
10. Remove only the drop cadence and verify recovery. Then cancel at `4.01 s` as the command sourced at
    `4 s` is due, verify same-tick queued work is purged, and compare that explicit cancellation with an
    age-triggered timeout.
11. Run `run_module_checks("P24")`, answer one interpretation prompt at a time, and give the required
    two-sentence teach-back.

No MATLAB-runtime, rendered-UI, wall-clock, external-protocol, target, bench, physical HIL, field, or
production evidence is claimed by this walkthrough.

## Source checks

# P24 checks: Close the Loop Through a Hardware-in-the-Loop Plant

Run `run_module_checks("P24")`, then answer one prompt at a time:

1. Which inputs define the controller clock, both transport paths, command-age policy, deterministic loss,
   cancellation, virtual plant, and bounded grid? Include units.
2. Why does increasing one-way latency change measurement age without changing controller release times or
   the plant equation?
3. Why does increasing controller period reduce command count even though the plant tick remains fixed?
4. From the plots alone, how can you distinguish computed force, delivered force, a dropped command, an
   age-triggered watchdog interval, and explicit cancellation?
5. What does the zero-latency limiting case do at a controller tick, and why must cancellation be evaluated
   before a command due on the same tick?
6. In the broken case, why does dropping every second command interact with `T_c=0.1 s` and `T_w=0.12 s`
   to create safe-zero intervals?
7. What clock synchronization, serialization, endianness, transport, deadline, scheduling, electrical,
   actuator, sensor, emergency-stop, fault-injection, bench, and physical HIL evidence is still required?

## Teach-back

In exactly two sentences, name controller period, one-way latency, measurement timestamp, command age, and
watchdog timeout. Then explain how loss or cancellation changes applied force and why this deterministic
virtual-time loop is not physical HIL validation.

The source checks and independent oracle provide static and simulated evidence only. No MATLAB-runtime,
rendered-UI, MATLAB numerical-fidelity, external-protocol, bench, physical HIL, field, or production
validation is claimed.
