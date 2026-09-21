# Build a Range Sensor Model

**Guiding question:** What inputs, observable effects, and failure modes matter when you build a Range Sensor Model?

## Concept and prediction

A range sensor does not directly report the perpendicular distance to a surface. It reports distance along a ray, then adds noise, bias, quantization, missed returns, and saturation. Keeping geometry and sensor imperfections separate makes residuals diagnosable.

Before running the model, predict how a 3 m wall distance changes when the beam rotates from 0 deg to 60 deg. Also predict whether zero-mean noise can repair a biased geometric model.

## Model, symbols, and equations

- $$r_{\mathrm{true}}=d/\cos\theta$$ — intersection range for a planar wall whose normal is aligned with the sensor x-axis.
- $$z_k=\operatorname{clip}(r_{\mathrm{true}}+n_k,0,r_{\max})$$ — bounded measurement model.
- $$e_k=z_k-r_{\mathrm{model}}$$ — innovation or residual used to judge the model.

Symbols and units:

- $d$ — perpendicular wall distance (m).
- $\theta$ — beam angle from the wall normal (deg at the control, rad internally).
- $n_k$ — zero-mean deterministic test-noise sequence with selected standard deviation (m).
- $r_{\max}$ — maximum reportable range (m).

The sensor origin is at $(0,0)$, +x follows the wall normal, and positive angles rotate counterclockwise. Range is nonnegative.

## Manipulation: two one-variable sweeps

1. Sweep `beam_angle_deg` through [0,30,60] while holding the wall fixed. The slant range should follow the secant curve and double at 60 deg.
2. Restore baseline, then sweep `noise_std_m` through [0,0.02,0.2]. The residual RMS should grow while its mean remains near the geometric modeling error.

The sample plot separates repeatability from model bias. The angle plot exposes the geometric mechanism and the saturation ceiling. Every axis states its unit.

## Evidence and limiting cases

The retained expected vectors use a closed-form ray-plane intersection and a normalized independent noise pattern. The production experiment generates the measurement trace and diagnostic signature separately.

- At $\theta=0$, slant range equals perpendicular distance.
- As $|\theta|$ approaches 90 deg, ideal range grows without bound and a finite sensor saturates.
- At zero noise, any residual is model or saturation error, not randomness.

This is software simulation evidence. It is not a physical range-sensor, robot, bench, HIL, field, or production result.

## Intentionally broken assumption

**Normal-incidence shortcut.** Broken mode assumes $r=d$ at every beam angle. Oblique returns then acquire a deterministic positive residual that random noise cannot average away.

## Explanation and recovery

Disable the shortcut, restore $d/\cos\theta$, and verify that residual bias collapses until saturation dominates. Recovery is complete only when you can distinguish geometric error, random spread, and clipping in the plots.

## Common mistakes

- Adding sensor noise before establishing the correct ray geometry.
- Treating a maximum-range return as an ordinary unbiased sample.
- Mixing beam angle from the surface tangent with angle from the surface normal.
- Changing angle, noise, and maximum range together and losing causal attribution.

## Focused check and teach-back

At baseline, estimate the slant range by hand, cite the measured residual RMS, reproduce the broken bias, and recover it. Then teach it back: state the frame, derive the secant term, identify the saturation limit, and explain why averaging cannot fix the wrong geometry.
