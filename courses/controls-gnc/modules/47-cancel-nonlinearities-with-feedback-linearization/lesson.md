# Cancel Nonlinearities with Feedback Linearization

Feedback linearization cancels a nonlinear drift only to the extent that its model is correct. State is normalized and time is in seconds; the quadratic plant coefficient is 1/s. This regulator integrates the residual nonlinear equation and stops if x reaches 10, so a departure event cannot masquerade as successful tracking.

## Model and equations

\[
\dot{x}=\delta x^2-kx,\qquad \frac{1}{x(t)}=\frac{\delta}{k}+\left(1-\frac{\delta}{k}\right)e^{kt}
\]

`dx/dt=x^2+u; reference=0; x(0)=1`

`u=-(1-mismatch)*x^2-k*x; dx/dt=delta*x^2-k*x`

`1/x(t)=delta/k+(1-delta/k)*exp(k*t)`

Worked example: With mismatch 0.08 and k=2/s, u=−0.92x²−2x and x_dot=0.08x²−2x. Starting at x=1 gives x_dot=−1.92/s. Exact cancellation instead gives x=exp(−2t).

## Baseline workflow

Does a positive tracking gain guarantee convergence for every mismatch and initial state? Use x_dot=x(delta*x−k) to identify the boundary.

Run the default controls, record the metrics, and explain the plotted quantities before changing a setting. Nonlinear cancellation dynamics compares integrated state against the exact-cancellation exponential. The second plot shows actual applied input and uncancelled plant drift separately. Observed duration and departure indicator distinguish a four-second endpoint from an earlier x=10 event.

## Two one-variable sweeps

Increase mismatch from 0.08 to 0.5 and inspect deviation from the ideal exponential. Reset, then increase tracking gain from 2 to 6/s and inspect the stronger local decay. To explore departure, use gain 0.2/s with mismatch 0.5.

## Intentionally broken case

Broken mode adds the estimated drift instead of subtracting it, so delta=2−mismatch. It retains both selected controls. At the default gain it decays slowly; at lower gain it can reach the departure threshold.

## Recovery

Restore the cancellation sign and default controls. Verify the observed duration returns to four seconds and terminal error decreases. Do not interpret a stopped trajectory as a clipped stable plant.

## Limiting cases and invariants

- With mismatch zero, healthy dynamics are exactly x_dot=−kx.
- For delta>0 the nonzero equilibrium x=k/delta separates decay from growth on the positive axis.
- The event threshold bounds this demonstration; it is not an actuator or state constraint implemented by the controller.

## Independent evidence

An independent reciprocal-state solution computes the trajectory and analytic x=10 crossing time. The production model uses event-driven numerical integration. Five retained scenarios cover baseline, each one-variable sweep, fault and exact recovery. Absolute and relative tolerances remain 1e-8. The reference does not import or consume the production result.

## Common mistakes

A linear exponential is only exact when cancellation is exact. A finite plotted endpoint can be a declared termination event rather than a stable final state.

## Teach-back

For k=0.2/s and delta=0.5/s, will x(0)=1 decay? What must accompany the terminal-error metric?

Answer rationale: No: x=1 exceeds k/delta=0.4 and initially grows at 0.3/s. The terminal error must be accompanied by observed duration and departure status; at x=10 the integrator stops before four seconds.

Use the Course checkpoint section to assemble your own evidence. These are authored self-checks, not measured learner outcomes or hardware qualification.
