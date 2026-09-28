# Separate factorial effects from held-out prediction

A four-corner factorial can identify two main effects and their interaction. This lesson uses an explicitly synthetic response surface; its times do not predict a measured vehicle or validate a physical aero/tire setup.

## Model and equations

Coded design factors $x_1,x_2\in\{-1,+1\}$ generate

\[T(x_1,x_2)=90-2a x_1-3t x_2-1.2at x_1x_2\quad[\mathrm{s}].\]

The controls $a,t$ are dimensionless effect scales. Fit $T=\beta_0+\beta_1x_1+\beta_2x_2+\beta_{12}x_1x_2$. The four balanced corners make these columns orthogonal and rank four.

The displayed main effects are **time reductions**, $-2\beta_1$ and $-2\beta_2$, rather than conventional signed high-minus-low changes. The interaction reduction contrast is $-4\beta_{12}$. All three are seconds. Fit residual and held-out residual are also seconds; rank is a count.

Held-out RMS is evaluated at unused interior points $(-0.5,0.25)$, $(0.25,-0.5)$ and $(0.5,0.5)$. No held-out response enters fitting. This checks interpolation of the declared synthetic function, not generalization to a different physical response law.

## Baseline workflow

Predict the coefficient signs with $a=t=1$. The exact coefficients are $(90,-2,-3,-1.2)$ s. At the high/high corner, time is $90-2-3-1.2=83.8$ s. Displayed reductions are 4, 6 and 4.8 s. Fit and unused-point residuals are numerical zero because the chosen basis contains the true synthetic function.

Inspect the four corner responses and residual plot, then explain the rank metric. A perfect residual is only informative together with what data and model produced it.

## Two one-variable sweeps

1. Keep tire scale 1 and reduce aero scale to 0.8. Predict aero reduction 3.2 s and interaction reduction 3.84 s. The tire reduction remains 6 s.
2. Restore aero scale 1 and raise tire scale to 1.15. Predict tire reduction 6.9 s and interaction reduction 5.52 s. Explain why interaction responds to both scales.

## Intentionally broken case

The broken design fits only the diagonal corners $(-1,-1)$ and $(1,1)$ with intercept and two main-effect columns. These data confound the factors and cannot identify an interaction. A minimum-norm least-squares fit has rank two; at baseline it attributes equal 5 s reductions to both factors. The unused-point RMS is about 1.2565 s, even though fitting the two available corners looks convincing.

## Recovery

Restore all four balanced corners and the interaction term. Refit without adding the unused points to training. Baseline coefficients, rank and validation errors must return exactly within the declared numerical tolerance.

## Limiting cases and invariants

A zero effect scale in the internal formula removes that main contribution and its interaction while leaving the other factor. Orthogonal four-corner columns identify four coefficients; two diagonal rows cannot. Held-out points must remain disjoint from training corners. Numerical zero error is expected only because this synthetic model is correctly specified and noiseless.

## Independent evidence

The reference computes Walsh/Hadamard contrast averages instead of solving the production linear system. It separately evaluates the unused points. Five independent signatures and rank/disjointness tests detect the old “held-out” metric that reused a fitted corner.

## Common mistakes

Do not interpret positive reduction as positive high-minus-low time, call an observed synthetic response measured data, or use a training residual as evidence of unseen prediction.

## Teach-back

- Why are diagonal corners confounded? Their factor columns are identical, so separate main effects cannot be distinguished.
- Why can healthy held-out error be zero? The same noiseless bilinear law generates unseen responses and lies in the fitted basis.
- What would physical validation require? Independent measured data, controlled experiments and an appropriate error model; this exercise supplies none of those.

## Formative checks

Calculate the synthetic response at the unused point $(0.5,0.5)$ for unit scales. Answer: $90-1-1.5-0.3=87.2$ s. Explain why evaluating this point provides a different check from predicting the fitted high/high corner. Then show that the diagonal design has identical factor columns and therefore cannot separately identify both effects.

This Python-first native lesson is not a source conversion and does not establish a measured-vehicle result.
