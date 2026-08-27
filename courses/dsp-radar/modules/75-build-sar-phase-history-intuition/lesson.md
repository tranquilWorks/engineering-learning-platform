# Build SAR Phase-History Intuition

> **Guiding question:** Why does moving one antenna create a large synthetic aperture?

## Guiding question

Why does moving one antenna create a large synthetic aperture?

## One antenna, many spatial samples

Imagine stopping one coherent radar at a sequence of surveyed positions along
a straight line. At every stop it transmits, receives the echo, and preserves
complex I/Q. Those looks were made by one antenna, but they sample the wavefield
across the full track. SAR processing treats the ordered positions as one
synthetic aperture only because their geometry and relative phase remain known.

For platform cross-range position `x_p`, target cross-range `x_t`, and closest
slant range `R_0`, the point-target range is

```text
R(x_p) = sqrt(R_0^2 + (x_p - x_t)^2).
```

The echo's two-way delay and carrier phase are

```text
tau(x_p) = 2 R(x_p) / c,
phi(x_p) = -2 pi f_c tau(x_p) = -4 pi R(x_p) / lambda.
```

The factor of two is the outbound-plus-return path. A range change of only
`lambda/2` therefore turns the complex echo through a full cycle. The script
subtracts one constant reference range before evaluating the phasor; that
rotates every sample by the same constant and leaves all spatial information
unchanged.

## What the raw phase history contains

At each position, the ideal complex fast-time record is modeled as

```text
s(x_p, r) = a(r - R(x_p)) exp(-j 4 pi [R(x_p)-R_ref] / lambda) + n(x_p, r),
```

where `a` is a visible Gaussian range envelope and `n` is seeded complex noise.
The envelope says where the echo arrives in fast time. The complex exponential
says how the carrier phase changes across the aperture. No toolbox simulator or
focuser hides either operation.

Near closest approach, let `u = x_p-x_t` and assume `|u| << R_0`. Then

```text
R(x_p) approximately R_0 + u^2/(2 R_0),
phi_relative(x_p) approximately -2 pi u^2/(lambda R_0).
```

That quadratic term is the visible phase curvature. Its vertex occurs at
`x_p = x_t`. Two targets with the same closest range but different cross-range
coordinates therefore have phase histories with the same basic shape shifted
to different platform positions. That is the key completion idea.

## Why a longer track helps

A short aperture sees only a small arc of the range curve. A longer aperture
observes a larger angular span and more two-way phase turns. In this baseline,
20, 40, and 80 m apertures reveal progressively more of the same curved history
while carrier, target, spatial spacing, and noise model remain fixed. Merely
extending the interval does not change the closest-approach local curvature
`-4*pi/(lambda*R_0)`.

More phase turns are not automatically useful. The spatial samples must be
dense enough that adjacent phase change does not alias, the platform positions
must be known, and the oscillator must stay coherent. The experiment rejects a
reviewed geometry if its largest adjacent phase step reaches `pi` radians.
P79 later treats resolution and aperture/window tradeoffs more fully.

## Coherent path matching

For a candidate target coordinate `x_h`, the script builds the expected unit
phasor `h(x_p; x_h)` from the same range equation and computes

```text
score(x_h) = abs(sum(s_phase(x_p) conj(h(x_p; x_h))))
             / sum(abs(s_phase(x_p))).
```

The L1 magnitude normalizer keeps the score between zero and one when selected
noisy ridge samples have slightly unequal magnitude. This is a transparent
one-dimensional coherent sum, not a black-box SAR image.
When the hypothesized path matches the measured path, conjugate phases cancel
and the terms add in phase. A wrong path leaves residual rotation and partial
cancellation. P77 generalizes this idea into backprojection over image pixels.

## The intentionally broken case

Taking `abs` of each complex aperture sample preserves echo strength but erases
the sign and amount of phase rotation. The magnitude-only record can no longer
distinguish the curved histories. Its best coherent score is small even though
the target is still visibly present in fast time.

Recovery does not invent a correction from magnitudes. It returns to an
unchanged copy of the original complex record and applies the same explicit
path-matched sum. Once phase has truly been discarded in acquisition, it
cannot be reconstructed from magnitude alone.

## Limiting cases and interpretation traps

- **Zero aperture:** repeated looks from one position add SNR but provide no
  cross-range phase history.
- **Target at track center:** the range and relative phase curves are symmetric;
  symmetry does not mean phase is constant.
- **Target shifted in cross-range:** the phase-history vertex shifts with it;
  target range has not necessarily changed.
- **Very distant target or very short aperture:** curvature becomes weak because
  the same lateral displacement changes slant range less.
- **Lower carrier frequency:** wavelength grows, so the same path change creates
  fewer phase turns.
- **Sparse spatial sampling:** wrapped phase may alias even when every individual
  sample is measured perfectly.
- **Magnitude-only data:** the range envelope survives, but coherent cross-range
  discrimination does not.
- **Unknown motion or oscillator phase:** position/phase errors corrupt the path
  match; P80 treats motion error and autofocus.
- **Long aperture:** range migration eventually matters. This module keeps it
  visible but small; P78 treats correction explicitly.
- **Point-target model:** terrain, antenna pattern, reflectivity variation,
  propagation, squint, Earth curvature, and full imaging are outside this slice.

## Dependencies and compatibility

P18 provides I/Q phase, P30 provides two-way delay, P36 provides coherent
phase progression, and P61-P63 provide spatial aperture and steering intuition.
P74 is the ordered prerequisite. The script targets base MATLAB R2016b or newer,
uses a private Park-Miller/Box-Muller noise stream, performs no file/network
I/O, creates five tagged figure groups, caps live storage at 4,000,000
eight-byte value equivalents, and requires no optional toolbox.

## Completion connection

You are ready to continue when you can say: two equal-closest-range targets at
different cross-range coordinates create different aperture-phase histories
because each target's path-length minimum—and therefore its phase-curvature
vertex—occurs at a different platform position.

## Use the Python GUI experiment

The GUI keeps the pinned source's mental model and processing order visible. The **aperture length** control scales the primary source variable around its documented baseline; **secondary stress** isolates the next important effect; the noise control uses a fixed retained seed so reruns are comparable.

### Prediction and sweep 1 — aperture length

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
