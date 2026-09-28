# Lesson: motion inside the target

## Guiding question

How do rotating or swinging target parts produce time-varying Doppler around bulk motion?

## One target can contain several velocities

A conventional point-target description gives one range and one radial
velocity. A walking person is not one rigid point. The torso may approach at a
nearly steady speed while arms and legs alternately move faster and slower
than the torso. Each scattering part contributes its own coherent phasor to
the selected range-bin return.

This experiment uses three ideal point scatterers: a strong torso and two
weaker, oppositely swinging limbs. It is deliberately small enough that every
stage remains visible. P70 supplies the selected FMCW range-bin viewpoint;
fast-time range processing is not repeated here.

## From component motion to coherent phase

Positive radial velocity means approaching. For component `i`,

```text
v_i(t) = v_bulk + v_micro,i(t)
f_d,i(t) = 2 v_i(t) / lambda
```

where `lambda = c/f_c`. A sinusoidal limb model is

```text
v_limb,A(t) = v_bulk + v_swing cos(2 pi f_swing t)
v_limb,B(t) = v_bulk + v_swing cos(2 pi f_swing t + pi).
```

Velocity must be integrated before constructing phase. The associated radial
advance is

```text
d_i(t) = integral from 0 to t of v_i(u) du.
```

The selected dechirped range-bin convention inherited from P70-P73 is

```text
x_i(t) = a_i exp(-j 4 pi d_i(t)/lambda + j phi_i).
```

Thus approaching motion has negative raw slow-time FFT frequency. The script
reverses both the complex FFT rows and their axis before plotting so the
displayed physical Doppler `f_d = +2v/lambda` increases left to right. Reversing
only the labels would be wrong.

Writing `exp(-j 2 pi f_d(t)t)` would not model time-varying velocity correctly:
its phase derivative contains an extra `t df_d/dt` term. Direct displacement,
or equivalently integrated Doppler, avoids that mistake.

The received signal is the coherent sum

```text
x(t) = sum_i x_i(t) + n(t).
```

Because phasors add before magnitude is taken, their cancellation can create
amplitude nulls and composite-phase jumps. The raw unwrapped phase is useful
evidence that motion is present, but its local slope is not a trustworthy label
for any one body part near a cancellation.

## What the dwell-wide spectrum loses

A full-record FFT projects all four seconds onto constant-frequency bins. The
strong torso creates energy near the bulk Doppler. Periodic limb phase
modulation spreads energy through a sideband pattern. That spectrum proves the
return is not one pure Doppler tone, but it cannot say when a limb was above or
below the torso velocity. A sideband line is not automatically a separate
constant-velocity target.

## The explicit STFT

For frame `m`, the script extracts a finite section, multiplies it by an
explicit Hann window, and computes a two-sided complex FFT:

```text
X[m,k] = sum_n x[n + mH] w[n] exp(-j 2 pi k n/Nfft).
```

`H` is the hop. `fftshift` exposes negative and positive raw frequencies; the
row-and-axis reversal then maps them to signed physical Doppler. Frame time is
the center of the window, not its first sample. No `spectrogram`, `stft`,
`pspectrum`, `instfreq`, or toolbox window call hides these operations.

The spectrogram shows a near-horizontal torso ridge around `+192 Hz` and
periodic limb energy sweeping about `+/-320 Hz` around it. Track crossings and
coherent interference can make a local maximum switch identity; the theoretical
component tracks are guides, not detector declarations.

## Three controlled changes

### Peak swing speed

Changing only `v_swing` changes the micro-Doppler extent

```text
Delta f_micro = 2 v_swing / lambda.
```

The bulk ridge and swing repetition rate stay fixed. Faster limbs spread the
periodic tracks farther above and below bulk Doppler. The experiment uses one
fixed nominal scatterer-power noise scale and reuses the same deterministic
additive-noise record in all three cases, so background
changes cannot masquerade as a speed effect.

### Carrier frequency

At fixed physical velocities, Doppler in hertz scales with carrier:

```text
f_d = 2 v f_c / c.
```

The `10`, `24`, and `77 GHz` cases show increasing bulk offset and micro-Doppler
width in hertz. Converting each axis back with `v = lambda f_d/2` would recover
the same physical velocities. This is wavelength sensitivity, not faster
motion.

### STFT window duration

All window cases process the exact same complex record on the same zero-padded
FFT display grid. The physical finite-window response is set approximately by
`1/T_window`, not by the displayed bin spacing:

- a short window follows rapid motion in time but spreads each local Doppler;
- a long window narrows constant-frequency response but averages across a
  larger fraction of the swing and smears curved tracks;
- overlap changes report density, not independent physical resolution.

Zero-padding provides a denser display between samples of the window response;
it does not manufacture a longer observation.

## The intentionally broken case

The broken path evaluates `abs(x)` before the STFT. The common bulk phasor is
removed, signed rotation is lost, and the strongest energy collapses toward
DC. Relative beating between coherent parts can remain, so the magnitude-only
plot is not required to be featureless; it simply cannot retain absolute
signed bulk and component Doppler.

