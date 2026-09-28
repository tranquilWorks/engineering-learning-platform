# P64 lesson: A Signed Angle Error from One Pair of Beams

Guiding question: How can sum and difference beams estimate small angle error around boresight?

## Physical mental model

Imagine two receive beams looking a few degrees to opposite sides of
boresight. A target exactly in the middle excites them equally. A target moving
right makes the right beam stronger and the left beam weaker. Their total says
"a target is present in the shared beam," while their imbalance says "move the
track direction right."

Both channel voltages come from the same snapshot. That simultaneity is the
point of monopulse: target amplitude does not need to remain unchanged during
an angle scan.

## From array phase to two receive channels

P61 introduced the broadside-referenced ULA steering vector

```text
a_m(theta) = exp(j 2 pi m q sin(theta)),  q = d/lambda.
```

P62 showed how element spacing and aperture shape the corresponding pattern,
and P63 applied the explicit receive sum `w^H x`. P64 uses two such fixed
weights, steered to `-theta_s` and `+theta_s`:

```text
L = w_L^H x,    R = w_R^H x.
```

Raw off-boresight beams generally have different complex phases at boresight.
The experiment measures those nominal phases and rotates both channels to the
same boresight reference before combining them. Without this step, subtracting
two arbitrary complex phases would not represent an amplitude imbalance.

## The sum, difference, and normalized ratio

After phase alignment, the explicit hybrid is

```text
Sigma = (R + L)/2
Delta = (R - L)/2
eta   = Re{Delta/Sigma}.
```

The factors of two cancel in the ratio. With the experiment's sign convention,
a positive target angle makes `R` larger and gives positive `eta`.

Near boresight, the symmetric ratio is approximately linear:

```text
eta(theta) approximately K theta,       theta approximately eta/K,
```

where `K` has units of ratio per degree and depends on the array and beam
squint. The script does not assume one universal slope. It computes a
noise-free lookup over `+/-4 deg`, verifies that it is strictly increasing,
and performs the visible piecewise-linear inverse between adjacent calibration
points.

This is a complex-voltage amplitude-comparison ratio. It is not the power ratio
`(P_R-P_L)/(P_R+P_L)`, which has a different calibration slope.

## What the first plots mean

The left and right magnitude patterns overlap around boresight. `|Sigma|` is
large there, while the signed real part of `Delta` crosses zero. Dividing by
`Sigma` removes common target-voltage scale and creates a steep signed error
curve. The red interval is the only sector the estimator claims.

For the `+2 deg` baseline target, each receiver-noise realization perturbs both
channel voltages. Individual `Delta/Sigma` samples scatter, while coherent
averaging of `Delta` and `Sigma` before division produces a stable estimate.
The script deliberately does not average already formed angle estimates and
call that coherent processing.

## Sweep 1: squint is a sensitivity tradeoff

Moving the two beams farther apart increases the local difference between
their responses, so the ratio slope becomes steeper. But each beam then looks
farther away from boresight, reducing `|Sigma(0)|`. A large slope is useful only
while the sum channel remains strong and the ratio stays monotonic over the
required tracking sector.

This is why the plot reports both ratio-per-degree slope and normalized
boresight sum voltage. Squint is not simply "more is better."

## Sweep 2: noise changes precision, not calibration

The SNR sweep reuses one normalized private noise record and scales only its
amplitude. The array, target, beam weights, and calibration curve do not move.
As SNR rises, the single-snapshot angle RMSE falls. Coherent channel averaging
reduces random noise further, but it cannot remove a fixed channel calibration
error.

Noisy ratios beyond the reviewed calibration endpoints are explicitly
saturated at `-4` or `+4 deg` for plotting and RMSE accounting. That visible
bounding is not evidence that the true target lies at the boundary; it says
the local sensor has run out of calibrated angle information.

## Broken case: gain mismatch looks like angle

Let the right receiver have an unknown voltage gain `g` while the target is at
boresight, so nominally `R=L=A`. The comparator now reports

```text
eta_broken = (g A - A)/(g A + A) = (g - 1)/(g + 1).
```

For `g=1.12`, this is positive even though the target is at `0 deg`. The ratio
cannot distinguish a physical rightward displacement from a right-channel
gain error unless the receiver is calibrated.

