# Build a closed track with dimensional checks

A useful track is more than a closed-looking picture. Its distance, curvature, heading change and closure errors describe different quantities and must retain their own units. This lesson uses a planar ellipse, not a surveyed circuit.

## Model and equations

Let $x=a\cos\theta$, $y=b\sin\theta$, with $b=0.6a$ and radii in metres. Sample one turn with the selected point count, including both endpoints. Analytic signed curvature is

\[\kappa(\theta)=\frac{ab}{(a^2\sin^2\theta+b^2\cos^2\theta)^{3/2}}\quad[\mathrm{m^{-1}}].\]

The displayed length is the sum of straight chords $\sum\|\mathbf p_{i+1}-\mathbf p_i\|$ in metres. Unwrap the tangent heading $\operatorname{atan2}(y',x')$ before taking its change. The curvature integral uses trapezoidal curvature times chord length and should approach $2\pi$ radians as sampling improves.

The arithmetic **parameter-sample mean curvature** averages uniformly spaced $\theta$ samples, including the repeated endpoint. It is not the arc-length average $2\pi/L$. These two means weight the ellipse differently.

## Baseline workflow

Predict where curvature peaks. With $a=60$ m and $b=36$ m, at $(a,0)$ the curvature is $a/b^2=0.0462963\,\mathrm{m^{-1}}$, corresponding to local radius 21.6 m. Run 181 points. The chord length is about 306.308 m, heading change 360°, and position closure is numerical zero. The integral residual is about $8.93\times10^{-5}$ rad.

Read each metric with its dimensional label: length m, peak and sample-mean curvature 1/m, heading degrees, position residual m and curvature-integral residual rad. The plan-view plot and curvature plot therefore use separate physical axes.

## Two one-variable sweeps

1. Keep point count fixed and change major radius from 60 to 40 m. Similarity predicts length scales by $2/3$, curvature by $3/2$, and total heading remains one turn.
2. Restore radius 60 m and raise the point count from 181 to 301. Chords more closely approximate arc length and the integral residual shrinks. Compare a convergence trend, not exact zero at finite resolution.

## Intentionally broken case

The fault stops the parameter at $1.8\pi$ instead of $2\pi$. The final segment is absent: position closure is about 24.06 m and heading change about 309.55°. No line is secretly inserted to make the course appear closed.

## Recovery

Restore the complete turn with the same radius and point count. Position, heading and integral closure return to the original finite-sampling values.

## Limiting cases and invariants

The internal circle limit sets $b=a=R$. Curvature is exactly $1/R$ and an $n$-segment regular polygon has perimeter $2nR\sin(\pi/n)$, tending to $2\pi R$. Reversing path orientation would reverse signed curvature and heading change. Uniform scaling changes length and curvature inversely but preserves their dimensionless integral.

## Independent evidence

The reference derives chord lengths with a half-angle ellipse identity and curvature directly from the closed form. It generates all five expected signatures independently. Circle, scaling and sample-refinement tests check dimensions and limiting behavior without treating a copied vector as a physical proof.

## Common mistakes

Do not label every metric “1,” confuse heading degrees with the radian curvature integral, or interpret the parameter-sample mean as distance-weighted curvature.

## Teach-back

- Why does scaling the track leave total curvature unchanged? Curvature contributes inverse metres and distance contributes metres.
- Why is the sampled integral not exactly $2\pi$? Chord length and finite quadrature approximate a smooth curve.
- Can a path look nearly closed and still fail? Yes; position and tangent closure are numerical requirements, not visual impressions.

## Formative checks

For a 100 m circle sampled as 100 equal chords, derive the polygon length and curvature before running an internal check. Answer: $20000\sin(\pi/100)$ m and $0.01\,\mathrm{m^{-1}}$. Explain why increasing samples raises chord length toward the circumference while leaving analytic curvature fixed. Then identify which two closure quantities reject the truncated ellipse and state their different units.

This Python-first native lesson is not a source conversion and does not establish a measured-vehicle result.
