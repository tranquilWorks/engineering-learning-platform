# Compare feasible constant-offset racing lines

This is a bounded family of parallel curves around a closed ellipse. It illustrates consistent geometry and travel-time integration; it is not a general racing-line optimizer with variable apexes, longitudinal acceleration or driver behavior.

## Model and equations

The centerline ellipse has semiaxes 180 m and 90 m. Analytic midpoint arc increments $ds$ and curvature $\kappa$ are sampled at 256 points. For a constant inward normal offset $o$,

\[ds_o=(1-o\kappa)ds,\qquad \kappa_o=\frac{\kappa}{1-o\kappa},\qquad v_o=\sqrt{11.5/\kappa_o}.\]

The lateral limit 11.5 has units m/s². All allowed offsets keep $1-o\kappa>0$. Travel time is

\[T(o)=\sum_i\frac{ds_{o,i}}{v_{o,i}},\qquad J(o)=T(o)+w o^2.\]

The penalty $w$ is in s/m². Its historical parameter id remains `smoothness_weight`, but the visible control correctly says **Offset penalty**: a constant-offset penalty is not a path-smoothness functional. Search 41 candidates inside $[-o_{max},o_{max}]$.

## Baseline workflow

Predict the competition: moving inward shortens distance but increases curvature and reduces local speed. On a circle of radius 100 m with lateral limit 10 m/s², $T=2\pi\sqrt{R/a_y}=19.869$ s. Moving inward by 3 m gives about 19.569 s, before adding a penalty. This worked circular limit separates travel time from objective value.

Run maximum offset 3 m and penalty 0.02 s/m². The chosen ellipse offset is about 2.4 m, line length 856.881 m and travel-time improvement about 0.231 s. The displayed improvement is $T(0)-T(o)$, not the penalized objective improvement. Inspect candidate travel times and the selected curvature profile, then use the stated penalty to explain selection.

## Two one-variable sweeps

1. Keep penalty 0.02 and reduce the corridor bound from 3 to 1 m. The earlier 2.4 m candidate is no longer feasible; compare the chosen boundary margin and time.
2. Restore the 3 m corridor and increase penalty to 0.06 s/m². Predict an offset closer to the centerline. Explain why the lowest unpenalized time need not minimize $J$.

## Intentionally broken case

The fault explicitly injects an out-of-corridor candidate $o=1.2o_{max}$ instead of selecting a feasible result. At the baseline bound this is 3.6 m, giving margin −0.6 m and feasibility excess 0.6 m. This demonstrates rejecting a tempting invalid candidate, not discovering an unconstrained global optimum.

## Recovery

Restore bounded candidate selection with identical controls. The line must return inside the corridor and recover the same baseline time and curvature.

## Limiting cases and invariants

Zero offset reproduces the centerline. A zero-width internal corridor contains only that line. In the circle limit, the offset radius is $R-o$, confirming both geometry relations. Travel time must sum distance divided by **local** speed; total length divided by arithmetic mean speed gives different weighting and is generally wrong.

## Independent evidence

The reference evaluates scalar ellipse quadrature and candidate scores separately from the production array implementation. Five scenarios, the circle formula, corridor limits and direct $\sum ds/v$ checks test the original geometry/time defect.

## Common mistakes

Do not confuse inward-offset sign, travel-time improvement and penalized objective improvement, or call this lateral-only speed estimate a dynamically reachable lap. Lesson 64 adds longitudinal reachability and energy.

## Teach-back

- Why can a shorter path still require lower speed? Inward offset raises curvature and lateral acceleration demand.
- What are the penalty's units? Seconds per square metre, so $wo^2$ can be added to time.
- Why reject the broken candidate even if it is faster? It violates the declared corridor before performance is considered.

## Formative checks

For a 3 m offset with penalty 0.02 s/m², compute the penalty alone. Answer: 0.18 s; this must be added to travel time before selecting a candidate. Explain why the displayed time improvement does not include that penalty. Then verify that a 3.6 m candidate in a 3 m corridor has margin −0.6 m and excess +0.6 m.

This Python-first native lesson is not a source conversion and does not establish a measured-vehicle result.
