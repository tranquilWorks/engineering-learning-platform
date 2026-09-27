# P29 Lesson: Build a Radar Power-Budget Experiment

## Guiding question

How quickly does received echo power fall with range?

## Physical model

A monostatic radar uses the same site to transmit and receive. Its pulse spreads
out on the trip to the target, the target redirects only a fraction described by
its radar cross section (RCS), and the echo spreads out again on the trip home.
Those two geometric spreading trips are why range appears to the fourth power,
not the second:

\[
P_r(R)=\frac{P_t G_t G_r \lambda^2 \sigma}
{(4\pi)^3 R^4 L}.
\]

Here `P_t` and `P_r` are transmit and received power in watts, `G_t` and `G_r`
are dimensionless power gains, `lambda` is wavelength in metres, `sigma` is RCS
in square metres, `R` is range in metres, and `L` is a dimensionless loss factor
greater than or equal to one. The experiment converts gains and losses from dB
to linear ratios before applying this equation. It then converts watts to dBW
with `10 log10(P/1 W)` and to dBm by adding 30 dB.

This is a power-budget model, not a waveform or range-estimation model. P30 will
turn round-trip delay into measured range; P29 asks whether an echo at a stated
range is strong enough to clear an illustrative receiver threshold.

## Why range is so expensive

At fixed transmit power, gains, wavelength, RCS, and losses,

\[
\frac{P_r(2R)}{P_r(R)}=\frac{1}{2^4}=\frac{1}{16}.
\]

Doubling range therefore loses `10 log10(16) = 12.04 dB`. Recovering that loss
requires 16 times the transmit power, 12.04 dB more total transmit/receive gain,
16 times the RCS, 12.04 dB less loss when that much removable loss exists, or a
valid combination of those budget terms. The 6 dB baseline loss cannot supply
the entire recovery by itself because the model requires `L >= 1`. A fourfold
transmit-power increase sounds large but extends
threshold-limited range by only `4^(1/4)`, about 1.41 times.
Because the equation contains the gain product `Gt*Gr`, that 12.04 dB can come
from one gain term alone or from about `+6.02 dB` in each reciprocal
transmit/receive gain.

On a logarithmic range axis the correct curve loses 40 dB per decade. The
broken `R^-2` case loses only 20 dB per decade because it accidentally counts
one spreading trip. Both broken and correct curves are anchored at 40 km, so
one matching point cannot validate a propagation law; the slope does.

## Receiver noise and detection margin

The experiment uses the available thermal-noise model

\[
N=kTBF,
\]

where `k` is Boltzmann's constant, `T` is the 290 K input reference/source
temperature, `B` is receiver noise bandwidth in hertz, and `F` is the linear
receiver noise factor referred to that input. Calling `T` a post-receiver
system noise temperature and also applying `F` would double-count receiver
noise. The experiment's
illustrative detection threshold is `N` multiplied by the required linear SNR.
The plotted margin is

\[
M_{dB}=P_{r,dBm}-(N_{dBm}+SNR_{required,dB}).
\]

Positive margin means this simple power criterion is met; it is not a promise
of a particular probability of detection. P28 explains why a real detection
claim also needs a threshold/statistical model. The seeded complex Gaussian
samples in P29 are normalized in square-root watts, so their mean squared
magnitude is power in watts. They merely show that a finite noise-power
measurement fluctuates around `kTBF`; the analytic noise floor controls the
budget.

## What each one-variable change means

- Doubling transmit power, RCS, or halving the linear loss adds about 3.01 dB.
- Adding 3 dB to either antenna gain adds 3 dB to received power.
- Doubling wavelength at fixed antenna gains adds about 6.02 dB because the
  equation contains `lambda^2`.
- A tenfold RCS increase adds 10 dB at every range; it shifts the curve without
  changing its `-40 dB/decade` slope.
- Increasing transmit power also shifts margin without changing the range
  slope, so maximum range grows only as the fourth root of power.

The frequency sweep deliberately holds both antenna gains fixed. It therefore
shows `P_r proportional to lambda^2`. Do not generalize this to fixed physical
antenna apertures: aperture gain itself changes approximately as
`1/lambda^2`, so changing frequency while holding aperture size fixed changes
more than one term. The stated invariant matters.

