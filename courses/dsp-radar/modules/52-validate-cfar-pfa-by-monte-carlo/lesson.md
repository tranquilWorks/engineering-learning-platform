# Lesson: a requested probability is a model claim to test

## Start with the counted event

False-alarm probability is not “the number of dots that look wrong.” It is a
conditional probability under target absence. This experiment defines one
trial as one valid noise-only cell under test (CUT) plus all `N` reference
cells required by the detector. Every trial therefore contributes exactly one
tested CUT and either zero or one false alarm.

If `K` alarms occur among `M` independently generated trials, the measured
rate is

`Pfa_hat = K / M`.

Edge locations with incomplete stencils are not silently counted as tests.
Targets, sidelobes, and detections near modeled target responses are also
absent, so the numerator is genuinely an H0 false-alarm count.

## The homogeneous reference model

Let each complex noise sample have independent zero-mean Gaussian I and Q
components with total mean power one. Its square-law power

`z = |n|^2`

is exponential with mean one. CA-CFAR averages `N` independent reference
powers,

`p_hat = (1/N) * sum(|r_i|^2, i=1...N)`,

and declares a false alarm when

`z > alpha * p_hat`.

For an independent exponential CUT and references, the exact probability is

`Pfa(alpha,N) = (1 + alpha/N)^(-N)`.

Solving for the multiplier gives

`alpha(N,Pfa) = N * (Pfa^(-1/N) - 1)`.

The script exposes complex-noise generation, the square law, cumulative
training-power sums, arithmetic means, alpha, and every comparison. No CFAR or
probability toolbox object stands between the model and the count.

## Why Monte Carlo does not equal the requested value exactly

Even a correctly calibrated detector produces a random alarm count. For
independent Bernoulli outcomes, a typical standard deviation of the measured
rate is approximately

`sqrt(Pfa*(1-Pfa)/M)`.

The figures report a 95% Wilson interval rather than interpreting every small
difference as detector error. With `p_hat=K/M` and `q=1.96`, its limits are

`[p_hat + q^2/(2M) +/- q*sqrt(p_hat*(1-p_hat)/M + q^2/(4M^2))]`

divided by `1 + q^2/M`. It remains nonzero when `K=0`. The interval quantifies
finite-trial uncertainty conditional on independent stationary trials; it
does not certify the assumed clutter model.

## Read the controlled sweeps

Sweep 1 changes requested `Pfa` while holding the same trial bank, `N=24`, and
the homogeneous model fixed. Alpha is recomputed for each request. The
measured points should track the identity line within ordinary counting
uncertainty, while smaller probabilities show larger relative uncertainty
because fewer alarms are observed.

Sweep 2 changes total independent training count through 8, 16, 24, 32, and
64. Every case uses its own finite-`N` alpha. Under the assumed model all cases
retain the same `Pfa`; more training cells are not supposed to lower the
false-alarm rate when calibration is correct.

Sweep 3 holds requested `Pfa`, `N`, and alpha fixed and changes only the noise
model:

- the reference case has independent exponential powers;
- the correlated-Gaussian case gives every complex cell a shared component,
  so CUT and reference powers move together; and
- the compound-lognormal case multiplies every exponential power by an
  independent, unit-mean, heavy-tailed texture.

The correlated case is conservative here because a high CUT tends to arrive
with a high reference estimate. The heavy-tailed case overspends because an
unusually large CUT texture is not reliably represented by the finite
training mean. Both departures are predictable consequences of model
mismatch, not proof that correlation always helps or every non-Gaussian model
fails in the same direction.

## The deliberately broken scaling

As `N` tends to infinity, finite-`N` alpha approaches the known-noise limit

`alpha_infinity = -log(Pfa)`.

Using that smaller limiting multiplier on a finite random training mean is the
broken implementation. Its exact homogeneous false-alarm probability is

`Pfa_broken = (1 + (-log(Pfa))/N)^(-N)`,

which exceeds the request for finite `N`. Recovery recomputes
`N*(Pfa^(-1/N)-1)` from the actual reference count and reruns the same explicit
comparison. A detector that reports more detections only because it spends
more false alarms has not improved.

## Limiting cases and model boundaries

- As `M` grows, Monte Carlo uncertainty shrinks roughly as `1/sqrt(M)`.
- As `N` grows under independent homogeneous exponential noise, alpha tends
  to `-log(Pfa)` while achieved `Pfa` stays at the request.
