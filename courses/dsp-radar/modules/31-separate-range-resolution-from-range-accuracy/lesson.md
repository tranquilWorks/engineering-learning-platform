# Separate Range Resolution from Range Accuracy

> **Guiding question:** Why can an estimate be precise even when two targets cannot be resolved?

## Guiding question

Why can an estimate be precise even when two targets cannot be resolved?

## Physical model: width versus location

Imagine painting one bright stripe with a brush. You may locate the center of
that stripe very accurately even though the brush is too wide to paint two
nearby stripes without their paint merging. A radar pulse has the same two
ideas:

- **response width** controls whether two targets produce distinguishable peaks;
- **peak-location error** says how far one estimated range is from the true
  range under a stated model.

Those are resolution and accuracy, respectively. Precision is narrower still:
it describes repeatability, such as the standard deviation across noise trials.
This lesson reports bias, standard deviation, and RMSE so the words do not get
silently interchanged.

## From bandwidth to a range response

The experiment transmits a real Gaussian envelope

```text
s(t) = exp(-t^2 / (2 sigma_t^2))
```

truncated at four time standard deviations and normalized to unit energy. Its
declared `B` is the two-sided half-power (−3 dB) bandwidth of the untruncated
Gaussian spectrum. That convention gives

```text
sigma_t = sqrt(log(2)) / (pi B).
```

The receiver delays zero-extended copies of this pulse. For a monostatic radar,

```text
tau = 2R/c,                 R = c tau / 2.
```

At every candidate lag `ell`, the script exposes the matched-filter operation

```text
y[ell] = sum_m x[ell + m] conj(s[m]).
```

No `xcorr`, `findpeaks`, `awgn`, or phased-array toolbox call hides the signal
flow. A single echo produces the pulse autocorrelation. Increasing bandwidth
shortens the pulse and narrows that matched response, so a fixed target spacing
can change from one blended maximum to two local maxima.

The familiar

```text
Delta R_nominal = c / (2B)
```

is retained as a useful nominal radar scale, not advertised as an exact
universal coefficient. Pulse shape, weighting, and the chosen separation
criterion change the coefficient. The experiment therefore also measures the
actual full −3 dB width of its sampled matched response and reports both values.

## Accuracy can be sub-response-width

For one isolated target, the integer peak chooses one range sample. Three-point
parabolic interpolation uses the curvature around that same maximum to estimate
its location between samples. With adequate SNR and a correct single-target
model, its error can be much smaller than either a range bin or the matched
response width.

That is not new resolution. Interpolation uses the shape and samples already
present; it does not add independent waveform bandwidth. The SNR sweep keeps
the pulse, sample rate, target, gate, and estimator fixed. Higher SNR reduces
the noise-driven spread of the estimate, while the measured response width is
unchanged.

## The blended-peak trap

Two close equal echoes add before peak estimation. If their spacing is below
what this waveform can distinguish, the matched response has one physical local
maximum. A dense interpolated plot can draw that one crest smoothly. Selecting
the two largest adjacent display samples and calling them two targets is the
intentionally broken method: it confuses display density with independent
information.

The blended maximum is also not an accurate estimate of either target. Under a
wrong one-target model it is generally biased toward a mixture-dependent
location. More SNR makes that wrong blended shape cleaner; it does not make the
two ranges identifiable.

## Assumptions and limiting cases

- Targets are stationary point echoes with equal amplitude in the resolution
  demonstrations; unequal amplitudes make the weaker one harder to separate.
- Delays are inserted before sampling with zero extension, so no echo wraps
  around the capture.
- The single-target accuracy sweep uses a declared range gate. It is an
  estimation experiment, not a global detection or false-alarm claim.
- Very low SNR can select a noise maximum. Model mismatch, multipath,
  calibration bias, sidelobes, and target extent can dominate even at high SNR.
- Sampling must be fast enough for the widest pulse bandwidth. More samples
  improve numerical representation but do not replace transmitted bandwidth.
- The Gaussian is truncated, so the measured sampled response—not the ideal
  infinite-duration formula—is authoritative for the plotted width.

## Common interpretation mistakes

1. **“A 1 m error means 1 m resolution.”** Error for one target does not prove
   that two targets 1 m apart can be separated.
2. **“More interpolation creates more bandwidth.”** It only produces a denser
   representation of existing samples.
3. **“Higher SNR always resolves the pair.”** SNR helps visibility, but it does
   not remove waveform overlap or repair an unidentifiable model.
4. **“`c/(2B)` is exact for every pulse.”** It is a convention-dependent scale;
   this lab also measures the actual response width.
5. **“Two largest bins mean two targets.”** Adjacent bins can belong to one
   broad peak. Distinct local maxima and an explicit criterion are required.

## Dependencies and concept connection

P08 supplies the correlation mental model. P13 already showed that a denser FFT
display does not create true spectral resolution; the same warning applies to
range interpolation here. P28 distinguished estimator bias/variance from
detection, and P30 established round-trip delay and `c*tau/2`. P32 will change
the waveform through pulse compression; this lesson first keeps the core
resolution-versus-accuracy distinction visible with a simple envelope.

## Use the Python GUI experiment

The GUI keeps the pinned source's mental model and processing order visible. The **target separation** control scales the primary source variable around its documented baseline; **secondary stress** isolates the next important effect; the noise control uses a fixed retained seed so reruns are comparable.

### Prediction and sweep 1 — target separation

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
