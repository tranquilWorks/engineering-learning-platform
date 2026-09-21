# Measure Motion with Encoders

**Guiding question:** What inputs, observable effects, and failure modes matter when you measure Motion with Encoders?

## Concept and prediction

An incremental quadrature encoder converts shaft angle into integer edge counts. Angle resolution is finite, and velocity is inferred from count differences over a sample interval.

Before running the model, predict this: More counts per revolution reduces angle quantization, while higher sample rate changes how many count increments appear in each velocity estimate. Record the sign and approximate scale you expect, not only “more” or “less.”

## Model, symbols, and equations

- $$C_k=\operatorname{round}\!\left(\frac{4N\theta_k}{2\pi}\right)$$ — Quadrature decoding yields four count edges per encoder line.
- $$\hat\theta_k=\frac{2\pi C_k}{4N}$$ — Counts reconstruct a quantized shaft angle.
- $$\hat\omega_k=\frac{\hat\theta_k-\hat\theta_{k-1}}{T_s}$$ — Sampled velocity comes from finite differences.

Symbols and units:

- $N$ — encoder lines per revolution; $C$ — cumulative quadrature edge count.
- $\theta,\hat\theta$ — true and reconstructed angle (rad).
- $\omega,\hat\omega$ — true and estimated speed (rad/s).
- $T_s$ — sample interval (s); RPM is converted by $2\pi/60$.

Positive shaft rotation increases count. The control states physical lines/rev; the decoder must explicitly apply the x4 quadrature edge factor.

## Manipulation: two one-variable sweeps

1. Sweep `counts_per_rev` through [128,1024,4096] while holding the other controls at baseline. Compare the angle-error stair steps and RMS error.
2. Restore baseline, then sweep `sample_rate_hz` through [10,50,200]. Compare velocity quantization at different count increments per sample.

The first plot shows the physical response. The second exposes the mechanism or residual that decides whether the result is trustworthy. Every axis states its unit.

## Evidence and limiting cases

Use the metric cards and both plots to test the prediction. The retained expected vectors are produced by an independent integer count equation and analytic quantization bound; the actual vectors come from this Python experiment.

- At zero speed, all counts and estimated velocities remain zero.
- Angle error magnitude is bounded by half a decoded count, $\pi/(4N)$.
- For an exact integer number of counts per sample, the velocity estimate is exact after the first sample.

This is simulated software evidence. It does not demonstrate a physical robot, motor, encoder, IMU, bench, HIL, field, or production result.

## Intentionally broken assumption

**Missing quadrature factor.** The broken decoder divides edge counts by $N$ rather than $4N$. It reports four times the true angle and speed.

## Explanation and recovery

Disable the missing-quadrature-factor mode and decode with four edges per encoder line. Recovery is complete only when the diagnostic signature returns to the independent reference tolerance and you can explain why.

## Common mistakes

- Confusing encoder lines with decoded quadrature edges.
- Computing RPM directly from counts without including sample time.

- Changing several controls at once and losing causal attribution.
- Treating a plausible plot as proof without checking units, residuals, and limiting cases.

## Focused check and teach-back

At baseline, identify one equation term changed by each sweep, reproduce the broken symptom, recover it, and cite one metric plus one plot feature as evidence. Then teach it back in two minutes: state the convention, derive the governing relationship, name the failed assumption, and explain why the recovery works.

