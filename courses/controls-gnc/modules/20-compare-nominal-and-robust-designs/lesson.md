# Compare Nominal and Robust Designs

**Guiding question:** What inputs, observable effects, and failure modes matter when you compare Nominal and Robust Designs?

This platform lesson makes a deliberately narrow comparison: two preselected proportional gains,
$K=2$ and $K=4$, are run against one point in a declared positive actuator-gain/drag family. It is
useful for building robustness intuition, but it is not robust-control synthesis, an optimum over a
continuous uncertainty set, or a certification result.

## Predict before running

At the matched point, predict which fixed gain will settle faster and which will apply more initial
acceleration. Then predict how lower actuator effectiveness or higher drag will change both traces.
Write the mechanism down before moving either control.

## Model and equations

The normalized speed plant is

$$
\dot v=-a v+b u,\qquad
u_K=K(r-v),\qquad K\in\{2,4\},
$$

where $a$ is the selected drag ratio, $b$ is the selected signed actuator-gain ratio, and $r=1\;
\mathrm{m/s}$. Forward Euler with $\Delta t=0.02\;\mathrm{s}$ gives

$$
v_{k+1}=\left[1-\Delta t(a+bK)\right]v_k+\Delta t\,bKr.
$$

For positive $a$, $b$, and $K$, the equilibrium is

$$
v_\infty=\frac{bK}{a+bK}r.
$$

The higher gain generally reduces equilibrium error and speeds the response, but it also raises
initial command. The displayed finite-horizon objective,

$$
J_K=\int_0^{12}\left[(r-v_K)^2+0.05u_K^2\right]dt,
$$

combines tracking and effort for the selected point only. A lower $J_K$ at one point is not a
worst-case guarantee.

## Two one-variable sweeps

1. Hold `drag_ratio=1.0` and sweep `actuator_gain_ratio` through `[0.5, 1.0, 1.5]`.
   Explain the change in closed-loop rate, equilibrium speed, and command.
2. Reset actuator gain to `1.0`, then sweep `drag_ratio` through `[0.5, 1.0, 2.0]`.
   Explain why higher loss increases the residual speed error for both proportional gains.

Do not move both ratios together until you can attribute each change to $a$ or $b$ in the recurrence.

## Intentionally broken case

Broken mode sets $b<0$: positive error produces acceleration in the wrong direction. That polarity
reversal is outside the positive uncertainty family. Both fixed-gain recurrences then grow rather
than support the intended negative-feedback interpretation.

## Recovery

Disable broken mode to restore positive actuator polarity in a fresh deterministic run. Confirm the
recovery in both the bounded speed trace and the finite objective; retuning a controller around an
unverified sign is not a recovery.

## Source-to-platform boundary

The pinned MATLAB source goes further: it compares nominal feedforward-plus-P control with a PI
candidate chosen by finite enumeration over 12 candidates and 25 positive plant points, including
stability and effort screens. This Python lesson does **not** reproduce that design search, PI state,
or its finite-grid result. Those behaviors are explicit omissions owned by the Controls/GNC
curriculum-expansion work; this module may claim only the two-fixed-gain comparison implemented here.

The independent Python reference verifies the displayed recurrence by a closed-form affine solution.
MATLAB runtime, values between or beyond the displayed parameter range, browser rendering, hardware,
and learner effectiveness are not evidence in this lesson.

## Common mistakes

- Calling $K=4$ “robust” without stating the two-gain experiment and positive parameter family.
- Treating one selected plant point or a finite sweep as a continuous uncertainty proof.
- Comparing only final speed while ignoring command effort and the 12-second horizon.
- Treating reversed polarity as merely a larger positive gain error.
- Assuming independent Python agreement means MATLAB was executed.

## Teach-back

In two sentences, identify $a$, $b$, and $K$ in the recurrence and describe the tracking/effort trade.
Then state why the broken sign and the omitted MATLAB design search bound every robustness claim here.
