# Estimate Vehicle State

> **Guiding question:** How do measured speed and yaw rate become a frame-consistent estimate of position, heading, and curvature?

## Physical model, frame, and units

The global frame uses +x forward at the initial state, +y left, and positive heading counter-clockwise from above. Speed `v` is nonnegative in m/s. Yaw rate enters the interface in degrees per second and is converted exactly once to `r` in rad/s. Constant-input curvature is `kappa = r/v`, turn radius is `1/|kappa|`, and lateral acceleration is `a_y = v r`.

The path integrates for 10 seconds with 0.1 s steps. Midpoint heading avoids using either the old or new orientation for the full interval: `x += v cos(psi + r dt/2) dt`, `y += v sin(psi + r dt/2) dt`, then `psi += r dt`. The retained invariants are path distance `vT` and heading change `rT`.

This is a Python-first native P19 design from a scaffold. It is not a claim of source or MATLAB-runtime equivalence, and its kinematic state is not a full tire-force observer.

## Predict and sweep one variable at a time

1. Hold yaw rate at 8 deg/s and sweep speed through 5, 20, and 45 m/s. Curvature falls as `1/v`, radius grows, but `a_y = vr` rises.
2. Restore 20 m/s and sweep yaw rate from -30 through +8 to +30 deg/s. Predict the turn side, curvature sign, and heading sign.

Always state the frame before interpreting a positive y displacement. Changing two inputs together would hide which relation caused the change.

## Named broken behavior and exact recovery

**Broken behavior:** send the numeric degrees-per-second value directly to a radian integrator. At 8 deg/s the integrator uses 8 rad/s instead of about 0.14 rad/s. The output remains finite but the heading and path are invalid.

**Exact recovery:** convert `deg/s * pi/180` once at the interface, then use radians internally. Restore 20 m/s and 8 deg/s to recover the exact baseline.

## Limits and limiting cases

At zero yaw rate, curvature and lateral acceleration are zero and the path is straight; the reported radius uses zero as a finite “straight/infinite” sentinel. Negative yaw rate mirrors turn direction. The model assumes constant inputs, no sideslip, planar motion, a flat road, exact timing, and no sensor noise. It cannot validate limit handling or tire saturation.

## Common mistakes

- Mixing degrees and radians inside the integration loop.
- Interpreting body lateral velocity as global y displacement.
- Using `a_y = v²r` when `r` is already yaw rate rather than curvature.
- Treating a kinematic path as a force-balanced vehicle response.
- Forgetting that radius is unsigned while curvature carries direction.

## Formative checks

1. Compute curvature, radius, and lateral acceleration at the baseline.
2. Verify distance and heading-change invariants.
3. Explain why speed changes radius at fixed yaw rate.
4. Identify the first interface where the broken units can be detected.

## Teach-back checklist

- [ ] I can name the frame and sign convention.
- [ ] I predicted both one-variable sweeps.
- [ ] I can derive the midpoint integration update.
- [ ] I diagnosed the named broken behavior and exact recovery.
- [ ] I can separate kinematic estimation from tire-force validation.

This is not measured-vehicle, firmware, radio, bench, vehicle/track, hardware/HIL, certification, release, or production evidence.
