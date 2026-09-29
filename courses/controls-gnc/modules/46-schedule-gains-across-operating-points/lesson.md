# Schedule Gains Across Operating Points

Gain scheduling uses a finite table of gains across an operating range. Here a normalized first-order plant has input effectiveness g(rho), and ideal feedback makes the decay rate 2/s. The lesson constructs actual table knots, including the endpoint at rho=1, then interpolates between them.

## Model and equations

\[
K(\rho)=(1-\theta)K_i+\theta K_{i+1},\qquad \theta=\frac{\rho-\rho_i}{\rho_{i+1}-\rho_i}
\]

`g(rho)=1+rho^2/2; K_exact(rho)=2/g(rho)`

`K_interp=(1-theta)*K_left+theta*K_right`

`closed-loop bandwidth=g(rho)*K_interp`

Worked example: For rho=0.5, the exact gain is 2/1.125=1.777778/s. With spacing 0.25, rho=0.5 is a knot, so interpolation error there is zero. Between knots the nonlinear reciprocal law generally differs from its secant.

## Baseline workflow

If the selected operating point is already a knot, will the selected bandwidth reveal the worst interpolation error?

Run the default controls, record the metrics, and explain the plotted quantities before changing a setting. Gain table and interpolation displays the exact law, used schedule and sampled knots. Resulting closed-loop bandwidth shows the resulting decay rate across the full operating range. The maximum gain error is measured on the displayed grid, which includes midpoints.

## Two one-variable sweeps

Move operating point from 0.5 to 1 and then to an off-knot value such as 0.6. Reset, then increase grid spacing from 0.25 to 0.5 and inspect between-knot error rather than only the selected metric.

## Intentionally broken case

Broken mode freezes K at its rho=0 value of 2/s. The table remains visible for comparison, but the used gain no longer adapts to the plant.

## Recovery

Restore interpolation, reset spacing and compare knot values with exact gains. Inspect an off-knot value as a separate check.

## Limiting cases and invariants

- Healthy interpolation equals the table exactly at every knot.
- As maximum knot spacing tends to zero, the smooth reciprocal law is recovered.
- The reported grid maximum is sampled evidence, not a rigorous continuous worst-case bound.

## Independent evidence

An independent secant evaluator selects the bracketing interval and computes barycentric interpolation directly. It also checks actual midpoint/grid errors. Five retained scenarios cover baseline, each one-variable sweep, fault and exact recovery. Absolute and relative tolerances remain 1e-8. The reference does not import or consume the production result.

## Common mistakes

Assigning an error proportional to spacing does not measure this table. Zero error at one selected knot says little about the intervals around it.

## Teach-back

Why can the selected bandwidth error be zero while sampled maximum gain error is positive? Which plot shows the missing information?

Answer rationale: The selected point can coincide with a knot. The schedule plot exposes departures between knots, and the bandwidth plot shows their closed-loop effect across rho.

Use the Course checkpoint section to assemble your own evidence. These are authored self-checks, not measured learner outcomes or hardware qualification.
