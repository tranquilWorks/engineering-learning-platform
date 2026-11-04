## P24 course checkpoint

**Predict and calculate.** Calculate which timing and latency assumptions the software HIL example actually exercises.

Use `u_c=\operatorname{clip}(18(r-x_m)-8v_m,-30,30); v_{k+1}=\alpha v_k+(1-\alpha)u_k/c; u_{applied}=0\;\text{during startup or when command age}\ge T_w` with the conventions in the lesson. Work one baseline value by hand before running. The live controls are **Controller period**, **One-way latency**.

**Collect evidence.** Save the default result, then perform the lesson's two one-variable sweeps separately. Record exact parameters, units, the `response` and `mechanism` plots, and the quantity that discriminates your prediction. Explain what stayed invariant as well as what changed.

**Fault and recovery.** Enable **Enable the source broken case** at the same inputs. Explain which governing term is changed or omitted, show its effect on the actual trajectory, matrix or criterion, then disable it and use **Reset parameters**. Confirm recovery reproduces the baseline rather than merely a more favorable number.

### Expected reasoning

A controller period and one-way latency affect command arrival and sample age. A simulated plant loop can validate its timing model and recovery logic while leaving real buses and devices entirely untested.

### Model boundary

This is software simulation, not physical HIL or a real-time scheduler measurement.

### Reasoning rubric

1. State the model, units, sign convention and independently worked value.
2. Explain both sweeps using this lesson's governing relation and recorded evidence.
3. Diagnose the actual fault mechanism and exact-input recovery.
4. Defend the stated boundary and link this result to the cumulative portfolio **A-REALTIME**.

This is authored self-assessment guidance. No learner completion, score or effectiveness result has been recorded.
