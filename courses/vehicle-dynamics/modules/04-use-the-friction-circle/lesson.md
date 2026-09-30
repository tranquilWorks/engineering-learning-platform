# Project a Force Request onto the Friction Circle

What should happen to both force components when a combined request exceeds tire capacity?

## Physical model

Assume fixed normal load F_z = 3600 N and friction coefficient μ = 1.05. The isotropic force capacity is C = μF_z = 3780 N. A request is the vector q = (F_x, F_y), with norm Q = √(F_x² + F_y²).

Scale s = min(1, C/Q) for Q > 0; s = 1 for Q = 0. Applied force is s q.

Both components receive the same nonnegative scale. The projection preserves direction and signs while reducing magnitude to the circle when needed. The response uses longitudinal force on x and lateral force on y, both in N, with equal geometric scales. The circle is the capacity boundary, the requested point is the desired force, and the applied vector ends at the feasible allocation.

Requested utilization Q/C may exceed one. Applied utilization must not exceed one for the nominal projection. These are distinct quantities: a high request is not evidence that the nominal applied output violated its constraint.

\[
\mathbf F_{\mathrm{applied}}=\min\!\left(1,\frac{\mu F_z}{\lVert\mathbf F_{\mathrm{request}}\rVert}\right)\mathbf F_{\mathrm{request}}\quad (\lVert\mathbf F_{\mathrm{request}}\rVert>0).
\]

## Worked baseline

At (2800, 3500) N the request magnitude is about 4482.187 N, utilization 1.18576, and scale about 0.843338. The applied components are about (2361.35, 2951.69) N. Their resultant is 3780 N and their ratio remains 2800/3500 = 0.8. Clipping each component independently to ±3780 N would leave this request unchanged and would therefore fail the combined-force limit.

## Predict and sweep

Before moving a control, write a sign and a trend prediction with units. The two sweep panels always show the **nominal** relationship with the other selected input fixed, even while the fault toggle is active. The response panel follows the selected mode. The comparison panel shows both modes at identical inputs; it is not a time sequence of failure and repair.

1. Hold lateral request at 3500 N and vary longitudinal request from −6500 to +6500 N. Predict an odd applied longitudinal component. Outside the feasible region, increasing longitudinal demand reallocates the fixed resultant and reduces the retained lateral component.
2. Hold longitudinal request at 2800 N and vary lateral request through the same range. Predict the analogous lateral-force curve. Compare points inside and outside the circle, checking the resultant rather than testing each component against capacity separately.

## Named broken behavior

The toggle bypasses radial projection and applies the requested vector directly. The default endpoint moves outside the circle, so the applied-utilization check fails. In the comparison chart the projected and unprojected vectors share the same origin and direction. A request inside the circle is a benign case: both modes coincide and the fault cannot be exposed there. Return to the default overloaded request to make the missing constraint observable.

## Exact recovery

Disable the fault without moving either input. Check that the selected response returns to the nominal member of the same-input comparison and explain which governing relation has been restored. Only then use **Reset parameters** to reproduce the worked baseline. Resetting inputs and repairing the model are separate actions; changing both at once prevents a causal comparison.

## Limits and limiting cases

The circle assumes equal longitudinal and lateral capacity, constant μ and fixed normal load. Real tire friction can be anisotropic and load dependent. This is a force allocator, not a brush tire model or proof that every interior request is dynamically achievable. At zero request no direction is defined, but a zero applied vector is well defined. Signed negative force components remain allowed; a norm is always nonnegative.

## Common mistakes

Do not interpret the requested-utilization metric as the applied-utilization verdict. Do not clamp two components independently or add their absolute values: the declared boundary uses Euclidean magnitude.

## Formative checks

Compare requests (2800, 3500), (1000, 1000), and (0, 0) N. For each, predict scale and whether the fault will be visible. For the overloaded request, verify the applied magnitude and component ratio. Explain why rectangular clipping would fail.

Check your reasoning: Only the first request is reduced; the other two have scale one and are benign for the bypass fault. The applied overloaded norm equals 3780 N and direction is preserved. A complete explanation checks a vector invariant and the capacity inequality, including the defined zero-request behavior.

## Teach-back checklist

Explain the declared input convention and governing equation before describing the curve. Reproduce the worked calculation with units, account for both one-variable trends, and identify a discriminating fault test. Finish by naming the specific limiting case above and the physical effects omitted by this model. The embedded Course checkpoint asks for evidence and reasoning; no learner score is stored.

This is deterministic synthetic teaching evidence, **not measured-vehicle** validation, a MATLAB-runtime comparison, or representative-learner acceptance. The original conversion ledger remains historical. This revision verifies the declared native model and its revised fault independently; it does not claim unchanged full-source equivalence.
