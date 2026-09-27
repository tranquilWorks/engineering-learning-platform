# P25 Lesson: Create and Equalize a Multipath Channel

## Guiding question

How do delayed copies distort symbols even when noise is small?

## Physical model

A receiver rarely sees only the direct path. Reflections from buildings,
terrain, cables, or impedance discontinuities arrive later and with changed
amplitude and phase. A short discrete channel is

\[
h[n]=\sum_{p=0}^{P-1} a_p\,\delta[n-d_p], \qquad
r[n]=s[n]*h[n]+v[n].
\]

Each coefficient `a_p` is a complex path gain and each `d_p` is a delay. The
convolution says that the receiver adds shifted copies of the pulse-shaped
waveform. P07 introduced this echo-addition view; here the copies extend into
neighboring QPSK decisions.

## Why the symbols smear

P24 arranged the transmit RRC pulse and receive matched filter so that one
isolated path has almost zero response at other symbol times. A path delayed
by one symbol moves the previous symbol directly onto the current decision:

\[
y[k]=h_0x[k]+h_1x[k-1]+h_2x[k-2]+n[k].
\]

The unwanted terms are intersymbol interference (ISI). They depend on nearby
data, so a constellation point becomes a cloud or several displaced clusters
even when `n[k]` is small. In the eye plot, those data-dependent paths cross
the decision time and close the opening.

## The same channel in frequency

The delayed copies add with a frequency-dependent phase:

\[
H(e^{j\omega})=\sum_p h_p e^{-j\omega d_p}.
\]

At some frequencies they reinforce; at others they cancel. This is
frequency-selective fading. For the broken channel
`h=[1, -0.999]`, the paths nearly cancel at zero frequency, leaving a very
deep null. The null and the eye closure are two views of the same convolution,
not separate impairments.

## What the equalizers actually do

Let `H` be the displayed convolution matrix made from the channel taps and
`w` the equalizer taps. The combined impulse response is `H*w`.

The causal zero-forcing (ZF) design in the experiment solves the leading
square system

\[
H_{\text{lead}}w_{\text{ZF}}=\delta.
\]

It cancels the first 30 postcursor terms exactly. For a moderate minimum-phase
channel this leaves a tiny tail. It also filters receiver noise, whose output
variance is proportional to

\[
\sigma_n^2\sum_m |w[m]|^2.
\]

Near a null, inverse taps must work hard. The sum of squared tap magnitudes
grows and so does the noise. A finite ZF filter also pushes uncancelled energy
into its trailing residual; it cannot recreate information that the channel
nearly removed.

The regularized/MMSE-style design instead minimizes

\[
\lVert Hw-\delta\rVert_2^2+\lambda\lVert w\rVert_2^2,
\]

so

\[
w=(H^H H+\lambda I)^{-1}H^H\delta.
\]

The script evaluates this equation with a linear solve rather than forming an
inverse. With `lambda` near the known symbol-sample noise variance, it accepts
some residual ISI to avoid enormous noise gain. This is the important trade:
MMSE does not reverse the channel perfectly; it chooses a lower total error.

## Limiting cases

- With only `h=[1]`, there is no multipath ISI and an equalizer adds no useful
  information.
- With echoes much smaller than the direct path, the spectrum has no deep
  null and both ZF and MMSE can recover tight clusters.
- As an echo approaches equal magnitude and opposite phase, the minimum of
  `|H|` approaches zero. Exact inversion becomes ill-conditioned and noise
  enhancement dominates.
- As `lambda` approaches zero, the regularized solution emphasizes channel
  inversion. As `lambda` becomes large, its taps shrink: noise gain falls but
  residual channel distortion rises.
- More equalizer taps can move the remaining ZF error farther into the tail,
  but they do not make a spectral null contain information again and they
  consume more resources.

## DSP and radar connection

Communication channels create ISI between symbols. Radar receivers meet the
same delayed-copy model as target echoes, clutter, antenna/cable ringing, and
range sidelobe coupling. Whether a delayed copy is desired or interference
depends on the processing goal. In either case, a deep transfer-function null
sets a real limit on deconvolution.

## Common interpretation mistakes

- **“High SNR means a clean constellation.”** High SNR only makes random noise
  small. Deterministic ISI can still dominate.
- **“The weakest path is always harmless.”** Its phase and delay determine
  where it cancels the other paths.
- **“ZF removes all error.”** This ZF is finite and causal; it leaves a trailing
  response and may strongly amplify noise.
- **“MMSE failed because residual ISI remains.”** MMSE deliberately leaves
  some ISI when removing it would create more noise error.
- **“An equalizer creates lost signal energy.”** It reweights observations. It
  cannot recover a frequency component that was exactly erased.

## Dependencies

P24 provides unit-energy QPSK pulse shaping, matched filtering, timing, and eye
language. P23 provides IQ decisions, P07 provides convolution as echo addition,
and P09 provides FIR/frequency-response language. The experiment uses base
MATLAB and exposes every essential operation; it does not use `comm.LinearEqualizer`,
`equalize`, `awgn`, `rcosdesign`, or another Communications Toolbox black box.

## Interactive lab: Create and Equalize a Multipath Channel

There are 480 QPSK symbols, eight samples per symbol, a span-8 rolloff-0.25 RRC and Es/N0=18 dB. The baseline paths are [1,0.45 exp(j0.45),0.20 exp(-j0.80)] with delays [0,1,2] symbols. Equalizers have 31 taps; metrics exclude 40 symbols at each end. A fixed 3920-sample NumPy noise bank is reused across channels, unlike the sequential MATLAB noise draws. The symbol-rate equalizer models the delayed path coefficients; finite RRC truncation remains visible in the complete sampled response. This is a finite regularized least-squares inverse, not an assertion of an exact colored-noise Wiener solution.

### Predict, manipulate, explain

Predict which equalizer has larger noise gain near a channel null. Can a regularized inverse reduce EVM while retaining more impulse-response distortion?

1. Start at the baseline. Change only **One-symbol echo magnitude** from 0.45 to 0.75 ratio. Inspect its dedicated sweep and the primary processing plots. Explain which equation predicts the observed change before resetting.
2. Start at the baseline. Change only **Equalizer regularization** from 0.0158489 to 0.1 ratio. Inspect its dedicated sweep and the primary processing plots. Explain which equation predicts the observed change before resetting.
3. Enable the broken case. The [1,-0.999] path has a -60 dB DC null. Finite ZF inversion boosts noise and leaves a tail: its symbol EVM and noise gain reveal the cost.
4. Recovery: The deep-null comparison uses lambda=0.01, nearest the 18 dB noise variance in the source grid. Regularization reduces noise enhancement but retains reported residual distortion; it does not perfectly recover lost information. Disable the toggle and restore both controls to reproduce baseline exactly.

### Focused check and teach-back

Predict which equalizer has larger noise gain near a channel null. Can a regularized inverse reduce EVM while retaining more impulse-response distortion? Explain your answer using one measured value, its units, and the relevant equation. Then describe the failure, the recovery assumption, and one limit of the model.

### Common mistakes

A finite ZF inverse neither removes all tails nor avoids noise amplification at a null.

### Scope of this lab

The source equations and processing stages above are retained. NumPy seeds make the software repeatable, but the random-number stream is not claimed to match MATLAB. MATLAB figure-window cleanup and console printing are replaced by the plots and metrics here. Plot traces are bounded to 512 displayed samples; calculations use the full stated record. This lab is a simulation, not a hardware measurement.
