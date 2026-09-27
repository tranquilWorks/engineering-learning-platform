# Lesson: the protected failure decides which side controls

## Start with the physical edge

Imagine walking outward in range from quiet ground into a much brighter
clutter region. A CUT close to that boundary can have quiet reference cells on
one side and bright reference cells on the other. There is no single local
background level for the window to average: the two halves describe different
physical regions.

P48 calls lower-index cells the leading/left side and higher-index cells the
lagging/right side. Those names do not decide the result. GO and SO respond to
the larger or smaller estimate regardless of which geometric side contains
the bright region.

## Expose both one-sided estimates

For `T` training cells on each side and `G` guards, the script forms linear
power means

`m_left(k) = (1/T) * sum(z(k-G-T : k-G-1))`

and

`m_right(k) = (1/T) * sum(z(k+G+1 : k+G+T))`.

The CUT and guards do not contribute. Greatest-of and smallest-of CFAR then
select

`m_GO = max(m_left, m_right)`

`m_SO = min(m_left, m_right)`.

The selected mean is multiplied by a detector-specific scale before comparing
it with CUT power. The `max` and `min` are visible in `experiment.m`; no CFAR
toolbox object hides the stencil or decision.

## Equal Pfa requires separate scale factors

Even in homogeneous exponential power, the maximum of two noisy means and the
minimum of those means have different distributions. Reusing one CA-CFAR scale
would make an unfair GO/SO comparison.

Let `X` and `Y` be independent means of `T` unit-mean exponential training
powers. For a candidate multiplier `a`, P48 evaluates

`Pfa_SO(a) = 2 * sum(q_k(a), k = 0...T-1)`

where

`q_k(a) = T^(T+k) * Gamma(T+k) / (Gamma(T) * k! * (2*T+a)^(T+k))`,

and

`Pfa_GO(a) = 2 * (T/(T+a))^T - Pfa_SO(a)`.

A fixed-iteration bisection finds one multiplier for each variant at the same
requested homogeneous `Pfa`. With `T = 12` per side and `Pfa = 1e-3`, GO uses
about `7.0890` and SO uses about `10.4809`. GO's selected estimate is larger,
but its calibrated multiplier is smaller. Therefore it is wrong to claim that
the GO threshold exceeds the SO threshold at every homogeneous sample.

## Why GO protects a clutter rise

Consider a high-clutter CUT just beyond the edge. One reference mean still
looks into low clutter and the other sees high clutter. SO chooses the quiet
side, so its threshold remains much too low for the high-power CUT population.
False alarms rise sharply. GO chooses the bright side and keeps the threshold
tied to the population containing the CUT.

The cost appears for a low-side target just before the rise. GO may let the
bright side control even though the CUT still belongs to low clutter. Its high
threshold can miss that target. “Conservative” means protection against false
alarms, not universal superiority.

## Why SO can preserve a target beside an interferer

In homogeneous clutter, place a strong second target in only one training
half. GO selects that contaminated mean, lifts the threshold, and can mask a
weaker target in the CUT. SO selects the clean half and can preserve the weak
target. This benefit lasts only while one side remains representative. If both
halves are contaminated, or the smaller side is from the wrong clutter
population, SO has no magic protection.

## The deliberately broken comparison

The ordinary 24-cell CA scale is between the correct GO and SO scales. Applying
that shared value to both variants makes GO more conservative than requested
and SO less conservative than requested. A plot that then compares detection
counts is not comparing the same operating point. Recovery calibrates the two
variants separately before interpreting edge or interferer behavior.

A second tempting mistake is to pick SO everywhere because it preserved the
weak target in the one-sided-contamination sweep. At the 12 dB clutter rise,
that choice spends a large number of high-side false alarms. Recovery is not a
claim that GO always wins; it selects GO when clutter-edge false-alarm control
is the protected failure.

## Limiting cases and boundaries

- At zero clutter contrast, there is no physical edge bias. GO and SO still
  have different finite-sample statistics, but separate calibration gives both
  the same homogeneous design `Pfa`.
- As the high/low contrast grows, a high-side SO CUT can compare high CUT power
  with a low-side estimate; its false-alarm probability tends toward one.
- A low-side GO target whose window reaches arbitrarily bright clutter becomes
  increasingly likely to be missed at fixed local SNR.
- As `T` grows without bound in representative homogeneous data, both side
  means approach the true mean and both multipliers approach `-log(Pfa)`.
- More cells do not fix a window that spans two populations. P46's geometry
  lesson still applies.

## What the experiment establishes

This is a deterministic simulated square-law model with independent
exponential background powers, an abrupt two-region mean, isolated baseline
target probes, and a deliberate one-sided training contaminator. It does not
validate rare-event `Pfa`, correlated or measured clutter, fluctuating targets,
2-D CFAR, sidelobes, hardware, or an operational radar.

## Interactive lab: Compare GO-CFAR and SO-CFAR at a Clutter Edge

**Guiding question:** Which side of a changing background should control the threshold?

GO uses max(left mean,right mean); SO uses min. Each side has twelve exponential reference powers. Their different homogeneous Pfa integrals are calibrated separately with bounded bisection. The 240-cell scene has an edge at source cell 121 and a 12 dB step; isolated baseline probes intentionally use background-only references. The 25000-trial contrast sweep puts CUT and right references on the high side. A separate weak 13 dB CUT sweep contaminates one left reference. Target additions in the profile are power additions; the Monte Carlo target is a coherent complex-amplitude addition. These are distinct stated models.

### Predict, sweep, explain

Predict which side of a clutter edge GO protects. Why can the same rule mask a weak target under one-sided contamination, and why does SO need a different alpha?

1. Start at the baseline. Sweep only **Clutter step db** from 12 to 18 dB. Predict, run, and explain the measured change using the equation; then reset.
2. Start at the baseline. Sweep only **Interferer power db** from 20 to 10 dB. Predict, run, and explain the measured change using the equation; then reset.
3. Enable the broken case. Always choosing SO because it preserved one weak target causes excess high-side edge crossings. A shared CA multiplier also fails to give GO and SO the same nominal Pfa.
4. Recovery: Restore statistic-specific calibration and choose GO for the protected edge-false-alarm comparison. Disable the toggle; retain the separate SO advantage under one-sided contamination. Restore the controls and disable the toggle to reproduce the selected baseline exactly.

### Focused check and teach-back

Predict which side of a clutter edge GO protects. Why can the same rule mask a weak target under one-sided contamination, and why does SO need a different alpha? Support your answer with a measured value and units. Explain the failure, the recovery assumption, and what this finite experiment cannot establish.

### Common mistakes

Always choosing SO because it preserved one weak target causes excess high-side edge crossings. A shared CA multiplier also fails to give GO and SO the same nominal Pfa. Do not equate seeded crossings with a field detection guarantee.

### Scope of this lab

The source lesson is preserved above. NumPy private seeds reproduce this port, not MATLAB random streams; array draws use NumPy row-major order. Source figure/console presentation becomes labeled plots and metrics. Vectorized arithmetic retains the source equations; the P42 linear convolution and P50 ring convolution are independently checked. All calculations use complete stated arrays; displays may retain at most 512 line points or 128×64 heatmap coordinates, preserving zero and prominent peaks. No MATLAB execution, browser/accessibility review, hardware, or learner-effectiveness claim is made.
