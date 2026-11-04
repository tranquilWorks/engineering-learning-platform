## P66 course checkpoint

**Predict and calculate.** Trace excitation, identified model, redesigned controller and estimator into the held-out stress histories.

Use `A=exp(-a dt), B=b(1-A)/a for normalized xdot=-a x+b u; [Ahat,Bhat]=argmin sum(x_next-Ahat*x-Bhat*u)^2 with rank([x,u])=2; K=(Ahat-exp(-2dt))/Bhat; u=clip((1-Ahat+Bhat*K)/Bhat-K*xhat,-3,3); Pprior=Ahat^2 P+Q; L=Pprior/(Pprior+R); NEES=(x-xhat)^2/P` with the conventions in the lesson. Work one baseline value by hand before running. The live controls are **Plant uncertainty**, **Measurement noise**.

**Collect evidence.** Save the default result, then perform the lesson's two one-variable sweeps separately. Record exact parameters, units, the `response` and `mechanism` plots, and the quantity that discriminates your prediction. Explain what stayed invariant as well as what changed.

**Fault and recovery.** Enable **Enable the intentionally broken case** at the same inputs. Explain which governing term is changed or omitted, show its effect on the actual trajectory, matrix or criterion, then disable it and use **Reset parameters**. Confirm recovery reproduces the baseline rather than merely a more favorable number.

### Expected reasoning

Identification rank must support both fitted coefficients. Stress changes the physical model while the design and estimator use the identified model; each requirement derives from recorded state, covariance or control evidence.

### Model boundary

A scalar synthetic identification/control/estimation loop is not full vehicle dynamics or robust certification.

### Reasoning rubric

1. State the model, units, sign convention and independently worked value.
2. Explain both sweeps using this lesson's governing relation and recorded evidence.
3. Diagnose the actual fault mechanism and exact-input recovery.
4. Defend the stated boundary and link this result to the cumulative portfolio **A-CAP-ID**.

This is authored self-assessment guidance. No learner completion, score or effectiveness result has been recorded.
