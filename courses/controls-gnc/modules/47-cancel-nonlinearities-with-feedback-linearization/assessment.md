## P47 evidence task

For k=0.2/s and delta=0.5/s, will x(0)=1 decay? What must accompany the terminal-error metric?

Before running: Does a positive tracking gain guarantee convergence for every mismatch and initial state? Use x_dot=x(delta*x−k) to identify the boundary.

Collect three records: the default plots and metrics; one change from the stated sweeps with the other control fixed; and the fault followed by restored defaults. Record parameter values and units beside each observation.

Nonlinear cancellation dynamics compares integrated state against the exact-cancellation exponential. The second plot shows actual applied input and uncancelled plant drift separately. Observed duration and departure indicator distinguish a four-second endpoint from an earlier x=10 event.

### Reasoning rubric

- Model: use `dx/dt=x^2+u; reference=0; x(0)=1` to explain the observed quantity rather than repeating a metric label.
- Evidence: With mismatch zero, healthy dynamics are exactly x_dot=−kx. Show where your plot or numerical record tests this statement.
- Diagnosis: Broken mode adds the estimated drift instead of subtracting it, so delta=2−mismatch. It retains both selected controls. At the default gain it decays slowly; at lower gain it can reach the departure threshold. Identify the measured consequence in your record.
- Recovery and scope: Restore the cancellation sign and default controls. Verify the observed duration returns to four seconds and terminal error decreases. Do not interpret a stopped trajectory as a clipped stable plant. State this limit: The event threshold bounds this demonstration; it is not an actuator or state constraint implemented by the controller.

### Check your explanation

No: x=1 exceeds k/delta=0.4 and initially grows at 0.3/s. The terminal error must be accompanied by observed duration and departure status; at x=10 the integrator stops before four seconds.

A complete answer includes the calculation or recurrence, an observed comparison with units, fault/recovery evidence and the stated limitation. Revisit the lesson if the explanation depends only on a changing headline number. This is a self-assessment; no learner score is stored.
