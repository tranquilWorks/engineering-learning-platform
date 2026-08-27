# Derive FMCW Range from Beat Frequency

> **Guiding question:** Why does a delayed chirp produce a nearly constant beat frequency?

## Guiding question

Why does a delayed chirp produce a nearly constant beat frequency?

## Physical mental model

Picture two rulers whose tick marks slide upward in frequency at the same
rate. One ruler is the transmitted chirp. The echo ruler starts later because
the wave travels to the target and back. During the interval where both rulers
exist, the vertical gap between parallel ramps is constant. The mixer turns
that frequency gap into a tone.

P17 established complex mixing, P30 made `tau = 2R/c` physical, P31 separated
resolution from accuracy, and P32 exposed linear-FM phase. P68 is the governed
batch prerequisite; P69 begins the FMCW sequence.

## Build the chirp from phase

For bandwidth `B`, chirp duration `T`, and slope in hertz per second,

```text
S = B/T.
```

The script uses a centered complex-baseband up-chirp:

```text
x_tx(t) = exp(j pi S (t - T/2)^2),   0 <= t < T.
```

Its instantaneous frequency is the phase derivative divided by `2 pi`:

```text
f_tx(t) = S(t - T/2).
```

Centering puts the sampled sweep between `-B/2` and `+B/2`. A physical RF
carrier would add the same common carrier term to transmit and receive; ideal
dechirping removes it, so it need not be sampled here.

## Delay the time argument, not the array circularly

For a stationary monostatic target at range `R`,

```text
tau = 2R/c.
```

The ideal attenuated echo is `a x_tx(t-tau)` only when `tau <= t < T`.
Before `tau` there is no echo from this chirp. The script evaluates the phase
at `t-tau` and gates that valid overlap; it does not wrap late samples to the
beginning with a circular shift.

The received instantaneous frequency during overlap is

```text
f_rx(t) = S(t - tau - T/2).
```

The two ramps have equal slope, so their gap is independent of `t`:

```text
f_tx(t) - f_rx(t) = S tau.
```

## The mixer sign is explicit

P69 forms

```text
y(t) = x_tx(t) conj(x_rx(t)).
```

Ignoring attenuation and noise, its phase is

```text
angle y(t) = 2 pi S tau (t - T/2) - pi S tau^2,
```

so an up-chirp produces the positive beat

```text
f_b = S tau.
```

Reversing the conjugation order would produce `-f_b`. Magnitude alone can hide
that error; the script asserts and plots the chosen sign.

## Beat frequency becomes range

Substitute the round-trip delay into the beat law:

```text
f_b = S(2R/c),
R = c f_b/(2S).
```

The FFT estimates the positive beat peak. A manually constructed Hann window
reduces overlap-edge leakage, zero padding samples the displayed spectrum more
finely, and a three-bin parabola refines the peak. None of those operations
changes the physical bandwidth or creates new target-separation information.

The phase-increment estimate is retained as a transparent cross-check:

```text
f_phase = angle(sum(conj(y[n]) y[n+1]))) fs/(2 pi).
```

It is not substituted for the required FFT path.

## Sweep 1: range changes the gap

The range sweep uses `15, 30, 45, 60, 75 m`. Bandwidth, duration, slope,
attenuation, sample grid, FFT, and the deterministic noise record stay fixed.
Round-trip delay and beat frequency grow linearly with range. Converting each
peak with the unchanged slope makes estimated range follow known range.

## Sweep 2: slope changes the gap, not the target

The slope sweep holds `R = 45 m` and `T = 40 us` while changing bandwidth from
`10` to `30 MHz`. Thus only `S = B/T` changes. Steeper ramps create a larger
frequency separation for the same delay:

```text
f_b proportional to S,   but   c f_b/(2S) approximately constant.
```

Using the baseline slope for every case would be a conversion mistake. Each
case must use the slope that generated its chirp.

## Broken case and recovery

The broken calculation uses

```text
R_wrong = c f_b/S.
```

