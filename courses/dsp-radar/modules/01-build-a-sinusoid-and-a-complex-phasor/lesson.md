# Build a Sinusoid and a Complex Phasor

**Mental model:** A sinusoid is a rotating vector's shadow.

## Guiding question

**How do amplitude, frequency, and phase appear in time and in the complex plane?**

This first experiment deliberately builds the signal from its equation. There
is no signal-generator shortcut hiding the relationship you are trying to see.

## Physical mental model

Imagine a pointer of length (A) rotating around the origin. Its complex
position is

\[
z(t)=A e^{j(2\pi f_0t+\phi)}
    =A\cos(2\pi f_0t+\phi)+jA\sin(2\pi f_0t+\phi).
\]

The horizontal and vertical coordinates are

\[
I(t)=\operatorname{real}\{z(t)\},\qquad
Q(t)=\operatorname{imag}\{z(t)\}.
\]

The real cosine is not merely similar to the complex motion. It is exactly the
horizontal projection:

\[
x(t)=A\cos(2\pi f_0t+\phi)=I(t).
\]

Follow the ordered points in the IQ plot. A static circle proves the radius,
but only sample order shows rotation direction.

## Signal flow

1. Choose (A), signed (f_0), (phi), sample rate (f_s), and duration.
2. Build sample instants (t_n=n/f_s), without including a duplicate endpoint.
3. Compute the shared angle (	heta_n=2\pi f_0t_n+\phi).
4. Form (z[n]=Ae^{j\theta_n}).
5. Project (z[n]) onto I and Q; verify (x[n]=I[n]) and (|z[n]|=A).
6. Compare positive and negative frequency using ordered IQ samples.
7. Sweep one parameter at a time, then deliberately undersample the tone.

That order matters: the equation establishes what the code must do before
NumPy performs the vectorized exponential.

## What each control changes

- **Amplitude (A)** is peak height in the time plot and radius in the IQ
  plot. Receiver gain scales I and Q together; it does not create a frequency
  shift.
- **Frequency (f_0)** is cycles per second. Its magnitude sets angular rate
  (omega_0=2\pi|f_0|); its sign sets rotation direction.
- **Phase (phi)** is the angle at (t=0). It moves the starting point without
  changing radius or rotation rate.
- **Sample rate (f_s)** sets the measurement spacing. It does not change the
  underlying continuous-time equation, but it determines whether frequency is
  identifiable from the samples.
- **Duration** changes how many cycles are observed, not the cycles-per-second
  rate.

With I to the right and Q upward, positive complex frequency rotates
counterclockwise and negative frequency rotates clockwise. This signed phase
slope is why complex receiver data can distinguish opposite mixer offsets or
Doppler directions after a convention is chosen.

A real cosine alone cannot preserve that sign because

\[
\cos(2\pi f_0t+\phi)=\tfrac12e^{j(2\pi f_0t+\phi)}
                     +\tfrac12e^{-j(2\pi f_0t+\phi)}.
\]

## Predict the baseline before running

The committed baseline is (A=1), (f_0=5\) Hz, (phi=\pi/6),
(f_s=200\) Sa/s, and a one-second record.

Predict these values first:

- sample count: (200);
- samples per cycle: (f_s/f_0=40);
- cycles in the record: (f_0T=5);
- initial I: (cos(\pi/6)=\sqrt3/2);
- initial Q: (sin(\pi/6)=1/2);
- positive phase step: (2\pi f_0/f_s=\pi/20) rad/sample;
- negative phase step: (-\pi/20) rad/sample.

The projection and radius errors should be floating-point roundoff. A larger
error would indicate an implementation mistake, not noise.

## Sweep 1: amplitude changes size

Compare (A=[0.5,1.0,1.5]).

- Predict which IQ circle is largest.
- Confirm that time-domain peak magnitude and IQ radius change together.
- Confirm that samples/cycle and cycles/record do not change.

## Sweep 2: phase changes the starting point

Compare (phi=[0,\pi/4,\pi/2]).

- Predict I and Q at (t=0) for (phi=\pi/2).
- Match each time trace's first value to its IQ starting point.
- Confirm that peak spacing and radius remain unchanged.

## Sweep 3: frequency changes rotation rate

Compare (f=[2.5,5,10]) Hz in the same 0.4-second view.

- Predict 1, 2, and 4 cycles.
- Confirm equal radius and peak magnitude.
- Compare the slopes of accumulated phase versus time.

## Intentionally broken case: undersampling

Turn on **Force the 5 Hz at 8 Sa/s broken case**. The Nyquist limit is only
4 Hz. The signed alias is

\[
f_a=f_0-\operatorname{round}(f_0/f_s)f_s=5-8=-3\text{ Hz}.
\]

For a real cosine, the negative signed alias appears as a positive 3 Hz cosine
with the corresponding phase reversal. The 5 Hz and apparent 3 Hz waveforms
pass through every sampled point, so the samples cannot identify which
continuous waveform produced them.

This is a measurement failure, not a failure of the phasor model. A smooth
line through sparse points is an interpolation assumption, not recovered
information.

## Recovery

Turn off the forced alias case and restore the committed values. At 200 Sa/s,
the 5 Hz tone again has 40 samples/cycle and the baseline predictions hold.
The runtime rejects a record above 5000 samples before allocating it.

## Limiting cases

- At (A=0), all samples are zero, so phase and frequency are unobservable.
  The GUI keeps amplitude positive so every displayed run remains instructive.
- At (f_0=0), the pointer is stationary; I and Q are constants set by
  (A) and (phi).
- Adding (2\pi) to phase returns the same starting point and waveform.
- A negative frequency reverses IQ rotation without changing radius.

## Common mistakes

- Treating phase as a time delay without accounting for frequency:
  (Delta t=-\Delta\phi/(2\pi f_0)).
- Reading a larger IQ circle as faster rotation rather than larger amplitude.
- Inferring direction from an un-ordered circle.
- Counting both (t=0) and (t=T) as distinct samples in a periodic record.
- Believing the apparent 3 Hz curve is a noisy estimate of the 5 Hz curve; it
  is a different waveform that is exactly indistinguishable at 8 Sa/s.

## Completion and teach-back

Before moving on, you should be able to:

- map amplitude to time-domain peak and IQ radius;
- map frequency magnitude to cycles/second and rotation rate;
- map frequency sign to IQ rotation direction;
- map phase to position within the cycle and initial IQ angle;
- explain why the real cosine equals the I-axis projection;
- predict the committed baseline metrics without running the code; and
- explain why 5 Hz and 3 Hz can match at every 8 Sa/s measurement.

Teach it back in two or three sentences without relying on the plot labels.