Recovery divides the recorded right channel by the known `g` and recomputes
`Sigma`, `Delta`, and the ratio. The target, array, and left/right raw channel
values are not regenerated. That same-data recovery isolates calibration as
the cause.

## Limiting cases and claim boundary

- At exact boresight with matched channels, symmetry makes `Delta=0` and
  `eta=0`.
- If target voltage scales both channels equally, the scale cancels in
  `Delta/Sigma` as long as the sum is not near zero.
- When `Sigma` is weak, noise can make the ratio arbitrarily unstable. The
  reviewed calibration sector enforces a minimum normalized sum magnitude.
- Outside the local monotonic sector, a beam pattern can turn, cross a null, or
  repeat a ratio. Monopulse is an angle-error sensor around a tracked look
  direction, not a global DOA search.
- A gain mismatch creates bias; a phase mismatch can also rotate energy between
  the real and imaginary comparator components.
- The narrowband, far-field model omits element patterns, coupling, multipath,
  near-field curvature, broadband squint, target scintillation, and automatic
  calibration estimation.

P67 will broaden the ideal single-channel mismatch into array calibration and
mutual-coupling errors. Repository static checks and a Python numerical oracle
do not validate MATLAB-rendered figures, antennas, hardware/HIL, real-time
execution, field performance, or operational radar behavior.

## Interactive lab: Build an Amplitude-Comparison Monopulse Experiment

**Guiding question:** How can sum and difference beams estimate small angle error around boresight?

Twelve half-wavelength sensors and 256 snapshots observe a coherent 2-degree target of phase .4 rad, at 15 dB SNR. Beams squint +/-3 degrees and are phase-aligned at boresight before Sigma=(R+L)/2 and Delta=(R-L)/2. A full -10:.05:10-degree pattern supplies monotone calibration within +/-4 degrees. Snapshot estimates require |Sigma|>=.15; valid ratios interpolate and clip at calibration endpoints, with clipping counted explicitly. The coherent estimate uses Re(mean Delta/mean Sigma), not mean of snapshot ratios. Squint 1.5/3/5 degrees and SNR -5/5/15/25 dB reuse inputs. The named noiseless boresight failure changes right gain to 1.12 and recovers via measured inverse gain.

### Predict, sweep, explain

Predict the sign of Delta/Sigma for a right-of-boresight target. Why do squint, sum-channel strength, SNR, calibration bounds and gain mismatch all matter for the angle estimate?

1. Start at the baseline. Sweep only **Beam squint deg** from 3 to 5 deg. Predict the change, run, and explain a measured value using the equation; then reset.
2. Start at the baseline. Sweep only **Receiver SNR db** from 15 to -5 dB. Predict the change, run, and explain a measured value using the equation; then reset.
3. Enable the broken case. Unknown right-channel gain 1.12 gives a nonzero angle for a noiseless boresight target. This named mismatch scene is separate from the selected noisy 2-degree target.
4. Recovery: Divide the right channel by the measured gain on unchanged boresight data. Disable the toggle for exact selected noisy-scene recovery. Calibration is local to +/-4 degrees; clipping is not evidence of accuracy outside that sector.

### Focused check and teach-back

Predict the sign of Delta/Sigma for a right-of-boresight target. Why do squint, sum-channel strength, SNR, calibration bounds and gain mismatch all matter for the angle estimate? Support your answer with a measured value and units. Explain the recovery assumption and identify what this finite experiment cannot establish.

### Common mistakes

Unknown right-channel gain 1.12 gives a nonzero angle for a noiseless boresight target. This named mismatch scene is separate from the selected noisy 2-degree target. Keep measured units, model assumptions and the named recovery boundary explicit.

### Scope of this lab

The source lesson is preserved above. The source Park–Miller/Box–Muller input formulas and array ordering are retained, including P58’s zero uniform offset and the array complex-noise convention. This is algorithmic software evidence, not a MATLAB runtime execution claim. Source console/figure presentation becomes labeled native plots and metrics. Calculations use the full stated arrays; displayed line and heatmap coordinates may be decimated. Independent numerical comparisons retain five scenarios. No MATLAB execution, browser/accessibility review, representative learner, hardware or production validation is claimed.
