# Implement Proportional Navigation

**Guiding question:** What inputs, observable effects, and failure modes matter when you implement Proportional Navigation?

Observe proportional navigation geometry, acceleration authority, and miss distance. This native lab preserves the source experiment while making the levers, diagnostics, and recovery available directly in the learning platform.

## Predict before running

Insufficient lateral acceleration should leave a finite miss even with a reasonable navigation constant. Write down the mechanism you expect—not only the trace direction—before moving a control.

## Model and equations

- $$a_n=N V_c\dot\lambda$$ — PN commands lateral acceleration from closing speed and line-of-sight rate.
- $$\dot\lambda=(r_xv_y-r_yv_x)/\|r\|^2$$ — LOS rotation encodes collision-course error.

The GUI evaluates these equations deterministically. Read the metric cards and both plots together: a pleasing response can still conceal poor authority, weak conditioning, stale data, or invalid assumptions.

## Two one-variable sweeps

1. Sweep `navigation_constant` through [2.0, 3.0, 5.0]. Hold every other control fixed and explain the causal chain from equation to trace to metric.
2. Sweep `maximum_acceleration_m_s2` through [20.0, 80.0, 120.0]. Compare the changed mechanism plot with your first prediction.

Do not tune both levers at once until you can identify which term each lever changes.

## Intentionally broken case

The broken case limits lateral acceleration to 5 m/s², preventing intercept in the modeled engagement. Predict the signature before enabling **broken mode**.

## Recovery

Disable the broken case and restore the 80 m/s² authority used by the baseline. A recovery is complete only when you can name the failed assumption and point to the metric or trace that confirms it.

## Common mistakes

- Treating a simulation trace as proof about hardware or production behavior.
- Changing multiple controls at once and losing causal attribution.
- Reading only the final value while ignoring transient effort, conditioning, delay, or saturation.
- Hiding a failed assumption by retuning instead of reproducing and explaining it.

## Teach-back

In two minutes: state the governing equation, explain what each live lever changes, identify the broken assumption, and justify the recovery with one visible metric and one plot feature.

---

## Source lesson (retained and polished into this GUI)

# P22 lesson: Implement Proportional Navigation

## Guiding question

What inputs, observable effects, and failure modes matter when you implement Proportional Navigation?

## Compounds on P21

P21 generated a smooth reference and compared its derivative demands with declared limits. P22 makes the
next distinction: a guidance law generates an acceleration request from relative geometry, while the
vehicle's acceleration authority decides whether that request can be applied. Guidance success and
trajectory feasibility are related boundaries, not interchangeable claims.

## Mental model

Imagine the line of sight as a bearing drawn from interceptor to target. If that bearing stays constant
while range decreases, the two paths are converging. If the bearing continues rotating, the interceptor
will pass to one side unless it turns enough to remove the rotation.

For relative position `r = [r_x,r_y]` and relative velocity `v_rel`, use

```text
R         = sqrt(r_x^2 + r_y^2)                     [m]
Vc        = -dot(r,v_rel)/R                          [m/s]
lambdaDot = (r_x*v_rel_y-r_y*v_rel_x)/R^2            [rad/s]
a_cmd     = N*max(Vc,0)*lambdaDot                    [m/s^2]
a_applied = clip(a_cmd,-a_max,+a_max)                [m/s^2]
psi_next  = psi + (a_applied/interceptor_speed)*dt   [rad]
```

The cross product order fixes the turn sign; the minus sign makes `Vc` positive while closing. The
`max(Vc,0)` term stops PN from treating an opening engagement as though it were still closing. The model
uses radians internally and accelerates normal to a constant-speed velocity.

## What the baseline reveals

At `[5000,600] m` with target crossing speed `60 m/s`, the initial range is about `5035.87 m`, closing
speed is about `290.72 m/s`, and LOS rate is about `0.01893 rad/s`. With `N=3`, the initial command is
about `16.51 m/s^2`, below the `80 m/s^2` limit. The path bends until LOS rotation is nearly removed and
the piecewise-linear relative segment first crosses the `5 m` capture circle.

Event interpolation matters: a time step can cross the circle between plotted samples. The source solves
the segment/circle intersection and stops at the first entry rather than calling the nearest sample an
exact collision.

## Two levers and the broken assumption

- Increasing `N` multiplies the initial command exactly because the initial `Vc` and `lambdaDot` are
  shared. Later paths differ because each turn changes future geometry. Too-small `N` can leave a miss;
  larger `N` commands more acceleration and eventually gives diminishing time benefit.
