## P59 course checkpoint

**Predict and calculate.** Compare prescribed accelerometer-bias correction over the same coast interval and inspect plotted endpoints.

Use `\dot{\delta v}=b_a,\quad \dot{\delta p}=\delta v; \delta v(T)=b_aT,\quad \delta p(T)=b_aT^2/2; b_{\rm residual}=0.05b_a\quad\text{for the declared nominal correction}` with the conventions in the lesson. Work one baseline value by hand before running. The live controls are **Accelerometer bias**, **Coast duration**.

**Collect evidence.** Save the default result, then perform the lesson's two one-variable sweeps separately. Record exact parameters, units, the `response` and `mechanism` plots, and the quantity that discriminates your prediction. Explain what stayed invariant as well as what changed.

**Fault and recovery.** Enable **Enable the intentionally broken case** at the same inputs. Explain which governing term is changed or omitted, show its effect on the actual trajectory, matrix or criterion, then disable it and use **Reset parameters**. Confirm recovery reproduces the baseline rather than merely a more favorable number.

### Expected reasoning

Velocity error is bias times time and position error is half bias times time squared. A five-percent residual bias produces five-percent position error; omitting correction leaves the full drift.

### Model boundary

The model has fixed attitude and does not execute full strapdown navigation.

### Reasoning rubric

1. State the model, units, sign convention and independently worked value.
2. Explain both sweeps using this lesson's governing relation and recorded evidence.
3. Diagnose the actual fault mechanism and exact-input recovery.
4. Defend the stated boundary and link this result to the cumulative portfolio **A-NAVIGATION**.

This is authored self-assessment guidance. No learner completion, score or effectiveness result has been recorded.
