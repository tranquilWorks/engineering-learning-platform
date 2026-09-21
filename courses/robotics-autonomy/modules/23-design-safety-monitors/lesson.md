# Design Safety Monitors

**Guiding question:** What inputs, observable effects, and failure modes matter when you design Safety Monitors?

## Concept and prediction

A safety monitor independently checks whether commanded behavior remains inside a conservative envelope. For obstacle approach, the decision must include current speed, reaction delay, available deceleration, and margin—not only current distance.

Predict the baseline stopping distance and compare it with a fixed 0.1 m trigger. Which policy can stop before a 3 m obstacle?

## Model, symbols, and equations

- $$d_b=v^2/(2a)$$ — ideal constant-deceleration braking distance.
- $$d_{stop}=v t_r+d_b+d_m$$ — required separation including reaction travel and margin.
- $$d_{meas}\le d_{stop}\Rightarrow u_{safe}=BRAKE$$ — monitor intervention rule.

Speed uses m/s, distance uses metres, reaction time uses seconds, and deceleration magnitude uses m/s^2. +x points toward the obstacle. Positive separation means the robot has not reached it.

## Manipulation: two one-variable sweeps

1. Sweep `command_speed_m_s` through [0.5,2,3]. Braking distance grows with speed squared.
2. Restore baseline, then sweep `reaction_time_s` through [0,0.2,0.8]. The reaction component grows linearly with speed and delay.

The approach plot shows speed and separation. The mechanism plot directly compares available separation with the required stopping envelope.

## Evidence and limiting cases

The independent reference executes the stated discrete braking recurrence and checks the continuous kinematic stopping limit. Production maintains its own monitor and state trace.

- At zero speed, braking distance is zero but static margin remains.
- Infinite deceleration removes ideal braking distance but not sensing/decision delay.
- A monitor built on optimistic deceleration is not conservative.

This is software safety-logic simulation, not a certified safety function, physical brake test, robot, HIL, field, or production result.

## Intentionally broken assumption

**Distance-only trigger.** Broken mode waits until separation reaches 0.1 m. It ignores the robot's kinetic state and therefore intervenes after collision is unavoidable.

## Explanation and recovery

Restore the speed-dependent envelope, latch braking, and use conservative bounds supported by physical validation before deployment. The software plot demonstrates logic, not safety integrity.

## Common mistakes

- Comparing distance with stopping time or other mismatched units.
- Using nominal rather than worst-case deceleration and reaction delay.
- Allowing lower-priority commands to overwrite a safety stop.
- Calling simulated separation a certified stopping-distance result.

## Focused check and teach-back

At baseline, calculate braking and reaction distance, cite minimum separation and stop time, reproduce the late-trigger collision, and recover it. Teach back units, envelope terms, monitor priority, and the physical evidence still required.