- Reducing `a_max` leaves the raw PN request intact but clips applied acceleration. The difference between
  command and applied turn is visible saturation, directly connecting to P21's limit discipline.
- In the deliberately broken `5 m/s^2` case, clipping persists, range bottoms out far outside `5 m`, then
  opens until the `25 s` time limit. Restoring `80 m/s^2` exactly recovers the baseline.

## Limiting cases

A target crossing speed of `-36 m/s` makes relative velocity initially parallel to `-r`; LOS rate and PN
command are zero, yet constant bearing plus decreasing range produces capture without a turn. `N=0`
also gives zero command, but for the `60 m/s` crossing baseline geometry the bearing rotates and the
interceptor misses. Once closing speed becomes nonpositive after a miss, the model commands zero rather
than using the magnitude of an opening speed.

## Misconceptions to correct directly

- PN does not aim at the target's current location; it acts on LOS rotation.
- LOS angle and LOS rate are different measurements.
- A larger `N` is not free: it raises acceleration demand.
- Commanded acceleration and applied acceleration are identical only when the actuator does not clip.
- Small range alone is not the mechanism; constant bearing with decreasing range is the intercept cue.
- Capture radius is not exact collision, and sampled simulation is not continuous-time proof.
- This point-mass model omits sensor noise, delay, actuator dynamics, target maneuver acceleration,
  autopilot stability, collision safety, HIL timing, and physical implementation.
- Independent reference arithmetic is not MATLAB-runtime or rendered-UI evidence.

Ask one observation question at a time. Request the teach-back only after executable checks pass.

## Source walkthrough

# P22 walkthrough: Implement Proportional Navigation

## Learner sequence

1. Read the guiding question and P21 connection before running code.
2. Predict only whether the baseline LOS bearing will keep rotating or settle toward constant bearing.
3. Visualize engagement geometry first. Observe the interceptor curve toward the target path.
4. Visualize range and LOS rate. Identify decreasing range and LOS rate approaching zero before reading
   the mechanism.
5. Compare commanded and applied lateral acceleration against the `80 m/s^2` limit.
6. Sweep only `N = [1 2 3 4 5]` while target crossing speed, acceleration limit, step, and horizon reset.
   Observe that initial command scales with `N`, `N=1` misses, and stronger guidance captures.
7. Explain the changed view from `a_cmd=N*max(Vc,0)*lambdaDot`, not from MATLAB plotting mechanics.
8. Reset `N=3`, then sweep only acceleration authority `[5 10 20 40 80] m/s^2`. Compare closest range,
   peak applied acceleration, clipping duration, and intercept status.
9. Explain that the PN request and available vehicle turn are separate contracts.
10. Run the broken `5 m/s^2` case. Identify sustained clipping, closest approach outside the capture
    radius, opening range, and time-limit termination; then restore the exact baseline.
11. Run `run_module_checks("P22")`, answer one interpretation prompt at a time, and give the required
    two-sentence teach-back.

No MATLAB-runtime, rendered-UI, autopilot, actuator-dynamics, bench, HIL, field, or physical evidence is
claimed by this walkthrough.

## Source checks

# P22 checks: Implement Proportional Navigation

Run `run_module_checks("P22")`, then answer one prompt at a time:

1. How do relative position and velocity produce range, closing speed, and LOS rate, including their units?
2. Why does constant bearing plus decreasing range indicate intercept, while small range by itself does not?
3. What does `N` change immediately, and why can increasing it raise acceleration demand?
4. Why can the raw PN command be correct while an acceleration-limited vehicle still misses?
5. What observable distinguishes the `5 m/s^2` broken case from the `80 m/s^2` baseline?
6. Why must capture be checked between time samples, and why is capture-radius entry not exact collision?
7. What sensor, delay, actuator, autopilot, target-maneuver, HIL, and field evidence is still required before
   transferring this result to a physical vehicle?

## Teach-back

In exactly two sentences, name `r`, `v_rel`, `Vc`, `lambdaDot`, `N`, and acceleration authority. Then explain
the visible constant-bearing/decreasing-range mechanism and why sustained command clipping causes the broken
case to miss.

The source and independent oracle provide static and simulated evidence only. No MATLAB-runtime,
rendered-UI, MATLAB numerical-fidelity, autopilot, bench, HIL, field, or production validation is claimed.
