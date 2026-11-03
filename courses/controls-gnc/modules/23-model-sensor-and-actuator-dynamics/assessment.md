## P23 course checkpoint

**Predict and calculate.** Trace how a sensor lag and actuator lag alter the measured and applied paths separately.

Use `\tau_a\dot u_a+u_a=u_c; \tau_s\dot y_s+y_s=u_a+b_s` with the conventions in the lesson. Work one baseline value by hand before running. The live controls are **Actuator time constant**, **Sensor time constant**.

**Collect evidence.** Save the default result, then perform the lesson's two one-variable sweeps separately. Record exact parameters, units, the `response` and `mechanism` plots, and the quantity that discriminates your prediction. Explain what stayed invariant as well as what changed.

**Fault and recovery.** Enable **Enable the source broken case** at the same inputs. Explain which governing term is changed or omitted, show its effect on the actual trajectory, matrix or criterion, then disable it and use **Reset parameters**. Confirm recovery reproduces the baseline rather than merely a more favorable number.

### Expected reasoning

The controller acts on delayed measurement and drives a lagged actuator. Their phase and amplitude effects occur at different loop locations, so matching time constants does not make them interchangeable.

### Model boundary

The linear lag model omits real sensor faults and actuator constraints beyond its scope.

### Reasoning rubric

1. State the model, units, sign convention and independently worked value.
2. Explain both sweeps using this lesson's governing relation and recorded evidence.
3. Diagnose the actual fault mechanism and exact-input recovery.
4. Defend the stated boundary and link this result to the cumulative portfolio **A-DIGITAL**.

This is authored self-assessment guidance. No learner completion, score or effectiveness result has been recorded.
