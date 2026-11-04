## P40 course checkpoint

**Predict and calculate.** Increase converter bits while keeping sampling jitter fixed and explain any error floor.

Use `Delta=V_FS/2^N; e_j approximately x_dot*delta_t; SNR=20 log10(rms(x)/rms(e))` with the conventions in the lesson. Work one baseline value by hand before running. The live controls are **Converter resolution**, **Peak jitter fraction**.

**Collect evidence.** Save the default result, then perform the lesson's two one-variable sweeps separately. Record exact parameters, units, the `response` and `mechanism` plots, and the quantity that discriminates your prediction. Explain what stayed invariant as well as what changed.

**Fault and recovery.** Enable **Enable the intentionally broken case** at the same inputs. Explain which governing term is changed or omitted, show its effect on the actual trajectory, matrix or criterion, then disable it and use **Reset parameters**. Confirm recovery reproduces the baseline rather than merely a more favorable number.

### Expected reasoning

Quantization error shrinks with code spacing, but timing error depends on waveform slope and jitter. Separate the two error traces before assigning combined SNR improvement to resolution.

### Model boundary

The deterministic jitter and quantizer do not model every ADC error mechanism.

### Reasoning rubric

1. State the model, units, sign convention and independently worked value.
2. Explain both sweeps using this lesson's governing relation and recorded evidence.
3. Diagnose the actual fault mechanism and exact-input recovery.
4. Defend the stated boundary and link this result to the cumulative portfolio **A-DIGITAL**.

This is authored self-assessment guidance. No learner completion, score or effectiveness result has been recorded.
