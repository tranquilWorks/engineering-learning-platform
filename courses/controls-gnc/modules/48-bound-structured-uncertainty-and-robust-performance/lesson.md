# Bound Structured Uncertainty and Robust Performance

Robust stability and sensitivity answer different questions. The uncertain pole rate a varies over a declared interval, and feedback gain K has units 1/s. Sensitivity is a ratio of responses and is dimensionless; an inverse decay rate would instead have units of seconds.

## Model and equations

\[
S(s)=\frac{1}{1+KP(s)}=\frac{s+a}{s+a+K}
\]

`P(s)=1/(s+a); a=1+delta; delta in [-radius,+radius] 1/s`

`S(s)=1/(1+K*P(s))=(s+a)/(s+a+K)`

`closed-loop pole=-(a+K)`

Worked example: At radius 0.3/s and K=1.5/s, a ranges from 0.7 to 1.3/s and the worst decay margin is 2.2/s. For a=1/s at zero frequency, S(0)=1/2.5=0.4. At high frequency, |S| tends to one.

## Baseline workflow

Can a finite, smooth frequency-response curve prove the closed-loop family is stable? Check the pole calculation separately.

Run the default controls, record the metrics, and explain the plotted quantities before changing a setting. Declared uncertainty family plots decay rate over exactly the selected perturbation interval. True sensitivity magnitude plots the maximum over 81 uncertainty samples at each of 160 frequencies from 0.05 to 100 rad/s. Its peak is a sampled finite-band quantity.

The frequency axis is logarithmic so both low-frequency shaping and the high-frequency limit remain visible.

## Two one-variable sweeps

Raise uncertainty radius from 0.3 to 0.9/s and inspect the worst margin. Reset, then increase feedback gain from 1.5 to 4/s and compare stability margins with low-frequency sensitivity.

## Intentionally broken case

Broken mode reverses the feedback sign, replacing a+K by a−K. At default settings the entire family is unstable even though finite-frequency magnitude values can still be computed.

## Recovery

Restore negative feedback and reset both controls. Verify the minimum decay margin is positive before interpreting sensitivity as a stable closed-loop disturbance response.

## Limiting cases and invariants

- Zero uncertainty radius collapses the family to one model.
- As frequency tends to infinity, sensitivity magnitude tends to one.
- An unstable transfer expression is not a bounded-input bounded-output performance certificate; the sampled finite-band peak is not an H-infinity norm.

## Independent evidence

Independent complex transfer-function evaluation checks every sampled frequency and parameter; a separate endpoint formula checks the worst pole margin. Five retained scenarios cover baseline, each one-variable sweep, fault and exact recovery. Absolute and relative tolerances remain 1e-8. The reference does not import or consume the production result.

## Common mistakes

Do not label 1/(decay rate) dimensionless sensitivity. Also do not infer stability from the absence of a singularity on a sampled frequency grid.

## Teach-back

Why does reversing feedback invalidate a robustness claim even when the sensitivity chart contains only finite values?

Answer rationale: The denominator has a right-half-plane pole whenever a−K<0. Sampling on the imaginary axis can produce finite values despite that pole; internal stability is a separate requirement.

Use the Course checkpoint section to assemble your own evidence. These are authored self-checks, not measured learner outcomes or hardware qualification.
