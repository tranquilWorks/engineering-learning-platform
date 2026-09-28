# Verify a faulted software loop

Commands carry source timestamps through a simulated transport before they reach a first-order plant. A watchdog must act on the age of the accepted command. Packet-loss percentage alone does not specify safe actuator behavior.

## Model and equations

The virtual loop runs 500 ticks at $\Delta t=0.02\,\mathrm{s}$. A source controller computes $u_k=\operatorname{clip}(2(1-x_k),-3,3)$. The actuator's delivered command $u^a_k$ drives

\[x_{k+1}=e^{-\Delta t}x_k+(1-e^{-\Delta t})u^a_k.\]

State and command are normalized. The no-fault proportional controller settles at $x=2/3$, not at one: solve $x=2(1-x)$. Tracking RMS therefore measures error from $2/3$ over the final 250 samples.

Transport delay is $d=\lceil L/20\,\mathrm{ms}\rceil$ ticks. A contiguous burst starting at tick 150 drops $\operatorname{round}(500f)$ source commands. If $f>0$, source tick 50 is also delivered again 50 ticks late. Healthy reception accepts only increasing source stamps. Age is $(k-k_{source})\Delta t$; when there is no valid source or age exceeds 0.05 s, the actuator applies zero. The delivery deadline is separately 0.03 s.

## Baseline workflow

Predict whether a 12 ms requested delay becomes 12 or 20 ms on this grid. It becomes one 20 ms tick. The 5% loss burst removes 25 commands over 0.5 s. The late duplicate still counts as a delivered deadline miss even though a healthy receiver rejects it.

Run the baseline and inspect the plant and age traces. The late-packet fraction is $1/475\approx0.002105$, the watchdog is active for 5% of sampled ticks, and expired nonzero actuator samples are zero. The requirement table separately checks late deliveries ≤1%, dropped commands ≤20%, zero unsafe samples and settled RMS ≤0.4. They are explicit software exercise bounds, not a real-time certification.

## Two one-variable sweeps

1. Keep drop fraction 0.05 and raise latency to 80 ms. Four-tick delay exceeds the freshness threshold: healthy fail-zero behavior can preserve the actuator requirement while failing timing and tracking.
2. Restore 12 ms and raise drop fraction to 0.5. A 250-command contiguous gap creates a long safe hold. Compare the measured state deviation with the nominal loss percentage; the gap's timing matters.

## Intentionally broken case

Broken mode accepts old source stamps and holds the last command beyond expiry. It changes receiver/watchdog behavior, not the requested latency or loss fraction. The retained event list and applied-command history show actual expired nonzero samples. A broken receiver does not make every packet late; the deadline metric still follows real arrivals.

## Recovery

Disable the fault at the same controls. Source-order rejection and fail-zero return. Re-run the baseline; command events and numerical signatures must reproduce the original values.

## Limiting cases and invariants

Zero latency and zero drops produce no injected late duplicate and no transport-age fault. An isolated dropped packet may remain within the age allowance; a long burst does not. Startup without a received command is fail-zero. Every nonzero healthy actuator sample must have an accepted source no more than 0.05 s old.

## Independent evidence

The reference reconstructs arrival indices directly from source ticks rather than using the production event queue. It recomputes the closed-loop state, late deliveries and expiry actions. Physical recurrence and timestamp tests complement the five independent scenarios.

## Common mistakes

Do not substitute requested latency for quantized arrival time, count a rejected old packet as the newest command, or call this virtual schedule hardware-in-the-loop evidence. The runtime's own execution deadline is a different concept.

## Teach-back

- Why is the target equilibrium $2/3$? Proportional control without an integral term has a static error on this plant.
- Can a safe actuator coexist with a failed overall run? Yes: fail-zero may satisfy safety while preventing tracking.
- Why count late rejected packets? Transport quality and receiver protection are separate requirements.

## Cumulative assessment

Reconstruct one delayed command, one burst-expired command and the late duplicate using source and arrival ticks. For each, determine age, acceptance and applied action. Then recover the baseline and explain the distinct timing, loss, safety and tracking verdicts.
