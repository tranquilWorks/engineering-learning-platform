## P36 evidence task

At x=0.5 m, v=0.4 m/s, which trace supplies 1.6 m/s², and why does the other show 4? Explain why the fault changes the endpoint without moving a pole.

Before running: Will changing only Nbar move the poles? Predict the final position with Nbar=1/s² before enabling the fault.

Collect three records: the default plots and metrics; one change from the stated sweeps with the other control fixed; and the fault followed by restored defaults. Record parameter values and units beside each observation.

Reference tracking shows position and the one-metre command. Full feedback command compares the acceleration that actually drives the states with the incomplete position-only expression. They differ whenever velocity is nonzero.

### Reasoning rubric

- Model: use `dx/dt=v; dv/dt=u` to explain the observed quantity rather than repeating a metric label.
- Evidence: At zero velocity, the complete and incomplete command expressions coincide. Show where your plot or numerical record tests this statement.
- Diagnosis: Broken mode uses Nbar=1/s² while retaining K and both propagated states. The baseline final-value position becomes 1/8 m even though both poles remain stable. Identify the measured consequence in your record.
- Recovery and scope: Disable broken mode and reset both controls. Check steady tracking error returns to zero and compare the two acceleration traces again. State this limit: A finite plotted endpoint need not equal the exact final value; the DC metric uses the equilibrium.

### Check your explanation

The complete command includes −6v=−2.4 m/s². Nbar changes the forced equilibrium Nbar/k_p; K fixes the characteristic polynomial. A correct explanation separates dynamics from command scale.

A complete answer includes the calculation or recurrence, an observed comparison with units, fault/recovery evidence and the stated limitation. Revisit the lesson if the explanation depends only on a changing headline number. This is a self-assessment; no learner score is stored.


---

## P36 course checkpoint

**Predict and calculate.** Separate state-feedback pole placement from reference prefilter scaling in the actual two-state trajectory.

Use `dx/dt=v; dv/dt=u; u=-k_p*x-k_d*v+Nbar*r; k_p=p1*p2; k_d=p1+p2; Nbar=k_p gives x(infinity)=r` with the conventions in the lesson. Work one baseline value by hand before running. The live controls are **Dominant pole magnitude**, **Second-pole ratio**.

**Collect evidence.** Save the default result, then perform the lesson's two one-variable sweeps separately. Record exact parameters, units, the `response` and `mechanism` plots, and the quantity that discriminates your prediction. Explain what stayed invariant as well as what changed.

**Fault and recovery.** Enable **Enable the intentionally broken case** at the same inputs. Explain which governing term is changed or omitted, show its effect on the actual trajectory, matrix or criterion, then disable it and use **Reset parameters**. Confirm recovery reproduces the baseline rather than merely a more favorable number.

### Expected reasoning

Both position and velocity terms contribute acceleration. Changing only the prefilter moves the equilibrium without moving closed-loop poles, so tracking error and pole stability are different tests.

### Model boundary

A finite endpoint does not equal the analytic final value automatically.

### Reasoning rubric

1. State the model, units, sign convention and independently worked value.
2. Explain both sweeps using this lesson's governing relation and recorded evidence.
3. Diagnose the actual fault mechanism and exact-input recovery.
4. Defend the stated boundary and link this result to the cumulative portfolio **A-STATE**.

This is authored self-assessment guidance. No learner completion, score or effectiveness result has been recorded.
