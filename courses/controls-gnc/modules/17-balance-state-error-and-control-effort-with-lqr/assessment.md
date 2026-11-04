## P17 course checkpoint

**Predict and calculate.** Compare state-error and control-effort weights while recording both state history and applied control.

Use `J=\sum(x^TQx+u^TRu); u_k=-Kx_k` with the conventions in the lesson. Work one baseline value by hand before running. The live controls are **Position-error weight**, **Control-effort weight**.

**Collect evidence.** Save the default result, then perform the lesson's two one-variable sweeps separately. Record exact parameters, units, the `response` and `mechanism` plots, and the quantity that discriminates your prediction. Explain what stayed invariant as well as what changed.

**Fault and recovery.** Enable **Enable the source broken case** at the same inputs. Explain which governing term is changed or omitted, show its effect on the actual trajectory, matrix or criterion, then disable it and use **Reset parameters**. Confirm recovery reproduces the baseline rather than merely a more favorable number.

### Expected reasoning

The LQR objective trades state cost against input cost; larger state weight generally changes gains and effort. It does not impose hard actuator constraints unless those constraints are modeled separately.

### Model boundary

Nominal unconstrained LQR is not a saturation or robust guarantee.

### Reasoning rubric

1. State the model, units, sign convention and independently worked value.
2. Explain both sweeps using this lesson's governing relation and recorded evidence.
3. Diagnose the actual fault mechanism and exact-input recovery.
4. Defend the stated boundary and link this result to the cumulative portfolio **A-STATE**.

This is authored self-assessment guidance. No learner completion, score or effectiveness result has been recorded.