## Assumptions and limiting cases

This compact equation assumes free-space far-field propagation, a point target
with constant RCS, matched polarization, boresight gains, a reciprocal
monostatic path, and one lumped loss. It omits atmosphere, multipath, clutter,
fluctuating targets, coherent processing gain, pulse integration, receiver
saturation, scan loss, and detailed detection probability.

- As range approaches zero, the formula tends to infinity. That is a sign the
  far-field point-target model has left its valid region, not infinite power.
- As RCS, transmit power, or either gain approaches zero, received power tends
  to zero.
- Bandwidth does not change echo power in this equation, but it changes thermal
  noise linearly and therefore changes margin.
- A loss stated as `6 dB` becomes a divisor of `10^(6/10)`, not a subtraction
  from a value still expressed in watts.
- RCS is an effective scattering area, not necessarily the physical silhouette
  area, and it can depend strongly on angle, polarization, and frequency.

## Common interpretation mistakes

1. Using `R^-2` because free-space one-way propagation is familiar. Radar pays
   for the outward and return spreading trips.
2. Mixing dB quantities into the linear equation. Add and subtract in dB, or
   multiply and divide linear ratios, but do not mix the two representations.
3. Confusing dBW and dBm. The numeric dBm value is 30 dB above dBW for the same
   power.
4. Treating a positive deterministic margin as guaranteed detection. Noise,
   target fluctuation, threshold choice, and processing determine probability.
5. Treating fixed gain and fixed aperture as the same frequency experiment.
6. Reading one anchored point as proof of the range law instead of checking the
   slope over a meaningful interval.

## Dependencies and DSP/radar connection

This module uses only base MATLAB and explicit arithmetic. It builds on P27's
finite-noise-measurement intuition and P28's separation of power margin from
detection probability. The same bookkeeping feeds later waveform, integration,
clutter, and CFAR modules: those processors can provide gain or alter the
threshold model, but none makes the two-way geometric range cost disappear.

## Interactive lab: Build a Radar Power-Budget Experiment

**Guiding question:** How quickly does received echo power fall with range?

The range grid is 1–120 km in 0.5 km steps. Both antenna gains are fixed at 35 dBi; carrier is 10 GHz, lumped loss 6 dB, input reference temperature 290 K, bandwidth 1 MHz, noise figure 4 dB and required SNR 13 dB. Seed 2901 generates 4096 complex-noise samples. Fixed gain is not fixed physical aperture.

### Predict, sweep, explain

Predict the cost of doubling range before inspecting the curves. Can one agreement at 40 km prove that the spreading law is correct?

1. Start at the baseline. Change only **Rcs m2** from 1 to 0.1 m². Predict and explain the change using the source equation, then reset.
2. Start at the baseline. Change only **Transmit power kw** from 100 to 400 kW. Predict and explain the change using the source equation, then reset.
3. Enable the broken case. The anchored R^-2 model agrees at 40 km but loses only 20 dB per decade. It omits one propagation trip.
4. Recovery: Disable the failure to restore R^-4 and the same private noise bank. Restore both controls and disable the toggle to reproduce the selected baseline exactly.

### Focused check and teach-back

Predict the cost of doubling range before inspecting the curves. Can one agreement at 40 km prove that the spreading law is correct? Explain your answer using a measured value and units, then describe the failure and the recovery assumption.

### Common mistakes

The anchored R^-2 model agrees at 40 km but loses only 20 dB per decade. It omits one propagation trip. Avoid treating a clean seeded demonstration as field performance.

### Scope of this lab

The pinned source lesson above describes the original MATLAB model. This interactive version uses bounded NumPy arrays and the same physical stages, with an independent numerical reference. Vectorized sums and linear convolution replace nested MATLAB accumulation loops without circular wrapping. NumPy seeds are reproducible but are not MATLAB RNG parity. MATLAB figure cleanup and console output become plots and metrics. Line displays retain at most 512 points; heatmaps retain at most 128 columns and 64 rows, while calculations use the full stated arrays. No MATLAB execution, visual/accessibility review, hardware, or learner-effectiveness claim is made.
