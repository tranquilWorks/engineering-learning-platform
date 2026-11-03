## P68 course checkpoint

**Predict and calculate.** Trace each software-HIL verdict to delivered packet timing, dropped commands and expired actuator state.

Use `arrival_tick=source_tick+ceil(latency_ms/20); dt=0.02 s; age=(tick-accepted_source_tick)dt; healthy applied command=0 if age>0.05 s; x_next=exp(-dt)x+(1-exp(-dt))*applied_command; u_source=clip(2(1-x),-3,3)` with the conventions in the lesson. Work one baseline value by hand before running. The live controls are **One-way latency**, **Packet drop fraction**.

**Collect evidence.** Save the default result, then perform the lesson's two one-variable sweeps separately. Record exact parameters, units, the `response` and `mechanism` plots, and the quantity that discriminates your prediction. Explain what stayed invariant as well as what changed.

**Fault and recovery.** Enable **Enable the intentionally broken case** at the same inputs. Explain which governing term is changed or omitted, show its effect on the actual trajectory, matrix or criterion, then disable it and use **Reset parameters**. Confirm recovery reproduces the baseline rather than merely a more favorable number.

### Expected reasoning

A watchdog must suppress actual applied output when a command expires. Distinguish late delivered packets from dropped source commands, and track the proportional-loop equilibrium rather than assuming unity tracking.

### Model boundary

Software event simulation does not measure real buses, operating-system deadlines or physical actuators.

### Reasoning rubric

1. State the model, units, sign convention and independently worked value.
2. Explain both sweeps using this lesson's governing relation and recorded evidence.
3. Diagnose the actual fault mechanism and exact-input recovery.
4. Defend the stated boundary and link this result to the cumulative portfolio **A-CAP-ID**.

This is authored self-assessment guidance. No learner completion, score or effectiveness result has been recorded.
