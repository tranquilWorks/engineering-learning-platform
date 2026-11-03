## P43 evidence task

Explain why decreasing energy can coexist with switching wells early in the trajectory. What equation would a fabricated phase curve fail?

Before running: Will positive damping force every initial condition toward the +1 m well? Use the phase portrait and the energy barrier at E=0 to justify your prediction.

Collect three records: the default plots and metrics; one change from the stated sweeps with the other control fixed; and the fault followed by restored defaults. Record parameter values and units beside each observation.

Double-well phase portrait plots the integrated x-v trajectory and all three equilibria. Mechanical energy balance compares computed energy with initial energy plus integrated damping work. The mean power metric averages the actual six-second energy change.

### Reasoning rubric

- Model: use `dx/dt=v; dv/dt=x-x^3-c*v` to explain the observed quantity rather than repeating a metric label.
- Evidence: For c=0, mechanical energy is conserved. Show where your plot or numerical record tests this statement.
- Diagnosis: Broken mode negates the selected damping, retaining the selected initial energy. Energy is supplied at +|c|v² rather than dissipated; the growing trajectory is integrated rather than replaced by an exponential sinusoid. Identify the measured consequence in your record.
- Recovery and scope: Restore positive damping and reset both controls. Check energy does not increase and the energy-work residual is small relative to the energy scale. State this limit: Energy decay alone does not establish global convergence to a particular well; the saddle and its invariant set remain.

### Check your explanation

While E is above the zero-energy barrier, crossings are possible even with dissipation. The actual phase curve must satisfy x_dot=v and v_dot=x−x³−cv, with E−E0 equal to accumulated −cv² work.

A complete answer includes the calculation or recurrence, an observed comparison with units, fault/recovery evidence and the stated limitation. Revisit the lesson if the explanation depends only on a changing headline number. This is a self-assessment; no learner score is stored.


---

## P43 course checkpoint

**Predict and calculate.** Distinguish local damping stability, a phase-portrait orbit and global energy behavior.

Use `dx/dt=v; dv/dt=x-x^3-c*v; E=v^2/2-x^2/2+x^4/4; dE/dt=-c*v^2; well characteristic: lambda^2+c*lambda+2=0` with the conventions in the lesson. Work one baseline value by hand before running. The live controls are **Damping**, **Initial energy**.

**Collect evidence.** Save the default result, then perform the lesson's two one-variable sweeps separately. Record exact parameters, units, the `response` and `mechanism` plots, and the quantity that discriminates your prediction. Explain what stayed invariant as well as what changed.

**Fault and recovery.** Enable **Enable the intentionally broken case** at the same inputs. Explain which governing term is changed or omitted, show its effect on the actual trajectory, matrix or criterion, then disable it and use **Reset parameters**. Confirm recovery reproduces the baseline rather than merely a more favorable number.

### Expected reasoning

The double-well potential has several equilibria. Reversing damping changes energy flow and local stability; distance from one well at a single oscillation phase is not a valid stability ranking.

### Model boundary

A finite simulated orbit is not a global Lyapunov proof.

### Reasoning rubric

1. State the model, units, sign convention and independently worked value.
2. Explain both sweeps using this lesson's governing relation and recorded evidence.
3. Diagnose the actual fault mechanism and exact-input recovery.
4. Defend the stated boundary and link this result to the cumulative portfolio **A-NONLINEAR**.

This is authored self-assessment guidance. No learner completion, score or effectiveness result has been recorded.
