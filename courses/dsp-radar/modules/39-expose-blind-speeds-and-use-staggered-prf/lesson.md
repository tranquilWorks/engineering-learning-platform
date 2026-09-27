# Lesson: a moving target can look stationary to a sampled canceller

## Guiding question

Why can a moving target vanish in an MTI radar?

## Physical mental model

A two-pulse MTI canceller compares the current echo with the previous echo. Stationary clutter repeats from pulse to pulse, so subtraction removes it. A moving target normally rotates in complex phase between pulses, so its two samples do not cancel.

The trap is that phase is circular. If a moving target advances by exactly one whole turn, or any integer number of turns, between pulse samples, the radar sees the same phase twice. The canceller cannot distinguish that sampled sequence from stationary clutter. Motion has not stopped; the sampling schedule has hidden it.

This module extends [P38](../38-implement-a-two-pulse-and-three-pulse-mti-canceller/), where the slow-time subtraction was introduced.

## From velocity to the canceller null

For a monostatic radar with wavelength \(\lambda\), an approaching target at radial velocity \(v\) has Doppler frequency

\[
f_d=\frac{2v}{\lambda}.
\]

With pulse repetition frequency \(f_r\), the phase change from one pulse to the next is

\[
\Delta\phi=2\pi\frac{f_d}{f_r}.
\]

The experiment applies the two-pulse operation directly:

\[
y[n]=x[n]-x[n-1].
\]

For a unit-amplitude complex Doppler sequence, its gain is

\[
|H|=|1-e^{-j\Delta\phi}|=2\left|\sin\left(\pi\frac{f_d}{f_r}\right)\right|.
\]

The normalized plots divide this maximum gain of two out, so their vertical scale runs from zero to one. A null occurs whenever \(f_d=kf_r\), giving blind velocities

\[
v_k=k\frac{\lambda f_r}{2},\qquad k=0,\pm1,\pm2,\ldots
\]

At 10 GHz, \(\lambda\approx0.02998\) m. For the 4.0 kHz primary PRF, the first positive blind speed is about 59.96 m/s. That target's Doppler is 4.0 kHz, exactly one phase revolution per pulse, so every sampled target phasor repeats.

## Why the second PRF recovers the target

The same physical target observed at 5.3 kHz PRF still has 4.0 kHz Doppler, but now its phase increment is \(2\pi(4000/5300)\), not an integer turn. Its samples differ and the subtraction produces a nonzero output.

P39 forms two coherent dwells, applies the canceller within each dwell, normalizes each amplitude, and then uses the larger amplitude (equivalently, an OR of threshold decisions). This fusion is deliberately noncoherent: samples taken with different pulse intervals are not added as though they shared one uniform slow-time grid.

Staggering moves the nonzero blind-speed nulls; it does not remove the zero-velocity notch. Both PRFs must suppress stationary clutter at \(v=0\). It also does not guarantee unlimited coverage: specially related PRFs can share nonzero nulls, and real radar scheduling introduces range ambiguity, dwell-time, transmitter, and processing tradeoffs not modeled here.

## Read the figures in physical order

1. **Blind target in two dwells:** the 4.0 kHz samples repeat modulo 360 degrees and subtract to zero; the 5.3 kHz samples walk and survive.
2. **Velocity response:** each colored curve has regularly spaced nulls. Their spacings differ because blind speed is proportional to PRF.
3. **Detection coverage:** an OR decision succeeds wherever either dwell exceeds the illustrative threshold.
4. **Second-PRF sweep:** only PRF 2 changes while the target remains at the primary blind speed. Reusing 4.0 kHz gives no diversity.
5. **Broken and recovered:** identical PRFs duplicate the same holes; restoring 5.3 kHz separates them.

## Limiting cases and interpretation cautions

- At \(v=0\), the output is zero for every PRF. That is the desired stationary-clutter notch, not a stagger failure.
- Near a null, gain is small rather than abruptly binary. Detection depends on target amplitude, noise, clutter residue, threshold, and integration.
- A null in MTI amplitude is not proof that no target exists. It is a property of the canceller plus sampling schedule.
- PRF changes the blind-speed spacing; it does not change the target's physical Doppler.
- The displayed threshold is pedagogical, not a CFAR design or a probability-of-detection claim.
- The synthetic point-target model omits acceleration, range migration, clutter decorrelation, transmitter limits, and ambiguous-range scheduling.

## Connection to the next concept

P39 treats each PRF dwell separately and combines its evidence. Later pulse-Doppler processing and detection modules will add coherent/noncoherent integration, clutter models, range-Doppler maps, and adaptive thresholds. The durable idea is already visible: diversity helps only when the second observation moves the failure mechanism.

## Interactive lab: Expose Blind Speeds and Use Staggered PRF

**Guiding question:** Why can a moving target vanish in an MTI radar?

Carrier is 10 GHz. Each PRF has a separate 32-pulse coherent dwell with target initial phase 20° and noise RMS 0.02; seed 3901 draws the two noise banks sequentially. The velocity control is a multiple of the primary blind-speed spacing; changing it leaves both PRFs fixed. Responses are normalized by the two-pulse maximum amplitude 2, and fusion takes their maximum. The 0.30 threshold is illustrative and is not a probability-of-detection claim.

### Predict, sweep, explain

Predict the first blind speed at 4.0 kHz and why another 4.0 kHz dwell cannot recover it. Which null remains even with a diverse PRF?

1. Start at the baseline. Change only **Secondary prf khz** from 5.3 to 4.5 kHz. Predict and explain the change using the source equation, then reset.
2. Start at the baseline. Change only **Primary blind speed multiple** from 1 to 0.5 ratio. Predict and explain the change using the source equation, then reset.
3. Enable the broken case. Using 4.0 kHz twice duplicates the same blind-speed holes. A repeated observation supplies no PRF diversity.
4. Recovery: Disable the failure and select 5.3 kHz for the primary first-blind-speed target. The zero-velocity null and possible shared nonzero nulls remain. Restore both controls and disable the toggle to reproduce the selected baseline exactly.

### Focused check and teach-back

Predict the first blind speed at 4.0 kHz and why another 4.0 kHz dwell cannot recover it. Which null remains even with a diverse PRF? Explain your answer using a measured value and units, then describe the failure and the recovery assumption.

### Common mistakes

Using 4.0 kHz twice duplicates the same blind-speed holes. A repeated observation supplies no PRF diversity. Avoid treating a clean seeded demonstration as field performance.

### Scope of this lab

The pinned source lesson above describes the original MATLAB model. This interactive version uses bounded NumPy arrays and the same physical stages, with an independent numerical reference. Vectorized sums and linear convolution replace nested MATLAB accumulation loops without circular wrapping. NumPy seeds are reproducible but are not MATLAB RNG parity. MATLAB figure cleanup and console output become plots and metrics. Line displays retain at most 512 points; heatmaps retain at most 128 columns and 64 rows, while calculations use the full stated arrays. No MATLAB execution, visual/accessibility review, hardware, or learner-effectiveness claim is made.
