# Integrate Wheel Odometry

**Guiding question:** What inputs, observable effects, and failure modes matter when you integrate Wheel Odometry?

## Concept and prediction

Wheel odometry composes many small relative motions. Encoder counts constrain wheel rotation, not ground motion, so correct integration can still drift when a wheel slips or its radius is miscalibrated.

Predict which error dominates at baseline: encoder quantization, the 2% right-wheel slip, or the choice between an exact twist and old-heading Euler integration.

## Model, symbols, and equations

- $$\Delta s=\tfrac12(\Delta s_R+\Delta s_L),\quad\Delta\theta=(\Delta s_R-\Delta s_L)/b$$ — local differential-drive twist.
- $$\Delta s_w=r\,\Delta n_w\,2\pi/(4N)$$ — x4 quadrature counts converted to wheel travel.
- $$\Delta\mathbf p=\Delta s\,\operatorname{sinc}(\Delta\theta/2)[\cos(\theta+\Delta\theta/2),\sin(\theta+\Delta\theta/2)]^T$$ — exact constant-twist translation.

$r$ is wheel radius, $b$ is track width, $N$ is encoder lines/rev, and $\theta$ is positive counterclockwise world yaw. Units are metres for geometry and position, radians internally for yaw, and lines/rev for encoder resolution. Body +x points forward and body +y left.

## Manipulation: two one-variable sweeps

1. Sweep `encoder_cpr` through [128,1024,4096]. Quantization ripple should shrink, but slip-driven bias should remain.
2. Restore baseline, then sweep `slip_percent` through [0,2,15]. Position and heading error should grow systematically.

The trajectory plot shows accumulated path disagreement. The diagnostic plot separates translational and heading errors versus time.

## Evidence and limiting cases

An independent oracle reconstructs the same count increments and composes closed-form SE(2) exponentials; the production experiment owns its own integration path.

- Equal wheel increments produce straight motion and the sinc limit approaches one.
- Infinite encoder resolution removes quantization but not slip.
- Zero slip and sufficiently fine counts recover the commanded differential-drive path.

This is software odometry evidence, not physical encoder, tire/track, robot, HIL, bench, or field validation.

## Intentionally broken assumption

**Old-heading Euler step.** Broken mode translates using the heading at the start of each interval instead of the twist midpoint. Finite rotations then introduce a systematic integration chord error.

## Explanation and recovery

Disable Euler mode and compose each wheel increment as an SE(2) twist. Then separate residual drift into quantization and wheel-to-ground model error; integration cannot infer unmeasured slip.

## Common mistakes

- Treating encoder rotation as guaranteed ground displacement.
- Forgetting x4 quadrature when converting line count to edge count.
- Updating translation with the new or old heading instead of the twist midpoint.
- Comparing wrapped and unwrapped heading differences directly.

## Focused check and teach-back

At baseline, cite final position and heading error, run both sweeps, reproduce the Euler failure, and recover it. Teach back the count conversion, twist equation, frame convention, and why perfect integration does not eliminate slip drift.
