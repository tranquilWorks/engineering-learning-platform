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


---

## P47 course checkpoint

**Predict and calculate.** Explain an actual departure event when feedback cancellation uses a mismatched nonlinear model.

Use `dx/dt=x^2+u; reference=0; x(0)=1; u=-(1-mismatch)*x^2-k*x; dx/dt=delta*x^2-k*x; 1/x(t)=delta/k+(1-delta/k)*exp(k*t)` with the conventions in the lesson. Work one baseline value by hand before running. The live controls are **Cancellation mismatch**, **Tracking gain**.

**Collect evidence.** Save the default result, then perform the lesson's two one-variable sweeps separately. Record exact parameters, units, the `response` and `mechanism` plots, and the quantity that discriminates your prediction. Explain what stayed invariant as well as what changed.

**Fault and recovery.** Enable **Enable the intentionally broken case** at the same inputs. Explain which governing term is changed or omitted, show its effect on the actual trajectory, matrix or criterion, then disable it and use **Reset parameters**. Confirm recovery reproduces the baseline rather than merely a more favorable number.

### Expected reasoning

Cancellation leaves residual dynamics whose sign can change stability or produce finite escape. Report the event and finite validity interval rather than extending a plotted solution past departure.

### Model boundary

Feedback linearization relies on the modeled input map and valid operating domain.

### Reasoning rubric

1. State the model, units, sign convention and independently worked value.
2. Explain both sweeps using this lesson's governing relation and recorded evidence.
3. Diagnose the actual fault mechanism and exact-input recovery.
4. Defend the stated boundary and link this result to the cumulative portfolio **A-NONLINEAR**.

This is authored self-assessment guidance. No learner completion, score or effectiveness result has been recorded.
