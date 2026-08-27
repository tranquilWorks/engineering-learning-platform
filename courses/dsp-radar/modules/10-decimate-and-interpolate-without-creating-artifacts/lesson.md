# Decimate and Interpolate Without Creating Artifacts

> **Guiding question:** Why must filtering accompany sample-rate changes?

## Guiding question

Why must filtering accompany sample-rate changes?

## Physical mental model

A sampler is a frequency ruler. Lowering the sample rate shortens that ruler:
after decimation by \(M\), the new Nyquist limit is

\[
f_{N,\mathrm{new}}=\frac{F_s/M}{2}.
\]

Anything above that limit does not disappear when samples are dropped. It
folds into the shorter ruler and becomes indistinguishable from legitimate
low-frequency content. An anti-alias low-pass filter must remove what will not
fit **before** the irreversible sample selection.

Interpolation reverses the sample-count change, not the lost information.
Putting \(L-1\) zeros between samples creates room on the time grid, but it
also repeats the low-rate spectrum around multiples of the low sample rate.
A reconstruction low-pass filter keeps the baseband copy, removes those
images, and applies gain \(L\) to undo the amplitude dilution from the zeros.

## The two operations made visible

For decimation by \(M\), the script shows both paths:

\[
y_{\text{naive}}[m]=x[mM],
\qquad
y_{\text{proper}}[m]=\sum_k h_{AA}[k]x[mM-k].
\]

The baseline starts at \(F_s=2400\) samples/s and uses \(M=4\), so the new
sample rate is 600 samples/s and new Nyquist is 300 Hz. The 90 Hz tone fits.
The 420 Hz tone does not, and naive decimation maps it to

\[
f_{alias}=|420-1(600)|=180\ \text{Hz}.
\]

Once 420 Hz and 180 Hz share the same low-rate samples, no later filter can
know which physical tone produced them. The fixed 240 Hz anti-alias FIR acts
while they are still distinct at the original sample rate.

For interpolation by \(L=4\), zero insertion is explicit:

\[
z[n]=
\begin{cases}
y[n/L], & n\ \text{is a multiple of}\ L,\\
0, & \text{otherwise}.
\end{cases}
\]

The retained 90 Hz spectrum is repeated at \(600-90=510\) Hz,
\(600+90=690\) Hz, and around later multiples of 600 Hz. Filtering with
\(Lh_{RC}[k]\) retains the baseband, rejects the images, and restores a
unit-amplitude input tone toward one volt.

## Why one filter cannot be moved to the other side

- The decimation filter must precede sample dropping because aliasing merges
  different original frequencies. Filtering afterward can remove a low-rate
  bin only by also removing any desired signal already in that bin.
- The interpolation filter must follow zero insertion because the images are
  created by the zero-stuffed sequence. The low-rate input has no samples at
  those high-rate image frequencies to filter beforehand.
- The two FIR coefficient shapes can be related, but the interpolation path
  needs gain \(L\); otherwise the desired spectral line remains about \(1/L\)
  of its original amplitude.

## Limiting cases

- \(M=1\) or \(L=1\): no sample-rate change, so this particular alias/image
  mechanism vanishes.
- A signal already confined safely below new Nyquist: an ideal anti-alias
  filter changes no wanted content, but a practical transition band still
  requires margin.
- A tone exactly at new Nyquist: its sampled phase can make the endpoint
  fragile; do not treat equality as safe design margin.
- Zero insertion without reconstruction: sample count increases, information
  does not, baseband amplitude falls by \(L\), and images remain.
- An ideal brick-wall FIR: perfect separation requires infinite duration.
  Finite filters trade transition width, ripple, image rejection, delay, and
  arithmetic cost.
- A very short reconstruction FIR: it smooths the zero-stuffed waveform but
  may leave appreciable images. More taps sharpen the transition while adding
  delay and work.

## Radar connection and common interpretation mistakes

Radar receivers often decimate after digital downconversion to reduce data
rate before pulse compression, Doppler processing, or detection. Energy
outside the intended complex baseband must be rejected before that reduction;
otherwise an interferer or noise band can fold into target-bearing bins.
Interpolation appears in waveform generation, timing changes, channelization,
and matched sample-rate interfaces, where images can become unwanted emitted
or processed bands.

Common mistakes:

- “Dropping samples removes high frequencies.” It only changes their digital
  identity; without filtering they fold.
- “A 180 Hz peak after decimation proves a 180 Hz input.” In the broken case it
  came from 420 Hz.
- “Zeros are a smooth estimate between measurements.” They are an intermediate
  sequence whose spectral replicas still require filtering.
- “More output samples mean recovered detail.” Interpolation constructs a
  band-limited representation; it cannot restore content discarded before
  decimation.
- “Any low-pass cutoff below original Nyquist is safe.” The relevant boundary
  is the **new** Nyquist limit, including practical transition margin.

## Dependency connection

P09 established that a practical FIR has passband, transition, stopband,
delay, and finite arithmetic cost. P10 uses those behaviors for a physical
job: protect a narrower sampled bandwidth before decimation and isolate one
spectral copy after interpolation. P03 supplies the visual meaning of aliasing;
P10 shows how a rate-change system prevents it rather than merely observing it.

## Use the Python GUI experiment

The GUI keeps the pinned source's mental model and processing order visible. The **rate change factor** control scales the primary source variable around its documented baseline; **secondary stress** isolates the next important effect; the noise control uses a fixed retained seed so reruns are comparable.

### Prediction and sweep 1 — rate change factor

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