Recovery does not synthesize a cleaner target or change a parameter. It reruns
the explicit STFT on the unchanged complex measurement. An equality assertion
protects that same-data boundary.

## Limiting cases and model boundaries

- `v_swing = 0`: all parts share bulk Doppler; the periodic spread vanishes.
- `v_bulk = 0`: the torso lies at zero while limb tracks cross positive and
  negative Doppler.
- `f_c -> 0`: Doppler in hertz shrinks for the same physical velocity.
- `f_swing = 0`: the sinusoidal displacement formula is undefined; this
  experiment rejects that malformed control rather than silently changing the
  model.
- A window as long as the dwell approaches the dwell-wide spectrum and loses
  most timing information.
- Slow-time Doppler must remain inside Nyquist. Aliased tracks can fold and
  imitate a different component velocity; validation checks the worst reviewed
  speed at the highest carrier before allocation.
- At exact phasor cancellation, composite phase is ill-conditioned even though
  every component phase is well-defined.
- Several scattering parts in one range cell cannot be uniquely associated
  merely by tracing the brightest spectrogram pixel through a crossing.

The synthetic point-scatterer model omits range migration, aspect-dependent
RCS, occlusion, multipath, acceleration outside the sinusoid, antenna pattern,
phase noise, clutter, leakage from adjacent range bins, and classifier logic.
It is not a biomechanical walking model or rotor certification case.

## Dependencies, resources, and compatibility

P15 provides STFT intuition, P18 signed I/Q, P36 coherent Doppler phase, P70
the selected-range-bin context, and P73 the governed prerequisite. The script
targets base MATLAB R2016b or newer with no optional toolbox. It is synchronous:
no worker, timer, network, hardware, or external persistent state is created.

The reviewed ceilings are 20,000 slow-time samples, 4,096 STFT FFT points,
65,536 dwell-spectrum FFT points, 1,000 frames per STFT, five cases per sweep,
50,000 private generator values, 15,000,000 eight-byte live-workspace value
equivalents (complex values count twice and container overhead is included),
and five tagged figure groups. Static tests and a Python oracle do not prove MATLAB
runtime, plot legibility, educational effectiveness, RF behavior, hardware/HIL,
bench, real-time RT1/RT2, field, Unreal, signing, deployment, staging,
production, or operational-radar performance.

## Interactive lab: Create a Micro-Doppler Spectrogram

**Guiding question:** How do rotating or swinging target parts produce time-varying Doppler around bulk motion?

Seed 7401; carrier 24 GHz, fs 4800 Hz, 4 s. Torso 1.2 m/s and opposite limbs with 2 m/s peak swing at 1.5 Hz have voltages 1/.35/.28 and phases 0/.7/-.9. Analytic integration supplies phase=-4 pi advance/lambda. A 512 sample Hann, 384 overlap and 2048 FFT baseline retains 147 frames. Speed 1/2/3 m/s uses seed 7501; carrier 10/24/77 GHz uses 7601; window 192/512/1536 reuses baseline data. Full spectra are computed before display reduction.

### Predict, sweep, explain

Predict the torso Doppler and limb extrema from physical velocity. Why do carrier frequency and STFT window length change different aspects of the spectrogram, and why is magnitude-only motion evidence incomplete?

1. Start at the baseline. Sweep only **Swing speed m/s** from 2 to 3 m/s. Predict, run, and explain a measured value using the governing equation; then reset.
2. Start at the baseline. Sweep only **Window samples** from 512 to 1536 samples. Predict, run, and explain a measured value using the governing equation; then reset.
3. Enable the broken case. Absolute value of the slow-time IQ record removes carrier phase and signed bulk Doppler; magnitude fluctuations cannot reconstruct the original motion phase.
4. Recovery: Use the retained unchanged complex IQ record. The plots use full STFT calculations; display coordinates are decimated and zero-padding is not independent frequency resolution.

### Focused check and teach-back

Predict the torso Doppler and limb extrema from physical velocity. Why do carrier frequency and STFT window length change different aspects of the spectrogram, and why is magnitude-only motion evidence incomplete? Support the explanation with a measured value and units, and state the recovery assumption.

### Common mistakes

Absolute value of the slow-time IQ record removes carrier phase and signed bulk Doppler; magnitude fluctuations cannot reconstruct the original motion phase. Distinguish the selected-control scene from a named separate failure scene.

### Scope of this lab

The pinned source lesson is preserved above. Private Park–Miller uniforms retain zero offset; P65–P72 split radius/phase uniform blocks and P73–P76 interleave them. Matrix inputs retain column-major ordering. P75 shorter apertures crop the full baseline noise record to isolate aperture changes. MUSIC missing-peak penalties and truth-defined audit neighborhoods are disclosed; neither manufactures successful detections. Source figures become labeled native plots; full arrays drive calculations before display decimation. Sixty independent software comparisons cover five scenarios per lesson. No MATLAB execution, browser/accessibility, learner, hardware or production validation is claimed.
