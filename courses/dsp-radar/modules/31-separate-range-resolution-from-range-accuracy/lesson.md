# Lesson: resolution is not an error bar

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

## Interactive lab: Separate Range Resolution from Range Accuracy

**Guiding question:** Why can an estimate be precise even when two targets cannot be resolved?

The Gaussian pulse has two-sided half-power bandwidth B, time sigma sqrt(log(2))/(πB), four-sigma truncation and unit energy. Sampling is 80 MHz, record length 960 and isolated range 900.37 m. Resolution scenes use 50 dB matched SNR; 128 trials at 0/15/30 dB report bias, sample standard deviation and RMSE inside a ±80 m gate. Width follows the source sampled-bin convention, not an interpolated width. NumPy uses row-major noise draws; MATLAB streams are not reproduced.

### Predict, sweep, explain

Predict which improves with more SNR: isolated-target accuracy or the physical width of this fixed waveform. Can two adjacent display samples be counted as two targets?

1. Start at the baseline. Change only **Bandwidth mhz** from 4 to 8 MHz. Predict and explain the change using the source equation, then reset.
2. Start at the baseline. Change only **Target separation m** from 22 to 45 m. Predict and explain the change using the source equation, then reset.
3. Enable the broken case. Selecting the two largest adjacent interpolated samples invents a second target within one crest.
4. Recovery: Disable the false count; count physical local maxima. Increase actual bandwidth to 8 MHz to resolve the baseline 22 m pair. Restore both controls and disable the toggle to reproduce the selected baseline exactly.

### Focused check and teach-back

Predict which improves with more SNR: isolated-target accuracy or the physical width of this fixed waveform. Can two adjacent display samples be counted as two targets? Explain your answer using a measured value and units, then describe the failure and the recovery assumption.

### Common mistakes

Selecting the two largest adjacent interpolated samples invents a second target within one crest. Avoid treating a clean seeded demonstration as field performance.

### Scope of this lab

The pinned source lesson above describes the original MATLAB model. This interactive version uses bounded NumPy arrays and the same physical stages, with an independent numerical reference. Vectorized sums and linear convolution replace nested MATLAB accumulation loops without circular wrapping. NumPy seeds are reproducible but are not MATLAB RNG parity. MATLAB figure cleanup and console output become plots and metrics. Line displays retain at most 512 points; heatmaps retain at most 128 columns and 64 rows, while calculations use the full stated arrays. No MATLAB execution, visual/accessibility review, hardware, or learner-effectiveness claim is made.
