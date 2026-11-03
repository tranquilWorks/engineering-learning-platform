## P27 course checkpoint

**Predict and calculate.** Relate damping and natural frequency to overshoot, settling estimates and system-type error.

Use `T(s)=omega_n^2/(s^2+2*zeta*omega_n*s+omega_n^2); M_p=exp(-pi*zeta/sqrt(1-zeta^2)); e_ramp=1/K_v=2*zeta/omega_n` with the conventions in the lesson. Work one baseline value by hand before running. The live controls are **Damping ratio**, **Natural frequency**.

**Collect evidence.** Save the default result, then perform the lesson's two one-variable sweeps separately. Record exact parameters, units, the `response` and `mechanism` plots, and the quantity that discriminates your prediction. Explain what stayed invariant as well as what changed.

**Fault and recovery.** Enable **Enable the intentionally broken case** at the same inputs. Explain which governing term is changed or omitted, show its effect on the actual trajectory, matrix or criterion, then disable it and use **Reset parameters**. Confirm recovery reproduces the baseline rather than merely a more favorable number.

### Expected reasoning

Damping changes the decay envelope and ringing; natural frequency scales time. A four-time-constant rule is an estimate, and an unstable response has no legitimate settling-time certification.

### Model boundary

The displayed second-order model is not a universal transient specification.

### Reasoning rubric

1. State the model, units, sign convention and independently worked value.
2. Explain both sweeps using this lesson's governing relation and recorded evidence.
3. Diagnose the actual fault mechanism and exact-input recovery.
4. Defend the stated boundary and link this result to the cumulative portfolio **A-CLASSICAL**.

This is authored self-assessment guidance. No learner completion, score or effectiveness result has been recorded.
