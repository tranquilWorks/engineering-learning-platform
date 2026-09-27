# Lesson: the reference window is a physical assumption

## Start with the picture

CA-CFAR decides whether one cell under test (CUT) is unusually large compared
with nearby reference cells. Guards create a moat around the CUT so energy from
the same target response does not enter the background estimate. Training cells
sample the background beyond that moat. Choosing the window therefore states
three beliefs: how wide a target response can be, how many independent-looking
background samples are needed, and how far the background remains local.

For `T` training cells and `G` guard cells on each side, the stencil is

`T training | G guards | CUT | G guards | T training`.

The physical span from the first leading reference to the last lagging
reference is `(2T + 2G + 1)*Delta_R`, where `Delta_R` is the range-cell spacing.
Increasing either count also excludes `T+G` edge CUTs at each end.

## The operation exposed

Let `z[k] = |x[k]|^2` be square-law power. The two reference sets for CUT `k`
contain offsets `-(G+T):- (G+1)` and `(G+1):(G+T)`. With `N=2T`, CA-CFAR forms

`p_hat[k] = (1/N) * sum(z[i] for i in both reference sets)`

and declares a detection when

`z[k] > alpha(N,Pfa) * p_hat[k]`,

where, for independent homogeneous exponential power samples,

`alpha(N,Pfa) = N * (Pfa^(-1/N) - 1)`.

The script constructs those indices and averages their linear powers directly.
No CFAR toolbox detector hides the stencil or comparison.

## Why too few guards self-mask a target

A matched-filtered target is not confined to one cell. Its mainlobe and
sidelobes occupy neighboring cells. If `G` is narrower than that response,
target energy enters the training sum, raises `p_hat`, and raises the threshold
against the target itself. This is self-masking. In the guard sweep, zero
guards put the broad target response directly into the references; four guards
protect its central mainlobe; ten guards also move the references beyond more
sidelobes.

More guards are not free. They move the nearest background evidence farther
away, enlarge the blind edge region, and can cross a clutter change. A guard
count should cover the expected compressed-pulse response and its material
sidelobes, not merely maximize detection margin in one plot.

## Why too few training cells make a noisy threshold

Even in a constant background, each square-law noise sample fluctuates. The
average of only a few samples fluctuates strongly, so the threshold becomes
jagged from CUT to CUT. More independent homogeneous reference samples reduce
that estimator variance. The finite-`N` scale factor also changes with `N`, so
the script recomputes `alpha` for every training-cell case rather than holding
it fixed.

Do not read one seeded threshold crossing count as a measured false-alarm
probability. P52 performs the repeated homogeneous trials needed for that
claim.

## Why too many training cells stop being local

Variance is only half the problem. A large window averages background power
from a wide range span. Around the script's gradual clutter transition, that
average mixes lower-power and higher-power regions. It becomes smooth but
biased relative to the CUT's actual local mean. The training sweep therefore
shows two different metrics:

- observed threshold roughness in a nearly homogeneous region; and
- deterministic locality error obtained by applying the same stencil to the
  known mean-background curve around the transition.

The first generally falls as `T` grows. The second grows here because a wider
window straddles more of the changing background. Smooth is not synonymous
with correct.

## Contamination is a model failure, not random bad luck

CA-CFAR treats every reference cell as background. In the broken case, a strong
neighbor falls inside the weaker target's nominal training set. One large
reference power dominates the arithmetic mean and masks the weaker CUT. The
demonstration recovers by widening the guard just enough to exclude that known
neighbor, then recomputing the estimate from the original profile.

That recovery teaches geometry; it is not a universal multi-target solution.
A very wide guard can lose locality, and several unknown interferers can still
contaminate the remaining references. Ordered-statistic CFAR in P49 addresses
that failure family more directly.

## Limiting cases and common mistakes

- `G=0`: adjacent target-response energy is treated as background; this is
  valid only when the response truly occupies one cell.
- very large `G`: self-leakage falls, but references become remote and edge
  coverage shrinks.
- very small `T`: the estimate is local but high variance, and `alpha` is
  larger for the same requested `Pfa`.
- very large `T`: the estimate is smooth under homogeneous noise but can smear
  clutter transitions or include other targets.
- averaging in dB is still wrong: CA-CFAR needs an arithmetic average of linear
  power, as established in P45.
- counting all non-target threshold crossings as false alarms is unsafe near a
  deterministic sidelobe; those cells are signal-contaminated, not H0 trials.
- changing `T` without recomputing `alpha` changes the detector design as well
  as the window.

## What this experiment establishes

It establishes deterministic source-level behavior for one synthetic,
square-law, 1-D CA-CFAR scene: guards trade target protection against locality,
and training cells trade estimator variance against locality. It does not
establish performance for correlated receiver cells, measured waveforms,
unknown target extent, real clutter, hardware, or operational radar data.

## Interactive lab: Vary CFAR Guard and Training Cells

**Guiding question:** What happens when the CFAR reference window is too small, too large, or contaminated?

The background rises gradually and has a logistic transition at cell 178. A 35 dB target at cell 88 has a sampled sinc response sinc(offset/5) over ±18 cells; the weak 18 dB target is at cell 138. Guards 0/4/10 isolate self-masking; training counts 4/12/36 use fixed guard 6 for the separate variance/locality sweep. The named contaminated case uses T=12,G=4 regardless of the selected uncontaminated controls; a 32 dB neighbor at cell 126 raises the weak CUT threshold. Recovery uses G=12 on that same contaminated scene. Window span and untested-edge count are explicit.

### Predict, sweep, explain

Predict the effect of larger guards on target leakage, then of more training cells on smoothness and locality. How can a neighbor change detection without changing the CUT?

1. Start at the baseline. Sweep only **Guard cells** from 4 to 0 cells. Predict, run, and explain the measured change using the equation; then reset.
2. Start at the baseline. Sweep only **Training cells** from 12 to 36 cells. Predict, run, and explain the measured change using the equation; then reset.
3. Enable the broken case. The named failure injects the source neighbor at cell 126 into the weak cell 138 reference window (T=12,G=4). Its CUT power is unchanged while its threshold rises.
4. Recovery: At the same contaminated scene, use G=12 and T=12 to exclude that neighbor and recover the weak target. This consumes more edge cells. Disable the toggle to restore the selected uncontaminated baseline. Restore the controls and disable the toggle to reproduce the selected baseline exactly.

### Focused check and teach-back

Predict the effect of larger guards on target leakage, then of more training cells on smoothness and locality. How can a neighbor change detection without changing the CUT? Support your answer with a measured value and units. Explain the failure, the recovery assumption, and what this finite experiment cannot establish.

### Common mistakes

The named failure injects the source neighbor at cell 126 into the weak cell 138 reference window (T=12,G=4). Its CUT power is unchanged while its threshold rises. Do not equate seeded crossings with a field detection guarantee.

### Scope of this lab

The source lesson is preserved above. NumPy private seeds reproduce this port, not MATLAB random streams; array draws use NumPy row-major order. Source figure/console presentation becomes labeled plots and metrics. Vectorized arithmetic retains the source equations; the P42 linear convolution and P50 ring convolution are independently checked. All calculations use complete stated arrays; displays may retain at most 512 line points or 128×64 heatmap coordinates, preserving zero and prominent peaks. No MATLAB execution, browser/accessibility review, hardware, or learner-effectiveness claim is made.