- As correlation coefficient tends to zero, the correlated construction
  returns to the independent Gaussian model. As it tends to one, CUT and
  references become nearly the same complex sample and the threshold ratio
  changes radically.
- As log-texture standard deviation tends to zero, the compound model returns
  to exponential power. Stronger texture creates a heavier tail.
- More training cells help represent the background only while they remain
  local and statistically relevant. P46 and P51 showed the geometry failures
  that this isolated noise-only trial deliberately removes.
- A reproducible seed supports audit and rerun; it does not turn simulation
  into measured-clutter, hardware, field, or operational evidence.

## Common interpretation mistakes

1. “Requested `Pfa` is automatically achieved.” It is achieved only for the
   calibrated statistic under its assumptions and correct tested-cell count.
2. “Every plotted cell is a trial.” Only CUTs with complete required
   references and an H0 truth label belong in the denominator.
3. “More training cells should reduce `Pfa`.” Correct recalibration keeps
   `Pfa` fixed; the training count changes alpha and estimate variability.
4. “A narrow interval validates the clutter model.” It quantifies counting
   uncertainty inside the selected model.
5. “Correlated clutter always lowers false alarms.” That direction belongs to
   this shared-component example, not to all correlation structures.

## Connection to the implemented CFAR chain

P45 introduced the explicit CA stencil, P47 separated finite-`N` scaling from
the known-noise limit, and P51 classified adverse scene disagreements. P52
closes Phase 5 by auditing the probability claim itself: define a valid H0
trial, count numerator and denominator, attach uncertainty, compare with exact
homogeneous theory, and then break one assumption at a time.

## Interactive lab: Validate CFAR Pfa by Monte Carlo

**Guiding question:** Does the implemented detector actually achieve the requested false-alarm probability?

The H0 baseline uses 200000 independent trials in blocks of 2000. Each block draws one CUT plus 64 references; selected N uses a prefix. Requested Pfa .01/.003/.001 and N=8/16/24/32/64 sweeps share trials. Wilson intervals use z=1.96 and include zero-count uncertainty. Model mismatch keeps N and alpha fixed: correlated Gaussian samples share a common component with correlation .65, while independent-cell lognormal texture has log standard deviation .9 and unit mean. Trials remain independent across rows. The largest control N is 24 to retain the source random-work ceiling while the reference-count sweep still reaches 64.

### Predict, sweep, explain

Predict how the interval narrows with independent trial count. Why can the exact iid Pfa formula fail for correlated or textured backgrounds without an implementation bug?

1. Start at the baseline. Sweep only **Training count** from 24 to 8 cells. Predict, run, and explain the measured change using the equation; then reset.
2. Start at the baseline. Sweep only **Design Pfa** from 0.001 to 0.003 probability. Predict, run, and explain the measured change using the equation; then reset.
3. Enable the broken case. Using −ln(Pfa) on a finite reference mean raises actual Pfa. A small or zero count is also not evidence of zero operational risk.
4. Recovery: Restore N(Pfa^(−1/N)−1), retain all 200000 independent trials and the interval, and disclose the background model. Disable the toggle for exact finite-N replay. Restore the controls and disable the toggle to reproduce the selected baseline exactly.

### Focused check and teach-back

Predict how the interval narrows with independent trial count. Why can the exact iid Pfa formula fail for correlated or textured backgrounds without an implementation bug? Support your answer with a measured value and units. Explain the failure, the recovery assumption, and what this finite experiment cannot establish.

### Common mistakes

Using −ln(Pfa) on a finite reference mean raises actual Pfa. A small or zero count is also not evidence of zero operational risk. Do not equate seeded crossings with a field detection guarantee.

### Scope of this lab

The source lesson is preserved above. NumPy private seeds reproduce this port, not MATLAB random streams; array draws use NumPy row-major order. Source figure/console presentation becomes labeled plots and metrics. Vectorized arithmetic retains the source equations; the P42 linear convolution and P50 ring convolution are independently checked. All calculations use complete stated arrays; displays may retain at most 512 line points or 128×64 heatmap coordinates, preserving zero and prominent peaks. No MATLAB execution, browser/accessibility review, hardware, or learner-effectiveness claim is made.
