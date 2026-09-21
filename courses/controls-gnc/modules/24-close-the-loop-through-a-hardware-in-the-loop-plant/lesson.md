# Close the Loop Through a Hardware-in-the-Loop Plant

**Guiding question:** What inputs, observable effects, and failure modes matter when you close the Loop Through a Hardware-in-the-Loop Plant?

Despite the retained curriculum title, this is a deterministic, software-only virtual protocol and
plant. It exercises timestamped measurement and command paths, packet loss, a watchdog, and an exact
mass–damper step. It is not a capstone and does not claim that physical HIL hardware ran.

## Predict before running

A measurement must travel to the controller before its command travels back to the plant. Predict
whether increasing one-way latency first changes packet age, applied force, or mechanical position.
Then predict when dropped commands will make the watchdog substitute zero force.

## Model and equations

The virtual plant is a mass $m=1.5\;\mathrm{kg}$ with viscous damping
$c=1.2\;\mathrm{N\,s/m}$:

$$
\dot x=v,\qquad m\dot v=u_{\mathrm{applied}}-cv.
$$

At a controller event, the most recently delivered measurement produces

$$
u_c=\operatorname{clip}\left(18(r-x_m)-8v_m,-30,30\right)\;\mathrm{N}.
$$

The reference is $1\;\mathrm m$ for the first four seconds and $-0.5\;\mathrm m$ afterward. For
one plant tick $\Delta t=0.01\;\mathrm s$ with held force, define
$\alpha=e^{-c\Delta t/m}$. The exact update is

$$
v_{k+1}=\alpha v_k+\frac{1-\alpha}{c}u_k,
$$

$$
x_{k+1}=x_k+\frac{m}{c}(1-\alpha)v_k+
\left[\frac{\Delta t}{c}-\frac{m}{c^2}(1-\alpha)\right]u_k.
$$

## Event order

At every integer plant tick, the software model performs this order:

1. At a controller-release tick, enqueue the current plant measurement for delivery after $L$.
2. Deliver a measurement due now.
3. If this is a controller tick and a measurement exists, compute and enqueue (or drop) a command.
4. Deliver a command due now.
5. Evaluate startup-safe and watchdog state, select applied force, then propagate the plant.

This order makes $L=0$ a real same-tick limiting case: the new measurement is visible to the
controller and its command is visible to the plant before propagation. Both transport directions use
the selected one-way latency, so a nonzero update experiences a round trip.

## Two one-variable sweeps

1. Hold `one_way_latency_s=0.01` and sweep `controller_period_s` through
   `[0.02, 0.05, 0.15]`. The plant tick stays fixed while feedback releases become less frequent.
2. Reset the period to `0.05`, then sweep `one_way_latency_s` through `[0.0, 0.01, 0.06]`.
   Read measurement and command age before interpreting the downstream position change.

Do not change both clocks at once until you can distinguish controller release time, measurement age,
command age, and plant integration time.

## Intentionally broken case

Broken mode fixes the controller period at $0.1\;\mathrm s$, one-way latency at
$0.04\;\mathrm s$, watchdog timeout at $0.12\;\mathrm s$, and drops every second command. The
$0.2\;\mathrm s$ spacing between surviving commands exceeds the watchdog threshold, so safe-zero
intervals appear. Packet loss does not itself apply zero; the receiver's age policy does.

## Recovery

Disable broken mode to restore the selected clocks, retain every command, and return to the
$0.2\;\mathrm s$ watchdog. Confirm that watchdog-active fraction returns to zero and that the
reference reversal remains tracked. This is still software-only and does not claim physical HIL.

## Source-to-platform boundary

The platform retains the source's two timestamped paths, same-tick delivery convention, reference
reversal, command saturation, deterministic drop schedule, fail-zero watchdog, and exact damped-plant
transition. The pinned source additionally exposes cancellation, watchdog timeout, drop cadence,
plant mass, plant tick, and duration as independent inputs and records detailed packet counters and
source ages. Those extra controls and cancellation precedence are explicit omissions here; they are
not silently presented as executed platform behavior.

The independent Python reference uses a separately implemented event schedule and exact transition.
No MATLAB runtime, wall-clock scheduling, serialization, external protocol, electrical interface,
physical actuator/sensor, emergency stop, bench, field, or production evidence is claimed.

## Common mistakes

- Treating controller period, one-way latency, measurement age, and command age as one quantity.
- Assuming the plant pauses while a packet is in flight.
- Treating a computed controller force as applied force before command delivery.
- Assuming a bounded virtual trace proves stability or physical safety.
- Calling this a course capstone or physical HIL result because of the retained title.

## Teach-back

In two sentences, describe the measurement-to-command round trip and the watchdog's fail-zero rule.
Then identify the omitted cancellation/physical-HIL evidence and explain why it bounds the conclusion.