That treats the measured delay as one-way travel and returns twice the
monostatic range. The signal, FFT peak, seed, and slope have not failed. The
interpretation has. Recovery reuses the exact same measured `f_b` and restores
the factor two:

```text
R_recovered = c f_b/(2S).
```

## Limiting cases and claim boundary

- As `R -> 0`, `tau -> 0` and the ideal beat approaches DC. Leakage and direct
  feedthrough then matter in a real sensor.
- As `S -> 0`, a constant-frequency waveform has no delay-proportional FMCW
  beat; this measurement cannot infer range from `f_b/S` at zero slope.
- If `tau >= T`, this one-chirp record has no transmit/echo overlap to mix.
- If `B` reaches the sample rate in complex baseband, the swept band reaches
  Nyquist and aliases. The reviewed controls keep `B < fs`.
- If the beat reaches `fs/2`, the sampled tone aliases. The full sweep is
  checked below that limit.
- The ideal range-resolution scale is `c/(2B)`. Zero padding can make a single
  clean peak estimate look smoother; it does not make two close targets
  resolvable.
- Target motion adds Doppler to the beat and can bias one-chirp range. That
  coupling belongs to P70/P71 and is intentionally absent here.
- Chirp nonlinearity makes the frequency gap vary with time, broadening or
  distorting the beat instead of producing the ideal narrow tone.

Static repository checks and a standard-library numerical oracle validate the
model contract and deterministic premise. They do not execute MATLAB, inspect
rendered figures, or establish RF, bench, hardware/HIL, real-time, field, or
operational performance.

## Common interpretation mistakes

- Omitting the factor two confuses one-way and round-trip propagation.
- Reversing mixer order without tracking sign can move the beat to negative
  frequency.
- Mixing pre-echo samples treats receiver noise as though a valid beat exists.
- Calling zero-padding improved range resolution confuses display sampling
  with bandwidth.
- Holding bandwidth fixed while claiming a slope-only sweep is impossible if
  duration also stays fixed; P69 varies bandwidth and holds duration.
- Applying one baseline slope to every slope-sweep peak biases the recovered
  ranges.
- Treating the received ramp as having a different slope misses why the gap is
  constant for an ideal linear chirp.
- Calling a simulated complex-baseband tone a validated RF radar measurement
  exceeds the evidence.

## Use the Python GUI experiment

The GUI keeps the pinned source's mental model and processing order visible. The **target range** control scales the primary source variable around its documented baseline; **secondary stress** isolates the next important effect; the noise control uses a fixed retained seed so reruns are comparable.

### Prediction and sweep 1 — target range

Hold secondary stress at 0.25 and predict the response at 0.6×, 1.0×, and 1.4× baseline. State which axis feature should move, which metric should change monotonically, and which quantity should remain invariant. Run those three cases and explain any departure using the governing equations above.

### Sweep 2 — secondary stress

Restore the primary scale to 1.0. Sweep secondary stress through 0.0, 0.5, and 1.0. Separate a genuine model change from a display-scale change, and connect the response to the source lesson's limiting cases.

### Intentionally broken case and recovery

Enable **Violate the central model assumption**. The experiment applies a deterministic ambiguity, contamination, association error, or coherent-processing error appropriate to this curriculum phase. Name the violated assumption before looking at the warning callout. Recover by disabling broken mode, returning primary scale to 1.0 and secondary stress to 0.25, and verifying that the original invariant returns.

## Common mistakes to avoid in the GUI

- Changing two controls at once and attributing the result to only one.
- Reading a smooth plotted line as information that was never measured or modeled.
- Ignoring axis units, normalization, sign, or the finite record/resource ceiling.
- Treating the broken response as random software behavior instead of a named assumption failure.

## Teach-back checklist

- [ ] Answer the guiding question in two or three sentences.
- [ ] Explain every symbol in at least one governing equation before invoking a processing shortcut.
- [ ] Predict and verify both one-variable sweeps.
- [ ] Identify the broken assumption from the plot and metric changes.
- [ ] Demonstrate the recovery and state what remains unproved by this software-only experiment.
